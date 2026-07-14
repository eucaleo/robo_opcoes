from pathlib import Path
import re
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DB_PATH = PROJECT_ROOT / "dados" / "app.db"

FORBIDDEN_TABLE_NAME_PATTERNS = [
    re.compile(r".*backup.*", re.IGNORECASE),
    re.compile(r".*bak.*", re.IGNORECASE),
    re.compile(r".*temp.*", re.IGNORECASE),
    re.compile(r".*tmp.*", re.IGNORECASE),
    re.compile(r".*scope.*", re.IGNORECASE),
    re.compile(r".*old.*", re.IGNORECASE),
]


def _connect_readonly(path: Path) -> sqlite3.Connection:
    uri = path.resolve(strict=True).as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def _schema_object_names(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type IN ('table', 'view', 'index', 'trigger')
        ORDER BY name
        """
    ).fetchall()

    return [row[0] for row in rows]


def test_app_db_has_no_residual_backup_temp_scope_objects():
    assert CANONICAL_DB_PATH.exists()
    assert CANONICAL_DB_PATH.is_file()

    with _connect_readonly(CANONICAL_DB_PATH) as conn:
        object_names = _schema_object_names(conn)

    violations = []

    for name in object_names:
        if name == "sqlite_sequence":
            continue

        for pattern in FORBIDDEN_TABLE_NAME_PATTERNS:
            if pattern.fullmatch(name):
                violations.append(name)
                break

    assert violations == []
