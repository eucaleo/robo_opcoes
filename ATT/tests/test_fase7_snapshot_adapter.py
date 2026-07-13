from __future__ import annotations

import inspect
from types import SimpleNamespace

from rtd_excel_online import fase7_snapshot_adapter as adapter
from rtd_excel_online.fase7_alertas_decisao import ParametrosAlerta


def test_converte_rtd_option_quote_dict_para_snapshot_mercado():
    row = {
        "codigo_opcao": " bovae195 ",
        "ultimo_preco": "1,23",
        "vwap": "1,20",
        "bid": "1,00",
        "ask": "1,08",
        "volume": "1500",
        "updated_at": "2026-07-11T10:00:00-03:00",
    }

    snapshot = adapter.snapshot_mercado_from_rtd_option_quote(row)

    assert snapshot.simbolo == "BOVAE195"
    assert snapshot.ultimo_preco == 1.23
    assert snapshot.vwap == 1.20
    assert snapshot.bid == 1.00
    assert snapshot.ask == 1.08
    assert snapshot.volume == 1500.0


def test_avaliar_rtd_option_quote_usa_snapshot_local_e_timestamp():
    row = {
        "codigo_opcao": "BOVAE195",
        "ultimo_preco": "1,23",
        "vwap": "1,20",
        "bid": "1,00",
        "ask": "1,08",
        "volume": "10",
        "updated_at": "2026-07-11T10:00:00-03:00",
    }

    resultado = adapter.avaliar_rtd_option_quote(
        row,
        ParametrosAlerta(
            max_spread_pct=0.03,
            min_volume=100,
        ),
    )

    regras = {alerta.regra for alerta in resultado.alertas}

    assert resultado.simbolo == "BOVAE195"
    assert resultado.timestamp == "2026-07-11T10:00:00-03:00"
    assert "SPREAD_ANORMAL" in regras
    assert "LIQUIDEZ_BAIXA" in regras
    assert "PRECO_ACIMA_VWAP" in regras
    assert resultado.decisao.classificacao == "EVITAR_OPERACAO"
    assert resultado.decisao.permite_execucao is False


def test_converte_leg_market_snapshot_like_object_sem_depender_do_dominio():
    leg = SimpleNamespace(
        ativo="bovae195",
        valor_executado="1,23",
        mid=1.22,
        bid="1,20",
        ask="1,26",
        pl_realista="25,5",
        timestamp="2026-07-11T10:05:00-03:00",
    )

    snapshot = adapter.snapshot_mercado_from_leg_market_snapshot(
        leg,
        vwap="1,10",
        payoff_anterior="20",
    )

    assert snapshot.simbolo == "BOVAE195"
    assert snapshot.ultimo_preco == 1.23
    assert snapshot.vwap == 1.10
    assert snapshot.bid == 1.20
    assert snapshot.ask == 1.26
    assert snapshot.payoff_anterior == 20.0
    assert snapshot.payoff_atual == 25.5


def test_adapter_nao_importa_dependencias_de_excel_com_ou_subprocesso():
    source = inspect.getsource(adapter).lower()

    forbidden_terms = {
        "win32com",
        "xlwings",
        "openpyxl",
        "subprocess",
        "popen",
        "check_output",
        "os.system",
        "excel.application",
    }

    for term in forbidden_terms:
        assert term not in source
