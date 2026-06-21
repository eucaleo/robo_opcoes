#!/usr/bin/env bash
set -euo pipefail

BRANCH_ESPERADA="fase-3a4-auto-pricing-manual-save"
TEST_FILE="ATT/tests/test_structure_editor_dialog.py"
EVID_DIR="docs/checkpoints/evidencias"
FECHAMENTO_FILE="$EVID_DIR/fase-2b-fechamento-normalizacao-numerica.md"
PYTEST_FILE="$EVID_DIR/fase-2b-pytest-fechamento-editor-dialog.txt"

echo "== Fase 2B - Fechamento automatizado =="
echo

echo "1) Verificando branch..."
CURRENT_BRANCH="$(git branch --show-current)"
echo "Branch atual: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "$BRANCH_ESPERADA" ]; then
  echo "ERRO: branch inesperada."
  echo "Esperada: $BRANCH_ESPERADA"
  echo "Atual:    $CURRENT_BRANCH"
  exit 1
fi

echo
echo "2) Verificando working tree..."
if [ -n "$(git status --porcelain)" ]; then
  echo "ERRO: existem alterações pendentes."
  git status --short
  exit 1
fi

mkdir -p "$EVID_DIR"

echo
echo "3) Rodando pytest final focado..."
set +e
python -m pytest "$TEST_FILE" -q > "$PYTEST_FILE" 2>&1
PYTEST_EXIT=$?
set -e

cat "$PYTEST_FILE"

if [ "$PYTEST_EXIT" -ne 0 ]; then
  echo
  echo "ERRO: pytest falhou. Fechamento não será gerado."
  exit "$PYTEST_EXIT"
fi

echo
echo "4) Gerando documento de fechamento..."
cat > "$FECHAMENTO_FILE" <<EOFMD
# Fase 2B - Fechamento da normalização numérica

Data: $(date +"%Y-%m-%d %H:%M:%S")
Branch: $CURRENT_BRANCH

## Objetivo

Registrar o fechamento da validação de normalização numérica no editor de estruturas,
com foco em \`StructureEditorDialog._build_legs_payload()\`.

## Escopo validado

Foram validados os seguintes campos numéricos:

- \`strike\`
- \`premium\`
- \`multiplier\`
- \`quantity\`

## Evidências principais

### Análise inicial

- \`docs/checkpoints/evidencias/fase-2b-analise-normalizacao-numerica.md\`
- \`docs/checkpoints/evidencias/fase-2b-grep-validacoes-numericas.txt\`
- \`docs/checkpoints/evidencias/fase-2b-grep-campos-numericos.txt\`
- \`docs/checkpoints/evidencias/fase-2b-gitgrep-normalizacao-existente.txt\`

### Baseline pytest

- \`docs/checkpoints/evidencias/fase-2b-pytest-editor-dialog-atual.txt\`

### Regressão de quantity

- \`docs/checkpoints/evidencias/fase-2b-quantity-normalizacao-regressao.md\`
- \`docs/checkpoints/evidencias/fase-2b-pytest-editor-dialog-quantity.txt\`

### Fechamento

- \`$PYTEST_FILE\`

## Resultado do pytest final

\`\`\`text
$(cat "$PYTEST_FILE")
\`\`\`

## Resultado final

Aprovado.

A normalização numérica do editor está coberta por testes automatizados focados.
O campo \`quantity\` foi validado com entradas inteiras em formato string,
decimal com vírgula e decimal com ponto, além de rejeição para valores inválidos.

## Commits relacionados

\`\`\`text
$(git log --oneline -8)
\`\`\`
EOFMD

echo
echo "5) Commitando fechamento..."
git add "$FECHAMENTO_FILE" "$PYTEST_FILE"

git commit -m "docs: fecha validacao da normalizacao numerica fase 2b"

echo
echo "6) Fechamento concluído."
git log --oneline -5
