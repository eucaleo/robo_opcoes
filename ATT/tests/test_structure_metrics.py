import pytest

from domain.structure_metrics import (
    compute_dte,
    compute_dte_min_from_canonical_input,
    compute_leg_metrics,
    compute_mid,
    compute_pl_realista,
    compute_realistic_price,
    compute_spread,
    compute_spread_pct,
    compute_structure_metrics,
    compute_structure_metrics_from_canonical_input,
    normalize_position_side,
)


def test_compute_dte_same_day():
    assert compute_dte("2026-05-15", "2026-05-15") == 0


def test_compute_dte_future_day():
    assert compute_dte("2026-05-15", "2026-05-20") == 5


def test_compute_dte_should_accept_br_date_format():
    assert compute_dte("15/05/2026", "20/05/2026") == 5


def test_compute_dte_invalid():
    assert compute_dte("2026-05-15", None) is None


def test_compute_dte_min_from_canonical_input():
    canonical_input = {
        "structure": {
            "structure_id": 1,
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "PUT",
                    "strike": 190.0,
                    "expiration_date": "2026-05-20",
                    "quantity": 1,
                },
                {
                    "position_side": "SHORT",
                    "option_type": "PUT",
                    "strike": 185.0,
                    "expiration_date": "2026-05-17",
                    "quantity": 1,
                },
            ],
        },
        "market": {
            "reference_date": "2026-05-15",
            "spot_price": 198.35,
        },
    }

    assert compute_dte_min_from_canonical_input(canonical_input) == 2


def test_compute_mid_spread_and_spread_pct():
    assert compute_mid(10.0, 12.0) == 11.0
    assert compute_spread(10.0, 12.0) == 2.0
    assert compute_spread_pct(10.0, 12.0) == pytest.approx(2.0 / 11.0)


def test_compute_spread_pct_should_return_none_when_mid_is_zero():
    assert compute_spread_pct(0.0, 0.0) is None


def test_normalize_position_side_should_accept_legacy_cv_values():
    assert normalize_position_side({"cv": "C"}) == "LONG"
    assert normalize_position_side({"cv": "V"}) == "SHORT"


def test_compute_realistic_price_for_long_leg_uses_bid_first():
    leg = {
        "cv": "C",
        "bid": 1.20,
        "ask": 1.40,
        "mid": 1.30,
    }

    assert compute_realistic_price(leg) == 1.20


def test_compute_realistic_price_for_short_leg_uses_ask_first():
    leg = {
        "cv": "V",
        "bid": 0.70,
        "ask": 0.80,
        "mid": 0.75,
    }

    assert compute_realistic_price(leg) == 0.80


def test_compute_pl_realista_for_long_leg():
    leg = {
        "cv": "C",
        "quant": 10,
        "valor_executado": 1.00,
        "bid": 1.20,
        "ask": 1.40,
    }

    assert compute_pl_realista(leg) == pytest.approx(2.0)


def test_compute_pl_realista_for_short_leg():
    leg = {
        "cv": "V",
        "quant": 10,
        "valor_executado": 1.00,
        "bid": 0.70,
        "ask": 0.80,
    }

    assert compute_pl_realista(leg) == pytest.approx(2.0)


def test_compute_leg_metrics_for_long_leg():
    leg = {
        "cv": "C",
        "quant": 10,
        "valor_executado": 1.00,
        "bid": 1.20,
        "ask": 1.40,
        "delta": 0.40,
        "gamma": 0.01,
        "theta": -0.02,
        "vega": 0.03,
        "vencimento": "2026-05-20",
    }

    result = compute_leg_metrics(leg, reference_date="2026-05-15")

    assert result["side"] == "LONG"
    assert result["quantity"] == 10
    assert result["mid"] == pytest.approx(1.30)
    assert result["spread"] == pytest.approx(0.20)
    assert result["spread_pct"] == pytest.approx(0.20 / 1.30)
    assert result["preco_realista"] == pytest.approx(1.20)
    assert result["pl_realista"] == pytest.approx(2.0)
    assert result["delta_exposto"] == pytest.approx(4.0)
    assert result["gamma_exposto"] == pytest.approx(0.10)
    assert result["theta_exposto"] == pytest.approx(-0.20)
    assert result["vega_exposto"] == pytest.approx(0.30)
    assert result["dte"] == 5


