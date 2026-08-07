!-- INICIO FRENTE 65 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 64 -->

## Frente 65 - Precheck local de SQLite fora de Boundary/Repository pos Frente 64

### Status

Concluida como precheck documental e tecnico.

A Frente 65 executou nova varredura local apos a Frente 64 para confirmar que os alvos
recentemente tratados permaneceram sem tokens SQLite fortes e para selecionar o proximo alvo
real ainda com SQL direto fora das camadas toleradas.

Esta frente nao alterou codigo operacional, nao alterou schema, nao alterou persistencia e
nao executou operacoes de Git.

### Contexto

As frentes anteriores removeram tokens SQLite fortes de:

- services/rtd_option_quotes_excel_sync.py
- UI/components/details_panel.py

A Frente 65 confirmou que esses dois alvos permaneceram limpos em relacao aos tokens fortes
monitorados e identificou o proximo alvo operacional recomendado.

### Objetivo

Mapear ocorrencias fortes e secundarias de SQL ou SQLite ainda presentes em camadas fora de
repositories, db e infra, especialmente em:

- services
- UI
- controllers
- domain

O objetivo foi produzir diagnostico pos Frente 64 para orientar a Frente 66.

### Escopo da varredura

Pastas analisadas:

- services
- UI
- controllers
- domain

Pastas excluidas:

- .git
- .pytest_cache
- ATT
- __pycache__
- dados
- db
- docs
- infra
- logs
- repositories
- scripts
- tools

As pastas repositories, db e infra permaneceram como locais tolerados para SQL direto nesta
checagem.

### Tokens pesquisados

Tokens fortes:

- import sqlite3
- sqlite3.connect
- sqlite_master
- PRAGMA table_info

Tokens secundarios:

- execute
- executemany
- SELECT
- INSERT
- UPDATE
- DELETE

### Resultado consolidado

- Arquivos analisados: 84
- Arquivos com achados: 25
- Ocorrencias encontradas: 117
- Status do relatorio: targets_found
- Frente recomendada seguinte: 66
- Alvo recomendado: services/rtd_option_quotes_excel_populator.py
- Risco do alvo recomendado: high

### Confirmacao dos alvos anteriores

O precheck confirmou que os alvos recentemente tratados ficaram sem tokens fortes:

- services/rtd_option_quotes_excel_sync.py
  - strong_hit_count: 0
- UI/components/details_panel.py
  - strong_hit_count: 0

### Proximo alvo recomendado

O alvo recomendado para a Frente 66 foi:

    services/rtd_option_quotes_excel_populator.py

O arquivo foi classificado como high por conter ocorrencias fortes e secundarias, incluindo:

- import sqlite3
- sqlite3.connect
- sqlite_master
- execute
- SELECT

### Outros candidatos relevantes remanescentes

A varredura ainda indicou outros candidatos para frentes futuras, entre eles:

- services/rtd_option_quotes_intraday_candle_service.py
- services/derived_service.py
- services/rtd_option_quotes_intraday_history_service.py
- domain/payoff_features.py
- domain/refs/structure_ref.py
- services/derived_payoff_persistence.py
- services/rtd_option_quotes_snapshot_status_service.py
- services/system_recalculation_command_service.py

### Artefatos locais

- ATT/patch_65_local_sql_boundary_precheck_pos_frente_64.py
- ATT/tests/test_frente_65_local_sql_boundary_precheck_pos_frente_64.py
- ATT/frente_65_local_sql_boundary_precheck_pos_frente_64_report.json

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_65_local_sql_boundary_precheck_pos_frente_64.py
    python -m py_compile ATT/patch_65_local_sql_boundary_precheck_pos_frente_64.py
    python -m pytest ATT/tests/test_frente_65_local_sql_boundary_precheck_pos_frente_64.py -q
    python -m json.tool ATT/frente_65_local_sql_boundary_precheck_pos_frente_64_report.json

Resultado local:

- py_compile sem erro.
- pytest com 5 passed.
- report JSON legivel.
- status do report: targets_found.
- recommended_next_front: 66.
- recommended_next_target: services/rtd_option_quotes_excel_populator.py.
- git_executed: false.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem alteracao de codigo operacional.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- Git nao executado.

### Proxima etapa recomendada

Abrir a Frente 66 para conter o SQL direto em services/rtd_option_quotes_excel_populator.py,
mantendo o recorte pequeno, reversivel e validavel.

A Frente 66 deve preservar:

- contratos publicos;
- comportamento externo esperado;
- schema existente;
- persistencia SQLite local;
- execucao 100 por cento local;
- ausencia de Web, HTTP ou API externa;
- ausencia de operacoes Git.

<!-- FIM FRENTE 65 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 64 -->

<!-- INICIO FRENTE 66 RTD OPTION QUOTES EXCEL POPULATOR SQL BOUNDARY -->

## Frente 66 - RTD Option Quotes Excel Populator SQL Boundary

### Status

Aplicada localmente e validada.

