!-- INICIO FRENTE 61 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 60 -->

## Frente 61 - Precheck local de SQLite fora de Boundary/Repository pos Frente 60

### Status

Concluida como precheck documental e tecnico.

A Frente 61 executou uma varredura local para identificar usos diretos de SQLite fora das camadas consideradas toleradas para acesso direto a banco, especialmente fora de repositories, db e infra.

Esta frente nao alterou codigo operacional, nao alterou schema, nao alterou persistencia e nao executou operacoes de Git.

### Objetivo

Mapear ocorrencias fortes de acesso direto a SQLite ainda presentes em camadas como:

- services
- UI
- controllers
- domain

A intencao foi produzir um diagnostico pos Frente 60 para orientar a proxima frente operacional de migracao para Boundary ou Repository.

### Escopo da varredura

Pastas analisadas:

- services
- UI
- controllers
- domain

Pastas excluidas:

- ATT
- docs
- repositories
- db
- infra
- scripts
- tools
- dados
- logs
- .git
- .pytest_cache
- __pycache__

As pastas repositories, db e infra foram tratadas como locais tolerados para SQLite direto nesta checagem.

### Tokens fortes pesquisados

A varredura procurou os seguintes padroes:

- import sqlite3
- sqlite3.connect
- sqlite_master
- PRAGMA table_info

### Resultado consolidado

- Arquivos analisados: 84
- Ocorrencias encontradas: 31
- Status do relatorio: precheck_completed
- Frente recomendada seguinte: 62
- Alvo recomendado: services/rtd_option_quotes_excel_sync.py

### Principais achados

O relatorio identificou usos diretos de SQLite nos seguintes arquivos principais:

- services/rtd_option_quotes_excel_sync.py
- UI/components/details_panel.py
- services/system_recalculation_command_service.py
- services/derived_payoff_persistence.py
- services/derived_service.py
- services/rtd_option_quotes_excel_populator.py
- services/rtd_option_quotes_intraday_candle_service.py
- services/rtd_option_quotes_intraday_history_service.py
- services/rtd_option_quotes_snapshot_status_service.py
- domain/payoff_features.py
- domain/refs/structure_ref.py

O alvo recomendado para a proxima frente foi:

    services/rtd_option_quotes_excel_sync.py

### Artefatos locais

- ATT/patch_61_local_sql_boundary_precheck_pos_frente_60_docs_fix.py
- ATT/tests/test_frente_61_local_sql_boundary_precheck_pos_frente_60_docs_fix.py
- ATT/frente_61_local_sql_boundary_precheck_pos_frente_60_report.json

### Validacao local sugerida

Comandos para validacao local:

    python ATT/patch_61_local_sql_boundary_precheck_pos_frente_60_docs_fix.py
    python -m pytest ATT/tests/test_frente_61_local_sql_boundary_precheck_pos_frente_60_docs_fix.py -q
    python -m json.tool ATT/frente_61_local_sql_boundary_precheck_pos_frente_60_report.json

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
- Documentacao local sincronizada nos documentos consolidados existentes.
- Documento separado docs/frente_61_local_sql_boundary_precheck_pos_frente_60.md nao deve permanecer como artefato final.
- Git nao executado.

### Proxima etapa recomendada

Abrir a Frente 62 para conter o SQL direto em services/rtd_option_quotes_excel_sync.py, desde que o alvo ainda seja confirmado pelo precheck local.

A Frente 62 deve manter o mesmo padrao operacional:

- um alvo real por vez;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao sincronizada nos arquivos consolidados;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

<!-- FIM FRENTE 61 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 60 -->

<!-- INICIO FRENTE 62 RTD OPTION QUOTES EXCEL SYNC SQL BOUNDARY -->

## Frente 62 - RTD Option Quotes Excel Sync SQL Boundary

### Status

Aplicada localmente, reparada e validada.

### Contexto

A Frente 62 deu continuidade a reducao incremental de SQL direto fora de repositories,
db e infra, apos o precheck local da Frente 61 ter recomendado como proximo alvo:

- services/rtd_option_quotes_excel_sync.py

O alvo ainda continha acoplamento SQLite direto em camada de service, incluindo uso de
sqlite3, sqlite3.connect, PRAGMA table_info e operacoes SQL diretas relacionadas a
cotacoes RTD de opcoes.

### Objetivo

Conter o SQL direto em services/rtd_option_quotes_excel_sync.py, delegando o acesso
persistido para repositories/rtd_option_quotes_repository.py, sem alterar schema,
persistencia, contratos publicos ou comportamento externo esperado.

### Escopo aplicado

- services/rtd_option_quotes_excel_sync.py passou a atuar como camada de service/delegacao.
- repositories/rtd_option_quotes_repository.py passou a concentrar o acesso SQLite do recorte.
- Foram removidos do service os tokens fortes de SQLite do recorte validado:
  - import sqlite3
  - sqlite3.connect
  - PRAGMA table_info
  - SQL direto operacional relacionado ao recorte
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma alteracao operacional ampla foi feita.
- Nenhuma operacao de git foi executada.

### Funcoes movidas/delegadas

Funcoes preservadas no service por delegacao fina:

- get_table_columns
- update_or_insert_quotes

Funcoes de boundary concentradas no repository:

- _frente62_get_table_columns_impl
- _frente62_update_or_insert_quotes_impl

### Arquivos principais

- services/rtd_option_quotes_excel_sync.py
- repositories/rtd_option_quotes_repository.py
- ATT/patch_62_rtd_option_quotes_excel_sync_sql_boundary.py
- ATT/tests/test_frente_62_rtd_option_quotes_excel_sync_sql_boundary.py
- ATT/frente_62_rtd_option_quotes_excel_sync_sql_boundary_report.json

### Repair local de sintaxe

Durante a validacao inicial, foi identificado problema de sintaxe relacionado a ordem de
from __future__ import annotations e ruido de escape no inicio dos arquivos alterados.

Foi aplicado repair local controlado:

- ATT/patch_62_fix_syntax_future_imports.py

O repair normalizou:

- services/rtd_option_quotes_excel_sync.py
- repositories/rtd_option_quotes_repository.py
- ATT/patch_62_rtd_option_quotes_excel_sync_sql_boundary.py
- ATT/tests/test_frente_62_rtd_option_quotes_excel_sync_sql_boundary.py

O report principal passou a registrar:

- syntax_repaired: true
- future_imports_normalized: true
- repair_backup_dir: ATT/backup_62_fix_syntax_future_imports_20260807_143136

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_62_rtd_option_quotes_excel_sync_sql_boundary.py
    python -m py_compile services/rtd_option_quotes_excel_sync.py repositories/rtd_option_quotes_repository.py ATT/patch_62_rtd_option_quotes_excel_sync_sql_boundary.py ATT/tests/test_frente_62_rtd_option_quotes_excel_sync_sql_boundary.py
    python -m pytest ATT/tests/test_frente_62_rtd_option_quotes_excel_sync_sql_boundary.py -q
    python -m json.tool ATT/frente_62_rtd_option_quotes_excel_sync_sql_boundary_report.json

Apos o repair de sintaxe/future imports, tambem foi executada validacao complementar de
guardrail de sintaxe.

Resultado local:

- py_compile sem erro.
- pytest principal com 6 passed.
- guard complementar com 10 passed.
- report JSON legivel.
- status do report: patched.
- service_forbidden_hits_after_patch: [].
- git_executed: false.

### Evidencia de boundary

A validacao final confirmou:

- services/rtd_option_quotes_excel_sync.py ficou sem tokens SQLite fortes do recorte.
- repositories/rtd_option_quotes_repository.py concentra as funcoes de acesso persistido.
- O service preserva os nomes funcionais esperados por delegacao.
- O repository contem as implementacoes de boundary da Frente 62.
- O report principal registra status patched.

### Backups operacionais