def test_compute_leg_metrics_for_short_leg():
    leg = {
        "cv": "V",
        "quant": 10,
        "valor_executado": 1.00,
        "bid": 0.70,
        "ask": 0.80,
        "delta": 0.40,
        "gamma": 0.01,
        "theta": -0.02,
        "vega": 0.03,
        "vencimento": "2026-05-17",
    }

    result = compute_leg_metrics(leg, reference_date="2026-05-15")

    assert result["side"] == "SHORT"
    assert result["quantity"] == 10
    assert result["mid"] == pytest.approx(0.75)
    assert result["spread"] == pytest.approx(0.10)
    assert result["spread_pct"] == pytest.approx(0.10 / 0.75)
    assert result["preco_realista"] == pytest.approx(0.80)
    assert result["pl_realista"] == pytest.approx(2.0)
    assert result["delta_exposto"] == pytest.approx(-4.0)
    assert result["gamma_exposto"] == pytest.approx(-0.10)
    assert result["theta_exposto"] == pytest.approx(0.20)
    assert result["vega_exposto"] == pytest.approx(-0.30)
    assert result["dte"] == 2


def test_compute_structure_metrics_should_aggregate_legs():
    legs = [
        {
            "cv": "C",
            "quant": 10,
            "valor_executado": 1.00,
            "bid": 1.20,
            "ask": 1.40,
            "delta": 0.40,
            "gamma": 0.01,
            "theta": -0.02,
            "vega": 0.03,
            "vencimento": "2026-05-20",
        },
        {
            "cv": "V",
            "quant": 10,
            "valor_executado": 1.00,
            "bid": 0.70,
            "ask": 0.80,
            "delta": 0.40,
            "gamma": 0.01,
            "theta": -0.02,
            "vega": 0.03,
            "vencimento": "2026-05-17",
        },
    ]

    result = compute_structure_metrics(legs, reference_date="2026-05-15")

    assert result["num_pernas"] == 2
    assert result["pl_realista_total"] == pytest.approx(4.0)
    assert result["delta_liq"] == pytest.approx(0.0)
    assert result["gamma_liq"] == pytest.approx(0.0)
    assert result["theta_liq"] == pytest.approx(0.0)
    assert result["vega_liq"] == pytest.approx(0.0)
    assert result["spread_medio"] == pytest.approx(0.15)
    assert result["spread_pct_medio"] == pytest.approx(((0.20 / 1.30) + (0.10 / 0.75)) / 2)
    assert result["dte_min"] == 2
    assert len(result["legs"]) == 2


def test_compute_structure_metrics_from_canonical_input():
    canonical_input = {
        "structure": {
            "structure_id": 1,
            "underlying_asset": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "quantity": 10,
                    "execution_price": 1.00,
                    "bid": 1.20,
                    "ask": 1.40,
                    "delta": 0.40,
                    "expiration_date": "2026-05-20",
                },
                {
                    "position_side": "SHORT",
                    "quantity": 10,
                    "execution_price": 1.00,
                    "bid": 0.70,
                    "ask": 0.80,
                    "delta": 0.40,
                    "expiration_date": "2026-05-17",
                },
            ],
        },
        "market": {
            "reference_date": "2026-05-15",
            "spot_price": 198.35,
        },
    }

    result = compute_structure_metrics_from_canonical_input(canonical_input)

    assert result["num_pernas"] == 2
    assert result["pl_realista_total"] == pytest.approx(4.0)
    assert result["delta_liq"] == pytest.approx(0.0)
    assert result["dte_min"] == 2
