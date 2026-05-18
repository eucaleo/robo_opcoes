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

    def _base_legs_response(
        self,
        structure: dict[str, Any],
        existing_legs: list[dict[str, Any]],
        aba: str | None,
        legs_source: str,
        legacy_timestamp: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return (
            {
                **structure,
                "legs": existing_legs,
            },
            {
                "legs_source": legs_source,
                "legacy_aba": aba,
                "legacy_timestamp": legacy_timestamp,
            },
        )

    def _enrich_structure_with_legs(
        self,
        structure: dict[str, Any],
        reference_date: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        existing_legs = structure.get("legs", [])
        aba = structure.get("alias_legacy_aba") or structure.get("name")
        aba = self._clean_text(aba)

        # 3B rule:
        # If canonical legs already exist in the structure repository,
        # they are always the source of truth for the main flow.
        if existing_legs:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                aba=aba,
                legs_source="canonical",
                legacy_timestamp=None,
            )

        if not self.enable_legacy_legs_fallback:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                aba=aba,
                legs_source="empty",
                legacy_timestamp=None,
            )

        if not aba or self.robo_legs_service is None:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                aba=aba,
                legs_source="empty",
                legacy_timestamp=None,
            )

        selected_timestamp = self._select_legacy_timestamp(
            aba=aba,
            reference_date=reference_date,
        )

        if not selected_timestamp:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                aba=aba,
                legs_source="empty",
                legacy_timestamp=None,
            )

        try:
            robo_legs = self.robo_legs_service.get_legs(
                aba=aba,
                timestamp=selected_timestamp,
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
            return (
                {
                    **structure,
                    "legs": canonical_robo_legs,
                },
                {
                    "legs_source": "legacy_robo",
                    "legacy_aba": aba,
                    "legacy_timestamp": selected_timestamp,
                },
            )

        return self._base_legs_response(
            structure=structure,
            existing_legs=existing_legs,
            aba=aba,
            legs_source="empty",
            legacy_timestamp=selected_timestamp,
        )

    def _select_legacy_timestamp(
        self,
        aba: str,
        reference_date: str | None = None,
    ) -> str | None:
        try:
            timestamps = self.robo_legs_service.repo.list_timestamps(aba)
        except Exception:
            timestamps = []

        if not timestamps:
            return None

        normalized = [str(ts) for ts in timestamps if ts]
        if not normalized:
            return None

        if reference_date:
            exact_prefix_matches = [ts for ts in normalized if ts.startswith(reference_date)]
            if exact_prefix_matches:
                return sorted(exact_prefix_matches)[-1]

        return sorted(normalized)[-1]

    def _clean_text(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value
