# Inventário de Patches

| Patch | Data | Status | Branch | Descrição |
|-------|------|--------|--------|-----------|
| patch_37 | 2026-06-02 | ✅ Aplicado | patch/3a-canonical-domain-decoupling | Remoção resíduos aba/abas: `_cache_abas`, `get_abas()`, `update_abas()` — arquivos: `ui_data.py`, `filters_panel.py`, `main_window.py` |
## patch_38 — Polish pós-patch_37 (2026-06-02)
get_structures() lazy-load consolidado; comentário regex corrigido

## patch_39  Restauração get_abas() alias (2026-06-02)
Over-removal do patch_37 corrigido: get_abas() recolocado como alias readonly
de get_structure_ids() conforme PERMANENT_DECISIONS[patch_34:filtro_aba].
5 testes de regressão restaurados (test_regression_aba_compat, test_ui_data_migration,
test_patch34_ui_data).

## patch_56 — StructureRef Propagation (2026-06-03 20:59)
- Corrigido bug f-string em get_payoff_by_aba()
- Corrigido NameError (aba,) -> col, val = ref.db_pair()
- Migrado get_payoff_by_structure_id() para StructureRef.from_id()
- Adicionado _unwrap_aba() em derived_repo.py
- 6 funções standalone aceitam str | StructureRef