### Contexto

A Frente 66 deu continuidade a reducao incremental de SQL direto fora de repositories, db e
infra, apos a Frente 65 ter recomendado como proximo alvo:

- services/rtd_option_quotes_excel_populator.py

O alvo foi classificado como high por conter acoplamento SQLite direto em camada de service,
incluindo import sqlite3, sqlite3.connect, sqlite_master, execute e consultas SELECT.

### Objetivo

Conter o SQL direto em services/rtd_option_quotes_excel_populator.py, movendo as rotinas de
acesso persistido para um boundary local em repositories, sem alterar schema, persistencia,
contratos publicos ou comportamento externo esperado.

### Escopo aplicado

- Criado boundary local em repositories/rtd_option_quotes_excel_populator_sql_boundary.py.
- services/rtd_option_quotes_excel_populator.py passou a delegar rotinas persistidas para o
  boundary.
- Removidos do service os tokens fortes e secundarios do recorte validado.
- SQL persistido ficou concentrado em repositories.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma operacao de git foi executada.

### Funcoes movidas/delegadas

Funcoes com acesso SQLite direto movidas para o boundary:

- validate_database
- load_option_codes_from_db

Dependencias auxiliares preservadas para manter o comportamento esperado:

- get_db_path
- is_option_code
- normalize_symbol

### Arquivos principais

- services/rtd_option_quotes_excel_populator.py
- repositories/rtd_option_quotes_excel_populator_sql_boundary.py
- ATT/patch_66_rtd_option_quotes_excel_populator_sql_boundary.py
- ATT/tests/test_frente_66_rtd_option_quotes_excel_populator_sql_boundary.py
- ATT/frente_66_rtd_option_quotes_excel_populator_sql_boundary_report.json

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_66_rtd_option_quotes_excel_populator_sql_boundary.py
    python -m py_compile ATT/patch_66_rtd_option_quotes_excel_populator_sql_boundary.py ATT/tests/test_frente_66_rtd_option_quotes_excel_populator_sql_boundary.py services/rtd_option_quotes_excel_populator.py repositories/rtd_option_quotes_excel_populator_sql_boundary.py
    python -m pytest ATT/tests/test_frente_66_rtd_option_quotes_excel_populator_sql_boundary.py -q
    python -m json.tool ATT/frente_66_rtd_option_quotes_excel_populator_sql_boundary_report.json

Resultado local:

- py_compile sem erro.
- pytest com 6 passed.
- report JSON legivel.
- status do report: patched.
- service_strong_hits_after_patch: [].
- service_secondary_hits_after_patch: [].
- git_executed: false.

### Evidencia de boundary

A varredura direcionada confirmou que os tokens SQLite fortes nao permanecem no service e
aparecem apenas no boundary criado:

- repositories/rtd_option_quotes_excel_populator_sql_boundary.py contem import sqlite3.
- repositories/rtd_option_quotes_excel_populator_sql_boundary.py contem sqlite3.connect.
- repositories/rtd_option_quotes_excel_populator_sql_boundary.py contem sqlite_master.
- services/rtd_option_quotes_excel_populator.py nao apresentou ocorrencias desses tokens na
  varredura direcionada.

Comando executado:

    grep -RInE "import sqlite3|sqlite3\.connect|sqlite_master|PRAGMA table_info|pragma table_info" services/rtd_option_quotes_excel_populator.py repositories/rtd_option_quotes_excel_populator_sql_boundary.py

Resultado observado:

- ocorrencias apenas em repositories/rtd_option_quotes_excel_populator_sql_boundary.py.

### Backup operacional

Backup registrado pelo report:

- ATT/backup_66_rtd_option_quotes_excel_populator_sql_boundary_20260807_151010

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- SQL persistido concentrado em repositories.
- Camada service passa a delegar acesso SQLite do recorte.
- Git nao executado.

### Posicao apos a Frente 66

A Frente 66 encerra localmente o recorte de contencao de SQL direto em
services/rtd_option_quotes_excel_populator.py. O service ficou sem tokens SQLite fortes e
secundarios do recorte validado, e o acesso persistido passou a residir em
repositories/rtd_option_quotes_excel_populator_sql_boundary.py.

### Proxima etapa recomendada

Executar novo precheck local pos Frente 66 para confirmar a reducao de achados e selecionar o
proximo alvo real ainda fora de repositories, db e infra.

A proxima frente deve manter:

- um alvo real por vez;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao sincronizada nos arquivos consolidados;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

<!-- FIM FRENTE 66 RTD OPTION QUOTES EXCEL POPULATOR SQL BOUNDARY -->


 Frentes 67 e 68 - Documentacao local de SQL Boundary

Documento gerado automaticamente em 2026-08-07T15:54:22.

Este arquivo consolida localmente as Frentes 67 e 68 antes da abertura da Frente 69.

Guardrails gerais preservados:

- Sistema 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem operacoes Git.
- Patches, testes e reports permanecem em ATT.
- Documentacao local permanece em docs.

