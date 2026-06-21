#!/usr/bin/env bash
set -euo pipefail

echo "== Branch =="
git branch --show-current

echo
echo "== Status curto =="
git status --short

echo
echo "== Últimos commits =="
git log --oneline -8

echo
echo "== Arquivos de evidência recentes =="
find docs/checkpoints/evidencias -maxdepth 1 -type f | sort | tail -20
