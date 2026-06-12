import pytest

from services.structure_events_service import StructureEventsService


class FakeStructureEventsRepository:
    def __init__(self):
        self.created = []
        self.cancelled = []
        self.events = {
            1: {
                "id": 1,
                "structure_id": 10,
                "event_type": "opening",
                "event_status": "registered",
                "event_date": "2026-06-12",
            }
        }

    def create_event(self, data):
        record = {
            "id": len(self.created) + 1,
            **data,
        }
        self.created.append(record)
        return record

    def cancel_event(self, event_id, notes=None):
        record = {
            "id": event_id,
            "event_status": "cancelled",
            "notes": notes,
        }
        self.cancelled.append(record)
        return record

    def get_event(self, event_id):
        return self.events.get(event_id)

    def list_events(
        self,
        structure_id=None,
        event_type=None,
        event_status=None,
        include_cancelled=False,
        limit=100,
        offset=0,
    ):
        return [
            {
                "structure_id": structure_id,
                "event_type": event_type,
                "event_status": event_status,
                "include_cancelled": include_cancelled,
                "limit": limit,
                "offset": offset,
            }
        ]

    def list_events_for_structure(self, structure_id, include_cancelled=False):
        return [
            {
                "structure_id": structure_id,
                "include_cancelled": include_cancelled,
            }
        ]

    def count_events(
        self,
        structure_id=None,
        event_type=None,
        include_cancelled=False,
    ):
        return 7


@pytest.fixture
def fake_repo():
    return FakeStructureEventsRepository()


@pytest.fixture
def service(fake_repo):
    return StructureEventsService(structure_events_repository=fake_repo)


def test_record_event_delegates_to_repository_with_normalized_payload(service, fake_repo):
    record = service.record_event(
        structure_id=10,
        leg_id=3,
        event_type="opening",
        event_status="confirmed",
        event_date="2026-06-12",
        quantity=100,
        price=1.23,
        symbol="  PETRA100  ",
        source="manual",
        notes="  abertura  ",
        metadata={"foo": "bar"},
    )

    assert record["id"] == 1
    assert record["structure_id"] == 10
    assert record["leg_id"] == 3
    assert record["event_type"] == "opening"
    assert record["event_status"] == "confirmed"
    assert record["event_date"] == "2026-06-12"
    assert record["quantity"] == 100
    assert record["price"] == 1.23
    assert record["symbol"] == "PETRA100"
    assert record["source"] == "manual"
    assert record["notes"] == "abertura"
    assert record["metadata"] == {"foo": "bar"}

    assert fake_repo.created == [record]


@pytest.mark.parametrize(
    "method_name,event_type",
    [
        ("register_opening", "opening"),
        ("register_adjustment", "adjustment"),
        ("register_rollover", "rollover"),
        ("register_partial_close", "partial_close"),
        ("register_full_close", "full_close"),
    ],
)
def test_semantic_registration_methods_create_expected_event_type(
    service,
    method_name,
    event_type,
):
    method = getattr(service, method_name)

    record = method(
        structure_id=10,
        leg_id=2,
        event_date="2026-06-12",
        quantity=50,
        price=2.5,
        symbol="PETRA100",
        source="system",
        notes="evento operacional",
        metadata={"reason": "test"},
    )

    assert record["event_type"] == event_type
    assert record["structure_id"] == 10
    assert record["leg_id"] == 2
    assert record["event_date"] == "2026-06-12"
    assert record["quantity"] == 50
    assert record["price"] == 2.5
    assert record["symbol"] == "PETRA100"
    assert record["source"] == "system"
    assert record["notes"] == "evento operacional"


def test_register_manual_close_forces_manual_source(service):
    record = service.register_manual_close(
        structure_id=10,
        event_date="2026-06-12",
        quantity=10,
        price=1.0,
        notes="encerramento manual",
    )

    assert record["event_type"] == "manual_close"
    assert record["source"] == "manual"
    assert record["quantity"] == 10
    assert record["price"] == 1.0


def test_register_note_requires_non_empty_notes(service):
    with pytest.raises(ValueError, match="notes must not be empty"):
        service.register_note(
            structure_id=10,
            event_date="2026-06-12",
            notes="   ",
        )


