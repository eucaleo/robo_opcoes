#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

BASE_DIR="FRENTE_RTD_EXCEL_BTG_ONLINE"
RESULT="${BASE_DIR}/AUDITORIA_FASE7_ALERTAS_DECISAO_RESULTADO.md"

mkdir -p "$BASE_DIR"

count_pattern() {
    local pattern="$1"
    local count

    count="$(
        (
            git grep -I -n -E "$pattern" -- . \
                ':!FRENTE_RTD_EXCEL_BTG_ONLINE/*.md' \
                ':!*.pdf' \
                ':!*.png' \
                ':!*.jpg' \
                ':!*.jpeg' \
                ':!*.gif' \
                ':!*.xlsx' \
                ':!*.xlsm' \
                2>/dev/null || true
        ) | wc -l | tr -d ' '
    )"

    echo "$count"
}

list_pattern() {
    local pattern="$1"

    (
        git grep -I -n -E "$pattern" -- . \
            ':!FRENTE_RTD_EXCEL_BTG_ONLINE/*.md' \
            ':!*.pdf' \
            ':!*.png' \
            ':!*.jpg' \
            ':!*.jpeg' \
            ':!*.gif' \
            ':!*.xlsx' \
            ':!*.xlsm' \
            2>/dev/null || true
    ) | sed -n '1,80p'
}

BRANCH="$(git branch --show-current)"
HEAD_LINE="$(git log --oneline --decorate -1)"
STATUS_SHORT="$(git status --short)"

RTD_COUNT="$(count_pattern 'RTD|rtd|RTD_OPTION_QUOTES|LISTA_RTD')"
VWAP_COUNT="$(count_pattern 'VWAP|vwap')"
ALERT_COUNT="$(count_pattern 'alerta|alert|Alert|ALERT')"
DECISION_COUNT="$(count_pattern 'decisao|decisão|decision|Decision|DECISION')"
SNAPSHOT_COUNT="$(count_pattern 'snapshot|estado_atual|current_state|symbol_state')"
SQLITE_COUNT="$(count_pattern 'sqlite|SQLite|sqlite3')"
UI_COUNT="$(count_pattern 'tkinter|PyQt|QtWidgets|streamlit|ui|UI|interface')"
PAYOFF_COUNT="$(count_pattern 'payoff|Payoff|PAYOFF')"
SPREAD_COUNT="$(count_pattern 'spread|Spread|SPREAD')"

cat > "$RESULT" <<MD
# Resultado da auditoria tecnica - Fase 7 alertas e decisao operacional

## Contexto

Esta auditoria foi gerada automaticamente para corrigir a rota da Fase 7 e verificar o estado atual do codigo antes de evoluir alertas e decisao operacional.

## Git

- Branch: \`$BRANCH\`
- HEAD: \`$HEAD_LINE\`

## Status do workspace no momento da auditoria

\`\`\`text
${STATUS_SHORT:-workspace limpo}
\`\`\`

## Contagens por tema no codigo versionado

| Tema | Ocorrencias encontradas |
|---|---:|
| RTD / RTD_OPTION_QUOTES / LISTA_RTD | $RTD_COUNT |
| VWAP | $VWAP_COUNT |
| Alertas | $ALERT_COUNT |
| Decisao | $DECISION_COUNT |
| Snapshot / estado atual | $SNAPSHOT_COUNT |
| SQLite | $SQLITE_COUNT |
| UI / interface | $UI_COUNT |
| Payoff | $PAYOFF_COUNT |
| Spread | $SPREAD_COUNT |

## Amostras encontradas

### RTD

\`\`\`text
$(list_pattern 'RTD|rtd|RTD_OPTION_QUOTES|LISTA_RTD')
\`\`\`

### VWAP

\`\`\`text
$(list_pattern 'VWAP|vwap')
\`\`\`

### Alertas

\`\`\`text
$(list_pattern 'alerta|alert|Alert|ALERT')
\`\`\`

### Decisao

\`\`\`text
$(list_pattern 'decisao|decisão|decision|Decision|DECISION')
\`\`\`

### Snapshot

\`\`\`text
$(list_pattern 'snapshot|estado_atual|current_state|symbol_state')
\`\`\`

### SQLite

\`\`\`text
$(list_pattern 'sqlite|SQLite|sqlite3')
\`\`\`

### UI

\`\`\`text
$(list_pattern 'tkinter|PyQt|QtWidgets|streamlit|ui|UI|interface')
\`\`\`

## Leitura preliminar

A Fase 7 operacional nao deve ser considerada encerrada apenas por documento de escopo.

Para encerrar a Fase 7 sem divida tecnica, ainda e necessario confirmar e evoluir:

1. Contrato de alertas.
2. Contrato de decisao operacional.
3. Motor de regras somente leitura.
4. Testes automatizados.
5. Relatorio composto com as fases anteriores.
6. Garantia de ausencia de efeito colateral operacional.

## Proxima acao tecnica recomendada

Criar o menor bloco implementavel da Fase 7R.2:

- contrato interno de alerta;
- avaliador deterministico;
- entrada simulada ou snapshot existente;
- saida textual auditavel;
- testes automatizados;
- sem Excel real;
- sem COM;
- sem escrita operacional;
- sem trigger real;
- sem decisao automatica.
MD

echo "Auditoria gerada em:"
echo "$RESULT"
