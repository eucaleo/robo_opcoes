# Fase 1: Probe controlado do Excel RTD

## Objetivo

Criar o primeiro componente funcional da frente RTD Excel BTG Online.

O componente deve diagnosticar o Excel aberto e a planilha LISTA_RTD.xlsm, sem alterar banco, UI ou fluxo de pricing.

## Arquivos adicionados

- services/excel_rtd_workbook_probe.py
- ATT/tests/test_excel_rtd_workbook_probe_contract.py
- scripts/probe_excel_rtd_workbook.py

## Decisao tecnica

O adaptador real usa win32com.client.GetActiveObject("Excel.Application").

Isso e proposital.

Nao usamos Dispatch("Excel.Application") neste componente, pois Dispatch pode abrir uma nova instancia do Excel. A arquitetura da frente exige observar o Excel ja aberto pela operacao.

## Responsabilidades

O probe deve:

1. Detectar se o Excel esta acessivel.
2. Localizar LISTA_RTD.xlsm.
3. Listar abas.
4. Escolher uma aba.
5. Ler cabecalhos e amostra.
6. Retornar status estruturado.

## Nao responsabilidades

O probe nao deve:

- gravar no banco;
- abrir corretora;
- abrir Excel;
- alterar UI;
- chamar subprocesso;
- substituir scripts legados;
- fazer refresh sob demanda por simbolo.

## Testes

Os testes unitarios usam adaptador fake e nao exigem Excel real.

Teste principal:

python -m pytest ATT/tests/test_excel_rtd_workbook_probe_contract.py -q

## Teste operacional manual

Com Excel ja aberto e LISTA_RTD.xlsm carregado:

python scripts/probe_excel_rtd_workbook.py

Com aba preferencial:

python scripts/probe_excel_rtd_workbook.py --sheet RTD_LINKS

O retorno e JSON e deve ser usado apenas para diagnostico.

## Garantia desta fase

Esta fase e apenas observacional.

Nao ha gravacao em banco.
Nao ha abertura de Excel.
Nao ha Dispatch.
Nao ha subprocesso.
Nao ha alteracao de UI.
