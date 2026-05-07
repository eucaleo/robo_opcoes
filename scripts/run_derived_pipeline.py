#!/usr/bin/env python3
import os
import sys
import argparse
import traceback
from pathlib import Path
from typing import List, Dict

# --- bootstrap: garantir raiz do projeto no sys.path ANTES dos imports internos ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# -----------------------------------------------------------------------------

# Opcional: carregar .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from services.derived_service import (
    init_db,
    save_payoff_curve,
    save_decision,
    cleanup_derived,
    insert_consolidacao_close_reopen,
)
from domain.decision import compute_decision_for_aba
from domain.payoff import compute_payoff_for_aba, get_app_db_connection


def get_active_abas() -> List[str]:
    """Busca abas ativas no app.db"""
    conn = get_app_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT aba FROM rtd_analise_robo
        WHERE aba IS NOT NULL AND aba != ''
        ORDER BY aba
    """)
    abas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return abas


def process_aba_payoff_and_decision(aba: str) -> Dict:
    """Processa uma aba: calcula payoff + decisão + grava no derived.db"""
    result = {"aba": aba, "success": False, "errors": []}

    try:
        payoff_data = compute_payoff_for_aba(aba)
        timestamp_used = payoff_data.get("timestamp_used")
        if not timestamp_used:
            raise RuntimeError("compute_payoff_for_aba não retornou timestamp_used")
        print(f"[DERIVED] Snapshot timestamp_used: aba={aba}, ts={timestamp_used}")

        points_count = save_payoff_curve(
            aba=aba,
            points=payoff_data["points"],
            meta=payoff_data.get("meta"),
            timestamp=timestamp_used,
        )
        result["payoff_points"] = points_count

        decision_data = compute_decision_for_aba(
            aba=aba,
            pl_max=payoff_data["pl_max"],
        )

        decision_id = save_decision(
            aba=aba,
            decision=decision_data,
            timestamp=timestamp_used,
        )

        result.update({
            "decision_id": decision_id,
            "decision": decision_data.get("decision"),
            "level": decision_data.get("level"),
            "pl_atual": decision_data.get("pl_atual"),
            "pl_max": payoff_data.get("pl_max"),
            "ratio": decision_data.get("pl_pct_of_max"),
            "success": True,
        })

        if decision_data.get("decision") == "CLOSE_REOPEN":
            insert_consolidacao_close_reopen(
                aba=aba,
                timestamp=timestamp_used,
                pl_atual=decision_data.get("pl_atual"),
                pl_max=payoff_data.get("pl_max"),
                ratio=decision_data.get("pl_pct_of_max", 0.0),
            )

    except Exception as e:
        result["errors"].append(f"Erro no processamento: {str(e)}\n{traceback.format_exc()}")

    return result


def main():
    parser = argparse.ArgumentParser(description="Pipeline de derivados - payoff e decisões")
    parser.add_argument("--aba", help="Processar apenas esta aba")
    parser.add_argument("--no-cleanup", action="store_true", help="Pular limpeza de dados antigos")
    parser.add_argument("--limit-abas", type=int, help="Processar no máximo N abas")
    args = parser.parse_args()

    from db.config import DERIVED_DB_PATH
    print(f"[PIPELINE] Usando derived DB: {DERIVED_DB_PATH}")

    if args.aba:
        print(f"[PIPELINE] Modo: processar apenas aba '{args.aba}'")
    else:
        print("[PIPELINE] Modo: processar todas as abas ativas")

    init_db()
    print("[DERIVED] derived.db inicializado")

    all_abas = get_active_abas()
    if args.aba:
        abas = [args.aba] if args.aba in all_abas else []
        if not abas:
            print(f"[DERIVED] AVISO: aba '{args.aba}' não encontrada em rtd_analise_robo")
            print(f"[DERIVED] Abas disponíveis: {all_abas}")
            return 2
    else:
        abas = all_abas
        if args.limit_abas and args.limit_abas > 0:
            abas = abas[:args.limit_abas]

    print(f"[DERIVED] {len(abas)} aba(s) para processar: {abas}")
    if not abas:
        print("[DERIVED] Nenhuma aba para processar")
        return 0

    results = []
    for aba in abas:
        print(f"\n[DERIVED] Processando {aba}...")
        result = process_aba_payoff_and_decision(aba)
        results.append(result)

        if result["success"]:
            print(f"  [DERIVED] Payoff: {result['payoff_points']} pontos, PL_max: {result['pl_max']:.2f}")
            print(f"  [DERIVED] Decisão: {result['decision']} (nível {result['level']}) - ratio: {result['ratio'] * 100:.1f}%")
        else:
            print(f"  [DERIVED] Erros: {result['errors']}")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print("\n[DERIVED] RESUMO:")
    print(f"  [DERIVED] Processadas com sucesso: {len(successful)}")
    print(f"  [DERIVED] Falharam: {len(failed)}")

    if successful:
        decisions_summary = {}
        for r in successful:
            dec = r["decision"]
            decisions_summary[dec] = decisions_summary.get(dec, 0) + 1
        print(f"  [DERIVED] Decisões: {decisions_summary}")

    if not args.no_cleanup:
        deleted = cleanup_derived(days_to_keep=30)
        print(f"[DERIVED] Limpeza: {deleted}")
    else:
        print("[DERIVED] Limpeza pulada (--no-cleanup)")

    app_db = "data/app.db"
    derived_db = os.getenv("DERIVED_DB_PATH", "data/derived.db")
    print("\n[DERIVED] Bancos:")
    print(f"  Raw: {os.path.abspath(app_db)}")
    print(f"  Derived: {os.path.abspath(derived_db)}")

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
