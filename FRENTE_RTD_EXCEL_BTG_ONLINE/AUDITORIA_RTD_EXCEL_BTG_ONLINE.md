# Auditoria RTD Excel BTG Online

## Objetivo

Registrar a evolução da frente RTD Excel BTG Online conforme as regras do projeto.

## Regras validadas nesta etapa

- Excel RTD tratado como ponte temporária.
- Dados permanentes devem ficar no SQLite.
- Artefatos gerados não devem ser versionados.
- Arquivos grandes não devem entrar no repositório.
- Toda alteração deve ter teste automatizado.
- Toda alteração concluída e testada deve ser commitada.

## Estado atual

- Bridge RTD_OPTION_QUOTES criado.
- Testes da frente RTD executados com sucesso.
- Suite ATT executada com sucesso.
- Push realizado para origin/refactor/bd-unico-appdb.
- Detectado alerta do GitHub para arquivos grandes em output.
- Criado guardrail para impedir versionamento de artefatos gerados e arquivos acima de 50 MB.

## Testes esperados

- ATT/tests/test_repository_generated_artifacts_guardrail.py
- Suite ATT completa

## Fase 1A - Status RTD Excel Online

### Objetivo

Criar uma camada backend para verificar o estado da conexão Excel RTD antes de integrar com a UI.

### Itens cobertos

- Verificação de disponibilidade do pywin32.
- Verificação de Excel aberto via COM.
- Verificação de workbook LISTA_RTD.xlsm aberto.
- Verificação da aba RTD_OPTION_QUOTES.
- Validação dos cabeçalhos obrigatórios por nome.
- Aceitação de colunas movidas na planilha.
- Status consolidado por objeto reutilizável.

### Regra operacional validada

O sistema não depende da posição física fixa das colunas. A validação usa os cabeçalhos da linha 1.

### Teste criado

- ATT/tests/test_excel_rtd_connection_status.py

## Fase 1B - Payload de Status RTD Excel para UI

### Objetivo

Criar uma camada de apresentação backend para converter o status técnico RTD Excel em payload consumível pela UI.

### Itens cobertos

- Status consolidado em view model.
- Payload serializável em dict.
- Severidade operacional: ok, warning ou error.
- Título amigável para exibição.
- Mensagem técnica preservada.
- Checks individuais para pywin32, Excel, workbook, aba e cabeçalhos.
- Injeção de checker para teste sem Excel real.

### Regra operacional validada

A UI não deve acessar COM diretamente. A UI deve consumir um payload pronto produzido pelo backend.

### Teste criado

- ATT/tests/test_excel_rtd_connection_status_presenter.py

## Fase 1C - Menu Ajuda com Status RTD Excel

### Objetivo

Conectar o payload backend de status RTD Excel à UI moderna por meio do menu Ajuda.

### Itens cobertos

- Inclusão do item Ajuda > Status RTD Excel.
- Chamada ao backend `get_excel_rtd_status_payload`.
- Exibição via messagebox conforme severidade:
  - ok: showinfo
  - warning: showwarning
  - error: showerror
- Formatação amigável do resumo operacional.
- Teste operacional com UI real em subprocess limpo e RTD/Excel real ativo.

### Regra operacional validada

A UI consome apenas o payload pronto do backend e não acessa COM diretamente. A validação operacional usa Excel/RTD real ativo.

### Teste criado

- ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py
## Fase 1 - Detecção Excel COM e validação da planilha

Data: 2026-07-10

Resultado validado:

- O arquivo C:\Users\eucal\projeto\LISTA_RTD.xlsm foi aberto via COM.
- O Python passou a enxergar o workbook corretamente.
- A aba RTD_OPTION_QUOTES foi encontrada.
- Os cabeçalhos obrigatórios foram encontrados.
- O teste ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py passou.

Evidência:

Workbooks: 1
LISTA_RTD.xlsm C:\Users\eucal\projeto\LISTA_RTD.xlsm

Cabeçalhos encontrados:

codigo_opcao
ativo_base
call_put
strike
vencimento
ultimo_preco
ultima_quantidade
bid
ask
volume
iv
delta
gamma
theta
vega
vwap