def test_register_note_creates_note_event(service):
    record = service.register_note(
        structure_id=10,
        event_date="2026-06-12",
        notes="observação operacional",
        metadata={"tag": "obs"},
    )

    assert record["event_type"] == "note"
    assert record["notes"] == "observação operacional"
    assert record["metadata"] == {"tag": "obs"}


@pytest.mark.parametrize(
    "field_name,kwargs,message",
    [
        (
            "structure_id",
            {"structure_id": 0},
            "structure_id must be greater than zero",
        ),
        (
            "leg_id",
            {"leg_id": 0},
            "leg_id must be greater than zero",
        ),
        (
            "event_type",
            {"event_type": "invalid"},
            "event_type must be one of",
        ),
        (
            "event_status",
            {"event_status": "invalid"},
            "event_status must be one of",
        ),
        (
            "event_date",
            {"event_date": ""},
            "event_date must not be empty",
        ),
        (
            "event_date",
            {"event_date": "12/06/2026"},
            "event_date must be in YYYY-MM-DD format",
        ),
        (
            "quantity",
            {"quantity": -1},
            "quantity must be greater than or equal to zero",
        ),
        (
            "quantity",
            {"quantity": 1.5},
            "quantity must be an integer",
        ),
        (
            "price",
            {"price": -0.01},
            "price must be greater than or equal to zero",
        ),
        (
            "price",
            {"price": "1.23"},
            "price must be numeric",
        ),
        (
            "source",
            {"source": "invalid"},
            "source must be one of",
        ),
    ],
)
def test_record_event_validations(service, field_name, kwargs, message):
    payload = {
        "structure_id": 10,
        "event_type": "opening",
        "event_status": "registered",
        "event_date": "2026-06-12",
        "source": "manual",
    }
    payload.update(kwargs)

    with pytest.raises(ValueError, match=message):
        service.record_event(**payload)


def test_cancel_event_validates_id_and_delegates(service, fake_repo):
    record = service.cancel_event(5, notes="  cancelado  ")

    assert record == {
        "id": 5,
        "event_status": "cancelled",
        "notes": "cancelado",
    }
    assert fake_repo.cancelled == [record]


def test_cancel_event_rejects_invalid_id(service):
    with pytest.raises(ValueError, match="event_id must be greater than zero"):
        service.cancel_event(0)


def test_get_event_validates_id_and_delegates(service):
    assert service.get_event(1)["id"] == 1

    with pytest.raises(ValueError, match="event_id must be greater than zero"):
        service.get_event(0)


def test_list_events_validates_filters_and_delegates(service):
    result = service.list_events(
        structure_id=10,
        event_type="opening",
        event_status="registered",
        include_cancelled=True,
        limit=20,
        offset=5,
    )

    assert result == [
        {
            "structure_id": 10,
            "event_type": "opening",
            "event_status": "registered",
            "include_cancelled": True,
            "limit": 20,
            "offset": 5,
        }
    ]


@pytest.mark.parametrize(
    "kwargs,message",
    [
        (
            {"structure_id": 0},
            "structure_id must be greater than zero",
        ),
        (
            {"event_type": "invalid"},
            "event_type must be one of",
        ),
        (
            {"event_status": "invalid"},
            "event_status must be one of",
        ),
        (
            {"limit": 0},
            "limit must be greater than zero",
        ),
        (
            {"offset": -1},
            "offset must be greater than or equal to zero",
        ),
    ],
)
def test_list_events_validations(service, kwargs, message):
    with pytest.raises(ValueError, match=message):
        service.list_events(**kwargs)


def test_list_events_for_structure_validates_and_delegates(service):
    result = service.list_events_for_structure(10, include_cancelled=True)

    assert result == [
        {
            "structure_id": 10,
            "include_cancelled": True,
        }
    ]

    with pytest.raises(ValueError, match="structure_id must be greater than zero"):
        service.list_events_for_structure(0)


def test_count_events_validates_and_delegates(service):
    assert service.count_events(
        structure_id=10,
        event_type="opening",
        include_cancelled=True,
    ) == 7

    with pytest.raises(ValueError, match="structure_id must be greater than zero"):
        service.count_events(structure_id=0)

    with pytest.raises(ValueError, match="event_type must be one of"):
        service.count_events(event_type="invalid")
