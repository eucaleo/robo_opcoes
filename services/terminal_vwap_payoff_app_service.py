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
    ) -> None:
        self.structure_repository = structure_repository
        self.market_snapshot_provider = market_snapshot_provider
        self.payoff_provider = payoff_provider
        self.viewmodel_service = viewmodel_service or self._default_viewmodel_service()

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
            "market": dict(market or {}),
            "meta": {
                "source": "terminal_vwap_payoff_app_service",
                "reference_date": reference_date,
            },
        }

        return compute_payoff_from_canonical_input(canonical_input)

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
            return list(payoff)

        if isinstance(payoff, dict):
            points = (
                payoff.get("points")
                or payoff.get("payoff_points")
                or payoff.get("curve")
                or []
            )
            return list(points)

        return []

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