<!-- INICIO FRENTE 67 SQL BOUNDARY DOCUMENTACAO LOCAL -->

## Frente 67 - Precheck local de SQLite fora de Boundary/Repository pos Frente 66

### Status

targets_found

### Contexto

A Frente 67 foi documentada a partir do report local ATT/frente_67_local_sql_boundary_precheck_pos_frente_66_report.json.

### Objetivo

Mapear ocorrencias fortes e secundarias de SQL ou SQLite ainda presentes fora das camadas toleradas, confirmar a reducao apos a Frente 66 e recomendar o proximo alvo operacional.

### Escopo documentado

- Alvo principal: services/rtd_option_quotes_intraday_candle_service.py
- Boundary ou repository associado: Nao aplicavel para precheck.
- Report local: ATT/frente_67_local_sql_boundary_precheck_pos_frente_66_report.json
- Patch local: ATT/patch_67_local_sql_boundary_precheck_pos_frente_66.py
- Teste local: ATT/tests/test_frente_67_local_sql_boundary_precheck_pos_frente_66.py
- Backup operacional: Informacao nao disponivel.

### Alteracoes registradas pelo report

- Nenhuma substituicao operacional listada no report.

### Contagem antes da frente

- Informacao nao disponivel.

### Contagem depois da frente

- Informacao nao disponivel.

### Validacoes registradas

- Informacao nao disponivel.

### Proxima etapa registrada

- Frente recomendada seguinte: 68
- Alvo recomendado seguinte: services/rtd_option_quotes_intraday_candle_service.py

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web: true
- Sem HTTP: true
- Sem API externa: true
- Schema alterado: false
- Schema de persistencia alterado: Informacao nao disponivel.
- Git executado: false

- precheck_only: true
- patches_reports_tests_in_ATT: true
- no_git: true
- no_schema_change: true
- no_persistence_change: true
- no_operational_code_change: true
- no_web: true
- no_http: true
- no_external_api: true

### Notas

- Frente 67 executa somente precheck local pos Frente 66.
- Nenhum codigo operacional foi alterado.
- Nenhum schema foi alterado.
- Nenhuma persistencia foi alterada.
- Repositories, db e infra permanecem como camadas toleradas para SQL direto.
- Git nao executado.

### Validacao local sugerida

    python ATT/patch_67_local_sql_boundary_precheck_pos_frente_66.py
    python -m py_compile ATT/patch_67_local_sql_boundary_precheck_pos_frente_66.py ATT/tests/test_frente_67_local_sql_boundary_precheck_pos_frente_66.py
    python -m pytest ATT/tests/test_frente_67_local_sql_boundary_precheck_pos_frente_66.py -q
    python -m json.tool ATT/frente_67_local_sql_boundary_precheck_pos_frente_66_report.json

<!-- FIM FRENTE 67 SQL BOUNDARY DOCUMENTACAO LOCAL -->


<!-- INICIO FRENTE 68 SQL BOUNDARY DOCUMENTACAO LOCAL -->

## Frente 68 - Intraday Candle Service SQL Boundary

### Status

patched

### Contexto

A Frente 68 foi documentada a partir do report local ATT/frente_68_intraday_candle_service_sql_boundary_report.json.

### Objetivo

Conter o SQL direto em services/rtd_option_quotes_intraday_candle_service.py, delegando a leitura de historico intraday para o repository boundary local, sem alterar schema, persistencia, contratos publicos ou comportamento externo esperado.

### Escopo documentado

- Alvo principal: services/rtd_option_quotes_intraday_candle_service.py
- Boundary ou repository associado: repositories/rtd_option_quotes_intraday_history_repository.py
- Report local: ATT/frente_68_intraday_candle_service_sql_boundary_report.json
- Patch local: ATT/patch_68_intraday_candle_service_sql_boundary.py
- Teste local: ATT/tests/test_frente_68_intraday_candle_service_sql_boundary.py
- Backup operacional: ATT/backup_frente_68_intraday_candle_service_sql_boundary_20260807_153757

### Alteracoes registradas pelo report

- load_history_points
  - line_start: 106
  - line_end: 155
  - old_contains_sqlite_connect: true
  - old_contains_sqlite_master: true
  - old_contains_pragma_table_info: true

### Contagem antes da frente

- strong_total: 4
- secondary_total: 5
- strong_counts:
  - import_sqlite3: 1
  - sqlite3_connect: 1
  - sqlite_master: 1
  - pragma_table_info: 1
- secondary_counts:
  - execute_call: 3
  - executemany_call: 0
  - select_sql: 2
  - insert_sql: 0
  - update_sql: 0
  - delete_sql: 0
