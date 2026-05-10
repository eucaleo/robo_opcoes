from typing import Any


class PricingEngineStub:
    def run(self, pricing_payload: dict[str, Any]) -> dict[str, Any]:
        if not pricing_payload:
            raise ValueError("pricing_payload is required")

        legs = pricing_payload.get("legs", [])
        if not legs:
            raise ValueError("pricing_payload.legs is required")

        total_quantity = sum(int(leg["quantity"]) for leg in legs)
        number_of_legs = len(legs)

        return {
            "engine": "stub",
            "status": "ok",
            "structure_id": pricing_payload["structure_id"],
            "underlying_asset": pricing_payload["underlying_asset"],
            "reference_date": pricing_payload["reference_date"],
            "metrics": {
                "number_of_legs": number_of_legs,
                "total_quantity": total_quantity,
                "spot_price": float(pricing_payload["spot_price"]),
                "interest_rate": float(pricing_payload["interest_rate"]),
                "volatility": float(pricing_payload["volatility"]),
            },
            "valuation": {
                "theoretical_value": 0.0,
                "premium_paid": 0.0,
                "max_profit": None,
                "max_loss": None,
            },
        }
