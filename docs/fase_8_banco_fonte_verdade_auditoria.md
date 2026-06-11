# Fase 8 - Banco Como Fonte da Verdade - Auditoria Inicial

## Objetivo

Consolidar o banco como centro operacional do sistema, conforme a ROTA MESTRE.

O banco deve ser a fonte da verdade para:

- ativos;
- instrumentos;
- contratos de opções;
- cotações de ativos;
- cotações de opções;
- snapshots RTD;
- estruturas;
- pernas;
- eventos de posição;
- encerramentos manuais;
- parâmetros;
- snapshots por perna;
- snapshots por estrutura;
- execuções de cálculo.

## Critério de saída da fase

O sistema deve conseguir consultar dados essenciais sem depender das abas calculadas do Excel.

## Estado do repositório no início da fase

Branch analisada:

- limpeza-tests-scripts-checks

Últimos commits relevantes:

- 1960a9d Documenta auditoria inicial da fase 8 banco fonte da verdade
- fc4d438 Fecha fase 7 isolamento nomes fisicos legados
- 0504b1b Move aliases fisicos da UI para repositorio
- 997501d Reduz referencias fisicas rtd em dominio e facade
- 3e2fe15 Documenta camada canonica de leitura da fase 6
- 37903fe Documenta isolamento do bridge Excel da fase 5

Estado inicial:

- working tree sem alterações reportadas por git status --short antes da criação da auditoria.

## Camadas analisadas

Foram consideradas as camadas versionadas:

- db/
- repositories/
- services/
- domain/
- UI/models/
- infra/

Arquivos locais de cache, como __pycache__, podem existir no diretório de trabalho, mas não fazem parte do código versionado conforme git ls-files.

## Auditoria de dados/derived.db

Banco encontrado:

- dados/derived.db

Objetos encontrados:

- payoff_curve_points
- payoff_curve_summary
- sqlite_sequence
- structure_decisions

Contagens:

- payoff_curve_points: 505
- payoff_curve_summary: 0
- sqlite_sequence: 1
- structure_decisions: 12

Leitura inicial:

- O banco derived.db concentra dados derivados, especialmente curva de payoff e decisões.
- Existem pontos de payoff persistidos.
- Existem decisões de estrutura persistidas.
- A tabela payoff_curve_summary existe, mas está vazia.
- Este banco deve ser tratado como área de dados derivados, não como fonte operacional primária isolada.

## Auditoria de dados/app.db

Banco encontrado:

- dados/app.db

Objetos encontrados:

- manual_analise_robo_legs
- pricing_executions
- rtd_analise_raiox
- rtd_analise_robo
- rtd_analise_robo_legs
- rtd_configuracoes
- rtd_consolidacoes
- rtd_encerramentos_manuais
- rtd_hist_robo
- rtd_option_quotes
- rtd_rolls_detectados
- sqlite_sequence
- structure_audit_log
- structure_legs
- structures

Contagens:

- manual_analise_robo_legs: 0
- pricing_executions: 15
- rtd_analise_raiox: 5
- rtd_analise_robo: 5
- rtd_analise_robo_legs: 20
- rtd_configuracoes: 4
- rtd_consolidacoes: 5
- rtd_encerramentos_manuais: 0
- rtd_hist_robo: 2400
- rtd_option_quotes: 1
- rtd_rolls_detectados: 20
- sqlite_sequence: 5
- structure_audit_log: 0
- structure_legs: 0
- structures: 5

## Classificação inicial das tabelas

### Tabelas operacionais atuais

- structures
- structure_legs
- pricing_executions
- structure_audit_log
- rtd_option_quotes

Observações:

- structures possui registros.
- structure_legs existe, mas está vazia.
- pricing_executions possui registros.
- structure_audit_log existe, mas está vazia.
- rtd_option_quotes possui apenas um registro no estado analisado.

### Tabelas RTD ou legado importado

- rtd_analise_raiox
- rtd_analise_robo
- rtd_analise_robo_legs
- rtd_configuracoes
- rtd_consolidacoes
- rtd_encerramentos_manuais
- rtd_hist_robo
- rtd_rolls_detectados
- manual_analise_robo_legs

Observações:

- Essas tabelas ainda carregam nomes físicos legados.
- A Fase 7 restringiu referências diretas a esses nomes físicos às fronteiras permitidas.
- Na Fase 8, elas devem ser tratadas como compatibilidade, ingestão, legado, migração ou apoio transitório.
- Elas não devem ser consideradas modelo operacional final.

## Cobertura atual frente à ROTA MESTRE

### Já existe no banco

