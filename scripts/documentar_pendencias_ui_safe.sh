#!/usr/bin/env bash
set -u

LOG_FILE="logs/documentar_pendencias_ui.log"

mkdir -p logs

exec > >(tee -a "$LOG_FILE") 2>&1

finalizar() {
  echo
  echo "== Script finalizado =="
  echo "Log salvo em: $LOG_FILE"
  echo
  echo "== Status final =="
  git status --short
  echo
  echo "== Ultimos commits =="
  git log --oneline --decorate -5
  echo
  read -p "Pressione ENTER para fechar..."
}

trap finalizar EXIT

echo "== Documentacao segura das pendencias remanescentes da UI =="
echo "Data: $(date '+%Y-%m-%d %H:%M:%S %z')"

BASE_DIR="$(git rev-parse --show-toplevel)"

if [ -z "$BASE_DIR" ]; then
  echo "ERRO: nao foi possivel localizar a raiz do repositorio."
  exit 1
fi

cd "$BASE_DIR"

BRANCH_ATUAL="$(git branch --show-current)"
DATA_ATUAL="$(date '+%Y-%m-%d %H:%M:%S %z')"

AUDIT_DOC="reports/auditoria/AUDITORIA_REFACTOR_UI.md"

if [ ! -f "$AUDIT_DOC" ]; then
  echo "ERRO: documento de auditoria nao encontrado: $AUDIT_DOC"
  exit 1
fi

mkdir -p docs

DEV_DOC=""

for candidato in \
  "docs/DESENVOLVIMENTO_UI.md" \
  "docs/DESENVOLVIMENTO.md" \
  "docs/desenvolvimento.md" \
  "DESENVOLVIMENTO_UI.md" \
  "DESENVOLVIMENTO.md"
do
  if [ -f "$candidato" ]; then
    DEV_DOC="$candidato"
    break
  fi
done

if [ -z "$DEV_DOC" ]; then
  DEV_DOC="docs/DESENVOLVIMENTO_UI.md"
  cat > "$DEV_DOC" <<'DOCDEV'
# Desenvolvimento UI

Documento de acompanhamento da frente UI.
DOCDEV
fi

MARKER="Checkpoint roadmap UI remanescente - Decisoes dark panel encerrado parcialmente"

