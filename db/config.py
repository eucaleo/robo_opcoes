# db/config.py
import os
from pathlib import Path
import sqlite3

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_DB_PATH     = Path(os.getenv("APP_DB_PATH",     str(_PROJECT_ROOT / "dados/app.db"))).resolve()
DERIVED_DB_PATH = Path(os.getenv("DERIVED_DB_PATH", str(_PROJECT_ROOT / "dados/app.db"))).resolve()

def connect_app() -> sqlite3.Connection:
    APP_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(APP_DB_PATH))

def connect_derived() -> sqlite3.Connection:
    APP_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(APP_DB_PATH))