Teste executado:

pytest ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py -q

Resultado:

1 passed in 1.76s

Conclusão:

A integração COM funciona quando o LISTA_RTD.xlsm é aberto pela instância Excel controlada pelo Python. A próxima melhoria necessária é automatizar no sistema a abertura ou reutilização correta desse workbook.
---

## Registro documental — Encerramento e refatoração

**Data:** 10/07/2026  
**Branch:** feature/rtd-excel-online-fase1  
**Tipo:** Registro documental e refatoração de rota

### Arquivos registrados

- 80_CONCLUSAO_DE_ETAPA_E_DIRETRIZ_DE_REFATORACAO_RTD_EXCEL_BTG_ONLINE.md
- EXCEL_RTD_BTG_ONLINE REESTRUTURADO.md

### Resultado

- Documento 80 criado para encerramento da etapa anterior.
- Documento reestruturado criado para orientar as fases daqui pra frente.
- Arquitetura principal consolidada como Excel RTD vivo contínuo.
- RTD_OPTION_QUOTES reposicionada como bridge auxiliar.
- SQLite mantido como persistência oficial.
- Execução automática de ordens mantida fora do escopo.
- Próxima ação definida: iniciar Fase 1 com auditoria, teste e commit ao final.

### Teste documental

- Arquivos presentes na pasta da frente.
- Documento reestruturado revisado em PDF.
- Escopo mantido conforme orientação: fases e aplicações daqui pra frente.
- Sem alteração de código nesta etapa.

### Status

ENCERRADO PARA REGISTRO DOCUMENTAL.

---
## Retificação e encerramento operacional da Fase 5 - UI operacional em tempo real

Marcador inicio: INICIO_RETIFICACAO_ENCERRAMENTO_OPERACIONAL_FASE_5_RTD_EXCEL_ONLINE_20260713

Data: 13/07/2026

### Motivo desta retificação

Esta seção substitui qualquer registro incompleto anterior de encerramento da Fase 5.

O conteúdo foi refeito sem blocos delimitados por crase. Os comandos e resultados foram registrados com indentação simples, preservando leitura documental e evitando quebra de geração por delimitadores Markdown.

### Escopo validado

A Fase 5 da frente RTD Excel BTG Online foi validada operacionalmente com foco na UI operacional em tempo real.

Arquitetura preservada:

    Corretora / RTD -> Excel LISTA_RTD.xlsm aberto -> Coletor Python online -> Snapshot SQLite -> Histórico Intraday -> Candles -> UI / Estruturas / Alertas

A validação confirma integração com:

    - snapshot RTD centralizado;
    - enriquecimento de legs sem subprocesso individual;
    - terminal VWAP/payoff;
    - candles intraday persistidos;
    - status operacional;
    - menu Ajuda com status RTD Excel;
    - validação real de Excel/RTD via COM;
    - histórico e candles encerrados nas fases anteriores.

### Testes executados

#### Suite focada da Fase 5

Comando executado:

    python -m pytest ATT/tests/test_rtd_option_quotes_sync_service.py \
      ATT/tests/test_structure_leg_rtd_enrichment_service.py \
      ATT/tests/test_terminal_vwap_payoff_app_service.py \
      ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py \
      ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py \
      ATT/tests/test_ui_modern_dark_window_operational_data_status_menu.py \
      ATT/tests/test_operational_data_status_service.py \
      ATT/tests/test_ui_intraday_candle_chart_consumption.py

Resultado:

    51 passed in 3.24s

#### Teste operacional real Excel/RTD

Comando executado:

    python -m pytest ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py -vv

Resultado:

    ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py::test_operational_dark_window_help_menu_and_live_excel_rtd_status PASSED
    1 passed in 5.07s

Esse teste validou em subprocesso Python limpo:

    - import real de UI.modern.dark_window;
    - tkinter/customtkinter/matplotlib reais;
    - construção real do menu Ajuda;
    - presença do item Status RTD Excel;
    - payload real do RTD/Excel ativo;
    - formatação real da mensagem exibida pela UI.

#### Suite ampliada integrada

