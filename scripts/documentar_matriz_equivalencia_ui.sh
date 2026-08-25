#!/usr/bin/env bash
set -euo pipefail

echo "== Documentando matriz global de equivalencia da UI =="

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

DATA_ATUAL="$(date '+%Y-%m-%d %H:%M:%S %z')"
BRANCH_ATUAL="$(git branch --show-current)"

MATRIZ_DOC="docs/MATRIZ_EQUIVALENCIA_UI.md"
DEV_DOC="docs/DESENVOLVIMENTO_UI.md"
AUDIT_DOC="reports/auditoria/AUDITORIA_REFACTOR_UI.md"

if [ ! -f "$DEV_DOC" ]; then
  echo "ERRO: documento de desenvolvimento UI nao encontrado: $DEV_DOC"
  exit 1
fi

if [ ! -f "$AUDIT_DOC" ]; then
  echo "ERRO: documento de auditoria nao encontrado: $AUDIT_DOC"
  exit 1
fi

if [ ! -f "$MATRIZ_DOC" ]; then
  cat > "$MATRIZ_DOC" <<EOF_DOC
# Matriz Global de Equivalencia da UI

Data inicial: $DATA_ATUAL

Branch de origem: $BRANCH_ATUAL

## Objetivo

Este documento define a matriz global de equivalencia entre a UI atual/canonica e as frentes modernas/dark em desenvolvimento.

A matriz existe para impedir substituicao prematura da UI principal antes de validacao funcional, operacional e documental.

## Principios

1. A UI atual/canonica permanece como caminho principal.
2. A UI moderna/dark pode ser validada por fatias.
3. Equivalencia parcial nao significa encerramento global da frente UI.
4. Cada aba ou painel deve ter criterio proprio.
5. Banco, regra de negocio, services, repositories e entrypoint principal devem permanecer preservados.
6. Substituicao de caminho principal exige validacao global, nao apenas visual.

## Classificacoes possiveis

### CANONICA

Tela ou fluxo atualmente considerado principal para operacao.

### EQUIVALENTE

Tela ou fluxo moderno/dark validado contra a UI canonica, cobrindo funcionalidades essenciais, estados vazios, erros esperados e operacao manual.

### EQUIVALENCIA_PARCIAL_OPERACIONAL

Tela ou fluxo moderno/dark cobre uma parte operacional relevante, mas ainda nao substitui a UI canonica.

### EXPERIMENTAL

Tela, painel ou fluxo em desenvolvimento, sem garantia de equivalencia.

### PENDENTE

Area ainda nao auditada ou nao validada.

### FORA_ESCOPO

Area explicitamente fora da fatia atual.

## Matriz inicial

| Area / Aba / Fluxo | UI canonica preservada | UI moderna/dark | Estado atual | Evidencia | Proxima acao |
|---|---:|---:|---|---|---|
| Decisoes / painel dark | Sim | Sim | EQUIVALENCIA_PARCIAL_OPERACIONAL | AUDITORIA_REFACTOR_UI.md | Separar backlog de melhorias |
| Terminal VWAP | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Abrir auditoria propria |
| Payoff curve | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Auditar fluxo e UIDataModel |
| UIDataModel | Sim | Indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Mapear consumidores |
| Banco/dados/pipeline | Sim | Nao aplicavel | PENDENTE | AUDITORIA_REFACTOR_UI.md | Auditar origem dos dados |
| Navegacao geral entre abas | Sim | Indefinido | PENDENTE | A definir | Criar smoke manual |
| Mensagens de status | Sim | Parcial | PENDENTE | A definir | Criar checklist por aba |
| Estados vazios e selecao invalida | Sim | Parcial | PENDENTE | A definir | Criar roteiro manual |
| Entrypoint principal | Sim | Nao deve mudar | CANONICA | Politica de preservacao | Preservar |

## Checklist minimo por area

Cada area da UI somente pode sair de PENDENTE ou EXPERIMENTAL quando houver validacao minima dos itens abaixo.

### Funcionalidade

- abertura da tela sem erro;
- carregamento de dados esperado;
- comportamento com dados ausentes;
- comportamento com selecao vazia;
- comportamento com selecao invalida;
- botoes dependentes habilitados/desabilitados corretamente;
- acoes principais executadas sem excecao;
- mensagens de status compreensiveis.

### Equivalencia operacional

- fluxo equivalente identificado na UI canonica;
- entradas e saidas comparadas;
- efeitos colaterais conhecidos;
- ausencia de mudanca em banco fora do previsto;
- ausencia de alteracao em services/repositories;
- preservacao de contratos canonicos.

### Regressao

