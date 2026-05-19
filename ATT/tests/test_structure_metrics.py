from domain.structure_metrics import compute_dte, compute_dte_min_from_canonical_input


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
