# Fase 6.4 - Regra explicita de cobertura

Marcador inicio: INICIO_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713

Data de geracao: 2026-07-13T14:21:08+00:00

## Natureza

Validacao operacional nao destrutiva e somente leitura.

Esta fase transforma o mapeamento da Fase 6.3 em uma regra explicita de cobertura.

## Regra explicita avaliada

- Chave do historico: `rtd_option_quotes_intraday_history.codigo_opcao`
- Chave dos candles: `rtd_option_quotes_intraday_candles.symbol`
- Tempo do historico: `rtd_option_quotes_intraday_history.captured_at`
- Bucket dos candles: `rtd_option_quotes_intraday_candles.bucket_start`
- Intervalo dos candles: `rtd_option_quotes_intraday_candles.interval_minutes`

Uma linha do historico e considerada coberta quando existe candle com:

```text
candles.symbol = history.codigo_opcao
candles.interval_minutes = intervalo avaliado
candles.bucket_start = floor(history.captured_at, intervalo avaliado)
```

## Banco

- Caminho: `dados/app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Volumetria

- Linhas no historico bruto: 60
- Linhas em candles: 110
- Intervalos encontrados: 1, 5, 15

## Cobertura por intervalo

| Intervalo min | Historico | Cobertos | Nao cobertos | Cobertura pct | Simbolos historico | Simbolos cobertos | Simbolos nao cobertos | Datas invalidas historico | Datas invalidas candles |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 60 | 10 | 50 | 16.6667 | 10 | 10 | 10 | 0 | 0 |
| 5 | 60 | 10 | 50 | 16.6667 | 10 | 10 | 10 | 0 | 0 |
| 15 | 60 | 10 | 50 | 16.6667 | 10 | 10 | 10 | 0 | 0 |

## Melhor intervalo candidato

- Intervalo: 1 minutos
- Linhas cobertas: 10
- Linhas nao cobertas: 50
- Cobertura percentual: 16.6667

## Resultado

- Status: NAO_CONCLUSIVO: regra candidata ainda apresenta linhas nao cobertas ou datas invalidas.
- Aprovado para limpeza real: nao
- Registros removidos: 0
- Banco alterado: nao

## Decisao

A Fase 6.4 define e avalia uma regra explicita de cobertura, mas nao autoriza limpeza real.

Qualquer remocao futura permanece bloqueada ate fase posterior com aprovacao explicita.

Marcador fim: FIM_FASE6_4_REGRA_EXPLICITA_COBERTURA_20260713
