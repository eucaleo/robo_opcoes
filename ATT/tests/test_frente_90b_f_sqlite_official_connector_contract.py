import sqlite3
from pathlib import Path


def test_frente_90b_f_db_config_exposes_app_db_path():
    import db.config as config

    assert hasattr(config, "APP_DB_PATH")
    assert str(config.APP_DB_PATH).strip()
    assert "app.db" in str(config.APP_DB_PATH).replace("\\", "/")


def test_frente_90b_f_db_sqlite_exports_official_connector_contract():
    import db.sqlite as db_sqlite

    required = {
        "connect",
        "get_connection",
        "open_connection",
        "connect_app_db",
        "connect_db",
        "app_db_connection",
        "resolve_app_db_path",
    }

    for name in required:
        assert hasattr(db_sqlite, name), name

    assert db_sqlite.get_connection is db_sqlite.connect
    assert db_sqlite.open_connection is db_sqlite.connect
    assert db_sqlite.connect_app_db is db_sqlite.connect
    assert db_sqlite.connect_db is db_sqlite.connect


def test_frente_90b_f_official_connector_runtime_contract(tmp_path):
    import db.config as config
    import db.sqlite as db_sqlite

    old_app_db_path = getattr(config, "APP_DB_PATH")
    config.APP_DB_PATH = str(tmp_path / "app.db")

    connection = None
    try:
        connection = db_sqlite.connect()
        assert connection.row_factory is sqlite3.Row
        assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1

        connection.execute("CREATE TABLE sample_90b_f (id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
        connection.execute("INSERT INTO sample_90b_f (value) VALUES (?)", ("ok",))
        row = connection.execute("SELECT value FROM sample_90b_f WHERE id = 1").fetchone()

        assert row["value"] == "ok"
    finally:
        if connection is not None:
            connection.close()
        config.APP_DB_PATH = old_app_db_path


def test_frente_90b_f_infra_sqlite_conn_delegates_to_official_connector():
    infra_text = Path("infra/sqlite_conn.py").read_text(encoding="utf-8")
    db_sqlite_text = Path("db/sqlite.py").read_text(encoding="utf-8")

    assert "from db.sqlite import" not in infra_text
    assert "sqlite3.connect" in infra_text
    assert "sqlite3.connect" not in db_sqlite_text
    assert "PRAGMA foreign_keys = ON" in infra_text
    assert "row_factory" in infra_text
    assert "APP_DB_PATH" in Path("db/config.py").read_text(encoding="utf-8")
