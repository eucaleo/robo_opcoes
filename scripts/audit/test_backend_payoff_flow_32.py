from pathlib import Path
from datetime import datetime
import json
import os
import sqlite3
import sys
import traceback

ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = os.environ.get("APP_DB_PATH")
STRUCTURE_ID = int(os.environ.get("STRUCTURE_ID", "2"))

TABLES = [
    "pricing_executions",
    "structure_snapshots",
    "system_snapshots",
    "payoff_curve_points",
    "structure_decisions",
]

def count_table(conn, table_name):
    try:
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        return int(cursor.fetchone()[0])
    except Exception as exc:
        return f"ERRO: {exc}"

def collect_counts(db_path):
    conn = sqlite3.connect(db_path)
    try:
        return {table: count_table(conn, table) for table in TABLES}
    finally:
        conn.close()

def diff_counts(before, after):
    result = {}

    for table in TABLES:
        b = before.get(table)
        a = after.get(table)

        if isinstance(b, int) and isinstance(a, int):
            result[table] = a - b
        else:
            result[table] = None

    return result

def execute_pricing(structure_id):
    sys.path.insert(0, str(ROOT))

    from services.pricing_execution_app_service import PricingExecutionAppService

    service = PricingExecutionAppService()

    attempts = [
        lambda: service.execute_pricing(structure_id=structure_id),
        lambda: service.execute_pricing(structure_id),
    ]

    last_exc = None

    for attempt in attempts:
        try:
            return attempt()
        except TypeError as exc:
            last_exc = exc

    raise last_exc

def main():
    if not DB_PATH:
        raise SystemExit(
            "Defina APP_DB_PATH antes de executar. Exemplo:\n"
            "APP_DB_PATH='caminho/do/banco.db' STRUCTURE_ID=2 "
            "python scripts/audit/test_backend_payoff_flow_32.py"
        )

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "db_path": DB_PATH,
        "structure_id": STRUCTURE_ID,
        "before": None,
        "after": None,
        "diff": None,
        "execute_pricing_result": None,
        "error": None,
        "traceback": None,
    }

    try:
        before = collect_counts(DB_PATH)
        result = execute_pricing(STRUCTURE_ID)
        after = collect_counts(DB_PATH)

        report["before"] = before
        report["after"] = after
        report["diff"] = diff_counts(before, after)
        report["execute_pricing_result"] = repr(result)

    except Exception as exc:
        report["error"] = str(exc)
        report["traceback"] = traceback.format_exc()

    out_file = OUT_DIR / "RELATORIO_32_1_TESTE_BACKEND_PAYOFF_FLOW.json"
    out_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"OK: relatório gerado em {out_file}")

    if report["error"]:
        print("ERRO durante o teste backend.")
        print(report["error"])
        raise SystemExit(1)

    diff = report["diff"] or {}

    print("Resumo de incremento:")
    for table, value in diff.items():
        print(f"- {table}: {value}")

    payoff_delta = diff.get("payoff_curve_points")
    decision_delta = diff.get("structure_decisions")

    if isinstance(payoff_delta, int) and payoff_delta <= 0:
        print("WARNING: pricing executou, mas payoff_curve_points não aumentou.")

    if isinstance(decision_delta, int) and decision_delta <= 0:
        print("WARNING: pricing executou, mas structure_decisions não aumentou.")

if __name__ == "__main__":
    main()