- estruturas
- cotações de opções
- snapshots/importações RTD legadas
- execuções de cálculo
- dados derivados de payoff
- decisões de estrutura

### Existe estrutura de tabela, mas sem dados suficientes

- pernas
- auditoria de estruturas
- resumo de payoff
- encerramentos manuais

### Ainda não consolidado como fonte da verdade

- eventos de posição
- snapshots por perna
- snapshots por estrutura
- parâmetros operacionais próprios
- contratos de opções normalizados
- ativos/instrumentos normalizados
- histórico operacional independente do Excel

## Principal achado da auditoria

O banco já possui estruturas persistidas:

- structures: 5

Mas não possui pernas persistidas:

- structure_legs: 0

Isso impede afirmar que o banco é fonte da verdade completa para estruturas operacionais, pois uma estrutura sem pernas não representa integralmente a operação.

## Impacto

Enquanto structure_legs permanecer vazio, o sistema provavelmente ainda precisa recorrer a dados legados, RTD ou mapeamentos auxiliares para montar pernas operacionais.

Esse ponto deve ser tratado antes ou durante a Fase 9, mas já fica registrado como pendência estrutural da Fase 8.

## Pontos de atenção encontrados no código

A auditoria SQL apontou acessos diretos a tabelas em:

- db/
- repositories/
- services/
- domain/
- UI/
- infra/

Pontos relevantes:

- repositories/ concentra acessos físicos ao banco, o que é esperado.
- db/ e infra/ concentram schema, bootstrap e persistência de baixo nível, o que é esperado.
- services/ ainda possui algumas consultas SQL diretas.
- UI/components/details_panel.py possui consultas SQL diretas, ponto a ser tratado na Fase 13.
- domain/payoff_features.py possui persistência SQL direta em payoff_curve_summary, ponto a ser revisado para manter domínio livre de persistência.

## Validação executada

Comando executado:

- pytest ATT/tests/test_structures_repository.py ATT/tests/test_market_snapshot_provider.py ATT/tests/test_ui_data_migration.py

Resultado:

- 47 passed em 5.49s

## Conclusão inicial

A Fase 8 pode seguir.

Estado atual:

- Banco já contém parte importante do estado operacional.
- Ainda há dependência estrutural de tabelas legadas para dados de pernas e histórico.
- O principal bloqueio para banco como fonte da verdade completa é a ausência de pernas persistidas em structure_legs.
- A próxima ação técnica deve mapear como as estruturas existentes em structures se relacionam com rtd_analise_robo_legs e como esse vínculo pode ser migrado ou normalizado sem corromper dados.

## Próxima auditoria recomendada

Mapear conteúdo e colunas de:

- structures
- structure_legs
- rtd_analise_robo_legs
- manual_analise_robo_legs
- rtd_option_quotes
- pricing_executions

Objetivos:

- identificar chave de vínculo entre estruturas e pernas;
- confirmar se alias_legacy_aba é suficiente para vincular estrutura com pernas legadas;
- verificar se há dados suficientes para popular structure_legs;
- definir se a migração será feita agora ou deixada como entrada controlada para a Fase 9.

## Auditoria complementar: vínculo entre estruturas e pernas legadas

Foi executada inspeção das tabelas centrais da Fase 8 para avaliar se as estruturas persistidas em `structures` possuem vínculo confiável com pernas vindas das tabelas RTD legadas.

### Tabelas inspecionadas em dados/app.db

- structures
- structure_legs
- rtd_analise_robo_legs
- manual_analise_robo_legs
- rtd_option_quotes
- pricing_executions
- rtd_analise_robo
- rtd_consolidacoes

### Tabelas inspecionadas em dados/derived.db

- structure_decisions
- payoff_curve_points
- payoff_curve_summary

## Resultado da inspeção de structures

A tabela `structures` possui 5 registros:

- id 44: BOVA11, alias_legacy_aba BOVA11
- id 45: EMBJ3, alias_legacy_aba EMBJ3
- id 46: PRIO3, alias_legacy_aba PRIO3
- id 47: SBSP3, alias_legacy_aba SBSP3
- id 48: SMAL11, alias_legacy_aba SMAL11

Colunas relevantes:

- id
- name
- underlying_asset
- alias_legacy_aba
- status
- notes
- created_at
- updated_at

## Resultado da inspeção de structure_legs

A tabela `structure_legs` existe, mas permanece vazia.

Total encontrado:

- structure_legs: 0

Colunas disponíveis para normalização:

- id
- structure_id
- position_side
- option_type
- symbol
- strike
- expiration_date
- quantity
- premium
- multiplier
- leg_order
- notes
- created_at
- updated_at

