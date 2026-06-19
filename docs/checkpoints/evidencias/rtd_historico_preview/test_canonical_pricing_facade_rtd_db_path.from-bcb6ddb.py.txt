import sqlite3
from pathlib import Path

from services.canonical_pricing_facade import (
    CanonicalPricingFacade,
    _resolve_rtd_option_quotes_db_path,
    _sqlite_table_exists,
)


def _create_sqlite_db(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(path)):
        pass


def _create_rtd_option_quotes_table(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS rtd_option_quotes (
                codigo_opcao TEXT PRIMARY KEY,
                ativo_base TEXT,
                ultimo_preco REAL
            )
            """
        )
        conn.commit()


def test_sqlite_table_exists_returns_false_for_missing_database(tmp_path):
    db_path = tmp_path / "missing.db"

    assert _sqlite_table_exists(db_path, "rtd_option_quotes") is False


def test_sqlite_table_exists_detects_existing_table(tmp_path):
    db_path = tmp_path / "app.db"
    _create_rtd_option_quotes_table(db_path)

    assert _sqlite_table_exists(db_path, "rtd_option_quotes") is True
    assert _sqlite_table_exists(db_path, "tabela_inexistente") is False


def test_resolve_rtd_option_quotes_db_path_prefers_app_db_when_primary_has_no_table(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    dados_dir = tmp_path / "dados"
    primary_db = dados_dir / "derived.db"
    app_db = dados_dir / "app.db"

    _create_sqlite_db(primary_db)
    _create_rtd_option_quotes_table(app_db)

    resolved = _resolve_rtd_option_quotes_db_path(primary_db)

    assert resolved == app_db


def test_resolve_rtd_option_quotes_db_path_prefers_primary_when_primary_has_table(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    dados_dir = tmp_path / "dados"
    primary_db = dados_dir / "derived.db"
    app_db = dados_dir / "app.db"

    _create_rtd_option_quotes_table(primary_db)
    _create_rtd_option_quotes_table(app_db)

    resolved = _resolve_rtd_option_quotes_db_path(primary_db)

    assert resolved == primary_db


def test_resolve_rtd_option_quotes_db_path_falls_back_to_primary_when_no_candidate_has_table(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    dados_dir = tmp_path / "dados"
    primary_db = dados_dir / "derived.db"
    app_db = dados_dir / "app.db"

    _create_sqlite_db(primary_db)
    _create_sqlite_db(app_db)

    resolved = _resolve_rtd_option_quotes_db_path(primary_db)

    assert resolved == primary_db


def test_canonical_pricing_facade_initializes_rtd_repository_with_resolved_app_db(
    tmp_path,
    monkeypatch,
):
    monkeypatch.chdir(tmp_path)

    dados_dir = tmp_path / "dados"
    primary_db = dados_dir / "derived.db"
    app_db = dados_dir / "app.db"

    _create_sqlite_db(primary_db)
    _create_rtd_option_quotes_table(app_db)

    facade = CanonicalPricingFacade(db_path=primary_db)

    assert facade._db_path == primary_db
    assert facade._rtd_option_quotes_db_path == app_db
    assert facade._rtd_option_quotes_repository.db_path == app_db
