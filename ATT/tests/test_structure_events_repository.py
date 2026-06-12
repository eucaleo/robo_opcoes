import pytest

from infra.bootstrap_structures_schema import ensure_structures_schema
from repositories.structure_events_repository import StructureEventsRepository
from repositories.structures_repository import StructuresRepository


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "app.db"
    ensure_structures_schema(path)
    return path


@pytest.fixture
def structures_repo(db_path):
    return StructuresRepository(db_path=str(db_path))


@pytest.fixture
def events_repo(db_path):
    repo = StructureEventsRepository(db_path=str(db_path))
    repo.ensure_schema()
    return repo


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


def create_structure_with_leg(structures_repo):
    structure_id = structures_repo.create_structure(valid_structure_payload())
    leg_id = structures_repo.add_leg(structure_id, valid_leg_payload())
    return structure_id, leg_id


def test_create_event_persists_operational_event(events_repo, structures_repo):
    structure_id, leg_id = create_structure_with_leg(structures_repo)

    event_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "partial_close",
            "event_date": "2026-06-12",
            "quantity": 1,
            "price": 2.35,
            "symbol": "BOVA11C120",
            "source": "manual",
            "notes": "encerramento parcial",
            "metadata": {
                "reason": "redução de risco",
            },
        }
    )

    event = events_repo.get_event(event_id)

    assert event is not None
    assert event["id"] == event_id
    assert event["structure_id"] == structure_id
    assert event["leg_id"] == leg_id
    assert event["event_type"] == "partial_close"
    assert event["event_status"] == "registered"
    assert event["event_date"] == "2026-06-12"
    assert event["quantity"] == 1
    assert event["price"] == 2.35
    assert event["symbol"] == "BOVA11C120"
    assert event["source"] == "manual"
    assert event["notes"] == "encerramento parcial"
    assert event["metadata"] == {"reason": "redução de risco"}
    assert event["created_at"].endswith("Z")
    assert event["updated_at"].endswith("Z")


def test_create_event_allows_structure_level_note_without_leg(events_repo, structures_repo):
    structure_id = structures_repo.create_structure(valid_structure_payload())

    event_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "event_type": "note",
            "event_date": "2026-06-12T10:00:00Z",
            "source": "system",
            "notes": "observação operacional",
        }
    )

    event = events_repo.get_event(event_id)

    assert event["structure_id"] == structure_id
    assert event["leg_id"] is None
    assert event["event_type"] == "note"
    assert event["quantity"] is None
    assert event["price"] is None
    assert event["metadata"] is None


def test_list_events_orders_by_event_date_and_id(events_repo, structures_repo):
    structure_id, leg_id = create_structure_with_leg(structures_repo)

    second_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "adjustment",
            "event_date": "2026-06-13",
            "source": "manual",
        }
    )
    first_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "open",
            "event_date": "2026-06-12",
            "source": "legacy_import",
        }
    )

    events = events_repo.list_events_for_structure(structure_id)

    assert [event["id"] for event in events] == [first_id, second_id]


def test_list_events_filters_by_type_and_status(events_repo, structures_repo):
    structure_id, leg_id = create_structure_with_leg(structures_repo)

    open_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "open",
            "event_date": "2026-06-12",
            "source": "legacy_import",
        }
    )
    close_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "total_close",
            "event_date": "2026-06-13",
            "source": "manual",
        }
    )

    events_repo.cancel_event(close_id, notes="cancelado por teste")

    open_events = events_repo.list_events(
        structure_id=structure_id,
        event_type="open",
    )
    registered_events = events_repo.list_events(
        structure_id=structure_id,
        event_status="registered",
    )
    all_events = events_repo.list_events(
        structure_id=structure_id,
        include_cancelled=True,
    )

    assert [event["id"] for event in open_events] == [open_id]
    assert [event["id"] for event in registered_events] == [open_id]
    assert [event["id"] for event in all_events] == [open_id, close_id]


