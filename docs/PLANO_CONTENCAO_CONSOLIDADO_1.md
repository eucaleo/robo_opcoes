# Plano de Contencao Consolidado

Documento local de desenvolvimento mantido conforme o plano efetivo.


## Frente 42 - Pricing execution envelope contract

- Status: aplicada localmente.
- Fase: Fase 4 - Pricing e payoff.
- Objetivo: criar contrato canonico para envelope de retorno do pricing.
- Resultado: Envelope canonico de pricing criado em services/pricing_execution_envelope.py.
- Teste local: ATT/tests/test_frente_42_pricing_execution_envelope_contract.py.
- Relatorio local: ATT/frente_42_pricing_execution_envelope_contract_report.json.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

Observacao:
- A antecipacao parcial entre Fase 3 e Fase 6 ficou limitada a normalizacao/parser.
- A Frente 42 reposiciona a execucao na Fase 4, sem alterar banco, schema ou fluxo operacional amplo.
\n
## Frente 43 — Integracao envelope canonico fluxo pricing

- Frente 43 aplicada localmente.
- Integracao envelope canonico fluxo pricing.
- Fase 4 - Pricing e payoff.
- Objetivo: iniciar integracao controlada do envelope canonico criado na Frente 42 nos services de pricing.
- Arquivos alvo:
  - services/pricing_execution_orchestration_service.py
  - services/pricing_execution_app_service.py
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 43 v2 - correcao de literal backslash-n

- Frente: 43 v2.
- Ajuste: remocao de linha literal backslash-n isolada inserida nos arquivos do fluxo de pricing.
- Arquivos conferidos:
  - services/pricing_execution_orchestration_service.py
  - services/pricing_execution_app_service.py
- Objetivo: restaurar py_compile e importacao dos adaptadores da Frente 43.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
- Proxima frente mantida: Frente 44 - propagacao controlada envelope retorno pricing.
- Gerado em: 2026-07-31T21:51:53.

## Frente 44 - Propagacao controlada envelope retorno pricing

- Status: aplicada localmente.
- Fase: Fase 4 - Pricing e payoff.
- Objetivo: propagar retorno de pricing no envelope canonico minimo nos services de pricing.
- Escopo: controlado, local e reversivel.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
- Observacao: mantem a sobreposicao anterior apenas como registro documental de normalizacao/parser, sem ampliar escopo.
\n## Frente 45 - Estabilizacao envelope query retorno pricing

- Frente 45
- Estabilizacao envelope query retorno pricing
- Fase 4 - Pricing e payoff
- Objetivo: estabilizar retornos de consulta de pricing no envelope canonico minimo.
- Arquivo alvo: services/pricing_execution_query_service.py
- Contrato preservado: status, error_message, pricing_payload, engine_result, persisted e pricing_execution_id.
- Sem troca de persistencia
- Sem troca de schema
- Sem alteracao operacional ampla
- Nenhuma operacao de versionamento executada
- Observacao: esta frente apenas cria adaptador conservador de retorno para query, sem alterar banco, repository ou fluxo de gravacao.\n

## Frente 45 v2 - Fix literal backslash-n query envelope

- Frente 45 v2
- Fix literal backslash-n query envelope
- Corrigido SyntaxError causado por bloco com \n literal em services/pricing_execution_query_service.py.
- Guardrail ajustado para procurar backslash-n literal, sem bloquear quebras de linha normais.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 46 - Porta PricingEngine controlada

- Frente 46 aplicada localmente.
- Porta PricingEngine controlada criada em services/pricing_engine_port.py.
- Contrato PricingEnginePort formalizado com metodo run(pricing_payload) -> dict.
- Helper run_pricing_engine() criado para chamada controlada do motor.
- PricingEngineStub permanece disponivel apenas para desenvolvimento/teste.
- Sem troca de engine real.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 47 - Fortalecimento validacao payload pricing payoff

- Frente 47 aplicada localmente.
- Fortalecimento validacao payload pricing payoff.
- Criado modulo services/pricing_payoff_payload_validation.py.
- Criadas validacoes controladas para payload minimo de pricing/payoff.
- CALL/PUT nao possui default perigoso.
- Position side nao possui default perigoso.
- Campo price e tratado como ambiguo e gera warning, preservando separacao entre premium, entry_premium e current_price.
- Esta frente apenas valida e retorna diagnostico estruturado.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

## Frente 48 - Validacao controlada payoff calculation request

Frente aplicada localmente para adicionar validação controlada do payload de payoff em domain/calculation_request.py,
mantendo a contenção da Fase 4 - Pricing e payoff.

Garantias:
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.

### Frente 49 - Correcao pontual bugs UI fluxo payoff

Frente local aplicada para conter bugs pontuais do fluxo de payoff na UI:
metodo preparador de decisoes recarregadas, selecao por structure_id com timestamp opcional
quando aplicavel, ponto defensivo de carregamento de estrutura no painel Terminal VWAP/Payoff
e guardrail documental para evitar vazamento de conexao em get_payoff_curve.

Sem troca de persistencia. Sem troca de schema. Sem alteracao operacional ampla.
Nenhuma operacao de versionamento executada.

### Frente 50 - Reducao SQL direto UI services criticos

Frente local aplicada para iniciar reducao controlada de SQL direto em UI/services
criticos por meio de inventario tecnico sql_direct_usage_inventory.

A Frente 50 nao substitui persistencia, nao altera schema e nao muda comportamento
operacional amplo. O inventario serve como base para migracoes pontuais posteriores
para repositories/services.
## Frente 51 - Reduzir SQL direto payoff UI services por prioridade

Priorizacao local criada para orientar a retirada incremental de SQL direto em UI/services relacionados a payoff.
A Frente 51 nao executa migracao de schema, nao troca persistencia e nao altera fluxo operacional amplo.

<!-- INICIO FRENTE 51 VALIDACAO LOCAL HOTFIX 51D -->

