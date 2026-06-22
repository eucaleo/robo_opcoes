#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Matriz provisoria do pacote de entrega da Fase 7"

echo "[INFO] Registrando matriz provisoria do pacote de entrega em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Matriz provisoria do pacote de entrega ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

TOTAL_TRACKED="$(git ls-files | wc -l | tr -d ' ')"
DOCS_TRACKED="$(git ls-files docs 2>/dev/null | wc -l | tr -d ' ')"
SCRIPTS_TRACKED="$(git ls-files scripts 2>/dev/null | wc -l | tr -d ' ')"
PY_TRACKED="$(git ls-files | grep -Ei '\.py$' | wc -l | tr -d ' ')"
SH_TRACKED="$(git ls-files | grep -Ei '\.sh$' | wc -l | tr -d ' ')"
ROOT_EXCEL_TRACKED="$(git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls)$' || true)"
DB_TRACKED="$(git ls-files | grep -Ei '\.(db|sqlite|sqlite3)$' || true)"
ENV_TRACKED="$(git ls-files | grep -Ei '(^|/)\.env($|\.)|\.env$' || true)"
LOG_TRACKED="$(git ls-files | grep -Ei '\.(log|tmp|bak)$' || true)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Registro documental de matriz provisoria para montagem futura de pacote de entrega."
  echo "- Nenhum pacote foi gerado nesta etapa."
  echo "- Nenhum arquivo foi alterado, removido, criado, renomeado ou movido nesta etapa."
  echo "- A matriz consolida criterios de inclusao, exclusao, pre-requisito externo e decisao manual."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da matriz: ${HEAD_LINE}"
  echo ""
  echo "### Resumo quantitativo do repositorio versionado"
  echo ""
  echo "- Total de arquivos versionados: ${TOTAL_TRACKED}"
  echo "- Arquivos em docs: ${DOCS_TRACKED}"
  echo "- Arquivos em scripts: ${SCRIPTS_TRACKED}"
  echo "- Arquivos Python versionados: ${PY_TRACKED}"
  echo "- Arquivos shell versionados: ${SH_TRACKED}"
  echo ""
  echo "### Artefatos sensiveis ou condicionais detectados"
  echo ""
  echo "#### Workbooks Excel versionados na raiz"
  echo ""
  if [[ -z "${ROOT_EXCEL_TRACKED}" ]]; then
    echo "- Nenhum workbook Excel versionado na raiz."
  else
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        echo "- ${file}"
      fi
    done <<< "${ROOT_EXCEL_TRACKED}"
  fi
  echo ""
  echo "#### Bancos locais versionados"
  echo ""
  if [[ -z "${DB_TRACKED}" ]]; then
    echo "- Nenhum banco local versionado identificado por extensao."
  else
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        echo "- ${file}"
      fi
    done <<< "${DB_TRACKED}"
  fi
  echo ""
  echo "#### Arquivos de ambiente versionados"
  echo ""
  if [[ -z "${ENV_TRACKED}" ]]; then
    echo "- Nenhum arquivo de ambiente versionado identificado por padrao."
  else
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        echo "- ${file}"
      fi
    done <<< "${ENV_TRACKED}"
  fi
  echo ""
  echo "#### Logs, temporarios ou backups versionados"
  echo ""
  if [[ -z "${LOG_TRACKED}" ]]; then
    echo "- Nenhum log, temporario ou backup versionado identificado por extensao."
  else
    while IFS= read -r file; do
      if [[ -n "${file}" ]]; then
        echo "- ${file}"
      fi
    done <<< "${LOG_TRACKED}"
  fi
  echo ""
  echo "### Matriz provisoria de decisao"
  echo ""
  echo "| Classe | Tratamento provisório | Observacao |"
  echo "| --- | --- | --- |"
  echo "| Codigo-fonte versionado | Incluir no pacote tecnico | Sujeito a validacao de testes e dependencias |"
  echo "| Documentacao versionada | Incluir | Mantem rastreabilidade das fases e decisoes |"
  echo "| Scripts de apoio versionados | Incluir com ressalva | Diferenciar scripts operacionais de scripts apenas historicos |"
  echo "| Checkpoints e evidencias | Incluir com revisao | Podem conter caminhos locais ou referencias historicas |"
  echo "| Workbooks Excel reais | Excluir por padrao de pacote externo | Incluir apenas com aprovacao explicita e revisao de conteudo |"
  echo "| Workbooks com macro | Excluir por padrao de pacote externo | Exigem revisao especifica de seguranca e necessidade operacional |"
  echo "| Bancos locais e caches | Excluir por padrao | Substituir por migracoes, seeds ou fixtures quando necessario |"
  echo "| Arquivos de ambiente | Excluir | Usar exemplos sem segredos, se aplicavel |"
  echo "| Logs, temporarios e backups | Excluir | Nao devem compor entrega limpa |"
  echo "| Dependencias externas ausentes | Registrar como pre-requisito | Nao criar artefato automaticamente por referencia textual |"
  echo ""
  echo "### Pre-requisitos externos candidatos"
  echo ""
  echo "- Validar se LISTA_RTD.xlsm ainda e necessario ao fluxo real, pois ha muitas referencias textuais e ausencia no repositorio."
  echo "- Validar se OPERACOES_E_OPCOES.xlsx e apenas legado ou se existe fluxo local que ainda depende dele."
  echo "- Confirmar se LISTA_RTD.xlsx e OPERACOES_E_OPCOES.xlsm devem permanecer no repositorio ou migrar para fixture controlada."
  echo "- Confirmar se a entrega final sera para uso interno, auditoria tecnica ou distribuicao externa."
  echo ""
  echo "### Regras provisorias para montagem futura"
  echo ""
  echo "- Nao gerar pacote final enquanto houver decisao pendente sobre arquivos Excel reais."
  echo "- Nao incluir dados reais em entrega externa sem aprovacao explicita."
  echo "- Nao incluir macros sem revisao especifica."
  echo "- Nao depender de arquivos ausentes sem declara-los como pre-requisitos."
  echo "- Preferir dados sinteticos, seeds ou fixtures anonimizadas para reproducibilidade."
  echo ""
  echo "### Conclusao da matriz"
  echo ""
  echo "- A matriz provisoria do pacote de entrega foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue preparada para consolidacao final do checklist de entrega."
} >> "${CHECKPOINT}"

python - <<'PY'
from pathlib import Path

path = Path("docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md")
text = path.read_text(encoding="utf-8")
text = text.replace(chr(96), "'")
path.write_text(text, encoding="utf-8", newline="\n")
PY

echo "[OK] Matriz provisoria do pacote de entrega registrada."
