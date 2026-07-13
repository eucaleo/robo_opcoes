# Fase 7.1 - Auditoria de rebaseline da Fase 7

Data: 13/07/2026

## Natureza

Auditoria manual de rebaseline baseada na varredura limpa da Fase 7.0.

Origem:

- fase7_00_varredura_limpa_adiantamentos_20260713.md
- fase7_00_varredura_limpa_adiantamentos_20260713.json

Esta etapa não implementa lógica nova.

Objetivo:

- classificar artefatos já existentes;
- separar itens aproveitáveis, ajustáveis, documentais, antecipados não validados, descartáveis ou bloqueados;
- impedir avanço de escopo para execução automática de ordens reais;
- preparar a base funcional segura para a Fase 7.

## Premissas obrigatórias

- A Fase 7 inicia por rebaseline dos artefatos encontrados.
- Nenhuma implementação nova deve ser feita antes da classificação manual.
- A execução automática de ordens reais permanece fora do escopo.
- Qualquer menção a broker, executor, roteamento automático ou automação real deve ser tratada como risco até validação explícita.
- Ocorrências de `ORDER BY`, `order`, `Ordem` e campos de ordenação podem ser falso positivo, mas devem ser marcadas como revisadas.
- Itens de eventos operacionais avançados, explicabilidade operacional e cadeia auditável final devem ser isolados se anteciparem fases futuras.

## Categorias de classificação

- APROVEITAVEL
- APROVEITAVEL_COM_AJUSTE
- DOCUMENTAL
- ANTECIPADO_NAO_VALIDADO
- DESCARTAR
- BLOQUEADO

## Resumo da Fase 7.0

- Arquivos rastreados no Git: 516
- Arquivos candidatos analisados: 313
- Arquivos com sinais relevantes: 142
- Arquivos com possível risco de escopo: 67
- Possíveis adiantamentos diretos da Fase 7: 9
- Possíveis suportes para Fase 7: 2
- Testes existentes relacionados: 48
- Contextos relacionados: 16
- Banco modificado: não
- Working tree esperado limpo: sim

## Decisão de abertura da Fase 7.1

A Fase 7.1 fica aberta como etapa de auditoria de rebaseline.

A frente de implementação permanece bloqueada até encerramento desta auditoria.

## Matriz principal de rebaseline

| Arquivo | Classificação Fase 7.0 | Decisão Fase 7.1 | Ação recomendada | Observação |
|---|---|---|---|---|
| UI/components/decisions_dark_panel.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL_COM_AJUSTE | Revisar contrato de dados e dependência de `get_decisions()` | Painel de decisões parece central para Fase 7, sem hits de risco |
| UI/components/decisions_grid.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL | Validar colunas, seleção e tags visuais | Grid direto de decisões, sem risco detectado |
| services/terminal_vwap_payoff_viewmodel_service.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL_COM_AJUSTE | Validar warnings como alertas não executores | Viewmodel já monta avisos operacionais úteis |
| services/structure_analysis_service.py | POSSIVEL_ADIANTAMENTO_FASE7 | ANTECIPADO_NAO_VALIDADO | Comparar com domínio canônico de decisão antes de reaproveitar | Calcula decisão a partir de payoff; pode colidir com contrato final da Fase 7 |
| services/derived_payoff_persistence.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL_COM_AJUSTE | Validar persistência derivada e atomicidade payoff/decisão | Útil, mas precisa garantir que não cria decisão fora do contrato validado |
| UI/modern/dark_window.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL_COM_AJUSTE | Revisar wiring decisão -> terminal VWAP | Integra decisão selecionada com terminal |
| UI/components/payoff_chart.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL_COM_AJUSTE | Validar uso apenas visual da decisão | Uso pequeno em gráfico/payoff |
| domain/refs/structure_ref.py | POSSIVEL_ADIANTAMENTO_FASE7 | DOCUMENTAL | Usar como referência de compatibilidade | Referências de rota/fase anterior e payloads |
| UI/components/filters_panel.py | POSSIVEL_ADIANTAMENTO_FASE7 | APROVEITAVEL | Validar filtro por decisão | Filtro simples e alinhado ao painel de decisões |
| services/structure_leg_rtd_enrichment_service.py | POSSIVEL_SUPORTE_FASE7 | APROVEITAVEL_COM_AJUSTE | Validar política de preço e snapshot | Suporte forte para enriquecer legs com RTD |
| services/canonical_input_service.py | POSSIVEL_SUPORTE_FASE7 | APROVEITAVEL_COM_AJUSTE | Revisar montagem de entrada canônica | Suporte provável para snapshot/entrada de decisão |

