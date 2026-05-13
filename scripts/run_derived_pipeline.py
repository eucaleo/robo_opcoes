#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

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


def validate_final_consistency() -> bool:
    """Valida consistência dos snapshots após processamento."""
    from db.config import connect_derived
    from db.derived_repo import validate_snapshot_consistency
    
    conn = connect_derived()
    try:
        return validate_snapshot_consistency(conn)
    finally:
        conn.close()



def _run_build_summaries(repo_root: str) -> int:
    """
    Placeholder: Gera payoff_curve_summary a partir de payoff_curve_points.
    (Implemente aqui quando necessário.)
    """
    _ = repo_root
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run derived pipeline")
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Não executar cleanup do derived.db antes de validar",
    )
    args = parser.parse_args(argv)

    # Imports internos (mantidos aqui para respeitar sys.path/bootstrap)
    from services.derived_service import cleanup_derived

    if not args.no_cleanup:
        cleanup_derived(days_to_keep=30)

    # (Opcional) build summaries
    rc = _run_build_summaries(str(PROJECT_ROOT))
    if rc != 0:
        return rc

    # Validação final OBRIGATÓRIA
    print("\n[PIPELINE] Validando consistência final dos snapshots...")
    if not validate_final_consistency():
        print("[ERROR] PIPELINE FALHOU: Inconsistências detectadas nos snapshots")
        return 1

    print("\n[OK] PIPELINE FINALIZADO COM SUCESSO!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
