from typing import Any

from services.payoff_pricing_engine import PayoffPricingEngine
from services.pricing_input_service import PricingInputService


class PricingExecutionService:
    def __init__(
        self,
        pricing_input_service: PricingInputService | None = None,
        pricing_engine: PayoffPricingEngine | None = None,
    ):
        self.pricing_input_service = pricing_input_service or PricingInputService()
        self.pricing_engine = pricing_engine or PayoffPricingEngine()

    def execute(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        pricing_payload = self.pricing_input_service.build_pricing_payload(
            structure_id=structure_id,
            reference_date=reference_date,
        )
        return self.execute_payload(pricing_payload)

    def execute_payload(
        self,
        pricing_payload: dict[str, Any],
    ) -> dict[str, Any]:
        result = self.pricing_engine.run(pricing_payload)

        return {
            "pricing_payload": pricing_payload,
            "result": result,
        }
