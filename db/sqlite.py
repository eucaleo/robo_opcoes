from __future__ import annotations

"""
Fachada publica de compatibilidade do conector SQLite.

A abertura de conexoes, configuracao de row factory e a ativacao de chaves
estrangeiras pertencem exclusivamente a infra.sqlite_conn.
"""

from pathlib import Path
from typing import Any

from infra import sqlite_conn as _official_sqlite_conn

APP_DB_PATH = _official_sqlite_conn.APP_DB_PATH
DEFAULT_DB_PATH = _official_sqlite_conn.DEFAULT_DB_PATH
DEFAULT_TIMEOUT_SECONDS = _official_sqlite_conn.DEFAULT_TIMEOUT_SECONDS


def official_connector_module():
    return _official_sqlite_conn.official_connector_module()


def resolve_app_db_path(db_path: str | Path | None = None) -> Path:
    return _official_sqlite_conn.resolve_app_db_path(db_path)


def connect_app_db(
    db_path: str | Path | None = None,
    *args: Any,
    **kwargs: Any,
):
    return _official_sqlite_conn.connect_app_db(db_path, *args, **kwargs)


def app_db_connection(
    db_path: str | Path | None = None,
    *args: Any,
    **kwargs: Any,
):
    return _official_sqlite_conn.app_db_connection(db_path, *args, **kwargs)


connect = connect_app_db
get_connection = connect
get_conn = connect
open_connection = connect
connect_db = connect
sqlite_conn = connect_app_db
sqlite_connect = connect_app_db
connect_sqlite = connect_app_db
get_sqlite_connection = connect


__all__ = [
    "APP_DB_PATH",
    "DEFAULT_DB_PATH",
    "DEFAULT_TIMEOUT_SECONDS",
    "official_connector_module",
    "resolve_app_db_path",
    "connect_app_db",
    "app_db_connection",
    "connect",
    "get_connection",
    "get_conn",
    "open_connection",
    "connect_db",
    "sqlite_conn",
    "sqlite_connect",
    "connect_sqlite",
    "get_sqlite_connection",
]
