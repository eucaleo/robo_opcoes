# Fase 2 — Auditoria do contrato RTD/Excel e arquivos de entrada

## Status

Iniciada.

## Objetivo

Auditar, sem alteração funcional, o contrato entre RTD, Excel e arquivos locais usados como entrada no fluxo de opções.

## Escopo principal

Arquivos P0 vindos da Fase 1:

- `dados/RTD_LINKS.csv`
- `bridge/analise_robo.csv`
- `bridge/analise_robo_legs.csv`
- `bridge/hist_robo.csv`
- `bridge/configuracoes.csv`
- `LISTA_RTD.xlsm`

## Restrições

Esta fase não autoriza alterações em:

- UI
- banco
- schema
- cálculo
- ingestão
- serviços operacionais
- arquivo Excel operacional

## Perguntas de auditoria

1. Qual é o papel de `dados/RTD_LINKS.csv`?
2. Quais colunas existem nos CSVs da pasta `bridge/`?
3. Quais arquivos parecem ser fonte primária?
4. Quais arquivos parecem ser derivados/exportados?
5. Há inconsistência de nomes de colunas entre arquivos?
6. Há dependência direta ou indireta do Excel `.xlsm`?
7. Quais arquivos devem ser preservados como contrato estável?
8. Quais arquivos devem ser tratados como legado ou compatibilidade?

## Resultado esperado

Gerar um mapa documental dos contratos de entrada para orientar as próximas fases.

Nen huma mudança funcional deve ser realizada.
