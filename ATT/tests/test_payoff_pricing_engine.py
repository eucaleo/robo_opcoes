import pytest

from services.payoff_pricing_engine import PayoffPricingEngine


def test_run_returns_payoff_based_metrics_and_valuation():
    engine = PayoffPricingEngine()

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "spot_price": 100.0,
        "interest_rate": 0.1175,
        "volatility": 0.22,
        "legs": [
            {
                "side": "LONG",
                "option_type": "CALL",
                "strike": 100.0,
                "quantity": 1,
                "multiplier": 100,
                "premium": 5.0,
            }
        ],
    }

    result = engine.run(pricing_payload)

    assert result["engine"] == "payoff_pricing_engine"
    assert result["status"] == "ok"
    assert result["structure_id"] == 123
    assert result["underlying_asset"] == "BOVA11"
    assert result["reference_date"] == "2026-05-16"

    assert result["metrics"]["number_of_legs"] == 1
    assert result["metrics"]["total_quantity"] == 1
    assert result["metrics"]["spot_price"] == 100.0
    assert result["metrics"]["interest_rate"] == 0.1175
    assert result["metrics"]["volatility"] == 0.22
    assert result["metrics"]["payoff_points"] == 101

    assert result["valuation"]["premium_paid"] == 500.0
    assert result["valuation"]["theoretical_value"] == -500.0
    assert result["valuation"]["pl_atual"] == -500.0
    assert result["valuation"]["pl_min"] == -500.0
    assert result["valuation"]["pl_max"] == 4500.0
    assert result["valuation"]["max_profit"] == 4500.0
    assert result["valuation"]["max_loss"] == -500.0

    assert "payoff" in result
    assert len(result["payoff"]["points"]) == 101


def test_run_accepts_position_side_alias():
    engine = PayoffPricingEngine()

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "spot_price": 100.0,
        "interest_rate": 0.0,
        "volatility": 0.0,
        "legs": [
            {
                "position_side": "LONG",
                "option_type": "PUT",
                "strike": 100.0,
                "quantity": 1,
                "multiplier": 100,
                "premium": 4.0,
            }
        ],
    }

    result = engine.run(pricing_payload)

    assert result["status"] == "ok"
    assert result["metrics"]["payoff_points"] == 101


def test_run_raises_when_pricing_payload_is_missing():
    engine = PayoffPricingEngine()

    with pytest.raises(ValueError, match="pricing_payload is required"):
        engine.run({})


def test_run_raises_when_legs_are_missing():
    engine = PayoffPricingEngine()

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "spot_price": 100.0,
        "interest_rate": 0.0,
        "volatility": 0.0,
        "legs": [],
    }

    with pytest.raises(ValueError, match="pricing_payload.legs is required"):
        engine.run(pricing_payload)


def test_run_raises_when_spot_price_is_missing():
    engine = PayoffPricingEngine()

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "spot_price": 0.0,
        "interest_rate": 0.0,
        "volatility": 0.0,
        "legs": [
            {
                "side": "LONG",
                "option_type": "CALL",
                "strike": 100.0,
                "quantity": 1,
                "multiplier": 100,
                "premium": 5.0,
            }
        ],
    }

    with pytest.raises(ValueError, match="pricing_payload.spot_price is required"):
        engine.run(pricing_payload)