- strong_hits:
  - services/rtd_option_quotes_intraday_candle_service.py:3 - import_sqlite3 - import sqlite3
  - services/rtd_option_quotes_intraday_candle_service.py:115 - sqlite3_connect - conn = sqlite3.connect(path)
  - services/rtd_option_quotes_intraday_candle_service.py:121 - sqlite_master - from sqlite_master
  - services/rtd_option_quotes_intraday_candle_service.py:133 - pragma_table_info - "pragma table_info(rtd_option_quotes_intraday_history)"

### Contagem depois da frente

- strong_total: 0
- secondary_total: 0
- strong_counts:
  - import_sqlite3: 0
  - sqlite3_connect: 0
  - sqlite_master: 0
  - pragma_table_info: 0
- secondary_counts:
  - execute_call: 0
  - executemany_call: 0
  - select_sql: 0
  - insert_sql: 0
  - update_sql: 0
  - delete_sql: 0
- strong_hits:
  - vazio

### Validacoes registradas

- service_has_no_strong_sqlite_hits: true
- service_uses_repository_helper: true
- repository_helper_present: true

### Proxima etapa registrada

- Informacao nao disponivel no report.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web: true
- Sem HTTP: true
- Sem API externa: true
- Schema alterado: false
- Schema de persistencia alterado: false
- Git executado: false

- patches_reports_tests_in_ATT: true
- no_git: true
- no_schema_change: true
- no_persistence_schema_change: true
- sql_moved_from_service_to_repository_boundary: true
- repositories_db_infra_are_tolerated_sql_boundaries: true
- report_resynced_after_manual_service_import_fix: true

### Notas

- Report ressincronizado apos remocao manual do import sqlite3 e reposicionamento do import do helper.

### Validacao local sugerida

    python ATT/patch_68_intraday_candle_service_sql_boundary.py
    python -m py_compile ATT/patch_68_intraday_candle_service_sql_boundary.py ATT/tests/test_frente_68_intraday_candle_service_sql_boundary.py
    python -m pytest ATT/tests/test_frente_68_intraday_candle_service_sql_boundary.py -q
    python -m json.tool ATT/frente_68_intraday_candle_service_sql_boundary_report.json

<!-- FIM FRENTE 68 SQL BOUNDARY DOCUMENTACAO LOCAL -->

<!-- INICIO FRENTE 70 INTRADAY HISTORY SERVICE SQL BOUNDARY -->

## Frente 70 - Intraday History Service SQL Boundary

### Status

Aplicada localmente e validada.

### Contexto

A Frente 70 deu continuidade a estrategia incremental de contencao de SQL direto fora de
repositories, db e infra, atuando sobre o alvo:

- services/rtd_option_quotes_intraday_history_service.py

O alvo ainda continha acoplamento SQLite direto em camada de service, incluindo:

- import sqlite3
- sqlite3.connect
- sqlite_master
- chamadas .execute
- consultas SELECT

### Objetivo

Mover o acesso SQLite direto do service de historico intraday para o repository boundary:

- repositories/rtd_option_quotes_intraday_history_repository.py

O service permanece como camada de orquestracao e passa a delegar conexao, checagem de tabela
e leitura de snapshot para helpers no repository.

### Escopo aplicado

- Removido import sqlite3 do service.
- Removido uso direto de sqlite3.connect do service.
- Removida consulta direta a sqlite_master do service.
- Removidas chamadas SQL secundarias do service no recorte validado.
- Adicionados helpers de boundary no repository.
- Preservada persistencia SQLite local.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma operacao de Git foi executada.

### Funcoes substituidas no service

- _connect: changed=true, old_contains_sqlite=true, old_contains_execute=true, old_contains_sqlite_master=true
- _read_snapshot_rows: changed=true, old_contains_sqlite=true, old_contains_execute=true, old_contains_sqlite_master=true
- _table_exists: changed=true, old_contains_sqlite=true, old_contains_execute=true, old_contains_sqlite_master=true

### Helpers concentrados no repository

- open_intraday_history_capture_connection
- intraday_history_snapshot_table_exists_for_capture
- fetch_snapshot_rows_for_intraday_history_capture

### Arquivos principais

- services/rtd_option_quotes_intraday_history_service.py
- repositories/rtd_option_quotes_intraday_history_repository.py
- ATT/patch_70_intraday_history_service_sql_boundary.py
- ATT/tests/test_frente_70_intraday_history_service_sql_boundary.py
- ATT/frente_70_intraday_history_service_sql_boundary_report.json
- ATT/patch_70_intraday_history_service_sql_boundary_docs.py
- ATT/frente_70_intraday_history_service_sql_boundary_docs_report.json
- docs/frente_70_intraday_history_service_sql_boundary.md

### Resultado consolidado do report

- status: patched
- sqlite_imports_removed: 1
- helper_imports_removed: 3
- service_repository_import_added: true
- repository_helpers_added: true
- schema_changed: false
- persistence_schema_changed: false
- operational_code_changed: true
- git_executed: false

### Antes da Frente 70

- strong_total: 3
- secondary_total: 4

Ocorrencias fortes antes:

