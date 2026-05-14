from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator, Optional


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Melhor compatibilidade com concorrência de leitura
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass
    try:
        conn.execute("PRAGMA foreign_keys=ON;")
    except Exception:
        pass
    return conn


@contextmanager
def sqlite_conn(db_path: str) -> Iterator[sqlite3.Connection]:
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = _connect(db_path)
        yield conn
    finally:
        if conn is not None:
            conn.close()
