#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Baseline tecnica operacional"

echo "[INFO] Registrando baseline tecnica operacional da Fase 7 em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Baseline tecnica operacional ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"
TRACKED_COUNT="$(git ls-files | wc -l | tr -d ' ')"
STATUS="$(git status --short)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Estado do repositorio"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit atual: ${HEAD_LINE}"
  echo "- Arquivos versionados: ${TRACKED_COUNT}"
  if [[ -z "${STATUS}" ]]; then
    echo "- Status Git antes do registro: limpo"
  else
    echo "- Status Git antes do registro: com alteracoes locais"
  fi
  echo ""
  echo "### Estrutura principal identificada"
  echo ""
  find . -maxdepth 1 -mindepth 1 \
    ! -name ".git" \
    ! -name ".venv" \
    ! -name "node_modules" \
    -printf "- %f\n" | sort
  echo ""
  echo "### Arquivos de manifesto e configuracao encontrados"
  echo ""
  FOUND_MANIFESTS="$(
    find . -maxdepth 3 -type f \( \
      -name "package.json" -o \
      -name "package-lock.json" -o \
      -name "pnpm-lock.yaml" -o \
      -name "yarn.lock" -o \
      -name "requirements.txt" -o \
      -name "pyproject.toml" -o \
      -name "poetry.lock" -o \
      -name "Pipfile" -o \
      -name "Pipfile.lock" -o \
      -name "Dockerfile" -o \
      -name "docker-compose.yml" -o \
      -name "docker-compose.yaml" -o \
      -name "Makefile" \
    \) \
    ! -path "./.git/*" \
    ! -path "./node_modules/*" \
    ! -path "./.venv/*" \
    | sed "s#^\./##" \
    | sort
  )"
  if [[ -z "${FOUND_MANIFESTS}" ]]; then
    echo "- Nenhum manifesto conhecido encontrado ate profundidade 3"
  else
    while IFS= read -r line; do
      echo "- ${line}"
    done <<< "${FOUND_MANIFESTS}"
  fi
  echo ""
  echo "### Scripts de desenvolvimento versionados"
  echo ""
  find scripts/dev -maxdepth 1 -type f | sort | while IFS= read -r line; do
    echo "- ${line}"
  done
  echo ""
  echo "### Conclusao da baseline"
  echo ""
  echo "- A baseline tecnica foi registrada sem alteracao funcional."
  echo "- O objetivo desta etapa e preparar a revisao operacional e a entrega controlada."
} >> "${CHECKPOINT}"

echo "[OK] Baseline tecnica operacional registrada."