Backups registrados:

- ATT/backup_62_rtd_option_quotes_excel_sync_sql_boundary_20260807_142842
- ATT/backup_62_fix_syntax_future_imports_20260807_143136

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
- Camada service passa a delegar o acesso SQLite do recorte.
- Git nao executado.

### Posicao apos a Frente 62

A Frente 62 encerra localmente o recorte de contencao de SQL direto em
services/rtd_option_quotes_excel_sync.py. O service ficou como camada de delegacao e o
acesso persistido SQLite do recorte passou a residir em repositories/rtd_option_quotes_repository.py.

Proxima etapa recomendada:

- Executar novo precheck local para selecionar o proximo alvo real ainda fora de
  repositories, db e infra.
- Manter a estrategia de uma frente pequena por vez.
- Priorizar os candidatos remanescentes indicados pela Frente 61, como UI/components/details_panel.py
  ou services/system_recalculation_command_service.py, somente apos confirmacao por varredura local.
- Nao executar git ate a consolidacao final.

<!-- FIM FRENTE 62 RTD OPTION QUOTES EXCEL SYNC SQL BOUNDARY -->

<!-- INICIO FRENTE 63 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 62 -->

## Frente 63 - Precheck local de SQLite fora de Boundary/Repository pos Frente 62

### Status

Concluida como precheck documental e tecnico.

A Frente 63 executou uma nova varredura local apos a Frente 62 para confirmar a reducao
do foco no alvo recem tratado e selecionar o proximo alvo real ainda com SQL direto fora
das camadas toleradas.

Esta frente nao alterou codigo operacional, nao alterou schema, nao alterou persistencia
e nao executou operacoes de Git.

### Contexto

A Frente 62 removeu tokens SQLite fortes de:

- services/rtd_option_quotes_excel_sync.py

A Frente 63 foi aberta para confirmar se esse alvo permaneceu limpo apos a contencao e
identificar o proximo recorte operacional seguro.

### Objetivo

Mapear ocorrencias fortes e secundarias de SQL ou SQLite ainda presentes em camadas fora
de repositories, db e infra, especialmente em:

- services
- UI
- controllers
- domain

O objetivo foi produzir um diagnostico pos Frente 62 para orientar a Frente 64.

### Escopo da varredura

Pastas analisadas:

- services
- UI
- controllers
- domain

Pastas excluidas:

- ATT
- docs
- repositories
- db
- infra
- scripts
- tools
- dados
- logs
- .git
- .mypy_cache
- .pytest_cache
- .ruff_cache
- .venv
- venv
- env
- node_modules
- __pycache__

As pastas repositories, db e infra permaneceram como locais tolerados para acesso SQLite
direto nesta checagem.

### Tokens pesquisados

Tokens fortes:

- import sqlite3
- sqlite3.connect
- sqlite_master
- PRAGMA table_info

Tokens secundarios:

- execute
- SELECT
- INSERT
- UPDATE
- DELETE

### Resultado consolidado

- Arquivos analisados: 84
- Arquivos com achados: 25
- Status do relatorio: targets_found
- Frente recomendada seguinte: 64
- Alvo recomendado: UI/components/details_panel.py
- Risco do alvo recomendado: high
- Alvo recem tratado na Frente 62: services/rtd_option_quotes_excel_sync.py
- Tokens fortes remanescentes no alvo da Frente 62: nenhum

### Principais achados

O relatorio confirmou que services/rtd_option_quotes_excel_sync.py ficou sem tokens fortes
apos a Frente 62.

O proximo alvo recomendado foi:

    UI/components/details_panel.py

O alvo recomendado foi classificado como high por conter ocorrencias fortes de SQLite,
incluindo:

- import sqlite3
- sqlite3.connect
- sqlite_master
- PRAGMA table_info
- execute
- SELECT MAX

Outros candidatos relevantes permaneceram no mapa para frentes futuras, entre eles:

