from typing import Any

from repositories.structures_repository import StructuresRepository
from services.market_snapshot_provider import MarketSnapshotProvider
from services.structure_market_input_assembler import assemble_structure_market_input


class CanonicalInputService:
    def __init__(
        self,
        repository: StructuresRepository | None = None,
        market_snapshot_provider: MarketSnapshotProvider | None = None,
    ):
        self.repository = repository or StructuresRepository()
        self.market_snapshot_provider = market_snapshot_provider or MarketSnapshotProvider()

    def build_structure_market_input(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        structure = self.repository.get_structure(structure_id)
        if structure is None:
            raise ValueError(f"structure not found: {structure_id}")

        snapshot = self.market_snapshot_provider.get_snapshot(
            structure["underlying_asset"],
            reference_date=reference_date,
        )

        return assemble_structure_market_input(structure, snapshot)
