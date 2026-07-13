# Fase 6.9 - Dry-run de limpeza com timezone local canonico

Marcador inicio: INICIO_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713

Data de geracao: 2026-07-13T16:26:51+00:00

## Natureza

Dry-run operacional, nao destrutivo e somente leitura.

Esta fase simula quais linhas do historico bruto seriam elegiveis para limpeza por ja possuirem candle correspondente pela regra canonica local.

## Regra canonica usada

```text
Timezone local operacional: America/Sao_Paulo
history.captured_at com timezone -> converter para America/Sao_Paulo
history.captured_at sem timezone -> assumir America/Sao_Paulo
candles.bucket_start -> tratar como horario local operacional
elegibilidade = existe candle com mesmo simbolo e mesmo bucket local
```

## Banco

- Caminho: `dados/app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Volumetria do dry-run

- Linhas no historico bruto: 60
- Linhas em candles: 110
- Intervalo primario avaliado: 1 minutos
- Linhas elegiveis por cobertura canonica local: 60/60
- Linhas bloqueadas: 0
- Percentual elegivel: 100.0000
- Datas invalidas no historico: 0
- Datas invalidas nos candles: 0

## Distribuicao por elegibilidade

| Valor | Quantidade |
|---|---:|
| `elegivel` | 60 |

## Distribuicao por motivo

| Valor | Quantidade |
|---|---:|
| `COBERTO_POR_CANDLE_CANONICO_LOCAL` | 60 |

## Distribuicao por origem de timezone em captured_at

| Valor | Quantidade |
|---|---:|
| `aware_UTC+00:00` | 50 |
| `aware_UTC-03:00` | 10 |

## IDs simulados

- IDs elegiveis simulados: `11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70`
- IDs bloqueados: ``

## Amostras do dry-run

| ID | Simbolo | Captured raw | Origem timezone | Captured local | Bucket local esperado | Elegivel | Motivo |
|---:|---|---|---|---|---|---|---|
| 11 | `PRIOG800` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 12 | `PRIOT700` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 13 | `PRIOS525` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 14 | `BOVAG34` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 15 | `BOVAH186` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 16 | `BOVAS61` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 17 | `BOVAT158` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 18 | `PRIOH505` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 19 | `BOVAK900` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 20 | `PRIOT690` | `2026-07-11T21:05:03.382706+00:00` | `aware_UTC+00:00` | `2026-07-11 18:05:03` | `2026-07-11 18:05:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 21 | `PRIOG800` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 22 | `PRIOT700` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 23 | `PRIOS525` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 24 | `BOVAG34` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 25 | `BOVAH186` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 26 | `BOVAS61` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 27 | `BOVAT158` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 28 | `PRIOH505` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 29 | `BOVAK900` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 30 | `PRIOT690` | `2026-07-11T21:06:18.727243+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:18` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 31 | `PRIOG800` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 32 | `PRIOT700` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 33 | `PRIOS525` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 34 | `BOVAG34` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 35 | `BOVAH186` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 36 | `BOVAS61` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 37 | `BOVAT158` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 38 | `PRIOH505` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 39 | `BOVAK900` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 40 | `PRIOT690` | `2026-07-11T21:06:25.918944+00:00` | `aware_UTC+00:00` | `2026-07-11 18:06:25` | `2026-07-11 18:06:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 41 | `PRIOG800` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 42 | `PRIOT700` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 43 | `PRIOS525` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 44 | `BOVAG34` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 45 | `BOVAH186` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 46 | `BOVAS61` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 47 | `BOVAT158` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 48 | `PRIOH505` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 49 | `BOVAK900` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 50 | `PRIOT690` | `2026-07-11T21:14:49.831254+00:00` | `aware_UTC+00:00` | `2026-07-11 18:14:49` | `2026-07-11 18:14:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 51 | `PRIOG800` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 52 | `PRIOT700` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 53 | `PRIOS525` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 54 | `BOVAG34` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 55 | `BOVAH186` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 56 | `BOVAS61` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 57 | `BOVAT158` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 58 | `PRIOH505` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 59 | `BOVAK900` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 60 | `PRIOT690` | `2026-07-11T21:18:19.235241+00:00` | `aware_UTC+00:00` | `2026-07-11 18:18:19` | `2026-07-11 18:18:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 61 | `PRIOG800` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 62 | `PRIOT700` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 63 | `PRIOS525` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 64 | `BOVAG34` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 65 | `BOVAH186` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 66 | `BOVAS61` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 67 | `BOVAT158` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 68 | `PRIOH505` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 69 | `BOVAK900` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |
| 70 | `PRIOT690` | `2026-07-11T18:22:27.276118-03:00` | `aware_UTC-03:00` | `2026-07-11 18:22:27` | `2026-07-11 18:22:00` | sim | `COBERTO_POR_CANDLE_CANONICO_LOCAL` |

## Resultado

- Status: DRY_RUN_CANONICO_VALIDADO: todas as linhas do historico bruto estao cobertas por candles pela regra local; limpeza real segue bloqueada.
- Linhas elegiveis por cobertura canonica local: 60/60
- Linhas bloqueadas: 0
- Aprovado para limpeza real: nao
- Registros removidos: 0
- Banco alterado: nao

## Decisao

A Fase 6.9 e apenas dry-run.

Mesmo com cobertura completa, nenhuma remocao real fica autorizada por esta fase.

A proxima fase podera criar o plano operacional de execucao controlada, com backup obrigatorio e comando separado de confirmacao.

Marcador fim: FIM_FASE6_9_DRY_RUN_LIMPEZA_CANONICA_TIMEZONE_LOCAL_20260713
