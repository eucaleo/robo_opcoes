# Plano de Contencao Consolidado

Documento local de desenvolvimento mantido conforme o plano efetivo.



<!-- INICIO FRENTE 55B VALIDACAO LOCAL TERMINAL VWAP DARK PANEL REPO BOUNDARY -->

## Frente 55b — Terminal VWAP Payoff Dark Panel com boundary de repository

### Status

Aplicada localmente e validada.

### Contexto

A Frente 55b deu continuidade a reducao incremental de SQL direto fora de repositories,
db e infra, apos a consolidacao da Frente 54 em UI/models/ui_data.py e a prechecagem
local da Frente 55a.

O alvo tecnico desta frente foi:

- UI/components/terminal_vwap_payoff_dark_panel.py

### Objetivo

Remover o SQL direto e o acoplamento SQLite remanescente do painel Terminal VWAP Payoff
Dark Panel, concentrando a leitura persistida em boundary local de repository.

### Escopo aplicado

- Criado boundary local em repositories/terminal_vwap_payoff_snapshot_repository.py.
- UI/components/terminal_vwap_payoff_dark_panel.py passou a delegar leituras persistidas
  para TerminalVWAPPayoffSnapshotRepository.
- A UI ficou sem ocorrencias diretas de SELECT, INSERT, UPDATE, DELETE, PRAGMA,
  sqlite_master, execute, sqlite3.connect e sqlite3 no alvo operacional.
- A logica persistida permaneceu local e concentrada em repository.
- Nenhuma migracao Web foi feita.
- Nenhum HTTP foi introduzido.
- Nenhuma API externa foi introduzida.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma alteracao operacional ampla foi feita.
- Nenhuma operacao de git foi executada.

### Metodos delegados no recorte validado

- _connect
- _tables_cols
- _load_structures
- _fetch_legs_rows
- _load_market
- _build_market_query
- _render_legs
- _set_alerts

### Artefatos locais

- Repository: repositories/terminal_vwap_payoff_snapshot_repository.py
- Relatorio: ATT/frente_55b_terminal_vwap_dark_panel_repo_boundary_report.json
- Teste: ATT/tests/test_frente_55b_terminal_vwap_dark_panel_repo_boundary_local.py
- Backup: ATT/backup_55b_terminal_vwap_dark_panel_repo_boundary_20260807_100746

### Validacao local executada

Compilacao direcionada executada com sucesso:

    python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py repositories/terminal_vwap_payoff_snapshot_repository.py ATT/tests/test_frente_55b_terminal_vwap_dark_panel_repo_boundary_local.py

Teste especifico da Frente 55b executado com sucesso:

    python -m pytest ATT/tests/test_frente_55b_terminal_vwap_dark_panel_repo_boundary_local.py -q

Resultado local:

    6 passed

Varredura final no alvo operacional:

    grep -RInE "SELECT|INSERT|UPDATE|DELETE|PRAGMA|sqlite_master|\.execute\(|sqlite3\.connect|sqlite3" UI/components/terminal_vwap_payoff_dark_panel.py || true

Resultado:

    Nenhuma ocorrencia encontrada no alvo operacional.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- Testes permanecem em ATT/tests.
- Documentacao local sincronizada em docs.
- Git nao executado.

### Posicao apos a Frente 55b

A Frente 55b encerra localmente o recorte de remocao de SQL direto do alvo
UI/components/terminal_vwap_payoff_dark_panel.py, mantendo a estrategia de um alvo real
por vez e preservando contratos, schema, persistencia e execucao local.

<!-- FIM FRENTE 55B VALIDACAO LOCAL TERMINAL VWAP DARK PANEL REPO BOUNDARY -->

<!-- INICIO FRENTE 56 UI DATA PAYOFF CURVE CONNECTION LIFECYCLE -->

## Frente 56 - UIDataModel payoff curve com ciclo de conexao seguro

### Status

Validada localmente.

### Objetivo

