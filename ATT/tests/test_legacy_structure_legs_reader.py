from datetime import datetime
from types import SimpleNamespace

import pytest

from services.legacy_structure_legs_reader import LegacyStructureLegsReader


class FakeRoboLegsRepository:
    def __init__(self, legs):
        self.legs = legs
        self.calls = []

    def get_legs_by_structure_id(self, structure_id, timestamp):
        self.calls.append(
            {
                "structure_id": structure_id,
                "timestamp": timestamp,
            }
        )
        return self.legs


def test_read_by_structure_id_maps_legacy_legs_to_structure_legs_payload():
    legacy_legs = [
        SimpleNamespace(
            cv="C",
            call_put="CALL",
            ativo=" bovae195 ",
            strike=195.0,
            vencimento=datetime(2026, 5, 15),
            quant=5000,
            preco=1.23,
        ),
        SimpleNamespace(
            cv="V",
            call_put="PUT",
            ativo=" bovao185 ",
            strike=185.0,
            vencimento=datetime(2026, 5, 15),
            quant=1000,
            preco=0.98,
        ),
    ]

    repo = FakeRoboLegsRepository(legacy_legs)
    reader = LegacyStructureLegsReader(robo_legs_repository=repo)

    result = reader.read_by_structure_id(
        structure_id=123,
        timestamp="2026-05-19 10:00:00",
    )

    assert repo.calls == [
        {
            "structure_id": 123,
            "timestamp": "2026-05-19 10:00:00",
        }
    ]

    assert result == [
        {
            "position_side": "LONG",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-05-15",
            "quantity": 5000,
            "premium": 1.23,
            "multiplier": 1.0,
            "leg_order": 1,
        },
        {
            "position_side": "SHORT",
            "option_type": "PUT",
            "symbol": "BOVAO185",
            "strike": 185.0,
            "expiration_date": "2026-05-15",
            "quantity": 1000,
            "premium": 0.98,
            "multiplier": 1.0,
            "leg_order": 2,
        },
    ]


def test_read_by_structure_id_propagates_mapper_errors():
    legacy_legs = [
        SimpleNamespace(
            cv="X",
            call_put="CALL",
            ativo="BOVAE195",
            strike=195.0,
            vencimento=datetime(2026, 5, 15),
            quant=1,
            preco=1.0,
        ),
    ]

    reader = LegacyStructureLegsReader(
        robo_legs_repository=FakeRoboLegsRepository(legacy_legs)
    )

    with pytest.raises(ValueError, match=r"invalid cv: X"):
        reader.read_by_structure_id(
            structure_id=123,
            timestamp="2026-05-19 10:00:00",
        )
