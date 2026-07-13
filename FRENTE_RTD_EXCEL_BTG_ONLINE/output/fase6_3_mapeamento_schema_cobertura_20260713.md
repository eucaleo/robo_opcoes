# Fase 6.3 - Mapeamento de schema para cobertura de candles

Marcador inicio: INICIO_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713

Data de geracao: 2026-07-13T14:14:08+00:00

## Natureza

Mapeamento operacional nao destrutivo e somente leitura.

A finalidade e identificar pares de colunas candidatos para tornar a validacao de cobertura mais objetiva.

## Banco

- Caminho: `dados/app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Tabela `rtd_option_quotes_intraday_history`

- Existe: sim
- Linhas: 60

| Coluna | Tipo | Not null | PK | Nao nulos | Distintos | Chave candidata | Temporal candidata |
|---|---|---:|---:|---:|---:|---:|---:|
| `id` | `INTEGER` | nao | 1 | 60 | 60 | nao | nao |
| `captured_at` | `TEXT` | sim | 0 | 60 | 6 | nao | sim |
| `codigo_opcao` | `TEXT` | sim | 0 | 60 | 10 | sim | nao |
| `bid` | `REAL` | nao | 0 | 60 | 7 | nao | nao |
| `ask` | `REAL` | nao | 0 | 60 | 6 | nao | nao |
| `last` | `REAL` | nao | 0 | 60 | 10 | nao | nao |
| `vwap` | `REAL` | nao | 0 | 60 | 7 | nao | nao |
| `volume` | `REAL` | nao | 0 | 60 | 7 | nao | nao |
| `source_updated_at` | `TEXT` | nao | 0 | 60 | 4 | nao | sim |
| `raw_payload_json` | `TEXT` | sim | 0 | 60 | 11 | nao | nao |
| `created_at` | `TEXT` | sim | 0 | 60 | 7 | nao | sim |

## Tabela `rtd_option_quotes_intraday_candles`

- Existe: sim
- Linhas: 110

| Coluna | Tipo | Not null | PK | Nao nulos | Distintos | Chave candidata | Temporal candidata |
|---|---|---:|---:|---:|---:|---:|---:|
| `id` | `INTEGER` | nao | 1 | 110 | 110 | nao | nao |
| `interval_minutes` | `INTEGER` | sim | 0 | 110 | 3 | nao | nao |
| `bucket_start` | `TEXT` | sim | 0 | 110 | 9 | nao | sim |
| `symbol` | `TEXT` | sim | 0 | 110 | 10 | sim | nao |
| `open_price` | `REAL` | nao | 0 | 110 | 10 | nao | nao |
| `high_price` | `REAL` | nao | 0 | 110 | 10 | nao | nao |
| `low_price` | `REAL` | nao | 0 | 110 | 10 | nao | nao |
| `close_price` | `REAL` | nao | 0 | 110 | 10 | nao | nao |
| `vwap` | `REAL` | nao | 0 | 110 | 7 | nao | nao |
| `bid` | `REAL` | nao | 0 | 110 | 7 | nao | nao |
| `ask` | `REAL` | nao | 0 | 110 | 6 | nao | nao |
| `spread` | `REAL` | nao | 0 | 110 | 7 | nao | nao |
| `volume_delta` | `REAL` | nao | 0 | 40 | 1 | nao | nao |
| `updates_count` | `INTEGER` | nao | 0 | 110 | 4 | nao | sim |
| `price_source` | `TEXT` | nao | 0 | 110 | 1 | nao | nao |
| `created_at` | `TEXT` | sim | 0 | 110 | 3 | nao | sim |
| `updated_at` | `TEXT` | sim | 0 | 110 | 3 | nao | sim |

## Pares candidatos para comparacao

| Historico | Candles | Score | Motivo | Distintos historico | Distintos candles | Historico sem candles | Candles sem historico |
|---|---|---:|---|---:|---:|---:|---:|
| `created_at` | `created_at` | 145 | mesmo nome de coluna; ambas parecem colunas temporais; mesmo tipo declarado | 7 | 3 | 7 | 3 |
| `id` | `id` | 120 | mesmo nome de coluna; mesmo tipo declarado; cardinalidade relativamente proxima | 60 | 110 | 60 | 110 |
| `bid` | `bid` | 120 | mesmo nome de coluna; mesmo tipo declarado; cardinalidade relativamente proxima | 7 | 7 | 0 | 0 |
| `ask` | `ask` | 120 | mesmo nome de coluna; mesmo tipo declarado; cardinalidade relativamente proxima | 6 | 6 | 0 | 0 |
| `vwap` | `vwap` | 120 | mesmo nome de coluna; mesmo tipo declarado; cardinalidade relativamente proxima | 7 | 7 | 0 | 0 |
| `codigo_opcao` | `symbol` | 60 | ambas parecem colunas de chave; mesmo tipo declarado; cardinalidade relativamente proxima | 10 | 10 | 0 | 0 |
| `captured_at` | `bucket_start` | 55 | ambas parecem colunas temporais; mesmo tipo declarado; cardinalidade relativamente proxima | 6 | 9 | 6 | 9 |
| `captured_at` | `created_at` | 55 | ambas parecem colunas temporais; mesmo tipo declarado; cardinalidade relativamente proxima | 6 | 3 | 6 | 3 |
| `captured_at` | `updated_at` | 55 | ambas parecem colunas temporais; mesmo tipo declarado; cardinalidade relativamente proxima | 6 | 3 | 6 | 3 |
| `source_updated_at` | `created_at` | 55 | ambas parecem colunas temporais; mesmo tipo declarado; cardinalidade relativamente proxima | 4 | 3 | 4 | 3 |
| `source_updated_at` | `updated_at` | 55 | ambas parecem colunas temporais; mesmo tipo declarado; cardinalidade relativamente proxima | 4 | 3 | 4 | 3 |
| `created_at` | `bucket_start` | 55 | ambas parecem colunas temporais; mesmo tipo declarado; cardinalidade relativamente proxima | 7 | 9 | 7 | 9 |
| `captured_at` | `updates_count` | 45 | ambas parecem colunas temporais; cardinalidade relativamente proxima | 6 | 4 | 6 | 4 |
| `source_updated_at` | `bucket_start` | 45 | ambas parecem colunas temporais; mesmo tipo declarado | 4 | 9 | 4 | 9 |
| `source_updated_at` | `updates_count` | 45 | ambas parecem colunas temporais; cardinalidade relativamente proxima | 4 | 4 | 4 | 4 |
| `created_at` | `updates_count` | 45 | ambas parecem colunas temporais; cardinalidade relativamente proxima | 7 | 4 | 7 | 4 |
| `created_at` | `updated_at` | 45 | ambas parecem colunas temporais; mesmo tipo declarado | 7 | 3 | 7 | 3 |

## Resultado

- Status: NAO_CONCLUSIVO: melhor par ainda indica historico sem candles correspondentes ou requer validacao humana.
- Aprovado para limpeza real: nao
- Registros removidos: 0
- Banco alterado: nao

## Decisao

A Fase 6.3 apenas mapeia schema e candidatos de comparacao.

A execucao de limpeza real permanece bloqueada ate aprovacao explicita em fase posterior.

Marcador fim: FIM_FASE6_3_MAPEAMENTO_SCHEMA_COBERTURA_20260713