Garantir que rotinas de payoff curve em UI/models/ui_data.py nao mantenham conexao
SQLite aberta apos montar ou retornar dados de curva de payoff.

### Resultado aplicado

A Frente 56 foi executada de forma tolerante ao estado atual do arquivo alvo.

O report registrou status no_patch_applicable porque nao havia mais sqlite3.connect
direto nas rotinas candidatas de payoff curve. Todas as funcoes candidatas foram
avaliadas e ignoradas com motivo no_sqlite_connect.

Esse resultado e esperado e aceitavel, pois a Frente 54q ja havia consolidado
UI/models/ui_data.py como boundary sem SQL direto, sem execute e sem sqlite3 direto.

### Arquivo alvo

- UI/models/ui_data.py

### Rotinas candidatas avaliadas

- _load_legacy_payoff_curve_info_points
- _build_legacy_payoff_curve_exact_sql
- _fetch_canonical_payoff_curve_points
- _fetch_latest_payoff_curve_timestamp
- _fetch_payoff_curve_latest_timestamp
- _build_payoff_curve_latest_timestamp_sql
- _fetch_payoff_curve_exact_rows
- _build_payoff_curve_exact_sql

### Resultado tecnico

- Nenhuma rotina precisou ser alterada.
- Nenhuma rotina candidata continha sqlite3.connect direto.
- Nenhuma conexao SQLite aberta sem fechamento foi identificada no recorte.
- O patch permaneceu tolerante a ausencia de get_payoff_curve.
- O arquivo de teste local foi criado e validado.
- O report JSON foi gerado e validado.

### Artefatos locais

- ATT/patch_56_ui_data_payoff_curve_connection_lifecycle.py
- ATT/tests/test_frente_56_ui_data_payoff_curve_connection_lifecycle.py
- ATT/frente_56_ui_data_payoff_curve_connection_lifecycle_report.json
- ATT/backup_56_ui_data_payoff_curve_connection_lifecycle_20260807_105618

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_56_ui_data_payoff_curve_connection_lifecycle.py
    python -m py_compile ATT/patch_56_ui_data_payoff_curve_connection_lifecycle.py UI/models/ui_data.py ATT/tests/test_frente_56_ui_data_payoff_curve_connection_lifecycle.py
    python -m pytest ATT/tests/test_frente_56_ui_data_payoff_curve_connection_lifecycle.py -q
    python -m json.tool ATT/frente_56_ui_data_payoff_curve_connection_lifecycle_report.json

Resultado:

- py_compile sem erro.
- pytest com 6 passed.
- report JSON legivel.
- status no_patch_applicable.
- patched_functions vazio.
- todas as rotinas candidatas ignoradas por no_sqlite_connect.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem alteracao de contrato financeiro.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- Documentacao local sincronizada em docs.
- Git nao executado.

### Posicao apos a Frente 56

A Frente 56 confirma que o recorte de payoff curve em UI/models/ui_data.py nao possui
mais conexao SQLite direta aberta sem fechamento local. O resultado reforca a boundary
consolidada na Frente 54q, em que UI/models/ui_data.py atua como orquestrador/delegador
e a camada db/repository concentra acesso persistido.

<!-- FIM FRENTE 56 UI DATA PAYOFF CURVE CONNECTION LIFECYCLE -->

<!-- INICIO PROXIMA ACAO POS FRENTE 56 -->

## Proxima acao pos Frente 56

A Frente 56 foi validada localmente e nao exige novo patch operacional.

Proxima etapa recomendada:

- Executar novo precheck local para identificar o proximo alvo real fora de repositories,
  db e infra que ainda contenha SQL direto, execute, sqlite3.connect ou acoplamento
  persistido inadequado.
- Manter a estrategia de uma frente pequena por vez.
- Preservar schema, persistencia, contratos publicos e execucao 100 por cento local.
- Nao executar git ate o encerramento e consolidacao final de todas as frentes.

Criterio de aceite da proxima frente:

