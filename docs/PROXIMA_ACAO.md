# PROXIMA ACAO

<!-- INICIO PROXIMA ACAO FRENTE 54I SQL DIRETO UI DATA INCREMENTAL -->

## Próxima ação — Frente 54i

### Direção

Continuar a redução incremental de SQL direto em UI/models/ui_data.py, após as frentes 54c, 54d, 54e, 54f, 54g e 54h já terem isolado pontos específicos de metadata, listagem de estruturas, decisões e payoff curve exato.

### Estado de partida

Últimas frentes locais já aplicadas e validadas:

- Frente 54c: isolamento de list_tables em db/app_metadata_repo.py.
- Frente 54d: isolamento de inspect_columns em db/app_metadata_repo.py.
- Frente 54e: isolamento da listagem distinta de structure_id em repository local de query.
- Frente 54f: isolamento da subquery e fetch de decisões em db/ui_data_query_repo.py.
- Frente 54f v2: repair local de indentação em decision_subquery, com compile OK.
- Frente 54g: isolamento da montagem SQL final de decisões em db/ui_data_query_repo.py.
- Frente 54g v2: repair local do token documental e guardrail WHERE_SQL, com testes verdes.
- Frente 54h: isolamento da montagem SQL e fetch do payoff curve exato em db/ui_data_query_repo.py.

Validação local após a Frente 54h:

- Compile de UI/models/ui_data.py: OK.
- Compile de db/ui_data_query_repo.py: OK.
- Compile do teste local da 54h: OK.
- Teste local da 54h: 4 passed.
- Git: não executado.
- Schema: não alterado.
- Contratos públicos: não alterados.
- Persistência: não alterada.
- Refatoração ampla: não executada.

Varredura local após a Frente 54h em UI/models/ui_data.py:

- SELECT: 5 ocorrências.
- INSERT: 0 ocorrência.
- UPDATE: 0 ocorrência.
- DELETE: 0 ocorrência.
- PRAGMA: 0 ocorrência.
- sqlite_master: 0 ocorrência.
- .execute: 6 ocorrências.
- sqlite3: 5 ocorrências, concentradas em import e conexão local.

### Objetivo da Frente 54i

Iniciar a Frente 54i com apenas um ponto real remanescente em UI/models/ui_data.py.

Candidato recomendado para a 54i:

- Isolar o recorte de timestamp mais recente de payoff curve:
  - _build_payoff_curve_latest_timestamp_sql
  - _fetch_payoff_curve_latest_timestamp

Direção sugerida:

- mover a montagem do SQL de timestamp mais recente para db/ui_data_query_repo.py;
- mover o fetch correspondente para o mesmo repository local;
- manter os métodos em UIDataModel como delegadores finos, para preservar compatibilidade interna;
- não alterar schema;
- não alterar contratos públicos;
- não alterar persistência;
- não fazer refatoração ampla;
- manter a frente limitada ao menor recorte validável.

### Restrições

- Não executar git.
- Não criar pasta nova na raiz.
- Usar ATT/ para patch, backup, relatório e testes locais.
- Usar ATT/tests/ para teste local da frente.
- Manter alteração automatizada e indentada via Git Bash.
- Não migrar para web.
- Não ampliar escopo para outras UIs ou services.
- Não usar crase em conteúdo documental gerado.

### Validação esperada

A Frente 54i deve gerar validação local equivalente ao padrão anterior:

- backup em ATT/backup_54i_*;
- relatório JSON em ATT/frente_54i_*_report.json;
- teste local em ATT/tests/test_frente_54i_*_local.py;
- py_compile para UI/models/ui_data.py;
- py_compile para db/ui_data_query_repo.py;
- py_compile para o teste local criado;
- teste local passando;
- grep final demonstrando redução incremental de SQL direto no método alvo da UI.

### Resultado esperado

Ao final da Frente 54i:

- o SQL de timestamp mais recente de payoff curve não deve permanecer montado diretamente no método alvo da UI;
- a UI deve delegar esse recorte para db/ui_data_query_repo.py;
- a contagem de SELECT em UI/models/ui_data.py deve reduzir incrementalmente;
- a contagem de .execute em UI/models/ui_data.py deve reduzir incrementalmente se o fetch também for movido;
- não deve haver alteração de schema;
- não deve haver alteração de contratos públicos;
- git deve permanecer não executado.

