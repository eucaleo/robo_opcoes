#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-5b-diagnostico-rtd-cadeia-real.txt"

{
  echo "============================================================"
  echo "FASE 5B - DIAGNOSTICO RTD CADEIA REAL E HISTORICO"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "============================================================"
  echo

  echo "== Status git =="
  git status --short
  echo

  echo "== Arquivos rastreados relacionados a RTD/quotes =="
  git ls-files | grep -Ei "rtd|quote|market|snapshot" | sort
  echo

  echo "== Arquivos atuais em scripts relacionados a RTD/quotes =="
  find scripts -maxdepth 2 -type f \
    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
    -not -path '*/__pycache__/*' \
    | sort
  echo

  echo "== Arquivos atuais em infra relacionados a RTD/quotes =="
  find infra -maxdepth 2 -type f \
    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
    -not -path '*/__pycache__/*' \
    | sort 2>/dev/null
  echo

  echo "== Arquivos atuais em repositories/services relacionados a RTD/quotes =="
  find repositories services -maxdepth 2 -type f \
    \( -iname '*rtd*' -o -iname '*quote*' -o -iname '*market*' -o -iname '*snapshot*' \) \
    -not -path '*/__pycache__/*' \
    | sort
  echo

  echo "== Historico Git de scripts RTD conhecidos =="
  for f in \
    scripts/run_rtd_option_quotes_pipeline.py \
    scripts/import_rtd_links_to_option_quotes.py \
    scripts/import_rtd_option_quotes_wide_csv.py \
    scripts/build_rtd_symbols.py \
    scripts/run_rtd_refresh_full.py \
    scripts/audit_rtd_option_quotes.py \
    scripts/refresh_rtd_option_quotes_excel.ps1 \
    infra/bootstrap_rtd_option_quotes_schema.py
  do
    echo "---- $f ----"
    git log --all --follow --oneline -- "$f" | head -20
    echo
  done
  echo

  echo "== Alteracoes historicas por nome contendo RTD em scripts/infra =="
  git log --all --name-status -- scripts infra | grep -Ei "commit |rtd|quote|market" | head -500
  echo

  echo "== Conteudo atual dos scripts RTD existentes =="
  for f in \
    scripts/run_rtd_option_quotes_pipeline.py \
    scripts/import_rtd_links_to_option_quotes.py \
    scripts/import_rtd_option_quotes_wide_csv.py \
    scripts/build_rtd_symbols.py \
    scripts/run_rtd_refresh_full.py \
    scripts/audit_rtd_option_quotes.py \
    infra/bootstrap_rtd_option_quotes_schema.py
  do
    if [ -f "$f" ]; then
      echo "============================================================"
      echo "ARQUIVO ATUAL: $f"
      echo "============================================================"
      sed -n '1,260p' "$f"
      echo
    else
      echo "ARQUIVO AUSENTE NO WORKTREE: $f"
    fi
  done
  echo

  echo "== Testes vigentes relacionados ao pipeline/import/audit RTD =="
  for f in \
    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
    ATT/tests/test_import_rtd_links_to_option_quotes.py \
    ATT/tests/test_audit_rtd_option_quotes.py \
    ATT/tests/test_rtd_option_quotes_repository_contract.py \
    ATT/tests/test_structure_leg_rtd_enrichment_service.py
  do
    if [ -f "$f" ]; then
      echo "============================================================"
      echo "TESTE: $f"
      echo "============================================================"
      sed -n '1,260p' "$f"
      echo
    else
      echo "TESTE AUSENTE: $f"
    fi
  done
  echo

  echo "== Schema e contagem rtd_option_quotes em app.db e derived.db =="
  python - <<'PY'
import sqlite3
from pathlib import Path

for db_name in ["dados/app.db", "dados/derived.db"]:
    db = Path(db_name)
    print("============================================================")
    print(f"DB: {db_name}")
    print(f"Existe: {db.exists()}")
    if not db.exists():
        continue

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row
    try:
        exists = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='rtd_option_quotes'"
        ).fetchone()
        print(f"rtd_option_quotes existe: {bool(exists)}")
        if not exists:
            continue

        count = con.execute("SELECT COUNT(*) AS c FROM rtd_option_quotes").fetchone()["c"]
        print(f"linhas: {count}")

        print("colunas:")
        for col in con.execute("PRAGMA table_info(rtd_option_quotes)").fetchall():
            print(f"- {col[1]} {col[2]}")

        print("ultimas linhas:")
        rows = con.execute(
            """
            SELECT codigo_opcao, ativo_base, call_put, strike, ultimo_preco, bid, ask, source, updated_at, created_at
            FROM rtd_option_quotes
            ORDER BY updated_at DESC, id DESC
            LIMIT 10
            """
        ).fetchall()
        for row in rows:
            print(dict(row))
    except Exception as e:
        print("ERRO:", repr(e))
    finally:
        con.close()
PY
  echo

  echo "== Arquivos de dados RTD atuais =="
  ls -la dados | grep -Ei "rtd|quote|lista" || true
  echo

  echo "== Primeiras linhas dados/RTD_LINKS.csv se existir =="
  if [ -f dados/RTD_LINKS.csv ]; then
    python - <<'PY'
from pathlib import Path
p = Path("dados/RTD_LINKS.csv")
print(f"Arquivo: {p}")
print(f"Tamanho: {p.stat().st_size} bytes")
with p.open("r", encoding="utf-8-sig", errors="replace") as f:
    for i, line in zip(range(20), f):
        print(line.rstrip())
PY
  else
    echo "dados/RTD_LINKS.csv ausente"
  fi
  echo

  echo "== Busca por PowerShell/Excel/COM/RTD nos arquivos atuais =="
  grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ --exclude='*.pyc' \
    -E "Excel.Application|Workbooks|RefreshAll|RTD|LISTA_RTD|RTD_LINKS|win32com|powershell|Start-Process" \
    scripts infra services repositories db UI ATT/tests 2>/dev/null | head -500
  echo

  echo "============================================================"
  echo "FIM DIAGNOSTICO FASE 5B"
  echo "============================================================"
} > "$OUT" 2>&1

echo "Diagnostico Fase 5B gerado em: $OUT"