## Itens de risco de escopo - decisão inicial

| Arquivo | Classificação Fase 7.0 | Decisão Fase 7.1 | Ação recomendada | Observação |
|---|---|---|---|---|
| ATT/tests/test_operational_cross_validation_service.py | REVISAR_RISCO_ESCOPO | ANTECIPADO_NAO_VALIDADO | Isolar de Fase 7 funcional | Forte presença de alerta, decisão, explicabilidade e evento; pode pertencer a etapa operacional/auditável futura |
| UI/components/terminal_vwap_payoff_dark_panel.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar helpers de decisão e falsos positivos de `ORDER BY` | Muitos hits parecem SQL/ordenação, mas há helpers automáticos de decisão |
| ATT/tests/test_operational_decision_explanation_service.py | REVISAR_RISCO_ESCOPO | ANTECIPADO_NAO_VALIDADO | Manter fora do contrato inicial da Fase 7 | Explicabilidade operacional pode ser frente posterior |
| services/structure_events_service.py | REVISAR_RISCO_ESCOPO | BLOQUEADO | Não usar na Fase 7 inicial sem decisão explícita | Eventos operacionais parecem antecipar escopo futuro |
| repositories/structure_events_repository.py | REVISAR_RISCO_ESCOPO | BLOQUEADO | Não usar na Fase 7 inicial sem decisão explícita | O próprio trecho cita Fase 12 — Eventos operacionais |
| ATT/tests/test_auditable_chain_closure_service.py | REVISAR_RISCO_ESCOPO | ANTECIPADO_NAO_VALIDADO | Isolar como material de auditoria futura | Cadeia auditável final não deve comandar Fase 7 inicial |
| UI/models/ui_data.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Validar consultas e contrato de decisões | Risco provável por `ORDER BY`; contém acesso a decisões |
| services/calculation_orchestrator.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar separação entre calcular payoff, decisão e pipeline | Orquestrador útil, mas termo executor exige revisão |
| UI/main_window.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Validar botão/menu "Executar Pipeline" como execução interna, não ordem real | Risco por nomenclatura de executor/automação |
| services/derived_service.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar persistência de decisão derivada | Provável reaproveitamento com ajuste |
| UI/components/details_panel.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Validar renderização de decisão/eventos sem acionar fluxo operacional | Uso visual de decisão |
| ATT/tests/test_final_audit_report_service.py | REVISAR_RISCO_ESCOPO | DOCUMENTAL | Usar como evidência de não execução real | Texto reforça sem autorização para execução real |
| ATT/tests/test_final_executive_summary_service.py | REVISAR_RISCO_ESCOPO | DOCUMENTAL | Usar como evidência de fechamento sem execução real | Cadeia encerrada sem execução real |
| UI/components/terminal_vwap_payoff_panel.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Validar `order` como coluna/ordenação, não ordem real | Provável falso positivo |
| scripts/repair_app_db_consistency.py | REVISAR_RISCO_ESCOPO | BLOQUEADO | Não rodar na Fase 7 sem aprovação específica | Script com opção de remoção/alinhamento de dados |
| domain/decision.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Validar como domínio canônico de decisão | Deve ser candidato forte, mas revisar texto "aguardar execução" |
| ATT/tests/test_audit_trail_consolidation_service.py | REVISAR_RISCO_ESCOPO | DOCUMENTAL | Manter como referência de ausência de broker/execução | Útil para comprovar escopo negativo |
| ATT/tests/test_rota_atualizada_pos_fase6.py | REVISAR_RISCO_ESCOPO | DOCUMENTAL | Manter como guarda de escopo | Reforça que ordem real, broker e robô executor estão fora |
| repositories/market_snapshot_repository.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar falsos positivos de `ORDER BY` | Snapshot é suporte provável; risco parece SQL |
| repositories/rtd_option_quotes_repository.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar falsos positivos de `ORDER BY` | Suporte de dados RTD |
| ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Validar ações como UI interna, não execução real | Mensagens de "executar ação" podem ser falso positivo |
| repositories/structures_repository.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar falsos positivos de `ORDER BY` | Repositório estrutural necessário |
| services/rtd_option_quotes_intraday_candle_service.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar uso como contexto de mercado | Risco parece ordenação SQL |
| services/pricing_execution_persistence_service.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Confirmar que "execution" é execução de cálculo/preço, não ordem real | Persistência derivada pode ser útil, mas nome exige cuidado |
| scripts/verify_rtd_excel_resume.py | REVISAR_RISCO_ESCOPO | DOCUMENTAL | Não usar como motor da Fase 7 | Relacionado a RTD/BTG/Excel; broker aparece como fonte RTD |
| repositories/robo_legs_repository.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar nomenclatura histórica "robo" e campos de ordem | Pode ser repositório legado necessário |
| repositories/rtd_option_quotes_intraday_candle_repository.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar falsos positivos de `ORDER BY` | Suporte de candle |
| repositories/rtd_option_quotes_intraday_history_repository.py | REVISAR_RISCO_ESCOPO | APROVEITAVEL_COM_AJUSTE | Revisar falsos positivos de `ORDER BY` | Histórico intraday |

