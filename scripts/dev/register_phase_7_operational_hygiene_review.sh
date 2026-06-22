#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Revisao de higiene operacional"

echo "[INFO] Registrando revisao de higiene operacional da Fase 7 em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Revisao de higiene operacional ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"
TRACKED_COUNT="$(git ls-files | wc -l | tr -d ' ')"

HYGIENE_CANDIDATES="$(
  git ls-files | grep -E '(^|/)(__pycache__|\.pytest_cache)(/|$)|\.(pyc|pyo|log|tmp|bak|db|sqlite|sqlite3)$|^backups/|^_resgate_db/|^_usage_audit/' || true
)"

ROOT_DATA_FILES="$(
  git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls|csv|db|sqlite|sqlite3)$' || true
)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Revisao documental de higiene operacional."
  echo "- Nenhum arquivo funcional foi alterado ou removido nesta etapa."
  echo "- A revisao serve para orientar a preparacao de entrega controlada."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da revisao: ${HEAD_LINE}"
  echo "- Arquivos versionados no momento da revisao: ${TRACKED_COUNT}"
  echo ""
  echo "### Possiveis candidatos a limpeza ou verificacao"
  echo ""
  if [[ -z "${HYGIENE_CANDIDATES}" ]]; then
    echo "- Nenhum candidato evidente encontrado nos padroes avaliados"
  else
    while IFS= read -r line; do
      echo "- ${line}"
    done <<< "${HYGIENE_CANDIDATES}"
  fi
  echo ""
  echo "### Arquivos de dados ou binarios na raiz"
  echo ""
  if [[ -z "${ROOT_DATA_FILES}" ]]; then
    echo "- Nenhum arquivo de dados ou binario identificado na raiz pelos padroes avaliados"
  else
    while IFS= read -r line; do
      echo "- ${line}"
    done <<< "${ROOT_DATA_FILES}"
  fi
  echo ""
  echo "### Observacoes"
  echo ""
  echo "- Itens listados como candidatos nao devem ser removidos automaticamente."
  echo "- Cada item deve ser avaliado quanto a necessidade operacional, historico e impacto na entrega."
  echo "- Caso algum item seja essencial ao projeto, ele deve permanecer versionado e documentado."
  echo "- Caso algum item seja artefato local, deve ser tratado em etapa propria com commit separado."
  echo ""
  echo "### Conclusao da revisao"
  echo ""
  echo "- A revisao de higiene operacional foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue pronta para avaliacao controlada de limpeza, documentacao e empacotamento."
} >> "${CHECKPOINT}"

echo "[OK] Revisao de higiene operacional registrada."