append_roadmap() {
  local arquivo="$1"

  if grep -q "$MARKER" "$arquivo"; then
    echo "Marcador ja existe em $arquivo. Nao sera duplicado."
    return 0
  fi

  cat >> "$arquivo" <<EOFROADMAP

---

## $MARKER

Data: $DATA_ATUAL

Branch: $BRANCH_ATUAL

### Estado atual registrado

A fatia Decisoes dark panel foi encerrada como:

    EQUIVALENCIA_PARCIAL_OPERACIONAL

Esta classificacao encerra apenas a entrega parcial e restrita da aba/painel de Decisoes no modo dark.

Nao encerra a frente UI completa.

A UI atual/canonica permanece como caminho principal ate que exista criterio global de equivalencia, regressao e substituicao controlada.

### O que foi considerado encerrado nesta fatia

- equivalencia operacional parcial da area de Decisoes no modo dark;
- callbacks essenciais presentes e documentados;
- selecao de decisao com validacao de indice;
- copia de detalhe;
- carregamento da estrutura associada;
- duplicacao de estrutura;
- arquivamento de estrutura;
- recalculo de payoff;
- registro de decisoes ADJUST e CLOSE;
- mensagens operacionais via _safe_status;
- preservacao de banco de dados, regra de negocio, services, repositories, entrypoint e contratos canonicos.

### Pendencias remanescentes da frente UI

As pendencias abaixo ficam fora do bloqueio desta branch e devem ser tratadas em frentes proprias.

#### 1. Backlog de melhorias da UI de Decisoes

Classificacao:

    BACKLOG_MELHORIA_UI_DECISOES

Itens:

- filtros avancados de decisoes;
- exibicao estruturada de rationale/why JSON;
- refinamentos visuais e ergonomicos;
- validacao manual ampliada de selecao vazia, selecao invalida e botoes dependentes;
- criterios adicionais de navegacao, ordenacao e leitura da tabela;
- revisao futura para eventual equivalencia completa com a UI atual.

#### 2. Criterio global de equivalencia da UI

Classificacao:

    CRITERIO_GLOBAL_UI

Itens:

- montar matriz de equivalencia entre UI atual/canonica e UI moderna/dark;
- definir quais telas podem ser consideradas equivalentes, parciais ou apenas experimentais;
- criar checklist minimo por aba;
- registrar criterios de substituicao segura;
- impedir troca do caminho principal sem validacao funcional e operacional.

#### 3. Terminal VWAP, payoff e UIDataModel

Classificacao:

    FORA_ESCOPO_BRANCH_DECISOES_DARK

Itens:

- Terminal VWAP;
- payoff curve;
- UI/models/ui_data.py;
- refatoracoes tecnicas de payoff;
- validacoes especificas de fluxo do terminal;
- consistencia de dados consumidos pela UI moderna.

Esta frente deve ser auditada separadamente, sem ser misturada com a entrega de Decisoes dark panel.

#### 4. Banco, dados e pipeline

Classificacao:

    BANCO_DADOS_PIPELINE

Itens:

- divergencia entre banco canonico moderno e banco volatil legado;
- verificacao de dados/app.db versus dados/derived.db;
- rastreio de origem dos dados exibidos;
- confirmacao dos contratos de leitura usados pela UI;
- saneamento de pipeline antes de qualquer conclusao global de UI.

Esta frente nao deve ser corrigida dentro de branch visual de Decisoes.

#### 5. Regressao e smoke manual da UI

Classificacao:

    REGRESSAO_UI

Itens:

- roteiro manual por aba;
- validacao de abertura da aplicacao pelo entrypoint principal;
- validacao de navegacao entre abas;
- validacao de acoes sem selecao;
- validacao de dados ausentes;
- validacao de mensagens de status;
- validacao visual em dark mode;
- registro de evidencias minimas antes de merge amplo.

#### 6. Estrategia de encerramento da frente UI

Classificacao:

    PLANO_ENCERRAMENTO_UI

Ordem sugerida:

1. manter a UI atual/canonica como caminho principal;
2. concluir documentacao das pendencias por classificacao;
3. abrir frentes pequenas e separadas por area;
4. evitar misturar banco, regra de negocio, services e UI visual na mesma branch;
5. validar cada fatia com py_compile, git diff --check e smoke manual;
6. somente discutir substituicao da UI atual apos matriz global de equivalencia.

### Decisao operacional

A branch atual pode seguir como encerrada para a fatia Decisoes dark panel, mas a frente UI permanece aberta.

Proximo trabalho recomendado:

    documentar matriz global de equivalencia UI
    separar backlog de Decisoes
    abrir auditoria propria para Terminal VWAP/payoff/UIDataModel
    abrir frente propria para banco/dados/pipeline

### Regra de preservacao

Enquanto a frente UI nao estiver encerrada globalmente, devem permanecer preservados:

- banco de dados;
- regras de negocio;
- services;
- repositories;
- entrypoint principal;
- contratos canonicos;
- UI atual como caminho principal.

EOFROADMAP

  echo "Roadmap anexado em $arquivo."
}

append_roadmap "$AUDIT_DOC"
append_roadmap "$DEV_DOC"

echo
echo "== Arquivos alvo =="
echo "$AUDIT_DOC"
echo "$DEV_DOC"
echo "scripts/documentar_pendencias_ui_safe.sh"

echo
echo "== Status antes do stage =="
git status --short

echo
echo "== Stage dos arquivos =="
git add scripts/documentar_pendencias_ui_safe.sh
git add -f "$AUDIT_DOC" "$DEV_DOC"

echo
echo "== Validando diff staged =="
git diff --cached --check

if [ $? -ne 0 ]; then
  echo "ERRO: git diff --cached --check encontrou problema."
  exit 1
fi

echo
echo "== Resumo do diff staged =="
git diff --cached --stat

if git diff --cached --quiet; then
  echo
  echo "Nada novo para commitar."
else
  echo
  echo "== Criando commit documental seguro =="
  git commit -m "Documenta pendencias remanescentes da frente UI"
fi

echo
echo "== Nenhum push foi executado. =="
