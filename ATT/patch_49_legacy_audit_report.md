# patch_49 -- Auditoria LegacyRoboLegsFallback

**Data:** 2026-06-03
**Branch:** branch/3a-canonical-domain-decoupling
**Status:** ISOLAMENTO CONFIRMADO

## Modulo auditado

`services/legacy_robo_legs_fallback.py`

## Checklist de isolamento

| Item | Resultado |
|------|-----------|
| Classe `LegacyRoboLegsFallback` definida no modulo correto | OK |
| Sem import direto de `db/` | OK |
| Sem import direto de `repositories/` | OK |
| `fallback_reason` presente em todos os caminhos de retorno | OK |
| `load()` implementado com contrato `(structure, reference_date)` | OK |
| `robo_legs_service` injetado via `__init__` (sem acesso direto a DB) | OK |

## Caminhos de fallback_reason mapeados

| Condicao | fallback_reason |
|----------|----------------|
| `alias_legacy_aba` ausente e `name` ausente | `alias_and_name_missing` |
| `alias_legacy_aba` ausente, `name` presente, name_fallback desabilitado | `alias_missing_name_fallback_disabled` |
| `alias_legacy_aba` ausente, `name` presente, name_fallback habilitado | `alias_missing_name_fallback_used` |
| `robo_legs_service` e None | `robo_legs_service_unavailable` |
| Timestamp nao resolvido | `no_legacy_timestamp_available` |
| Legs nao encontradas para aba/timestamp | `no_legacy_legs_found` |
| Legs encontradas mas nao convertidas | `legacy_legs_not_convertible` |
| Sucesso | None (sem fallback_reason) |

## Acesso a bancos de dados

O modulo nao importa nem referencia diretamente:
- `db/`
- `repositories/`
- `sqlite3`
- `get_app_db_connection`

Todo acesso a dados e delegado ao `robo_legs_service` injetado externamente.

## Decisao

Nenhuma acao de remocao ou refatoracao necessaria.
O modulo esta dentro do boundary definido para compatibilidade legada.
Boundary formalizado no patch_50 via comentario BRIDGE LEGADO em
`services/canonical_input_service.py`.

## Arquivos verificados

- `services/legacy_robo_legs_fallback.py`
- `services/canonical_input_service.py`

## Referencia cruzada

- patch_40: `RoboLegsService` migrado para `get_legs_by_structure_id()`
- patch_50: boundary bridge legado formalizado no `canonical_input_service`
