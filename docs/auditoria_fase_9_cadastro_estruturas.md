# Auditoria Fase 9 — Cadastro e Persistência de Estruturas

## Objetivo

Validar e corrigir o fluxo de cadastro e persistência de estruturas, garantindo que uma nova estrutura criada no sistema seja gravada no banco, tenha pernas persistidas, seja recuperada pela UI e possa alimentar o fluxo de cálculo sem edição manual no Excel.

## Critério de saída da Fase 9

Nova estrutura criada no sistema aparece corretamente na UI sem edição manual no Excel.

## Estado inicial

Branch: limpeza-tests-scripts-checks

Validações iniciais executadas:

```text
git status
python -m py_compile api/structures_controller.py repositories/structures_repository.py services/structure_input_mapper.py services/structure_analysis_service.py
python scripts/run_derived_pipeline.py --no-cleanup
python scripts/validate_derived_db.py
python -m pytest ATT/tests/test_structures_repository.py


## Auditoria dirigida — Achados iniciais

### Schema

O schema canônico de estruturas está definido em:

```text
infra/bootstrap_structures_schema.py


## Auditoria dirigida — Achados iniciais

### Schema

O schema canônico de estruturas está definido em:

```text
infra/bootstrap_structures_schema.py

### Correção Fase 9 — criação atômica de estrutura com legs

Diagnóstico:

O fluxo anterior da UI criava primeiro a estrutura e depois gravava as legs em operação separada.
Em caso de falha na gravação das legs, poderia sobrar estrutura persistida sem pernas.

Correção aplicada:

Foi criado método transacional create_structure_with_legs() no repository canônico.
A UI passou a usar esse método no cadastro de nova estrutura.

Arquivos alterados:

- repositories/structures_repository.py
- UI/components/structure_editor_dialog.py

Validação esperada:

- python -m py_compile repositories/structures_repository.py UI/components/structure_editor_dialog.py
- python -m pytest ATT/tests/test_structures_repository.py ATT/tests/test_structure_editor_dialog.py ATT/tests/test_structure_editor_integration.py
