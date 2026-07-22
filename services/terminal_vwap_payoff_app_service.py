"""App service do Terminal VWAP Payoff.

Incremento 2:
- orquestra estrutura, mercado, payoff e ViewModel;
- usa dependências injetadas para manter teste isolado;
- não acessa Excel, RTD real ou UI pesada diretamente.
"""

from __future__ import annotations

from typing import Any, Callable


class TerminalVWAPPayoffAppService:
    """Orquestra a montagem do ViewModel do Terminal VWAP Payoff.

    O serviço foi desenhado para receber dependências externas injetadas:

    - structure_repository: deve expor get_structure(structure_id) ou similar;
    - market_snapshot_provider: opcional, deve expor get_market_snapshot(...) ou similar;
    - payoff_provider: opcional, deve expor compute_payoff(...) ou similar;
    - viewmodel_service: opcional, por padrão usa TerminalVWAPPayoffViewModelService.

    Isso permite evoluir a integração real depois, sem acoplar o terminal
    diretamente a Excel, RTD, Tkinter ou banco em testes unitários.
    """

    def __init__(
        self,
        *,
        structure_repository: Any | None = None,
        market_snapshot_provider: Any | None = None,
        payoff_provider: Any | None = None,
        viewmodel_service: Any | None = None,
        rtd_leg_enrichment_service: Any | None = None,
        decision_repository: Any | None = None,
    ) -> None:
        self.structure_repository = structure_repository
        self.market_snapshot_provider = market_snapshot_provider
        self.payoff_provider = payoff_provider
        self.viewmodel_service = viewmodel_service or self._default_viewmodel_service()
        self.rtd_leg_enrichment_service = rtd_leg_enrichment_service
        self.decision_repository = decision_repository

    def build_for_structure_id(
        self,
        structure_id: int,
        *,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        """Monta o ViewModel do terminal para uma estrutura canônica."""

        sid = self._validate_structure_id(structure_id)

        structure = self._load_structure(sid)
        if not structure:
            raise ValueError(f"structure not found: {sid}")
        structure = self._with_repository_legs(sid, structure)

        market = self._load_market_snapshot(
            structure_id=sid,
            structure=structure,
            reference_date=reference_date,
        )

        payoff = self._compute_payoff(
            structure=structure,
            market=market,
            reference_date=reference_date,
        )
        payoff_points = self._extract_payoff_points(payoff)

        return self._build_viewmodel(
            structure=structure,
            market=market,
            payoff=payoff,
            payoff_points=payoff_points,
        )

    def list_structures(self, include_archived: bool = True) -> list[dict[str, Any]]:
        """Lista estruturas via repositório injetado, sem acesso direto pela UI."""

        if self.structure_repository is None:
            return []

        result = self._call_first_available(
            self.structure_repository,
            method_names=(
                "list_structures",
                "list_available_structures",
                "listar_estruturas",
            ),
            call_variants=(
                lambda method: method(include_archived=include_archived),
                lambda method: method(include_archived),
                lambda method: method(),
            ),
            default=[],
        )
        return list(result or [])

    def list_decisions(
        self,
        structure_id: int | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Lista decisões da tabela structure_decisions."""

        if self.decision_repository is None:
            return []

        return self._call_first_available(
            self.decision_repository,
            method_names=(
                "list_decisions",
            ),
            call_variants=(
                lambda method: method(
                    structure_id=structure_id,
                    limit=limit,
                ),
                lambda method: method(
                    structure_id,
                    limit,
                ),
                lambda method: method(limit=limit),
                lambda method: method(),
            ),
            default=[],
        ) or []

    @staticmethod
    def _validate_structure_id(structure_id: int) -> int:
        try:
            sid = int(structure_id)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"structure_id must be positive integer: {structure_id!r}") from exc

        if sid <= 0:
            raise ValueError(f"structure_id must be positive integer: {structure_id!r}")

        return sid

    @staticmethod
    def _default_viewmodel_service() -> Any:
        from services.terminal_vwap_payoff_viewmodel_service import (
            TerminalVWAPPayoffViewModelService,
        )

        return TerminalVWAPPayoffViewModelService()

    def _load_structure(self, structure_id: int) -> dict[str, Any] | None:
        if self.structure_repository is None:
            raise ValueError("structure_repository is required")

        return self._call_first_available(
            self.structure_repository,
            method_names=(
                "get_structure",
                "get_by_id",
                "fetch_structure",
                "load_structure",
            ),
            call_variants=(
                lambda method: method(structure_id),
                lambda method: method(structure_id=structure_id),
            ),
        )


    def _with_repository_legs(self, structure_id: int, structure: dict[str, Any]) -> dict[str, Any]:
        """Enriquece a estrutura com legs vindas do repositório, quando disponíveis.

        A UI não busca dados vivos aqui. Este método apenas monta a estrutura
        operacional usando dados já persistidos/servidos pelo backend/repositórios.
        """
        if not isinstance(structure, dict):
            return structure

        existing_legs = structure.get("legs")
        if isinstance(existing_legs, list) and existing_legs:
            return structure

        repository = self.structure_repository
        if repository is None:
            return structure

        candidate_methods = (
            "get_structure_legs",
            "list_structure_legs",
            "get_legs",
            "list_legs",
            "get_legs_by_structure_id",
            "list_legs_by_structure_id",
            "fetch_structure_legs",
        )

        legs = None

        for method_name in candidate_methods:
            method = getattr(repository, method_name, None)
            if not callable(method):
                continue

            call_attempts = (
                lambda: method(structure_id),
                lambda: method(structure_id=structure_id),
            )

            for call in call_attempts:
                try:
                    result = call()
                except TypeError:
                    continue
                except Exception:
                    continue

                if result:
                    legs = result
                    break

            if legs:
                break

        if not legs:
            return structure

        normalized_legs = []
        for leg in legs:
            if isinstance(leg, dict):
                normalized_legs.append(dict(leg))
                continue

            if hasattr(leg, "_asdict"):
                normalized_legs.append(dict(leg._asdict()))
                continue

            if hasattr(leg, "__dict__"):
                normalized_legs.append(
                    {
                        key: value
                        for key, value in vars(leg).items()
                        if not key.startswith("_")
                    }
                )
                continue

            normalized_legs.append(leg)

        normalized_legs = self._enrich_repository_legs_from_rtd(normalized_legs)

        enriched = dict(structure)
        enriched["legs"] = normalized_legs
        return enriched


    def _enrich_repository_legs_from_rtd(
        self,
        legs: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Aplica enriquecimento RTD injetado às legs da estrutura.

        O app service não acessa Excel/RTD real. Ele apenas usa um serviço
        injetado, geralmente baseado em rtd_option_quotes já persistido.
        """

        service = self.rtd_leg_enrichment_service
        if service is None:
            return legs

        for method_name in (
            "enrich_legs",
            "enrich_many",
            "enrich_structure_legs",
        ):
            method = getattr(service, method_name, None)
            if not callable(method):
                continue

            call_attempts = (
                lambda: method(
                    legs,
                    strict=False,
                    apply_live_price=True,
                ),
                lambda: method(legs),
            )

            for call in call_attempts:
                try:
                    result = call()
                except TypeError:
                    continue
                except Exception:
                    return legs

                if isinstance(result, list):
                    return result

        enriched: list[dict[str, Any]] = []
        for leg in legs:
            if not isinstance(leg, dict):
                enriched.append(leg)
                continue

            current = dict(leg)
            for method_name in ("enrich_live_market_fields", "enrich"):
                method = getattr(service, method_name, None)
                if not callable(method):
                    continue

                try:
                    current = method(current)
                    break
                except Exception:
                    continue

            enriched.append(current)

        return enriched

    def _load_market_snapshot(
        self,
        *,
        structure_id: int,
        structure: dict[str, Any],
        reference_date: str | None,
    ) -> dict[str, Any]:
        if self.market_snapshot_provider is None:
            return {}

        result = self._call_first_available(
            self.market_snapshot_provider,
            method_names=(
                "get_market_snapshot",
                "get_snapshot_for_structure",
                "get_snapshot",
                "get_market_for_structure",
                "get_market",
            ),
            call_variants=(
                lambda method: method(
                    structure_id=structure_id,
                    structure=structure,
                    reference_date=reference_date,
                ),
                lambda method: method(structure_id=structure_id, structure=structure),
                lambda method: method(structure_id, structure),
                lambda method: method(structure_id),
                lambda method: method(structure),
            ),
            default={},
        )

        return dict(result or {})

    def _compute_payoff(
        self,
        *,
        structure: dict[str, Any],
        market: dict[str, Any],
        reference_date: str | None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        if self.payoff_provider is not None:
            return self._call_first_available(
                self.payoff_provider,
                method_names=(
                    "compute_payoff",
                    "build_payoff",
                    "calculate_payoff",
                    "get_payoff",
                ),
                call_variants=(
                    lambda method: method(
                        structure=structure,
                        market=market,
                        reference_date=reference_date,
                    ),
                    lambda method: method(structure=structure, market=market),
                    lambda method: method(structure, market),
                    lambda method: method(structure),
                ),
                default={},
            )

        from domain.payoff import compute_payoff_from_canonical_input

        canonical_input = {
            "structure": self._normalize_structure_for_payoff(structure),
            "market": self._normalize_market_for_payoff(market),
            "meta": {
                "source": "terminal_vwap_payoff_app_service",
                "reference_date": reference_date,
            },
        }

        return compute_payoff_from_canonical_input(canonical_input)


    @staticmethod
    def _normalize_market_for_payoff(market: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(market or {})

        if "spot_price" not in normalized or normalized.get("spot_price") in (None, ""):
            for key in (
                "spot_price",
                "current_price",
                "underlying_price",
                "last_price",
                "preco_atual",
            ):
                value = normalized.get(key)
                if value not in (None, ""):
                    normalized["spot_price"] = value
                    break

        if "underlying_asset" not in normalized:
            for key in ("asset", "ticker", "ativo", "ativo_base"):
                value = normalized.get(key)
                if value not in (None, ""):
                    normalized["underlying_asset"] = value
                    break

        return normalized

    @staticmethod
    def _normalize_structure_for_payoff(structure: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(structure or {})
        normalized_legs = []

        for index, raw_leg in enumerate(normalized.get("legs") or [], start=1):
            leg = dict(raw_leg or {})

            if "premium" not in leg:
                leg["premium"] = (
                    leg.get("valor_executado")
                    or leg.get("premio")
                    or leg.get("prêmio")
                    or 0.0
                )

            if "option_type" not in leg and "call_put" in leg:
                leg["option_type"] = leg.get("call_put")

            if "position_side" not in leg:
                leg["position_side"] = (
                    leg.get("side")
                    or leg.get("cv")
                    or leg.get("position")
                    or "COMPRADO"
                )

            if "leg_order" not in leg:
                leg["leg_order"] = index

            if "multiplier" not in leg:
                leg["multiplier"] = 1.0

            normalized_legs.append(leg)

        normalized["legs"] = normalized_legs
        return normalized

    @staticmethod
    def _extract_payoff_points(
        payoff: dict[str, Any] | list[dict[str, Any]] | None,
    ) -> list[dict[str, Any]]:
        if payoff is None:
            return []

        if isinstance(payoff, list):
            raw_points = payoff
        elif isinstance(payoff, dict):
            raw_points = (
                payoff.get("points")
                or payoff.get("payoff_points")
                or payoff.get("curve")
                or []
            )
        else:
            raw_points = []

        points: list[dict[str, Any]] = []
        for point in raw_points:
            normalized = TerminalVWAPPayoffAppService._normalize_payoff_point(point)
            if normalized is not None:
                points.append(normalized)

        return points

    @staticmethod
    def _normalize_payoff_point(point: Any) -> dict[str, Any] | None:
        if isinstance(point, dict):
            normalized = dict(point)

            x_value = (
                normalized.get("spot")
                if normalized.get("spot") is not None
                else normalized.get("underlying_price")
            )
            if x_value is None:
                x_value = normalized.get("price")
            if x_value is None:
                x_value = normalized.get("x")

            y_value = (
                normalized.get("pl")
                if normalized.get("pl") is not None
                else normalized.get("result")
            )
            if y_value is None:
                y_value = normalized.get("payoff")
            if y_value is None:
                y_value = normalized.get("profit_loss")
            if y_value is None:
                y_value = normalized.get("y")

            if x_value is not None:
                normalized.setdefault("spot", x_value)
                normalized.setdefault("underlying_price", x_value)

            if y_value is not None:
                normalized.setdefault("pl", y_value)
                normalized.setdefault("result", y_value)

            return normalized

        if isinstance(point, (tuple, list)) and len(point) >= 2:
            x_value = point[0]
            y_value = point[1]
            return {
                "spot": x_value,
                "pl": y_value,
                "underlying_price": x_value,
                "result": y_value,
            }

        return None

    def _build_viewmodel(
        self,
        *,
        structure: dict[str, Any],
        market: dict[str, Any],
        payoff: dict[str, Any] | list[dict[str, Any]],
        payoff_points: list[dict[str, Any]],
    ) -> dict[str, Any]:
        service = self.viewmodel_service

        method = None
        for method_name in (
            "build",
            "build_terminal_vwap_payoff_viewmodel",
            "build_viewmodel",
        ):
            candidate = getattr(service, method_name, None)
            if callable(candidate):
                method = candidate
                break

        if method is None and callable(service):
            method = service

        if method is None:
            raise ValueError("viewmodel_service does not expose a build method")

        return self._call_viewmodel_builder(
            method,
            structure=structure,
            market=market,
            payoff=payoff,
            payoff_points=payoff_points,
        )

    @staticmethod
    def _call_viewmodel_builder(
        method: Callable[..., dict[str, Any]],
        *,
        structure: dict[str, Any],
        market: dict[str, Any],
        payoff: dict[str, Any] | list[dict[str, Any]],
        payoff_points: list[dict[str, Any]],
    ) -> dict[str, Any]:
        call_attempts = (
            lambda: method(
                structure=structure,
                market=market,
                payoff=payoff,
                payoff_points=payoff_points,
            ),
            lambda: method(
                structure=structure,
                market=market,
                payoff_points=payoff_points,
            ),
            lambda: method(
                structure=structure,
                market_snapshot=market,
                payoff_points=payoff_points,
            ),
            lambda: method(structure, market, payoff_points),
        )

        last_type_error: TypeError | None = None

        for attempt in call_attempts:
            try:
                return attempt()
            except TypeError as exc:
                last_type_error = exc

        raise last_type_error or TypeError("unable to call viewmodel builder")

    @staticmethod
    def _call_first_available(
        target: Any,
        *,
        method_names: tuple[str, ...],
        call_variants: tuple[Callable[[Callable[..., Any]], Any], ...],
        default: Any = None,
    ) -> Any:
        for method_name in method_names:
            method = getattr(target, method_name, None)
            if not callable(method):
                continue

            last_type_error: TypeError | None = None
            for variant in call_variants:
                try:
                    return variant(method)
                except TypeError as exc:
                    last_type_error = exc

            if last_type_error is not None:
                raise last_type_error

        return default
