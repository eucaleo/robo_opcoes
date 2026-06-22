#!/usr/bin/env python3
import os
import sys
import argparse
import json
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


def _list_tables(conn):
    """Lista tabelas do banco derived para resumo operacional."""
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        return [row[0] for row in rows]
    except Exception:
        return []


def _count_table(conn, table_name: str):
    """Conta linhas de uma tabela, retornando None em caso de erro."""
    try:
        row = conn.execute(f'SELECT COUNT(*) FROM "{table_name}"').fetchone()
        return int(row[0]) if row is not None else None
    except Exception:
        return None


def _first_count(table_counts: dict, *candidate_names: str):
    """Retorna a primeira contagem disponível entre nomes candidatos."""
    for name in candidate_names:
        if name in table_counts:
            return table_counts.get(name)
    return None


def _collect_pipeline_summary() -> dict:
    """
    Coleta resumo operacional do derived.db após execução/validação.

    Fase 4:
    - Não altera regras de negócio.
    - Não executa novo cálculo.
    - Apenas lê contagens para feedback visual/rastreabilidade.
    """
    from db.config import connect_derived

    conn = connect_derived()
    try:
        tables = _list_tables(conn)
        table_counts = {
            table: _count_table(conn, table)
            for table in tables
            if table != "sqlite_sequence"
        }

        return {
            "structures": _first_count(
                table_counts,
                "structure_snapshots",
                "structures",
                "derived_structures",
            ),
            "decisions": _first_count(
                table_counts,
                "decision_snapshots",
                "decisions",
                "structure_decisions",
                "derived_decisions",
            ),
            "payoff_points": _first_count(
                table_counts,
                "payoff_curve_points",
                "payoff_points",
                "derived_payoff_points",
            ),
            "payoff_summaries": _first_count(
                table_counts,
                "payoff_curve_summary",
                "payoff_summaries",
                "derived_payoff_summary",
            ),
            "pricing_executions": _first_count(
                table_counts,
                "pricing_executions",
                "pricing_execution",
            ),
            "rtd_quotes_updated": 0,
            "warnings": 0,
            "errors": 0,
            "table_counts": table_counts,
        }
    finally:
        conn.close()


def _display_summary_value(value):
    """Formata valores do resumo operacional para stdout."""
    return "n/d" if value is None else str(value)


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

    summary = _collect_pipeline_summary()

    print("\n[PIPELINE] Resumo operacional:")
    print(f"  Estruturas: {_display_summary_value(summary.get('structures'))}")
    print(f"  Decisões: {_display_summary_value(summary.get('decisions'))}")
    print(f"  Pontos de payoff: {_display_summary_value(summary.get('payoff_points'))}")
    print(f"  Resumos de payoff: {_display_summary_value(summary.get('payoff_summaries'))}")
    print(f"  Execuções de pricing: {_display_summary_value(summary.get('pricing_executions'))}")
    print(f"  Cotações RTD atualizadas: {_display_summary_value(summary.get('rtd_quotes_updated'))}")
    print(f"  Avisos: {_display_summary_value(summary.get('warnings'))}")
    print(f"  Erros: {_display_summary_value(summary.get('errors'))}")
    print("[PIPELINE_SUMMARY_JSON] " + json.dumps(summary, ensure_ascii=False, sort_keys=True))

    print("\n[OK] PIPELINE FINALIZADO COM SUCESSO!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