- import_sqlite3: 1
- sqlite3_connect: 1
- sqlite_master: 1
- pragma_table_info: 0

Ocorrencias secundarias antes:

- execute_call: 2
- executemany_call: 0
- select_sql: 2
- insert_sql: 0
- update_sql: 0
- delete_sql: 0

### Depois da Frente 70

- strong_total: 0
- secondary_total: 0
- strong_hits: []
- secondary_hits: []

Validacoes registradas:

- service_has_no_strong_sqlite_hits: true
- service_has_no_secondary_sql_hits: true
- service_uses_repository_helpers: true
- repository_helpers_present: true

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_70_intraday_history_service_sql_boundary.py
    python -m pytest ATT/tests/test_frente_70_intraday_history_service_sql_boundary.py -q
    python -m json.tool ATT/frente_70_intraday_history_service_sql_boundary_report.json
    grep -RInE "import sqlite3|sqlite3\.connect|sqlite_master|PRAGMA table_info|pragma table_info|\.execute\(|SELECT|fetch_snapshot_rows_for_intraday_history_capture|intraday_history_snapshot_table_exists_for_capture|open_intraday_history_capture_connection" services/rtd_option_quotes_intraday_history_service.py repositories/rtd_option_quotes_intraday_history_repository.py

Resultado local observado:

- pytest da Frente 70 com 5 passed.
- report JSON legivel.
- status do report: patched.
- service_has_no_strong_sqlite_hits: true.
- service_has_no_secondary_sql_hits: true.
- service_uses_repository_helpers: true.
- repository_helpers_present: true.
- strong_total depois: 0.
- secondary_total depois: 0.
- git_executed: false.

### Evidencia de boundary

A Frente 70 confirmou que o service deixou de conter SQL direto do recorte validado.

O acesso SQLite direto passou a residir no repository boundary:

- repositories/rtd_option_quotes_intraday_history_repository.py

Helpers adicionados ou confirmados no repository:

- open_intraday_history_capture_connection
- intraday_history_snapshot_table_exists_for_capture
- fetch_snapshot_rows_for_intraday_history_capture

O service passou a delegar para esses helpers em:

- _connect
- _read_snapshot_rows
- _table_exists

### Backup operacional

Backup registrado pelo report:

- ATT/backup_frente_70_intraday_history_service_sql_boundary_20260807_160446

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web: true
- Sem HTTP: true
- Sem API externa: true
- Sem troca de persistencia.
- Sem alteracao de schema: true
- Sem alteracao de schema de persistencia: true
- Sem criacao de pasta nova na raiz: true
- Patches, relatorios e testes permanecem em ATT: true
- SQL movido do service para repository boundary: true
- repositories, db e infra seguem como boundaries tolerados: true
- Uma frente operacional por alvo: true
- Git nao executado: true

### Posicao apos a Frente 70

A Frente 70 encerra localmente o recorte de contencao de SQL direto em
services/rtd_option_quotes_intraday_history_service.py.

O service ficou sem tokens fortes e secundarios do recorte validado, e o acesso persistido
SQLite passou a residir em repositories/rtd_option_quotes_intraday_history_repository.py.

### Proxima etapa recomendada

Executar novo precheck local apos a Frente 70 para confirmar a reducao de achados e selecionar
o proximo alvo real ainda fora de repositories, db e infra.

A proxima frente deve manter:

- um alvo real por vez;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao sincronizada nos arquivos consolidados;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

<!-- FIM FRENTE 70 INTRADAY HISTORY SERVICE SQL BOUNDARY -->

<!-- INICIO FRENTE 71 INTRADAY CANDLE SERVICE SQL BOUNDARY -->
# FRENTE 71 INTRADAY CANDLE SERVICE SQL BOUNDARY

## Status

CONCLUIDA LOCALMENTE

## Objetivo

Conter a fronteira SQL do fluxo de candles intraday, garantindo que o service services/rtd_option_quotes_intraday_candle_service.py nao seja dono de acesso direto ao SQLite.

A regra desta frente e simples:

    Service orquestra regra de aplicacao.
    Repository executa persistencia e consultas SQL.
    UI e command services nao devem depender de SQL direto deste fluxo.

## Arquivos envolvidos

Alvos principais:

    services/rtd_option_quotes_intraday_candle_service.py
    repositories/rtd_option_quotes_intraday_candle_repository.py

Guardrail criado:

    ATT/tests/test_frente_71_intraday_candle_service_sql_boundary.py

Relatorio local:

    ATT/frente_71_intraday_candle_service_sql_boundary_report.json

## Contrato protegido

O service de candles intraday nao deve conter:

    import sqlite3
    sqlite3.connect
    conn.execute
    connection.execute
    cur.execute
    cursor.execute
    SQL embutido com CREATE TABLE, ALTER TABLE, INSERT INTO, UPDATE, DELETE FROM, SELECT FROM ou DROP TABLE

A fronteira SQL permitida para este fluxo fica no repository:

    repositories/rtd_option_quotes_intraday_candle_repository.py

