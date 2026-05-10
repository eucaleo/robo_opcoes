from infra.bootstrap_structures_schema import ensure_structures_schema
from repositories.structures_repository import StructuresRepository


def main():
    ensure_structures_schema()

    repo = StructuresRepository()

    structure_id = repo.create_structure(
        {
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "status": "active",
            "notes": "smoke test",
        }
    )

    repo.add_leg(
        structure_id,
        {
            "position_side": "LONG",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-05-15",
            "quantity": 1000,
            "premium": None,
            "multiplier": 1,
            "leg_order": 1,
            "notes": "leg 1",
        },
    )

    repo.add_leg(
        structure_id,
        {
            "position_side": "SHORT",
            "option_type": "CALL",
            "symbol": "BOVAE200",
            "strike": 200.0,
            "expiration_date": "2026-05-15",
            "quantity": 1000,
            "premium": None,
            "multiplier": 1,
            "leg_order": 2,
            "notes": "leg 2",
        },
    )

    structures = repo.list_structures()
    print("STRUCTURES:", structures)

    structure = repo.get_structure(structure_id)
    print("STRUCTURE WITH LEGS:", structure)

    repo.update_structure(
        structure_id,
        {
            "name": "BOVA11 Condor Maio/2026 - Atualizada",
            "notes": "updated by smoke",
        },
    )

    repo.replace_legs(
        structure_id,
        [
            {
                "position_side": "LONG",
                "option_type": "PUT",
                "symbol": "BOVAM190",
                "strike": 190.0,
                "expiration_date": "2026-05-15",
                "quantity": 2000,
                "multiplier": 1,
                "notes": "replacement leg 1",
            },
            {
                "position_side": "SHORT",
                "option_type": "PUT",
                "symbol": "BOVAM185",
                "strike": 185.0,
                "expiration_date": "2026-05-15",
                "quantity": 2000,
                "multiplier": 1,
                "notes": "replacement leg 2",
            },
        ],
    )

    updated = repo.get_structure(structure_id)
    print("UPDATED STRUCTURE:", updated)

    repo.archive_structure(structure_id)

    archived = repo.get_structure(structure_id)
    print("ARCHIVED STRUCTURE:", archived)

    print("SMOKE OK")


if __name__ == "__main__":
    main()
