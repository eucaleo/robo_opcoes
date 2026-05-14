from repositories.structures_repository import StructuresRepository
from _smoke_context import update_context


def _find_structure_by_id(items, structure_id):
    for item in items:
        if item["id"] == structure_id:
            return item
    return None


def main():
    repository = StructuresRepository()

    create_payload = {
        "name": "BOVA11 Condor Maio/2026",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "notes": "smoke test",
        "legs": [
            {
                "position_side": "LONG",
                "option_type": "CALL",
                "symbol": "BOVAE195",
                "strike": 195.0,
                "expiration_date": "2026-05-15",
                "quantity": 1000,
                "premium": None,
                "multiplier": 1.0,
                "leg_order": 1,
                "notes": "leg 1",
            },
            {
                "position_side": "SHORT",
                "option_type": "CALL",
                "symbol": "BOVAE200",
                "strike": 200.0,
                "expiration_date": "2026-05-15",
                "quantity": 1000,
                "premium": None,
                "multiplier": 1.0,
                "leg_order": 2,
                "notes": "leg 2",
            },
        ],
    }

    created_structure_id = repository.create_structure(create_payload)
    update_context(structure_id=created_structure_id)

    all_structures = repository.list_structures()
    created_structure = _find_structure_by_id(all_structures, created_structure_id)

    print("CREATED STRUCTURE ID:", created_structure_id)
    print("CREATED STRUCTURE:", created_structure)

    if created_structure is None:
        raise RuntimeError("created structure should be present in repository list")

    update_payload = {
        "name": "BOVA11 Condor Maio/2026 - Atualizada",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "status": "active",
        "notes": "updated by smoke",
        "legs": [
            {
                "position_side": "LONG",
                "option_type": "PUT",
                "symbol": "BOVAM190",
                "strike": 190.0,
                "expiration_date": "2026-05-15",
                "quantity": 2000,
                "premium": None,
                "multiplier": 1.0,
                "leg_order": 1,
                "notes": "replacement leg 1",
            },
            {
                "position_side": "SHORT",
                "option_type": "PUT",
                "symbol": "BOVAM185",
                "strike": 185.0,
                "expiration_date": "2026-05-15",
                "quantity": 2000,
                "premium": None,
                "multiplier": 1.0,
                "leg_order": 2,
                "notes": "replacement leg 2",
            },
        ],
    }

    repository.update_structure(created_structure_id, update_payload)

    refreshed_structures = repository.list_structures()
    loaded_structure = _find_structure_by_id(refreshed_structures, created_structure_id)

    print("LOADED STRUCTURE:", loaded_structure)

    if created_structure_id <= 0:
        raise RuntimeError("created structure id should be greater than zero")

    if loaded_structure is None:
        raise RuntimeError("loaded structure should be present after update")

    if loaded_structure["id"] != created_structure_id:
        raise RuntimeError("loaded structure id should match created structure id")

    if loaded_structure["status"] != "active":
        raise RuntimeError("loaded structure status should be active")

    print("SMOKE OK")


if __name__ == "__main__":
    main()
