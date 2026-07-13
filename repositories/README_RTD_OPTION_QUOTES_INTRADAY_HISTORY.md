# Repositories - Historico intraday RTD Option Quotes

## Contexto

Esta pasta contem repositorios de persistencia do projeto.

Para a Fase 3 da frente RTD Excel BTG Online, o repositorio previsto e:

- `repositories/rtd_option_quotes_intraday_history_repository.py`

## Responsabilidade prevista

O repositorio de historico intraday deve ser responsavel por:

- garantir ou validar o schema minimo da tabela de historico intraday;
- inserir amostras temporais vindas do snapshot `rtd_option_quotes`;
- consultar amostras por `codigo_opcao`;
- consultar amostras por intervalo de tempo;
- manter comportamento append-only ou predominantemente append-only;
- nao acessar Excel diretamente;
- nao executar subprocessos;
- nao substituir o snapshot atual da Fase 2.

## Tabela preferencial

Nome tecnico preferencial:

- `rtd_option_quotes_intraday_history`

## Separacao obrigatoria

A tabela `rtd_option_quotes` continua sendo o snapshot atual.

A tabela de historico intraday deve representar amostras temporais desse snapshot.

## Proibicoes

Nao implementar aqui:

- leitura direta do Excel;
- loop operacional permanente;
- subprocesso RTD;
- candles;
- OHLC;
- VWAP temporal calculado;
- logica de UI.

## Fonte contratual

Contrato oficial:

- `FRENTE_RTD_EXCEL_BTG_ONLINE/18_CONTRATO_FASE3_HISTORICO_INTRADAY.md`
