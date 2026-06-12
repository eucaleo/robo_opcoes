# Fase 15 — Validação Integrada

Data: 2026-06-12
Branch: `fase-15-validacao-integrada`

## Objetivo

Executar uma validação integrada do estado atual do projeto após a integração da Fase 14 na `main`, cobrindo:

- estado Git da rota;
- suíte automatizada de testes;
- checks operacionais locais;
- conferência de scripts versionados;
- conferência dos bancos SQLite operacionais;
- evidências de continuidade entre as fases anteriores.

## Base Git validada

A Fase 15 foi iniciada a partir da `main` após integração da Fase 14.

Commits de referência:

```text
e1d90fd merge: integra fase 14 migracao de dados legados
a347140 fase 14: documenta migração de eventos legados
fc25b3a refactor: load operational state from UI app database
```

## Correção aplicada durante a validação

Durante a execução de `python -m ATT.checks.run_all_checks`, o check `check_cleanup_residuals.py` falhou porque a allowlist de scripts operacionais estava desatualizada.

A allowlist foi atualizada para refletir os scripts realmente versionados e utilizados pelo projeto:

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

Nenhum script foi removido ou movido nesta fase.

## Resultado da suíte automatizada

Comando executado:

```bash
python -m pytest ATT/tests -q
```

Resultado:

```text
564 passed, 10 skipped in 34.73s
```

## Resultado dos checks integrados

Comando executado:

```bash
python -m ATT.checks.run_all_checks
```

Resultado final:

```text
[OK] Todos os checks passaram
```

Checks executados com sucesso:

```text
check_api_routes.py
check_legs.py
check_structures.py
check_end_to_end.py
check_cleanup_residuals.py
```

## Conferência da rota de desenvolvimento

Comando executado:

```bash
python scripts/check_rota_desenvolvimento.py
```

Resultado observado:

- branch atual: `fase-15-validacao-integrada`;
- Fase 14 presente no histórico;
- documentos das fases anteriores localizados;
- `dados/app.db` encontrado e populado;
- `dados/derived.db` encontrado;
- estruturas 44-48 presentes em `dados/app.db`;
- pernas normalizadas para estruturas 44-48 presentes em `structure_legs`.

Resumo operacional observado:

```text
structure_id=44 | alias=BOVA11 | structure_legs=4
structure_id=45 | alias=EMBJ3 | structure_legs=4
structure_id=46 | alias=PRIO3 | structure_legs=4
structure_id=47 | alias=SBSP3 | structure_legs=4
structure_id=48 | alias=SMAL11 | structure_legs=4
```

## Decisão

A Fase 15 valida que:

- a Fase 14 está integrada na `main`;
- a branch da Fase 15 nasceu da base correta;
- a suíte automatizada está verde;
- os checks operacionais estão verdes;
- a allowlist de scripts operacionais foi alinhada ao estado real do repositório;
- a rota de desenvolvimento possui evidências suficientes para continuidade.

## Status

Fase 15 considerada validada.
