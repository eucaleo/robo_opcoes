# Checkpoint — Fase 4/5 — Reconciliação rtd_option_quotes e RTD/Excel

## Contexto

Checkpoint da ROTA_MESTRE_3 para registrar a reconciliação controlada da tabela `rtd_option_quotes` e da ponte RTD oficial `LISTA_RTD.xlsm`.

Branch:

```text
fase-12-fechamento-ciclo
```

Commit funcional relacionado:

```text
b8a3201 fix: importa cotações RTD de opções e fecha Excel corretamente
```

## Fase 4 — Reconciliação de schema

A tabela `rtd_option_quotes` foi reconciliada em `dados/app.db`.

Foi criado script controlado para bootstrap/validação de schema vazio:

```text
infra/bootstrap_rtd_option_quotes_schema.py
```

Interface validada:

```bash
python infra/bootstrap_rtd_option_quotes_schema.py --help
```

Resultado observado:

```text
Cria/valida o schema vazio de rtd_option_quotes em banco SQLite.
--db DB     Caminho do banco SQLite. Padrão: dados/app.db
```

Auditoria executada:

```bash
python scripts/audit_rtd_option_quotes.py --db dados/app.db
```

Resultado:

```text
Auditoria rtd_option_quotes
Banco: dados\app.db
Tabela: rtd_option_quotes
Status: ok

Métricas:
- distinct_codigo_count: 4
- duplicate_codigo_count: 0
- max_age_minutes: 30
- missing_codigo_count: 0
- row_count: 4
- stale_rows: 0
```

## Fase 5 — Reconciliação RTD/Excel

A ponte RTD operacional oficial permanece sendo:

```text
LISTA_RTD.xlsm
```

A aba tabular validada foi:

```text
RTD_OPTION_QUOTES
```

Tickers validados:

```text
PRIOG800, PRIOH515, PRIOT700, PRIOS525
```

Pipeline executado:

```bash
python scripts/run_lista_rtd_option_quotes_pipeline.py \
  --db dados/app.db \
  --workbook LISTA_RTD.xlsm \
  --sheet RTD_OPTION_QUOTES \
  --wait-seconds 10
```

Resultado:

```text
Pipeline LISTA_RTD.xlsm -> rtd_option_quotes
Status: ok
read: 4
inserted: 0
updated: 4
skipped: 0
row_count: 4
stale_rows: 0
```

## Ciclo de vida do Excel

O importador passou a usar instância isolada de Excel via `DispatchEx`, sem reaproveitar Excel aberto via `GetActiveObject`.

Também foi implementado fechamento explícito de workbook e encerramento do Excel:

```text
workbook.Close(SaveChanges=False)
excel.Quit()
```

Validação operacional após o pipeline:

```bash
tasklist | grep -i EXCEL
```

Resultado:

```text
sem processos EXCEL.EXE remanescentes
```

## Backups locais

Foram gerados backups operacionais locais em `backups/`.

Esses arquivos são evidências operacionais locais e não devem ser versionados.

O diretório foi adicionado ao `.gitignore`:

```text
backups/
```

## Decisão

A reconciliação funcional da tabela `rtd_option_quotes` e da ponte RTD/Excel foi validada.

A Fase 4 pode ser considerada funcionalmente reconciliada para `rtd_option_quotes`.

A Fase 5 pode ser considerada funcionalmente reconciliada para a ponte:

```text
LISTA_RTD.xlsm -> RTD_OPTION_QUOTES -> rtd_option_quotes
```

A rota pode avançar para preparação da Fase 6, desde que antes seja produzido mapa de impacto para alterações em UI, API, repository ou serviço.
