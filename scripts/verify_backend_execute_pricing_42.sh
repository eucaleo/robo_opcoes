#!/usr/bin/env bash
set -u

echo "==> verificacao 42 - teste backend execute_pricing sem UI"
date
echo

ROOT_DIR="$(pwd)"
OUT_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_CENTRO_VERDADE_34/VERIFICACAO_BACKEND_EXECUTE_PRICING_42"
mkdir -p "$OUT_DIR"

LOG="$OUT_DIR/01_backend_execute_pricing_42.log"
PY="$OUT_DIR/02_backend_execute_pricing_42.py"

echo "Diretorio raiz: $ROOT_DIR" | tee "$LOG"
echo "Saida: $OUT_DIR" | tee -a "$LOG"
echo | tee -a "$LOG"

echo "==> status git inicial" | tee -a "$LOG"
git status --short | tee "$OUT_DIR/00_git_status_inicial.txt" | tee -a "$LOG"
echo | tee -a "$LOG"

cat > "$PY" <<'PY'
from __future__ import annotations

import inspect
import json
import os
import sqlite3
import sys
import traceback
from pathlib import Path

ROOT = Path.cwd()
DB_PATH = ROOT / "dados" / "app.db"
STRUCTURE_ID = 2

TABLES = [
    "pricing_executions",
    "structure_snapshots",
    "payoff_curve_points",
    "structure_decisions",
]

def count_rows(conn: sqlite3.Connection, table: str) -> int | None:
    try:
        cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
        return int(cur.fetchone()[0])
    except Exception:
        return None

def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table,),
    )
    return cur.fetchone() is not None

def snapshot_counts(label: str) -> dict:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {DB_PATH}")

    with sqlite3.connect(str(DB_PATH)) as conn:
        result = {}
        for table in TABLES:
            result[table] = count_rows(conn, table) if table_exists(conn, table) else None
        return result

def try_build_app_service():
    from services.pricing_execution_app_service import PricingExecutionAppService

    sig = inspect.signature(PricingExecutionAppService)
    print("PricingExecutionAppService signature:", sig)

    attempts = []

    attempts.append(("no_args", lambda: PricingExecutionAppService()))

    attempts.append((
        "db_path_keyword",
        lambda: PricingExecutionAppService(db_path=str(DB_PATH)),
    ))

    attempts.append((
        "app_db_path_keyword",
        lambda: PricingExecutionAppService(app_db_path=str(DB_PATH)),
    ))

    last_error = None

    for name, factory in attempts:
        try:
            svc = factory()
            print(f"OK: instancia criada por tentativa: {name}")
            return svc
        except Exception as exc:
            last_error = exc
            print(f"INFO: tentativa falhou: {name}: {type(exc).__name__}: {exc}")

    raise RuntimeError(
        "Nao foi possivel instanciar PricingExecutionAppService automaticamente. "
        f"Ultimo erro: {last_error}"
    )

def call_execute_pricing(service):
    method = getattr(service, "execute_pricing")
    sig = inspect.signature(method)
    print("execute_pricing signature:", sig)

    attempts = [
        ("structure_id_keyword", lambda: method(structure_id=STRUCTURE_ID)),
        ("positional_structure_id", lambda: method(STRUCTURE_ID)),
    ]

    last_error = None

    for name, caller in attempts:
        try:
            result = caller()
            print(f"OK: execute_pricing executado por tentativa: {name}")
            return result
        except Exception as exc:
            last_error = exc
            print(f"INFO: chamada falhou: {name}: {type(exc).__name__}: {exc}")

    raise RuntimeError(
        "Nao foi possivel chamar execute_pricing automaticamente. "
        f"Ultimo erro: {last_error}"
    )

def main() -> int:
    print("ROOT:", ROOT)
    print("DB_PATH:", DB_PATH)
    print("STRUCTURE_ID:", STRUCTURE_ID)
    print()

    before = snapshot_counts("before")
    print("COUNTS_BEFORE:")
    print(json.dumps(before, indent=2, ensure_ascii=False))
    print()

    service = try_build_app_service()
    result = call_execute_pricing(service)

    print()
    print("EXECUTE_RESULT_TYPE:", type(result).__name__)
    try:
        print("EXECUTE_RESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    except Exception:
        print("EXECUTE_RESULT_REPR:")
        print(repr(result))

    print()
    after = snapshot_counts("after")
    print("COUNTS_AFTER:")
    print(json.dumps(after, indent=2, ensure_ascii=False))
    print()

    deltas = {}
    for table in TABLES:
        if before.get(table) is None or after.get(table) is None:
            deltas[table] = None
        else:
            deltas[table] = after[table] - before[table]

    print("DELTAS:")
    print(json.dumps(deltas, indent=2, ensure_ascii=False))
    print()

    required = [
        "pricing_executions",
        "structure_snapshots",
        "payoff_curve_points",
        "structure_decisions",
    ]

    failures = []
    for table in required:
        delta = deltas.get(table)
        if delta is None:
            failures.append(f"{table}: tabela ausente ou contagem indisponivel")
        elif delta <= 0:
            failures.append(f"{table}: delta nao subiu ({delta})")

    if failures:
        print("RESULTADO: FALHA")
        for item in failures:
            print("FALHA:", item)
        return 1

    print("RESULTADO: OK")
    print("As quatro contagens subiram apos execute_pricing.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        print("RESULTADO: FALHA")
        traceback.print_exc()
        raise SystemExit(1)
PY

echo "==> executando teste backend" | tee -a "$LOG"
PYTHONPATH=. python "$PY" > "$OUT_DIR/03_backend_execute_pricing_42_output.txt" 2>&1
RC=$?

cat "$OUT_DIR/03_backend_execute_pricing_42_output.txt" | tee -a "$LOG"
echo | tee -a "$LOG"

echo "==> status git final" | tee -a "$LOG"
git status --short | tee "$OUT_DIR/04_git_status_final.txt" | tee -a "$LOG"
echo | tee -a "$LOG"

if [ "$RC" -eq 0 ]; then
  echo "RESULTADO: OK" | tee -a "$LOG"
  echo "Backend execute_pricing validado sem UI." | tee -a "$LOG"
else
  echo "RESULTADO: FALHA" | tee -a "$LOG"
  echo "Verifique o arquivo:" | tee -a "$LOG"
  echo "$OUT_DIR/03_backend_execute_pricing_42_output.txt" | tee -a "$LOG"
fi

echo | tee -a "$LOG"
echo "Nenhum git add, commit ou push foi executado por este script." | tee -a "$LOG"
exit "$RC"
