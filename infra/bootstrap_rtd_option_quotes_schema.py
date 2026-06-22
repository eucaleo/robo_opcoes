from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


TABLE_NAME = "rtd_option_quotes"

REQUIRED_COLUMNS = {
    "id",
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "source",
    "raw_json",
    "updated_at",
    "created_at",
}


DDL = """
CREATE TABLE IF NOT EXISTS rtd_option_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo_opcao TEXT NOT NULL,
    ativo_base TEXT,

    call_put TEXT,
    strike REAL,
    vencimento TEXT,

    ultimo_preco REAL,
    ultima_quantidade REAL,

    bid REAL,
    ask REAL,
    volume REAL,

    iv REAL,
    delta REAL,
    gamma REAL,
    theta REAL,
    vega REAL,

    source TEXT NOT NULL DEFAULT 'rtd_links',
    raw_json TEXT,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(codigo_opcao)
)
"""


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        LIMIT 1
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def get_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    return {row[1] for row in rows}



def ensure_rtd_option_quotes_schema(db_path: Path | str) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(DDL)
        conn.commit()

        columns = get_columns(conn, TABLE_NAME)
        missing = sorted(REQUIRED_COLUMNS - columns)

        if missing:
            raise RuntimeError(
                "Tabela rtd_option_quotes existe, mas está sem colunas obrigatórias: "
                + ", ".join(missing)
            )

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cria/valida o schema vazio de rtd_option_quotes em banco SQLite."
    )
    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite. Padrão: dados/app.db",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    print("Bootstrap rtd_option_quotes")
    print(f"DB: {db_path.resolve()}")

    with sqlite3.connect(str(db_path)) as conn:
        existed_before = table_exists(conn, TABLE_NAME)

        if existed_before:
            print("[INFO] Tabela já existia. Validando schema...")
        else:
            print("[INFO] Tabela ausente. Criando schema vazio...")

        conn.execute(DDL)
        conn.commit()

        columns = get_columns(conn, TABLE_NAME)
        missing = sorted(REQUIRED_COLUMNS - columns)

        if missing:
            print("[ERRO] Tabela existe, mas está sem colunas obrigatórias:")
            for col in missing:
                print(f"  - {col}")
            return 2

        count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]

    print("[OK] Schema rtd_option_quotes disponível.")
    print(f"[INFO] Linhas atuais: {count}")

    if count == 0:
        print("[INFO] Nenhum dado fictício foi inserido.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
