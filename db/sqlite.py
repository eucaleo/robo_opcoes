import sqlite3
from pathlib import Path

from db.config import ensure_parent_dir, get_app_db_path


DEFAULT_DB_PATH = get_app_db_path()


def connect(db_path: str | Path | None = None):
    resolved_path = (
        Path(db_path).expanduser().resolve()
        if db_path is not None
        else get_app_db_path()
    )
    ensure_parent_dir(resolved_path)
    conn = sqlite3.connect(str(resolved_path))
    conn.row_factory = sqlite3.Row
    return conn