## Testes existentes relacionados - aproveitamento inicial

| Teste | Decisão Fase 7.1 | Observação |
|---|---|---|
| ATT/tests/test_fase7_alertas_decisao.py | APROVEITAVEL_COM_AJUSTE | Teste mais diretamente ligado a alertas e decisão da Fase 7 |
| ATT/tests/test_fase7_snapshot_adapter.py | APROVEITAVEL_COM_AJUSTE | Teste de adapter/snapshot com regras e decisão |
| ATT/tests/test_structure_analysis_service.py | APROVEITAVEL_COM_AJUSTE | Útil se o service for revalidado |
| ATT/tests/test_decision.py | APROVEITAVEL | Cobre domínio de decisão |
| ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | APROVEITAVEL_COM_AJUSTE | Cobre warnings do viewmodel |
| ATT/tests/test_ui_data_migration.py | APROVEITAVEL_COM_AJUSTE | Valida presença de decisões no modelo |
| ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py | APROVEITAVEL_COM_AJUSTE | Valida ligação decisão -> terminal |
| ATT/tests/test_orchestrator_run_methods.py | APROVEITAVEL_COM_AJUSTE | Útil após revisão do orquestrador |
| ATT/tests/test_terminal_vwap_payoff_app_service.py | APROVEITAVEL_COM_AJUSTE | Contexto de terminal/payoff/snapshot |
| ATT/tests/test_market_snapshot_provider.py | APROVEITAVEL | Suporte para snapshot |
| ATT/tests/test_market_snapshot_selector.py | APROVEITAVEL | Suporte para seleção de snapshot |
| ATT/tests/test_rtd_option_quotes_service.py | APROVEITAVEL_COM_AJUSTE | Informação parcial no inventário; revisar se aplicável |
| ATT/tests/test_fase7_rtd_option_quotes_service.py | APROVEITAVEL_COM_AJUSTE | Relacionado a Fase 7 e snapshot/RTD |

## Contextos relacionados

