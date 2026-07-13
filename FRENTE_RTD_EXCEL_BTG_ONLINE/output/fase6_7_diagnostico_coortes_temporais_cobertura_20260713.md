# Fase 6.7 - Diagnostico de coortes temporais de cobertura

Marcador inicio: INICIO_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713

Data de geracao: 2026-07-13T14:35:17+00:00

## Natureza

Diagnostico operacional nao destrutivo e somente leitura.

Esta fase classifica cada linha do historico pelo offset horario que permite encontrar candle correspondente.

## Objetivo

Verificar se existem coortes temporais distintas, por exemplo:

- linhas que exigem offset `-3h`;
- linhas que exigem offset `0h`;
- linhas com timezone explicito em `captured_at`;
- linhas sem timezone explicito em `captured_at`.

## Banco

- Caminho: `dados/app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Volumetria

- Linhas no historico bruto: 60
- Linhas em candles: 110
- Intervalo primario avaliado: 1 minutos
- Linhas cobertas por algum offset: 60/60
- Linhas nao cobertas por nenhum offset: 0
- Cobertura por coortes: 100.0000

## Distribuicao por status

| Valor | Quantidade |
|---|---:|
| `COBERTO` | 60 |

## Distribuicao por offset escolhido

| Valor | Quantidade |
|---|---:|
| `-3` | 50 |
| `0` | 10 |

## Distribuicao por presenca de timezone explicito

| Valor | Quantidade |
|---|---:|
| `com timezone explicito` | 60 |

## Distribuicao por timezone explicito e offset

| Timezone explicito | Offset escolhido | Quantidade |
|---|---:|---:|
| `com timezone explicito` | -3 | 50 |
| `com timezone explicito` | 0 | 10 |

## Amostras classificadas

| ID | Simbolo | Captured raw | Tem timezone explicito | Offsets que cobrem | Offset escolhido | Bucket escolhido | Status |
|---:|---|---|---|---|---:|---|---|
| 11 | `PRIOG800` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 12 | `PRIOT700` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 13 | `PRIOS525` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 14 | `BOVAG34` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 15 | `BOVAH186` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 16 | `BOVAS61` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 17 | `BOVAT158` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 18 | `PRIOH505` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 19 | `BOVAK900` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 20 | `PRIOT690` | `2026-07-11T21:05:03.382706+00:00` | sim | `-3` | -3 | `2026-07-11 18:05:00` | COBERTO |
| 21 | `PRIOG800` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 22 | `PRIOT700` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 23 | `PRIOS525` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 24 | `BOVAG34` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 25 | `BOVAH186` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 26 | `BOVAS61` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 27 | `BOVAT158` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 28 | `PRIOH505` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 29 | `BOVAK900` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 30 | `PRIOT690` | `2026-07-11T21:06:18.727243+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 31 | `PRIOG800` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 32 | `PRIOT700` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 33 | `PRIOS525` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 34 | `BOVAG34` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 35 | `BOVAH186` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 36 | `BOVAS61` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 37 | `BOVAT158` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 38 | `PRIOH505` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 39 | `BOVAK900` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 40 | `PRIOT690` | `2026-07-11T21:06:25.918944+00:00` | sim | `-3` | -3 | `2026-07-11 18:06:00` | COBERTO |
| 41 | `PRIOG800` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 42 | `PRIOT700` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 43 | `PRIOS525` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 44 | `BOVAG34` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 45 | `BOVAH186` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 46 | `BOVAS61` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 47 | `BOVAT158` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 48 | `PRIOH505` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 49 | `BOVAK900` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 50 | `PRIOT690` | `2026-07-11T21:14:49.831254+00:00` | sim | `-3` | -3 | `2026-07-11 18:14:00` | COBERTO |
| 51 | `PRIOG800` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 52 | `PRIOT700` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 53 | `PRIOS525` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 54 | `BOVAG34` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 55 | `BOVAH186` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 56 | `BOVAS61` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 57 | `BOVAT158` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 58 | `PRIOH505` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 59 | `BOVAK900` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 60 | `PRIOT690` | `2026-07-11T21:18:19.235241+00:00` | sim | `-3` | -3 | `2026-07-11 18:18:00` | COBERTO |
| 61 | `PRIOG800` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 62 | `PRIOT700` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 63 | `PRIOS525` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 64 | `BOVAG34` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 65 | `BOVAH186` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 66 | `BOVAS61` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 67 | `BOVAT158` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 68 | `PRIOH505` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 69 | `BOVAK900` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |
| 70 | `PRIOT690` | `2026-07-11T18:22:27.276118-03:00` | sim | `0` | 0 | `2026-07-11 18:22:00` | COBERTO |

## Resultado

- Status: COORTES_TEMPORAIS_MULTIPLAS_CONFIRMADAS: todas as linhas possuem cobertura com offsets distintos; limpeza real segue bloqueada.
- Linhas cobertas por algum offset: 60/60
- Linhas nao cobertas por nenhum offset: 0
- Aprovado para limpeza real: nao
- Registros removidos: 0
- Banco alterado: nao

## Decisao

A Fase 6.7 apenas diagnostica coortes temporais.

Nenhuma regra destrutiva e nenhuma limpeza real ficam autorizadas por esta fase.

Uma fase posterior podera propor regra normalizada de cobertura por coorte, ainda em modo dry-run.

Marcador fim: FIM_FASE6_7_DIAGNOSTICO_COORTES_TEMPORAIS_COBERTURA_20260713
