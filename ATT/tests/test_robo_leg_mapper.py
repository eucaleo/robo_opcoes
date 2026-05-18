from datetime import datetime

import pytest

from services.robo_leg_mapper import to_canonical_leg


class FakeEnum:
    def __init__(self, value):
        self.value = value


class FakeLegObject:
    def __init__(
        self,
        cv,
        call_put,
        ativo,
        strike,
        vencimento,
        quant,
        preco,
    ):
        self.cv = cv
        self.call_put = call_put
        self.ativo = ativo
        self.strike = strike
        self.vencimento = vencimento
        self.quant = quant
        self.preco = preco


def test_to_canonical_leg_maps_valid_dict_input():
    leg = {
        "cv": "C",
        "call_put": "PUT",
        "ativo": " bovam190 ",
        "strike": "190",
        "vencimento": datetime(2026, 5, 15),
        "quant": "2000",
        "preco": "1.25",
    }

    result = to_canonical_leg(leg, multiplier=100)

    assert result == {
        "position_side": "LONG",
        "option_type": "PUT",
        "symbol": "BOVAM190",
        "strike": 190.0,
        "expiration_date": "2026-05-15",
        "quantity": 2000,
        "premium": 1.25,
        "multiplier": 100.0,
    }


def test_to_canonical_leg_maps_valid_object_and_enum_input():
    leg = FakeLegObject(
        cv=FakeEnum("V"),
        call_put=FakeEnum("CALL"),
        ativo=" bovaM210 ",
        strike=210,
        vencimento=datetime(2026, 6, 19),
        quant=10,
        preco=None,
    )

    result = to_canonical_leg(leg, multiplier=1)

    assert result == {
        "position_side": "SHORT",
        "option_type": "CALL",
        "symbol": "BOVAM210",
        "strike": 210.0,
        "expiration_date": "2026-06-19",
        "quantity": 10,
        "premium": None,
        "multiplier": 1.0,
    }


def test_to_canonical_leg_raises_for_invalid_cv():
    leg = {
        "cv": "X",
        "call_put": "PUT",
        "ativo": "BOVAM190",
        "strike": 190,
        "vencimento": datetime(2026, 5, 15),
        "quant": 1,
        "preco": None,
    }

    with pytest.raises(ValueError, match="invalid cv: X"):
        to_canonical_leg(leg)


def test_to_canonical_leg_raises_for_invalid_call_put():
    leg = {
        "cv": "C",
        "call_put": "INVALID",
        "ativo": "BOVAM190",
        "strike": 190,
        "vencimento": datetime(2026, 5, 15),
        "quant": 1,
        "preco": None,
    }

    with pytest.raises(ValueError, match="invalid call_put: INVALID"):
        to_canonical_leg(leg)