<!-- FIM PROXIMA ACAO FRENTE 54I SQL DIRETO UI DATA INCREMENTAL -->

<!-- INICIO PROXIMA ACAO POS FRENTE 54 CONSOLIDADA -->

## Próxima ação — Pós Frente 54 consolidada

### Direção

A Frente 54 está consolidada localmente no recorte UI/models/ui_data.py e db/ui_data_query_repo.py.

A próxima etapa deve continuar a redução controlada de SQL direto fora das camadas permitidas,
mas sem reabrir a boundary já estabilizada da Frente 54, salvo correção pontual de regressão.

### Estado de partida

Validação final conhecida da Frente 54q:

- compile direcionado OK;
- pytest direcionado das frentes 54h, 54i, 54j, 54k, 54l, 54l v2, 54o, 54p e 54q com 35 passed;
- UI/models/ui_data.py sem SQL direto, execute ou sqlite3 no recorte validado;
- db/ui_data_query_repo.py concentrando sqlite3, conexão, row_factory, SQL e execute;
- documentação local de boundary e consolidação atualizada;
- git não executado.

### Próximo passo recomendado

Preparar a próxima frente com pré-checagem local antes de qualquer alteração operacional.

A recomendação é iniciar uma nova frente pós 54 para auditar os candidatos remanescentes de
SQL direto fora de repositories, escolhendo apenas um alvo real por vez.

Possíveis candidatos devem ser reavaliados por scanner local atualizado, sem assumir que
relatórios antigos ainda representam o estado atual.

### Restrições

- Não executar git.
- Não alterar schema.
- Não trocar persistência.
- Não introduzir Web, HTTP ou API externa.
- Não fazer refatoração ampla.
- Não criar pasta nova na raiz.
- Manter patches, backups, relatórios e testes locais em ATT.
- Manter documentação local sincronizada em docs.
- Executar git somente ao final de todas as frentes.

### Critério de aceite da próxima frente

A próxima frente deve conter:

- patch automatizado;
- backup local;
- relatório JSON em ATT;
- teste local específico em ATT/tests;
- compile dos arquivos afetados;
- pytest direcionado;
- documentação atualizada se houver mudança de arquitetura ou boundary;
- confirmação explícita de que git não foi executado.

<!-- FIM PROXIMA ACAO POS FRENTE 54 CONSOLIDADA -->

<!-- INICIO PROXIMA ACAO FRENTE 55B REDUCAO SQL DIRETO POS 54 -->

## Proxima acao — Frente 55b

### Direcao

Dar continuidade a reducao incremental de SQL direto fora de repositories, db e infra,
apos a consolidacao da Frente 54 em UI/models/ui_data.py e a prechecagem local da Frente 55a.

### Estado de partida

- Frente 54q consolidou o boundary UIData x repository.
- Frente 54r atualizou a documentacao local pos-consolidacao.
- Frente 55a confirmou o estado pos-Frente 54 e selecionou o proximo alvo real.
- UI/models/ui_data.py deve permanecer fora do escopo operacional imediato, pois ja foi
  consolidado na Frente 54.

### Candidato recomendado

- Alvo: UI/components/terminal_vwap_payoff_dark_panel.py
- Prioridade: alta

### Objetivo da Frente 55b

Aplicar apenas um recorte pequeno e reversivel no alvo recomendado pela Frente 55a,
reduzindo SQL direto ou acoplamento SQLite real fora das camadas permitidas.

### Restricoes

- Nao executar git.
- Nao criar pasta nova na raiz.
- Usar ATT para patch, backup, relatorio e temporarios.
- Usar ATT/tests para teste local da frente.
- Manter alteracao automatizada e indentada via Git Bash.
- Nao migrar para Web.
- Nao introduzir HTTP.
- Nao introduzir API externa.
- Nao alterar schema.
- Nao trocar persistencia.
- Nao fazer refatoracao ampla.
- Nao reabrir UI/models/ui_data.py salvo para guardrail de regressao.

### Validacao esperada

