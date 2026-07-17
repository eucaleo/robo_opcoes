# Relatório 32.13.1 - Auditoria sintaxe UI e bloqueio cálculo local

Gerado em: 2026-07-17T20:40:04.526154-03:00
Status: error

## Arquivo auditado

C:\Users\eucal\projeto\UI\components\terminal_vwap_payoff_dark_panel.py

## Sintaxe

Syntax OK: False

Erro de sintaxe:

'(' was never closed em linha 1270, coluna 43

## Funções proibidas


## Chamadas ainda encontradas

Nenhuma chamada local proibida encontrada via AST.

## Observação

A UI não deve calcular payoff localmente. O fluxo oficial é UI para PayoffRefreshCommandService.
