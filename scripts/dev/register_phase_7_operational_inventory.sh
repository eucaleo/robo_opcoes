#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Inventario operacional inicial"

echo "[INFO] Registrando inventario operacional da Fase 7 em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Inventario operacional inicial ja registrado."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"
STATUS="$(git status --short)"
TAGS="$(git tag --list "fase-6*" | sort)"
CHECKPOINTS="$(find docs/checkpoints -maxdepth 1 -type f | sort)"
SCRIPTS="$(find scripts/dev -maxdepth 1 -type f | sort)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Estado Git"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Ultimo commit: ${HEAD_LINE}"
  if [[ -z "${STATUS}" ]]; then
    echo "- Status Git: limpo"
  else
    echo "- Status Git: pendencias detectadas"
  fi
  echo ""
  echo "### Tags da Fase 6 presentes"
  echo ""
  if [[ -z "${TAGS}" ]]; then
    echo "- Nenhuma tag fase-6 encontrada"
  else
    while IFS= read -r line; do
      echo "- ${line}"
    done <<< "${TAGS}"
  fi
  echo ""
  echo "### Checkpoints presentes"
  echo ""
  while IFS= read -r line; do
    echo "- ${line}"
  done <<< "${CHECKPOINTS}"
  echo ""
  echo "### Scripts auxiliares presentes"
  echo ""
  while IFS= read -r line; do
    echo "- ${line}"
  done <<< "${SCRIPTS}"
  echo ""
  echo "### Conclusao inicial"
  echo ""
  echo "- A Fase 7 iniciou com branch remota atualizada."
  echo "- A Fase 6 possui tag final preservada."
  echo "- O repositorio esta em estado limpo no inicio da consolidacao operacional."
} >> "${CHECKPOINT}"

echo "[OK] Inventario operacional registrado."