## Frente 51 — Validação local consolidada da priorização de SQL direto payoff UI/services

A Frente 51 foi aplicada localmente e validada como etapa da Fase 5 — UI e
command services.

Objetivo consolidado:

- reduzir SQL direto em UI/services relacionados a payoff por meio de inventário
  técnico priorizado;
- orientar a próxima retirada incremental de SQL direto;
- preservar contratos existentes;
- não alterar banco, schema, persistência ou fluxo operacional amplo.

Artefatos consolidados:

- services/sql_direct_usage_prioritizer.py
- ATT/frente_51_sql_direto_payoff_ui_services_priority.json
- ATT/tests/test_frente_51_reduzir_sql_direto_payoff_ui_services_por_prioridade.py

Correção local complementar:

- aplicado hotfix 51d para remover risco de travamento na rotina de stripping de
  prefixos literais;
- mantida implementação sem loop para evitar nova interrupção durante análise de
  previews;
- reduzidos falsos positivos Python na priorização.

Validação local:

- bash ATT/verify_erros_frente_51.sh
- Resultado: Nenhum erro detectado pelo verificador da Frente 51.
- pytest direcionado: 5 passed.
- Inventário final priorizado: 29 candidatos.
- Distribuição final:
  - P0: 18
  - P1: 5
  - P2: 5
  - P3: 1

Limites preservados:

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional ampla.
- Nenhuma operação de versionamento executada.
- Sem git até o encerramento geral das frentes.
- Sistema permanece 100 por cento local.

Continuidade:

A próxima frente técnica deve avançar para a Frente 52, focada na redução
incremental de SQL direto nos candidatos P0/P1, sem mudar contratos e sem
refatoração ampla.

<!-- FIM FRENTE 51 VALIDACAO LOCAL HOTFIX 51D -->
<!-- INICIO FRENTE 52 REFINAR PRIORIZACAO SQL DIRETO P0 P1 -->

## Frente 52 — Refinar priorização de SQL direto P0/P1 sem alterar contratos

### Status

Aplicada localmente.

### Objetivo

Refinar o inventário priorizado produzido na Frente 51 para reduzir falso-positivos
antes da retirada incremental de SQL direto em UI/services relacionados a payoff.

A Frente 52 atua somente sobre a classificação técnica dos candidatos. Ela não remove
SQL direto de arquivos operacionais, não cria schema, não troca persistência e não
altera fluxo operacional amplo.

### Escopo aplicado

- Entrada analisada: ATT/frente_51_sql_direto_payoff_ui_services_priority.json.
- Saída refinada: ATT/frente_52_sql_direto_payoff_ui_services_priority_refined.json.
- Remoção de falso-positivos evidentes:
  - .join(...) de Python sem SQL real;
  - .update(...) de dicionário/widget sem UPDATE SQL;
  - .insert(...) de UI/Python sem INSERT INTO;
  - .select(...) de métodos/selectors sem SELECT SQL.
- Criação de guardrail local em ATT/tests/test_frente_52_refinar_priorizacao_sql_direto_p0_p1.py.
- Criação de relatório local em ATT/frente_52_refinar_priorizacao_sql_direto_p0_p1_report.json.

### Resultado local esperado

Inventário refinado:

- Total de candidatos após refinamento: 15.
- P0: 12.
- P1: 0.
- P2: 3.
- P3: 0.
- Achados removidos como falso-positivo: 54.

### Guardrails preservados

- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de versionamento executada.
- Sem criacao de pasta nova na raiz.
- Patches e temporarios permanecem em ATT.
- Testes permanecem em ATT/tests.

### Próxima etapa sugerida

Após validar a Frente 52, a próxima frente deve atacar somente os candidatos P0/P1
remanescentes que tenham SQL direto real, um arquivo por vez, preferencialmente
começando por UI/components/details_panel.py ou UI/models/ui_data.py, sem mudar
schema, persistência ou contratos públicos.

<!-- FIM FRENTE 52 REFINAR PRIORIZACAO SQL DIRETO P0 P1 -->

## Frente 53 — Reduzir SQL direto real P0 sem alterar contratos

Status: preparada para execução técnica local.

A Frente 53 parte do inventário refinado da Frente 52:

- Fonte: ATT/frente_52_sql_direto_payoff_ui_services_priority_refined.json
- Relatório de pré-checagem: ATT/frente_53_reduzir_sql_direto_p0_precheck_report.json
- Teste de pré-checagem: ATT/tests/test_frente_53_reduzir_sql_direto_p0_precheck.py
- Total de candidatos refinados encontrados: 15
- Candidatos P0 encontrados: 12
- Primeiro alvo sugerido: UI\components\terminal_vwap_payoff_dark_panel.py

Escopo permitido:

- Reduzir SQL direto somente em candidatos reais classificados como P0.
- Preservar contratos públicos.
- Não alterar schema.
- Não alterar comportamento operacional.
- Não fazer versionamento.

Critério para a próxima etapa:

- Escolher um único candidato P0.
- Aplicar patch mínimo e reversível.
- Criar teste específico validando ausência de regressão contratual.
- Atualizar relatório da Frente 53 com antes/depois.<!-- INICIO FRENTE 53A VALIDACAO LOCAL DERIVED REPO PAYOFF PANEL -->

## Frente 53a — Terminal VWAP Payoff Dark Panel consumindo derived_repo

### Status

Aplicada localmente e validada.

### Contexto

A Frente 53a deu continuidade à Frente 53, que iniciou a redução controlada de SQL direto real P0 em UI/services relacionados a payoff.

O primeiro alvo técnico permaneceu o arquivo:

- UI/components/terminal_vwap_payoff_dark_panel.py

A alteração foi feita de forma local, incremental e reversível, preservando o contrato operacional do painel Terminal VWAP/Payoff.

### Objetivo

Reduzir SQL direto no painel Terminal VWAP/Payoff para os pontos relacionados a:

- payoff_curve_points;
- structure_decisions.

