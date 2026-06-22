#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Checklist consolidado de preparacao para entrega da Fase 7"

echo "[INFO] Registrando checklist consolidado de preparacao para entrega em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Checklist consolidado de preparacao para entrega ja registrado."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

TOTAL_TRACKED="$(git ls-files | wc -l | tr -d ' ')"
DOCS_TRACKED="$(git ls-files docs 2>/dev/null | wc -l | tr -d ' ')"
SCRIPTS_TRACKED="$(git ls-files scripts 2>/dev/null | wc -l | tr -d ' ')"
ROOT_EXCEL_TRACKED="$(git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls)$' || true)"
ROOT_DATA_TRACKED="$(git ls-files | grep -Ei '^[^/]+\.(csv|json|db|sqlite|sqlite3|xlsx|xlsm|xls)$' || true)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Consolidacao documental do estado de preparacao da Fase 7 para entrega."
  echo "- Nenhum pacote foi gerado nesta etapa."
  echo "- Nenhum arquivo operacional foi alterado, removido, criado, renomeado ou movido nesta etapa."
  echo "- O checklist consolida as revisoes ja registradas sobre higiene, dependencias, workbooks, sensibilidade e matriz de pacote."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base do checklist: ${HEAD_LINE}"
  echo "- Total de arquivos versionados no momento da revisao: ${TOTAL_TRACKED}"
  echo "- Arquivos versionados em docs: ${DOCS_TRACKED}"
  echo "- Arquivos versionados em scripts: ${SCRIPTS_TRACKED}"
  echo ""
  echo "### Revisoes documentais consolidadas"
  echo ""
  echo "- Higiene operacional da Fase 7: registrada."
  echo "- Classificacao dos arquivos de dados da raiz: registrada."
  echo "- Revisao de dependencias dos arquivos de dados da raiz: registrada."
  echo "- Normalizacao de referencias da revisao de dependencias: registrada."
  echo "- Revisao de aderencia entre workbooks referenciados e versionados: registrada."
  echo "- Diretriz provisoria de empacotamento dos artefatos Excel: registrada."
  echo "- Revisao de sensibilidade dos artefatos Excel versionados: registrada."
  echo "- Matriz provisoria do pacote de entrega: registrada."
  echo ""
  echo "### Arquivos de dados versionados na raiz observados"
  echo ""
  if [[ -z "${ROOT_DATA_TRACKED}" ]]; then
    echo "- Nenhum arquivo de dados versionado na raiz foi identificado pelos padroes avaliados."
  else
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        echo "- ${file}"
      fi
    done <<< "${ROOT_DATA_TRACKED}"
  fi
  echo ""
  echo "### Workbooks Excel versionados na raiz observados"
  echo ""
  if [[ -z "${ROOT_EXCEL_TRACKED}" ]]; then
    echo "- Nenhum workbook Excel versionado na raiz foi identificado."
  else
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        echo "- ${file}"
      fi
    done <<< "${ROOT_EXCEL_TRACKED}"
  fi
  echo ""
  echo "### Checklist de prontidao documental"
  echo ""
  echo "- Estrutura documental da Fase 7 atualizada: sim."
  echo "- Evidencia de arquivos sensiveis ou condicionais registrada: sim."
  echo "- Decisao automatica de remocao de artefatos evitada: sim."
  echo "- Decisao automatica de inclusao de workbooks ausentes evitada: sim."
  echo "- Regras provisorias para entrega externa registradas: sim."
  echo "- Necessidade de revisao manual de Excel real registrada: sim."
  echo "- Necessidade de revisao especifica para macro registrada: sim."
  echo "- Pre-requisitos externos candidatos registrados: sim."
  echo "- Pacote final gerado nesta etapa: nao."
  echo "- Alteracao funcional realizada nesta etapa: nao."
  echo ""
  echo "### Pendencias que exigem decisao explicita"
  echo ""
  echo "- Decidir se LISTA_RTD.xlsx permanece no repositorio, entra no pacote interno ou deve ser substituido por fixture."
  echo "- Decidir se OPERACOES_E_OPCOES.xlsm permanece no repositorio, entra no pacote interno ou deve ser excluido de entrega externa."
  echo "- Decidir se LISTA_RTD.xlsm e pre-requisito externo, dependencia historica ou referencia obsoleta."
  echo "- Decidir se OPERACOES_E_OPCOES.xlsx e dependencia local, referencia legada ou artefato a remover das referencias futuras."
  echo "- Definir se a entrega final sera interna, tecnica, auditavel ou externa."
  echo "- Definir se havera pacote reproduzivel com dados sinteticos, seeds ou fixtures anonimizadas."
  echo ""
  echo "### Regras de bloqueio para pacote externo"
  echo ""
  echo "- Bloquear inclusao de planilhas reais sem revisao de conteudo e aprovacao explicita."
  echo "- Bloquear inclusao de arquivos com macro sem revisao especifica de seguranca."
  echo "- Bloquear inclusao de arquivos de ambiente com segredos."
  echo "- Bloquear inclusao de logs, temporarios, caches e backups."
  echo "- Bloquear dependencia silenciosa de arquivos ausentes."
  echo ""
  echo "### Criterio provisorio de encerramento documental da Fase 7"
  echo ""
  echo "- A Fase 7 pode ser considerada documentalmente consolidada quando este checklist estiver versionado e enviado ao remoto."
  echo "- A geracao de pacote final deve permanecer condicionada as decisoes explicitas listadas acima."
  echo "- A consolidacao documental nao equivale a aprovacao automatica de distribuicao externa."
  echo ""
  echo "### Conclusao do checklist"
  echo ""
  echo "- O checklist consolidado de preparacao para entrega da Fase 7 foi registrado sem alteracao funcional."
  echo "- A Fase 7 segue pronta para decisao final de encerramento documental ou abertura de etapa especifica de empacotamento."
} >> "${CHECKPOINT}"

python - <<'PY'
from pathlib import Path

path = Path("docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md")
text = path.read_text(encoding="utf-8")
text = text.replace(chr(96), "'")
path.write_text(text, encoding="utf-8", newline="\n")
PY

echo "[OK] Checklist consolidado de preparacao para entrega registrado."
