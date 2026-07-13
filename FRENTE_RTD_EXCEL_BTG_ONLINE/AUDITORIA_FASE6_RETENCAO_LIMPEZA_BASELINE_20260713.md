# Auditoria técnica inicial da Fase 6 - Retenção, limpeza e consolidação

Marcador inicio: INICIO_AUDITORIA_FASE6_RETENCAO_LIMPEZA_BASELINE_20260713

Data: 13/07/2026

Natureza: auditoria inicial, sem alteração destrutiva de dados

## Objetivo

Iniciar a Fase 6 com levantamento técnico do estado atual do banco, dos schemas, dos índices, das tabelas relacionadas a snapshot, histórico intraday e candles, além de identificar arquivos candidatos já existentes para retenção, limpeza, consolidação e manutenção.

Esta auditoria não implementa limpeza de dados, não remove registros, não executa compactação e não altera o banco operacional.

## Arquitetura preservada

    Corretora / RTD -> Excel LISTA_RTD.xlsm aberto -> Coletor Python online -> Snapshot SQLite -> Histórico Intraday -> Candles -> UI / Estruturas / Alertas

## Status de entrada

    Fase 1: encerrada
    Fase 2: encerrada
    Fase 3: encerrada
    Fase 4: encerrada
    Fase 5: encerrada
    Fase 6: iniciada
    Fase 7: não encerrada

## Banco auditado

    Caminho: dados\app.db
    Existe: sim
    Tamanho em bytes: 1548288

## Tabelas e views identificadas

    - table: payoff_curve_points
    - table: pricing_executions
    - table: rtd_option_quotes
    - table: rtd_option_quotes_intraday_candles
    - table: rtd_option_quotes_intraday_history
    - table: rtd_underlying_quotes
    - table: sqlite_sequence
    - table: structure_audit_log
    - table: structure_decisions
    - table: structure_events
    - table: structure_leg_snapshots
    - table: structure_legs
    - table: structure_snapshots
    - table: structures

## Tabelas alvo da Fase 6

### rtd_option_quotes

    Status: encontrada
    Linhas atuais: 10

    Colunas:
        - id | tipo: INTEGER | notnull: 0 | pk: 1
        - codigo_opcao | tipo: TEXT | notnull: 1 | pk: 0
        - ativo_base | tipo: TEXT | notnull: 0 | pk: 0
        - call_put | tipo: TEXT | notnull: 0 | pk: 0
        - strike | tipo: REAL | notnull: 0 | pk: 0
        - vencimento | tipo: TEXT | notnull: 0 | pk: 0
        - ultimo_preco | tipo: REAL | notnull: 0 | pk: 0
        - ultima_quantidade | tipo: REAL | notnull: 0 | pk: 0
        - bid | tipo: REAL | notnull: 0 | pk: 0
        - ask | tipo: REAL | notnull: 0 | pk: 0
        - volume | tipo: REAL | notnull: 0 | pk: 0
        - iv | tipo: REAL | notnull: 0 | pk: 0
        - delta | tipo: REAL | notnull: 0 | pk: 0
        - gamma | tipo: REAL | notnull: 0 | pk: 0
        - theta | tipo: REAL | notnull: 0 | pk: 0
        - vega | tipo: REAL | notnull: 0 | pk: 0
        - source | tipo: TEXT | notnull: 1 | pk: 0
        - raw_json | tipo: TEXT | notnull: 0 | pk: 0
        - updated_at | tipo: TEXT | notnull: 1 | pk: 0
        - created_at | tipo: TEXT | notnull: 1 | pk: 0
        - vwap | tipo: REAL | notnull: 0 | pk: 0

    Índices:
        - idx_rtd_option_quotes_ativo_base | unique: 0 | origin: c
            - coluna: ativo_base
        - ux_rtd_option_quotes_codigo_opcao_normalized | unique: 1 | origin: c
            - coluna: 
        - idx_rtd_option_quotes_codigo_opcao | unique: 0 | origin: c
            - coluna: codigo_opcao
        - sqlite_autoindex_rtd_option_quotes_1 | unique: 1 | origin: u
            - coluna: codigo_opcao

