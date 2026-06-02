import pytest

from services.pricing_engine_stub import PricingEngineStub


def test_run_returns_stub_result_with_metrics_and_valuation():
    engine = PricingEngineStub()

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "spot_price": 198.35,
        "interest_rate": 0.1175,
        "volatility": 0.22,
        "legs": [
            {"quantity": 1000},
            {"quantity": 500},
        ],
    }

    result = engine.run(pricing_payload)

    assert result == {
        "engine": "stub",
        "status": "ok",
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "metrics": {
            "number_of_legs": 2,
            "total_quantity": 1500,
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        },
        "valuation": {
            "theoretical_value": 0.0,
            "premium_paid": 0.0,
            "max_profit": None,
            "max_loss": None,
        },
    }


def test_run_raises_when_pricing_payload_is_missing():
    engine = PricingEngineStub()

    with pytest.raises(ValueError, match="pricing_payload is required"):
        engine.run({})


def test_run_raises_when_legs_are_missing():
    engine = PricingEngineStub()

    pricing_payload = {
        "structure_id": 123,
        "underlying_asset": "BOVA11",
        "reference_date": "2026-05-16",
        "spot_price": 198.35,
        "interest_rate": 0.1175,
        "volatility": 0.22,
        "legs": [],
    }

    with pytest.raises(ValueError, match="pricing_payload.legs is required"):
        engine.run(pricing_payload)
