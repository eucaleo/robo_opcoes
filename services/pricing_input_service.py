from typing import Any

from services.canonical_input_service import CanonicalInputService
from services.pricing_payload_adapter import to_pricing_payload


class PricingInputService:
    def __init__(
        self,
        canonical_input_service: CanonicalInputService | None = None,
    ):
        self.canonical_input_service = canonical_input_service or CanonicalInputService()

    def build_pricing_payload(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        canonical_input = self.canonical_input_service.build_structure_market_input(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        return to_pricing_payload(canonical_input)