### rtd_option_quotes_intraday_history

    Status: encontrada
    Linhas atuais: 60

    Colunas:
        - id | tipo: INTEGER | notnull: 0 | pk: 1
        - captured_at | tipo: TEXT | notnull: 1 | pk: 0
        - codigo_opcao | tipo: TEXT | notnull: 1 | pk: 0
        - bid | tipo: REAL | notnull: 0 | pk: 0
        - ask | tipo: REAL | notnull: 0 | pk: 0
        - last | tipo: REAL | notnull: 0 | pk: 0
        - vwap | tipo: REAL | notnull: 0 | pk: 0
        - volume | tipo: REAL | notnull: 0 | pk: 0
        - source_updated_at | tipo: TEXT | notnull: 0 | pk: 0
        - raw_payload_json | tipo: TEXT | notnull: 1 | pk: 0
        - created_at | tipo: TEXT | notnull: 1 | pk: 0

    Índices:
        - idx_rtd_option_quotes_intraday_history_captured_at | unique: 0 | origin: c
            - coluna: captured_at
        - idx_rtd_option_quotes_intraday_history_codigo_captured_at | unique: 0 | origin: c
            - coluna: codigo_opcao
            - coluna: captured_at

### rtd_option_quotes_intraday_candles

    Status: encontrada
    Linhas atuais: 110

    Colunas:
        - id | tipo: INTEGER | notnull: 0 | pk: 1
        - interval_minutes | tipo: INTEGER | notnull: 1 | pk: 0
        - bucket_start | tipo: TEXT | notnull: 1 | pk: 0
        - symbol | tipo: TEXT | notnull: 1 | pk: 0
        - open_price | tipo: REAL | notnull: 0 | pk: 0
        - high_price | tipo: REAL | notnull: 0 | pk: 0
        - low_price | tipo: REAL | notnull: 0 | pk: 0
        - close_price | tipo: REAL | notnull: 0 | pk: 0
        - vwap | tipo: REAL | notnull: 0 | pk: 0
        - bid | tipo: REAL | notnull: 0 | pk: 0
        - ask | tipo: REAL | notnull: 0 | pk: 0
        - spread | tipo: REAL | notnull: 0 | pk: 0
        - volume_delta | tipo: REAL | notnull: 0 | pk: 0
        - updates_count | tipo: INTEGER | notnull: 0 | pk: 0
        - price_source | tipo: TEXT | notnull: 0 | pk: 0
        - created_at | tipo: TEXT | notnull: 1 | pk: 0
        - updated_at | tipo: TEXT | notnull: 1 | pk: 0

    Índices:
        - idx_rtd_intraday_candles | unique: 0 | origin: c
            - coluna: symbol
            - coluna: interval_minutes
            - coluna: bucket_start
        - sqlite_autoindex_rtd_option_quotes_intraday_candles_1 | unique: 1 | origin: u
            - coluna: interval_minutes
            - coluna: bucket_start
            - coluna: symbol

### system_snapshots

    Status: não encontrada

