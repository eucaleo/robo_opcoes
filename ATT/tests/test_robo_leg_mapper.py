from datetime import datetime

import pytest

from services.robo_leg_mapper import to_canonical_leg


def test_to_canonical_leg_should_map_long_call():
    leg = {
        "cv": "C",
        "call_put": "CALL",
        "ativo": " bovae195 ",
        "strike": 195.0,
        "vencimento": datetime(2026, 5, 15),
        "quant": 5000,
        "preco": 1.23,
    }

    result = to_canonical_leg(leg)

    assert result["position_side"] == "LONG"
    assert result["option_type"] == "CALL"
    assert result["symbol"] == "BOVAE195"
    assert result["strike"] == 195.0
    assert result["expiration_date"] == "2026-05-15"
    assert result["quantity"] == 5000
    assert result["premium"] == 1.23
    assert result["multiplier"] == 1.0


def test_to_canonical_leg_should_map_short_put():
    leg = {
        "cv": "V",
        "call_put": "PUT",
        "ativo": " bovao185 ",
        "strike": 185.0,
        "vencimento": datetime(2026, 5, 15),
        "quant": 1000,
        "preco": 0.98,
    }

    result = to_canonical_leg(leg)

    assert result["position_side"] == "SHORT"
    assert result["option_type"] == "PUT"
    assert result["symbol"] == "BOVAO185"
    assert result["expiration_date"] == "2026-05-15"


def test_to_canonical_leg_should_raise_for_invalid_cv():
    leg = {
        "cv": "X",
        "call_put": "CALL",
        "ativo": "BOVAE195",
        "strike": 195.0,
        "vencimento": datetime(2026, 5, 15),
        "quant": 1,
        "preco": 1.0,
    }

    with pytest.raises(ValueError, match=r"invalid cv: X"):
        to_canonical_leg(leg)


def test_to_canonical_leg_should_raise_for_invalid_call_put():
    leg = {
        "cv": "C",
        "call_put": "XXX",
        "ativo": "BOVAE195",
        "strike": 195.0,
        "vencimento": datetime(2026, 5, 15),
        "quant": 1,
        "preco": 1.0,
    }

    with pytest.raises(ValueError, match=r"invalid call_put: XXX"):
        to_canonical_leg(leg)


def test_to_canonical_leg_should_raise_for_invalid_strike():
    leg = {
        "cv": "C",
        "call_put": "CALL",
        "ativo": "BOVAE195",
        "strike": "abc",
        "vencimento": datetime(2026, 5, 15),
        "quant": 1,
        "preco": 1.0,
    }

    with pytest.raises(ValueError, match=r"invalid strike: abc"):
        to_canonical_leg(leg)


def test_to_canonical_leg_should_raise_for_invalid_quant():
    leg = {
        "cv": "C",
        "call_put": "CALL",
        "ativo": "BOVAE195",
        "strike": 195.0,
        "vencimento": datetime(2026, 5, 15),
        "quant": "abc",
        "preco": 1.0,
    }

    with pytest.raises(ValueError, match=r"invalid quant: abc"):
        to_canonical_leg(leg)
