#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-5e-validacao-integracao-rtd-derived-pipeline.txt"

{
  echo "============================================================"
  echo "FASE 5E - VALIDACAO INTEGRACAO RTD NO DERIVED PIPELINE"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "============================================================"
  echo

  echo "== Status git inicial =="
  git status --short
  echo

  echo "== Diff scripts/run_derived_pipeline.py =="
  git diff -- scripts/run_derived_pipeline.py
  echo

  echo "== Teste novo =="
  sed -n '1,260p' ATT/tests/test_run_derived_pipeline_rtd_integration.py
  echo

  echo "== Py compile =="
  python -m py_compile scripts/run_derived_pipeline.py
  echo "py_compile ok"
  echo

  echo "== Testes focados RTD/pipeline =="
  python -m pytest \
    ATT/tests/test_run_derived_pipeline_rtd_integration.py \
    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
    ATT/tests/test_audit_rtd_option_quotes.py \
    ATT/tests/test_import_rtd_links_to_option_quotes.py \
    ATT/tests/test_rtd_option_quotes_repository_contract.py \
    -q
  echo

  echo "== Execucao run_derived_pipeline.py --no-cleanup =="
  python scripts/run_derived_pipeline.py --no-cleanup
  echo

  echo "== Auditoria derived.db depois do pipeline derivado =="
  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
  echo

  echo "== Estado SQLite rtd_option_quotes derived.db =="
  python - <<'PY'
import sqlite3
from pathlib import Path

db = Path("dados/derived.db")
print("DB:", db)
print("Existe:", db.exists())

con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
try:
    exists = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='rtd_option_quotes'"
    ).fetchone()
    print("rtd_option_quotes existe:", bool(exists))

    if exists:
        row = con.execute("""
            SELECT
                COUNT(*) AS total,
                COUNT(DISTINCT codigo_opcao) AS distintos,
                MIN(updated_at) AS min_updated_at,
                MAX(updated_at) AS max_updated_at
            FROM rtd_option_quotes
        """).fetchone()
        print(dict(row))

        for row in con.execute("""
            SELECT codigo_opcao, ativo_base, call_put, strike, vencimento,
                   ultimo_preco, bid, ask, source, updated_at
            FROM rtd_option_quotes
            ORDER BY codigo_opcao
            LIMIT 20
        """).fetchall():
            print(dict(row))
finally:
    con.close()
PY
  echo

  echo "== Suite completa =="
  python -m pytest ATT/tests -q
  echo

  echo "== Status git final =="
  git status --short
  echo

  echo "============================================================"
  echo "FIM FASE 5E VALIDACAO"
  echo "============================================================"
} > "$OUT" 2>&1

echo "Validacao Fase 5E registrada em: $OUT"
