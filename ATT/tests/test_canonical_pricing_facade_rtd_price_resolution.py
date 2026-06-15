from types import SimpleNamespace

from services.canonical_pricing_facade import (
    _lookup_rtd_option_quote,
    _pick_rtd_option_price,
    _resolve_effective_leg_price,
    _snapshot_result_to_payload,
)


class FakeRtdOptionQuotesRepository:
    def __init__(self, quotes=None, fail=False):
        self.quotes = quotes or {}
        self.fail = fail
        self.calls = []

    def get_by_codigo(self, codigo_opcao):
        self.calls.append(codigo_opcao)

        if self.fail:
            raise RuntimeError("simulated repository failure")

        return self.quotes.get(codigo_opcao)


def test_pick_rtd_option_price_prefers_ultimo_preco():
    quote = {
        "ultimo_preco": 10.5,
        "price": 11.5,
        "last_price": 12.5,
        "bid": 9.0,
        "ask": 10.0,
    }

    assert _pick_rtd_option_price(quote) == 10.5


def test_pick_rtd_option_price_falls_back_to_price_and_last_price():
    assert _pick_rtd_option_price({"ultimo_preco": 0, "price": 11.5}) == 11.5
    assert _pick_rtd_option_price({"ultimo_preco": None, "price": 0, "last_price": "12,50"}) == 12.5


def test_pick_rtd_option_price_falls_back_to_bid_ask_mid():
    quote = {
        "ultimo_preco": None,
        "price": None,
        "last_price": None,
        "bid": 2.0,
        "ask": 4.0,
    }

    assert _pick_rtd_option_price(quote) == 3.0


def test_pick_rtd_option_price_falls_back_to_bid_or_ask():
    assert _pick_rtd_option_price({"bid": 2.0, "ask": 0}) == 2.0
    assert _pick_rtd_option_price({"bid": 0, "ask": 4.0}) == 4.0


def test_pick_rtd_option_price_returns_none_when_no_positive_price_exists():
    assert _pick_rtd_option_price({}) is None
    assert _pick_rtd_option_price({"ultimo_preco": 0, "price": 0, "bid": 0, "ask": 0}) is None


def test_lookup_rtd_option_quote_tries_original_and_uppercase_codigo():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ultimo_preco": 1.23,
            }
        }
    )

    quote = _lookup_rtd_option_quote(repository, "abcd11")

    assert quote["codigo_opcao"] == "ABCD11"
    assert repository.calls == ["abcd11", "ABCD11"]


def test_lookup_rtd_option_quote_returns_none_when_repository_raises():
    repository = FakeRtdOptionQuotesRepository(fail=True)

    quote = _lookup_rtd_option_quote(repository, "ABCD11")

    assert quote is None


def test_resolve_effective_leg_price_preserves_explicit_manual_price():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ultimo_preco": 9.99,
            }
        }
    )

    price, price_source = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="manual",
        rtd_option_quotes_repository=repository,
    )

    assert price == 5.55
    assert price_source == "manual"
    assert repository.calls == []


def test_resolve_effective_leg_price_uses_rtd_when_source_is_not_manual():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ultimo_preco": 9.99,
            }
        }
    )

    price, price_source = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
    )

    assert price == 9.99
    assert price_source == "rtd_option_quotes"
    assert repository.calls == ["ABCD11"]


def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_when_no_rtd_quote():
    repository = FakeRtdOptionQuotesRepository()

    price, price_source = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
    )

    assert price == 5.55
    assert price_source == "snapshot"


def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_on_repository_error():
    repository = FakeRtdOptionQuotesRepository(fail=True)

    price, price_source = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
    )

    assert price == 5.55
    assert price_source == "snapshot"


def test_snapshot_result_to_payload_uses_rtd_price_for_canonical_leg_fields(tmp_path):
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ultimo_preco": 9.99,
            }
        }
    )

    selection_result = SimpleNamespace(
        legs=[
            {
                "quantity": 100,
                "premium": 5.55,
                "symbol": "ABCD11",
                "option_type": "CALL",
                "strike": 10.0,
                "expiration_date": "2026-06-15",
                "source": "rtd",
                "side": "LONG",
            }
        ],
        spot_price=100.0,
        source="rtd",
        aba="ABCD",
        manual_overrides=[],
    )

    payload = _snapshot_result_to_payload(
        selection_result=selection_result,
        structure_id=123,
        underlying_asset="ABCD",
        reference_date="2026-06-15",
        db_path=tmp_path / "app.db",
        rtd_option_quotes_repository=repository,
    )

    leg = payload["legs"][0]

    assert leg["price"] == 9.99
    assert leg["premium"] == 9.99
    assert leg["price_source"] == "rtd_option_quotes"
    assert leg["asset"] == "ABCD11"
    assert leg["symbol"] == "ABCD11"
    assert payload["spot_price"] == 100.0
