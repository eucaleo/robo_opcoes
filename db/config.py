# db/config.py
import os
from pathlib import Path
import sqlite3

APP_DB_PATH = Path(os.getenv("APP_DB_PATH", "data/app.db")).resolve()
DERIVED_DB_PATH = Path(os.getenv("DERIVED_DB_PATH", "data/derived.db")).resolve()

def connect_app() -> sqlite3.Connection:
    return sqlite3.connect(str(APP_DB_PATH))

def connect_derived() -> sqlite3.Connection:
    return sqlite3.connect(str(DERIVED_DB_PATH))
