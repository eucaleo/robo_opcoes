"""ViewModel do Terminal VWAP Payoff.

Este módulo monta um payload puro para a futura UI do Terminal VWAP Payoff.

Premissas:
- não acessa Excel;
- não acessa RTD real;
- não acessa banco diretamente;
- recebe dados já carregados por serviços/repositórios existentes;
- retorna um dicionário estável para consumo pela UI.
"""

from __future__ import annotations

from typing import Any


class TerminalVWAPPayoffViewModelService:
    """Monta o ViewModel canônico do Terminal VWAP Payoff."""

    def build(
        self,
        *,
        structure: Any,
        market_snapshot: Any | None = None,
        payoff_points: list[Any] | None = None,
        meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Retorna um ViewModel consolidado para a UI.

        Args:
            structure: estrutura canônica ou objeto similar.
            market_snapshot: snapshot de mercado já resolvido.
            payoff_points: pontos de payoff já calculados.
            meta: metadados adicionais da chamada.

        Returns:
            dict com blocos: terminal, structure, market, legs, payoff, meta.
        """

        normalized_structure = self._normalize_structure(structure)
        normalized_legs = [
            self._normalize_leg(leg, index=index)
            for index, leg in enumerate(
                self._get(structure, "legs", default=[]) or [],
                start=1,
            )
        ]

        normalized_market = self._normalize_market(market_snapshot)
        normalized_payoff = self._normalize_payoff(payoff_points or [])

        return {
            "terminal": {
                "name": "ui-terminal-vwap-payoff",
                "version": 1,
                "ready": True,
            },
            "structure": normalized_structure,
            "market": normalized_market,
            "legs": normalized_legs,
            "payoff": normalized_payoff,
            "meta": {
                "source": "terminal_vwap_payoff_viewmodel_service",
                "input_meta": meta or {},
                "warnings": self._build_warnings(
                    structure=normalized_structure,
                    market=normalized_market,
                    legs=normalized_legs,
                    payoff=normalized_payoff,
                ),
            },
        }

    def _normalize_structure(self, structure: Any) -> dict[str, Any]:
        structure_id = self._get(
            structure,
            "structure_id",
            "id",
            default=None,
        )

        return {
            "structure_id": structure_id,
            "name": self._get(structure, "name", "nome", default=None),
            "underlying_asset": self._get(
                structure,
                "underlying_asset",
                "ativo_objeto",
                "asset",
                "ticker",
                default=None,
            ),
            "status": self._get(structure, "status", default=None),
        }

    def _build_leg_viewmodel(self, leg: Any, *, index: int) -> dict[str, Any]:
        """Compatibilidade com consumidores do contrato anterior.

        Delega para a normalização canônica da leg, preservando a separação
        entre ``premium`` (preço de entrada) e ``current_price`` (RTD).
        """
        return self._normalize_leg(leg, index=index)

    def _normalize_leg(self, leg: Any, *, index: int) -> dict[str, Any]:
        symbol = self._get(
            leg,
            "symbol",
            "asset",
            "ativo",
            "codigo_opcao",
            default=None,
        )

        quantity = self._to_float(
            self._get(leg, "quantity", "quant", "qty", default=None)
        )

        premium = self._to_float(
            self._get(
                leg,
                "premium",
                "price",
                "valor_executado",
                "mid",
                "preco",
                default=None,
            )
        )

        strike = self._to_float(
            self._get(leg, "strike", "preco_exercicio", default=None)
        )

        # Preço de mercado da opção, independente do prêmio de entrada.
        # A prioridade segue o contrato RTD adotado no enrichment service.
        current_price = self._to_float(
            self._get(
                leg,
                "current_price",
                "ultimo_preco",
                "last_price",
                "price",
                default=None,
            )
        )

        return {
            "leg_order": self._get(leg, "leg_order", default=index),
            "symbol": symbol,
            "position_side": self._get(
                leg,
                "position_side",
                "side",
                "cv",
                default=None,
            ),
            "option_type": self._get(
                leg,
                "option_type",
                "call_put",
                "tipo",
                default=None,
            ),
            "quantity": quantity,
            "premium": premium,
            "current_price": current_price,
            "strike": strike,
            "expiration_date": self._get(
                leg,
                "expiration_date",
                "expiry",
                "vencimento",
                default=None,
            ),
            "source": self._get(leg, "source", "fonte", default=None),
        }

    def _normalize_market(self, market_snapshot: Any | None) -> dict[str, Any]:
        current_price = self._to_float(
            self._get(
                market_snapshot,
                "current_price",
                "spot_price",
                "underlying_price",
                "last_price",
                "preco_atual",
                default=None,
            )
        )

        vwap = self._to_float(
            self._get(
                market_snapshot,
                "vwap",
                "VWAP",
                "quote_vwap",
                default=None,
            )
        )

        difference = None
        if current_price is not None and vwap not in (None, 0):
            difference = ((current_price - vwap) / vwap) * 100

        return {
            "current_price": current_price,
            "vwap": vwap,
            "price_vs_vwap_percent": difference,
            "status_vwap": "available" if vwap is not None else "unavailable",
            "source": self._get(
                market_snapshot,
                "source",
                "snapshot_source",
                "fonte",
                default=None,
            ),
            "timestamp": self._get(
                market_snapshot,
                "timestamp",
                "updated_at",
                "data_hora",
                default=None,
            ),
        }

    def _normalize_payoff(self, payoff_points: list[Any]) -> dict[str, Any]:
        points = []

        for point in payoff_points:
            x_value = self._to_float(
                self._get(
                    point,
                    "underlying_price",
                    "price",
                    "spot",
                    "x",
                    default=None,
                )
            )

            y_value = self._to_float(
                self._get(
                    point,
                    "result",
                    "payoff",
                    "pl",
                    "profit_loss",
                    "y",
                    default=None,
                )
            )

            if x_value is None or y_value is None:
                continue

            points.append(
                {
                    "underlying_price": x_value,
                    "result": y_value,
                }
            )

        results = [point["result"] for point in points]

        return {
            "points": points,
            "points_count": len(points),
            "min_result": min(results) if results else None,
            "max_result": max(results) if results else None,
            "break_even_points": self._estimate_break_even_points(points),
        }

    def _estimate_break_even_points(
        self,
        points: list[dict[str, float]],
    ) -> list[float]:
        if len(points) < 2:
            return []

        ordered = sorted(points, key=lambda item: item["underlying_price"])
        break_evens: list[float] = []

        previous = ordered[0]

        if previous["result"] == 0:
            break_evens.append(previous["underlying_price"])

        for current in ordered[1:]:
            previous_x = previous["underlying_price"]
            previous_y = previous["result"]
            current_x = current["underlying_price"]
            current_y = current["result"]

            if current_y == 0:
                break_evens.append(current_x)
            elif (previous_y < 0 < current_y) or (previous_y > 0 > current_y):
                denominator = current_y - previous_y
                if denominator != 0:
                    ratio = -previous_y / denominator
                    estimated_x = previous_x + ratio * (current_x - previous_x)
                    break_evens.append(estimated_x)

            previous = current

        return break_evens

    def _build_warnings(
        self,
        *,
        structure: dict[str, Any],
        market: dict[str, Any],
        legs: list[dict[str, Any]],
        payoff: dict[str, Any],
    ) -> list[str]:
        warnings = []

        if structure.get("structure_id") is None:
            warnings.append("structure_id ausente")

        if not legs:
            warnings.append("estrutura sem legs")

        if market.get("current_price") is None:
            warnings.append("preço atual ausente")

        if market.get("vwap") is None:
            warnings.append("vwap ausente")

        if payoff.get("points_count") == 0:
            warnings.append("payoff sem pontos")

        return warnings

    def _get(self, source: Any, *keys: str, default: Any = None) -> Any:
        if source is None:
            return default

        for key in keys:
            if isinstance(source, dict) and key in source:
                return source[key]

            if hasattr(source, key):
                return getattr(source, key)

        return default

    def _to_float(self, value: Any) -> float | None:
        if value is None:
            return None

        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            normalized = value.strip()

            if not normalized:
                return None

            normalized = normalized.replace("R$", "").replace("%", "").strip()

            if "," in normalized and "." in normalized:
                normalized = normalized.replace(".", "").replace(",", ".")
            elif "," in normalized:
                normalized = normalized.replace(",", ".")

            try:
                return float(normalized)
            except ValueError:
                return None

        return None