- alvo real identificado por varredura local;
- recorte pequeno e reversivel;
- patch, teste e report em ATT;
- documentacao local sincronizada em docs;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

<!-- FIM PROXIMA ACAO POS FRENTE 56 -->

<!-- INICIO FRENTE 57 PRECHECK SQL BOUNDARY LOCAL -->

## Frente 57 - Precheck local de SQL direto fora da boundary persistida

### Status

Executada localmente.

### Objetivo

Identificar o proximo alvo real fora de repositories, db e infra que ainda contenha
SQL direto, execute, sqlite3.connect ou acoplamento persistido inadequado.

### Resultado

- Arquivos Python avaliados: 123
- Arquivos com achados: 24
- Status: targets_found
- Proximo alvo recomendado: services/canonical_pricing_facade.py
- Risco do alvo recomendado: high

### Artefatos locais

- ATT/patch_57_local_sql_boundary_precheck.py
- ATT/tests/test_frente_57_local_sql_boundary_precheck.py
- ATT/frente_57_local_sql_boundary_precheck_report.json

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- Documentacao local sincronizada em docs.
- Git nao executado.

### Proxima etapa sugerida

Abrir o alvo recomendado no report JSON e criar uma frente pequena e reversivel para
remover ou conter o SQL direto identificado, preferencialmente migrando o acesso para
repository ou service ja existente.

<!-- FIM FRENTE 57 PRECHECK SQL BOUNDARY LOCAL -->

<!-- INICIO FRENTE 58 CANONICAL PRICING FACADE SQL BOUNDARY -->

## Frente 58 - Canonical Pricing Facade SQL Boundary

### Status

Aplicada localmente e validada.

### Contexto

A Frente 58 deu continuidade a reducao incremental de SQL direto fora de repositories,
db e infra, apos o precheck local da Frente 57 ter indicado como proximo alvo recomendado:

- services/canonical_pricing_facade.py

O alvo foi classificado como risco high no precheck porque ainda concentrava acesso SQLite
direto em camada de service.

### Objetivo

Conter SQL direto em services/canonical_pricing_facade.py, movendo rotinas top-level com
SQLite direto para um boundary persistido em repositories, sem alterar schema, persistencia,
contratos publicos ou comportamento externo esperado.

### Escopo aplicado

- Criado boundary local em repositories/canonical_pricing_facade_sql_boundary.py.
- services/canonical_pricing_facade.py passou a delegar o acesso SQLite para o boundary.
- Removido acoplamento direto com sqlite3 do service no recorte validado.
- Mantidas as funcoes privadas esperadas pela facade por delegacao.
- SQL persistido ficou concentrado em repositories.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma alteracao operacional ampla foi feita.
- Nenhuma operacao de git foi executada.

### Funcoes movidas

Funcoes top-level com SQLite direto movidas para repositories/canonical_pricing_facade_sql_boundary.py:

- _get_structure_info
- _lookup_spot_price

Funcoes SQL internas ou de classe nao movidas automaticamente por seguranca:

- nenhuma

### Arquivos principais

- services/canonical_pricing_facade.py
- repositories/canonical_pricing_facade_sql_boundary.py
- ATT/patch_58_canonical_pricing_facade_sql_boundary.py
- ATT/tests/test_frente_58_canonical_pricing_facade_sql_boundary.py
- ATT/frente_58_canonical_pricing_facade_sql_boundary_report.json

### Validacao local executada

Comandos executados localmente:

    python -m py_compile services/canonical_pricing_facade.py repositories/canonical_pricing_facade_sql_boundary.py ATT/patch_58_canonical_pricing_facade_sql_boundary.py ATT/tests/test_frente_58_canonical_pricing_facade_sql_boundary.py
    python -m pytest ATT/tests/test_frente_58_canonical_pricing_facade_sql_boundary.py -q
    python -m json.tool ATT/frente_58_canonical_pricing_facade_sql_boundary_report.json
    grep -RIn "sqlite3.connect\|import sqlite3\|sqlite_master\|PRAGMA table_info" services/canonical_pricing_facade.py repositories/canonical_pricing_facade_sql_boundary.py

