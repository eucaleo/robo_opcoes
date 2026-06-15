#!/usr/bin/env python
"""
Limpa e popula rtd_option_quotes com dados manuais atuais das estruturas
SPSB-SMAL e PRIO.

Uso:

    python scripts/seed_current_rtd_option_quotes.py
    python scripts/seed_current_rtd_option_quotes.py --db dados/app.db

Observação:

- O script limpa somente a tabela rtd_option_quotes.
- Não altera outras tabelas do banco.
- updated_at e created_at são preenchidos com o timestamp atual.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB = "dados/app.db"


CURRENT_QUOTES = [
    {
        "codigo_opcao": "SMALF129",
        "ativo_base": "SMAL",
        "estrutura": "SPSB-SMAL",
        "preco_referencia_ativo": 108.45,
        "call_put": "C",
        "strike": 129.0,
        "ultimo_preco": 1.25,
        "ultima_quantidade": 4500,
    },
    {
        "codigo_opcao": "SMALF103",
        "ativo_base": "SMAL",
        "estrutura": "SPSB-SMAL",
        "preco_referencia_ativo": 108.45,
        "call_put": "V",
        "strike": 103.0,
        "ultimo_preco": 4.00,
        "ultima_quantidade": 2000,
    },
    {
        "codigo_opcao": "SMALR127",
        "ativo_base": "SMAL",
        "estrutura": "SPSB-SMAL",
        "preco_referencia_ativo": 108.45,
        "call_put": "V",
        "strike": 127.0,
        "ultimo_preco": 10.32,
        "ultima_quantidade": 2100,
    },
    {
        "codigo_opcao": "SMALR108",
        "ativo_base": "SMAL",
        "estrutura": "SPSB-SMAL",
        "preco_referencia_ativo": 108.45,
        "call_put": "C",
        "strike": 108.0,
        "ultimo_preco": 1.41,
        "ultima_quantidade": 2500,
    },
    {
        "codigo_opcao": "PRIOG800",
        "ativo_base": "PRIO",
        "estrutura": "PRIO",
        "preco_referencia_ativo": 61.34,
        "call_put": "C",
        "strike": 80.0,
        "ultimo_preco": 0.46,
        "ultima_quantidade": 1000,
    },
    {
        "codigo_opcao": "PRIOH515",
        "ativo_base": "PRIO",
        "estrutura": "PRIO",
        "preco_referencia_ativo": 61.34,
        "call_put": "V",
        "strike": 51.5,
        "ultimo_preco": 13.94,
        "ultima_quantidade": 1000,
    },
    {
        "codigo_opcao": "PRIOT700",
        "ativo_base": "PRIO",
        "estrutura": "PRIO",
        "preco_referencia_ativo": 61.34,
        "call_put": "V",
        "strike": 70.0,
        "ultimo_preco": 6.64,
        "ultima_quantidade": 1000,
    },
    {
        "codigo_opcao": "PRIOS525",
        "ativo_base": "PRIO",
        "estrutura": "PRIO",
        "preco_referencia_ativo": 61.34,
        "call_put": "C",
        "strike": 52.5,
        "ultimo_preco": 0.20,
        "ultima_quantidade": 1000,
    },
]


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def seed_database(db_path: str) -> int:
    database = Path(db_path)

    if not database.exists():
        raise FileNotFoundError(f"Banco não encontrado: {database}")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect(database) as connection:
        if not table_exists(connection, "rtd_option_quotes"):
            raise RuntimeError("Tabela rtd_option_quotes não encontrada.")

        before_count = connection.execute(
            "SELECT COUNT(*) FROM rtd_option_quotes"
        ).fetchone()[0]

        connection.execute("DELETE FROM rtd_option_quotes")

        insert_sql = """
            INSERT INTO rtd_option_quotes (
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                ultima_quantidade,
                bid,
                ask,
                volume,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            )
            VALUES (
                :codigo_opcao,
                :ativo_base,
                :call_put,
                :strike,
                :vencimento,
                :ultimo_preco,
                :ultima_quantidade,
                :bid,
                :ask,
                :volume,
                :iv,
                :delta,
                :gamma,
                :theta,
                :vega,
                :source,
                :raw_json,
                :updated_at,
                :created_at
            )
        """

        for quote in CURRENT_QUOTES:
            payload = {
                "origem": "seed_manual_fase_7g",
                "estrutura": quote["estrutura"],
                "preco_referencia_ativo": quote["preco_referencia_ativo"],
                "valor_executado": quote["ultimo_preco"],
                "quantidade": quote["ultima_quantidade"],
            }

            record = {
                "codigo_opcao": quote["codigo_opcao"],
                "ativo_base": quote["ativo_base"],
                "call_put": quote["call_put"],
                "strike": quote["strike"],
                "vencimento": None,
                "ultimo_preco": quote["ultimo_preco"],
                "ultima_quantidade": quote["ultima_quantidade"],
                "bid": None,
                "ask": None,
                "volume": None,
                "iv": None,
                "delta": None,
                "gamma": None,
                "theta": None,
                "vega": None,
                "source": "manual_seed_fase_7g",
                "raw_json": json.dumps(payload, ensure_ascii=False, sort_keys=True),
                "updated_at": now,
                "created_at": now,
            }

            connection.execute(insert_sql, record)

        after_count = connection.execute(
            "SELECT COUNT(*) FROM rtd_option_quotes"
        ).fetchone()[0]

        connection.commit()

    print("Seed rtd_option_quotes concluído.")
    print(f"Banco: {database}")
    print(f"Registros removidos: {before_count}")
    print(f"Registros inseridos: {after_count}")
    print(f"Timestamp aplicado: {now}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Limpa e popula rtd_option_quotes com dados atuais de SMAL e PRIO."
    )
    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help=f"Caminho do banco SQLite. Padrão: {DEFAULT_DB}",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return seed_database(args.db)


if __name__ == "__main__":
    raise SystemExit(main())
