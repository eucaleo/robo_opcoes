#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-5d-validacao-rtd-restaurado-operacional.txt"

{
  echo "============================================================"
  echo "FASE 5D - VALIDACAO OPERACIONAL RTD RESTAURADO"
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

  echo "== Arquivo CSV atual =="
  if [ -f dados/RTD_LINKS.csv ]; then
    ls -l dados/RTD_LINKS.csv
    echo
    echo "Primeiras linhas:"
    sed -n '1,10p' dados/RTD_LINKS.csv
  else
    echo "ERRO: dados/RTD_LINKS.csv ausente"
  fi
  echo

  echo "== Arquivo de símbolos atual =="
  if [ -f dados/rtd_symbols.txt ]; then
    ls -l dados/rtd_symbols.txt
    echo
    cat dados/rtd_symbols.txt
  else
    echo "dados/rtd_symbols.txt ausente"
  fi
  echo

  echo "== Auditoria antes - app.db =="
  python scripts/audit_rtd_option_quotes.py --db dados/app.db --max-age-minutes 0
  echo

  echo "== Auditoria antes - derived.db =="
  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
  echo

  echo "== Dry-run importador - app.db =="
  python scripts/import_rtd_option_quotes_wide_csv.py \
    --csv dados/RTD_LINKS.csv \
    --db dados/app.db \
    --dry-run
  echo

  echo "== Dry-run importador - derived.db =="
  python scripts/import_rtd_option_quotes_wide_csv.py \
    --csv dados/RTD_LINKS.csv \
    --db dados/derived.db \
    --dry-run
  echo

  echo "== Pipeline RTD restaurado - app.db =="
  python scripts/run_rtd_option_quotes_pipeline.py \
    --csv dados/RTD_LINKS.csv \
    --db dados/app.db \
    --max-age-minutes 0
  echo

  echo "== Pipeline RTD restaurado - derived.db =="
  python scripts/run_rtd_option_quotes_pipeline.py \
    --csv dados/RTD_LINKS.csv \
    --db dados/derived.db \
    --max-age-minutes 0
  echo

  echo "== Auditoria depois - app.db =="
  python scripts/audit_rtd_option_quotes.py --db dados/app.db --max-age-minutes 0
  echo

  echo "== Auditoria depois - derived.db =="
  python scripts/audit_rtd_option_quotes.py --db dados/derived.db --max-age-minutes 0
  echo

  echo "== Estado SQLite resumido =="
  python - <<'PY'
import sqlite3
from pathlib import Path

for db in ["dados/app.db", "dados/derived.db"]:
    print("=" * 60)
    print("DB:", db)
    p = Path(db)
    print("Existe:", p.exists())
    if not p.exists():
        continue

    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    try:
        exists = con.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type='table'
              AND name='rtd_option_quotes'
            """
        ).fetchone()
        print("rtd_option_quotes existe:", bool(exists))
        if not exists:
            continue

        row = con.execute(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(DISTINCT codigo_opcao) AS distintos,
                MIN(updated_at) AS min_updated_at,
                MAX(updated_at) AS max_updated_at
            FROM rtd_option_quotes
            """
        ).fetchone()
        print(dict(row))

        rows = con.execute(
            """
            SELECT
                codigo_opcao,
                ativo_base,
                call_put,
                strike,
                vencimento,
                ultimo_preco,
                bid,
                ask,
                source,
                updated_at
            FROM rtd_option_quotes
            ORDER BY codigo_opcao
            """
        ).fetchall()

        for r in rows:
            print(dict(r))
    finally:
        con.close()
PY
  echo

  echo "== Testes RTD restaurados novamente =="
  python -m pytest -q \
    ATT/tests/test_audit_rtd_option_quotes.py \
    ATT/tests/test_import_rtd_links_to_option_quotes.py \
    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
    ATT/tests/test_rtd_option_quotes_repository_contract.py
  echo

  echo "== Status git final =="
  git status --short
  echo

  echo "============================================================"
  echo "FIM FASE 5D VALIDACAO OPERACIONAL"
  echo "============================================================"
} > "$OUT" 2>&1

echo "Validacao Fase 5D registrada em: $OUT"