Resultado local:

- py_compile sem erro.
- pytest com 4 passed.
- report JSON legivel.
- status do report: patched.
- moved_functions:
  - _get_structure_info
  - _lookup_spot_price
- skipped_sql_functions: vazio.
- git_executed: false.

### Evidencia de boundary

A varredura final confirmou que os tokens SQLite persistidos aparecem apenas no boundary:

- repositories/canonical_pricing_facade_sql_boundary.py contem import sqlite3.
- repositories/canonical_pricing_facade_sql_boundary.py contem sqlite3.connect.
- repositories/canonical_pricing_facade_sql_boundary.py contem sqlite_master.
- repositories/canonical_pricing_facade_sql_boundary.py contem PRAGMA table_info.

O arquivo services/canonical_pricing_facade.py nao apresentou ocorrencias desses tokens na
varredura direcionada.

### Observacao tecnica

Antes da execucao final, o script de patch local teve um repair pontual de sintaxe para
remover uma chave solta no proprio arquivo ATT/patch_58_canonical_pricing_facade_sql_boundary.py.
Apos o repair, o patch compilou, executou, gerou report e os testes da Frente 58 ficaram verdes.

Backup operacional registrado pelo report principal:

- ATT/backup_58_canonical_pricing_facade_sql_boundary_20260807_112235

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- SQL persistido concentrado em repositories.
- Camada service passa a delegar o acesso SQLite.
- Git nao executado.

### Posicao apos a Frente 58

A Frente 58 encerra localmente o recorte de contencao de SQL direto em
services/canonical_pricing_facade.py. O service ficou como camada de facade/delegacao e o
acesso persistido SQLite do recorte passou a residir em repositories.

<!-- FIM FRENTE 58 CANONICAL PRICING FACADE SQL BOUNDARY -->

<!-- INICIO PROXIMA ACAO POS FRENTE 58 -->

## Proxima acao pos Frente 58

A Frente 58 foi aplicada e validada localmente.

Proxima etapa recomendada:

- Seguir para o proximo alvo real de SQL boundary indicado pelo precheck da Frente 57.
- Manter a estrategia de uma frente pequena por vez.
- Preservar schema, persistencia, contratos publicos e execucao 100 por cento local.
- Nao executar git ate o encerramento e consolidacao final de todas as frentes.

Proximos candidatos naturais registrados apos a Frente 58:

- services/operational_data_status_service.py
- services/rtd_option_quotes_excel_sync.py
- services/payoff_refresh_command_service.py

Criterio de aceite da proxima frente:

- alvo real confirmado por varredura local;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao local sincronizada em docs;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

Comandos sugeridos para iniciar a proxima frente:

    python ATT/patch_57_local_sql_boundary_precheck.py
    python -m pytest ATT/tests/test_frente_57_local_sql_boundary_precheck.py -q
    python -m json.tool ATT/frente_57_local_sql_boundary_precheck_report.json

<!-- FIM PROXIMA ACAO POS FRENTE 58 -->

<!-- INICIO FRENTE 59 OPERATIONAL DATA STATUS SERVICE SQL BOUNDARY -->

## Frente 59 - Operational Data Status Service SQL Boundary

### Status

Aplicada localmente e validada.

### Contexto

A Frente 59 deu continuidade a reducao incremental de SQL direto fora de repositories,
db e infra, apos a Frente 58 ter removido o SQL direto de
services/canonical_pricing_facade.py.

O precheck pos Frente 58 indicou como proximo alvo recomendado:

- services/operational_data_status_service.py

O alvo foi classificado como risco high, com indicadores de acoplamento SQLite direto:

- import_sqlite3
- sqlite3_connect
- sqlite_master
- pragma_table_info
- execute_call
- select_sql

### Objetivo

