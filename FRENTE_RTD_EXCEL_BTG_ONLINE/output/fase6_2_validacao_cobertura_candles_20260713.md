# Fase 6.2 - Validação de cobertura dos candles

Marcador inicio: INICIO_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713

Data de geração: 2026-07-13T14:10:00+00:00

## Natureza

Validação operacional não destrutiva e somente leitura.

A finalidade é avaliar se há evidência mínima de cobertura entre histórico intraday bruto e candles consolidados.

## Banco

- Caminho: `dados\app.db`
- Existe: sim
- Tamanho em bytes: 1548288

## Perfis avaliados

### `rtd_option_quotes_intraday_history`

- Existe: sim
- Linhas: 60
- Coluna de chave detectada: não detectada
- Coluna temporal detectada: `captured_at`
- Menor data/hora: `2026-07-11T18:22:27.276118-03:00`
- Maior data/hora: `2026-07-11T21:18:19.235241+00:00`
- Chaves distintas: não disponível

Colunas detectadas:

- `id`
- `captured_at`
- `codigo_opcao`
- `bid`
- `ask`
- `last`
- `vwap`
- `volume`
- `source_updated_at`
- `raw_payload_json`
- `created_at`

### `rtd_option_quotes_intraday_candles`

- Existe: sim
- Linhas: 110
- Coluna de chave detectada: `symbol`
- Coluna temporal detectada: `created_at`
- Menor data/hora: `2026-07-12T12:53:33.754949+00:00`
- Maior data/hora: `2026-07-12T12:53:34.382882+00:00`
- Chaves distintas: 10

Colunas detectadas:

- `id`
- `interval_minutes`
- `bucket_start`
- `symbol`
- `open_price`
- `high_price`
- `low_price`
- `close_price`
- `vwap`
- `bid`
- `ask`
- `spread`
- `volume_delta`
- `updates_count`
- `price_source`
- `created_at`
- `updated_at`

## Comparação

- Comparável por chave: não
- Chaves no histórico sem candles correspondentes: não disponível
- Chaves em candles sem histórico correspondente: não disponível

## Resultado

- Status de cobertura: NAO_CONCLUSIVO: não foi possível comparar chaves entre histórico e candles.
- Aprovado para limpeza real: não
- Registros removidos: 0
- Banco alterado: não

## Decisão

A Fase 6.2 apenas valida cobertura e preserva bloqueio de limpeza real.

Qualquer remoção futura deve exigir aprovação explícita em fase posterior.

Marcador fim: FIM_FASE6_2_VALIDACAO_COBERTURA_CANDLES_20260713
