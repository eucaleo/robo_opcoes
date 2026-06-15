# Checkpoint — Fase 8B — Reconciliação de estruturas/legs com rtd_option_quotes

## Objetivo

Reconciliar as estruturas e legs persistidas com as cotações atuais disponíveis em `rtd_option_quotes`, antes de qualquer alteração funcional no fluxo de snapshot, cálculo ou UI.

## Evidência associada

A evidência bruta da auditoria foi registrada em:

```text
docs/checkpoints/fase-8b-diagnostico-reconciliacao-rtd-option-quotes.txt
```

Commit da evidência:

```text
bde167f docs: registra diagnostico reconciliacao rtd option quotes fase 8b
```

## Banco auditado

```text
dados/app.db
```

## Estruturas encontradas

Foram encontradas 5 estruturas em `structures`:

```text
BOVA11  archived
EMBJ3   active
PRIO3   active
SBSP3   active
SMAL11  active
```

## Legs canônicas encontradas

A tabela `structure_legs` contém 20 legs associadas às estruturas.

As legs observadas apontam majoritariamente para vencimentos antigos:

```text
2026-04-17
2026-05-15
```

Exemplos:

```text
PRIOD750
PRIOE515
PRIOQ720
PRIOP600
SMALD139
SMALE119
SMALQ119
SMALP970
```

## Cotações RTD atuais encontradas

A tabela `rtd_option_quotes` contém 8 cotações atuais importadas de `LISTA_RTD.xlsm`.

Códigos observados:

```text
PRIOG800
PRIOH515
PRIOS525
PRIOT700
SMALF103
SMALF129
SMALR108
SMALR127
```

Os vencimentos observados em `rtd_option_quotes` são:

```text
2026-06-19
2026-07-17
2026-08-21
```

## Resultado do match exato

A comparação direta:

```text
structure_legs.symbol = rtd_option_quotes.codigo_opcao
```

retornou zero correspondências.

Resultado operacional:

```text
matched_legs: 0
```

## Resultado do match aproximado

Foi encontrada apenas uma coincidência aproximada por ativo, tipo e strike:

```text
structure_legs.symbol: PRIOE515
structure_legs.expiration_date: 2026-05-15
structure_legs.strike: 51.5

rtd_option_quotes.codigo_opcao: PRIOH515
rtd_option_quotes.vencimento: 2026-08-21
rtd_option_quotes.strike: 51.5
```

Essa coincidência não deve ser tratada como match funcional, pois o código da opção e o vencimento são diferentes.

```text
PRIOE515 != PRIOH515
2026-05-15 != 2026-08-21
```

## Achado principal

As estruturas/legs persistidas em `structure_legs` estão desatualizadas em relação às cotações atuais importadas para `rtd_option_quotes`.

O problema não está ainda no mecanismo de snapshot, mas na divergência anterior entre:

```text
legs persistidas em structure_legs
        e
códigos atuais importados em rtd_option_quotes
```

## Decisão técnica

Não integrar `rtd_option_quotes` ao snapshot neste momento.

Não alterar ainda:

```text
services/market_snapshot_selector.py
services/canonical_pricing_facade.py
repositories/market_snapshot_repository.py
```

Também não alterar cálculo, UI ou schema nesta fase.

## Justificativa

Uma integração funcional agora continuaria sem utilizar as cotações RTD atuais, pois o join por código exato retorna zero correspondências.

Além disso, usar match aproximado por ativo, tipo e strike seria inseguro, pois pode ligar opções de vencimentos diferentes.

## Risco evitado

A fase evita o risco de mascarar o problema real:

```text
structure_legs representa legs antigas/vencidas,
enquanto rtd_option_quotes representa códigos atuais vindos do LISTA_RTD.xlsm.
```

## Próxima etapa recomendada

Abrir a fase:

```text
Fase 8C — Origem da verdade das legs atuais
```

Objetivos:

1. Auditar `rtd_analise_robo_legs`.
2. Comparar `rtd_analise_robo_legs` com `structure_legs`.
3. Comparar ambas com `rtd_option_quotes`.
4. Confirmar se `LISTA_RTD.xlsm` contém apenas cotações ou também contém composição atual das estruturas.
5. Identificar o importador responsável por atualizar as legs canônicas.
6. Definir se `structure_legs` deve ser atualizada a partir de uma fonte controlada.

## Arquivos funcionais alterados nesta fase

Nenhum.

## Status

Fase 8B concluída como reconciliação diagnóstica sem alteração funcional.
