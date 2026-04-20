import os
import sqlite3
from pathlib import Path

DB_PATH = os.getenv("DERIVED_DB_PATH", "derived.db")

def get_connection():
    # Garante diretório existente quando usar caminhos com subpastas
    db_path = Path(DB_PATH)
    if db_path.parent and not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))
