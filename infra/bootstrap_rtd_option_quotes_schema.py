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
    "vwap",
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


ADDITIVE_COLUMNS = {
    "vwap": "REAL",
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
    vwap REAL,

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


def apply_additive_migrations(conn: sqlite3.Connection) -> None:
    columns = get_columns(conn, TABLE_NAME)

    for column_name, column_type in ADDITIVE_COLUMNS.items():
        if column_name not in columns:
            conn.execute(
                f'ALTER TABLE {TABLE_NAME} ADD COLUMN "{column_name}" {column_type}'
            )

    conn.commit()


def validate_required_columns(conn: sqlite3.Connection) -> None:
    columns = get_columns(conn, TABLE_NAME)
    missing = sorted(REQUIRED_COLUMNS - columns)

    if missing:
        raise RuntimeError(
            "Tabela rtd_option_quotes existe, mas está sem colunas obrigatórias: "
            + ", ".join(missing)
        )


def ensure_rtd_option_quotes_schema(db_path: Path | str) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(DDL)
        conn.commit()

        apply_additive_migrations(conn)
        validate_required_columns(conn)


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

        before_columns = get_columns(conn, TABLE_NAME)
        missing_additive = [
            name
            for name in ADDITIVE_COLUMNS
            if name not in before_columns
        ]

        for column_name in missing_additive:
            column_type = ADDITIVE_COLUMNS[column_name]
            print(f"[INFO] Adicionando coluna ausente: {column_name} {column_type}")

        apply_additive_migrations(conn)
        validate_required_columns(conn)

        count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]

    print("[OK] Schema rtd_option_quotes disponível.")
    print(f"[INFO] Linhas atuais: {count}")

    if count == 0:
        print("[INFO] Nenhum dado fictício foi inserido.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