Conter o SQL direto em services/operational_data_status_service.py, movendo o acesso
SQLite para um boundary persistido em repositories, sem alterar schema, persistencia,
contratos publicos ou comportamento externo esperado.

### Escopo aplicado

- Criado boundary local em repositories/operational_data_status_service_sql_boundary.py.
- services/operational_data_status_service.py passou a delegar o acesso SQLite para o boundary.
- Removido acoplamento direto com sqlite3 do service.
- Mantidas as chamadas publicas esperadas pelo service.
- SQL persistido ficou concentrado em repositories.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma alteracao operacional ampla foi feita.
- Nenhuma operacao de git foi executada.

### Simbolos movidos para o boundary

- build_operational_data_status
- _table_names
- _column_names
- _count_rows
- _count_distinct
- _max_text

### Arquivos principais

- services/operational_data_status_service.py
- repositories/operational_data_status_service_sql_boundary.py
- ATT/patch_59_operational_data_status_service_sql_boundary.py
- ATT/tests/test_frente_59_operational_data_status_service_sql_boundary.py
- ATT/frente_59_operational_data_status_service_sql_boundary_report.json

### Validacao local executada

Comandos executados localmente:

    python -m py_compile services/operational_data_status_service.py repositories/operational_data_status_service_sql_boundary.py ATT/patch_59_operational_data_status_service_sql_boundary.py ATT/tests/test_frente_59_operational_data_status_service_sql_boundary.py
    python -m pytest ATT/tests/test_frente_59_operational_data_status_service_sql_boundary.py -q
    python -m json.tool ATT/frente_59_operational_data_status_service_sql_boundary_report.json
    grep -RIn "sqlite3.connect\|import sqlite3\|sqlite_master\|PRAGMA table_info" services/operational_data_status_service.py repositories/operational_data_status_service_sql_boundary.py

Resultado local:

- py_compile sem erro.
- pytest com 5 passed.
- report JSON legivel.
- status do report: patched.
- service_forbidden_hits_after_patch: [].
- git_executed: false.

### Evidencia de boundary

A varredura final confirmou que os tokens SQLite persistidos aparecem apenas no boundary:

- repositories/operational_data_status_service_sql_boundary.py contem import sqlite3.
- repositories/operational_data_status_service_sql_boundary.py contem sqlite3.connect.
- repositories/operational_data_status_service_sql_boundary.py contem sqlite_master.
- repositories/operational_data_status_service_sql_boundary.py contem PRAGMA table_info.

O arquivo services/operational_data_status_service.py nao apresentou ocorrencias desses
tokens na varredura direcionada.

### Backup operacional

Backup principal registrado pelo report:

- ATT/backup_59_operational_data_status_service_sql_boundary_20260807_123536

### Repair local

Durante a validacao inicial, foi identificado problema de indentacao no service apos o
patch automatizado. Foi aplicado repair local controlado, reconstruindo o service a partir
de backup valido e preservando a delegacao para o boundary.

Evidencias do repair:

- repair_backup_dir: ATT/backup_59_rebuild_operational_data_status_service_20260807_124319
- repair_source_backup: ATT/backup_59_operational_data_status_service_sql_boundary_20260807_123536/operational_data_status_service.py
- service_forbidden_hits_after_patch: []

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- SQL persistido concentrado em repositories.
- Camada service passa a delegar o acesso SQLite.
- Git nao executado.

### Posicao apos a Frente 59

A Frente 59 encerra localmente o recorte de contencao de SQL direto em
services/operational_data_status_service.py. O service ficou como camada de delegacao e o
acesso persistido SQLite do recorte passou a residir em repositories.

<!-- FIM FRENTE 59 OPERATIONAL DATA STATUS SERVICE SQL BOUNDARY -->

<!-- INICIO PROXIMA ACAO POS FRENTE 59 -->

## Proxima acao pos Frente 59

A Frente 59 foi aplicada e validada localmente.

Proxima etapa recomendada:

