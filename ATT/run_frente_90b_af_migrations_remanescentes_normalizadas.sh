#!/usr/bin/env bash
# Compatibilidade 90B-AF:
# O checkpoint 90B-AK preserva este nome histórico como artefato da cadeia.
# A execução efetiva continua centralizada no runner canônico.
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CANONICAL="$ROOT/ATT/run_frente_90b_af_normalizacao_migrations_restantes.sh"

if [[ ! -f "$CANONICAL" ]]; then
  printf 'ERRO: runner canonico ausente: %s\n' "$CANONICAL" >&2
  exit 1
fi

printf 'RUNNER_COMPAT_90B_AF=%s\n' "$BASH_SOURCE"
printf 'RUNNER_CANONICAL_90B_AF=%s\n' "$CANONICAL"

if bash "$CANONICAL" "$@"; then
  printf 'RUNNER_COMPAT_90B_AF_STATUS=OK\n'
  exit 0
else
  rc=$?
  printf 'RUNNER_COMPAT_90B_AF_STATUS=FAIL exit_code=%s\n' "$rc" >&2
  exit "$rc"
fi
