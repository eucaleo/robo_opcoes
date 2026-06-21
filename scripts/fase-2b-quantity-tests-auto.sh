#!/usr/bin/env bash
set -euo pipefail

BRANCH_ESPERADA="fase-3a4-auto-pricing-manual-save"
TEST_FILE="ATT/tests/test_structure_editor_dialog.py"
EVID_DIR="docs/checkpoints/evidencias"
EVID_FILE="$EVID_DIR/fase-2b-pytest-editor-dialog-quantity.txt"
ANALISE_FILE="$EVID_DIR/fase-2b-quantity-normalizacao-regressao.md"
MARKER="FASE_2B_QUANTITY_NORMALIZATION_TESTS"

echo "== Fase 2B - Quantity normalization tests =="
echo

echo "1) Verificando branch atual..."
CURRENT_BRANCH="$(git branch --show-current)"
echo "Branch atual: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "$BRANCH_ESPERADA" ]; then
  echo "ERRO: branch atual diferente da esperada."
  echo "Esperada: $BRANCH_ESPERADA"
  echo "Atual:    $CURRENT_BRANCH"
  exit 1
fi

echo
echo "2) Verificando arquivos pendentes..."
if [ -n "$(git status --porcelain)" ]; then
  echo "ERRO: existem alterações pendentes no working tree."
  echo "Revise antes de rodar este script:"
  git status --short
  exit 1
fi

echo
echo "3) Validando existência do arquivo de teste..."
if [ ! -f "$TEST_FILE" ]; then
  echo "ERRO: arquivo não encontrado: $TEST_FILE"
  exit 1
fi

mkdir -p "$EVID_DIR"

echo
echo "4) Verificando se os testes de quantity já foram adicionados..."
if grep -q "$MARKER" "$TEST_FILE"; then
  echo "Testes de quantity já existem. Nada será duplicado."
else
  echo "Adicionando testes de regressão para quantity em $TEST_FILE..."

  cat >> "$TEST_FILE" <<'PYEOF'


# FASE_2B_QUANTITY_NORMALIZATION_TESTS
import pytest


def _dlg_com_quantity_para_teste(quantity_value):
    dlg = object.__new__(StructureEditorDialog)
    dlg._legs_rows = [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "strike": "100,00",
            "expiration_date": "2026-12-18",
            "quantity": quantity_value,
            "premium": None,
            "multiplier": 1,
            "symbol": "TESTC100",
            "notes": None,
        }
    ]
    return dlg


@pytest.mark.parametrize("quantity_value", ["1", "1,0", "1.0"])
def test_build_legs_payload_normaliza_quantity_inteiro_valido(quantity_value):
    dlg = _dlg_com_quantity_para_teste(quantity_value)

    payload = dlg._build_legs_payload()

    assert payload[0]["quantity"] == 1
    assert isinstance(payload[0]["quantity"], int)


@pytest.mark.parametrize("quantity_value", ["1,5", "abc"])
def test_build_legs_payload_rejeita_quantity_invalido(quantity_value):
    dlg = _dlg_com_quantity_para_teste(quantity_value)

    with pytest.raises(
        (ValueError, TypeError),
        match=r"(?i)(quantity|quantidade|inteiro|integer|invalid|inv[aá]lid)",
    ):
        dlg._build_legs_payload()
PYEOF

fi

echo
echo "5) Registrando análise documental..."
cat > "$ANALISE_FILE" <<EOFMD
# Fase 2B - Regressão de normalização numérica para quantity

Data: $(date +"%Y-%m-%d %H:%M:%S")
Branch: $CURRENT_BRANCH

## Objetivo

Adicionar testes automatizados específicos para garantir que o campo \`quantity\`
seja normalizado como inteiro durante a montagem do payload em
\`StructureEditorDialog._build_legs_payload()\`.

## Casos cobertos

### Entradas aceitas

- \`"1"\` deve gerar \`1\` como \`int\`
- \`"1,0"\` deve gerar \`1\` como \`int\`
- \`"1.0"\` deve gerar \`1\` como \`int\`

### Entradas rejeitadas

- \`"1,5"\` deve ser rejeitado
- \`"abc"\` deve ser rejeitado

## Arquivo alterado

- \`$TEST_FILE\`

## Evidência de pytest

- \`$EVID_FILE\`

EOFMD

echo
echo "6) Rodando pytest focado..."
set +e
python -m pytest "$TEST_FILE" -q > "$EVID_FILE" 2>&1
PYTEST_EXIT=$?
set -e

cat "$EVID_FILE"

echo
echo "7) Avaliando resultado..."
if [ "$PYTEST_EXIT" -ne 0 ]; then
  echo
  echo "ATENÇÃO: os testes falharam."
  echo "Isso pode indicar que o código ainda não normaliza/rejeita quantity conforme esperado."
  echo
  echo "Arquivos gerados/modificados:"
  git status --short
  echo
  echo "Nenhum commit automático será feito."
  echo "Próximo passo: ajustar o código de normalização ou revisar expectativa dos testes."
  exit "$PYTEST_EXIT"
fi

echo
echo "8) Pytest verde. Preparando commit..."
git add "$TEST_FILE" "$ANALISE_FILE" "$EVID_FILE"

if git diff --cached --quiet; then
  echo "Nada novo para commitar."
  exit 0
fi

git commit -m "test: adiciona regressao para normalizacao de quantity"

echo
echo "9) Commit criado com sucesso."
git log --oneline -3

echo
echo "Concluído."
