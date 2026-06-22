#!/usr/bin/env bash
set -euo pipefail

CHECKPOINT="docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md"
SECTION_TITLE="## Diretriz provisoria de empacotamento dos artefatos Excel"

echo "[INFO] Registrando diretriz provisoria de empacotamento dos artefatos Excel em: ${CHECKPOINT}"

if grep -q "^${SECTION_TITLE}$" "${CHECKPOINT}"; then
  echo "[SKIP] Diretriz provisoria de empacotamento dos artefatos Excel ja registrada."
  exit 0
fi

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline -1)"

{
  echo ""
  echo "${SECTION_TITLE}"
  echo ""
  echo "### Escopo"
  echo ""
  echo "- Registro documental de diretriz provisoria para tratamento de arquivos Excel na entrega."
  echo "- Nenhum arquivo foi alterado, removido, criado ou movido nesta etapa."
  echo "- A diretriz se baseia nas revisoes de classificacao, dependencias e aderencia entre referencias e arquivos versionados."
  echo ""
  echo "### Estado de referencia"
  echo ""
  echo "- Branch atual: ${BRANCH}"
  echo "- Commit base da diretriz: ${HEAD_LINE}"
  echo ""
  echo "### Diretriz por artefato"
  echo ""
  echo "- Arquivo: LISTA_RTD.xlsx"
  echo "  - Estado observado: presente e versionado na raiz."
  echo "  - Leitura operacional: artefato legado ou historico, com referencias documentais relevantes."
  echo "  - Diretriz provisoria: manter no repositorio ate decisao funcional explicita."
  echo "  - Restricao para entrega externa: revisar conteudo antes de empacotar, pois pode conter dados operacionais ou sensiveis."
  echo ""
  echo "- Arquivo: LISTA_RTD.xlsm"
  echo "  - Estado observado: referenciado com frequencia, mas ausente e nao versionado na raiz."
  echo "  - Leitura operacional: possivel dependencia operacional externa, historica ou nao empacotada."
  echo "  - Diretriz provisoria: nao criar, nao renomear e nao substituir automaticamente."
  echo "  - Restricao para entrega externa: registrar como lacuna ou pre-requisito externo caso ainda seja necessario ao fluxo real."
  echo ""
  echo "- Arquivo: OPERACOES_E_OPCOES.xlsm"
  echo "  - Estado observado: presente e versionado na raiz."
  echo "  - Leitura operacional: artefato de dados operacional com potencial uso em validacoes locais e fluxos legados."
  echo "  - Diretriz provisoria: manter versionado ate decisao funcional explicita."
  echo "  - Restricao para entrega externa: revisar conteudo e macros antes de empacotar."
  echo ""
  echo "- Arquivo: OPERACOES_E_OPCOES.xlsx"
  echo "  - Estado observado: referenciado, ausente, nao versionado e ignorado pelo Git."
  echo "  - Leitura operacional: referencia legada ou alternativa ao workbook principal."
  echo "  - Diretriz provisoria: nao incluir na entrega sem decisao explicita."
  echo "  - Restricao para entrega externa: se necessario, documentar como arquivo local esperado ou substituir por fixture controlada."
  echo ""
  echo "### Regras provisorias para entrega"
  echo ""
  echo "- Nao empacotar arquivos Excel com dados reais sem revisao de conteudo."
  echo "- Nao empacotar arquivos com macro sem revisao especifica de seguranca e necessidade operacional."
  echo "- Nao substituir extensoes xlsx por xlsm, ou xlsm por xlsx, sem validacao funcional."
  echo "- Nao inferir que arquivo ausente deve ser criado apenas por haver referencia textual."
  echo "- Caso a entrega precise ser reproduzivel sem planilhas reais, criar etapa futura para fixtures anonimizadas ou dados de exemplo."
  echo ""
  echo "### Conclusao da diretriz"
  echo ""
  echo "- A diretriz provisoria de empacotamento dos artefatos Excel foi registrada sem alteracao funcional."
  echo "- A Fase 7 segue preparada para revisao de sensibilidade dos artefatos versionados e definicao final de pacote de entrega."
} >> "${CHECKPOINT}"

python - <<'PY'
from pathlib import Path

path = Path("docs/checkpoints/FASE_7_CONSOLIDACAO_OPERACIONAL_PREPARO_ENTREGA.md")
text = path.read_text(encoding="utf-8")
text = text.replace(chr(96), "'")
path.write_text(text, encoding="utf-8", newline="\n")
PY

echo "[OK] Diretriz provisoria de empacotamento dos artefatos Excel registrada."
