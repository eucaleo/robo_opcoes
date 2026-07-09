from pathlib import Path
import importlib
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DB_PATH = PROJECT_ROOT / "dados" / "app.db"
CANONICAL_DB_RESOLVED = CANONICAL_DB_PATH.resolve(strict=False)

EXPECTED_RTD_TABLES = {
    "rtd_option_quotes",
}


def _connect_readonly(path: Path) -> sqlite3.Connection:
    uri = path.resolve(strict=True).as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        """
        SELECT lower(name)
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()
    return {row[0] for row in rows}


def test_expected_rtd_tables_exist_in_canonical_app_db():
    assert CANONICAL_DB_PATH.exists()
    assert CANONICAL_DB_PATH.is_file()

    with _connect_readonly(CANONICAL_DB_PATH) as conn:
        tables = _table_names(conn)

    missing_tables = sorted(EXPECTED_RTD_TABLES - tables)

    assert missing_tables == []


def test_connect_app_uses_canonical_app_db_for_rtd_tables():
    config = importlib.import_module("db.config")

    with config.connect_app() as conn:
        database_rows = conn.execute("PRAGMA database_list").fetchall()
        main_rows = [row for row in database_rows if row[1] == "main"]

        assert len(main_rows) == 1

        main_db_path = Path(main_rows[0][2]).resolve(strict=False)

        assert main_db_path == CANONICAL_DB_RESOLVED

        tables = _table_names(conn)

    missing_tables = sorted(EXPECTED_RTD_TABLES - tables)

    assert missing_tables == []
