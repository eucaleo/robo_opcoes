# Fase 1.1: Diagnostico da instancia COM do Excel

## Objetivo

Identificar qual instancia do Excel o Python enxerga via COM.

Esta fase foi criada porque o probe encontrou Excel acessivel, mas nao encontrou nenhum workbook aberto.

Isso pode acontecer quando ha mais de uma instancia do Excel aberta e o COM anexa na instancia errada.

## Script adicionado

- scripts/diagnose_excel_com.py

## Como executar

Com o Excel aberto:

python scripts/diagnose_excel_com.py

## O que o diagnostico mostra

O retorno JSON mostra:

- nome da aplicacao Excel;
- versao;
- visibilidade;
- identificador de janela;
- quantidade de workbooks;
- nomes dos workbooks;
- caminhos completos;
- abas de cada workbook;
- analise automatica procurando as abas RTD-BTG, LISTA e RTD_OPTION_QUOTES.

## Interpretacao esperada

Se workbook_count_seen for 0, o Python anexou em uma instancia do Excel sem arquivo aberto.

Se matching_workbooks_by_sheet trouxer algum item, o arquivo RTD foi localizado por aba, mesmo que o nome dele nao seja LISTA_RTD.xlsm.

Se nenhum workbook aparecer, fechar todas as instancias do Excel e abrir apenas a planilha RTD antes de rodar novamente.
