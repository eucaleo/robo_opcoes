from __future__ import annotations

import inspect

import pytest

from rtd_excel_online import fase7_rtd_option_quotes_service as service
from rtd_excel_online.fase7_alertas_decisao import (
    ParametrosAlerta,
    ResultadoAvaliacao,
)


class FakeQuoteProvider:
    def __init__(self, row):
        self.row = row
        self.codigo_recebido = None

    def get_by_codigo_opcao(self, codigo):
        self.codigo_recebido = codigo
        return self.row


def test_avalia_codigo_opcao_local_com_provider_injetado():
    row = {
        "codigo_opcao": "bovae195",
        "ultimo_preco": "1,23",
        "vwap": "1,20",
        "bid": "1,00",
        "ask": "1,08",
        "volume": "1500",
        "updated_at": "2026-07-11T10:00:00-03:00",
    }

    provider = FakeQuoteProvider(row)

    resultado = service.avaliar_codigo_opcao_local(
        " bovae195 ",
        ParametrosAlerta(),
        quote_provider=provider,
    )

    assert provider.codigo_recebido == "BOVAE195"
    assert isinstance(resultado, ResultadoAvaliacao)


def test_retorna_snapshot_mercado_por_codigo_opcao_local():
    row = {
        "codigo_opcao": "bovae195",
        "ultimo_preco": "1,23",
        "vwap": "1,20",
        "bid": "1,00",
        "ask": "1,08",
        "volume": "1500",
        "updated_at": "2026-07-11T10:00:00-03:00",
    }

    provider = FakeQuoteProvider(row)

    snapshot = service.snapshot_mercado_from_codigo_opcao_local(
        "bovae195",
        quote_provider=provider,
    )

    assert snapshot.simbolo == "BOVAE195"
    assert snapshot.ultimo_preco == 1.23
    assert snapshot.vwap == 1.20
    assert snapshot.bid == 1.00
    assert snapshot.ask == 1.08
    assert snapshot.volume == 1500.0


def test_levanta_erro_quando_cotacao_nao_existe():
    provider = FakeQuoteProvider(None)

    with pytest.raises(service.CotacaoRtdNaoEncontrada):
        service.avaliar_codigo_opcao_local(
            "BOVAE999",
            quote_provider=provider,
        )


def test_codigo_opcao_obrigatorio():
    with pytest.raises(ValueError):
        service.avaliar_codigo_opcao_local(
            "",
            quote_provider=lambda codigo: None,
        )


def test_service_nao_depende_de_integracoes_externas_pesadas():
    source = inspect.getsource(service).lower()

    forbidden_terms = (
        "win32com",
        "xlwings",
        "openpyxl",
        "pywin32",
        "subprocess",
    )

    for term in forbidden_terms:
        assert term not in source