A UI passou a preferir métodos consolidados em db/derived_repo.py, evitando acesso direto da camada de interface às tabelas sensíveis de payoff e decisões.

### Escopo aplicado

- Remoção de import sqlite3 do painel Terminal VWAP/Payoff Dark Panel.
- Remoção de SQL direto contra structure_decisions no painel.
- Remoção de SQL direto contra payoff_curve_points no bloco inspecionado pelo guardrail da Frente 53a.
- Preservação da ponte local com db/derived_repo.py.
- Preservação do comportamento operacional do painel.
- Sem alteração de schema.
- Sem troca de persistência.
- Sem alteração operacional ampla.
- Nenhuma operação de versionamento executada.

### Validação local executada

Foram executadas validações locais direcionadas com sucesso.

Comando de compilação:

    python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py db/derived_repo.py

Teste específico da Frente 53a:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py -q

Resultado:

    4 passed

Bateria direcionada do Terminal VWAP/Payoff:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_app_service.py -q

Resultado:

    49 passed

### Guardrails preservados

- Sem git nesta etapa.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sistema permanece 100 por cento local.
- UI não deve acessar diretamente payoff_curve_points nem structure_decisions para os pontos cobertos pela Frente 53a.
- A continuidade da redução de SQL direto deve seguir um arquivo por vez, com teste específico.

### Posição do projeto após a Frente 53a

O projeto permanece na Fase 5 — UI e command services, dentro do eixo de redução incremental de SQL direto fora de repositories.

A Frente 53a conclui a primeira retirada validada no alvo P0 Terminal VWAP/Payoff Dark Panel. A próxima etapa técnica recomendada é continuar a Frente 53 em novo recorte pequeno, preferencialmente como Frente 53b, escolhendo apenas um próximo candidato P0 real do inventário refinado da Frente 52.

Candidatos naturais para análise seguinte, conforme o plano consolidado, são:

- UI/components/details_panel.py
- UI/models/ui_data.py

A escolha deve ser feita somente após nova pré-checagem local, preservando contratos públicos, sem alteração de schema, sem troca de persistência e sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 53A VALIDACAO LOCAL DERIVED REPO PAYOFF PANEL -->

<!-- INICIO FRENTE 53B SELECT NEXT P0 SQL DIRECT TARGET -->

## Frente 53b — Seleção do próximo alvo P0 real para redução de SQL direto

### Status

Preparada localmente por patch automatizado e pendente de validação local.

### Objetivo

Dar continuidade à Frente 53 após a conclusão validada da Frente 53a, mantendo a
redução incremental de SQL direto real em UI/services relacionados a payoff.

A Frente 53b não altera código operacional. Ela seleciona o próximo alvo P0 real
com base no inventário refinado da Frente 52 e na inspeção local do fonte atual.

### Resultado da seleção local

- Inventário de origem: ATT/frente_52_sql_direto_payoff_ui_services_priority_refined.json
- Alvo já tratado e excluído da seleção: UI/components/terminal_vwap_payoff_dark_panel.py
- Próximo alvo selecionado: UI/components/details_panel.py
- Linhas com evidência de SQL direto no alvo selecionado: 23
- Total de candidatos P0 reais encontrados para continuidade: 14

### Escopo preservado

- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional ampla.
- Nenhuma operação de versionamento executada.
- Sem criação de pasta nova na raiz.
- Patch e relatório permanecem em ATT.
- Teste permanece em ATT/tests.
- Sistema permanece 100 por cento local.

### Próxima etapa recomendada

Após validar esta seleção, executar a retirada incremental no alvo selecionado como
um patch pequeno e reversível, preferindo repository/service já existente sempre que
possível e criando guardrail específico para impedir regressão.

<!-- FIM FRENTE 53B SELECT NEXT P0 SQL DIRECT TARGET -->

<!-- INICIO FRENTE 53B VALIDACAO LOCAL DETAILS PANEL DERIVED REPO USAGE -->

## Frente 53b — DetailsPanel consumindo derived_repo para payoff local

### Status

Aplicada localmente e validada.

### Contexto

A Frente 53b deu continuidade à Frente 53, após a Frente 53a ter removido SQL direto
do painel Terminal VWAP/Payoff Dark Panel para os pontos cobertos por payoff e decisões.

O novo recorte técnico foi o arquivo:

- UI/components/details_panel.py

A alteração seguiu a seleção local já registrada para a Frente 53b, usando como alvo
o próximo candidato P0 real do inventário refinado da Frente 52.

### Objetivo

Reduzir SQL direto no DetailsPanel para os pontos relacionados a:

- leitura da decisão mais recente da estrutura;
- leitura dos pontos de payoff por structure_id;
- leitura de auditoria mínima de payoff por structure_id.

A UI passou a delegar essas leituras para db/derived_repo.py, preservando o banco
SQLite local e evitando que a camada de interface consulte diretamente as tabelas
sensíveis de payoff e decisões nesse recorte.

### Escopo aplicado

- UI/components/details_panel.py passou a consumir db.derived_repo para:
  - get_latest_structure_decision;
  - get_payoff_curve_points_by_structure_id;
  - get_structure_payoff_audit_info.
- db/derived_repo.py recebeu funções locais de leitura para atender o DetailsPanel.
- ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py foi criado como guardrail
  específico da frente.
- ATT/frente_53b_details_panel_derived_repo_usage_report.json foi gerado como relatório
  local da frente.
- Nenhuma migração Web foi feita.
- Nenhum HTTP foi introduzido.
- Nenhuma API externa foi introduzida.
- Nenhuma troca de persistência foi feita.
- Nenhuma alteração de schema foi feita.
- Nenhuma alteração operacional ampla foi feita.
- Nenhuma operação de versionamento foi executada.

### Validação local executada

Compilação executada com sucesso:

    python -m py_compile UI/components/details_panel.py db/derived_repo.py ATT/repair_53b_details_panel_no_web_local_only.py

