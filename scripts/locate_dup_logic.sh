#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"

echo "## Locais com lógica de fallback de tabela (manual vs rtd vs snapshot)"
( cd "$ROOT" && {
  rg -n "for\s+table\s+in\s+\(|manual_analise_robo_legs.*rtd_analise_robo_legs|rtd_analise_robo_legs.*manual_analise_robo_legs" -S services domain || true
  echo
})

echo "## Locais que calculam timestamp 'mais recente'"
( cd "$ROOT" && {
  rg -n "MAX\(timestamp\)|ORDER\s+BY\s+timestamp|latest.*timestamp|get_.*timestamp" -S services domain || true
  echo
})

echo "## Sugestão de candidatos para virar helper"
( cd "$ROOT" && {
  rg -n "def\s+.*(source|resolve|choose).*table|def\s+.*timestamp" -S domain services db || true
  echo
})
