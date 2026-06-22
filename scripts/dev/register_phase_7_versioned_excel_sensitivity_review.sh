#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Revisao de sensibilidade dos artefatos Excel versionados"

echo "[INFO] Registrando revisao de sensibilidade dos artefatos Excel versionados em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Revisao de sensibilidade dos artefatos Excel versionados ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

ROOT_EXCEL_FILES="$(
  git ls-files | grep -Ei '^[^/]+\.(xlsx|xlsm|xls)$' || true
)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Revisao documental de sensibilidade dos arquivos Excel versionados na raiz."
  echo "- Nenhum arquivo foi aberto para leitura de conteudo operacional."
  echo "- Nenhum arquivo foi alterado, removido, criado, renomeado ou movido nesta etapa."
  echo "- A revisao considera apenas presenca, versionamento, extensao, tamanho e risco operacional presumido."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da revisao: ${HEAD_LINE}"
  echo ""
  echo "### Artefatos Excel versionados avaliados"
  echo ""

  if [[ -z "${ROOT_EXCEL_FILES}" ]]; then
    echo "- Nenhum artefato Excel versionado encontrado na raiz."
  else
    while IFS= read -r file; do
      if [[ -z "${file}" ]]; then
        continue
      fi

      EXT="${file##*.}"
      SIZE_BYTES="indisponivel"
      LAST_COMMIT="sem historico identificado"
      RISK="sensibilidade operacional potencial"
      MACRO_RISK="nao aplicavel"

      if [[ -e "${file}" ]]; then
        SIZE_BYTES="$(wc -c < "${file}" | tr -d ' ')"
      fi

      LAST_COMMIT="$(git log -1 --oneline -- "${file}" 2>/dev/null || echo sem historico identificado)"

      case "${EXT,,}" in
        xlsm)
          RISK="alto"
          MACRO_RISK="possivel presenca de macros por extensao xlsm"
          ;;
        xlsx)
          RISK="medio"
          MACRO_RISK="baixo por extensao xlsx, sem validacao de conteudo"
          ;;
        xls)
          RISK="alto"
          MACRO_RISK="formato legado com risco operacional a revisar"
          ;;
        *)
          RISK="indefinido"
          MACRO_RISK="extensao nao classificada"
          ;;
      esac

      echo "- Arquivo: ${file}"
      echo "  - Extensao: ${EXT}"
      echo "  - Tamanho em bytes: ${SIZE_BYTES}"
      echo "  - Ultimo commit relacionado: ${LAST_COMMIT}"
      echo "  - Risco presumido para entrega externa: ${RISK}"
      echo "  - Observacao sobre macro: ${MACRO_RISK}"
      echo "  - Diretriz provisoria: revisar conteudo e necessidade operacional antes de empacotar."
    done <<< "${ROOT_EXCEL_FILES}"
  fi

  echo ""
  echo "### Criterios de sensibilidade adotados"
  echo ""
  echo "- Arquivos Excel podem conter dados reais, parametros operacionais, informacoes historicas ou formulas proprietarias."
  echo "- Arquivos xlsm devem ser tratados como sensiveis ate revisao explicita, pois podem conter macros."
  echo "- Arquivos xlsx tambem podem ser sensiveis mesmo sem macros, pois podem conter dados operacionais."
  echo "- Tamanho, extensao e versionamento nao comprovam seguranca para distribuicao."
  echo "- A ausencia de leitura de conteudo nesta etapa evita exposicao desnecessaria de dados."
  echo ""
  echo "### Regras provisorias derivadas"
  echo ""
  echo "- Nao incluir artefatos Excel reais em pacote externo sem aprovacao explicita."
  echo "- Preferir fixtures anonimizadas ou dados sinteticos quando a entrega exigir reprodutibilidade."
  echo "- Se o fluxo real depender de workbook externo ausente, documentar como pre-requisito e nao como arquivo entregue automaticamente."
  echo "- Se arquivo com macro for necessario, exigir revisao especifica de seguranca e finalidade operacional."
  echo ""
  echo "### Conclusao da revisao"
  echo ""
  echo "- A revisao de sensibilidade dos artefatos Excel versionados foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue preparada para definicao final do pacote de entrega e lista de exclusoes ou pre-requisitos."
} >> "${CHECKPOINT}"

python - <<'PY'
from pathlib import Path

path = Path("docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md")
text = path.read_text(encoding="utf-8")
text = text.replace(chr(96), "'")
path.write_text(text, encoding="utf-8", newline="\n")
PY

echo "[OK] Revisao de sensibilidade dos artefatos Excel versionados registrada."
