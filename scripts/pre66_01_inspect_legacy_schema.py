"""
pre66_01_inspect_legacy_schema.py
Inspeciona schema e amostra de dados das tabelas legadas.
Nenhuma alteracao. Somente leitura.
"""
import sqlite3
import os
from pathlib import Path

DB_PATH = Path("dados/app.db")


def inspect_table(conn, table_name):
    cur = conn.cursor()

    print(f"\n{'='*60}")
    print(f"TABELA: {table_name}")
    print(f"{'='*60}")

    # Schema
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = cur.fetchall()
    if not cols:
        print(f"  [AVISO] Tabela '{table_name}' nao encontrada ou vazia.")
        return []

    col_names = [c[1] for c in cols]
    print("\nColunas:")
    for c in cols:
        print(f"  [{c[0]}] {c[1]:30s} type={c[2]:15s} notnull={c[3]} default={c[4]}")

    # Contagem
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    total = cur.fetchone()[0]
    print(f"\nTotal de registros: {total}")

    # Valores distintos de 'aba' se existir
    if "aba" in col_names:
        cur.execute(f"SELECT DISTINCT aba FROM {table_name} ORDER BY aba LIMIT 30")
        abas = [r[0] for r in cur.fetchall()]
        print(f"\nValores distintos de 'aba' (max 30): {len(abas)} encontrados")
        for a in abas:
            print(f"  - {a}")

    # Amostra de 3 registros
    print("\nAmostra (3 registros):")
    cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
    rows = cur.fetchall()
    for row in rows:
        for col, val in zip(col_names, row):
            print(f"  {col:30s} = {val}")
        print("  ---")

    return col_names


def main():
    if not DB_PATH.exists():
        print(f"[ERRO] Banco nao encontrado: {DB_PATH}")
        return

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    tables = [
        "rtd_analise_robo",
        "rtd_analise_robo_legs",
        "manual_analise_robo_legs",
        "structures",
        "structure_legs",
    ]

    for t in tables:
        inspect_table(conn, t)

    conn.close()
    print("\n[OK] Inspecao concluida. Nenhum dado alterado.")


if __name__ == "__main__":
    main()
