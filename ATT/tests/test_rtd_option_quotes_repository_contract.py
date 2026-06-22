import sqlite3
from pathlib import Path

import pytest

from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository


def _create_schema(db_path: Path) -> None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_opcao TEXT,
                ativo_base TEXT,
                call_put TEXT,
                strike REAL,
                vencimento TEXT,
                ultimo_preco REAL,
                ultima_quantidade REAL,
                bid REAL,
                ask REAL,
                volume REAL,
                iv REAL,
                delta REAL,
                gamma REAL,
                theta REAL,
                vega REAL,
                source TEXT,
                raw_json TEXT,
                updated_at TEXT,
                created_at TEXT
            )
            """
        )


def test_get_by_codigo_returns_quote_dict_when_codigo_exists(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "PETRA123",
                "PETR4",
                "CALL",
                30.0,
                "2026-07-17",
                1.23,
                100,
                1.20,
                1.26,
                1000,
                0.25,
                0.50,
                0.10,
                -0.01,
                0.20,
                "rtd_option_quotes",
                '{"origem": "teste"}',
                "2026-06-18 10:00:00",
                "2026-06-18 09:59:00",
            ),
        )

    repository = RtdOptionQuotesRepository(db_path=db_path)

    quote = repository.get_by_codigo("PETRA123")

    assert quote is not None
    assert quote["codigo_opcao"] == "PETRA123"
    assert quote["ativo_base"] == "PETR4"
    assert quote["ultimo_preco"] == 1.23
    assert quote["bid"] == 1.20
    assert quote["ask"] == 1.26
    assert quote["source"] == "rtd_option_quotes"
    assert quote["updated_at"] == "2026-06-18 10:00:00"


def test_get_by_codigo_returns_none_when_codigo_does_not_exist(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)

    repository = RtdOptionQuotesRepository(db_path=db_path)

    assert repository.get_by_codigo("INEXISTENTE") is None


def test_get_by_codigo_uses_exact_codigo_match(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                source,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "PETRA123",
                "PETR4",
                "CALL",
                30.0,
                "2026-07-17",
                1.23,
                "rtd_option_quotes",
                "2026-06-18 10:00:00",
                "2026-06-18 09:59:00",
            ),
        )

    repository = RtdOptionQuotesRepository(db_path=db_path)

    assert repository.get_by_codigo("petra123") is None
    assert repository.get_by_codigo("PETRA123") is not None


def test_get_by_codigo_propagates_sqlite_error_when_table_is_missing(tmp_path):
    db_path = tmp_path / "app.db"
    db_path.touch()

    repository = RtdOptionQuotesRepository(db_path=db_path)

    with pytest.raises(sqlite3.OperationalError):
        repository.get_by_codigo("PETRA123")


def test_list_by_ativo_base_returns_ordered_quotes_for_asset(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)

    rows = [
        ("PETRB123", "PETR4", "PUT", 32.0, "2026-08-17", 2.0),
        ("PETRA123", "PETR4", "CALL", 30.0, "2026-07-17", 1.0),
        ("VALEA123", "VALE3", "CALL", 60.0, "2026-07-17", 3.0),
    ]

    with sqlite3.connect(str(db_path)) as conn:
        conn.executemany(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                source,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
            """,
            rows,
        )

    repository = RtdOptionQuotesRepository(db_path=db_path)

    quotes = repository.list_by_ativo_base("PETR4")

    assert [quote["codigo_opcao"] for quote in quotes] == ["PETRA123", "PETRB123"]
    assert all(quote["ativo_base"] == "PETR4" for quote in quotes)


def test_list_all_returns_quotes_as_dicts(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)

    rows = [
        ("VALEA123", "VALE3", "CALL", 60.0, "2026-07-17", 3.0),
        ("PETRA123", "PETR4", "CALL", 30.0, "2026-07-17", 1.0),
    ]

    with sqlite3.connect(str(db_path)) as conn:
        conn.executemany(
            """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                source,
                updated_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 'rtd_option_quotes', '2026-06-18 10:00:00', '2026-06-18 09:59:00')
            """,
            rows,
        )

    repository = RtdOptionQuotesRepository(db_path=db_path)

    quotes = repository.list_all()

    assert [quote["codigo_opcao"] for quote in quotes] == ["PETRA123", "VALEA123"]
    assert all(isinstance(quote, dict) for quote in quotes)
