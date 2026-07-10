import sqlite3
from pathlib import Path

from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
from services.rtd_option_quotes_sync_service import (
    sync_rtd_option_quotes_from_excel,
    sync_rtd_option_quotes_records,
)


def test_sync_records_upserts_one_snapshot_row_per_symbol(tmp_path: Path):
    db_path = tmp_path / "app.db"

    first = sync_rtd_option_quotes_records(
        [
            {
                "codigo_opcao": "petrs424",
                "ativo_base": "petr4",
                "call_put": "CALL",
                "strike": 42.4,
                "vencimento": "21-08-2026",
                "ultimo_preco": 1.10,
                "ultima_quantidade": 100,
                "bid": 1.08,
                "ask": 1.12,
                "volume": 1000,
                "vwap": 1.09,
                "iv": 0.31,
                "delta": 0.45,
                "gamma": 0.02,
                "theta": -0.01,
                "vega": 0.07,
            }
        ],
        db_path=db_path,
        read_at="2026-07-09T21:00:00-03:00",
    )

    assert first.ok
    assert first.rows_read == 1
    assert first.rows_upserted == 1

    second = sync_rtd_option_quotes_records(
        [
            {
                "codigo_opcao": "PETRS424",
                "ativo_base": "PETR4",
                "call_put": "CALL",
                "strike": "42,40",
                "vencimento": "21-08-2026",
                "ultimo_preco": "1,25",
                "ultima_quantidade": "200",
                "bid": "1,24",
                "ask": "1,26",
                "volume": "1500",
                "vwap": "1,245",
                "iv": "0,33",
                "delta": "0,47",
                "gamma": "0,021",
                "theta": "-0,011",
                "vega": "0,071",
            }
        ],
        db_path=db_path,
        read_at="2026-07-09T21:01:00-03:00",
    )

    assert second.ok
    assert second.rows_read == 1
    assert second.rows_upserted == 1

    repo = RtdOptionQuotesRepository(db_path)
    quote = repo.get_by_codigo("petrs424")

    assert quote is not None
    assert quote["codigo_opcao"] == "PETRS424"
    assert quote["ativo_base"] == "PETR4"
    assert quote["bid"] == 1.24
    assert quote["ask"] == 1.26
    assert quote["vwap"] == 1.245
    assert quote["updated_at"] == "2026-07-09T21:01:00-03:00"
    assert quote["created_at"] == "2026-07-09T21:00:00-03:00"
    assert quote["source"] == "excel_rtd_live"
    assert "PETRS424" in quote["raw_json"]

    with sqlite3.connect(str(db_path)) as conn:
        count = conn.execute(
            """
            SELECT COUNT(*)
            FROM rtd_option_quotes
            WHERE UPPER(TRIM(codigo_opcao)) = 'PETRS424'
            """
        ).fetchone()[0]

    assert count == 1


def test_sync_from_excel_uses_reader_result_without_real_excel(tmp_path: Path):
    db_path = tmp_path / "app.db"

    def fake_reader(**kwargs):
        return {
            "ok": True,
            "workbook_name": "LISTA_RTD.xlsm",
            "workbook_path": "C:/users/eucal/projeto/LISTA_RTD.xlsm",
            "sheet_name": "RTD_OPTION_QUOTES",
            "read_at": "2026-07-09T21:05:00-03:00",
            "record_count": 1,
            "records": [
                {
                    "codigo_opcao": "BOVAE195",
                    "ativo_base": "BOVA11",
                    "call_put": "CALL",
                    "strike": 195,
                    "vencimento": "21-08-2026",
                    "ultimo_preco": 1.23,
                    "bid": 1.22,
                    "ask": 1.24,
                    "vwap": 1.23,
                }
            ],
        }

    result = sync_rtd_option_quotes_from_excel(
        db_path=db_path,
        reader_fn=fake_reader,
    )

    assert result.ok
    assert result.rows_read == 1
    assert result.rows_upserted == 1
    assert result.workbook_name == "LISTA_RTD.xlsm"
    assert result.sheet_name == "RTD_OPTION_QUOTES"
    assert result.read_at == "2026-07-09T21:05:00-03:00"

    quote = RtdOptionQuotesRepository(db_path).get_by_codigo("BOVAE195")

    assert quote is not None
    assert quote["codigo_opcao"] == "BOVAE195"
    assert quote["ativo_base"] == "BOVA11"
    assert quote["bid"] == 1.22
    assert quote["ask"] == 1.24


def test_sync_from_excel_returns_controlled_error_when_reader_fails(tmp_path: Path):
    db_path = tmp_path / "app.db"

    def fake_reader(**kwargs):
        return {
            "ok": False,
            "workbook_name": "LISTA_RTD.xlsm",
            "workbook_path": "",
            "sheet_name": "RTD_OPTION_QUOTES",
            "read_at": "2026-07-09T21:05:00-03:00",
            "record_count": 0,
            "records": [],
            "error": "Excel fechado",
        }

    result = sync_rtd_option_quotes_from_excel(
        db_path=db_path,
        reader_fn=fake_reader,
    )

    assert not result.ok
    assert result.rows_read == 0
    assert result.rows_upserted == 0
    assert result.error == "Excel fechado"
