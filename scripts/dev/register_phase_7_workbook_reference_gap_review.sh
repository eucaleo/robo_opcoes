#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Revisao de aderencia entre workbooks referenciados e versionados"

echo "[INFO] Registrando revisao de aderencia entre workbooks referenciados e versionados em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Revisao de aderencia entre workbooks referenciados e versionados ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

EXPECTED_FILES=(
  "LISTA_RTD.xlsx"
  "LISTA_RTD.xlsm"
  "OPERACOES_E_OPCOES.xlsm"
  "OPERACOES_E_OPCOES.xlsx"
)

ROOT_WORKBOOKS="$(
  git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls)$' || true
)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Revisao documental de aderencia entre workbooks citados e arquivos efetivamente presentes ou versionados."
  echo "- Nenhum arquivo foi alterado, removido, criado ou movido nesta etapa."
  echo "- O objetivo e identificar lacunas antes de decisao de empacotamento, limpeza ou entrega."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da revisao: ${HEAD_LINE}"
  echo ""
  echo "### Workbooks versionados na raiz"
  echo ""
  if [[ -z "${ROOT_WORKBOOKS}" ]]; then
    echo "- Nenhum workbook versionado encontrado na raiz."
  else
    while IFS= read -r file; do
      echo "- ${file}"
    done <<< "${ROOT_WORKBOOKS}"
  fi
  echo ""
  echo "### Matriz de presenca dos workbooks relevantes"
  echo ""
  for file in "${EXPECTED_FILES[@]}"; do
    if [[ -e "${file}" ]]; then
      EXISTS="sim"
    else
      EXISTS="nao"
    fi

    if git ls-files --error-unmatch "${file}" >/dev/null 2>&1; then
      TRACKED="sim"
      LAST_COMMIT="$(git log -1 --oneline -- "${file}" 2>/dev/null || echo sem historico identificado)"
    else
      TRACKED="nao"
      LAST_COMMIT="nao aplicavel"
    fi

    if git check-ignore -q "${file}" 2>/dev/null; then
      IGNORED="sim"
    else
      IGNORED="nao"
    fi

    REF_COUNT="$(git grep -n -I "${file}" -- . \
      ':!docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md' \
      ':!scripts/dev/register_phase_7_workbook_reference_gap_review.sh' \
      2>/dev/null | wc -l | tr -d ' ')"

    echo "- Arquivo: ${file}"
    echo "  - Existe no diretorio de trabalho: ${EXISTS}"
    echo "  - Versionado pelo Git: ${TRACKED}"
    echo "  - Ignorado pelo Git: ${IGNORED}"
    echo "  - Quantidade de referencias textuais: ${REF_COUNT}"
    echo "  - Ultimo commit relacionado: ${LAST_COMMIT}"
  done
  echo ""
  echo "### Pontos de atencao operacional"
  echo ""
  echo "- Referencias a workbooks ausentes ou nao versionados podem indicar dependencia historica, dependencia externa ou lacuna de empacotamento."
  echo "- Arquivos presentes e versionados, mas tambem ignorados, podem representar artefatos rastreados antes da regra de ignore."
  echo "- Divergencias entre extensoes xlsx e xlsm devem ser tratadas com cuidado, pois arquivos xlsm podem conter macros e fluxos operacionais manuais."
  echo "- Nenhuma decisao automatica de remocao, inclusao ou renomeacao deve ser tomada apenas por esta revisao."
  echo ""
  echo "### Conclusao da revisao"
  echo ""
  echo "- A aderencia entre workbooks referenciados e versionados foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue preparada para uma decisao explicita de empacotamento e tratamento de artefatos Excel."
} >> "${CHECKPOINT}"

python - <<'PY'
from pathlib import Path

paths = [
    Path("docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"),
]

for path in paths:
    text = path.read_text(encoding="utf-8")
    text = text.replace(chr(96), "'")
    path.write_text(text, encoding="utf-8", newline="\n")
PY

echo "[OK] Revisao de aderencia entre workbooks referenciados e versionados registrada."
