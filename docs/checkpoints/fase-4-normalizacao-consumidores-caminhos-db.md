# Fase 4 — Normalização incremental dos consumidores de caminhos de banco

## Contexto

Durante a Fase 4 da ROTA_MESTRE_3, após o inventário funcional de consumidores de caminhos de banco e o plano de normalização, foi executada uma refatoração incremental para remover dependências diretas de caminhos fixos como:

- dados/app.db
- dados/derived.db
- ./dados/app.db

A alteração foi limitada aos consumidores identificados e validada por testes automatizados, compilação e scripts de consistência dos bancos.

## Branch

fase-12-fechamento-ciclo

## Commit relacionado

5d31457 fix: resolve database paths from runtime config

## Arquivos alterados

- ATT/tests/test_db_config_paths.py
- UI/components/structure_editor_dialog.py
- db/derived_repo.py
- db/reader.py
- db/writer.py
- repositories/robo_legs_repository.py
- repositories/robo_legs_status_repository.py
- services/canonical_pricing_facade.py
- services/pricing_execution_app_service.py

## Decisão técnica

Os consumidores passaram a resolver caminhos de banco em tempo de execução por meio das funções centrais de configuração:

- get_app_db_path()
- get_derived_db_path()
- ensure_parent_dir()

Foi preservada a possibilidade de injeção explícita de db_path nos construtores para testes, cenários controlados e compatibilidade com chamadas existentes.

## Escopo da alteração

A normalização atingiu consumidores de:

- banco principal app.db;
- banco derivado derived.db;
- repositories;
- services;
- camada de UI afetada por caminho explícito de banco;
- testes de configuração de caminhos.

A alteração não teve como objetivo alterar regra de negócio, contrato RTD/Excel ou schema da tabela rtd_option_quotes.

## Validações executadas

### Testes de configuração de caminhos

Comando executado:

python -m pytest ATT/tests/test_db_config_paths.py -q

Resultado:

14 passed

### Suíte focada de repositórios, status e pricing

Comando executado:

python -m pytest ATT/tests/test_robo_legs_repository.py ATT/tests/test_robo_legs_status_repository.py ATT/tests/test_canonical_pricing_facade_rtd_db_path.py ATT/tests/test_canonical_pricing_facade_execute_pricing_rtd_integration.py ATT/tests/test_pricing_executions_repository.py -q

Resultado:

21 passed

### Validação dos bancos

Comandos executados:

python scripts/validate_app_db.py
python scripts/validate_derived_db.py

Resultado:

APP.DB ESTA CONSISTENTE
BANCO ESTA CONSISTENTE

### Compilação dos arquivos alterados

Comando executado:

python -m py_compile db/derived_repo.py db/reader.py db/writer.py repositories/robo_legs_repository.py repositories/robo_legs_status_repository.py services/canonical_pricing_facade.py services/pricing_execution_app_service.py UI/components/structure_editor_dialog.py ATT/tests/test_db_config_paths.py

Resultado:

Sem erros.

## Resultado

A normalização incremental dos consumidores de caminhos de banco foi concluída, testada, commitada e enviada ao remoto.

## Estado após o push

fase-12-fechamento-ciclo sincronizada com origin/fase-12-fechamento-ciclo

## Restrições preservadas da rota

Esta intervenção respeitou as restrições da ROTA_MESTRE_3:

- não criou tabelas;
- não alterou schema diretamente;
- não executou limpeza destrutiva;
- não versionou bancos locais;
- não alterou o papel do Excel como gateway RTD;
- não avançou para retomada funcional ampla.

## Situação da Fase 4

A Fase 4 permanece em andamento.

A decisão pendente continua sendo a forma correta de reconciliação da tabela rtd_option_quotes, ausente em dados/app.db, podendo envolver:

- migração;
- bootstrap;
- script controlado;
- restauração validada;
- ou outro mecanismo formalmente documentado após auditoria.

## Próximo passo recomendado

Executar auditoria final da presença histórica e das dependências de rtd_option_quotes antes de qualquer criação de tabela ou alteração funcional relacionada ao fluxo RTD.
