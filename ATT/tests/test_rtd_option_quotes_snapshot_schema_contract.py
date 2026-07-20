from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema


def _index_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute("PRAGMA index_list(rtd_option_quotes)").fetchall()
    return {str(row[1]) for row in rows}


def test_rtd_option_quotes_schema_has_snapshot_indexes(tmp_path: Path):
    db_path = tmp_path / "app.db"

    ensure_rtd_option_quotes_schema(db_path)

    with sqlite3.connect(str(db_path)) as conn:
        indexes = _index_names(conn)

    assert "idx_rtd_option_quotes_codigo_opcao" in indexes
    assert "ux_rtd_option_quotes_codigo_opcao_normalized" in indexes
    assert "idx_rtd_option_quotes_ativo_base" in indexes


def test_rtd_option_quotes_rejects_duplicate_normalized_symbol(tmp_path: Path):
    db_path = tmp_path / "app.db"

    ensure_rtd_option_quotes_schema(db_path)

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (codigo_opcao)
            VALUES (?)
            """,
            ("PETRS424",),
        )
        conn.commit()

        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                """
                INSERT INTO rtd_option_quotes (codigo_opcao)
                VALUES (?)
                """,
                (" petrs424 ",),
            )


def test_rtd_option_quotes_schema_deduplicates_and_normalizes_existing_symbols(
    tmp_path: Path,
):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_opcao TEXT NOT NULL,
                ativo_base TEXT,
                call_put TEXT,
                strike REAL,
                vencimento TEXT,
                ultimo_preco REAL,
                ultima_quantidade REAL,
                bid REAL,
                ask REAL,
                volume REAL,
                vwap REAL,
                iv REAL,
                delta REAL,
                gamma REAL,
                theta REAL,
                vega REAL,
                source TEXT NOT NULL DEFAULT 'rtd_links',
                raw_json TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (codigo_opcao, bid)
            VALUES (?, ?)
            """,
            ("petrs424", 1.10),
        )
        conn.execute(
            """
            INSERT INTO rtd_option_quotes (codigo_opcao, bid)
            VALUES (?, ?)
            """,
            (" PETRS424 ", 1.20),
        )
        conn.commit()

    ensure_rtd_option_quotes_schema(db_path)

    with sqlite3.connect(str(db_path)) as conn:
        rows = conn.execute(
            """
            SELECT codigo_opcao, bid
            FROM rtd_option_quotes
            ORDER BY id
            """
        ).fetchall()

    assert rows == [("PETRS424", 1.20)]
