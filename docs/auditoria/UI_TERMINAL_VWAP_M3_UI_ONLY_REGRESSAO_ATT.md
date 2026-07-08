# M3 UI-only Terminal VWAP - regressao automatizada acumulada

Data: 2026-07-07

Branch:

audit/ui-modern-terminal-vwap-m3-ui-only

HEAD no momento da validacao:

b23e901

## 1. Objetivo

Registrar a evidencia de regressao automatizada acumulada apos as correcoes e testes UI-only relacionados ao carregamento de estrutura do Terminal VWAP a partir de decisoes na UI moderna dark.

## 2. Commits recentes validados

b23e901 test(ui): rejeita id de decisao nao numerico
01c09ba test(ui): ignora ids de estrutura nao numericos
2eb52c5 test(ui): cobre id de estrutura com zeros a esquerda
2ad5b03 fix(ui): compara id de estrutura como numero
5fd9d4d fix(ui): normaliza id ao carregar estrutura da decisao
72425a0 test(ui): aceita id numerico como texto ao carregar estrutura
61b4d25 test(ui): ignora ids invalidos ao carregar estrutura
468b13f test(ui): avisa quando estrutura carregada nao existe

## 3. Validacao automatizada executada

Comando executado:

python -m pytest ATT/tests -q

Resultado:

729 passed, 2 skipped, 6 subtests passed in 40.40s

## 4. Validacao de estado Git

Estado apos os commits e antes deste registro documental:

On branch audit/ui-modern-terminal-vwap-m3-ui-only
nothing to commit, working tree clean

## 5. Comportamentos cobertos nesta sequencia

A sequencia validou o carregamento de estrutura do Terminal VWAP a partir de decisoes para casos como:

- estrutura inexistente;
- ids invalidos;
- id numerico vindo como texto;
- normalizacao de id;
- comparacao numerica de id;
- id com zeros a esquerda;
- ids de estrutura nao numericos ignorados;
- id de decisao nao numerico rejeitado.

## 6. Garantias de escopo

Esta regressao nao autoriza equivalencia global da UI moderna dark.

A frente permanece restrita a UI e testes, sem alterar intencionalmente:

- banco;
- schema;
- pipeline;
- services;
- repositories;
- controllers;
- regra de negocio;
- payoff;
- UIDataModel.

## 7. Classificacao

M3_UI_ONLY_REGRESSAO
AUDITORIA_TERMINAL_VWAP
TESTADO_COM_PYTEST
REGRESSAO_AUTOMATIZADA_ACUMULADA