Teste específico da Frente 53b executado com sucesso:

    python -m pytest ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py -q

Resultado:

    6 passed

Bateria direcionada de regressão executada com sucesso:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_app_service.py -q

Resultado:

    55 passed

Verificação local contra dependências Web/HTTP/API externa nos arquivos operacionais:

    grep -RInE "import requests|from requests|import httpx|from httpx|import aiohttp|from aiohttp|urllib.request|urlopen\(|socket.create_connection|websocket|fastapi|flask|django" UI/components/details_panel.py db/derived_repo.py

Resultado:

    Nenhuma ocorrência encontrada nos arquivos operacionais verificados.

### Observação sobre o guardrail

O teste da Frente 53b contém strings textuais com tokens proibidos para validar ausência
de Web/HTTP/API externa nos alvos operacionais. Por isso, buscas amplas que incluam o
arquivo de teste podem encontrar esses tokens no próprio guardrail. A verificação
operacional correta foi feita somente sobre:

- UI/components/details_panel.py
- db/derived_repo.py

E ficou limpa.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem troca de schema.
- Sem alteração operacional ampla.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sem git nesta etapa.
- A consolidação em git fica reservada para o encerramento geral das frentes.

### Posição do projeto após a Frente 53b

A Frente 53b conclui mais um recorte incremental da redução de SQL direto real P0
em UI/services relacionados a payoff.

O projeto permanece na Fase 5 — UI e command services, seguindo a regra de avançar
um arquivo por vez, com patch pequeno, reversível e testável.

A próxima etapa técnica recomendada é continuar a Frente 53 em novo recorte pequeno,
preferencialmente avaliando outro candidato P0 real do inventário refinado da Frente 52,
como UI/models/ui_data.py, antes de qualquer refatoração ampla.

<!-- FIM FRENTE 53B VALIDACAO LOCAL DETAILS PANEL DERIVED REPO USAGE -->

<!-- INICIO FRENTE 53C VALIDACAO LOCAL PAYOFF REPO BRIDGE -->

## Frente 53c — Terminal VWAP Payoff Dark Panel com payoff persistido via derived_repo

### Status

Aplicada localmente e validada.

### Contexto

A Frente 53c deu continuidade à redução incremental de SQL direto real P0 em UI/services
relacionados a payoff, mantendo o mesmo padrão das Frentes 53a e 53b:

- um recorte pequeno por vez;
- alteração local e reversível;
- preservação de contratos públicos;
- sem troca de persistência;
- sem alteração de schema;
- sem migração para Web;
- sem execução de git.

O alvo técnico desta frente foi novamente o arquivo:

- UI/components/terminal_vwap_payoff_dark_panel.py

O recorte aplicado foi específico sobre o método:

- _load_persisted_payoff_points

### Objetivo

Remover SQL direto do carregamento de pontos persistidos de payoff no painel Terminal
VWAP/Payoff Dark Panel, fazendo o método _load_persisted_payoff_points consumir a ponte
local existente em db/derived_repo.py.

A função utilizada como ponte canônica foi:

- derived_repo.get_payoff_curve_points_by_structure_id

### Escopo aplicado

- Substituição do carregamento direto de payoff persistido por chamada ao derived_repo.
- Preservação da identificação por structure_id.
- Normalização defensiva dos pontos retornados no formato spot/pl.
- Preservação da ordenação por spot.
- Preservação do caminho canônico UI.
- Nenhuma pasta ui minúscula foi criada.
- Nenhum import operacional por ui minúsculo foi introduzido.
- Nenhuma chamada Web foi introduzida.
- Nenhum HTTP foi introduzido.
- Nenhuma API externa foi introduzida.
- Nenhuma alteração de schema foi feita.
- Nenhuma troca de persistência foi feita.
- Nenhuma alteração operacional ampla foi feita.
- Nenhuma operação de versionamento foi executada.

### Artefatos locais

- Patch: ATT/patch_53c_terminal_dark_panel_payoff_repo_bridge.py
- Teste: ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py
- Relatório: ATT/frente_53c_terminal_dark_panel_payoff_repo_bridge_report.json
- Backup: ATT/backup_before_53c_terminal_dark_panel_payoff_repo_bridge_20260803_203237_UI__components__terminal_vwap_payoff_dark_panel.py

### Validação local executada

Foram executadas validações locais com sucesso.

Compilação do patch, alvo operacional, repository e teste:

    python -m py_compile ATT/patch_53c_terminal_dark_panel_payoff_repo_bridge.py

    python -m py_compile UI/components/terminal_vwap_payoff_dark_panel.py db/derived_repo.py ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py

Execução do patch:

    python ATT/patch_53c_terminal_dark_panel_payoff_repo_bridge.py

Resultado do patch:

- OK: Frente 53c aplicada localmente.
- target: UI\components\terminal_vwap_payoff_dark_panel.py
- test: ATT\tests\test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py
- relatorio: ATT\frente_53c_terminal_dark_panel_payoff_repo_bridge_report.json
- git: nao executado
- guardrail: sistema local, sem Web, sem HTTP, sem API externa

Teste específico da Frente 53c:

    python -m pytest ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py -q

Resultado:

    3 passed

Bateria direcionada de regressão das Frentes 53a, 53b, 53c e Terminal VWAP/Payoff:

    python -m pytest ATT/tests/test_frente_53a_terminal_vwap_payoff_dark_panel_derived_repo_usage.py ATT/tests/test_frente_53b_details_panel_derived_repo_usage.py ATT/tests/test_frente_53c_terminal_dark_panel_payoff_repo_bridge.py ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py ATT/tests/test_terminal_vwap_payoff_controller.py ATT/tests/test_terminal_vwap_payoff_app_service.py -q

Resultado:

    58 passed

### Evidência do relatório local

O relatório local da Frente 53c registrou:

