# Fase 7H — Pipeline LISTA_RTD Option Quotes

## Status

Concluído.

## Objetivo

Oficializar o fluxo de atualização de cotações de opções via Excel RTD, usando `LISTA_RTD.xlsm` como gateway para a tabela `rtd_option_quotes`.

## Fluxo validado

```text
LISTA_RTD.xlsm
-> aba RTD_PROBE_OPTIONS / RTD_OPTION_QUOTES
-> scripts/import_lista_rtd_excel_to_option_quotes.py
-> dados/app.db
-> rtd_option_quotes
-> scripts/audit_rtd_option_quotes.py
