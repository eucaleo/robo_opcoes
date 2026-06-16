# db/sqlite.py
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path("dados") / "app.db"

def connect(db_path: str | Path = DEFAULT_DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
