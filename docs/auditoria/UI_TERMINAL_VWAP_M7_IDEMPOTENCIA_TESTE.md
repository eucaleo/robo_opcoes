# UI Terminal VWAP - M7 - Idempotencia automatizada

## 1. Identificacao

Branch:

~~~text
audit/ui-modern-terminal-vwap-m7-idempotencia-teste
~~~

Commit base auditado:

~~~text
69bc95b
~~~

Documento gerado em:

~~~text
2026-07-08 08:15:15
~~~

## 2. Objetivo

Registrar a evidencia automatizada de idempotencia do carregamento de estrutura no fluxo Terminal VWAP integrado ao painel de Decisoes.

## 3. Evidencias no codigo

Arquivo auditado:

~~~text
ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py
~~~

Testes obrigatorios localizados:

~~~text
test_modern_dark_window_load_structure_from_decision_keeps_valid_selection_after_missing_structure
test_modern_dark_window_load_structure_from_decision_is_idempotent_when_already_selected
~~~

## 4. Garantias cobertas

- Carregar uma estrutura valida preserva a selecao corrente.
- Tentativa posterior de carregar estrutura inexistente nao limpa selecao valida anterior.
- Carregar novamente a mesma estrutura, inclusive com representacao equivalente como zero padding, nao duplica selecao.
- O fluxo nao exige alteracao em banco, schema, services, repositories ou regra de negocio.

## 5. Validacao automatizada

### Comando

~~~bash
python -m pytest ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py::test_modern_dark_window_load_structure_from_decision_is_idempotent_when_already_selected -q
~~~

### Resultado

~~~text
.                                                                        [100%]
1 passed in 0.11s
~~~

### Comando

~~~bash
python -m pytest ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py -q
~~~

### Resultado

~~~text
.........................                                                [100%]
25 passed in 0.26s
~~~

### Comando

~~~bash
python -m pytest ATT/tests -q
~~~

### Resultado

~~~text
........................................................................ [  9%]
........................................................................ [ 19%]
........................................................................ [ 29%]
.................................................................. [ 38%]
........................................................................ [ 48%]
........................................................................ [ 58%]
........................................................................ [ 67%]
......................................................ss................ [ 77%]
........................................................................ [ 87%]
........................................................................ [ 97%]
...................                                                      [100%]
731 passed, 2 skipped, 6 subtests passed in 39.53s
~~~


## 6. Conclusao

A regressao automatizada confirma que o carregamento de estrutura no Terminal VWAP permanece idempotente e preserva selecao valida.