## Validacao recomendada

Executar:

    pytest -q ATT/tests/test_frente_71_intraday_candle_service_sql_boundary.py
    pytest -q ATT/tests/test_rtd_option_quotes_intraday_candle_service.py ATT/tests/test_rtd_option_quotes_intraday_candle_repository.py

Validar documentos:

    grep -RIn 'crases_triplas' docs/frente_71_intraday_candle_service_sql_boundary.md docs/PLANO_CONTENCAO_CONSOLIDADO_3.md docs/FRENTES_CORRIGIDAS_PARTE_6.md
    grep -RIn "FRENTE 71 INTRADAY CANDLE SERVICE SQL BOUNDARY" docs/frente_71_intraday_candle_service_sql_boundary.md docs/PLANO_CONTENCAO_CONSOLIDADO_3.md docs/FRENTES_CORRIGIDAS_PARTE_6.md

## Resultado esperado

A FRENTE 71 fecha o limite arquitetural do service de candles intraday, mantendo SQL somente no repository e impedindo regressao futura para acesso direto a banco dentro da camada de service.

<!-- FIM FRENTE 71 INTRADAY CANDLE SERVICE SQL BOUNDARY -->

<!-- INICIO FRENTE 72 SERVICES SQL BOUNDARY AUDIT -->
# FRENTE 72 SERVICES SQL BOUNDARY AUDIT

## Objetivo

Criar uma barreira de contenção para impedir crescimento de SQL direto dentro da camada services.

## Escopo

- Pasta auditada: services
- Tipo de frente: auditoria estática e guardrail de regressão
- Código operacional alterado: não
- Schema alterado: não
- Persistência alterada: não
- Git executado: não

## Política validada

Services não devem abrir conexão SQLite nem executar SQL diretamente.
A persistência deve ser delegada para repositories ou portas equivalentes.

## Resultado da auditoria

Total de ocorrências detectadas no baseline: 41

## Principais candidatos para próximas frentes

- services/derived_service.py: 11 ocorrência(s)
- services/rtd_option_quotes_snapshot_status_service.py: 5 ocorrência(s)
- services/derived_payoff_persistence.py: 4 ocorrência(s)
- services/system_recalculation_command_service.py: 3 ocorrência(s)
- services/excel_rtd_workbook_probe.py: 2 ocorrência(s)
- services/rtd_option_quotes_intraday_candle_chart_service.py: 2 ocorrência(s)
- services/rtd_option_quotes_intraday_candle_service.py: 2 ocorrência(s)
- services/rtd_option_quotes_intraday_history_service.py: 2 ocorrência(s)
- services/rtd_option_quotes_sync_service.py: 2 ocorrência(s)
- services/sql_direct_usage_prioritizer.py: 2 ocorrência(s)

## Validações recomendadas

python -m json.tool ATT/frente_72_services_sql_boundary_audit_report.json

pytest -q ATT/tests/test_frente_72_services_sql_boundary_audit.py

## Próxima ação sugerida

Selecionar o primeiro arquivo da lista de candidatos e criar uma frente específica para migrar o SQL direto para repository, mantendo teste de regressão antes e depois da alteração.
<!-- FIM FRENTE 72 SERVICES SQL BOUNDARY AUDIT -->

BEGIN_FRENTE_73_DERIVED_SERVICE_SQL_BOUNDARY_INVENTORY

## Frente 73 - Derived Service SQL Boundary Inventory

### Status

Inventario local criado, documentado e validado.

### Contexto

A Frente 73 foi aberta apos a Frente 72 identificar services/derived_service.py como o principal candidato remanescente para reducao de SQL direto em services.

A Frente 72 apontou services/derived_service.py com 11 ocorrencias no baseline geral da camada services. A Frente 73 aprofundou esse alvo e criou um inventario por contexto interno do arquivo, sem alterar codigo operacional.

### Objetivo

Inventariar os pontos de SQL direto em services/derived_service.py para preparar uma migracao incremental e segura para repository ou porta adequada.

Esta frente nao removeu SQL, nao mudou comportamento e nao alterou persistencia. Ela apenas consolidou o mapa tecnico para orientar a Frente 74.

### Escopo

- Alvo principal: services/derived_service.py
- Tipo de frente: inventario local e guardrail documental
- Report local: ATT/frente_73_derived_service_sql_boundary_inventory_report.json
- Teste local: ATT/tests/test_frente_73_derived_service_sql_boundary_inventory.py
- Documento local: docs/frente_73_derived_service_sql_boundary_inventory.md
- Codigo operacional alterado: false
- Schema alterado: false
- Schema de persistencia alterado: false
- Git executado: false

### Resultado do inventario

- Status do report: inventory_created
- Achados totais: 23
- Politica validada: Services nao devem abrir conexao SQLite nem executar SQL diretamente; persistencia deve passar por repositories.

### Hotspots por contexto