## Arquivos candidatos encontrados

    - ATT/tests/README_RTD_OPTION_QUOTES_INTRADAY_HISTORY_TESTS.md
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - ATT/tests/check_cleanup_residuals.py
        - correspondência no nome: cleanup, clean
        - correspondência no conteúdo: cleanup, clean, limpeza
    - ATT/tests/check_structures.py
        - correspondência no conteúdo: consolid
    - ATT/tests/run_all_checks.py
        - correspondência no conteúdo: cleanup, clean
    - ATT/tests/test_audit_trail_consolidation_service.py
        - correspondência no nome: consolid
        - correspondência no conteúdo: consolid
    - ATT/tests/test_auditable_chain_closure_service.py
        - correspondência no conteúdo: consolid
    - ATT/tests/test_bd_unico_absorcao_funcional.py
        - correspondência no conteúdo: consolid
    - ATT/tests/test_database_retention_inventory_service.py
        - correspondência no nome: retention
        - correspondência no conteúdo: retention, intraday, history
    - ATT/tests/test_database_retention_simulation_service.py
        - correspondência no nome: retention
        - correspondência no conteúdo: retention, retencao
    - ATT/tests/test_final_audit_report_service.py
        - correspondência no conteúdo: consolid, consolidacao
    - ATT/tests/test_final_executive_summary_service.py
        - correspondência no conteúdo: consolid
    - ATT/tests/test_operational_data_status_service.py
        - correspondência no conteúdo: intraday, candle, candles, history
    - ATT/tests/test_operational_observability_presentation.py
        - correspondência no conteúdo: retention, retencao
    - ATT/tests/test_operational_observability_query.py
        - correspondência no conteúdo: retention, retencao
    - ATT/tests/test_operational_observability_service.py
        - correspondência no conteúdo: retention, retencao
    - ATT/tests/test_rtd_option_quotes_intraday_build_candles_command.py
        - correspondência no nome: intraday, candle, candles
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - ATT/tests/test_rtd_option_quotes_intraday_candle_guardrails.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - ATT/tests/test_rtd_option_quotes_intraday_candle_repository.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - ATT/tests/test_rtd_option_quotes_intraday_candle_service.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - ATT/tests/test_rtd_option_quotes_intraday_candle_timezone.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - ATT/tests/test_rtd_option_quotes_intraday_capture_once_command.py
        - correspondência no nome: intraday
        - correspondência no conteúdo: intraday
    - ATT/tests/test_rtd_option_quotes_intraday_capture_service.py
        - correspondência no nome: intraday
        - correspondência no conteúdo: intraday, history
    - ATT/tests/test_rtd_option_quotes_intraday_history_repository.py
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, history
    - ATT/tests/test_rtd_option_quotes_intraday_history_schema_contract.py
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, history
    - ATT/tests/test_rtd_option_quotes_intraday_price_mapping_regression.py
        - correspondência no nome: intraday
        - correspondência no conteúdo: intraday, candle, candles, history
    - ATT/tests/test_ui_intraday_candle_chart_consumption.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - ATT/tests/test_ui_modern_moderndarkui_contract.py
        - correspondência no conteúdo: clean
    - FRENTE_RTD_EXCEL_BTG_ONLINE/00_EXCEL_RTD_BTG_ONLINE.md
        - correspondência no conteúdo: limpeza, consolid, intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/01_README_DA_FRENTE.md
        - correspondência no conteúdo: limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/02_AUDITORIA_INICIAL.md
        - correspondência no conteúdo: intraday
    - FRENTE_RTD_EXCEL_BTG_ONLINE/03_PLANO_DE_FASES.md
        - correspondência no conteúdo: consolid, intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/05_CHECKLIST_TESTES.md
        - correspondência no conteúdo: candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/06_DECISOES_TECNICAS.md
        - correspondência no conteúdo: candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/07_LIMPEZA_ENCERRAMENTO.md
        - correspondência no nome: limpeza
        - correspondência no conteúdo: limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/09_PROXIMA_ACAO_FASE1.md
        - correspondência no conteúdo: intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/12_FASE2_SNAPSHOT_ONLINE.md
        - correspondência no conteúdo: intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/14_STATUS_ROTA_ATUAL_RTD_EXCEL.md
        - correspondência no conteúdo: retencao, manutencao, intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/16_FECHAMENTO_FASE2_SNAPSHOT_RTD_ONLINE.md
        - correspondência no conteúdo: intraday, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/17_AUDITORIA_PRE_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/18_CONTRATO_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/19_MAPEAMENTO_PASTAS_GIT_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/20_REVISAO_PADROES_PRE_IMPL_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/21_IMPLEMENTACAO_MINIMA_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/22_AUDITORIA_POS_IMPL_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: intraday, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/23_IMPLEMENTACAO_FASE3_1_CAPTURA_MANUAL_UNICA.md
        - correspondência no conteúdo: intraday, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/24_AUDITORIA_REBASELINE_FASE3_HISTORICO_INTRADAY.md
        - correspondência no nome: intraday, historico
        - correspondência no conteúdo: retencao, consolid, consolidacao, intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/24_IMPLEMENTACAO_MINIMA_FASE4_MOTOR_CANDLES.md
        - correspondência no nome: candle, candles
        - correspondência no conteúdo: intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/28_IMPLEMENTACAO_FASE5_1_RESUMO_OPERACIONAL_DADOS.md
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/29_AUDITORIA_PRE_FASE5_2_INTEGRACAO_UI.md
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/31_COMPARACAO_EVOLUCAO_PLANO_VS_GIT.md
        - correspondência no conteúdo: retencao, limpeza, consolid, consolidacao, intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/32_AUDITORIA_POS_COMPARACAO_FASE5_3_VALIDACAO_UI.md
        - correspondência no conteúdo: retencao, limpeza, consolid, consolidacao, manutencao, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/33_VALIDACAO_FASE5_3_UI_STATUS_OPERACIONAL.md
        - correspondência no conteúdo: retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/34_AUDITORIA_FECHAMENTO_PARCIAL_FASE5_UI_OPERACIONAL.md
        - correspondência no conteúdo: retencao, limpeza, consolid, consolidacao, manutencao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/35_AUDITORIA_PRE_FASE6_RETENCAO_LIMPEZA_CONSOLIDACAO.md
        - correspondência no nome: retencao, limpeza, consolid, consolidacao
        - correspondência no conteúdo: retencao, limpeza, consolid, consolidacao, manutencao, intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/36_IMPLEMENTACAO_FASE6_1_INVENTARIO_BANCO_RETENCAO.md
        - correspondência no nome: retencao
        - correspondência no conteúdo: retention, retencao, limpeza, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/37_AUDITORIA_FASE6_2_POLITICA_MINIMA_RETENCAO.md
        - correspondência no nome: retencao
        - correspondência no conteúdo: retencao, limpeza, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/38_IMPLEMENTACAO_FASE6_3_RETENCAO_MODO_SIMULADO.md
        - correspondência no nome: retencao
        - correspondência no conteúdo: retention, retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/39_AUDITORIA_POS_FASE6_3_RETENCAO_MODO_SIMULADO.md
        - correspondência no nome: retencao
        - correspondência no conteúdo: retention, retencao, limpeza, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/40_AUDITORIA_FECHAMENTO_PARCIAL_FASE6_RETENCAO_SIMULADA.md
        - correspondência no nome: retencao
        - correspondência no conteúdo: retention, retencao, limpeza, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/41_AUDITORIA_TRANSICAO_POS_FASE6_PROXIMA_FRENTE_OPERACIONAL.md
        - correspondência no conteúdo: retention, retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/42_AUDITORIA_PRE_FASE7_OBSERVABILIDADE_OPERACIONAL.md
        - correspondência no conteúdo: retention, retencao, limpeza, consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/43_IMPLEMENTACAO_FASE7_1_OBSERVABILIDADE_OPERACIONAL_BASE.md
        - correspondência no conteúdo: retention, retencao, limpeza, vacuum
    - FRENTE_RTD_EXCEL_BTG_ONLINE/44_AUDITORIA_POS_FASE7_1_OBSERVABILIDADE_OPERACIONAL_BASE.md
        - correspondência no conteúdo: retention, retencao, limpeza, consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/45_AUDITORIA_PRE_FASE7_2_CONTRATO_APRESENTACAO_OBSERVABILIDADE.md
        - correspondência no conteúdo: retention, retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/46_IMPLEMENTACAO_FASE7_2_CONTRATO_APRESENTACAO_OBSERVABILIDADE.md
        - correspondência no conteúdo: retention, retencao, limpeza, vacuum
    - FRENTE_RTD_EXCEL_BTG_ONLINE/47_AUDITORIA_POS_FASE7_2_CONTRATO_APRESENTACAO_OBSERVABILIDADE.md
        - correspondência no conteúdo: retention, retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/48_AUDITORIA_PRE_FASE7_3_EXPOSICAO_CONTROLADA_OBSERVABILIDADE.md
        - correspondência no conteúdo: retention, retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/49_IMPLEMENTACAO_FASE7_3_EXPOSICAO_CONTROLADA_OBSERVABILIDADE.md
        - correspondência no conteúdo: retention, retencao, limpeza
    - FRENTE_RTD_EXCEL_BTG_ONLINE/50_AUDITORIA_POS_FASE7_3_EXPOSICAO_CONTROLADA_OBSERVABILIDADE.md
        - correspondência no conteúdo: retention, retencao, limpeza, consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/51_FECHAMENTO_FASE7_OBSERVABILIDADE_OPERACIONAL.md
        - correspondência no conteúdo: retention, retencao, limpeza, consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/52_AUDITORIA_DE_ROTA_POS_FASE7_RTD_EXCEL_ONLINE.md
        - correspondência no conteúdo: retention, retencao, limpeza, consolid, consolidacao, intraday, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/53_AUDITORIA_PRE_FASE8_EXCEL_RTD_ONLINE_CONTROLADO.md
        - correspondência no conteúdo: retention, limpeza, candle, candles, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/54_IMPLEMENTACAO_FASE8_1_CONTRATO_RTD_OPTION_QUOTES.md
        - correspondência no conteúdo: retention
    - FRENTE_RTD_EXCEL_BTG_ONLINE/56_FECHAMENTO_INTEGRAL_FASE7_RECONCILIADA.md
        - correspondência no conteúdo: consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/58_IMPLEMENTACAO_FASE7R2_R3_CONTRATO_MOTOR_ALERTAS_DECISAO.md
        - correspondência no conteúdo: consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/62_AUDITORIA_POS_FASE7R4_DECISAO_OPERACIONAL_EXPLICAVEL.md
        - correspondência no conteúdo: clean
    - FRENTE_RTD_EXCEL_BTG_ONLINE/65_AUDITORIA_POS_FASE7R5_VALIDACAO_CRUZADA_EXPLICACOES_ALERTAS.md
        - correspondência no conteúdo: clean, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/66_CONTRATO_FASE7R6_CONSOLIDACAO_TRILHA_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES.md
        - correspondência no nome: consolid, consolidacao
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/67_IMPLEMENTACAO_FASE7R6_CONSOLIDACAO_TRILHA_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES.md
        - correspondência no nome: consolid, consolidacao
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/68_AUDITORIA_POS_FASE7R6_CONSOLIDACAO_TRILHA_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES.md
        - correspondência no nome: consolid, consolidacao
        - correspondência no conteúdo: clean, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/69_CONTRATO_FASE7R7_RELATORIO_FINAL_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES_VALIDACOES.md
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/70_IMPLEMENTACAO_FASE7R7_RELATORIO_FINAL_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES_VALIDACOES.md
        - correspondência no conteúdo: consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/71_AUDITORIA_POS_FASE7R7_RELATORIO_FINAL_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES_VALIDACOES.md
        - correspondência no conteúdo: clean, consolid
    - FRENTE_RTD_EXCEL_BTG_ONLINE/72_CONTRATO_FASE7R8_ENCERRAMENTO_CADEIA_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES_VALIDACOES_RELATORIOS.md
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/73_IMPLEMENTACAO_FASE7R8_ENCERRAMENTO_CADEIA_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES_VALIDACOES_RELATORIOS.md
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/74_AUDITORIA_POS_FASE7R8_ENCERRAMENTO_CADEIA_AUDITAVEL_ALERTAS_DECISOES_EXPLICACOES_VALIDACOES_RELATORIOS.md
        - correspondência no conteúdo: clean, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/75_CONTRATO_FASE7R9_SUMARIO_EXECUTIVO_FINAL_CADEIA_AUDITAVEL_SOMENTE_LEITURA.md
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/76_IMPLEMENTACAO_FASE7R9_SUMARIO_EXECUTIVO_FINAL_CADEIA_AUDITAVEL_SOMENTE_LEITURA.md
        - correspondência no conteúdo: clean, consolid, manutencao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/77_AUDITORIA_POS_FASE7R9_SUMARIO_EXECUTIVO_FINAL_CADEIA_AUDITAVEL_SOMENTE_LEITURA.md
        - correspondência no conteúdo: clean, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/78_ENCERRAMENTO_FORMAL_FASE7R9_SUMARIO_EXECUTIVO_FINAL_CADEIA_AUDITAVEL_SOMENTE_LEITURA.md
        - correspondência no conteúdo: consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/79_CONSOLIDACAO_FINAL_SEQUENCIA_7R_CADEIA_AUDITAVEL_SOMENTE_LEITURA.md
        - correspondência no nome: consolid, consolidacao
        - correspondência no conteúdo: clean, consolid, consolidacao
    - FRENTE_RTD_EXCEL_BTG_ONLINE/80_CONCLUSAO_DE_ETAPA_E_DIRETRIZ_DE_REFATORACAO_RTD_EXCEL_BTG_ONLINE.md
        - correspondência no conteúdo: consolid, intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_RTD_EXCEL_BTG_ONLINE.md
        - correspondência no conteúdo: limpeza, consolid, intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_RTD_ONLINE_LEGADA.md
        - correspondência no conteúdo: consolid, consolidacao, intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/EXCEL_RTD_BTG_ONLINE REESTRUTURADO.md
        - correspondência no conteúdo: limpeza, consolid, intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/auditoria_fase4_ui_candles.md
        - correspondência no nome: candle, candles
        - correspondência no conteúdo: intraday, candle, candles
    - FRENTE_RTD_EXCEL_BTG_ONLINE/auditoria_fase5_mapa_lacunas_ui_operacional.md
        - correspondência no conteúdo: retention, cleanup, clean, consolid, intraday, candle, candles, history
    - FRENTE_RTD_EXCEL_BTG_ONLINE/auditoria_fase5_precheck_ui_operacional.md
        - correspondência no conteúdo: retention, cleanup, clean, consolid, intraday, candle, candles, history, historico
    - FRENTE_RTD_EXCEL_BTG_ONLINE/resumo_desenvolvimento_fase4_ui_candles.md
        - correspondência no nome: candle, candles
        - correspondência no conteúdo: intraday, candle, candles
    - UI/components/terminal_vwap_payoff_dark_panel.py
        - correspondência no conteúdo: clean, intraday, candle, candles, history, historico
    - UI/models/ui_data.py
        - correspondência no conteúdo: consolid
    - repositories/README_RTD_OPTION_QUOTES_INTRADAY_HISTORY.md
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - repositories/rtd_option_quotes_intraday_candle_repository.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - repositories/rtd_option_quotes_intraday_history_repository.py
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, history, historico
    - repositories/rtd_option_quotes_repository.py
        - correspondência no conteúdo: clean, intraday, historico
    - repositories/structures_repository.py
        - correspondência no conteúdo: historico
    - repositories/ui_data_table_candidates.py
        - correspondência no conteúdo: consolid
    - scripts/09g_cleanup_robo_legs_repository.py
        - correspondência no nome: cleanup, clean
        - correspondência no conteúdo: cleanup, clean
    - scripts/09h_restore_robo_legs_cleanup_backup.py
        - correspondência no nome: cleanup, clean
        - correspondência no conteúdo: cleanup, clean
    - scripts/__init__.py
        - correspondência no conteúdo: maintenance
    - scripts/import_rtd_option_quotes_wide_csv.py
        - correspondência no conteúdo: clean
    - scripts/purge_derived_snapshots.py
        - correspondência no conteúdo: consolid
    - scripts/refresh_rtd_symbol_to_option_quotes.py
        - correspondência no conteúdo: consolid
    - scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
        - correspondência no conteúdo: clean
    - scripts/rtd_option_quotes_intraday_build_candles.py
        - correspondência no nome: intraday, candle, candles
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - scripts/rtd_option_quotes_intraday_capture_once.py
        - correspondência no nome: intraday
        - correspondência no conteúdo: intraday, history, historico
    - scripts/run_derived_pipeline.py
        - correspondência no conteúdo: cleanup, clean
    - services/README_RTD_OPTION_QUOTES_INTRADAY_HISTORY.md
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, candle, candles, history, historico
    - services/canonical_input_service.py
        - correspondência no conteúdo: clean
    - services/derived_service.py
        - correspondência no conteúdo: cleanup, clean, consolid
    - services/legacy_robo_legs_fallback.py
        - correspondência no conteúdo: clean
    - services/operational_data_status_service.py
        - correspondência no conteúdo: intraday, candle, candles, history
    - services/pricing_execution_app_service.py
        - correspondência no conteúdo: consolid
    - services/pricing_payload_adapter.py
        - correspondência no conteúdo: clean
    - services/rtd_option_quotes_intraday_candle_chart_service.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles
    - services/rtd_option_quotes_intraday_candle_service.py
        - correspondência no nome: intraday, candle
        - correspondência no conteúdo: intraday, candle, candles, history
    - services/rtd_option_quotes_intraday_history_service.py
        - correspondência no nome: intraday, history
        - correspondência no conteúdo: intraday, history, historico
    - services/structure_input_mapper.py
        - correspondência no conteúdo: clean
    - services/terminal_vwap_payoff_viewmodel_service.py
        - correspondência no conteúdo: consolid

## Leitura preliminar

A Fase 6 deve partir do banco real e dos contratos existentes, sem duplicar tabelas e sem alterar o fluxo aceito das fases anteriores.

Pontos que devem ser confirmados antes de qualquer implementação destrutiva:

    - política de retenção para histórico intraday bruto;
    - política de retenção para candles de 1 minuto;
    - política futura para candles de 5 minutos, 15 minutos e diário;
    - existência ou criação de snapshot final do dia;
    - modo dry-run obrigatório para limpeza;
    - preservação de candles consolidados;
    - ausência de VACUUM automático sem controle explícito;
    - testes integrados com Fases 1 a 5 antes do encerramento.

## Decisão desta auditoria inicial

A Fase 6 está iniciada em modo de auditoria e baseline.

Nenhuma rotina de limpeza deve ser aplicada antes da definição dos contratos de retenção, dry-run, preservação de candles e snapshot final do dia.

Marcador fim: FIM_AUDITORIA_FASE6_RETENCAO_LIMPEZA_BASELINE_20260713
