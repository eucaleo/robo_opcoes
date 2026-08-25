from __future__ import annotations

"""
Configuracao central do banco local da aplicacao.

Este modulo somente define caminho e configuracao. A abertura efetiva da
conexao pertence a infra.sqlite_conn, importada tardiamente para evitar ciclo.
"""

import os
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DADOS_DIR = PROJECT_ROOT / "dados"
DEFAULT_APP_DB_PATH = DADOS_DIR / "app.db"
DEFAULT_TIMEOUT = 30.0


def resolve_app_db_path(db_path: str | Path | None = None) -> Path:
    raw_path = db_path if db_path is not None else os.environ.get("APP_DB_PATH")
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    return DEFAULT_APP_DB_PATH.resolve()


def get_app_db_path(db_path: str | Path | None = None) -> Path:
    return resolve_app_db_path(db_path)


APP_DB_PATH = resolve_app_db_path()


def connect_app(
    db_path: str | Path | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    enable_wal: bool = True,
    **kwargs: Any,
):
    # Import tardio: infra.sqlite_conn importa APP_DB_PATH deste modulo.
    from infra.sqlite_conn import connect_app_db

    conn = connect_app_db(db_path, timeout=timeout, **kwargs)

    if enable_wal:
        try:
            conn.execute("PRAGMA journal_mode = WAL")
        except Exception:
            pass

    return conn


def connect(
    db_path: str | Path | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    enable_wal: bool = True,
    **kwargs: Any,
):
    return connect_app(
        db_path,
        timeout=timeout,
        enable_wal=enable_wal,
        **kwargs,
    )


def get_connection(
    db_path: str | Path | None = None,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    enable_wal: bool = True,
    **kwargs: Any,
):
    return connect(
        db_path,
        timeout=timeout,
        enable_wal=enable_wal,
        **kwargs,
    )


__all__ = [
    "APP_DB_PATH",
    "DEFAULT_APP_DB_PATH",
    "DEFAULT_TIMEOUT",
    "resolve_app_db_path",
    "get_app_db_path",
    "connect_app",
    "connect",
    "get_connection",
]