- Executar novo precheck local pos Frente 59 para confirmar a reducao de achados e
  selecionar o proximo alvo real.
- Manter a estrategia de uma frente pequena por vez.
- Preservar schema, persistencia, contratos publicos e execucao 100 por cento local.
- Nao executar git ate o encerramento e consolidacao final de todas as frentes.

Proximos candidatos naturais conforme precheck pos Frente 58:

- services/rtd_option_quotes_excel_sync.py
- services/payoff_refresh_command_service.py
- UI/components/details_panel.py

Criterio de aceite da proxima frente:

- alvo real confirmado por varredura local;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao local sincronizada em docs;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

Comandos sugeridos antes da proxima frente:

    python -m pytest ATT/tests/test_frente_59_operational_data_status_service_sql_boundary.py -q
    python -m json.tool ATT/frente_59_operational_data_status_service_sql_boundary_report.json
    grep -RIn "sqlite3.connect\|import sqlite3\|sqlite_master\|PRAGMA table_info" services/operational_data_status_service.py repositories/operational_data_status_service_sql_boundary.py

<!-- FIM PROXIMA ACAO POS FRENTE 59 -->

<!-- INICIO FRENTE 60 PAYOFF REFRESH COMMAND SERVICE SQL BOUNDARY -->

## Frente 60 - Payoff Refresh Command Service SQL Boundary

### Status

Aplicada localmente e validada.

### Contexto

A Frente 60 deu continuidade a reducao incremental de SQL direto fora de repositories,
db e infra, apos a Frente 59 ter removido o SQL direto de
services/operational_data_status_service.py.

O alvo tecnico desta frente foi:

- services/payoff_refresh_command_service.py

O patch inicial e a versao v2 abortaram corretamente ao detectar tokens SQLite
remanescentes no service. A versao v3 aplicou o recorte de forma completa e validavel.

### Objetivo

Conter o SQL direto em services/payoff_refresh_command_service.py, movendo o acesso
SQLite do command service para um boundary persistido em repositories, sem alterar
schema, persistencia, contratos publicos ou comportamento externo esperado.

### Escopo aplicado

- Criado boundary local em repositories/payoff_refresh_command_service_sql_boundary.py.
- services/payoff_refresh_command_service.py passou a delegar o acesso SQLite para o boundary.
- Removido acoplamento direto com sqlite3 do command service.
- Mantidas as chamadas privadas esperadas pelo command service por delegacao.
- SQL persistido ficou concentrado em repositories.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma alteracao operacional ampla foi feita.
- Nenhuma operacao de git foi executada.

### Simbolos movidos para o boundary

Metodos movidos do command service para repositories/payoff_refresh_command_service_sql_boundary.py:

- PayoffRefreshCommandService._ensure_active_structure
- PayoffRefreshCommandService._connect
- PayoffRefreshCommandService._latest_payoff_summary
- PayoffRefreshCommandService._decision_exists
- PayoffRefreshCommandService._latest_snapshot_id

### Arquivos principais

- services/payoff_refresh_command_service.py
- repositories/payoff_refresh_command_service_sql_boundary.py
- ATT/patch_60_payoff_refresh_command_service_sql_boundary_v3.py
- ATT/tests/test_frente_60_payoff_refresh_command_service_sql_boundary.py
- ATT/frente_60_payoff_refresh_command_service_sql_boundary_report.json

### Validacao local executada

Comandos executados localmente:

    python -m py_compile services/payoff_refresh_command_service.py repositories/payoff_refresh_command_service_sql_boundary.py ATT/patch_60_payoff_refresh_command_service_sql_boundary_v3.py ATT/tests/test_frente_60_payoff_refresh_command_service_sql_boundary.py
    python -m pytest ATT/tests/test_frente_60_payoff_refresh_command_service_sql_boundary.py -q
    python -m json.tool ATT/frente_60_payoff_refresh_command_service_sql_boundary_report.json
    grep -RIn "sqlite3.connect\|import sqlite3\|sqlite_master\|PRAGMA table_info" services/payoff_refresh_command_service.py repositories/payoff_refresh_command_service_sql_boundary.py

