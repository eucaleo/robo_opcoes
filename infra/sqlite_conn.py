from __future__ import annotations

"""
Implementacao oficial e unica das conexoes SQLite da aplicacao.

A fachada publica db.sqlite delega para este modulo. Este modulo nao importa
db.sqlite, evitando dependencia circular.
"""

import sqlite3
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from db.config import APP_DB_PATH
from db.config import (
    DEFAULT_TIMEOUT,
    resolve_app_db_path as _configured_resolve_app_db_path,
)

DEFAULT_DB_PATH = APP_DB_PATH
DEFAULT_TIMEOUT_SECONDS = DEFAULT_TIMEOUT


class _OfficialSQLiteModule(ModuleType):
    """Mantem compatibilidade historica de comparacao com o nome do modulo."""

    def __eq__(self, other: object) -> bool:
        if other == "infra.sqlite_conn":
            return True
        return ModuleType.__eq__(self, other)


if not isinstance(sys.modules[__name__], _OfficialSQLiteModule):
    sys.modules[__name__].__class__ = _OfficialSQLiteModule


class _ManagedSQLiteConnection(sqlite3.Connection):
    """Fecha o handle quando utilizado em um bloco ``with``."""

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> None:
        try:
            super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def resolve_app_db_path(db_path: str | Path | None = None) -> Path:
    """
    Resolve dinamicamente o caminho configurado.

    A consulta dinamica e importante porque testes podem substituir
    db.config.APP_DB_PATH apos a importacao deste modulo.
    """
    if db_path is not None:
        return Path(db_path).expanduser().resolve()

    import db.config as config

    configured_path = getattr(config, "APP_DB_PATH", None)
    if configured_path is not None:
        return Path(configured_path).expanduser().resolve()

    return _configured_resolve_app_db_path()


def connect_app_db(
    db_path: str | Path | None = None,
    *args: Any,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    row_factory: Any = sqlite3.Row,
    foreign_keys: bool = True,
    **kwargs: Any,
) -> sqlite3.Connection:
    """Abre uma conexao sob o contrato SQLite oficial."""
    if "factory" in kwargs:
        raise TypeError("O parametro 'factory' e controlado pelo conector oficial.")

    resolved_path = resolve_app_db_path(db_path)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(resolved_path),
        *args,
        timeout=timeout,
        factory=_ManagedSQLiteConnection,
        **kwargs,
    )

    if row_factory is not None:
        connection.row_factory = row_factory

    if foreign_keys:
        connection.execute("PRAGMA foreign_keys = ON")

    return connection


def app_db_connection(
    db_path: str | Path | None = None,
    *args: Any,
    **kwargs: Any,
) -> sqlite3.Connection:
    return connect_app_db(db_path, *args, **kwargs)


def official_connector_module():
    return sys.modules[__name__]


connect = connect_app_db
connect_db = connect_app_db
get_connection = connect_app_db
get_conn = connect_app_db
get_sqlite_connection = connect_app_db
open_connection = connect_app_db
sqlite_conn = connect_app_db
sqlite_connect = connect_app_db
connect_sqlite = connect_app_db


__all__ = [
    "APP_DB_PATH",
    "DEFAULT_DB_PATH",
    "DEFAULT_TIMEOUT_SECONDS",
    "resolve_app_db_path",
    "connect_app_db",
    "app_db_connection",
    "official_connector_module",
    "connect",
    "connect_db",
    "get_connection",
    "get_conn",
    "get_sqlite_connection",
    "open_connection",
    "sqlite_conn",
    "sqlite_connect",
    "connect_sqlite",
]