- status: aplicada_localmente;
- alvo: UI\components\terminal_vwap_payoff_dark_panel.py;
- método: _load_persisted_payoff_points;
- old_had_execute: true;
- new_uses_derived_repo: true;
- forbidden_sql_after: lista vazia;
- canonical_path: UI;
- has_exact_UI: true;
- has_exact_lower_ui: false;
- case_policy: caminho canonico UI preservado; sem criar/importar ui lowercase;
- git: nao executado.

### Observação sobre o scanner 53c

Após o encerramento da Frente 53c, o scanner local identificou 66 candidatos gerais com
possíveis ocorrências de SQL/Web direto ou tokens relacionados.

Esse scanner é amplo e inclui:

- repositories;
- migrations;
- scripts;
- diagnósticos;
- falsos positivos textuais;
- arquivos já parcialmente tratados;
- arquivos onde SQL é esperado por camada.

Portanto, o resultado do scanner não deve ser tratado como regressão automática da Frente
53c. A leitura correta é usá-lo como base para selecionar o próximo recorte pequeno e
validável, mantendo a regra de um arquivo por vez.

### Próxima frente recomendada

A próxima frente técnica recomendada é:

- Frente 53d — Pré-checagem e redução incremental de SQL direto em UI/models/ui_data.py

Justificativa:

- UI/models/ui_data.py aparece como candidato HIGH no scanner local da Frente 53c.
- O Plano de Contenção Consolidado já indicava UI/models/ui_data.py como candidato natural
  após DetailsPanel.
- O Plano Efetivo Inicial cita UIDataModel.get_payoff_curve como ponto de risco por acesso
  direto ao SQLite e possível vazamento de conexão.
- O alvo segue dentro da Fase 5 — UI e command services.
- O recorte deve ser precedido por pré-checagem local para distinguir SQL real de falso
  positivo textual.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem criação de pasta nova na raiz.
- Patches e relatórios permanecem em ATT.
- Testes permanecem em ATT/tests.
- Sem git nesta etapa.
- Caminho canônico UI preservado.

<!-- FIM FRENTE 53C VALIDACAO LOCAL PAYOFF REPO BRIDGE -->

<!-- INICIO FRENTE 37 RTD OPTION QUOTES INTRADAY CANDLE CHART PARSER BRIDGE CONTRACT -->

## Frente 37 — RTD Option Quotes Intraday Candle Chart Service Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar ponte controlada de parser para o service de chart de candles intraday
de RTD Option Quotes, preservando o contrato local e evitando duplicacao de
normalizacao numerica e temporal.

### Escopo aplicado

- Arquivo alvo: rtd_option_quotes_intraday_candle_chart_service.py.
- Uso controlado de parser bridge para dados intraday candle chart.
- Preservacao de compatibilidade com o fluxo local existente.
- Uso de utils/number_parser.py para normalizacao numerica.
- Uso de utils/date_parser.py para normalizacao temporal.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 37 RTD OPTION QUOTES INTRADAY CANDLE CHART SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 37 V3 FIX GUARDRAIL MARKER NORMALIZATION -->

## Frente 37 v3 — Fix guardrail marker normalization

### Status

Aplicada localmente.

### Objetivo

Registrar a correcao documental da Frente 37 v3 para estabilizar o guardrail de
normalizacao de marcadores.

### Correção aplicada

- Frente 37 v3 registrada nos documentos locais.
- normalizacao case-insensitive preservada para marcadores documentais.
- Guardrail documental alinhado sem alterar codigo operacional.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

<!-- FIM FRENTE 37 V3 FIX GUARDRAIL MARKER NORMALIZATION -->

<!-- INICIO FRENTE 38 RTD OPTION QUOTES INTRADAY CANDLE REPOSITORY PARSER BRIDGE CONTRACT -->

## Frente 38 — RTD Option Quotes Intraday Candle Repository Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar ponte controlada de parser para o repository de candles intraday de
RTD Option Quotes, mantendo a normalizacao local antes do consumo pelas camadas
superiores.

### Escopo aplicado

- Arquivo alvo: rtd_option_quotes_intraday_candle_repository.py.
- Ponte local com parser bridge para dados intraday candle.
- Preservacao do contrato de repository.
- Uso de utils/number_parser.py para normalizacao numerica.
- Uso de utils/date_parser.py para normalizacao temporal.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 38 RTD OPTION QUOTES INTRADAY CANDLE REPOSITORY PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 38 V2 FIX REPORT TARGET PATH NORMALIZATION -->

## Frente 38 v2 — Fix report target path normalization

### Status

Aplicada localmente.

### Objetivo

Registrar a correcao documental da Frente 38 v2 para estabilizar o guardrail de
normalizacao de caminho do target no relatorio local.

### Correção aplicada

- Frente 38 v2 registrada nos documentos locais.
- normalizacao posix do target preservada nos relatorios e documentos locais.
- Guardrail documental alinhado sem alterar codigo operacional.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

<!-- FIM FRENTE 38 V2 FIX REPORT TARGET PATH NORMALIZATION -->

<!-- INICIO FRENTE 39 RTD OPTION QUOTES INTRADAY HISTORY REPOSITORY PARSER BRIDGE CONTRACT -->

## Frente 39 — RTD Option Quotes Intraday History Repository Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar ponte controlada de parser para o repository de historico intraday de
RTD Option Quotes, preservando normalizacao numerica e temporal em ponto
reutilizavel.

### Escopo aplicado

- Arquivo alvo: rtd_option_quotes_intraday_history_repository.py.
- Ponte local com parser bridge para historico intraday.
- Preservacao do contrato de repository.
- Uso de utils/number_parser.py para normalizacao numerica.
- Uso de utils/date_parser.py para normalizacao temporal.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 39 RTD OPTION QUOTES INTRADAY HISTORY REPOSITORY PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 40 RTD OPTION QUOTES INTRADAY HISTORY SERVICE PARSER BRIDGE CONTRACT -->

## Frente 40 — RTD Option Quotes Intraday History Service Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Consolidar a ponte controlada de parser no service de historico intraday de RTD
Option Quotes, preservando o fluxo local e evitando alteracao operacional ampla.