Conclusão:

- O schema operacional de pernas já existe.
- Ainda não há dados normalizados nessa tabela.
- A normalização pode ser tecnicamente viável, mas exige mapeamento explícito e testado dos campos legados.

## Resultado da inspeção de rtd_analise_robo_legs

A tabela `rtd_analise_robo_legs` possui 20 registros.

Cada uma das 5 estruturas possui 4 pernas.

Campos relevantes encontrados:

- timestamp
- aba
- ativo
- cv
- call_put
- quant
- valor_executado
- bid
- ask
- spread
- spread_pct
- iv
- delta
- gamma
- theta
- vega
- strike
- vencimento
- dte
- pl_realista

Leitura inicial:

- `aba` é a chave legada que identifica a estrutura.
- `ativo` representa o código da opção.
- `cv` representa compra/venda no legado.
- `call_put` representa CALL ou PUT.
- `quant` representa quantidade.
- `valor_executado` pode servir como prêmio/preço executado.
- `strike` e `vencimento` podem alimentar os campos normalizados de perna.
- Os campos de gregas e mercado podem alimentar snapshots, não necessariamente `structure_legs`.

## Resultado do vínculo structures x rtd_analise_robo_legs

Consulta realizada:

- structures.alias_legacy_aba x rtd_analise_robo_legs.aba

Resultado:

- BOVA11 encontrou 4 pernas RTD
- EMBJ3 encontrou 4 pernas RTD
- PRIO3 encontrou 4 pernas RTD
- SBSP3 encontrou 4 pernas RTD
- SMAL11 encontrou 4 pernas RTD

Não foram encontradas abas em `rtd_analise_robo_legs` sem estrutura correspondente.

Não foram encontradas estruturas sem pernas em `rtd_analise_robo_legs`.

## Classificação do cenário

Classificação:

- Cenário A: vínculo perfeito

Conclusão:

- `alias_legacy_aba` é suficiente, no estado atual do banco, para vincular cada estrutura persistida às suas pernas legadas.
- Há dados suficientes para criar uma migração controlada para popular `structure_legs`.
- A migração não deve ser feita automaticamente sem antes definir regras formais de conversão de `cv`, `call_put`, `quant`, `valor_executado` e `vencimento`.

## Observações sobre pricing_executions

A tabela `pricing_executions` possui 15 registros.

Os registros analisados já carregam payloads com pernas canônicas dentro de `pricing_payload`, incluindo:

- structure_id
- underlying_asset
- reference_date
- legs
- quantity
- price
- asset
- option_type
- strike
- expiry
- iv
- delta
- gamma
- theta
- vega
- source

Leitura:

- Além da ponte direta com `rtd_analise_robo_legs`, existe uma segunda fonte já parcialmente canonizada dentro de `pricing_executions.pricing_payload`.
- Essa fonte pode ser útil para validação cruzada, mas não deve substituir uma migração explícita e auditável para `structure_legs`.

## Observações sobre dados derivados

A tabela `structure_decisions` possui decisões associadas a `structure_id`.

A tabela `payoff_curve_points` possui pontos de curva associados a `structure_id`.

A tabela `payoff_curve_summary` existe, mas está vazia.

Leitura:

- Parte dos derivados já referencia estruturas por `structure_id`.
- Isso reforça que `structures.id` já está sendo usado como identificador operacional em parte do sistema.
- A ausência de `structure_legs` continua sendo a principal lacuna para completar o banco como fonte da verdade operacional.

## Decisão técnica após auditoria complementar

A próxima etapa técnica da Fase 8 deve ser preparar uma leitura/migração controlada das pernas.

Antes de inserir dados em `structure_legs`, devem ser definidos e testados os mapeamentos:

- rtd_analise_robo_legs.aba -> structures.alias_legacy_aba
- structures.id -> structure_legs.structure_id
- rtd_analise_robo_legs.cv -> structure_legs.position_side
- rtd_analise_robo_legs.call_put -> structure_legs.option_type
- rtd_analise_robo_legs.ativo -> structure_legs.symbol
- rtd_analise_robo_legs.strike -> structure_legs.strike
- rtd_analise_robo_legs.vencimento -> structure_legs.expiration_date
- rtd_analise_robo_legs.quant -> structure_legs.quantity
- rtd_analise_robo_legs.valor_executado -> structure_legs.premium
- ordem estável das pernas -> structure_legs.leg_order

Critério recomendado:

- criar primeiro função ou serviço de leitura canônica;
- cobrir com testes;
- só depois decidir se haverá backfill persistente em `structure_legs`.

