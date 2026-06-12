from services.structure_events_service import StructureEventsService


class FakeEventsRepository:
    def __init__(self, events):
        self.events = events

    def list_events_for_structure(self, structure_id, include_cancelled=False):
        if include_cancelled:
            return self.events

        return [
            event
            for event in self.events
            if event.get("event_status") != "cancelled"
        ]


def make_structure():
    return {
        "id": 10,
        "name": "BOVA11 Condor",
        "underlying_asset": "BOVA11",
        "status": "active",
        "legs": [
            {
                "id": 1,
                "position_side": "LONG",
                "option_type": "PUT",
                "symbol": "BOVAM190",
                "strike": 190.0,
                "expiration_date": "2026-05-15",
                "quantity": 100,
                "premium": 1.0,
                "multiplier": 1.0,
            },
            {
                "id": 2,
                "position_side": "SHORT",
                "option_type": "PUT",
                "symbol": "BOVAM185",
                "strike": 185.0,
                "expiration_date": "2026-05-15",
                "quantity": 100,
                "premium": 1.0,
                "multiplier": 1.0,
            },
        ],
    }


def test_apply_events_partial_close_reduces_target_leg_quantity():
    service = StructureEventsService(
        structure_events_repository=FakeEventsRepository(
            events=[
                {
                    "id": 1,
                    "structure_id": 10,
                    "leg_id": 1,
                    "event_type": "partial_close",
                    "event_status": "confirmed",
                    "event_date": "2026-06-12",
                    "quantity": 40,
                }
            ]
        )
    )

    result = service.apply_events_to_structure(make_structure())

    assert result["legs"][0]["quantity"] == 60
    assert result["legs"][1]["quantity"] == 100
    assert result["legs"][0]["_original_quantity"] == 100
    assert result["operational_state"]["events_applied"] == 1
    assert result["operational_state"]["is_closed"] is False


def test_apply_events_full_close_without_leg_id_zeros_all_legs():
    service = StructureEventsService(
        structure_events_repository=FakeEventsRepository(
            events=[
                {
                    "id": 1,
                    "structure_id": 10,
                    "leg_id": None,
                    "event_type": "full_close",
                    "event_status": "confirmed",
                    "event_date": "2026-06-12",
                    "quantity": None,
                }
            ]
        )
    )

    result = service.apply_events_to_structure(make_structure())

    assert result["legs"][0]["quantity"] == 0
    assert result["legs"][1]["quantity"] == 0
    assert result["legs"][0]["operational_status"] == "closed"
    assert result["legs"][1]["operational_status"] == "closed"
    assert result["operational_state"]["is_closed"] is True


def test_apply_events_cancelled_event_is_ignored():
    service = StructureEventsService(
        structure_events_repository=FakeEventsRepository(
            events=[
                {
                    "id": 1,
                    "structure_id": 10,
                    "leg_id": 1,
                    "event_type": "partial_close",
                    "event_status": "cancelled",
                    "event_date": "2026-06-12",
                    "quantity": 40,
                }
            ]
        )
    )

    result = service.apply_events_to_structure(make_structure())

    assert result["legs"][0]["quantity"] == 100
    assert result["legs"][1]["quantity"] == 100
    assert result["operational_state"]["events_applied"] == 0
    assert result["operational_state"]["events_ignored_cancelled"] == 1


def test_apply_events_manual_close_with_quantity_reduces_leg():
    service = StructureEventsService(
        structure_events_repository=FakeEventsRepository(
            events=[
                {
                    "id": 1,
                    "structure_id": 10,
                    "leg_id": 2,
                    "event_type": "manual_close",
                    "event_status": "registered",
                    "event_date": "2026-06-12",
                    "quantity": 25,
                }
            ]
        )
    )

    result = service.apply_events_to_structure(make_structure())

    assert result["legs"][0]["quantity"] == 100
    assert result["legs"][1]["quantity"] == 75


def test_apply_events_manual_close_without_quantity_zeros_leg():
    service = StructureEventsService(
        structure_events_repository=FakeEventsRepository(
            events=[
                {
                    "id": 1,
                    "structure_id": 10,
                    "leg_id": 2,
                    "event_type": "manual_close",
                    "event_status": "registered",
                    "event_date": "2026-06-12",
                    "quantity": None,
                }
            ]
        )
    )

    result = service.apply_events_to_structure(make_structure())

    assert result["legs"][0]["quantity"] == 100
    assert result["legs"][1]["quantity"] == 0


def test_apply_events_note_and_rollover_do_not_change_quantities():
    service = StructureEventsService(
        structure_events_repository=FakeEventsRepository(
            events=[
                {
                    "id": 1,
                    "structure_id": 10,
                    "event_type": "note",
                    "event_status": "registered",
                    "event_date": "2026-06-12",
                    "quantity": None,
                },
                {
                    "id": 2,
                    "structure_id": 10,
                    "event_type": "rollover",
                    "event_status": "registered",
                    "event_date": "2026-06-13",
                    "quantity": None,
                },
            ]
        )
    )

    result = service.apply_events_to_structure(make_structure())

    assert result["legs"][0]["quantity"] == 100
    assert result["legs"][1]["quantity"] == 100
    assert result["operational_state"]["events_applied"] == 2
