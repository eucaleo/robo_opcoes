# scripts/05_smoke_repo_status.py
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Optional, Tuple

APP_DB = Path("./dados/app.db")

# Garante que a raiz do projeto entre no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def latest_ts(conn: sqlite3.Connection, table: str, aba: str) -> Optional[str]:
    row = conn.execute(
        f"SELECT MAX(timestamp) FROM {table} WHERE aba=?",
        (aba,),
    ).fetchone()
    return row[0] if row else None

def choose_key(conn: sqlite3.Connection, aba: str) -> Tuple[Optional[str], Optional[str]]:
    m_ts = latest_ts(conn, "manual_analise_robo_legs", aba)
    if m_ts:
        return ("manual", m_ts)
    r_ts = latest_ts(conn, "rtd_analise_robo_legs", aba)
    if r_ts:
        return ("rtd", r_ts)
    return (None, None)

def main() -> int:
    if not APP_DB.exists():
        raise SystemExit("ERRO: ./dados/app.db não encontrado")

    with sqlite3.connect(APP_DB) as conn:
        conn.row_factory = sqlite3.Row
        abas = [r[0] for r in conn.execute("""
            SELECT aba FROM (
                SELECT DISTINCT aba FROM manual_analise_robo_legs
                UNION
                SELECT DISTINCT aba FROM rtd_analise_robo_legs
            )
            ORDER BY CASE WHEN aba='BOVA11' THEN 0 ELSE 1 END, aba
        """).fetchall()]

        if not abas:
            raise SystemExit("ERRO: nenhuma aba encontrada em manual/rtd legs")

        aba = abas[0]
        source, ts = choose_key(conn, aba)
        if not ts:
            raise SystemExit(f"ERRO: não achei timestamp para aba={aba}")

    print("== SMOKE REPO + STATUS ==")
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("ABA escolhida:", aba)
    print("Chave escolhida (esperada):", source, ts)

    try:
        from repositories.robo_legs_repository import RoboLegsRepository
    except Exception as e:
        print("\nERRO ao importar RoboLegsRepository:", repr(e))
        print("Dica: confirmar estrutura do projeto com find/grep.")
        raise

    repo = RoboLegsRepository()
    legs = repo.get_legs(aba, ts)
    print("\n-- Repository.get_legs --")
    print("qtd legs:", len(legs))
    if legs:
        print("leg[0]:", legs[0])

    try:
        from services.robo_legs_status_service import RoboLegsStatusService
    except Exception as e:
        print("\nERRO ao importar RoboLegsStatusService:", repr(e))
        print("Dica: confirmar estrutura do projeto com find/grep.")
        raise

    svc = RoboLegsStatusService()
    res = svc.status(aba, ts, ttl_seconds=300)

    print("\n-- StatusService.status --")
    for attr in ["freshness", "chosen_fonte", "chosen_ts", "manual_latest_ts", "rtd_latest_ts"]:
        print(f"{attr}:", getattr(res, attr, None))

    print("\nOK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
