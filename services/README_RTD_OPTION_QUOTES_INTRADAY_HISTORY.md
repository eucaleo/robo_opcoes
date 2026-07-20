# Services - Historico intraday RTD Option Quotes

## Contexto

Esta pasta contem servicos de aplicacao.

Para a Fase 3 da frente RTD Excel BTG Online, o servico previsto e:

- `services/rtd_option_quotes_intraday_history_service.py`

## Responsabilidade prevista

O servico de captura historica intraday deve ser responsavel por:

- consumir o snapshot atual `rtd_option_quotes`;
- montar amostras historicas com horario de captura;
- persistir essas amostras usando o repositorio de historico intraday;
- retornar quantidade de linhas capturadas;
- preservar o contrato aceito da Fase 2;
- nao acessar Excel diretamente;
- nao criar consulta RTD sob demanda;
- nao executar subprocessos.

## Fluxo permitido

Fluxo correto:

1. Excel RTD vivo alimenta o snapshot.
2. Snapshot e persistido em `rtd_option_quotes`.
3. Servico da Fase 3 le `rtd_option_quotes`.
4. Servico grava amostras em `rtd_option_quotes_intraday_history`.

## Fluxo proibido

Nao e permitido:

1. Historico chamar Excel diretamente.
2. Historico executar script externo RTD.
3. Historico recriar consulta individual por opcao.
4. Historico substituir a tabela `rtd_option_quotes`.
5. Historico criar candles nesta fase.

## Fonte contratual

Contrato oficial:

- `FRENTE_RTD_EXCEL_BTG_ONLINE/18_CONTRATO_FASE3_HISTORICO_INTRADAY.md`
