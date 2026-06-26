from typing import Any

from domain.payoff import compute_payoff_curve_from_canonical_legs
from domain.position_side import to_pricing_engine_side


class PayoffPricingEngine:
    """
    Motor financeiro inicial baseado na curva de payoff canônica.

    Objetivo:
    - substituir o motor stub no fluxo real;
    - manter o contrato de saída esperado por PricingExecutionService;
    - gerar métricas financeiras não nulas quando houver dados suficientes;
    - não depender ainda de Black-Scholes.
    """

    engine_name = "payoff_pricing_engine"

    def run(self, pricing_payload: dict[str, Any]) -> dict[str, Any]:
        if not pricing_payload:
            raise ValueError("pricing_payload is required")

        legs = pricing_payload.get("legs") or []
        if not legs:
            raise ValueError("pricing_payload.legs is required")

        spot_price = float(pricing_payload.get("spot_price") or 0.0)
        if spot_price <= 0:
            raise ValueError("pricing_payload.spot_price is required")

        if self._is_static_market_snapshot(pricing_payload):
            raise ValueError(
                "pricing_payload.spot_price veio de static_fallback; "
                "informe um snapshot real/atual antes de calcular PL atual"
            )

        normalized_legs = [self._normalize_leg(leg) for leg in legs]

        total_quantity = sum(
            int(float(leg.get("quantity") or 0))
            for leg in normalized_legs
        )
        number_of_legs = len(normalized_legs)

        payoff = compute_payoff_curve_from_canonical_legs(
            legs=normalized_legs,
            spot_ref=spot_price,
            low_pct=0.5,
            high_pct=1.5,
            step_pct=0.01,
        )

        pl_max = payoff.get("pl_max")
        pl_min = payoff.get("pl_min")
        pl_atual = self._compute_pl_at_spot(
            legs=normalized_legs,
            spot_price=spot_price,
        )

        premium_paid = self._compute_net_premium_paid(normalized_legs)

        max_profit = pl_max
        max_loss = pl_min

        return {
            "engine": self.engine_name,
            "status": "ok",
            "structure_id": pricing_payload.get("structure_id"),
            "underlying_asset": pricing_payload.get("underlying_asset"),
            "reference_date": pricing_payload.get("reference_date"),
            "metrics": {
                "number_of_legs": number_of_legs,
                "total_quantity": total_quantity,
                "spot_price": spot_price,
                "interest_rate": float(pricing_payload.get("interest_rate") or 0.0),
                "volatility": float(pricing_payload.get("volatility") or 0.0),
                "payoff_points": len(payoff.get("points") or []),
                "pl_max": pl_max,
                "pl_min": pl_min,
                "pl_atual": pl_atual,
            },
            "valuation": {
                "theoretical_value": pl_atual,
                "premium_paid": premium_paid,
                "max_profit": max_profit,
                "max_loss": max_loss,
                "pl_max": pl_max,
                "pl_min": pl_min,
                "pl_atual": pl_atual,
                "method": "expiration_payoff_grid",
            },
            "payoff": payoff,
        }

    @staticmethod
    def _is_static_market_snapshot(pricing_payload: dict[str, Any]) -> bool:
        meta = pricing_payload.get("meta") or {}
        input_meta = pricing_payload.get("input_meta") or {}

        source = str(
            pricing_payload.get("market_snapshot_source")
            or pricing_payload.get("snapshot_source")
            or meta.get("market_snapshot_source")
            or meta.get("snapshot_source")
            or input_meta.get("market_snapshot_source")
            or input_meta.get("snapshot_source")
            or ""
        ).strip().lower()

        explicit_static_flag = any(
            bool(value)
            for value in [
                pricing_payload.get("is_static_fallback"),
                pricing_payload.get("market_is_static_fallback"),
                meta.get("is_static_fallback"),
                meta.get("market_is_static_fallback"),
                input_meta.get("is_static_fallback"),
                input_meta.get("market_is_static_fallback"),
            ]
        )

        return explicit_static_flag or source == "static_fallback"

    @staticmethod
    def _normalize_leg(leg: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(leg)

        side = (
            normalized.get("position_side")
            or normalized.get("side")
            or normalized.get("direction")
        )
        normalized["position_side"] = to_pricing_engine_side(side)

        normalized["option_type"] = str(
            normalized.get("option_type")
            or normalized.get("type")
            or normalized.get("kind")
            or ""
        ).strip().upper()

        normalized["strike"] = float(normalized.get("strike") or 0.0)
        normalized["quantity"] = float(normalized.get("quantity") or 0.0)
        normalized["multiplier"] = float(normalized.get("multiplier") or 1.0)

        premium = (
            normalized.get("premium")
            if normalized.get("premium") is not None
            else normalized.get("entry_price")
        )
        if premium is None:
            premium = normalized.get("price")
        if premium is None:
            premium = normalized.get("last_price")
        if premium is None:
            premium = 0.0

        normalized["premium"] = float(premium)

        return normalized

    @staticmethod
    def _intrinsic_value(option_type: str, strike: float, spot: float) -> float:
        if option_type == "CALL":
            return max(spot - strike, 0.0)
        if option_type == "PUT":
            return max(strike - spot, 0.0)
        return 0.0

    def _compute_pl_at_spot(
        self,
        legs: list[dict[str, Any]],
        spot_price: float,
    ) -> float:
        total = 0.0

        for leg in legs:
            intrinsic = self._intrinsic_value(
                option_type=str(leg.get("option_type") or "").upper(),
                strike=float(leg.get("strike") or 0.0),
                spot=spot_price,
            )

            premium = float(leg.get("premium") or 0.0)
            quantity = float(leg.get("quantity") or 0.0)
            multiplier = float(leg.get("multiplier") or 1.0)

            unit_pl = intrinsic - premium

            if leg.get("position_side") == "SHORT":
                unit_pl = -unit_pl

            total += unit_pl * quantity * multiplier

        return round(float(total), 6)

    @staticmethod
    def _compute_net_premium_paid(legs: list[dict[str, Any]]) -> float:
        total = 0.0

        for leg in legs:
            premium = float(leg.get("premium") or 0.0)
            quantity = float(leg.get("quantity") or 0.0)
            multiplier = float(leg.get("multiplier") or 1.0)

            amount = premium * quantity * multiplier

            if leg.get("position_side") == "SHORT":
                amount = -amount

            total += amount

        return round(float(total), 6)
