# Relatorio 32.13.2 - Auditoria UI sintaxe e payoff somente backend

Gerado em: 2026-07-17T20:42:27
Status: ok

## Checks

- Nome: arquivo_ui
  - Status: ok
  - Detalhe: Arquivo encontrado: C:\Users\eucal\projeto\UI\components\terminal_vwap_payoff_dark_panel.py

- Nome: py_compile
  - Status: ok
  - Detalhe: Arquivo UI compila sem erro de sintaxe.

- Nome: ast_parse
  - Status: ok
  - Detalhe: AST carregada com sucesso.

- Nome: bloqueio_calculo_local_payoff
  - Status: ok
  - Detalhe: Funcao local de payoff bloqueada com marcador e retorno vazio.

- Nome: escopo_funcao_bloqueada
  - Status: ok
  - Detalhe: Nao foram encontrados sinais fortes de calculo local dentro da funcao bloqueada.

## Conclusao
UI compila e calculo local de payoff permanece bloqueado.