- services/system_recalculation_command_service.py
- services/derived_payoff_persistence.py
- services/derived_service.py
- services/rtd_option_quotes_excel_populator.py
- services/rtd_option_quotes_intraday_candle_service.py
- services/rtd_option_quotes_intraday_history_service.py
- services/rtd_option_quotes_snapshot_status_service.py
- domain/payoff_features.py
- domain/refs/structure_ref.py

### Artefatos locais

- ATT/patch_63_local_sql_boundary_precheck_pos_frente_62.py
- ATT/tests/test_frente_63_local_sql_boundary_precheck_pos_frente_62.py
- ATT/frente_63_local_sql_boundary_precheck_pos_frente_62_report.json

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_63_local_sql_boundary_precheck_pos_frente_62.py
    python -m py_compile ATT/patch_63_local_sql_boundary_precheck_pos_frente_62.py ATT/tests/test_frente_63_local_sql_boundary_precheck_pos_frente_62.py
    python -m pytest ATT/tests/test_frente_63_local_sql_boundary_precheck_pos_frente_62.py -q
    python -m json.tool ATT/frente_63_local_sql_boundary_precheck_pos_frente_62_report.json

Resultado local:

- py_compile sem erro.
- pytest com 5 passed.
- report JSON legivel.
- status do report: targets_found.
- just_patched_target_strong_hits_after_frente_62: vazio.
- recommended_next_target: UI/components/details_panel.py.
- recommended_next_front: 64.
- git_executed: false.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem alteracao operacional.
- Sem criacao de pasta nova na raiz.
- Patches, relatorios e testes permanecem em ATT.
- Git nao executado.

### Proxima etapa recomendada

Abrir a Frente 64 para conter o SQL direto em UI/components/details_panel.py, mantendo o
recorte pequeno, reversivel e validavel.

A Frente 64 deve preservar:

- contratos publicos;
- comportamento externo esperado da UI;
- schema existente;
- persistencia SQLite local;
- execucao 100 por cento local;
- ausencia de Web, HTTP ou API externa;
- ausencia de operacoes Git.

<!-- FIM FRENTE 63 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 62 -->

<!-- INICIO FRENTE 64 DETAILS PANEL SQL BOUNDARY -->

## Frente 64 - Details Panel SQL Boundary

### Status

Aplicada localmente e validada.

### Contexto

A Frente 64 deu continuidade a reducao incremental de SQL direto fora de repositories,
db e infra, apos a Frente 63 ter recomendado como proximo alvo:

- UI/components/details_panel.py

O alvo estava classificado como high por conter acoplamento SQLite direto dentro da camada
de UI, incluindo import sqlite3, sqlite3.connect, sqlite_master, PRAGMA table_info e SELECT
MAX.

### Objetivo

Conter o SQL direto em UI/components/details_panel.py, movendo as rotinas de consulta
persistida para um boundary local em repositories, sem alterar schema, persistencia,
contratos publicos ou comportamento externo esperado.

### Escopo aplicado

- Criado boundary local em repositories/details_panel_sql_boundary.py.
- UI/components/details_panel.py passou a delegar consultas persistidas para o boundary.
- Removidos da UI os tokens fortes do recorte validado:
  - import sqlite3
  - sqlite3.connect
  - sqlite_master
  - PRAGMA table_info
  - SELECT MAX
- A UI permaneceu como camada de apresentacao e orquestracao.
- SQL persistido ficou concentrado em repositories.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma alteracao operacional ampla foi feita.
- Nenhuma operacao de git foi executada.

### Metodos extraidos para boundary

Metodos extraidos do DetailsPanel para repositories/details_panel_sql_boundary.py:

- _latest_snapshot_timestamp_in_db
- _table_names
- _table_columns
- _max_timestamp_for_structure_column

Total de metodos extraidos:

- 4

### Arquivos principais

- UI/components/details_panel.py
- repositories/details_panel_sql_boundary.py
- ATT/patch_64_details_panel_sql_boundary.py
- ATT/tests/test_frente_64_details_panel_sql_boundary.py
- ATT/frente_64_details_panel_sql_boundary_report.json

