from typing import Any

from repositories.structures_repository import StructuresRepository
from services.market_snapshot_provider import MarketSnapshotProvider
from services.robo_leg_mapper import to_canonical_leg
from services.structure_market_input_assembler import assemble_structure_market_input


class CanonicalInputService:
    def __init__(
        self,
        repository: StructuresRepository | None = None,
        market_snapshot_provider: MarketSnapshotProvider | None = None,
        robo_legs_service: Any | None = None,
    ):
        self.repository = repository or StructuresRepository()
        self.market_snapshot_provider = market_snapshot_provider or MarketSnapshotProvider()

        if robo_legs_service is not None:
            self.robo_legs_service = robo_legs_service
        else:
            try:
                from services.robo_legs_service import RoboLegsService
                self.robo_legs_service = RoboLegsService()
            except Exception:
                self.robo_legs_service = None

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

        enriched_structure = self._enrich_structure_with_legs(
            structure=structure,
            reference_date=reference_date or snapshot["reference_date"],
        )

        return assemble_structure_market_input(enriched_structure, snapshot)

    def _enrich_structure_with_legs(
        self,
        structure: dict[str, Any],
        reference_date: str,
    ) -> dict[str, Any]:
        aba = structure.get("alias_legacy_aba") or structure.get("name")
        existing_legs = structure.get("legs", [])

        if not aba or self.robo_legs_service is None:
            return {
                **structure,
                "legs": existing_legs,
            }

        try:
            robo_legs = self.robo_legs_service.get_legs(
                aba=aba,
                timestamp=reference_date,
                validate=False,
            )
        except Exception:
            robo_legs = []

        canonical_robo_legs = []
        for leg in robo_legs:
            try:
                canonical_leg = to_canonical_leg(leg)
                if canonical_leg.get("expiration_date") is None:
                    continue
                canonical_robo_legs.append(canonical_leg)
            except Exception:
                continue

        if canonical_robo_legs:
            return {
                **structure,
                "legs": canonical_robo_legs,
            }

        return {
            **structure,
            "legs": existing_legs,
        }
