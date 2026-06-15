from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "audit_rtd_option_quotes.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "audit_rtd_option_quotes_under_test",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def create_schema(db_path: Path, unique: bool = True) -> None:
    unique_sql = ", UNIQUE(codigo_opcao)" if unique else ""

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            f"""
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
                iv REAL,
                delta REAL,
                gamma REAL,
                theta REAL,
                vega REAL,
                source TEXT NOT NULL DEFAULT 'rtd_links',
                raw_json TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                {unique_sql}
            )
            """
        )


def insert_quote(
    db_path: Path,
    codigo_opcao: str,
    updated_at: str = "CURRENT_TIMESTAMP",
) -> None:
    if updated_at == "CURRENT_TIMESTAMP":
        updated_at_sql = "CURRENT_TIMESTAMP"
        params = (codigo_opcao,)
    else:
        updated_at_sql = "?"
        params = (codigo_opcao, updated_at)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            f"""
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                bid,
                ask,
                source,
                updated_at,
                created_at
            )
            VALUES (?, 'PETR4', 'CALL', 30.0, 1.0, 1.1, 'rtd_links', {updated_at_sql}, CURRENT_TIMESTAMP)
            """,
            params,
        )


def test_audit_reports_error_when_database_does_not_exist(tmp_path: Path):
    module = load_module()

    result = module.audit_database(tmp_path / "missing.db")

    assert result["status"] == "error"
    assert "database file not found" in result["errors"]


def test_audit_reports_error_when_table_does_not_exist(tmp_path: Path):
    module = load_module()
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path):
        pass

    result = module.audit_database(db_path)

    assert result["status"] == "error"
    assert "table not found: rtd_option_quotes" in result["errors"]


def test_audit_reports_ok_for_valid_table_with_rows(tmp_path: Path):
    module = load_module()
    db_path = tmp_path / "app.db"

    create_schema(db_path)
    insert_quote(db_path, "PETRA300")
    insert_quote(db_path, "PETRA310")

    result = module.audit_database(db_path, max_age_minutes=0)

    assert result["status"] == "ok"
    assert result["metrics"]["row_count"] == 2
    assert result["metrics"]["distinct_codigo_count"] == 2
    assert result["metrics"]["duplicate_codigo_count"] == 0
    assert result["errors"] == []


def test_audit_reports_warning_for_empty_table(tmp_path: Path):
    module = load_module()
    db_path = tmp_path / "app.db"

    create_schema(db_path)

    result = module.audit_database(db_path, max_age_minutes=0)

    assert result["status"] == "warn"
    assert result["metrics"]["row_count"] == 0
    assert "table is empty" in result["warnings"]


def test_audit_reports_error_for_missing_required_columns(tmp_path: Path):
    module = load_module()
    db_path = tmp_path / "app.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                codigo_opcao TEXT NOT NULL
            )
            """
        )

    result = module.audit_database(db_path, max_age_minutes=0)

    assert result["status"] == "error"
    assert "ativo_base" in result["missing_columns"]
    assert result["errors"]


def test_audit_reports_error_for_duplicated_codigo_opcao(tmp_path: Path):
    module = load_module()
    db_path = tmp_path / "app.db"

    create_schema(db_path, unique=False)
    insert_quote(db_path, "PETRA300")
    insert_quote(db_path, "PETRA300")

    result = module.audit_database(db_path, max_age_minutes=0)

    assert result["status"] == "error"
    assert result["metrics"]["duplicate_codigo_count"] == 1
    assert "duplicated codigo_opcao groups: 1" in result["errors"]


def test_audit_reports_warning_for_stale_rows(tmp_path: Path):
    module = load_module()
    db_path = tmp_path / "app.db"

    create_schema(db_path)
    insert_quote(db_path, "PETRA300", updated_at="2000-01-01 00:00:00")

    result = module.audit_database(db_path, max_age_minutes=30)

    assert result["status"] == "warn"
    assert result["metrics"]["stale_rows"] == 1
    assert "rows older than 30 minutes: 1" in result["warnings"]
