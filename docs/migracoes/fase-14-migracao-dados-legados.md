# Fase 14 — Migração de dados legados

## Status

Concluída.

## Resultado

- Tabela `structure_events` criada a partir do schema oficial.
- 16 registros migráveis de `rtd_rolls_detectados` migrados para `structure_events`.
- Evento legado `OPEN` normalizado como `opening`.
- Todos os eventos migrados possuem vínculo válido com `structures` e `structure_legs`.
- `source` utilizado: `legacy:rtd_rolls_detectados`.
- `event_status` utilizado: `registered`.
- Idempotência baseada no `EVENT_ID` legado armazenado em `metadata_json`.

## Validação

~~~text
structure_events por source/event_type/status:
legacy:rtd_rolls_detectados / opening / registered = 16

Eventos migrados da Fase 14:
16

Vínculos inválidos:
0
~~~

## Pendências

4 registros ABEV3 permaneceram fora da migração por ausência de estrutura canônica:

- ABEVQ134
- ABEVE186
- ABEVQ161
- ABEVE161

Esses registros devem ser tratados em fase posterior de reconciliação de órfãos legados ou criação/mapeamento manual de estrutura ABEV3.

## Observações

- `rtd_hist_robo` permaneceu como legado, sem migração nesta fase.
- `structures` e `structure_legs` não foram remigradas.
