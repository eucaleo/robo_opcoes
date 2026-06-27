from services.payoff_pricing_engine import PayoffPricingEngine


def test_payoff_engine_uses_mtm_when_current_option_price_is_available():
    engine = PayoffPricingEngine()

    result = engine.run(
        {
            "structure_id": 1,
            "underlying_asset": "TESTE",
            "reference_date": "2026-06-27",
            "spot_price": 100.0,
            "market_snapshot_source": "rtd_underlying_quotes",
            "legs": [
                {
                    "symbol": "TESTC100",
                    "option_type": "CALL",
                    "position_side": "LONG",
                    "strike": 100.0,
                    "quantity": 100,
                    "multiplier": 1,
                    "premium": 2.0,
                    "current_price": 3.0,
                    "current_price_source": "rtd_option_quotes.ultimo_preco",
                }
            ],
        }
    )

    assert result["valuation"]["method"] == "expiration_payoff_grid_with_mark_to_market"
    assert result["valuation"]["pl_atual_source"] == "mark_to_market"
    assert result["valuation"]["pl_atual_mtm"] == 100.0
    assert result["valuation"]["pl_atual"] == 100.0

    assert result["valuation"]["payoff_at_spot"] == -200.0
    assert result["metrics"]["mtm_complete"] is True
    assert result["valuation"]["leg_valuations"][0]["pl_mtm"] == 100.0


def test_payoff_engine_mtm_handles_short_leg():
    engine = PayoffPricingEngine()

    result = engine.run(
        {
            "structure_id": 1,
            "underlying_asset": "TESTE",
            "reference_date": "2026-06-27",
            "spot_price": 100.0,
            "market_snapshot_source": "rtd_underlying_quotes",
            "legs": [
                {
                    "symbol": "TESTC100",
                    "option_type": "CALL",
                    "position_side": "SHORT",
                    "strike": 100.0,
                    "quantity": 10,
                    "multiplier": 1,
                    "premium": 5.0,
                    "current_price": 3.0,
                    "current_price_source": "rtd_option_quotes.ultimo_preco",
                }
            ],
        }
    )

    assert result["valuation"]["pl_atual_mtm"] == 20.0
    assert result["valuation"]["pl_atual"] == 20.0
    assert result["valuation"]["leg_valuations"][0]["pl_mtm"] == 20.0


def test_payoff_engine_keeps_payoff_at_spot_when_mtm_price_is_missing():
    engine = PayoffPricingEngine()

    result = engine.run(
        {
            "structure_id": 1,
            "underlying_asset": "TESTE",
            "reference_date": "2026-06-27",
            "spot_price": 100.0,
            "market_snapshot_source": "rtd_underlying_quotes",
            "legs": [
                {
                    "symbol": "TESTC100",
                    "option_type": "CALL",
                    "position_side": "LONG",
                    "strike": 100.0,
                    "quantity": 100,
                    "multiplier": 1,
                    "premium": 2.0,
                }
            ],
        }
    )

    assert result["valuation"]["method"] == "expiration_payoff_grid"
    assert result["valuation"]["pl_atual_source"] == "expiration_payoff_at_spot"
    assert result["valuation"]["pl_atual_mtm"] is None
    assert result["valuation"]["payoff_at_spot"] == -200.0
    assert result["valuation"]["pl_atual"] == -200.0
    assert result["metrics"]["mtm_complete"] is False