Os seguintes contextos não devem ser alterados nesta etapa, mas podem servir como apoio de entendimento:

- services/rtd_option_quotes_intraday_candle_chart_service.py
- services/terminal_vwap_payoff_app_service.py
- services/operational_data_status_service.py
- services/rtd_option_quotes_excel_sync.py
- infra/bootstrap_rtd_option_quotes_schema.py
- services/rtd_option_quotes_intraday_history_service.py
- domain/structure_metrics.py
- services/market_snapshot_selector.py
- services/rtd_option_quotes_excel_populator.py
- services/structure_market_input_assembler.py
- services/structure_input_mapper.py
- services/rtd_option_quotes_schema.py
- scripts/rtd_option_quotes_intraday_build_candles.py
- scripts/rtd_option_quotes_intraday_capture_once.py
- scripts/07_audit_snapshot_keys.py
- scripts/run_excel_rtd_option_quotes_snapshot_loop.py

Decisão:

- CONTEXTO_RELACIONADO
- Sem alteração
- Consultar apenas se necessário para validar entrada, snapshot, VWAP, candle, spread ou delta

## Frente funcional permitida após esta auditoria

Após encerramento da Fase 7.1, a Fase 7 poderá seguir por três trilhas controladas:

### Trilha A - Contrato de decisão e alerta

Arquivos candidatos:

- domain/decision.py
- ATT/tests/test_decision.py
- ATT/tests/test_fase7_alertas_decisao.py
- ATT/tests/test_fase7_snapshot_adapter.py

Objetivo:

- consolidar contrato de decisão;
- consolidar regras de alerta;
- garantir que a decisão não autoriza execução real.

### Trilha B - Entrada canônica e snapshot

Arquivos candidatos:

- services/canonical_input_service.py
- services/structure_leg_rtd_enrichment_service.py
- repositories/market_snapshot_repository.py
- services/market_snapshot_selector.py
- services/structure_market_input_assembler.py

Objetivo:

- validar entrada de mercado;
- validar snapshot;
- evitar dependência direta de UI;
- manter leitura sem execução operacional.

### Trilha C - UI de decisão

Arquivos candidatos:

- UI/components/decisions_dark_panel.py
- UI/components/decisions_grid.py
- UI/components/filters_panel.py
- UI/components/details_panel.py
- UI/modern/dark_window.py

Objetivo:

- exibir decisões;
- filtrar decisões;
- navegar da decisão para a estrutura;
- não criar comando de execução real.

## Bloqueios explícitos

Ficam bloqueados para implementação nesta etapa:

- envio automático de ordens reais;
- roteamento automático para broker;
- robô executor;
- integração operacional que envie ordens;
- execução real a partir de decisão;
- uso de eventos operacionais avançados como motor de decisão da Fase 7 sem nova autorização;
- scripts de reparo, prune, limpeza ou alteração de banco sem aprovação específica.

## Conclusão da Fase 7.1

A Fase 7.1 estabelece o rebaseline inicial da Fase 7.

Decisão consolidada:

- Existe base aproveitável para Fase 7.
- A base principal está em decisão, alertas, snapshot, VWAP/payoff e UI de decisões.
- Há antecipações relevantes que devem ser isoladas.
- Há muitos falsos positivos de risco por `ORDER BY`, `order` e nomenclatura histórica.
- A execução automática de ordens reais permanece fora do escopo.

## Próxima etapa recomendada

Abrir a Fase 7.2 com foco em contrato mínimo de decisão e alertas, sem alterar fluxo operacional real.

Sugestão de próximo artefato:

- fase7_02_contrato_minimo_decisao_alertas_20260713.md

Escopo sugerido para Fase 7.2:

- validar contrato de saída de decisão;
- validar contrato de alertas;
- validar adapter de snapshot;
- reaproveitar testes existentes;
- não implementar execução real;
- não integrar broker;
- não criar automação operacional.

Marcador fim: FIM_FASE7_01_AUDITORIA_REBASELINE_20260713
