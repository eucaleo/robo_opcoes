# scripts/02_legs_integrity_report.py
from __future__ import annotations

import sqlite3
from pathlib import Path

APP_DB = Path("./dados/app.db")

LEG_TABLES = [
    "rtd_analise_robo_legs",
    "manual_analise_robo_legs",
]

def count(conn: sqlite3.Connection, sql: str, params=()) -> int:
    return int(conn.execute(sql, params).fetchone()[0] or 0)

def sample(conn: sqlite3.Connection, sql: str, params=(), limit: int = 5):
    return conn.execute(sql + f" LIMIT {limit}", params).fetchall()

def main() -> int:
    if not APP_DB.exists():
        raise SystemExit("ERRO: ./dados/app.db não encontrado")

    with sqlite3.connect(APP_DB) as conn:
        conn.row_factory = sqlite3.Row

        for t in LEG_TABLES:
            print(f"\n==============================")
            print(f"INTEGRITY: {t}")
            print(f"==============================")

            total = count(conn, f"SELECT COUNT(*) FROM {t}")
            print("Total rows:", total)

            # Nulos críticos
            null_ts = count(conn, f"SELECT COUNT(*) FROM {t} WHERE timestamp IS NULL OR TRIM(timestamp) = ''")
            null_aba = count(conn, f"SELECT COUNT(*) FROM {t} WHERE aba IS NULL OR TRIM(aba) = ''")
            null_strike = count(conn, f"SELECT COUNT(*) FROM {t} WHERE strike IS NULL OR TRIM(CAST(strike AS TEXT)) = ''")
            null_quant = count(conn, f"SELECT COUNT(*) FROM {t} WHERE quant IS NULL OR TRIM(CAST(quant AS TEXT)) = ''")

            print("NULL/empty timestamp:", null_ts)
            print("NULL/empty aba:", null_aba)
            print("NULL/empty strike:", null_strike)
            print("NULL/empty quant:", null_quant)

            # Valores fora do padrão (heurística, sem "corrigir" nada)
            bad_call_put = count(conn, f"""
                SELECT COUNT(*) FROM {t}
                WHERE call_put IS NOT NULL
                  AND UPPER(TRIM(call_put)) NOT IN ('CALL','PUT','C','P')
            """)
            bad_cv = count(conn, f"""
                SELECT COUNT(*) FROM {t}
                WHERE cv IS NOT NULL
                  AND UPPER(TRIM(cv)) NOT IN ('C','V','COMPRA','VENDA','BUY','SELL','LONG','SHORT')
            """)

            print("call_put fora do esperado:", bad_call_put)
            print("cv fora do esperado:", bad_cv)

            # Amostras
            if null_ts:
                rows = sample(conn, f"SELECT rowid, aba, timestamp, cv, call_put, strike, quant FROM {t} WHERE timestamp IS NULL OR TRIM(timestamp) = ''")
                print("\nExemplos timestamp vazio:")
                for r in rows:
                    print(dict(r))

            if bad_call_put:
                rows = sample(conn, f"""
                    SELECT rowid, aba, timestamp, call_put
                    FROM {t}
                    WHERE call_put IS NOT NULL
                      AND UPPER(TRIM(call_put)) NOT IN ('CALL','PUT','C','P')
                """)
                print("\nExemplos call_put inválido:")
                for r in rows:
                    print(dict(r))

            if bad_cv:
                rows = sample(conn, f"""
                    SELECT rowid, aba, timestamp, cv
                    FROM {t}
                    WHERE cv IS NOT NULL
                      AND UPPER(TRIM(cv)) NOT IN ('C','V','COMPRA','VENDA','BUY','SELL','LONG','SHORT')
                """)
                print("\nExemplos cv inválido:")
                for r in rows:
                    print(dict(r))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
