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

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="manual",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
    )

    assert price == 5.55
    assert price_source == "manual"
    assert traceability["price_resolution_status"] == "ok"
    assert traceability["rtd_quote_found"] is None
    assert traceability["rtd_validation_status"] == "not_applicable"
    assert "manual explícito" in traceability["rtd_validation_message"]
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

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
    )

    assert price == 9.99
    assert price_source == "rtd_option_quotes"
    assert repository.calls == ["ABCD11"]


def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_when_no_rtd_quote():
    repository = FakeRtdOptionQuotesRepository()

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
    )

    assert price == 5.55
    assert price_source == "snapshot"
    assert traceability["price_resolution_status"] == "missing_rtd_quote"
    assert traceability["rtd_quote_found"] is False
    assert traceability["rtd_validation_status"] == "error"
    assert "não encontrada" in traceability["rtd_validation_message"]


def test_resolve_effective_leg_price_falls_back_to_original_snapshot_price_on_repository_error():
    repository = FakeRtdOptionQuotesRepository(fail=True)

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
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

def test_resolve_effective_leg_price_exposes_rtd_quote_traceability_metadata():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ativo_base": "ABCD",
                "ultimo_preco": 9.99,
                "source": "rtd_option_quotes",
                "updated_at": "2026-06-15T10:01:00",
                "created_at": "2026-06-15T10:00:00",
            }
        }
    )

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
    )

    assert price == 9.99
    assert price_source == "rtd_option_quotes"
    assert traceability == {
        "price_resolution_status": "ok",
        "rtd_quote_found": True,
        "rtd_validation_status": "ok",
        "rtd_validation_message": None,
        "rtd_price_field": "ultimo_preco",
        "rtd_quote_codigo_opcao": "ABCD11",
        "rtd_quote_ativo_base": "ABCD",
        "rtd_price_source": "rtd_option_quotes",
        "rtd_price_updated_at": "2026-06-15T10:01:00",
        "rtd_price_created_at": "2026-06-15T10:00:00",
    }


def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_has_no_usable_price():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ativo_base": "ABCD",
                "ultimo_preco": 0,
                "price": 0,
                "last_price": 0,
                "bid": 0,
                "ask": 0,
                "source": "rtd_option_quotes",
                "updated_at": "2026-06-15T10:01:00",
                "created_at": "2026-06-15T10:00:00",
            }
        }
    )

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
    )

    assert price == 5.55
    assert price_source == "snapshot"
    assert traceability["price_resolution_status"] == "invalid_rtd_price"
    assert traceability["rtd_quote_found"] is True
    assert traceability["rtd_validation_status"] == "error"
    assert "sem preço utilizável" in traceability["rtd_validation_message"]
    assert traceability["rtd_quote_codigo_opcao"] == "ABCD11"
    assert traceability["rtd_quote_ativo_base"] == "ABCD"
    assert traceability["rtd_price_source"] == "rtd_option_quotes"
    assert traceability["rtd_price_updated_at"] == "2026-06-15T10:01:00"
    assert traceability["rtd_price_created_at"] == "2026-06-15T10:00:00"


def test_snapshot_result_to_payload_does_not_leak_rtd_traceability_for_manual_price(tmp_path):
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ativo_base": "ABCD",
                "ultimo_preco": 9.99,
                "source": "rtd_option_quotes",
                "updated_at": "2026-06-15T10:01:00",
                "created_at": "2026-06-15T10:00:00",
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
                "source": "manual",
                "side": "LONG",
            }
        ],
        spot_price=100.0,
        source="manual",
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

    assert leg["price"] == 5.55
    assert leg["premium"] == 5.55
    assert leg["price_source"] == "manual"
    assert "rtd_price_field" not in leg
    assert "rtd_quote_codigo_opcao" not in leg
    assert "rtd_quote_ativo_base" not in leg
    assert "rtd_price_source" not in leg
    assert "rtd_price_updated_at" not in leg
    assert "rtd_price_created_at" not in leg
    assert repository.calls == []


