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
