#!/usr/bin/env bash
set -u

OUT="docs/checkpoints/evidencias/fase-5e-diagnostico-integracao-rtd-derived.txt"

{
  echo "============================================================"
  echo "FASE 5E - DIAGNOSTICO INTEGRACAO RTD NO DERIVED PIPELINE"
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

  echo "== scripts/run_derived_pipeline.py =="
  if [ -f scripts/run_derived_pipeline.py ]; then
    sed -n '1,260p' scripts/run_derived_pipeline.py
  else
    echo "ERRO: scripts/run_derived_pipeline.py nao encontrado"
  fi
  echo

  echo "== Ocorrencias de rtd_quotes_updated =="
  grep -R "rtd_quotes_updated" -n . \
    --exclude-dir=.git \
    --exclude-dir=.pytest_cache \
    --exclude-dir=__pycache__ \
    --exclude="*.db" \
    --exclude="*.sqlite" \
    --exclude="*.pyc" || true
  echo

  echo "== Ocorrencias de run_derived_pipeline =="
  grep -R "run_derived_pipeline" -n . \
    --exclude-dir=.git \
    --exclude-dir=.pytest_cache \
    --exclude-dir=__pycache__ \
    --exclude="*.db" \
    --exclude="*.sqlite" \
    --exclude="*.pyc" || true
  echo

  echo "== Ocorrencias de RTD na UI/controladores =="
  grep -R "RTD\\|rtd\\|Atualizar Dados\\|Executar Pipeline" -n \
    app ATT infra scripts \
    --exclude-dir=.git \
    --exclude-dir=.pytest_cache \
    --exclude-dir=__pycache__ \
    --exclude="*.db" \
    --exclude="*.sqlite" \
    --exclude="*.pyc" || true
  echo

  echo "== Testes relacionados a derived pipeline/orquestracao =="
  find ATT/tests -type f | grep -Ei "derived|pipeline|orchestrator|refresh|rtd" | sort
  echo

  echo "============================================================"
  echo "FIM FASE 5E DIAGNOSTICO"
  echo "============================================================"
} > "$OUT" 2>&1

echo "Diagnostico Fase 5E registrado em: $OUT"
