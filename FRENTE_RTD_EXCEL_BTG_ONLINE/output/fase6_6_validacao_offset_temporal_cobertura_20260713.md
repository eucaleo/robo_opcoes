# Fase 6.6 - Validacao de offset temporal de cobertura

Marcador inicio: INICIO_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713

Data de geracao: 2026-07-13T14:30:58+00:00

## Natureza

Validacao operacional nao destrutiva e somente leitura.

Esta fase testa offsets horarios aplicados ao timestamp do historico bruto antes do calculo do bucket esperado.

## Hipotese validada

A Fase 6.5 mostrou cobertura completa por simbolo e por data, mas baixa cobertura exata de bucket.

A divergencia observada sugere diferenca de fuso horario entre `captured_at` e `bucket_start`.

## Regra avaliada

```text
captured_ajustado = history.captured_at + offset_horas
bucket_esperado = floor(captured_ajustado, candles.interval_minutes)
candles.symbol = history.codigo_opcao
candles.bucket_start = bucket_esperado
```

## Banco

- Caminho: `dados/app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Volumetria

- Linhas no historico bruto: 60
- Linhas em candles: 110
- Intervalos encontrados: 1, 5, 15
- Offsets testados em horas: -12 ate 12

## Ranking de offsets

| Rank | Intervalo min | Offset horas aplicado ao historico | Cobertos | Nao cobertos | Cobertura pct | Pares esperados | Pares candles | Pares esperados ausentes | Pares candles extras |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | -3 | 50 | 10 | 83.3333 | 50 | 50 | 10 | 10 |
| 2 | 5 | -3 | 50 | 10 | 83.3333 | 40 | 40 | 10 | 10 |
| 3 | 15 | -3 | 50 | 10 | 83.3333 | 30 | 20 | 10 | 0 |
| 4 | 1 | 0 | 10 | 50 | 16.6667 | 50 | 50 | 40 | 40 |
| 5 | 5 | 0 | 10 | 50 | 16.6667 | 40 | 40 | 30 | 30 |
| 6 | 15 | 0 | 10 | 50 | 16.6667 | 30 | 20 | 20 | 10 |
| 7 | 1 | -1 | 0 | 60 | 0.0000 | 50 | 50 | 50 | 50 |
| 8 | 1 | 1 | 0 | 60 | 0.0000 | 50 | 50 | 50 | 50 |
| 9 | 5 | -1 | 0 | 60 | 0.0000 | 40 | 40 | 40 | 40 |
| 10 | 5 | 1 | 0 | 60 | 0.0000 | 40 | 40 | 40 | 40 |
| 11 | 15 | -1 | 0 | 60 | 0.0000 | 30 | 20 | 30 | 20 |
| 12 | 15 | 1 | 0 | 60 | 0.0000 | 30 | 20 | 30 | 20 |
| 13 | 1 | -2 | 0 | 60 | 0.0000 | 50 | 50 | 50 | 50 |
| 14 | 1 | 2 | 0 | 60 | 0.0000 | 50 | 50 | 50 | 50 |
| 15 | 5 | -2 | 0 | 60 | 0.0000 | 40 | 40 | 40 | 40 |
| 16 | 5 | 2 | 0 | 60 | 0.0000 | 40 | 40 | 40 | 40 |
| 17 | 15 | -2 | 0 | 60 | 0.0000 | 30 | 20 | 30 | 20 |
| 18 | 15 | 2 | 0 | 60 | 0.0000 | 30 | 20 | 30 | 20 |
| 19 | 1 | 3 | 0 | 60 | 0.0000 | 50 | 50 | 50 | 50 |
| 20 | 5 | 3 | 0 | 60 | 0.0000 | 40 | 40 | 40 | 40 |

## Melhor offset candidato

- Intervalo: 1 minutos
- Offset aplicado ao historico: -3 horas
- Linhas cobertas: 50/60
- Linhas nao cobertas: 10
- Cobertura percentual: 83.3333
- Pares esperados ausentes: 10
- Pares candles extras: 10
- Datas invalidas no historico: 0
- Datas invalidas nos candles: 0

## Amostras de lacunas apos melhor offset

| ID historico | Simbolo | Captured raw | Offset horas | Captured ajustado | Bucket esperado |
|---:|---|---|---:|---|---|
| 61 | `PRIOG800` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 62 | `PRIOT700` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 63 | `PRIOS525` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 64 | `BOVAG34` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 65 | `BOVAH186` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 66 | `BOVAS61` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 67 | `BOVAT158` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 68 | `PRIOH505` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 69 | `BOVAK900` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |
| 70 | `PRIOT690` | `2026-07-11T18:22:27.276118-03:00` | -3 | `2026-07-11 15:22:27` | `2026-07-11 15:22:00` |

## Resultado

- Status: OFFSET_TEMPORAL_CANDIDATO_PARCIAL: ajuste temporal melhora cobertura, mas ainda restam lacunas.
- Aprovado para limpeza real: nao
- Registros removidos: 0
- Banco alterado: nao

## Decisao

A Fase 6.6 apenas valida a hipotese de offset temporal.

Mesmo com cobertura completa, a limpeza real permanece bloqueada ate fase posterior explicitamente aprovada.

Marcador fim: FIM_FASE6_6_VALIDACAO_OFFSET_TEMPORAL_COBERTURA_20260713
