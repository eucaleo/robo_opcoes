#!/usr/bin/env bash
set -e

echo "===== GUARDRAIL: referencias a derived.db ====="

grep -RInE \
  "derived\.db|DERIVED_DB|derived_db|run_derived|validate_derived|repair_derived|purge_derived" \
  . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=venv \
  --exclude-dir=__pycache__ \
  --exclude-dir=.pytest_cache \
  --exclude-dir=dados \
  --exclude-dir=FRENTE_BD_UNICO_APPDB \
  --exclude="*.pyc" \
  --exclude="*.db" \
  --exclude="*.sqlite" \
  --exclude="*.png" \
  --exclude="*.jpg" \
  --exclude="*.jpeg" \
  --exclude="*.gif" \
  && {
    echo
    echo "ERRO: ainda existem referencias operacionais a derived.db."
    exit 1
  } || {
    echo "OK: nenhuma referencia operacional a derived.db encontrada no escopo analisado."
  }
