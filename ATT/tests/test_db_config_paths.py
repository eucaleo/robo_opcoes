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

def test_db_sqlite_connect_preserves_row_factory(tmp_path):
    from db import sqlite as db_sqlite

    db_path = tmp_path / "row_factory.db"

    with db_sqlite.connect(db_path) as conn:
        conn.execute("CREATE TABLE sample (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO sample (name) VALUES ('ok')")
        row = conn.execute("SELECT name FROM sample").fetchone()

    assert row["name"] == "ok"


def test_structures_repository_uses_runtime_app_db_env(monkeypatch, tmp_path):
    from repositories.structures_repository import StructuresRepository

    custom = tmp_path / "runtime" / "structures_app.db"
    monkeypatch.setenv("APP_DB_PATH", str(custom))

    repo = StructuresRepository()

    assert Path(repo.db_path) == custom.resolve()


def test_structure_events_repository_uses_runtime_app_db_env(monkeypatch, tmp_path):
    from repositories.structure_events_repository import StructureEventsRepository

    custom = tmp_path / "runtime" / "events_app.db"
    monkeypatch.setenv("APP_DB_PATH", str(custom))

    repo = StructureEventsRepository()

    assert Path(repo.db_path) == custom.resolve()

def test_derived_repo_uses_runtime_derived_db_env(monkeypatch, tmp_path):
    from db.derived_repo import DerivedRepo

    custom = tmp_path / "runtime" / "derived_repo.db"
    monkeypatch.setenv("DERIVED_DB_PATH", str(custom))

    repo = DerivedRepo()

    assert Path(repo._db_path) == custom.resolve()
    assert custom.exists()


def test_payoff_reader_uses_runtime_derived_db_env(monkeypatch, tmp_path):
    from db.reader import PayoffReader

    custom = tmp_path / "runtime" / "reader_derived.db"
    monkeypatch.setenv("DERIVED_DB_PATH", str(custom))

    reader = PayoffReader()

    assert reader.db_path == custom.resolve()


def test_payoff_writer_uses_runtime_derived_db_env(monkeypatch, tmp_path):
    from db.writer import PayoffWriter

    custom = tmp_path / "runtime" / "writer_derived.db"
    monkeypatch.setenv("DERIVED_DB_PATH", str(custom))

    writer = PayoffWriter()

    assert writer.db_path == custom.resolve()
    assert custom.exists()


def test_robo_legs_repo_config_uses_runtime_app_db_env(monkeypatch, tmp_path):
    from repositories.robo_legs_repository import RoboLegsRepoConfig

    custom = tmp_path / "runtime" / "robo_legs_app.db"
    monkeypatch.setenv("APP_DB_PATH", str(custom))

    config = RoboLegsRepoConfig()

    assert Path(config.app_db_path) == custom.resolve()


def test_robo_legs_status_repo_config_uses_runtime_app_db_env(monkeypatch, tmp_path):
    from repositories.robo_legs_status_repository import RoboLegsStatusRepoConfig

    custom = tmp_path / "runtime" / "robo_legs_status_app.db"
    monkeypatch.setenv("APP_DB_PATH", str(custom))

    config = RoboLegsStatusRepoConfig()

    assert Path(config.app_db_path) == custom.resolve()