Comando executado:

    python -m pytest ATT/tests -k "rtd or snapshot or intraday or candle or terminal_vwap or operational_data_status"

Resultado:

    245 passed, 564 deselected in 11.25s

### Critérios da Fase 5

Critérios considerados atendidos:

    - UI atualiza com dados reais do snapshot;
    - legs são preenchidas sem subprocesso individual;
    - estruturas usam fluxo integrado de dados de mercado;
    - gráfico consome candles intraday gerados pelo sistema;
    - status de conexão está visível;
    - menu Ajuda possui Status RTD Excel;
    - status operacional está disponível;
    - teste operacional real com Excel/RTD ativo foi aprovado;
    - teste integrado com Fases 1, 2, 3 e 4 foi executado;
    - ausência de regressão foi validada na suíte ampliada;
    - auditoria foi atualizada.

### Observação sobre fases posteriores

Artefatos ou testes relacionados a retenção, limpeza, alertas e decisão operacional permanecem classificados como antecipação técnica ou documental.

Esta validação não encerra Fase 6 nem Fase 7.

### Decisão

A Fase 5 está encerrada operacionalmente.

A próxima fase permitida é a Fase 6 - Retenção, limpeza e consolidação.

Marcador fim: FIM_RETIFICACAO_ENCERRAMENTO_OPERACIONAL_FASE_5_RTD_EXCEL_ONLINE_20260713

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

---

## Fase 6.1 - Contrato de retenção com dry-run obrigatório

Marcador inicio: INICIO_AUDITORIA_FASE6_1_CONTRATO_RETENCAO_DRY_RUN_20260713

Data: 13/07/2026

### Natureza

Contrato operacional e simulação não destrutiva para retenção, limpeza e consolidação da frente RTD Excel BTG Online.

### Guardrails preservados

- Nenhum `DELETE` executado.
- Nenhum `UPDATE` executado.
- Nenhum `DROP` executado.
- Nenhum `ALTER` executado.
- Nenhum `VACUUM` executado.
- Nenhuma compactação executada.
- Nenhum dado removido.
- Banco auditado em modo somente leitura no dry-run.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_1_CONTRATO_RETENCAO_DRY_RUN_20260713.md`
- `ATT/patches/fase6_1_contrato_retencao_dry_run_20260713.md`
- `ATT/scripts/fase6_1_retencao_dry_run_20260713.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_1_retencao_dry_run_20260713.md`

### Decisão

A Fase 6.1 estabelece contrato e simulação obrigatória.

A execução destrutiva permanece bloqueada até fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_1_CONTRATO_RETENCAO_DRY_RUN_20260713

---

## Fase 6.2 - Validação de cobertura dos candles antes de limpeza real

Marcador inicio: INICIO_AUDITORIA_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713

Data: 13/07/2026

### Natureza

Validação operacional não destrutiva para comparar histórico intraday bruto e candles consolidados.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum dado removido.
- Nenhum schema alterado.
- Nenhuma compactação executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713.md`
- `ATT/patches/fase6_2_validacao_cobertura_candles_20260713.md`
- `ATT/scripts/fase6_2_validacao_cobertura_candles_20260713.py`
- `ATT/tests/test_fase6_2_candle_coverage_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_2_validacao_cobertura_candles_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_2_pytest_20260713.txt`

### Decisão

A validação de cobertura não autoriza limpeza real.

A execução destrutiva permanece bloqueada até fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713

---

## Fase 6.3 - Mapeamento de schema para cobertura de candles

Marcador inicio: INICIO_AUDITORIA_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713

Data: 13/07/2026

### Natureza

Mapeamento operacional nao destrutivo para identificar colunas e pares candidatos de comparacao entre historico intraday bruto e candles consolidados.

### Contexto

