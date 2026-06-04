# scripts/62_inspect_snapshot_tables.py
"""
Inspeciona o schema real das tabelas de snapshot no app.db
Uso: python scripts/62_inspect_snapshot_tables.py
"""
from pathlib import Path
import sqlite3
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "dados" / "app.db"

TABELAS = [
    "rtd_analise_robo",
    "rtd_analise_robo_legs",
    "manual_analise_robo_legs",
]

def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    for tabela in TABELAS:
        print(f"\n {tabela} ")
        try:
            info = conn.execute(f"PRAGMA table_info({tabela})").fetchall()
            if not info:
                print("  [AVISO]  Tabela não encontrada ou vazia")
                continue
            for col in info:
                print(f"  [{col['cid']:>2}] {col['name']:<30} {col['type']:<15} notnull={col['notnull']} pk={col['pk']}")

            # Mostra uma amostra de dados (1 linha)
            row = conn.execute(f"SELECT * FROM {tabela} LIMIT 1").fetchone()
            if row:
                print(f"\n  Amostra:")
                for k in row.keys():
                    print(f"    {k}: {row[k]}")
            else:
                print(f"\n  [INFO]  Tabela vazia")
        except Exception as e:
            print(f"  [FALHOU] Erro: {e}")

    conn.close()

if __name__ == "__main__":
    main()