### Arquivos envolvidos

- services/rtd_option_quotes_intraday_history_service.py
- services/rtd_option_quotes_intraday_history_repository.py
- utils/number_parser.py
- utils/date_parser.py

### Escopo aplicado

- A Frente 40 manteve o service de historico intraday usando parser controlado.
- O contrato parser bridge foi preservado no recorte local.
- A documentacao local foi alinhada ao guardrail da frente.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

- Nenhuma operacao de versionamento executada.
<!-- FIM FRENTE 40 RTD OPTION QUOTES INTRADAY HISTORY SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO FRENTE 41 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT -->

## Frente 41 — RTD Option Quotes Intraday Candle Service Parser Bridge Contract

### Status

Aplicada localmente e validada.

### Objetivo

Registrar a Frente 41 como recorte local do service de candle intraday de RTD Option
Quotes consumindo parser controlado, preservando contratos e sem refatoracao ampla.

### Arquivos envolvidos

- rtd_option_quotes_intraday_candle_service.py
- utils/number_parser.py
- utils/date_parser.py

### Escopo aplicado

- Parser bridge preservado para o service de candle intraday.
- Normalizacao numerica e temporal mantida em helpers locais.
- Guardrail documental atualizado para refletir a frente encerrada.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Guardrails preservados

- Sistema permanece local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem versionamento nesta etapa.

<!-- FIM FRENTE 41 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT -->

<!-- INICIO RESUMO LOCAL FRENTES ENCERRADAS 37 38 39 -->

## Resumo local — Frentes encerradas 37, 38 e 39

### Status

Frentes 37, 38 e 39 encerradas localmente e documentadas.

### Escopo consolidado

- Frente 37: RTD Option Quotes Intraday Candle Chart Service Parser Bridge Contract.
- Frente 37 v3: normalizacao case-insensitive de marcadores documentais.
- Frente 38: RTD Option Quotes Intraday Candle Repository Parser Bridge Contract.
- Frente 38 v2: normalizacao posix do target no relatorio local.
- Frente 39: RTD Option Quotes Intraday History Repository Parser Bridge Contract.

### Validacao local registrada

- Bateria local direcionada das Frentes 37, 38 e 39 executada.
- Resultado registrado: 31 passed.
- Guardrails documentais das frentes encerradas preservados.

### Decisoes operacionais preservadas

- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sistema permanece 100 por cento local.
- Decisoes operacionais mantidas sem ampliacao de escopo.

- Nenhuma operacao de versionamento executada.
- Resultado local: nenhum erro detectado.
- Sem operacao de git nesta etapa.
- Validacao local: relatorios JSON locais validos.
<!-- FIM RESUMO LOCAL FRENTES ENCERRADAS 37 38 39 -->

<!-- INICIO FRENTE 53D UI DATA PAYOFF REPO BRIDGE -->

## Frente 53d — UIDataModel consumindo derived_repo para payoff curve

### Status

Aplicada localmente e validada em teste direcionado.

### Contexto

A Frente 53d deu continuidade a reducao incremental de SQL direto real P0 em
UI/services relacionados a payoff, apos as Frentes 53a, 53b e 53c.

O alvo tecnico desta frente foi:

- UI/models/ui_data.py

### Objetivo

Remover SQL direto dos metodos publicos de payoff em UIDataModel para que a UI
consuma a ponte local de repository derivado ao carregar pontos de payoff.

A ponte canonica utilizada foi:

- db.derived_repo.get_payoff_curve_points_by_structure_id

### Escopo aplicado

- UI/models/ui_data.py passou a importar db.derived_repo.
- Foi criada ponte local segura por alias _PAYOFF_REPO_LOADER.
- get_payoff_curve passou a usar _PAYOFF_REPO_LOADER.
- get_payoff_curve_info passou a usar _PAYOFF_REPO_LOADER diretamente.
- Os metodos publicos de payoff nao executam SQL direto.
- Os metodos publicos de payoff nao acessam diretamente payoff_curve_points.
- Preservado o uso do banco local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistencia.
- Sem troca de schema.
- Sem alteracao operacional ampla.
- Nenhuma operacao de git executada.
- Caminho canonico UI preservado.

### Artefatos locais

- Patch: ATT/patch_53d_ui_data_payoff_repo_bridge.py
- Reparo local: ATT/repair_53d_ui_data_payoff_methods.py
- Teste: ATT/tests/test_frente_53d_ui_data_payoff_repo_bridge.py
- Relatorio: ATT/frente_53d_ui_data_payoff_repo_bridge_report.json

### Validacao local executada

Compilacao executada com sucesso:

    python -m py_compile UI/models/ui_data.py db/derived_repo.py

Teste especifico da Frente 53d executado com sucesso:

    python -m pytest ATT/tests/test_frente_53d_ui_data_payoff_repo_bridge.py -q

Resultado:

    3 passed

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
- Sem git nesta etapa.

<!-- FIM FRENTE 53D UI DATA PAYOFF REPO BRIDGE -->

<!-- INICIO FRENTE 53D ROUND5 VALIDACAO LOCAL ABA LEGACY CONTRACT -->

## Frente 53d round5 — Validação local do contrato legado aba em UIDataModel

### Status

Aplicada localmente e validada com suíte completa.

### Contexto

Após a Frente 53d remover SQL direto dos métodos públicos de payoff em
UI/models/ui_data.py, restou alinhar o contrato legado retornado por
get_payoff_curve_info().

Os testes de migração da UI esperavam que o campo info["aba"] preservasse o
valor bruto de structure_id, e não o texto derivado no formato structure:<id>.

### Ajuste aplicado

Foi aplicado patch local em:

- UI/models/ui_data.py

O método get_payoff_curve_info() passou a garantir, antes do retorno público:

- info["aba"] = structure_id

Com isso, o contrato legado fica compatível com os consumidores antigos que ainda
leem o campo aba, enquanto a identidade canônica permanece baseada em
structure_id.