A Fase 6.2 retornou status nao conclusivo por nao conseguir comparar chaves entre as tabelas avaliadas.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713.md`
- `ATT/patches/fase6_3_mapeamento_schema_cobertura_20260713.md`
- `ATT/scripts/fase6_3_mapeamento_schema_cobertura_20260713.py`
- `ATT/tests/test_fase6_3_schema_mapping_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_3_mapeamento_schema_cobertura_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_3_pytest_20260713.txt`

### Decisão

A Fase 6.3 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713

---

## Fase 6.4 - Regra explicita de cobertura entre historico bruto e candles

Marcador inicio: INICIO_AUDITORIA_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713

Data: 13/07/2026

### Natureza

Validacao operacional nao destrutiva para transformar o mapeamento da Fase 6.3 em regra explicita de cobertura.

### Regra avaliada

- Historico: `rtd_option_quotes_intraday_history.codigo_opcao`
- Candles: `rtd_option_quotes_intraday_candles.symbol`
- Tempo historico: `rtd_option_quotes_intraday_history.captured_at`
- Bucket candle: `rtd_option_quotes_intraday_candles.bucket_start`
- Intervalo candle: `rtd_option_quotes_intraday_candles.interval_minutes`

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713.md`
- `ATT/patches/fase6_4_regra_explicita_cobertura_20260713.md`
- `ATT/scripts/fase6_4_regra_explicita_cobertura_20260713.py`
- `ATT/tests/test_fase6_4_explicit_coverage_rule_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_4_regra_explicita_cobertura_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_4_pytest_20260713.txt`

### Decisao

A Fase 6.4 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713

---

## Fase 6.5 - Diagnostico das lacunas de cobertura

Marcador inicio: INICIO_AUDITORIA_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713

Data: 13/07/2026

### Natureza

Diagnostico operacional nao destrutivo para investigar lacunas da regra explicita de cobertura definida na Fase 6.4.

### Contexto

A Fase 6.4 indicou melhor intervalo candidato de 1 minuto, com cobertura parcial de 10 linhas em 60 linhas do historico bruto.

### Diagnosticos executados

- Cobertura exata por chave e bucket.
- Cobertura por simbolo.
- Cobertura por data e simbolo.
- Proximidade temporal ao candle mais proximo.
- Pares esperados ausentes.
- Pares extras em candles.
- Amostras de lacunas.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713.md`
- `ATT/patches/fase6_5_diagnostico_lacunas_cobertura_20260713.md`
- `ATT/scripts/fase6_5_diagnostico_lacunas_cobertura_20260713.py`
- `ATT/tests/test_fase6_5_coverage_gaps_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_5_diagnostico_lacunas_cobertura_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_5_pytest_20260713.txt`

### Decisao

A Fase 6.5 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_5_DIAGNOSTICO_LACUNAS_COBERTURA_20260713

---

## Fase 6.6 - Validacao de offset temporal de cobertura

Marcador inicio: INICIO_AUDITORIA_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713

Data: 13/07/2026

### Natureza

Validacao operacional nao destrutiva para testar offsets temporais entre `captured_at` do historico bruto e `bucket_start` dos candles.

### Contexto

A Fase 6.5 indicou cobertura por simbolo e por data de 60/60, mas cobertura exata de bucket de apenas 10/60.

A suspeita operacional e diferenca de fuso horario, especialmente offset de -3 horas entre timestamps do historico e buckets dos candles.

### Diagnosticos executados

- Teste de offsets horarios de -12 ate +12.
- Comparacao por intervalo de candle.
- Ranking de cobertura por offset.
- Identificacao do melhor offset candidato.
- Confirmacao de bloqueio de limpeza real.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713.md`
- `ATT/patches/fase6_6_validacao_offset_temporal_cobertura_20260713.md`
- `ATT/scripts/fase6_6_validacao_offset_temporal_cobertura_20260713.py`
- `ATT/tests/test_fase6_6_temporal_offset_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_6_validacao_offset_temporal_cobertura_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_6_pytest_20260713.txt`

### Decisao

A Fase 6.6 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713

---

## Fase 6.7 - Diagnostico de coortes temporais de cobertura

Marcador inicio: INICIO_AUDITORIA_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713

Data: 13/07/2026

### Natureza

Diagnostico operacional nao destrutivo para classificar linhas do historico bruto por offset temporal de cobertura.

### Contexto

A Fase 6.6 validou o offset `-3h` como melhor candidato global, cobrindo 50/60 linhas.

