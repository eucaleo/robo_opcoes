# Linha do Tempo v2 -- Executado

## Scripts/Patches aplicados (sequência reproduzível):

### patch_00_fix_gitignore.sh
- Criação/ajuste de: `BAK/`, `ATT/`, `.gitignore`, `.gitkeep`
- Resolvendo problemas de expansão `!` no bash/git
- Comando:
  `$ ./patch_00_fix_gitignore.sh`

---

### patch_01_analyze_repo.sh
- Rodados:
    - `_scan_utils_v2.py`
    - `analyze_code_imports_v2.py`
    - `analyze_pipeline_entrypoints_v2.py`
    - `analyze_sql_usage_v2.py`
    - `analyze_sql_usage_v3.py`
- Artefatos gerados:
    - `ATT/reports/entrypoints_report_v2.json`
    - `ATT/reports/imports_report_v2.json`
    - `ATT/reports/report_v2.json`
    - `ATT/reports/sql_report_v2.json`
    - `ATT/reports/sql_report_v3.json`
- Comando:
  `$ ./patch_01_analyze_repo.sh`
- Saída confirmada: dumps, relatórios `.json` e `.TXT`

---

## DB: Estado após análise

- Dump do `sqlite_master` mostra:
    - **app.db**: 8 tabelas (conforme baseline)
    - **derived.db**: 3 tabelas (payoff_curve_points, structure_decisions, sqlite_sequence)

---

## Próximos patches/documentações recomendados:
- Consolidar baseline (feito acima)
- Detalhar fluxo/run-all e produzir scripts de QA

---

### patch_02_docs_base.sh
- Criou/atualizou: baseline_v2.md, executed_v2.md, roteiro_v2.md, SQL_SURFACE_MAP_v2.md


---

### patch_03_gen_module_map.sh
- Gera/recria docs/MAPA_MODULOS_FUNCOES.md a partir de ATT/reports/sql_report_v3.json
