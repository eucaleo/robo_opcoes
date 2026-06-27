from pathlib import Path
from typing import Any

from repositories.structures_repository import StructuresRepository
from services.canonical_input_service import CanonicalInputService
from services.market_snapshot_provider import MarketSnapshotProvider
from services.pricing_payload_adapter import to_pricing_payload


class PricingInputService:
    def __init__(
        self,
        canonical_input_service: CanonicalInputService | None = None,
        db_path: str | Path | None = None,
    ):
        if canonical_input_service is not None:
            self.canonical_input_service = canonical_input_service
            return

        repository = None

        if db_path is not None:
            try:
                repository = StructuresRepository(db_path=db_path)
            except TypeError:
                repository = StructuresRepository()
        else:
            repository = StructuresRepository()

        market_snapshot_provider = (
            MarketSnapshotProvider(db_path=db_path)
            if db_path is not None
            else MarketSnapshotProvider()
        )

        self.canonical_input_service = CanonicalInputService(
            repository=repository,
            market_snapshot_provider=market_snapshot_provider,
        )

    def build_pricing_payload(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        canonical_input = self.canonical_input_service.build_structure_market_input(
            structure_id=structure_id,
            reference_date=reference_date,
        )

        return self.build_pricing_payload_from_canonical_input(canonical_input)

    def build_pricing_payload_from_canonical_input(
        self,
        canonical_input: dict[str, Any],
    ) -> dict[str, Any]:
        return to_pricing_payload(canonical_input)
