#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

echo "## Logging existente (logger / logging / print) em payoff + derived"
( cd "$ROOT" && {
  rg -n "logger\.|logging\.|print\(" -S domain/payoff.py services/derived_service.py || true
  echo
})

echo "## Onde a fonte (manual vs rtd) poderia ser registrada"
( cd "$ROOT" && {
  rg -n "manual_analise_robo_legs|rtd_analise_robo_legs|source_table|fallback|prefer" -S domain/payoff.py services/derived_service.py || true
  echo
})

echo "## Padrão de config de logging no projeto"
( cd "$ROOT" && {
  rg -n "basicConfig\(|getLogger\(|logging\.config|dictConfig" -S . || true
  echo
})