- py_compile dos arquivos Python alterados;
- git diff --check limpo;
- smoke manual registrado;
- evidencia minima documentada;
- rollback simples identificado.

## Criterio para declarar equivalencia completa

Uma area so pode ser declarada EQUIVALENTE quando:

1. a UI canonica correspondente estiver identificada;
2. todos os fluxos principais tiverem sido testados;
3. estados vazios e invalidos tiverem sido testados;
4. nao houver dependencia de banco volatil ou origem de dados ambigua;
5. nao houver alteracao silenciosa de regra de negocio;
6. o comportamento visual e operacional estiver documentado;
7. houver decisao explicita registrada em auditoria.

## Criterio para substituicao da UI principal

A UI moderna/dark so pode substituir a UI atual/canonica quando:

1. a matriz global estiver completa;
2. todas as areas criticas estiverem como EQUIVALENTE;
3. areas nao equivalentes estiverem documentadas e aceitas;
4. houver smoke manual global;
5. houver plano de rollback;
6. entrypoint principal for alterado apenas em branch propria;
7. a decisao estiver registrada em documento de auditoria.

## Pendencias abertas

- detalhar inventario completo de abas;
- identificar arquivos principais da UI canonica;
- identificar arquivos principais da UI moderna/dark;
- criar roteiro de smoke manual global;
- auditar Terminal VWAP separadamente;
- auditar payoff curve separadamente;
- auditar UIDataModel separadamente;
- auditar banco/dados/pipeline separadamente.

## Decisao operacional

Este documento nao encerra a frente UI.

Ele cria a matriz inicial para orientar proximas fatias pequenas e impedir mistura de escopos.

EOF_DOC
  echo "Criado: $MATRIZ_DOC"
else
  echo "Documento ja existe: $MATRIZ_DOC"
fi

MARKER_DEV="Referencia matriz global de equivalencia UI"

if ! grep -q "$MARKER_DEV" "$DEV_DOC"; then
  cat >> "$DEV_DOC" <<EOF_DEV

---

## $MARKER_DEV

Data: $DATA_ATUAL

Foi criada a matriz global de equivalencia da UI em:

    docs/MATRIZ_EQUIVALENCIA_UI.md

A matriz passa a ser o documento de referencia para classificar telas e fluxos como:

- CANONICA;
- EQUIVALENTE;
- EQUIVALENCIA_PARCIAL_OPERACIONAL;
- EXPERIMENTAL;
- PENDENTE;
- FORA_ESCOPO.

Regra operacional:

A UI atual/canonica permanece como caminho principal ate que a matriz global esteja completa e validada.

EOF_DEV
  echo "Atualizado: $DEV_DOC"
else
  echo "Marcador ja existe em $DEV_DOC"
fi

MARKER_AUDIT="Checkpoint matriz global de equivalencia UI"

if ! grep -q "$MARKER_AUDIT" "$AUDIT_DOC"; then
  cat >> "$AUDIT_DOC" <<EOF_AUDIT

---

## $MARKER_AUDIT

Data: $DATA_ATUAL

Branch: $BRANCH_ATUAL

Foi criada a matriz global de equivalencia da UI:

    docs/MATRIZ_EQUIVALENCIA_UI.md

### Motivo

A frente UI possui entregas parciais e areas fora de escopo que nao devem ser confundidas com equivalencia global.

Este checkpoint formaliza que:

- Decisoes dark panel permanece como equivalencia parcial operacional;
- Terminal VWAP permanece fora do escopo da branch de Decisoes;
- payoff curve permanece fora do escopo da branch de Decisoes;
- UIDataModel permanece fora do escopo da branch de Decisoes;
- banco/dados/pipeline exigem auditoria propria;
- UI canonica permanece preservada como caminho principal.

### Proxima fatia recomendada

Abrir inventario de abas e fluxos da UI para preencher a matriz com base em arquivos reais do projeto.

EOF_AUDIT
  echo "Atualizado: $AUDIT_DOC"
else
  echo "Marcador ja existe em $AUDIT_DOC"
fi

python - <<'PY'
from pathlib import Path

arquivos = [
    Path("docs/MATRIZ_EQUIVALENCIA_UI.md"),
    Path("docs/DESENVOLVIMENTO_UI.md"),
    Path("reports/auditoria/AUDITORIA_REFACTOR_UI.md"),
    Path("scripts/documentar_matriz_equivalencia_ui.sh"),
]

for path in arquivos:
    if not path.exists():
        continue

    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    while lines and lines[-1].strip() == "":
        lines.pop()

    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Normalizado EOF: {path}")
PY

echo "== Fim da documentacao da matriz =="
