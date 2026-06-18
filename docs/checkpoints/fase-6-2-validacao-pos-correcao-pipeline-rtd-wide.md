# Fase 6.2 — Validação pós-correção do pipeline RTD wide/autobootstrap

## Contexto

A Fase 6.1 registrou a validação operacional inicial do pipeline RTD.

Após esse checkpoint, foi publicado o commit técnico:

- `700a716 Corrige pipeline RTD wide com autobootstrap de schema`

Esse commit corrigiu o pipeline RTD wide para utilizar o importador operacional correto e garantir o schema `rtd_option_quotes` de forma controlada antes da importação.

## Arquivos impactados pelo commit técnico

- `infra/bootstrap_rtd_option_quotes_schema.py`
- `scripts/import_rtd_option_quotes_wide_csv.py`
- `scripts/run_rtd_option_quotes_pipeline.py`
- `ATT/tests/test_run_rtd_option_quotes_pipeline.py`

## Escopo da Fase 6.2

Validar a correção aplicada ao pipeline RTD wide/autobootstrap, sem ampliar escopo funcional.

Esta fase não autoriza alteração ampla em UI, API, repository ou serviço.

## Comandos planejados/executados

```bash
git status
git log --oneline --decorate -15
python -m pytest ATT/tests/test_run_rtd_option_quotes_pipeline.py ATT/tests/test_audit_rtd_option_quotes.py
python -m pytest ATT/tests -k "rtd_option_quotes"
```

## Critérios de validação

A Fase 6.2 será considerada válida se:

1. o pipeline RTD compilar;
2. os testes específicos de `rtd_option_quotes` passarem;
3. o pipeline usar o importador wide oficial;
4. o schema `rtd_option_quotes` for validado/criado de forma controlada;
5. o Excel permanecer apenas como gateway RTD;
6. não houver alteração não autorizada em UI, API, repository ou serviço;
7. o working tree ficar limpo após o commit documental.

## Relação com a ROTA_MESTRE_3

A Fase 6 permanece como retomada funcional controlada.

A Fase 6.1 registrou a validação operacional inicial do pipeline RTD.

A Fase 6.2 existe porque houve correção técnica posterior no pipeline em:

- `700a716 Corrige pipeline RTD wide com autobootstrap de schema`

Portanto, esta fase registra a necessidade de validação pós-correção antes de avançar para nova alteração funcional.

## Status

Concluída em 2026-06-18.

Validação pós-correção executada com sucesso.

Comandos executados:

```bash
python -m pytest ATT/tests/test_run_rtd_option_quotes_pipeline.py ATT/tests/test_audit_rtd_option_quotes.py
python -m pytest ATT/tests -k "rtd_option_quotes"
```

Resultados registrados:

- `16 passed in 0.43s`
- `19 passed, 630 deselected in 3.10s`

Conclusão:

- o pipeline RTD wide foi validado após a correção `700a716`;
- os testes específicos de `rtd_option_quotes` ficaram verdes;
- o pipeline permanece usando o fluxo wide/autobootstrap controlado;
- não houve ampliação funcional nesta fase.
