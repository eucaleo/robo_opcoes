from typing import Any

from repositories.structures_repository import StructuresRepository
from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback
from services.market_snapshot_provider import MarketSnapshotProvider
from services.structure_market_input_assembler import assemble_structure_market_input


class CanonicalInputService:
    def __init__(
        self,
        repository: StructuresRepository | None = None,
        market_snapshot_provider: MarketSnapshotProvider | None = None,
        robo_legs_service: Any | None = None,
        prefer_canonical_legs: bool = True,
        enable_legacy_legs_fallback: bool = True,
    ):
        self.repository = repository or StructuresRepository()
        self.market_snapshot_provider = market_snapshot_provider or MarketSnapshotProvider()
        self.prefer_canonical_legs = prefer_canonical_legs
        self.enable_legacy_legs_fallback = enable_legacy_legs_fallback

        if robo_legs_service is not None:
            self.robo_legs_service = robo_legs_service
        else:
            try:
                from services.robo_legs_service import RoboLegsService
                self.robo_legs_service = RoboLegsService()
            except Exception:
                self.robo_legs_service = None

        self.legacy_robo_legs_fallback = LegacyRoboLegsFallback(
            robo_legs_service=self.robo_legs_service,
        )

    def build_structure_market_input(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        structure = self.repository.get_structure(structure_id)
        if structure is None:
            raise ValueError(f"structure not found: {structure_id}")

        structure = {
            **structure,
            "name": self._clean_text(structure.get("name")),
            "underlying_asset": self._clean_text(structure.get("underlying_asset")),
            "alias_legacy_aba": self._clean_text(structure.get("alias_legacy_aba")),
        }

        snapshot = self.market_snapshot_provider.get_snapshot(
            structure["underlying_asset"],
            reference_date=reference_date,
        )

        effective_reference_date = reference_date or snapshot.get("reference_date")

        enriched_structure, enrichment_meta = self._enrich_structure_with_legs(
            structure=structure,
            reference_date=effective_reference_date,
        )

        assembled = assemble_structure_market_input(enriched_structure, snapshot)
        assembled_meta = assembled.get("meta") or {}

        return {
            **assembled,
            "meta": {
                **assembled_meta,
                "reference_date": effective_reference_date,
                **enrichment_meta,
            },
        }

    def _build_meta(
        self,
        legs_source: str,
        legacy_timestamp: str | None = None,
    ) -> dict[str, Any]:
        meta = {
            "legs_source": legs_source,
        }

        if legacy_timestamp is not None:
            meta["legacy_timestamp"] = legacy_timestamp

        return meta

    def _base_legs_response(
        self,
        structure: dict[str, Any],
        existing_legs: list[dict[str, Any]],
        legs_source: str,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return (
            {
                **structure,
                "legs": existing_legs,
            },
            self._build_meta(
                legs_source=legs_source,
            ),
        )

    def _enrich_structure_with_legs(
        self,
        structure: dict[str, Any],
        reference_date: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        existing_legs = structure.get("legs", [])

        # 3B rule:
        # If canonical legs already exist in the structure repository,
        # they are always the source of truth for the main flow.
        if existing_legs:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                legs_source="canonical",
            )

        if not self.enable_legacy_legs_fallback:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                legs_source="empty",
            )

        fallback_legs, fallback_meta = self.legacy_robo_legs_fallback.load(
            structure=structure,
            reference_date=reference_date,
        )

        if fallback_legs:
            return (
                {
                    **structure,
                    "legs": fallback_legs,
                },
                fallback_meta,
            )

        return self._base_legs_response(
            structure=structure,
            existing_legs=existing_legs,
            legs_source="empty",
        )

    def _clean_text(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value