- Backup em ATT.
- Relatorio JSON em ATT.
- Teste local em ATT/tests.
- py_compile dos arquivos alterados.
- Teste local passando.
- Grep final demonstrando reducao incremental no metodo ou recorte alvo.
- Documentacao local atualizada.
- Git permanecendo nao executado.

<!-- FIM PROXIMA ACAO FRENTE 55B REDUCAO SQL DIRETO POS 54 -->

<!-- INICIO PROXIMA ACAO POS FRENTE 55B -->

## Proxima acao — Pos Frente 55b

### Direcao

Continuar a reducao incremental de SQL direto fora de repositories, db e infra,
sem reabrir o recorte estabilizado da Frente 55b, salvo correcao pontual de regressao.

### Estado de partida

- Frente 54q consolidou o boundary UIDataModel x db/ui_data_query_repo.py.
- Frente 54r atualizou a documentacao local pos-consolidacao.
- Frente 55a selecionou UI/components/terminal_vwap_payoff_dark_panel.py como alvo real.
- Frente 55b removeu SQL direto do alvo UI/components/terminal_vwap_payoff_dark_panel.py
  e concentrou a persistencia em repositories/terminal_vwap_payoff_snapshot_repository.py.
- Teste direcionado da Frente 55b passou com 6 passed.
- Git permaneceu nao executado.

### Proximo passo recomendado

Executar nova prechecagem local antes de qualquer nova alteracao operacional, escolhendo
somente um alvo real por vez entre os remanescentes fora das camadas permitidas.

Possiveis candidatos devem ser reavaliados por scanner local atualizado, sem assumir que
relatorios antigos ainda representam o estado atual.

### Restricoes

- Nao executar git.
- Nao alterar schema.
- Nao trocar persistencia.
- Nao introduzir Web.
- Nao introduzir HTTP.
- Nao introduzir API externa.
- Nao fazer refatoracao ampla.
- Nao criar pasta nova na raiz.
- Manter patches, backups, relatorios e testes locais em ATT.
- Manter testes locais em ATT/tests.
- Manter documentacao local sincronizada em docs.
- Executar git somente ao final de todas as frentes.

### Criterio de aceite da proxima frente

A proxima frente deve conter:

- patch automatizado;
- backup local;
- relatorio JSON em ATT;
- teste local especifico em ATT/tests;
- compile dos arquivos afetados;
- pytest direcionado;
- grep final do alvo operacional;
- documentacao atualizada se houver mudanca de boundary;
- confirmacao explicita de que git nao foi executado.

<!-- FIM PROXIMA ACAO POS FRENTE 55B -->

<!-- INICIO FRENTE 56 UI DATA PAYOFF CURVE CONNECTION LIFECYCLE -->

## Frente 56 - UIDataModel.get_payoff_curve com ciclo de conexao seguro

### Objetivo

A Frente 56 executa uma correcao pontual prevista no plano de contencao:
garantir que UIDataModel.get_payoff_curve ou rotina equivalente de payoff curve
nao mantenha conexao SQLite aberta apos montar ou retornar a curva de payoff.

### Arquivo alvo

- UI/models/ui_data.py

### Escopo aplicado

- Contencao local de ciclo de vida de conexao.
- Fechamento garantido via try/finally quando ha sqlite3.connect direto sem guardrail.
- Deteccao tolerante quando get_payoff_curve nao existe no arquivo atual.
- Sem alteracao de schema.
- Sem criacao de tabela.
- Sem alteracao de contrato financeiro.
- Sem migracao para web.
- Sem HTTP, API externa ou dependencia remota.
- Sem execucao de git.

### Evidencia esperada

Validacao local:

    python -m py_compile ATT/patch_56_ui_data_payoff_curve_connection_lifecycle.py UI/models/ui_data.py ATT/tests/test_frente_56_ui_data_payoff_curve_connection_lifecycle.py
    python -m pytest ATT/tests/test_frente_56_ui_data_payoff_curve_connection_lifecycle.py -q
    python -m json.tool ATT/frente_56_ui_data_payoff_curve_connection_lifecycle_report.json

### Observacao de robustez

Se o metodo get_payoff_curve nao existir mais em UI/models/ui_data.py, a frente nao deve quebrar.
Nesse caso, o report registra target_method_not_found_no_action e os testes validam que nao ha
candidato de payoff curve com sqlite3.connect aberto sem fechamento.

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
