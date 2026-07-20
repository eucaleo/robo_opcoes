# Tests - Historico intraday RTD Option Quotes

## Contexto

Esta pasta contem os testes automatizados do projeto.

Para a primeira implementacao funcional da Fase 3, os testes previstos sao:

- `ATT/tests/test_rtd_option_quotes_intraday_history_schema_contract.py`
- `ATT/tests/test_rtd_option_quotes_intraday_history_repository.py`
- `ATT/tests/test_rtd_option_quotes_intraday_capture_service.py`

## Cobertura obrigatoria

Os testes da Fase 3 devem garantir:

- schema minimo do historico intraday;
- criacao ou validacao da tabela de historico;
- append de multiplas amostras para o mesmo `codigo_opcao`;
- consulta por `codigo_opcao`;
- consulta por intervalo de tempo;
- captura a partir do snapshot `rtd_option_quotes`;
- ausencia de subprocesso;
- ausencia de leitura direta do Excel no servico de historico;
- preservacao dos testes da Fase 1;
- preservacao dos testes da Fase 2.

## Baseline obrigatorio

Ao implementar a Fase 3, devem continuar passando os testes da rota RTD ja aceitos, incluindo:

- probe Excel RTD;
- reader RTD;
- sync de `rtd_option_quotes`;
- contrato do snapshot;
- repositorio do snapshot;
- enriquecimento de legs;
- guardrail contra subprocesso operacional.

## Fora de escopo nesta fase

Nao testar ainda:

- candles;
- OHLC;
- VWAP temporal calculado;
- agregacoes;
- UI em tempo real;
- loop operacional permanente.

## Fonte contratual

Contrato oficial:

- `FRENTE_RTD_EXCEL_BTG_ONLINE/18_CONTRATO_FASE3_HISTORICO_INTRADAY.md`
