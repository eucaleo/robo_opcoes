#!/usr/bin/env python3
import os
import sys
import argparse
import traceback
import subprocess
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





def validate_final_consistency() -> bool:
    """Valida consistência dos snapshots após processamento."""
    from db.derived_repo import get_derived_connection, validate_snapshot_consistency
    
    conn = get_derived_connection()
    try:
        return validate_snapshot_consistency(conn)
    finally:
        conn.close()



def _run_build_summaries(repo_root: str):
    """Gera payoff_curve_summary a partir de payoff_curve_points."""
    env = os.environ.copy()

    if not args.no_cleanup:
        cleanup_derived(days_to_keep=30)

    # Validação final OBRIGATÓRIA
    print("
[PIPELINE] Validando consistência final dos snapshots...")
    if not validate_final_consistency():
        print("[ERROR] PIPELINE FALHOU: Inconsistências detectadas nos snapshots")
        return 1

    print("
[OK] PIPELINE FINALIZADO COM SUCESSO!")
    print(f"Processadas {len(results)} abas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
