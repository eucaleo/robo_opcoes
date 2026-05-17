from datetime import datetime

from dto.robo_leg_dto import CallPutType, CVType, FonteType, RoboLegDTO
from services.robo_leg_mapper import to_canonical_leg


def test_to_canonical_leg_maps_dto_to_uppercase_canonical_dict():
    leg = RoboLegDTO(
        aba="BOVA11",
        timestamp=datetime(2026, 5, 16, 10, 0, 0),
        cv=CVType.C,
        call_put=CallPutType.CALL,
        strike=120.5,
        quant=2,
        ativo=" bova11c001 ",
        vencimento=datetime(2026, 6, 20),
        fonte=FonteType.MANUAL,
        preco=1.75,
    )

    result = to_canonical_leg(leg, multiplier=100)

    assert result == {
        "position_side": "LONG",
        "option_type": "CALL",
        "symbol": "BOVA11C001",
        "strike": 120.5,
        "expiration_date": "2026-06-20",
        "quantity": 2,
        "premium": 1.75,
        "multiplier": 100.0,
    }


def test_to_canonical_leg_maps_dict_input():
    leg = {
        "cv": "V",
        "call_put": "PUT",
        "ativo": " petr4p123 ",
        "strike": 31.2,
        "vencimento": datetime(2026, 7, 15),
        "quant": 5,
        "preco": 0.88,
    }

    result = to_canonical_leg(leg)

    assert result == {
        "position_side": "SHORT",
        "option_type": "PUT",
        "symbol": "PETR4P123",
        "strike": 31.2,
        "expiration_date": "2026-07-15",
        "quantity": 5,
        "premium": 0.88,
        "multiplier": 1.0,
    }


def test_to_canonical_leg_returns_none_symbol_and_expiration_when_missing():
    leg = {
        "cv": "C",
        "call_put": "PUT",
        "ativo": None,
        "strike": 10,
        "vencimento": None,
        "quant": 1,
        "preco": None,
    }

    result = to_canonical_leg(leg)

    assert result["position_side"] == "LONG"
    assert result["option_type"] == "PUT"
    assert result["symbol"] is None
    assert result["expiration_date"] is None
    assert result["premium"] is None
    assert result["multiplier"] == 1.0