- get_recent_decisions: 7 ocorrencia(s)
- get_all_payoff_curves: 4 ocorrencia(s)
- get_payoff_by_structure_id: 4 ocorrencia(s)
- _load_aba_cache: 3 ocorrencia(s)
- module: 1 ocorrencia(s)
- init_db: 1 ocorrencia(s)
- save_payoff_curve: 1 ocorrencia(s)
- save_decision: 1 ocorrencia(s)
- cleanup_derived: 1 ocorrencia(s)

### Principais pontos identificados

O inventario local encontrou ocorrencias em:

- module
- _load_aba_cache
- init_db
- save_payoff_curve
- save_decision
- cleanup_derived
- get_all_payoff_curves
- get_payoff_by_structure_id
- get_recent_decisions

O maior hotspot identificado foi get_recent_decisions, com 7 ocorrencias.

### Decisao da Frente 73

Nao alterar codigo operacional nesta frente.

A decisao foi manter a Frente 73 como inventario tecnico e documental, preparando a Frente 74 para remover apenas um bloco real de SQL direto por vez.

### Validacoes executadas localmente

- python -m json.tool ATT/frente_73_derived_service_sql_boundary_inventory_report.json: OK
- pytest -q ATT/tests/test_frente_73_derived_service_sql_boundary_inventory.py: 5 passed
- pytest -q ATT/tests/test_derived_service.py: 9 passed
- pytest -q ATT/tests/test_derived_service.py ATT/tests/test_guardrail_derived_repo_consistency_structure_id.py ATT/tests/test_guardrail_derived_repo_get_payoff_by_structure_id.py ATT/tests/test_guardrail_derived_repo_structure_id_deletes.py: 18 passed

### Validacoes recomendadas para repeticao

    python -m json.tool ATT/frente_73_derived_service_sql_boundary_inventory_report.json
    pytest -q ATT/tests/test_frente_73_derived_service_sql_boundary_inventory.py
    pytest -q ATT/tests/test_derived_service.py

### Guardrails preservados

- Sistema permanece 100 por cento local: true
- Sem Web: true
- Sem HTTP: true
- Sem API externa: true
- Sem alteracao de schema: true
- Sem alteracao de schema de persistencia: true
- Sem alteracao de codigo operacional: true
- Git nao executado: true
- Documentos sem cercas de codigo: true
- Marcador inicial preservado: true
- Marcador final preservado: true

### Backup operacional

Backup registrado:

- ATT/backup_frente_73_derived_service_sql_boundary_inventory_20260807_164449

### Proxima frente recomendada

- Frente recomendada: 74
- Alvo: services/derived_service.py
- Acao: extrair um unico bloco real de SQL direto para repository ou porta adequada
- Restricao: uma alteracao operacional pequena, reversivel e testada

A Frente 74 deve escolher um unico bloco real de SQL direto em services/derived_service.py e mover para repository ou porta adequada, mantendo comportamento externo, schema e persistencia SQLite local.

### Posicao apos a Frente 73

A Frente 73 fica concluida como inventario local. O alvo services/derived_service.py esta mapeado e pronto para uma frente operacional pequena, reversivel e validada.

END_FRENTE_73_DERIVED_SERVICE_SQL_BOUNDARY_INVENTORY

\n\n

" docs/frente_74_derived_service_sql_boundary_guardrail.md
- grep -n "

" docs/FRENTES_CORRIGIDAS_PARTE_6.md
- pytest -q ATT/tests/test_frente_74_derived_service_sql_boundary_guardrail.py
- pytest -q ATT/tests/test_derived_service.py

Proxima acao sugerida:
- Seguir para o proximo alvo inventariado com SQL direto, preferencialmente UI/components/details_panel.py ou UI/components/terminal_vwap_payoff_dark_panel.py, repetindo inventario, guardrail, migracao pequena, teste e documentacao.
" docs/frente_74_derived_service_sql_boundary_guardrail.md\n- grep -n "

" docs/frente_74_derived_service_sql_boundary_guardrail.md
- grep -n "

" docs/FRENTES_CORRIGIDAS_PARTE_6.md
- pytest -q ATT/tests/test_frente_74_derived_service_sql_boundary_guardrail.py
- pytest -q ATT/tests/test_derived_service.py

Proxima acao sugerida:
- Seguir para o proximo alvo inventariado com SQL direto, preferencialmente UI/components/details_panel.py ou UI/components/terminal_vwap_payoff_dark_panel.py, repetindo inventario, guardrail, migracao pequena, teste e documentacao.

BEGIN_FRENTE_74_DERIVED_SERVICE_SQL_BOUNDARY_GUARDRAIL
# Frente 74 - Derived Service SQL Boundary Guardrail

Status: concluida e saneada documentalmente

Objetivo:
- Manter services/derived_service.py sem SQL direto.
- Delegar detalhes SQL para repositories/derived_service_sql_boundary.py.
- Preservar fronteira entre service e persistencia.

