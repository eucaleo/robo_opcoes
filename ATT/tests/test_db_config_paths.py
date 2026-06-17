from pathlib import Path

from db import config


def test_default_db_paths_point_to_project_dados():
    assert config.get_app_db_path() == (config.PROJECT_ROOT / "dados" / "app.db").resolve()
    assert config.get_derived_db_path() == (
        config.PROJECT_ROOT / "dados" / "derived.db"
    ).resolve()


def test_env_override_app_db_path(monkeypatch, tmp_path):
    custom = tmp_path / "custom" / "app_test.db"

    monkeypatch.setenv("APP_DB_PATH", str(custom))

    assert config.get_app_db_path() == custom.resolve()


def test_env_override_derived_db_path(monkeypatch, tmp_path):
    custom = tmp_path / "custom" / "derived_test.db"

    monkeypatch.setenv("DERIVED_DB_PATH", str(custom))

    assert config.get_derived_db_path() == custom.resolve()


def test_connect_app_creates_parent_dir(tmp_path):
    db_path = tmp_path / "nested" / "app.db"

    with config.connect_app(db_path) as conn:
        conn.execute("SELECT 1")

    assert db_path.exists()


def test_connect_derived_creates_parent_dir(tmp_path):
    db_path = tmp_path / "nested" / "derived.db"

    with config.connect_derived(db_path) as conn:
        conn.execute("SELECT 1")

    assert db_path.exists()

def test_db_sqlite_connect_uses_runtime_app_db_env(monkeypatch, tmp_path):
    from db import sqlite as db_sqlite

    custom = tmp_path / "runtime" / "app_runtime.db"
    monkeypatch.setenv("APP_DB_PATH", str(custom))

    with db_sqlite.connect() as conn:
        conn.execute("SELECT 1")

    assert custom.exists()
