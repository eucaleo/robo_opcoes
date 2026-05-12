#!/usr/bin/env bash
set -euo pipefail

PATCH_DIR="ATT/paches/PATCH-01-auditoria-inicial"
OUT_DIR="${PATCH_DIR}/output"

mkdir -p "$OUT_DIR"

echo "[INFO] Iniciando auditoria..."
echo "[INFO] Saída em: $OUT_DIR"

find . \
  -path "./.git" -prune -o \
  -path "./node_modules" -prune -o \
  -path "./vendor" -prune -o \
  -path "./dist" -prune -o \
  -path "./build" -prune -o \
  -path "./coverage" -prune -o \
  -path "./.next" -prune -o \
  -path "./out" -prune -o \
  -path "./tmp" -prune -o \
  -path "./temp" -prune -o \
  -print > "${OUT_DIR}/files.txt"

find . \
  -path "./.git" -prune -o \
  -path "./node_modules" -prune -o \
  -path "./vendor" -prune -o \
  -path "./dist" -prune -o \
  -path "./build" -prune -o \
  -path "./coverage" -prune -o \
  -path "./.next" -prune -o \
  -path "./out" -prune -o \
  -path "./tmp" -prune -o \
  -path "./temp" -prune -o \
  -type d -print > "${OUT_DIR}/tree.txt"

find . -type f \( \
  -iname "*.env" -o \
  -iname ".env*" -o \
  -iname "*.json" -o \
  -iname "*.yml" -o \
  -iname "*.yaml" -o \
  -iname "*.ini" -o \
  -iname "*.conf" -o \
  -iname "*.config" -o \
  -iname "Dockerfile" -o \
  -iname "docker-compose*" -o \
  -iname "package.json" -o \
  -iname "requirements.txt" -o \
  -iname "pyproject.toml" -o \
  -iname "pom.xml" -o \
  -iname "build.gradle" -o \
  -iname "composer.json" \
\) > "${OUT_DIR}/configs.txt"

find . -type f \( \
  -iname "*.sh" -o \
  -iname "*.bash" -o \
  -iname "*.ps1" -o \
  -iname "*.bat" -o \
  -iname "*.cmd" -o \
  -iname "Makefile" -o \
  -iname "package.json" \
\) > "${OUT_DIR}/scripts.txt"

{
  echo "### package.json"
  find . -type f -iname "package.json" -exec sh -c 'for f do echo "--- $f"; grep -nE "\"dependencies\"|\"devDependencies\"|\"scripts\"" "$f" || true; done' sh {} +
  echo
  echo "### requirements.txt"
  find . -type f -iname "requirements.txt" -exec sh -c 'for f do echo "--- $f"; cat "$f"; echo; done' sh {} +
  echo
  echo "### pyproject.toml"
  find . -type f -iname "pyproject.toml" -exec sh -c 'for f do echo "--- $f"; cat "$f"; echo; done' sh {} +
  echo
  echo "### composer.json"
  find . -type f -iname "composer.json" -exec sh -c 'for f do echo "--- $f"; grep -nE "\"require\"|\"require-dev\"" "$f" || true; done' sh {} +
} > "${OUT_DIR}/deps.txt"

grep -RInE "legacy|deprecated|todo|fixme|xxx|hack|obsolete" . \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude-dir=vendor \
  --exclude-dir=dist \
  --exclude-dir=build \
  --exclude-dir=coverage \
  --exclude-dir=.next \
  --exclude-dir=out \
  --exclude-dir=tmp \
  --exclude-dir=temp \
  > "${OUT_DIR}/legado.txt" || true

{
  echo "Resumo da auditoria"
  echo
  echo "Data: $(date)"
  echo "Diretório: $(pwd)"
  echo
  echo "Total de arquivos:"
  wc -l < "${OUT_DIR}/files.txt"
  echo
  echo "Total de diretórios:"
  wc -l < "${OUT_DIR}/tree.txt"
  echo
  echo "Total de configs localizadas:"
  wc -l < "${OUT_DIR}/configs.txt"
  echo
  echo "Total de scripts localizados:"
  wc -l < "${OUT_DIR}/scripts.txt"
  echo
  echo "Total de ocorrências de legado:"
  wc -l < "${OUT_DIR}/legado.txt"
} > "${OUT_DIR}/resumo.txt"

echo "[OK] Auditoria concluída."
echo "[OK] Arquivos gerados em: $OUT_DIR"
