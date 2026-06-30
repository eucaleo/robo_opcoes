#!/usr/bin/env bash
set -u

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" || exit 1

echo "Gerando mapa compacto de alvos RTD - Fase 0.2"

if command -v python >/dev/null 2>&1; then
    python scripts/rtd_mapa_alvos_fase0.py
elif command -v python3 >/dev/null 2>&1; then
    python3 scripts/rtd_mapa_alvos_fase0.py
elif command -v py >/dev/null 2>&1; then
    py -3 scripts/rtd_mapa_alvos_fase0.py
else
    echo "Python nao encontrado no PATH."
    exit 1
fi

echo "Mapa compacto concluido."
