import pytest

from infra.bootstrap_structures_schema import ensure_structures_schema
from repositories.structures_repository import StructuresRepository


@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "app.db"
    ensure_structures_schema(db_path)
    return StructuresRepository(db_path=str(db_path))


def valid_structure_payload():
    return {
        "name": "Fence BOVA11",
        "underlying_asset": "bova11",
        "alias_legacy_aba": "BOVA11",
        "status": "active",
        "notes": "estrutura teste",
    }


def valid_leg_payload(**overrides):
    payload = {
        "position_side": "LONG",
        "option_type": "CALL",
        "symbol": "BOVA11C120",
        "strike": 120.0,
        "expiration_date": "2026-06-20",
        "quantity": 2,
        "premium": 1.5,
        "multiplier": 100,
        "leg_order": 1,
        "notes": "leg teste",
    }
    payload.update(overrides)
    return payload


def test_create_structure_normalizes_underlying_asset(repo):
    structure_id = repo.create_structure(valid_structure_payload())

    structure = repo.get_structure(structure_id)

    assert structure is not None
    assert structure["name"] == "Fence BOVA11"
    assert structure["underlying_asset"] == "BOVA11"
    assert structure["status"] == "active"
    assert structure["legs"] == []


def test_create_structure_raises_when_name_missing(repo):
    payload = valid_structure_payload()
    payload["name"] = ""

    with pytest.raises(ValueError, match="name is required"):
        repo.create_structure(payload)


def test_create_structure_raises_when_underlying_asset_missing(repo):
    payload = valid_structure_payload()
    payload["underlying_asset"] = "   "

    with pytest.raises(ValueError, match="underlying_asset is required"):
        repo.create_structure(payload)


def test_create_structure_raises_when_status_invalid(repo):
    payload = valid_structure_payload()
    payload["status"] = "draft"

    with pytest.raises(ValueError, match="invalid status: draft"):
        repo.create_structure(payload)


def test_list_structures_excludes_archived_by_default(repo):
    active_id = repo.create_structure(valid_structure_payload())
    archived_id = repo.create_structure(
        {
            "name": "Trava PETR4",
            "underlying_asset": "PETR4",
            "status": "active",
        }
    )
    repo.archive_structure(archived_id)

    result = repo.list_structures()

    assert [item["id"] for item in result] == [active_id]


def test_list_structures_can_include_archived(repo):
    first_id = repo.create_structure(valid_structure_payload())
    second_id = repo.create_structure(
        {
            "name": "Trava PETR4",
            "underlying_asset": "PETR4",
            "status": "active",
        }
    )
    repo.archive_structure(second_id)

    result = repo.list_structures(include_archived=True)

    assert [item["id"] for item in result] == [first_id, second_id]
    assert result[1]["status"] == "archived"


def test_get_structure_returns_legs_ordered_by_leg_order(repo):
    structure_id = repo.create_structure(valid_structure_payload())

    repo.add_leg(structure_id, valid_leg_payload(leg_order=2, symbol="BOVA11C130", strike=130.0))
    repo.add_leg(
        structure_id,
        valid_leg_payload(
            leg_order=1,
            option_type="PUT",
            symbol="BOVA11P110",
            strike=110.0,
        ),
    )

    structure = repo.get_structure(structure_id)

    assert structure is not None
    assert [leg["leg_order"] for leg in structure["legs"]] == [1, 2]
    assert [leg["symbol"] for leg in structure["legs"]] == ["BOVA11P110", "BOVA11C130"]


def test_update_structure_updates_fields_and_keeps_missing_ones(repo):
    structure_id = repo.create_structure(valid_structure_payload())

    repo.update_structure(
        structure_id,
        {
            "name": "Fence BOVA11 Ajustada",
            "notes": "nota nova",
        },
    )

    structure = repo.get_structure(structure_id)

    assert structure["name"] == "Fence BOVA11 Ajustada"
    assert structure["underlying_asset"] == "BOVA11"
    assert structure["alias_legacy_aba"] == "BOVA11"
    assert structure["notes"] == "nota nova"


def test_update_structure_raises_when_structure_not_found(repo):
    with pytest.raises(ValueError, match="structure not found: 999"):
        repo.update_structure(999, {"name": "x"})


def test_archive_structure_marks_structure_as_archived(repo):
    structure_id = repo.create_structure(valid_structure_payload())

    repo.archive_structure(structure_id)

    structure = repo.get_structure(structure_id)
    assert structure["status"] == "archived"


def test_archive_structure_raises_when_not_found(repo):
    with pytest.raises(ValueError, match="structure not found: 999"):
        repo.archive_structure(999)


def test_add_leg_adds_leg_to_structure(repo):
    structure_id = repo.create_structure(valid_structure_payload())

    leg_id = repo.add_leg(structure_id, valid_leg_payload())

    structure = repo.get_structure(structure_id)

    assert leg_id > 0
    assert len(structure["legs"]) == 1
    assert structure["legs"][0]["position_side"] == "LONG"
    assert structure["legs"][0]["option_type"] == "CALL"


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("position_side", "INVALID", "invalid position_side: INVALID"),
        ("option_type", "INVALID", "invalid option_type: INVALID"),
        ("strike", "abc", "strike must be numeric"),
        ("quantity", "abc", "quantity must be integer"),
        ("quantity", 0, "quantity must be > 0"),
        ("multiplier", "abc", "multiplier must be numeric"),
        ("multiplier", 0, "multiplier must be > 0"),
        ("leg_order", "abc", "leg_order must be integer"),
        ("leg_order", 0, "leg_order must be >= 1"),
        ("expiration_date", "20-06-2026", "expiration_date must be a valid date in YYYY-MM-DD format"),
    ],
)
def test_add_leg_validates_fields(repo, field, value, error):
    structure_id = repo.create_structure(valid_structure_payload())
    payload = valid_leg_payload(**{field: value})

    with pytest.raises(ValueError, match=error):
        repo.add_leg(structure_id, payload)


def test_add_leg_raises_when_structure_not_found(repo):
    with pytest.raises(ValueError, match="structure not found: 999"):
        repo.add_leg(999, valid_leg_payload())


def test_replace_legs_replaces_existing_legs(repo):
    structure_id = repo.create_structure(valid_structure_payload())

    repo.add_leg(structure_id, valid_leg_payload(leg_order=1, symbol="BOVA11C120", strike=120))
    repo.add_leg(structure_id, valid_leg_payload(leg_order=2, symbol="BOVA11P110", strike=110, option_type="PUT"))

    repo.replace_legs(
        structure_id,
        [
            valid_leg_payload(
                leg_order=1,
                position_side="SHORT",
                option_type="PUT",
                symbol="BOVA11P100",
                strike=100,
            )
        ],
    )

    structure = repo.get_structure(structure_id)

    assert len(structure["legs"]) == 1
    assert structure["legs"][0]["symbol"] == "BOVA11P100"
    assert structure["legs"][0]["position_side"] == "SHORT"
    assert structure["legs"][0]["option_type"] == "PUT"


def test_replace_legs_raises_when_structure_not_found(repo):
    with pytest.raises(ValueError, match="structure not found: 999"):
        repo.replace_legs(999, [valid_leg_payload()])


def test_get_structure_returns_none_when_not_found(repo):
    assert repo.get_structure(999) is None
