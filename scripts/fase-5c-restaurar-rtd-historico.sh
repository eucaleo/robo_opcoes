#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-5c-restauracao-rtd-historico.txt"
SRC_COMMIT="8a56969"

FILES=(
  "infra/bootstrap_rtd_option_quotes_schema.py"
  "scripts/audit_rtd_option_quotes.py"
  "scripts/build_rtd_symbols.py"
  "scripts/create_rtd_option_quotes_sheet.py"
  "scripts/import_lista_rtd_excel_to_option_quotes.py"
  "scripts/import_rtd_links_to_option_quotes.py"
  "scripts/import_rtd_option_quotes_wide_csv.py"
  "scripts/mapear_automacao_opcoes_rtd.py"
  "scripts/refresh_rtd_option_quotes_excel.ps1"
  "scripts/run_lista_rtd_option_quotes_pipeline.py"
  "scripts/run_rtd_option_quotes_pipeline.py"
  "scripts/run_rtd_refresh_full.py"
  "scripts/seed_current_rtd_option_quotes.py"
  "ATT/tests/test_audit_rtd_option_quotes.py"
  "ATT/tests/test_import_rtd_links_to_option_quotes.py"
  "ATT/tests/test_run_rtd_option_quotes_pipeline.py"
  "ATT/tests/test_rtd_option_quotes_repository_contract.py"
)

{
  echo "============================================================"
  echo "FASE 5C - RESTAURACAO RTD HISTORICO"
  echo "Data:"
  date
  echo "Branch:"
  git branch --show-current
  echo "Commit atual:"
  git rev-parse --short HEAD
  echo "Commit fonte:"
  echo "$SRC_COMMIT"
  echo "============================================================"
  echo

  echo "== Status git antes =="
  git status --short
  echo

  echo "== Restaurando arquivos existentes no commit fonte =="
  for f in "${FILES[@]}"; do
    if git cat-file -e "${SRC_COMMIT}:${f}" 2>/dev/null; then
      echo "[RESTORE] $f"
      git checkout "$SRC_COMMIT" -- "$f"
    else
      echo "[SKIP AUSENTE NO COMMIT] $f"
    fi
  done
  echo

  echo "== Status git depois da restauracao =="
  git status --short
  echo

  echo "== Arquivos RTD restaurados =="
  for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
      echo "[OK] $f"
    fi
  done
  echo

  echo "== Cabecalhos dos scripts restaurados =="
  for f in \
    infra/bootstrap_rtd_option_quotes_schema.py \
    scripts/audit_rtd_option_quotes.py \
    scripts/build_rtd_symbols.py \
    scripts/import_rtd_option_quotes_wide_csv.py \
    scripts/run_rtd_option_quotes_pipeline.py \
    scripts/run_rtd_refresh_full.py
  do
    if [ -f "$f" ]; then
      echo "============================================================"
      echo "ARQUIVO: $f"
      echo "============================================================"
      sed -n '1,220p' "$f"
      echo
    fi
  done

  echo "== PowerShell RTD restaurado se existir =="
  if [ -f scripts/refresh_rtd_option_quotes_excel.ps1 ]; then
    sed -n '1,220p' scripts/refresh_rtd_option_quotes_excel.ps1
  else
    echo "PowerShell nao restaurado"
  fi
  echo

  echo "== Py compile dos arquivos Python RTD restaurados =="
  PY_FILES=()
  for f in "${FILES[@]}"; do
    case "$f" in
      *.py)
        if [ -f "$f" ]; then
          PY_FILES+=("$f")
        fi
        ;;
    esac
  done

  if [ "${#PY_FILES[@]}" -gt 0 ]; then
    python -m py_compile "${PY_FILES[@]}"
    echo "[OK] py_compile"
  else
    echo "Nenhum arquivo Python RTD restaurado para compilar"
  fi
  echo

  echo "== Testes RTD restaurados disponíveis =="
  for f in \
    ATT/tests/test_audit_rtd_option_quotes.py \
    ATT/tests/test_import_rtd_links_to_option_quotes.py \
    ATT/tests/test_run_rtd_option_quotes_pipeline.py \
    ATT/tests/test_rtd_option_quotes_repository_contract.py
  do
    if [ -f "$f" ]; then
      echo "[TESTE] $f"
    fi
  done
  echo

  echo "============================================================"
  echo "FIM FASE 5C RESTAURACAO"
  echo "============================================================"
} > "$OUT" 2>&1

echo "Restauracao Fase 5C registrada em: $OUT"
