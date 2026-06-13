# Plano de Testes do Ciclo 2

## Objetivo

Iniciar a evolução posterior à ROTA MESTRE 1 com foco em validação, organização da suíte de testes e definição segura da próxima rota técnica.

## Premissa

Nenhuma alteração funcional deve ser iniciada antes de:

```text
1. mapear os testes existentes;
2. classificar checks, testes e scripts operacionais;
3. identificar lacunas;
4. definir a ordem oficial de validação;
5. registrar a nova evolução pretendida.
```

## Estado inicial

Branch de trabalho:

```text
ciclo-2-testes-evolucao
```

Marco anterior:

```text
rota-mestre-v1
```

Base da branch:

```text
main em ffb1fab
```

## Resultado validado antes do ciclo

```text
pytest: 564 passed, 10 skipped
ATT/checks/run_all_checks.py: PASS
validate_db.py: executado
```

## Testes existentes em ATT/tests

Arquivos de teste identificados:

```text
ATT/tests/test_canonical_input_service.py
ATT/tests/test_canonical_validators.py
ATT/tests/test_contracts.py
ATT/tests/test_decision.py
ATT/tests/test_derived_service.py
ATT/tests/test_legacy_robo_legs_fallback.py
ATT/tests/test_legacy_structure_legs_importer.py
ATT/tests/test_legacy_structure_legs_importer_integration.py
ATT/tests/test_legacy_structure_legs_reader.py
ATT/tests/test_market_snapshot_provider.py
ATT/tests/test_orchestrator_run_methods.py
ATT/tests/test_payoff_canonical.py
ATT/tests/test_payoff_chart.py
ATT/tests/test_pricing_engine_stub.py
ATT/tests/test_pricing_execution_app_service.py
ATT/tests/test_pricing_execution_controller.py
ATT/tests/test_pricing_execution_orchestration_service.py
ATT/tests/test_pricing_execution_persistence_service.py
ATT/tests/test_pricing_execution_query_service.py
ATT/tests/test_pricing_execution_service.py
ATT/tests/test_pricing_executions_repository.py
ATT/tests/test_pricing_input_service.py
ATT/tests/test_pricing_payload_adapter.py
ATT/tests/test_robo_leg_mapper.py
ATT/tests/test_robo_legs_repository.py
ATT/tests/test_robo_legs_service.py
ATT/tests/test_robo_legs_status_repository.py
ATT/tests/test_robo_legs_status_service.py
ATT/tests/test_structure_analysis_service.py
ATT/tests/test_structure_editor_dialog.py
ATT/tests/test_structure_editor_integration.py
ATT/tests/test_structure_events_api.py
ATT/tests/test_structure_events_effective_state.py
ATT/tests/test_structure_events_repository.py
ATT/tests/test_structure_events_service.py
ATT/tests/test_structure_input_mapper.py
ATT/tests/test_structure_market_input_assembler.py
ATT/tests/test_structure_metrics.py
ATT/tests/test_structures_api.py
ATT/tests/test_structures_archive_wiring.py
ATT/tests/test_structures_legs_endpoints.py
ATT/tests/test_structures_repository.py
ATT/tests/test_system_snapshots_repository.py
ATT/tests/test_system_snapshots_schema.py
ATT/tests/test_ui_data_migration.py
```

## Checks existentes em ATT/checks

```text
ATT/checks/check_api_routes.py
ATT/checks/check_cleanup_residuals.py
ATT/checks/check_end_to_end.py
ATT/checks/check_legs.py
ATT/checks/check_structures.py
ATT/checks/run_all_checks.py
```

## Scripts operacionais existentes

```text
scripts/apply_fase9_atomic_create.py
scripts/apply_fase9_atomic_create.sh
scripts/apply_fase9_update_tests_atomic_create.py
scripts/check_rota_desenvolvimento.py
scripts/import_legacy_structure_legs.py
scripts/patch_derived_payoff_timestamp_consistency.sh
scripts/purge_derived_snapshots.py
scripts/repair_derived_db_consistency.py
scripts/run_derived_pipeline.py
scripts/validate_derived_db.py
```

## Scripts citados anteriormente, mas ausentes

```text
scripts/run_smoke_quick.py
scripts/run_smoke_full.py
ATT/checks/run_real_smokes.py
```

Classificação:

```text
Ausentes na árvore atual.
Devem ser removidos da documentação como comandos oficiais ou recriados formalmente no ciclo 2.
```

## Arquivos locais observados no mapeamento

O comando find também encontrou arquivos de cache e referências internas do Git:

```text
ATT/tests/__pycache__/
.git/logs/
.git/refs/
```

Classificação:

```text
Artefatos locais.
Não devem ser versionados.
Devem permanecer ignorados.
```

Também foi observado:

```text
debug_bridge_check_after_vba.py
```

Classificação inicial:

```text
Arquivo a verificar.
Necessário confirmar se é versionado, ignorado ou resíduo local antes de qualquer remoção.
```

## Ordem oficial de validação proposta

### Validação rápida

```bash
python validate_db.py
python ATT/checks/run_all_checks.py
pytest
```

### Validação de scripts operacionais

```bash
python scripts/validate_derived_db.py
python scripts/run_derived_pipeline.py
python scripts/check_rota_desenvolvimento.py
```

### Validação de repositório

```bash
git status --short
git ls-files ATT/tests/__pycache__
git ls-files | grep -E "__pycache__|\.pyc$" || true
git ls-files debug_bridge_check_after_vba.py
git check-ignore -v ATT/tests/__pycache__/test_canonical_input_service.cpython-313-pytest-9.0.3.pyc || true
```

## Lacunas iniciais

```text
1. Não existe script formal de smoke quick.
2. Não existe script formal de smoke full.
3. Não existe run_real_smokes.py em ATT/checks.
4. A nomenclatura oficial entre teste, check, smoke e script operacional ainda precisa ser padronizada.
5. É necessário decidir se os smokes serão recriados ou se run_all_checks.py será o executor oficial.
```

## Primeira recomendação técnica

A recomendação inicial para o Ciclo 2 é:

```text
1. transformar ATT/checks/run_all_checks.py no executor oficial de checks;
2. auditar debug_bridge_check_after_vba.py;
3. verificar se os caches Python estão corretamente ignorados;
4. só depois decidir se serão criados smoke quick e smoke full.
```

## Critério de saída do Ciclo 2 de Testes

O ciclo de testes será considerado fechado quando:

```text
1. a suíte oficial estiver documentada;
2. os comandos ausentes forem removidos da documentação ou implementados;
3. os testes automatizados passarem;
4. os checks passarem;
5. os scripts operacionais críticos forem classificados;
6. o repositório estiver limpo;
7. a próxima rota técnica estiver documentada antes de alterações funcionais.
```

## Decisão inicial

O Ciclo 2 começa como ciclo de organização e validação.

Não haverá alteração funcional antes do fechamento do mapa de testes.

