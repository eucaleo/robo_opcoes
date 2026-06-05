
---

## patch_62 — Auditoria wrappers `aba` / deduplicação AbaResolverMixin

**Data:** auto-registrado por patch_62_apply.py

### Alterações
| Arquivo | Ação |
|---|---|
| `repositories/_aba_resolver_mixin.py` | CRIADO — mixin compartilhado |
| `repositories/robo_legs_repository.py` | Herda mixin, remove método local, corrige L251 |
| `repositories/robo_legs_status_repository.py` | Herda mixin, remove método local |
| `services/derived_service.py` | Deprecação formal de `get_payoff_by_aba()` |

### Residuos confirmados como falsos positivos
- `db/derived_repo.py` — `aba` é coluna SQL e parâmetro interno, coberto por `_unwrap_aba()`
- `domain/payoff_features.py:148` — tupla de valores internos, sem wrapper
- `services/derived_service.py` linhas 181, 196, 260, 276 — passagem normal de parâmetro

### Pendente (patch_65)
- Remoção definitiva de `get_payoff_by_aba()`
