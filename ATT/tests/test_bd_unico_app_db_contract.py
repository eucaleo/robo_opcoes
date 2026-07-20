from pathlib import Path
import importlib


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DB_PATH = PROJECT_ROOT / "dados" / "app.db"
CANONICAL_DB_RESOLVED = CANONICAL_DB_PATH.resolve(strict=False)

CONFIG_DB_PATH_NAMES = [
    "DB_PATH",
    "APP_DB_PATH",
    "DATABASE_PATH",
    "SQLITE_PATH",
    "APP_DATABASE_PATH",
]


def _as_project_path(value):
    path = Path(value).expanduser()

    if not path.is_absolute():
        path = PROJECT_ROOT / path

    return path.resolve(strict=False)


def test_canonical_app_db_file_exists():
    assert CANONICAL_DB_PATH.exists()
    assert CANONICAL_DB_PATH.is_file()


def test_db_config_points_to_canonical_app_db():
    config = importlib.import_module("db.config")

    discovered_paths = []

    for name in CONFIG_DB_PATH_NAMES:
        if not hasattr(config, name):
            continue

        value = getattr(config, name)

        if value is None:
            continue

        if isinstance(value, (str, Path)):
            discovered_paths.append((name, _as_project_path(value)))

    assert discovered_paths != []

    for name, resolved_path in discovered_paths:
        assert resolved_path == CANONICAL_DB_RESOLVED, (
            f"{name} deve apontar para {CANONICAL_DB_PATH}, "
            f"mas aponta para {resolved_path}"
        )


def test_dados_directory_has_only_canonical_app_db_file():
    dados_dir = PROJECT_ROOT / "dados"

    assert dados_dir.exists()
    assert dados_dir.is_dir()

    db_files = sorted(path for path in dados_dir.glob("*.db") if path.is_file())

    unexpected_db_files = [
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in db_files
        if path.resolve(strict=False) != CANONICAL_DB_RESOLVED
    ]

    assert unexpected_db_files == []