Evidencias:
- pytest do guardrail da Frente 74: 4 passed.
- pytest de derived_service: 9 passed.
- Documento saneado para manter exatamente um marcador BEGIN e um marcador END da Frente 74.

Escopo:
- Git executado: nao.
- Schema alterado: nao.
- Persistencia alterada nesta etapa documental: nao.

END_FRENTE_74_DERIVED_SERVICE_SQL_BOUNDARY_GUARDRAIL

BEGIN_FRENTE_75_DETAILS_PANEL_SQL_BOUNDARY_INVENTORY
# Frente 75 - DetailsPanel SQL Boundary Inventory

Status: inventario criado

Objetivo:
- Inventariar SQL direto em UI/components/details_panel.py.
- Preparar a migracao segura para repository, service ou boundary dedicado.
- Impedir que a divida fique invisivel antes da remocao operacional.

Alvo:
- UI/components/details_panel.py

Resultado do inventario:
- Linhas com literais SQL diretos: 0
- Imports diretos de sqlite3: 0
- Chamadas diretas de connect SQLite: 0
- Divida SQL direta detectada: False

Arquivos criados ou atualizados:
- ATT/frente_75_details_panel_sql_boundary_inventory_report.json
- ATT/tests/test_frente_75_details_panel_sql_boundary_inventory.py
- ATT/tests/test_frente_74_doc_marker_integrity.py
- docs/frente_75_details_panel_sql_boundary_inventory.md
- docs/FRENTES_CORRIGIDAS_PARTE_6.md

Escopo operacional:
- Codigo operacional alterado: nao.
- Schema alterado: nao.
- Schema de persistencia alterado: nao.
- Git executado: nao.

Proxima acao sugerida:
- Frente 75b: extrair o acesso SQLite do DetailsPanel para repository ou boundary dedicado, mantendo a UI consumindo apenas servico ou metodo de leitura encapsulado.

END_FRENTE_75_DETAILS_PANEL_SQL_BOUNDARY_INVENTORY

BEGIN_FRENTE_75A_V2_FIX_REPORT_PATH_NORMALIZATION
# Frente 75a-v2 - Fix Report Path Normalization

Status: documentada localmente

Gerado em: 2026-08-07T17:33:14

Objetivo:
- Documentar a normalizacao de caminhos do report da Frente 75a.
- Garantir que o alvo seja registrado com barras POSIX.
- Remover divergencia entre Windows backslash e expectativa dos testes.
- Preservar a Frente 75a como inventario sem alterar codigo operacional.

Contexto:
- A Frente 75a criou inventario para UI/components/details_panel.py.
- O report inicial foi gerado com caminho usando separadores Windows.
- O teste ATT/tests/test_frente_75_details_panel_sql_boundary_inventory.py esperava UI/components/details_panel.py.
- A Frente 75a-v2 normalizou o campo target e os caminhos do report para barras.

Alvo documentado:
- UI/components/details_panel.py

Target esperado:
- UI/components/details_panel.py

Target atual:
- UI/components/details_panel.py

Status do inventario 75a:
- inventory_created

Status da correcao 75a-v2:
- report_path_normalized

Arquivos documentados:
- ATT/frente_75_details_panel_sql_boundary_inventory_report.json
- ATT/frente_75a_v2_fix_report_path_normalization_report.json
- docs/frente_75a_v2_fix_report_path_normalization.md
- docs/FRENTES_CORRIGIDAS_PARTE_6.md

Validacoes locais confirmadas:
- python -m json.tool ATT/frente_75_details_panel_sql_boundary_inventory_report.json
- python -m json.tool ATT/frente_75a_v2_fix_report_path_normalization_report.json
- pytest -q ATT/tests/test_frente_74_doc_marker_integrity.py
- pytest -q ATT/tests/test_frente_75_details_panel_sql_boundary_inventory.py
- pytest -q ATT/tests/test_frente_74_derived_service_sql_boundary_guardrail.py
- pytest -q ATT/tests/test_derived_service.py

Resultado observado:
- Report 75a legivel.
- Report 75a-v2 legivel.
- Teste documental da Frente 74 aprovado.
- Teste de inventario da Frente 75 aprovado.
- Guardrail da Frente 74 aprovado.
- Testes de derived_service aprovados.

Escopo operacional:
- Codigo operacional alterado: nao.
- Schema alterado: nao.
- Schema de persistencia alterado: nao.
- Git executado: nao.
- Alteracao restrita a documentacao e report de normalizacao.

Guardrails preservados:
- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem alteracao de codigo operacional.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- Documentacao permanece em docs.
- Git nao executado.

Proxima acao sugerida:
- Encerrar documentalmente a Frente 75a-v2.
- Abrir a proxima frente em alvo real ainda relevante, preferencialmente UI/components/terminal_vwap_payoff_dark_panel.py.
- Repetir inventario, guardrail, migracao pequena, teste e documentacao.
END_FRENTE_75A_V2_FIX_REPORT_PATH_NORMALIZATION