def test_cancel_event_marks_event_as_cancelled(events_repo, structures_repo):
    structure_id, leg_id = create_structure_with_leg(structures_repo)

    event_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "manual_close",
            "event_date": "2026-06-12",
            "source": "manual",
            "notes": "original",
        }
    )

    events_repo.cancel_event(event_id, notes="cancelado")

    event = events_repo.get_event(event_id)

    assert event["event_status"] == "cancelled"
    assert event["notes"] == "cancelado"


def test_count_events_ignores_cancelled_by_default(events_repo, structures_repo):
    structure_id, leg_id = create_structure_with_leg(structures_repo)

    first_id = events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "open",
            "event_date": "2026-06-12",
            "source": "manual",
        }
    )
    events_repo.create_event(
        {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": "roll",
            "event_date": "2026-06-13",
            "source": "manual",
            "metadata": {
                "exit_symbol": "BOVA11C120",
                "entry_symbol": "BOVA11C125",
            },
        }
    )

    events_repo.cancel_event(first_id)

    assert events_repo.count_events(structure_id=structure_id) == 1
    assert events_repo.count_events(structure_id=structure_id, include_cancelled=True) == 2
    assert events_repo.count_events(structure_id=structure_id, event_type="roll") == 1


def test_get_event_returns_none_when_not_found(events_repo):
    assert events_repo.get_event(999) is None


def test_create_event_raises_when_structure_not_found(events_repo):
    with pytest.raises(ValueError, match="structure not found: 999"):
        events_repo.create_event(
            {
                "structure_id": 999,
                "event_type": "open",
                "event_date": "2026-06-12",
            }
        )


def test_create_event_raises_when_leg_does_not_belong_to_structure(
    events_repo,
    structures_repo,
):
    first_structure_id, _first_leg_id = create_structure_with_leg(structures_repo)
    second_structure_id = structures_repo.create_structure(
        {
            "name": "Trava PETR4",
            "underlying_asset": "PETR4",
            "status": "active",
        }
    )
    second_leg_id = structures_repo.add_leg(
        second_structure_id,
        valid_leg_payload(symbol="PETR4C40", strike=40.0),
    )

    with pytest.raises(ValueError, match="leg not found for structure"):
        events_repo.create_event(
            {
                "structure_id": first_structure_id,
                "leg_id": second_leg_id,
                "event_type": "partial_close",
                "event_date": "2026-06-12",
            }
        )


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("structure_id", 0, "structure_id must be > 0"),
        ("event_type", "invalid", "invalid event_type: invalid"),
        ("event_status", "invalid", "invalid event_status: invalid"),
        ("event_date", "", "event_date is required"),
        ("quantity", "abc", "quantity must be integer when provided"),
        ("quantity", 0, "quantity must be > 0 when provided"),
        ("price", "abc", "price must be numeric when provided"),
        ("source", "invalid", "invalid source: invalid"),
        ("metadata", "abc", "metadata must be a dict when provided"),
    ],
)
def test_create_event_validates_payload(
    events_repo,
    structures_repo,
    field,
    value,
    error,
):
    structure_id, leg_id = create_structure_with_leg(structures_repo)

    payload = {
        "structure_id": structure_id,
        "leg_id": leg_id,
        "event_type": "open",
        "event_date": "2026-06-12",
        "source": "manual",
    }
    payload[field] = value

    with pytest.raises(ValueError, match=error):
        events_repo.create_event(payload)


def test_cancel_event_raises_when_not_found(events_repo):
    with pytest.raises(ValueError, match="event not found: 999"):
        events_repo.cancel_event(999)


def test_list_events_validates_filters(events_repo):
    with pytest.raises(ValueError, match="invalid event_type: invalid"):
        events_repo.list_events(event_type="invalid")

    with pytest.raises(ValueError, match="invalid event_status: invalid"):
        events_repo.list_events(event_status="invalid")

    with pytest.raises(ValueError, match="limit must be > 0"):
        events_repo.list_events(limit=0)

    with pytest.raises(ValueError, match="offset must be >= 0"):
        events_repo.list_events(offset=-1)
