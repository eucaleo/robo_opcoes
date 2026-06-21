# Fase 2B - Regressão de normalização numérica para quantity

Data: 2026-06-21 20:53:47
Branch: fase-3a4-auto-pricing-manual-save

## Objetivo

Adicionar testes automatizados específicos para garantir que o campo `quantity`
seja normalizado como inteiro durante a montagem do payload em
`StructureEditorDialog._build_legs_payload()`.

## Casos cobertos

### Entradas aceitas

- `"1"` deve gerar `1` como `int`
- `"1,0"` deve gerar `1` como `int`
- `"1.0"` deve gerar `1` como `int`

### Entradas rejeitadas

- `"1,5"` deve ser rejeitado
- `"abc"` deve ser rejeitado

## Arquivo alterado

- `ATT/tests/test_structure_editor_dialog.py`

## Evidência de pytest

- `docs/checkpoints/evidencias/fase-2b-pytest-editor-dialog-quantity.txt`