### Escopo preservado

- Sem SQL direto reintroduzido em get_payoff_curve.
- Sem SQL direto reintroduzido em get_payoff_curve_info.
- Sem acesso direto da UI à tabela payoff_curve_points nos métodos públicos de payoff.
- Ponte local por db.derived_repo preservada.
- Alias seguro _PAYOFF_REPO_LOADER preservado.
- Contrato público points, info preservado.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem criação de pasta nova na raiz.
- Patches, relatórios e temporários permanecem em ATT.
- Testes permanecem em ATT/tests.
- Nenhuma operação de git executada.

### Artefatos locais

- Patch round5: ATT/patch_53d_ui_data_payoff_curve_info_round5_aba_legacy_contract.py
- Relatório round5: ATT/patch_53d_ui_data_payoff_curve_info_round5_aba_legacy_contract_report.json
- Backup local: UI/models/ui_data.py.backup_53d_round5_20260805_133919

### Validação local executada

Compilação executada com sucesso:

    python -m py_compile UI/models/ui_data.py db/derived_repo.py ATT/patch_53d_ui_data_payoff_curve_info_round5_aba_legacy_contract.py

Bateria direcionada da Frente 53d e migração UI executada com sucesso:

    python -m pytest ATT/tests/test_frente_53d_ui_data_payoff_repo_bridge.py ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_retorna_dados ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_tem_structure_id ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_aba_continuidade ATT/tests/test_ui_data_migration.py::test_payoff_curve_info_pontos_validos -q

Resultado local:

    7 passed

Suíte completa local executada com sucesso:

    python -m pytest ATT/tests -q

Resultado local:

    1107 passed, 4 skipped, 2 warnings, 6 subtests passed

### Observação sobre warnings

Os 2 warnings registrados são DeprecationWarning esperados nos testes de contenção
dos módulos legados:

- db.reader.py
- db.writer.py

Esses warnings fazem parte do contrato local de aposentadoria operacional da Frente 17
e não representam regressão da Frente 53d.

### Posição do projeto após a Frente 53d round5

A Frente 53d fica encerrada localmente com validação direcionada e suíte completa verde.

O projeto permanece na Fase 5 — UI e command services, seguindo a diretriz de reduzir
SQL direto real fora de repositories por recortes pequenos, reversíveis e testáveis.

### Próxima etapa recomendada

A próxima frente técnica deve continuar como novo recorte pequeno da Frente 53,
preferencialmente como Frente 53e, iniciando por pré-checagem local do próximo alvo
P0 real ainda remanescente no inventário refinado da Frente 52.

A escolha do próximo alvo deve preservar as regras do plano:

- um arquivo por vez;
- sem refatoração ampla;
- sem alteração de schema;
- sem troca de persistência;
- sem mudança operacional ampla;
- sem Web, HTTP ou API externa;
- sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 53D ROUND5 VALIDACAO LOCAL ABA LEGACY CONTRACT -->

<!-- INICIO FRENTE 54A VALIDACAO LOCAL RTD SNAPSHOT STATUS SERVICE -->

## Frente 54a — ModernDarkWindow consumindo service local de status RTD Option Quotes

### Status

Aplicada localmente e validada em testes direcionados.

### Contexto

Após o encerramento local da Frente 53d round5, a varredura local de SQL direto em UI
indicou ocorrência remanescente em UI/modern/dark_window.py.

O ponto identificado era o watcher de snapshot RTD Option Quotes, que lia diretamente
o maior updated_at da tabela rtd_option_quotes para detectar mudança no snapshot local.

A consulta estava encapsulada na janela moderna apenas para detectar mudança do snapshot
já persistido, mas ainda representava SQL direto dentro da camada UI.

### Objetivo

Reduzir SQL direto em UI/modern/dark_window.py sem alterar comportamento operacional,
sem alterar schema, sem trocar persistência e sem introduzir Web, HTTP ou API externa.

A UI passou a delegar a leitura de MAX updated_at de rtd_option_quotes para um service
local pequeno e específico.

### Escopo aplicado

- Criado service local services/rtd_option_quotes_snapshot_status_service.py.
- O service concentra a leitura do maior updated_at de rtd_option_quotes.
- UI/modern/dark_window.py passou a consumir o service local.
- O SQL direto foi removido do watcher de snapshot RTD dentro da UI moderna.
- A consulta SQL ficou isolada em camada de service local.
- Nenhuma alteração de schema foi feita.
- Nenhuma troca de persistência foi feita.
- Nenhuma API externa foi introduzida.
- Nenhum HTTP foi introduzido.
- Nenhuma migração Web foi feita.
- Nenhuma operação de versionamento foi executada.

### Validação local registrada

Validação direcionada da Frente 54a:

- Resultado: 4 passed.

Regressão direcionada das Frentes 53c e 53d:

- Resultado: 6 passed.

Varredura local em UI/modern/dark_window.py:

- Nenhuma ocorrência operacional de execute encontrada no arquivo da UI moderna.
- A leitura de MAX updated_at de rtd_option_quotes ficou concentrada em services/rtd_option_quotes_snapshot_status_service.py.

### Artefatos locais

- Service: services/rtd_option_quotes_snapshot_status_service.py.
- Patch documental: ATT/patch_54a_docs_validacao_local.py.
- Relatório documental: ATT/frente_54a_docs_validacao_local_report.json.

### Guardrails preservados

- Sistema permanece 100 por cento local.
- Sem Web.
- Sem HTTP.
- Sem API externa.
- Sem troca de persistência.
- Sem alteração de schema.
- Sem alteração operacional ampla.
- Sem criação de pasta nova na raiz.
- Patches e temporários permanecem em ATT.
- Testes permanecem em ATT/tests.
- Nenhuma operação de git executada.
- Caminho canônico UI preservado.

### Decisão aplicada

A Frente 54a conclui um recorte pequeno da redução de SQL direto em UI, mantendo o
padrão já adotado nas Frentes 53a, 53b, 53c e 53d.

