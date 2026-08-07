#!/usr/bin/env bash
set -euo pipefail

echo "[stage_etapa_1] Staging de encerramento da etapa 1, excluindo ATT e backups locais..."

git add -A -- .   ':!ATT'   ':!ATT/**'   ':!*.bak'   ':!*.bak_*'   ':!**/*.bak'   ':!**/*.bak_*'   ':!docs/FRENTES_CORRIGIDAS_old.md'   ':!docs/FRENTES_CORRIGIDAS_PARTE_2 .md'

echo "[stage_etapa_1] Verificando se ATT entrou no stage..."
if git diff --cached --name-only | grep -E '^ATT(/|$)' >/dev/null; then
  echo "[stage_etapa_1][ERRO] Existem arquivos ATT staged. Abortando."
  git diff --cached --name-only | grep -E '^ATT(/|$)' || true
  exit 1
fi

echo "[stage_etapa_1] Verificando backups locais staged..."
if git diff --cached --name-only | grep -E '(\.bak$|\.bak_|bak_)' >/dev/null; then
  echo "[stage_etapa_1][ERRO] Existem backups staged. Revise antes de commit."
  git diff --cached --name-only | grep -E '(\.bak$|\.bak_|bak_)' || true
  exit 1
fi

echo "[stage_etapa_1] Verificando arquivo docs/FRENTES_CORRIGIDAS_PARTE_2 com espaço no nome..."
if git diff --cached --name-only | grep -F 'docs/FRENTES_CORRIGIDAS_PARTE_2 .md' >/dev/null; then
  echo "[stage_etapa_1][ERRO] Arquivo com espaço no nome entrou no stage."
  exit 1
fi

echo "[stage_etapa_1] Arquivos staged:"
git diff --cached --name-status

echo "[stage_etapa_1] OK. Revise o diff antes de commitar:"
echo "  git diff --cached --stat"
echo "  git diff --cached --name-status"
