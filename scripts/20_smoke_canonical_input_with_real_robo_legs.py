from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from repositories.structures_repository import StructuresRepository
from services.market_snapshot_provider import MarketSnapshotProvider
from services.robo_legs_service import RoboLegsService
from services.robo_leg_mapper import to_canonical_leg
from services.structure_market_input_assembler import assemble_structure_market_input
from _smoke_context import require_context_value


def _find_structure_by_id(items, structure_id):
    for item in items:
        if item["id"] == structure_id:
            return item
    return None


def main():
    repository = StructuresRepository()
    market_snapshot_provider = MarketSnapshotProvider()
    robo_legs_service = RoboLegsService()

    structure_id = require_context_value("structure_id")
    structures = repository.list_structures()
    structure = _find_structure_by_id(structures, structure_id)

    if structure is None:
        raise RuntimeError("structure should exist in repository list")

    aba = structure.get("alias_legacy_aba") or structure.get("name")
    if not aba:
        raise RuntimeError("structure should provide alias_legacy_aba or name")

    timestamps = robo_legs_service.repo.list_timestamps(aba)
    if not timestamps:
        raise RuntimeError(f"no legacy timestamps found for aba: {aba}")

    timestamp = timestamps[0]
    robo_legs = robo_legs_service.get_legs(
        aba=aba,
        timestamp=timestamp,
        validate=False,
    )

    if not robo_legs:
        raise RuntimeError("robo legs should not be empty for selected timestamp")

    canonical_legs = []
    for leg in robo_legs:
        mapped = to_canonical_leg(leg)
        if mapped.get("expiration_date") is None:
            continue
        canonical_legs.append(mapped)

    if not canonical_legs:
        raise RuntimeError("canonical legs should not be empty after mapping")

    snapshot = market_snapshot_provider.get_snapshot(
        structure["underlying_asset"],
        reference_date="2026-05-14",
    )

    enriched_structure = {
        **structure,
        "legs": canonical_legs,
    }

    payload = assemble_structure_market_input(enriched_structure, snapshot)

    if payload["structure"]["structure_id"] != structure_id:
        raise RuntimeError("payload structure_id should match smoke context structure_id")

    if not payload["structure"]["legs"]:
        raise RuntimeError("payload should contain real canonical legs")

    print("STRUCTURE TARGET:", structure["underlying_asset"])
    print("ABA:", aba)
    print("TIMESTAMP USADO:", timestamp)
    print("CANONICAL LEGS:", canonical_legs)
    print("STRUCTURE MARKET INPUT COM LEGS REAIS:", payload)
    print("CANONICAL INPUT WITH REAL ROBO LEGS SMOKE OK")


if __name__ == "__main__":
    main()
