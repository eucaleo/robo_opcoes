#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Classificacao dos arquivos de dados na raiz"

echo "[INFO] Registrando classificacao dos arquivos de dados da raiz em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Classificacao dos arquivos de dados da raiz ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

ROOT_DATA_FILES="$(
  git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls|csv|db|sqlite|sqlite3)$' || true
)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Classificacao documental dos arquivos de dados ou binarios localizados na raiz."
  echo "- Nenhum arquivo foi alterado, removido ou movido nesta etapa."
  echo "- O objetivo e orientar a decisao de entrega sem risco funcional."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da classificacao: ${HEAD_LINE}"
  echo ""
  echo "### Arquivos avaliados"
  echo ""
  if [[ -z "${ROOT_DATA_FILES}" ]]; then
    echo "- Nenhum arquivo de dados ou binario versionado foi encontrado na raiz."
  else
    while IFS= read -r file; do
      if [[ -f "${file}" ]]; then
        SIZE_BYTES="$(stat -c%s "${file}" 2>/dev/null || echo desconhecido)"
        LAST_COMMIT="$(git log -1 --oneline -- "${file}" 2>/dev/null || echo sem historico identificado)"
        echo "- Arquivo: ${file}"
        echo "  - Tamanho em bytes: ${SIZE_BYTES}"
        echo "  - Ultimo commit relacionado: ${LAST_COMMIT}"
        echo "  - Classificacao preliminar: artefato de dados operacional"
        echo "  - Acao recomendada: manter documentado ate decisao funcional explicita"
      else
        echo "- Arquivo: ${file}"
        echo "  - Situacao: listado pelo Git, mas nao encontrado no diretorio de trabalho"
      fi
    done <<< "${ROOT_DATA_FILES}"
  fi
  echo ""
  echo "### Diretriz de tratamento"
  echo ""
  echo "- Arquivos de planilha na raiz podem representar insumos operacionais, exemplos, bases manuais ou artefatos locais."
  echo "- A remocao ou movimentacao deve ocorrer somente apos confirmacao de dependencia funcional."
  echo "- Caso sejam essenciais, devem permanecer versionados e documentados."
  echo "- Caso sejam apenas artefatos locais, devem ser removidos ou movidos em etapa propria, com commit separado."
  echo "- Caso contenham dados sensiveis, devem ser tratados antes da entrega externa."
  echo ""
  echo "### Conclusao da classificacao"
  echo ""
  echo "- A classificacao dos arquivos de dados da raiz foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue preparada para revisao de dependencias operacionais e empacotamento controlado."
} >> "${CHECKPOINT}"

echo "[OK] Classificacao dos arquivos de dados da raiz registrada."