Resultado local:

- py_compile sem erro.
- pytest com 5 passed.
- report JSON legivel.
- status do report: patched.
- service_forbidden_hits_after_patch: [].
- git_executed: false.

### Evidencia de boundary

A varredura final confirmou que os tokens SQLite persistidos aparecem apenas no boundary:

- repositories/payoff_refresh_command_service_sql_boundary.py contem import sqlite3.
- repositories/payoff_refresh_command_service_sql_boundary.py contem sqlite3.connect.
- repositories/payoff_refresh_command_service_sql_boundary.py contem PRAGMA table_info.

O arquivo services/payoff_refresh_command_service.py nao apresentou ocorrencias desses
tokens na varredura direcionada.

### Backups operacionais

Backups registrados durante a Frente 60:

- ATT/backup_60_payoff_refresh_command_service_sql_boundary_20260807_135404
- ATT/backup_60_payoff_refresh_command_service_sql_boundary_v2_20260807_135722
- ATT/backup_60_payoff_refresh_command_service_sql_boundary_v3_20260807_140012

O backup principal da aplicacao validada v3 foi:

- ATT/backup_60_payoff_refresh_command_service_sql_boundary_v3_20260807_140012

### Observacao tecnica

As tentativas anteriores abortaram corretamente com status de protecao:

- aborted_remaining_sqlite_tokens_in_service

Esse comportamento preservou o guardrail de evitar alteracao parcial quando ainda havia
tokens SQLite fortes no service. A aplicacao final validada foi realizada pela versao v3.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- SQL persistido concentrado em repositories.
- Camada command service passa a delegar o acesso SQLite.
- Git nao executado.

### Posicao apos a Frente 60

A Frente 60 encerra localmente o recorte de contencao de SQL direto em
services/payoff_refresh_command_service.py. O command service ficou como camada de
orquestracao/delegacao e o acesso persistido SQLite do recorte passou a residir em
repositories.

<!-- FIM FRENTE 60 PAYOFF REFRESH COMMAND SERVICE SQL BOUNDARY -->

<!-- INICIO PROXIMA ACAO POS FRENTE 60 -->

## Proxima acao pos Frente 60

A Frente 60 foi aplicada e validada localmente.

Proxima etapa recomendada:

- Executar novo precheck local pos Frente 60 para confirmar a reducao de achados e
  selecionar o proximo alvo real.
- Manter a estrategia de uma frente pequena por vez.
- Preservar schema, persistencia, contratos publicos e execucao 100 por cento local.
- Nao executar git ate o encerramento e consolidacao final de todas as frentes.

Proximos candidatos naturais ainda pendentes conforme rota recente:

- services/rtd_option_quotes_excel_sync.py
- UI/components/details_panel.py
- services/system_recalculation_command_service.py

Recomendacao operacional:

- Priorizar services/rtd_option_quotes_excel_sync.py somente se o precheck confirmar que
  ainda ha SQL direto relevante fora do repository.
- Caso o alvo RTD esteja parcialmente contido por frentes anteriores, seguir para
  UI/components/details_panel.py em recorte pequeno e reversivel.
- Evitar refatoracao ampla de UI ou RTD nesta etapa.

Criterio de aceite da proxima frente:

- alvo real confirmado por varredura local;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao local sincronizada em docs;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

Comandos sugeridos antes da proxima frente:

    python -m pytest ATT/tests/test_frente_60_payoff_refresh_command_service_sql_boundary.py -q
    python -m json.tool ATT/frente_60_payoff_refresh_command_service_sql_boundary_report.json
    grep -RIn "sqlite3.connect\|import sqlite3\|sqlite_master\|PRAGMA table_info" services/payoff_refresh_command_service.py repositories/payoff_refresh_command_service_sql_boundary.py

<!-- FIM PROXIMA ACAO POS FRENTE 60 -->
