# Próxima ação: preparação da Fase 1

## Objetivo da Fase 1

Transformar o Excel `LISTA_RTD.xlsm` em fonte RTD online viva, sem substituir ainda a arquitetura existente.

## Estratégia segura

A Fase 1 deve começar com um módulo pequeno e testável de diagnóstico do Excel.

Antes de atualizar banco ou UI, o sistema deve conseguir responder:

1. O Excel está aberto?
2. A planilha `LISTA_RTD.xlsm` está aberta?
3. Quais abas existem?
4. Qual aba contém a tabela RTD?
5. Quais cabeçalhos existem?
6. A leitura em bloco funciona?
7. O sistema falha sem travar quando Excel não está disponível?

## Não fazer ainda

Nesta etapa ainda não devemos:

- Alterar preenchimento de legs.
- Alterar fluxo de pricing.
- Alterar UI operacional.
- Remover scripts de refresh.
- Criar histórico intraday.
- Criar candles.

## Primeiro componente funcional futuro

Nome sugerido:

`services/excel_rtd_workbook_probe.py`

Responsabilidade:

- Detectar Excel via COM.
- Localizar `LISTA_RTD.xlsm`.
- Listar abas.
- Ler cabeçalhos e algumas linhas de amostra.
- Retornar status estruturado.

## Primeiro teste futuro

Nome sugerido:

`ATT/tests/test_excel_rtd_workbook_probe_contract.py`

Responsabilidade:

- Testar contrato sem exigir Excel real.
- Validar objetos de status.
- Validar erro controlado quando Excel não estiver disponível.
- Permitir teste unitário com adaptador fake.

## Primeiro script operacional futuro

Nome sugerido:

`scripts/probe_excel_rtd_workbook.py`

Responsabilidade:

- Rodar diagnóstico manual no ambiente Windows.
- Mostrar status do Excel, workbook, abas e cabeçalhos.
- Não gravar banco ainda.
