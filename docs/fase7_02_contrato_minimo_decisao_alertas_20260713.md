# Fase 7.2 - Contrato mínimo de decisão e alertas

Data: 13/07/2026

## Natureza

Definição documental e técnica do contrato mínimo da Fase 7 para decisão operacional assistida e alertas.

Esta etapa não implementa execução real, não envia ordens, não integra broker e não cria automação operacional de mercado.

## Origem

- EXCEL_RTD_BTG_ONLINE REESTRUTURADO
- docs/fase7_01_auditoria_rebaseline_20260713.md
- fase7_00_varredura_limpa_adiantamentos_20260713.md
- fase7_00_varredura_limpa_adiantamentos_20260713.json

## Objetivo

Definir o contrato mínimo reaproveitável para:

- saída de decisão;
- alertas operacionais;
- entrada baseada em snapshot/dados vivos;
- validação de que decisões e alertas não executam ordens reais;
- reaproveitamento seguro dos testes existentes da Fase 7.

## Escopo permitido

A Fase 7.2 pode tratar apenas de:

- contrato de decisão;
- contrato de alerta;
- regras objetivas de alerta;
- adapter de snapshot para decisão;
- validação de payloads;
- testes de domínio e adapter;
- documentação dos bloqueios de execução real.

## Fora do escopo

Permanecem fora do escopo:

- envio automático de ordens reais;
- roteamento automático para broker;
- abertura automática de posição;
- fechamento automático de posição;
- robô executor;
- automação de decisão com execução em mercado real;
- integração operacional que envie ordens;
- alteração de banco sem aprovação específica;
- uso de eventos operacionais avançados como motor da Fase 7 inicial.

## Contrato mínimo de decisão

Uma decisão operacional da Fase 7 deve representar recomendação assistiva, explicável e auditável.

Campos mínimos esperados:

- decision_id ou identificador lógico equivalente;
- structure_id ou referência da estrutura;
- symbol ou ativo/opção principal quando aplicável;
- decision_type;
- status;
- reason;
- confidence ou nível de confiança quando aplicável;
- alerts relacionados;
- market_context;
- created_at ou timestamp equivalente;
- source;
- no_real_order_execution.

Valores conceituais permitidos para decision_type:

- AGUARDAR;
- MONITORAR;
- ALERTAR;
- FAVORAVEL;
- DESFAVORAVEL;
- INDEFINIDA.

Regra obrigatória:

- A decisão não pode representar autorização de execução real.
- A decisão não pode disparar ordem.
- A decisão não pode rotear para broker.
- A decisão deve apoiar decisão humana.

## Contrato mínimo de alerta

Um alerta operacional da Fase 7 deve ser derivado de dados vivos ou snapshot aceito.

Campos mínimos esperados:

- alert_id ou identificador lógico equivalente;
- alert_type;
- severity;
- symbol;
- structure_id quando aplicável;
- message;
- evidence;
- source;
- created_at ou timestamp equivalente;
- acknowledged ou estado visual quando aplicável;
- no_real_order_execution.

Tipos mínimos previstos:

- PRECO_CRUZOU_VWAP;
- SPREAD_ANORMAL;
- LIQUIDEZ_BAIXA;
- DELTA_EM_LIMITE;
- PAYOFF_MUDOU;
- ESTRUTURA_FAVORAVEL;
- ATRASO_DADOS;
- FALHA_RTD;
- CAMPO_OBRIGATORIO_DIVERGENTE;
- SIMBOLO_SEM_RESPOSTA_RTD.

Severidades mínimas:

- INFO;
- WARNING;
- CRITICAL.

Regra obrigatória:

- Alertas são sinais operacionais assistivos.
- Alertas não executam ordens.
- Alertas não substituem decisão humana.

## Entrada mínima para decisão e alerta

A entrada deve vir de fontes já aceitas nas fases anteriores:

- snapshot centralizado;
- histórico intraday;
- candles;
- UI operacional;
- estruturas/payoff;
- VWAP;
- spread;
- volume;
- gregas disponíveis.

Fontes candidatas:

- repositories/market_snapshot_repository.py
- repositories/rtd_option_quotes_repository.py
- services/market_snapshot_selector.py
- services/canonical_input_service.py
- services/structure_leg_rtd_enrichment_service.py
- services/terminal_vwap_payoff_viewmodel_service.py

## Arquivos candidatos para validação

### Domínio e contrato

- domain/decision.py
- ATT/tests/test_decision.py

### Alertas e regras

- ATT/tests/test_fase7_alertas_decisao.py
- ATT/tests/test_fase7_snapshot_adapter.py

### Snapshot e entrada

- services/canonical_input_service.py
- services/structure_leg_rtd_enrichment_service.py
- repositories/market_snapshot_repository.py
- services/market_snapshot_selector.py

### UI e exibição

- UI/components/decisions_dark_panel.py
- UI/components/decisions_grid.py
- UI/components/filters_panel.py
- UI/components/details_panel.py
- UI/modern/dark_window.py

## Critérios de validação da Fase 7.2

A Fase 7.2 somente poderá avançar quando:

- o contrato mínimo de decisão estiver identificado;
- o contrato mínimo de alerta estiver identificado;
- os testes existentes forem classificados para reaproveitamento;
- não houver comando de execução real;
- não houver integração com broker;
- não houver alteração operacional de banco sem aprovação;
- a auditoria for atualizada;
- o commit for realizado.

## Testes sugeridos para primeira validação

Comando sugerido:

python -m pytest ATT/tests/test_decision.py ATT/tests/test_fase7_alertas_decisao.py ATT/tests/test_fase7_snapshot_adapter.py -q

## Decisão da Fase 7.2

A Fase 7.2 fica aberta como etapa de consolidação do contrato mínimo de decisão e alertas.

A implementação funcional permanece condicionada à validação dos contratos e dos testes existentes.

Marcador fim: FIM_FASE7_02_CONTRATO_MINIMO_DECISAO_ALERTAS_20260713