As 10 linhas restantes sugerem coorte temporal separada, possivelmente com timestamp ja armazenado em horario local ou com timezone explicito.

### Diagnosticos executados

- Classificacao linha a linha por offsets de -12h ate +12h.
- Identificacao de offsets que cobrem cada linha.
- Escolha de offset preferencial por linha.
- Distribuicao por presenca de timezone explicito.
- Confirmacao de bloqueio de limpeza real.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713.md`
- `ATT/patches/fase6_7_diagnostico_coortes_temporais_cobertura_20260713.md`
- `ATT/scripts/fase6_7_diagnostico_coortes_temporais_cobertura_20260713.py`
- `ATT/tests/test_fase6_7_temporal_cohorts_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_7_diagnostico_coortes_temporais_cobertura_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_7_pytest_20260713.txt`

### Decisao

A Fase 6.7 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713

---

## Fase 6.8 - Validacao da regra canonica de timezone local

Marcador inicio: INICIO_AUDITORIA_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713

Data: 13/07/2026

### Natureza

Validacao operacional nao destrutiva da regra canonica de normalizacao temporal para cobertura de candles.

### Contexto

A Fase 6.7 confirmou a existencia de coortes temporais:

- registros com `captured_at` em UTC `+00:00`;
- registros com `captured_at` em horario local `-03:00`.

A regra correta e normalizar timestamps com timezone para `America/Sao_Paulo`, sem aplicar offset fixo indistintamente.

### Regra validada

- `captured_at` com timezone explicito: converter para `America/Sao_Paulo`.
- `captured_at` sem timezone explicito: assumir horario local operacional.
- `bucket_start` dos candles: tratar como horario local operacional.
- Comparar por simbolo e bucket local arredondado pelo intervalo.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713.md`
- `ATT/patches/fase6_8_validacao_regra_canonica_timezone_local_20260713.md`
- `ATT/scripts/fase6_8_validacao_regra_canonica_timezone_local_20260713.py`
- `ATT/tests/test_fase6_8_canonical_local_timezone_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_8_validacao_regra_canonica_timezone_local_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_8_pytest_20260713.txt`

### Decisao

A Fase 6.8 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_8_VALIDACAO_REGRA_CANONICA_TIMEZONE_LOCAL_20260713

---

## Fase 6.9 - Dry-run de limpeza com timezone local canonico

Marcador inicio: INICIO_AUDITORIA_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713

Data: 13/07/2026

### Natureza

Dry-run operacional nao destrutivo para simular elegibilidade de limpeza usando a regra canonica de timezone local.

### Contexto

A Fase 6.8 validou cobertura completa com normalizacao para `America/Sao_Paulo`.

A Fase 6.9 usa essa regra para classificar quais linhas do historico bruto estariam elegiveis para limpeza em uma fase futura.

### Regra simulada

- `captured_at` com timezone explicito: converter para `America/Sao_Paulo`.
- `captured_at` sem timezone explicito: assumir horario local operacional.
- `bucket_start` dos candles: tratar como horario local operacional.
- Elegibilidade: existencia de candle com mesmo simbolo e mesmo bucket local.

### Guardrails preservados

- Banco aberto em modo somente leitura.
- Nenhum registro removido.
- Nenhum schema alterado.
- Nenhuma compactacao executada.
- Nenhuma limpeza real aprovada.

### Artefatos

- `FRENTE_RTD_EXCEL_BTG_ONLINE/AUDITORIA_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713.md`
- `ATT/patches/fase6_9_dry_run_limpeza_canonica_timezone_local_20260713.md`
- `ATT/scripts/fase6_9_dry_run_limpeza_canonica_timezone_local_20260713.py`
- `ATT/tests/test_fase6_9_dry_run_canonical_local_timezone_read_only.py`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_9_dry_run_limpeza_canonica_timezone_local_20260713.md`
- `FRENTE_RTD_EXCEL_BTG_ONLINE/output/fase6_9_pytest_20260713.txt`

### Decisao

A Fase 6.9 nao autoriza limpeza real.

A execucao destrutiva permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_AUDITORIA_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713
