import pytest

from services.structure_leg_rtd_enrichment_service import (
    StructureLegRtdEnrichmentService,
)


class FakeRtdOptionQuotesRepository:
    def __init__(self, rows):
        self.rows = rows
        self.requested_codigo = None

    def get_by_codigo(self, codigo_opcao):
        self.requested_codigo = codigo_opcao
        return self.rows.get(codigo_opcao)


def test_enrich_leg_from_symbol_uses_rtd_quote_and_returns_canonical_leg():
    repo = FakeRtdOptionQuotesRepository(
        {
            "BOVA11C130": {
                "codigo_opcao": "BOVA11C130",
                "ativo_base": "BOVA11",
                "call_put": "CALL",
                "strike": 130.0,
                "vencimento": "2026-07-17",
            }
        }
    )
    service = StructureLegRtdEnrichmentService(repo)

    leg = service.enrich(
        {
            "symbol": " bova11c130 ",
            "position_side": "C",
            "quantity": 100,
            "premium": 1.25,
            "leg_order": 0,
            "notes": "entrada via simbolo",
        }
    )

    assert repo.requested_codigo == "BOVA11C130"
    assert leg == {
        "symbol": "BOVA11C130",
        "position_side": "COMPRADO",
        "option_type": "CALL",
        "strike": 130.0,
        "expiration_date": "2026-07-17",
        "quantity": 100.0,
        "premium": 1.25,
        "multiplier": 100.0,
        "leg_order": 0,
        "notes": "entrada via simbolo",
        "underlying_asset": "BOVA11",
    }


def test_enrich_leg_accepts_codigo_opcao_as_symbol_alias():
    repo = FakeRtdOptionQuotesRepository(
        {
            "PETR4P2800": {
                "codigo_opcao": "PETR4P2800",
                "ativo_base": "PETR4",
                "call_put": "PUT",
                "strike": 28.0,
                "vencimento": "2026-08-21",
            }
        }
    )
    service = StructureLegRtdEnrichmentService(repo)

    leg = service.enrich(
        {
            "codigo_opcao": "PETR4P2800",
            "position_side": "V",
            "quantity": "200",
        }
    )

    assert leg["symbol"] == "PETR4P2800"
    assert leg["position_side"] == "VENDIDO"
    assert leg["option_type"] == "PUT"
    assert leg["strike"] == 28.0
    assert leg["expiration_date"] == "2026-08-21"
    assert leg["quantity"] == 200.0
    assert leg["premium"] == 0.0
    assert leg["multiplier"] == 100.0
    assert leg["leg_order"] == 0
    assert leg["notes"] is None
    assert leg["underlying_asset"] == "PETR4"


def test_enrich_leg_raises_value_error_when_symbol_is_missing():
    service = StructureLegRtdEnrichmentService(
        FakeRtdOptionQuotesRepository({})
    )

    with pytest.raises(ValueError, match="symbol is required"):
        service.enrich(
            {
                "position_side": "C",
                "quantity": 100,
            }
        )


def test_enrich_leg_raises_value_error_when_rtd_quote_is_not_found():
    service = StructureLegRtdEnrichmentService(
        FakeRtdOptionQuotesRepository({})
    )

    with pytest.raises(ValueError, match="option quote not found"):
        service.enrich(
            {
                "symbol": "BOVA11C999",
                "position_side": "C",
                "quantity": 100,
            }
        )


def test_enrich_leg_raises_value_error_when_rtd_quote_has_missing_required_fields():
    service = StructureLegRtdEnrichmentService(
        FakeRtdOptionQuotesRepository(
            {
                "BOVA11C130": {
                    "codigo_opcao": "BOVA11C130",
                    "ativo_base": "BOVA11",
                    "call_put": "CALL",
                    "strike": 130.0,
                }
            }
        )
    )

    with pytest.raises(ValueError, match="missing required RTD field"):
        service.enrich(
            {
                "symbol": "BOVA11C130",
                "position_side": "C",
                "quantity": 100,
            }
        )
