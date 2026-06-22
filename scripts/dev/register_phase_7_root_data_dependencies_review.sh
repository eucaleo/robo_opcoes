#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Revisao de dependencias dos arquivos de dados da raiz"

echo "[INFO] Registrando revisao de dependencias dos arquivos de dados da raiz em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Revisao de dependencias dos arquivos de dados da raiz ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

REFERENCE_LIST="$(
  {
    git grep -n -I -E 'LISTA_RTD|OPERACOES_E_OPCOES|xlsx|xlsm|xls' -- . \
      ':!docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md' \
      ':!scripts/dev/register_phase_7_root_data_dependencies_review.sh' \
      2>/dev/null || true
  }
)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Revisao documental de referencias a arquivos de dados ou planilhas."
  echo "- Nenhum arquivo foi alterado, removido ou movido nesta etapa."
  echo "- O objetivo e identificar possiveis dependencias antes de qualquer decisao de limpeza ou empacotamento."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da revisao: ${HEAD_LINE}"
  echo ""
  echo "### Arquivos de dados previamente classificados"
  echo ""
  echo "- LISTA_RTD.xlsx"
  echo "- OPERACOES_E_OPCOES.xlsm"
  echo ""
  echo "### Referencias encontradas no repositorio"
  echo ""
  if [[ -z "${REFERENCE_LIST}" ]]; then
    echo "- Nenhuma referencia textual encontrada pelos padroes avaliados."
  else
    while IFS= read -r line; do
      echo "- ${line}"
    done <<< "${REFERENCE_LIST}"
  fi
  echo ""
  echo "### Interpretacao operacional"
  echo ""
  echo "- Referencias textuais indicam possivel dependencia operacional, documental ou historica."
  echo "- Ausencia de referencia textual nao garante ausencia de dependencia, pois planilhas podem ser usadas manualmente ou por configuracao externa."
  echo "- Arquivos xlsx e xlsm devem ser avaliados com cuidado especial antes de remocao, movimentacao ou substituicao."
  echo "- Arquivos com macro devem ser tratados como artefatos operacionais sensiveis para entrega."
  echo ""
  echo "### Conclusao da revisao"
  echo ""
  echo "- A revisao de dependencias dos arquivos de dados da raiz foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue preparada para decisao explicita sobre manutencao, documentacao ou tratamento desses artefatos."
} >> "${CHECKPOINT}"

echo "[OK] Revisao de dependencias dos arquivos de dados da raiz registrada."
