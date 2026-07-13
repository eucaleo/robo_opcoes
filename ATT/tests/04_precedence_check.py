# scripts/04_precedence_check.py
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

APP_DB = Path("./dados/app.db")

@dataclass(frozen=True)
class SnapshotKey:
    aba: str
    timestamp: str

def get_latest_ts(conn: sqlite3.Connection, table: str, aba: str) -> Optional[str]:
    row = conn.execute(
        f"SELECT MAX(timestamp) AS ts FROM {table} WHERE aba = ?",
        (aba,),
    ).fetchone()
    if not row:
        return None
    return row[0]

def count_rows(conn: sqlite3.Connection, table: str, aba: str, timestamp: str) -> int:
    row = conn.execute(
        f"SELECT COUNT(*) FROM {table} WHERE aba = ? AND timestamp = ?",
        (aba, timestamp),
    ).fetchone()
    return int(row[0] or 0)

def list_abas(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("""
        SELECT aba FROM (
            SELECT DISTINCT aba FROM manual_analise_robo_legs
            UNION
            SELECT DISTINCT aba FROM rtd_analise_robo_legs
        )
        ORDER BY aba
    """).fetchall()
    return [r[0] for r in rows]

def main() -> int:
    if not APP_DB.exists():
        raise SystemExit("ERRO: ./dados/app.db não encontrado")

    with sqlite3.connect(APP_DB) as conn:
        conn.row_factory = sqlite3.Row

        abas = list_abas(conn)
        print("== PRECEDENCE CHECK (manual > rtd) ==")
        print("Abas encontradas:", ", ".join(abas) if abas else "(nenhuma)")

        # Regra do domínio: tenta manual para (aba,timestamp); se não houver, cai no RTD.
        # Aqui vamos imprimir um resumo por aba com:
        # - latest_ts manual e contagem de legs manual
        # - latest_ts rtd e contagem de legs rtd
        # - se existe um timestamp que aparece nos dois (manual e rtd), com contagens em ambos
        for aba in abas:
            m_ts = get_latest_ts(conn, "manual_analise_robo_legs", aba)
            r_ts = get_latest_ts(conn, "rtd_analise_robo_legs", aba)

            print("\n----------------------------------")
            print("ABA:", aba)

            if m_ts:
                m_n = count_rows(conn, "manual_analise_robo_legs", aba, m_ts)
                print(f"MANUAL latest_ts={m_ts} rows={m_n}")
            else:
                print("MANUAL latest_ts=None rows=0")

            if r_ts:
                r_n = count_rows(conn, "rtd_analise_robo_legs", aba, r_ts)
                print(f"RTD    latest_ts={r_ts} rows={r_n}")
            else:
                print("RTD    latest_ts=None rows=0")

            # procura timestamp em comum para provar override 1:1 quando existir
            common = conn.execute("""
                SELECT m.timestamp AS ts,
                       (SELECT COUNT(*) FROM manual_analise_robo_legs mm WHERE mm.aba=? AND mm.timestamp=m.timestamp) AS m_cnt,
                       (SELECT COUNT(*) FROM rtd_analise_robo_legs rr WHERE rr.aba=? AND rr.timestamp=m.timestamp) AS r_cnt
                FROM manual_analise_robo_legs m
                WHERE m.aba=?
                  AND EXISTS (
                      SELECT 1 FROM rtd_analise_robo_legs r
                      WHERE r.aba=m.aba AND r.timestamp=m.timestamp
                  )
                ORDER BY m.timestamp DESC
                LIMIT 1
            """, (aba, aba, aba)).fetchone()

            if common:
                print(f"COMMON ts={common['ts']} manual_rows={common['m_cnt']} rtd_rows={common['r_cnt']}")
                print("Esperado: domínio escolhe MANUAL nesse (aba,timestamp).")
            else:
                print("COMMON ts: (nenhum timestamp comum manual x rtd para esta aba)")

        print("\nOK")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
