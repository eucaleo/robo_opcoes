# Ciclo 2 — Fase 7B — Auditoria focada de escrita/importação RTD/opções

Data: 2026-06-14

Branch: ciclo-2-testes-evolucao

## Objetivo

Auditar se existe rotina ativa versionada responsável por importar ou sincronizar dados de opções RTD para a tabela `rtd_option_quotes`.

A auditoria procurou evidências de:

- leitura de `dados/RTD_LINKS.csv`;
- escrita em `rtd_option_quotes`;
- uso de `INSERT`, `UPDATE`, `UPSERT`, `ON CONFLICT`, `REPLACE INTO`, `to_sql`, `executemany` ou equivalente;
- uso de campos de cotação como `codigo_opcao`, `ultimo_preco`, `bid`, `ask`, `volume`, `iv`, `delta`, `gamma`, `theta` e `vega`.

## Evidências encontradas

### Tabela `rtd_option_quotes`

A busca encontrou referências documentais e históricas em `docs/`.

Em código ativo, o principal arquivo identificado foi:

- `repositories/rtd_option_quotes_repository.py`

Esse arquivo contém consultas de leitura usando `FROM rtd_option_quotes`.

Não foram localizadas instruções de escrita nesse repositório.

### Arquivo `RTD_LINKS.csv`

As referências a `RTD_LINKS.csv` aparecem principalmente em documentação, mapeamentos e comentários.

Não foi localizada rotina ativa que leia explicitamente `dados/RTD_LINKS.csv` e grave o resultado em `rtd_option_quotes`.

### Rotinas genéricas de escrita/importação

Foram encontradas rotinas de escrita/importação relacionadas a outras tabelas, como:

- `structures`;
- `structure_legs`;
- `rtd_analise_robo_legs`;
- `manual_analise_robo_legs`;
- `payoff_curve_points`;
- `structure_decisions`;
- `pricing_executions`;
- `structure_events`;
- `structure_snapshots`;
- `structure_leg_snapshots`.

Também existem rotinas genéricas de ingestão CSV e Excel, como:

- `bridge_ingest_csv.py`;
- `db/import_excel.py`.

Porém, não foi localizada rotina ativa que escreva especificamente em `rtd_option_quotes`.

## Conclusões

1. Não foi localizada rotina ativa que leia `dados/RTD_LINKS.csv`.
2. Não foi localizada rotina ativa que escreva em `rtd_option_quotes`.
3. Não foi localizado `INSERT`, `UPDATE`, `UPSERT`, `to_sql` ou `executemany` direcionado a `rtd_option_quotes`.
4. O uso ativo identificado de `rtd_option_quotes` é de leitura via `repositories/rtd_option_quotes_repository.py`.

## Decisão técnica sugerida

Como existe tabela/repositório de leitura, mas não foi encontrada rotina ativa de alimentação, a próxima fase deve criar um importador inicial, isolado e idempotente para:

`dados/RTD_LINKS.csv -> rtd_option_quotes`

O importador deve:

- ler `dados/RTD_LINKS.csv`;
- validar o contrato esperado;
- normalizar campos;
- montar registros por `codigo_opcao`;
- fazer UPSERT em `rtd_option_quotes`;
- preservar `UNIQUE(codigo_opcao)`;
- preencher `source = 'rtd_links'`;
- preencher `raw_json` para rastreabilidade;
- não alterar UI;
- não alterar cálculo;
- não depender de Excel aberto.

## Próxima fase sugerida

Fase 7C — criar importador idempotente `RTD_LINKS.csv` para `rtd_option_quotes`.

Arquivo sugerido:

- `scripts/import_rtd_links_to_option_quotes.py`

Execução sugerida:

- `python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db`

Critérios mínimos:

- modo `--dry-run`;
- validação de colunas obrigatórias;
- parse robusto de números brasileiros;
- UPSERT por `codigo_opcao`;
- log de registros lidos, normalizados, inseridos/atualizados ou ignorados;
- testes unitários sem depender do CSV real.
