#!/usr/bin/env bash

set -euo pipefail

# Limpeza segura do repositório
# Por padrão roda em DRY-RUN.
#
# Uso:
#   ./limpar_repositorio_seguro.sh --dry-run
#   ./limpar_repositorio_seguro.sh --apply
#   ./limpar_repositorio_seguro.sh --apply --remove-xlsx-duplicado
#   ./limpar_repositorio_seguro.sh --apply --remove-trash
#
# Não remove bancos, CSVs, XLSM, dados, scripts nem reports.
# Remove somente caches/temporários por padrão.

MODE="dry-run"
REMOVE_XLSX_DUPLICADO="false"
REMOVE_TRASH="false"

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      MODE="dry-run"
      ;;
    --apply)
      MODE="apply"
      ;;
    --remove-xlsx-duplicado)
      REMOVE_XLSX_DUPLICADO="true"
      ;;
    --remove-trash)
      REMOVE_TRASH="true"
      ;;
    -h|--help)
      sed -n '1,35p' "$0"
      exit 0
      ;;
    *)
      echo "Argumento desconhecido: $arg"
      exit 1
      ;;
  esac
done

ROOT="$(pwd)"
TS="$(date +"%Y-%m-%d_%H-%M-%S")"
REPORT_DIR="_cleanup_reports/cleanup_${TS}"
mkdir -p "$REPORT_DIR"

REPORT_FILE="$REPORT_DIR/limpeza_report.txt"
TARGETS_FILE="$REPORT_DIR/alvos_limpeza.txt"

echo "======================================"
echo " Limpeza segura do repositório"
echo " Diretório: $ROOT"
echo " Modo: $MODE"
echo " Relatório: $REPORT_DIR"
echo "======================================"
echo ""

{
  echo "Limpeza segura do repositório"
  echo "Data: $(date)"
  echo "Diretório: $ROOT"
  echo "Modo: $MODE"
  echo ""
  echo "Git status antes:"
  git status --short || true
  echo ""
} > "$REPORT_FILE"

echo "Mapeando alvos seguros..."

# Diretórios de cache
find . \
  -path "./.git" -prune -o \
  -path "./_cleanup_reports" -prune -o \
  -type d \( -name "__pycache__" -o -name ".pytest_cache" \) \
  -print > "$TARGETS_FILE"

# Arquivos temporários/compilados
find . \
  -path "./.git" -prune -o \
  -path "./_cleanup_reports" -prune -o \
  -type f \( \
    -name "*.pyc" -o \
    -name "*.pyo" -o \
    -name "*.swp" -o \
    -name "*.swo" -o \
    -name ".DS_Store" -o \
    -name "Thumbs.db" -o \
    -name "*~" \
  \) \
  -print >> "$TARGETS_FILE"

# Opcional: remover XLSX duplicado, mantendo XLSM
if [ "$REMOVE_XLSX_DUPLICADO" = "true" ]; then
  if [ -e "./OPERACOES_E_OPCOES.xlsx" ]; then
    echo "./OPERACOES_E_OPCOES.xlsx" >> "$TARGETS_FILE"
  fi
fi

# Opcional: remover .trash se ainda existir dentro do projeto
if [ "$REMOVE_TRASH" = "true" ]; then
  if [ -d "./.trash" ]; then
    echo "./.trash" >> "$TARGETS_FILE"
  fi
fi

# Remover duplicidades na lista
sort -u "$TARGETS_FILE" -o "$TARGETS_FILE"

COUNT="$(wc -l < "$TARGETS_FILE" | tr -d ' ')"

echo "Alvos encontrados: $COUNT"
echo ""

{
  echo "Alvos encontrados: $COUNT"
  echo ""
  cat "$TARGETS_FILE"
  echo ""
} >> "$REPORT_FILE"

if [ "$COUNT" = "0" ]; then
  echo "Nenhum alvo de limpeza encontrado."
  echo "Nenhum alvo de limpeza encontrado." >> "$REPORT_FILE"
  exit 0
fi

if [ "$MODE" = "dry-run" ]; then
  echo "DRY-RUN: nada foi removido."
  echo ""
  echo "Veja a lista em:"
  echo "  $TARGETS_FILE"
  echo ""
  echo "Para aplicar:"
  echo "  ./limpar_repositorio_seguro.sh --apply"
  echo ""
  echo "Para aplicar e remover também OPERACOES_E_OPCOES.xlsx:"
  echo "  ./limpar_repositorio_seguro.sh --apply --remove-xlsx-duplicado"
  echo ""
  echo "DRY-RUN: nada foi removido." >> "$REPORT_FILE"
  exit 0
fi

echo "Aplicando limpeza..."

# Remove item por item com segurança
while IFS= read -r target; do
  [ -z "$target" ] && continue

  if [ -e "$target" ]; then
    echo "Removendo: $target"
    rm -rf -- "$target"
  fi
done < "$TARGETS_FILE"

echo ""
echo "Limpeza aplicada."

{
  echo ""
  echo "Limpeza aplicada em: $(date)"
  echo ""
  echo "Git status depois:"
  git status --short || true
} >> "$REPORT_FILE"

echo ""
echo "Relatório salvo em:"
echo "  $REPORT_FILE"
echo ""
echo "Status Git atual:"
git status --short || true

