import sqlite3
from types import SimpleNamespace

import pytest

from services.canonical_pricing_facade import _snapshot_result_to_payload


def _selection(**overrides):
    defaults = {
        "legs": [],
        "spot_price": 124.66,
        "source": "rtd",
        "aba": "ABA_LEGADA_NAO_E_UNDERLYING",
        "manual_overrides": [],
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_snapshot_result_to_payload_uses_explicit_underlying_asset_not_legacy_aba(tmp_path):
    selection = _selection(
        aba="SMAL11_ABA_LEGADA",
        legs=[
            {
                "quantity": "-100",
                "price": "R$ 1,25",
                "asset": "SMALF100",
                "option_type": "CALL",
                "strike": "100,00",
                "expiry": "2026-07-17T12:00:00",
                "source": "rtd_option_quotes",
            }
        ],
        spot_price="124,66",
        manual_overrides=["price"],
    )

    payload = _snapshot_result_to_payload(
        selection_result=selection,
        structure_id=10,
        underlying_asset="SMAL11",
        reference_date="2026-06-19",
        db_path=tmp_path / "app.db",
    )

    assert payload["structure_id"] == 10
    assert payload["underlying_asset"] == "SMAL11"
    assert payload["reference_date"] == "2026-06-19"
    assert payload["spot_price"] == 124.66

    assert payload["meta"] == {
        "snapshot_source": "rtd",
        "snapshot_aba": "SMAL11_ABA_LEGADA",
        "manual_overrides": ["price"],
        "legs_count": 1,
    }

    leg = payload["legs"][0]
    assert leg["asset"] == "SMALF100"
    assert leg["symbol"] == "SMALF100"
    assert leg["price"] == 1.25
    assert leg["premium"] == 1.25
    assert leg["strike"] == 100.0
    assert leg["expiry"] == "2026-07-17T12:00:00"
    assert leg["expiration_date"] == "2026-07-17"
    assert leg["side"] == "SHORT"
    assert leg["position_side"] == "SHORT"
    assert leg["source"] == "rtd_option_quotes"


@pytest.mark.parametrize(
    "leg_input, expected_side",
    [
        ({"quantity": "100", "price": 2.5, "asset": "ABCD100"}, "LONG"),
        ({"quantity": "-100", "price": 2.5, "asset": "ABCD100"}, "SHORT"),
        ({"quantity": "100", "price": 2.5, "asset": "ABCD100", "side": "short"}, "SHORT"),
        ({"quantity": "-100", "price": 2.5, "asset": "ABCD100", "position_side": "long"}, "LONG"),
    ],
)
def test_snapshot_result_to_payload_side_matrix(tmp_path, leg_input, expected_side):
    payload = _snapshot_result_to_payload(
        selection_result=_selection(legs=[leg_input]),
        structure_id=20,
        underlying_asset="ABCD11",
        reference_date=None,
        db_path=tmp_path / "app.db",
    )

    leg = payload["legs"][0]
    assert leg["side"] == expected_side
    assert leg["position_side"] == expected_side


def test_snapshot_result_to_payload_uses_spot_fallback_from_database(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("CREATE TABLE market_prices (underlying_asset TEXT, spot REAL)")
        conn.execute(
            "INSERT INTO market_prices (underlying_asset, spot) VALUES (?, ?)",
            ("SMAL11", 124.66),
        )
        conn.commit()

    payload = _snapshot_result_to_payload(
        selection_result=_selection(spot_price=0, legs=[]),
        structure_id=30,
        underlying_asset="SMAL11",
        reference_date="2026-06-19",
        db_path=db_path,
    )

    assert payload["spot_price"] == 124.66
    assert payload["legs"] == []
    assert payload["meta"]["legs_count"] == 0


def test_snapshot_result_to_payload_rejects_missing_or_invalid_spot(tmp_path):
    with pytest.raises(ValueError) as exc:
        _snapshot_result_to_payload(
            selection_result=_selection(spot_price=0, legs=[]),
            structure_id=40,
            underlying_asset="SMAL11",
            reference_date="2026-06-19",
            db_path=tmp_path / "app.db",
        )

    assert "spot_price inválido ou ausente para underlying_asset=SMAL11" in str(exc.value)
    assert "Não persistir execução OK com spot_price <= 0" in str(exc.value)
