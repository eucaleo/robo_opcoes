#!/usr/bin/env python
"""
Valida o banco unico da aplicacao app.db.

Regras:
- usa APP_DB_PATH, se definido;
- caso contrario, usa dados/app.db a partir da raiz do projeto;
- nao depende de funcoes de conexao legadas.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_APP_DB_PATH = PROJECT_ROOT / "dados" / "app.db"


def find_app_db_path() -> Path:
    env = os.environ.get("APP_DB_PATH")
    if env:
        return Path(env).expanduser().resolve()
    return DEFAULT_APP_DB_PATH.resolve()


def validate_app_db(path: Path) -> int:
    print(f"[INFO] APP_DB_PATH: {path}")

    if not path.exists():
        print("[ERRO] Banco app.db nao encontrado.")
        print("       Defina APP_DB_PATH apontando para o arquivo correto.")
        return 2

    try:
        with sqlite3.connect(str(path)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = [row[0] for row in cur.fetchall()]
    except Exception as exc:
        print(f"[ERRO] Falha ao abrir/consultar banco: {exc}")
        return 3

    print(f"[OK] Banco acessivel: {path}")
    print(f"[INFO] Total de tabelas: {len(tables)}")

    if tables:
        print("[INFO] Tabelas:")
        for name in tables:
            print(f"  - {name}")

    return 0


def main() -> int:
    path = find_app_db_path()
    return validate_app_db(path)


if __name__ == "__main__":
    raise SystemExit(main())
