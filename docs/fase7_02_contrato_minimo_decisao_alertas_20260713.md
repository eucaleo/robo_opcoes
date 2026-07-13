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

## Validação inicial executada

Data: 13/07/2026

Comando executado:

    python -m pytest ATT/tests/test_decision.py ATT/tests/test_fase7_alertas_decisao.py ATT/tests/test_fase7_snapshot_adapter.py -q

Resultado:

    12 passed in 0.39s

Interpretação:

- O domínio de decisão possui baseline testável.
- Os testes iniciais de alertas da Fase 7 estão reaproveitáveis.
- O adapter de snapshot da Fase 7 possui baseline funcional.
- Não houve evidência de execução automática de ordens reais.
- Não houve integração com broker.
- Não houve alteração de banco.

Decisão:

A Fase 7.2 pode avançar para auditoria técnica dos contratos reais existentes em código, mantendo bloqueada qualquer implementação de execução operacional real.


## Auditoria de contratos reais existentes

Data: 13/07/2026

Arquivos auditados:

    domain/decision.py
    ATT/tests/test_decision.py
    ATT/tests/test_fase7_alertas_decisao.py
    ATT/tests/test_fase7_snapshot_adapter.py

Resultado da auditoria focada:

    Arquivos auditados: 4
    Ocorrências úteis para Fase 7: 127
    Ocorrências de risco de escopo nos arquivos focados: 0

Classificação técnica do contrato de decisão:

    Função: compute_decision_from_inputs
    Natureza: decisão a partir de P&L atual, P&L máximo, DTE mínimo, spread médio e thresholds.
    Saída: dicionário explicável com decision, level, ratio, pl_pct_of_max, why_json, why e alternatives.
    Execução real: ausente.

    Função: compute_decision_from_payoff
    Natureza: decisão a partir de dicionário de payoff canônico.
    Comportamento: trata payoff vazio ou inválido como HOLD com justificativa de erro.
    Execução real: ausente.

    Função: compute_decision_from_contract
    Natureza: entrada canônica via CanonicalStructureMarketInput.
    Comportamento: delega para decisão por payoff quando payoff é fornecido, ou por inputs quando não é.
    Execução real: ausente.

Classificação técnica do contrato de alertas:

    Entidade: SnapshotMercado
    Natureza: snapshot local de mercado usado para avaliação somente leitura.

    Entidade: ParametrosAlerta
    Natureza: parâmetros locais para regras de alerta, como spread máximo, volume mínimo e delta relevante de payoff.

    Função: avaliar_snapshot
    Natureza: avalia snapshot e gera alertas explicáveis.
    Sinais cobertos pelos testes: preço acima do VWAP, cruzamento de alta do VWAP, spread anormal, liquidez baixa, payoff alterado e estrutura favorável.
    Execução real: bloqueada pelo contrato de decisão dos testes, com permite_execucao falso.

Classificação técnica do contrato de adapter:

    Função: snapshot_mercado_from_rtd_option_quote
    Natureza: converte linha de cotação RTD em SnapshotMercado local.

    Função: avaliar_rtd_option_quote
    Natureza: converte cotação RTD, avalia snapshot e preserva timestamp local.

    Função: snapshot_mercado_from_leg_market_snapshot
    Natureza: converte objeto similar a leg market snapshot sem depender diretamente do domínio operacional.

Bloqueios técnicos observados:

    Nenhuma ocorrência de envio de ordem real nos arquivos focados.
    Nenhuma ocorrência de broker nos arquivos focados.
    Nenhuma ocorrência de executor operacional nos arquivos focados.
    Nenhuma ocorrência de roteamento de ordem nos arquivos focados.
    Nenhuma dependência de Excel COM nos módulos testados de alerta e adapter.
    Nenhuma dependência de subprocesso nos módulos testados de alerta e adapter.
    Nenhuma alteração de banco envolvida.

Conclusão da classificação:

    O contrato mínimo existente da Fase 7.2 é de decisão explicável, alertas locais e adapter de snapshot.
    A base atual é compatível com operação somente leitura.
    A base atual não implementa execução automática real.
    A base atual não integra broker.
    A base atual pode avançar para fechamento documental da Fase 7.2 antes de qualquer ajuste em código.


## Fechamento formal da Fase 7.2

Data: 13/07/2026

Resumo final:

    A Fase 7.2 identificou e classificou o contrato mínimo real existente para decisão, alertas e adapter de snapshot.
    A auditoria focada confirmou ausência de termos de risco nos arquivos diretamente auditados.
    A validação inicial de testes foi executada com sucesso.
    A documentação foi ajustada para manter blocos indentados sem uso de crases.
    A classificação técnica foi registrada em documento versionado.

Evidências versionadas:

    Documento de auditoria e rebaseline da Fase 7.1.
    Documento de contrato mínimo da Fase 7.2.
    Registro de validação inicial com 12 testes passando.
    Registro de auditoria focada com 4 arquivos auditados.
    Registro de classificação técnica dos contratos mínimos existentes.

Decisão final:

    A Fase 7.2 está documentalmente concluída.
    A base pode avançar para a Fase 7.3.
    A Fase 7.3 deve permanecer restrita a testes, documentação ou ajustes mínimos de contrato somente leitura.
    Continua bloqueada qualquer implementação de execução real, broker, robô executor, roteamento operacional ou alteração de banco.

Marcador final:

    FIM_FASE7_02_CONTRATO_MINIMO_DECISAO_ALERTAS_20260713

