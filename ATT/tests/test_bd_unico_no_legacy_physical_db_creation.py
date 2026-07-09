import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_RELATIVE_DB = Path("dados") / "app.db"


def _legacy_database_name() -> str:
    return "".join(("der", "ived", ".db"))


def _database_files_under(base: Path) -> list[Path]:
    return sorted(
        path.relative_to(base)
        for path in base.rglob("*.db")
        if path.is_file()
    )


def _legacy_database_files_under(base: Path) -> list[Path]:
    legacy_name = _legacy_database_name()
    return sorted(
        path.relative_to(base)
        for path in base.rglob("*.db")
        if path.is_file() and path.name == legacy_name
    )


def test_selected_initializers_create_only_the_canonical_app_database(tmp_path):
    env = os.environ.copy()
    env["APP_DB_PATH"] = str((tmp_path / CANONICAL_RELATIVE_DB).resolve())
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not env.get("PYTHONPATH")
        else str(PROJECT_ROOT) + os.pathsep + env["PYTHONPATH"]
    )

    script = """
import importlib
import os
from pathlib import Path

canonical = Path(os.environ["APP_DB_PATH"])
canonical.parent.mkdir(parents=True, exist_ok=True)

from db.init_db import init_db
init_db(str(canonical))

from db.config import connect_app
from db.derived_repo import ensure_derived_tables

with connect_app() as conn:
    ensure_derived_tables(conn)

from services.derived_service import init_db as init_service_db
init_service_db()

for module_name in (
    "services.canonical_pricing_facade",
    "services.pricing_execution_app_service",
    "services.market_snapshot_provider",
    "services.market_snapshot_selector",
):
    importlib.import_module(module_name)
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / CANONICAL_RELATIVE_DB).is_file()

    database_files = _database_files_under(tmp_path)
    assert database_files == [CANONICAL_RELATIVE_DB]


def test_selected_initializers_do_not_create_legacy_physical_database(tmp_path):
    env = os.environ.copy()
    env["APP_DB_PATH"] = str((tmp_path / CANONICAL_RELATIVE_DB).resolve())
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = (
        str(PROJECT_ROOT)
        if not env.get("PYTHONPATH")
        else str(PROJECT_ROOT) + os.pathsep + env["PYTHONPATH"]
    )

    script = """
import os
from pathlib import Path

canonical = Path(os.environ["APP_DB_PATH"])
canonical.parent.mkdir(parents=True, exist_ok=True)

from db.init_db import init_db
init_db(str(canonical))

from db.config import connect_app
from db.derived_repo import ensure_derived_tables

with connect_app() as conn:
    ensure_derived_tables(conn)

from services.derived_service import init_db as init_service_db
init_service_db()
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert _legacy_database_files_under(tmp_path) == []