def test_resolve_effective_leg_price_diagnoses_missing_rtd_quote():
    repository = FakeRtdOptionQuotesRepository()

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
        underlying_asset="ABCD",
    )

    assert price == 5.55
    assert price_source == "snapshot"
    assert traceability["rtd_quote_found"] is False
    assert traceability["price_resolution_status"] == "missing_rtd_quote"
    assert traceability["rtd_validation_status"] == "error"
    assert "não encontrada" in traceability["rtd_validation_message"]


def test_resolve_effective_leg_price_diagnoses_invalid_rtd_price():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ativo_base": "ABCD",
                "ultimo_preco": 0,
                "price": 0,
                "last_price": 0,
                "bid": 0,
                "ask": 0,
                "source": "rtd_option_quotes",
            }
        }
    )

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
        underlying_asset="ABCD",
    )

    assert price == 5.55
    assert price_source == "snapshot"
    assert traceability["rtd_quote_found"] is True
    assert traceability["price_resolution_status"] == "invalid_rtd_price"
    assert traceability["rtd_validation_status"] == "error"
    assert traceability["rtd_quote_codigo_opcao"] == "ABCD11"
    assert traceability["rtd_quote_ativo_base"] == "ABCD"


def test_resolve_effective_leg_price_diagnoses_rtd_asset_mismatch():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ativo_base": "WXYZ",
                "ultimo_preco": 9.99,
                "source": "rtd_option_quotes",
            }
        }
    )

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
        underlying_asset="ABCD",
    )

    assert price == 5.55
    assert price_source == "snapshot"
    assert traceability["rtd_quote_found"] is True
    assert traceability["price_resolution_status"] == "rtd_asset_mismatch"
    assert traceability["rtd_validation_status"] == "error"
    assert traceability["rtd_quote_ativo_base"] == "WXYZ"
    assert "diverge" in traceability["rtd_validation_message"]


def test_snapshot_result_to_payload_preserves_rtd_guardrails_for_valid_quote(tmp_path):
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ativo_base": "ABCD",
                "ultimo_preco": 9.99,
                "source": "rtd_option_quotes",
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

    assert leg["price_source"] == "rtd_option_quotes"
    assert leg["price_resolution_status"] == "ok"
    assert leg["rtd_quote_found"] is True
    assert leg["rtd_validation_status"] == "ok"
    assert leg["rtd_validation_message"] is None
    assert leg["rtd_price_field"] == "ultimo_preco"
    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert leg["rtd_quote_ativo_base"] == "ABCD"


def test_snapshot_result_to_payload_preserves_rtd_guardrails_when_falling_back_to_snapshot(tmp_path):
    repository = FakeRtdOptionQuotesRepository()

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

    assert leg["price"] == 5.55
    assert leg["premium"] == 5.55
    assert leg["price_source"] == "snapshot"
    assert leg["price_resolution_status"] == "missing_rtd_quote"
    assert leg["rtd_quote_found"] is False
    assert leg["rtd_validation_status"] == "error"

def test_resolve_effective_leg_price_falls_back_to_snapshot_when_rtd_quote_is_stale():
    repository = FakeRtdOptionQuotesRepository(
        quotes={
            "ABCD11": {
                "codigo_opcao": "ABCD11",
                "ultimo_preco": 9.99,
                "bid": 9.50,
                "ask": 10.50,
                "updated_at": "2000-01-01 00:00:00",
            }
        }
    )

    price, price_source, traceability = _resolve_effective_leg_price(
        raw_price=5.55,
        raw_asset="ABCD11",
        leg_source="rtd",
        rtd_option_quotes_repository=repository,
        reference_date="2026-06-15",
    )

    assert price == 5.55
    assert price_source == "snapshot"
    assert traceability["price_resolution_status"] == "stale_rtd_quote"
    assert traceability["rtd_quote_found"] is True
    assert traceability["rtd_validation_status"] == "warn"
    assert "vencida" in traceability["rtd_validation_message"]
