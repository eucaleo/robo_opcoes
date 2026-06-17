"""
Configuracao centralizada dos caminhos de banco SQLite do projeto.

Este modulo e o ponto unico para resolver os caminhos padrao de:

- dados/app.db
- dados/derived.db

Mantem compatibilidade com constantes e funcoes legadas ja usadas no codigo:
APP_DB_PATH, DERIVED_DB_PATH, connect_app() e connect_derived().

Variaveis de ambiente suportadas:

- APP_DB_PATH
- DERIVED_DB_PATH
- DERIVED_DB
- DERIVED_DB_FILE
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Optional, Union


PathLike = Union[str, Path]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DADOS_DIR = PROJECT_ROOT / "dados"


def _resolve_path(value: Optional[PathLike], default: Path) -> Path:
    """
    Resolve um caminho SQLite.

    - Se value for None ou vazio, usa default.
    - Se value for relativo, resolve a partir do diretorio atual do processo,
      preservando compatibilidade com chamadas legadas.
    - Expande "~" quando presente.
    """
    if value is None:
        return default.resolve()

    raw = str(value).strip()
    if not raw:
        return default.resolve()

    return Path(raw).expanduser().resolve()


def get_app_db_path() -> Path:
    """Retorna o caminho efetivo do app.db."""
    return _resolve_path(os.getenv("APP_DB_PATH"), DADOS_DIR / "app.db")


def get_derived_db_path() -> Path:
    """Retorna o caminho efetivo do derived.db."""
    env_value = (
        os.getenv("DERIVED_DB_PATH")
        or os.getenv("DERIVED_DB")
        or os.getenv("DERIVED_DB_FILE")
    )
    return _resolve_path(env_value, DADOS_DIR / "derived.db")


# Constantes legadas preservadas para compatibilidade.
APP_DB_PATH = get_app_db_path()
DERIVED_DB_PATH = get_derived_db_path()


def ensure_parent_dir(path: PathLike) -> Path:
    """Garante que a pasta pai do banco exista e retorna o Path resolvido."""
    resolved = Path(path).expanduser().resolve()
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def connect_app(db_path: Optional[PathLike] = None) -> sqlite3.Connection:
    """
    Abre conexao com app.db.

    Se db_path for informado, ele tem prioridade sobre APP_DB_PATH.
    """
    resolved = _resolve_path(db_path, get_app_db_path()) if db_path else get_app_db_path()
    ensure_parent_dir(resolved)
    return sqlite3.connect(str(resolved))


def connect_derived(db_path: Optional[PathLike] = None) -> sqlite3.Connection:
    """
    Abre conexao com derived.db.

    Se db_path for informado, ele tem prioridade sobre DERIVED_DB_PATH.
    """
    resolved = (
        _resolve_path(db_path, get_derived_db_path())
        if db_path
        else get_derived_db_path()
    )
    ensure_parent_dir(resolved)
    return sqlite3.connect(str(resolved))


# Aliases explicitos para novos consumidores.
connect_app_db = connect_app
connect_derived_db = connect_derived