### Validacao local executada

Comandos executados localmente:

    python ATT/patch_64_details_panel_sql_boundary.py
    python -m py_compile ATT/patch_64_details_panel_sql_boundary.py ATT/tests/test_frente_64_details_panel_sql_boundary.py UI/components/details_panel.py repositories/details_panel_sql_boundary.py
    python -m pytest ATT/tests/test_frente_64_details_panel_sql_boundary.py -q
    python -m json.tool ATT/frente_64_details_panel_sql_boundary_report.json

Resultado local:

- py_compile sem erro.
- pytest com 6 passed.
- report JSON legivel.
- status do report: patched.
- ui_forbidden_hits_after_patch: vazio.
- boundary_has_sql: true.
- git_executed: false.

### Evidencia de boundary

A varredura direcionada confirmou que os tokens SQLite fortes nao permanecem no alvo de UI
e aparecem apenas no boundary criado:

- repositories/details_panel_sql_boundary.py contem import sqlite3.
- repositories/details_panel_sql_boundary.py contem sqlite3.connect.
- repositories/details_panel_sql_boundary.py contem sqlite_master.
- repositories/details_panel_sql_boundary.py contem PRAGMA table_info.
- repositories/details_panel_sql_boundary.py contem SELECT MAX.
- UI/components/details_panel.py nao apresentou ocorrencias desses tokens na varredura direcionada.

Comando executado:

    grep -RInE "import sqlite3|sqlite3\.connect|sqlite_master|PRAGMA table_info|pragma table_info|SELECT MAX" UI/components/details_panel.py repositories/details_panel_sql_boundary.py

Resultado observado:

- ocorrencias apenas em repositories/details_panel_sql_boundary.py.

### Backup operacional

Backup registrado pelo report:

- ATT/backup_64_details_panel_sql_boundary_20260807_144556

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
- Camada UI passa a delegar acesso SQLite do recorte.
- Git nao executado.

### Posicao apos a Frente 64

A Frente 64 encerra localmente o recorte de contencao de SQL direto em
UI/components/details_panel.py. O DetailsPanel ficou sem tokens SQLite fortes do recorte
validado e o acesso persistido passou a residir em repositories/details_panel_sql_boundary.py.

### Proxima etapa recomendada

Executar novo precheck local pos Frente 64 para confirmar a reducao de achados e selecionar
o proximo alvo real.

Candidatos naturais ainda indicados pela rota recente:

- services/system_recalculation_command_service.py
- services/derived_payoff_persistence.py
- services/derived_service.py
- services/rtd_option_quotes_excel_populator.py
- services/rtd_option_quotes_intraday_candle_service.py
- services/rtd_option_quotes_intraday_history_service.py
- services/rtd_option_quotes_snapshot_status_service.py
- domain/payoff_features.py
- domain/refs/structure_ref.py

A proxima frente deve manter:

- um alvo real por vez;
- recorte pequeno, reversivel e validavel;
- patch, teste e report em ATT;
- documentacao sincronizada nos arquivos consolidados;
- sem Web, HTTP, API externa, alteracao de schema ou troca de persistencia;
- sem git nesta etapa.

<!-- FIM FRENTE 64 DETAILS PANEL SQL BOUNDARY -->

<!-- INICIO FRENTE 65 LOCAL SQL BOUNDARY PRECHECK POS FRENTE 64 -->

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

Status: inventario local criado.

Escopo: services/derived_service.py.

Achados totais: 23.

Decisao: nao alterar codigo operacional nesta frente. A proxima frente deve remover um bloco real por vez, preferencialmente via repository.

Validacoes:

- python -m json.tool ATT/frente_73_derived_service_sql_boundary_inventory_report.json
- pytest -q ATT/tests/test_frente_73_derived_service_sql_boundary_inventory.py

END_FRENTE_73_DERIVED_SERVICE_SQL_BOUNDARY_INVENTORY