A leitura de status do snapshot RTD Option Quotes deixa de ficar dentro da UI moderna
e passa a ser responsabilidade de service local dedicado.

### Próxima etapa recomendada

A próxima frente técnica deve continuar a redução incremental de SQL direto fora de
repositories, sempre com pré-checagem local do próximo alvo real.

A recomendação é seguir como Frente 54b, selecionando apenas um novo ponto remanescente
por vez, sem refatoração ampla, sem alteração de schema, sem troca de persistência,
sem Web, sem HTTP, sem API externa e sem git até o encerramento geral das frentes.

<!-- FIM FRENTE 54A VALIDACAO LOCAL RTD SNAPSHOT STATUS SERVICE -->

<!-- INICIO FRENTE 54B V3 AUDITORIA SQL DIRETO FILTRADA -->

## Frente 54b v3 — Auditoria filtrada de SQL direto fora de repositories/db/infra

### Status

Aplicada localmente e validada.

### Contexto

A Frente 54b v3 deu continuidade à auditoria refinada de SQL direto fora das camadas
permitidas, partindo do relatório local da Frente 54b v2.

Relatório de origem:

- ATT/frente_54b_v2_auditoria_sql_direto_refinada_report.json

O objetivo foi reduzir falsos positivos remanescentes antes de escolher o próximo recorte
operacional pequeno para remoção incremental de SQL direto.

### Objetivo

Filtrar a auditoria refinada para separar:

- SQL direto real;
- acoplamento relevante com sqlite3;
- chamadas indiretas suspeitas de execute;
- falsos positivos textuais, como with de Python, select como método ou docstring e
  comentários pragma no cover.

### Resultado local

Relatório gerado:

- ATT/frente_54b_v3_auditoria_sql_direto_filtrada_report.json

Resumo registrado no relatório:

- Frente: 54b_v3;
- Status: auditoria_filtrada_local_gerada;
- Achados de origem: 192;
- Achados mantidos: 143;
- Falsos positivos filtrados: 49;
- Arquivos com achados mantidos: 15;
- Git: nao executado.

### Principais candidatos remanescentes

- UI\models\ui_data.py — prioridade alta, ocorrências mantidas: 25, SQL real: 11, acoplamento sqlite: 4, execute indireto suspeito: 6.
- UI\components\terminal_vwap_payoff_dark_panel.py — prioridade alta, ocorrências mantidas: 10, SQL real: 5, acoplamento sqlite: 2, execute indireto suspeito: 3.
- UI\components\details_panel.py — prioridade alta, ocorrências mantidas: 12, SQL real: 3, acoplamento sqlite: 6, execute indireto suspeito: 0.
- services\payoff_refresh_command_service.py — prioridade media_alta, ocorrências mantidas: 16, SQL real: 7, acoplamento sqlite: 5, execute indireto suspeito: 3.
- services\derived_service.py — prioridade media_alta, ocorrências mantidas: 12, SQL real: 5, acoplamento sqlite: 2, execute indireto suspeito: 0.

### Leitura técnica

A filtragem confirmou que ainda há SQL ou acoplamento SQLite relevante fora de
repositories/db/infra, mas a lista ficou mais limpa para orientar a próxima frente.

A prioridade prática permanece concentrada em recortes pequenos, especialmente nos arquivos
de UI ainda com acoplamento direto ou consultas auxiliares:

- UI/models/ui_data.py;
- UI/components/details_panel.py;
- UI/components/terminal_vwap_payoff_dark_panel.py.

Como as Frentes 53a, 53b, 53c, 53d e 54a já removeram pontos específicos sem alterar
contratos, a continuidade deve evitar refatoração ampla e escolher apenas um novo ponto
real por vez.

### Validação local executada

Validação da Frente 54b v3 registrada localmente:

- python ATT/patch_54b_v3_filter_auditoria_sql_direto_refinada.py
- python -m pytest ATT/tests/test_frente_54b_v2_auditoria_sql_direto_refinada_local.py -q
- python -m json.tool ATT/frente_54b_v3_auditoria_sql_direto_filtrada_report.json

### Próximo passo recomendado

Iniciar a Frente 54c com redução incremental localizada em UI/models/ui_data.py.

A próxima frente deve:

- escolher um único ponto real;
- preservar contratos públicos;
- não alterar schema;
- não executar git;
- manter validação local pequena;
- registrar relatório em ATT.

<!-- FIM FRENTE 54B V3 AUDITORIA SQL DIRETO FILTRADA -->

<!-- INICIO FRENTE 54C ISOLAR LIST TABLES UI DATA -->

## Frente 54c — Isolar listagem de tabelas em UI models ui_data

### Status

Aplicada localmente.

### Objetivo

Reduzir um ponto real de SQL direto em UI/models/ui_data.py, isolando a consulta de
listagem de tabelas na camada db, sem alterar comportamento externo.

### Escopo aplicado

- Removido de UI/models/ui_data.py o SQL direto usado para consultar sqlite_master em
  _list_tables.
- Criado db/app_metadata_repo.py com funcao list_tables.
- Mantida a conexao local ja existente em UI/models/ui_data.py.
- Preservado o retorno publico de _list_tables como lista de nomes de tabelas.
- Nenhuma alteracao de schema.
- Nenhuma alteracao operacional ampla.
- Nenhuma operacao de git executada.

### Arquivos envolvidos

- UI/models/ui_data.py
- db/app_metadata_repo.py
- ATT/frente_54c_isolar_list_tables_ui_data_report.json

### Validacao local recomendada

- python ATT/patch_54c_isolar_list_tables_ui_data.py
- python -m pytest ATT/tests/test_frente_54c_isolar_list_tables_ui_data_local.py -q
- python -m json.tool ATT/frente_54c_isolar_list_tables_ui_data_report.json

<!-- FIM FRENTE 54C ISOLAR LIST TABLES UI DATA -->

