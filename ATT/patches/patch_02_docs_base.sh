#!/bin/bash
set -euo pipefail

# Descobre a raiz do repositório a partir de ATT/patches
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

mkdir -p docs

# === baseline_v2.md ===
cat > docs/baseline_v2.md <<'EOF'
# Baseline v2 — Estado do Sistema

## Tabelas por banco

| Tabela                    | AppDB (`app.db`) | DerivedDB (`derived.db`) | Observações                                            |
|---------------------------|:----------------:|:-----------------------:|--------------------------------------------------------|
| rtd_analise_robo          |        ✔️         |                         | Estrutura principal dos robôs                          |
| rtd_analise_robo_legs     |        ✔️         |                         | Legs (pernas) de cada estrutura                        |
| rtd_consolidacoes         |        ✔️         |                         | Resultados consolidados (outputs pipeline)             |
| payoff_curve_points       |                  |           ✔️            | Pontos da curva payoff (resultado calculado)           |
| structure_decisions       |                  |           ✔️            | Decisão por estrutura/aba após pipeline                |
| payoff_curve_summary      |                  |           ~             | Referência no código, mas não vista em derived.db      |
| payoff_points             |                  |           ~             | Só referência na UI e schema, não criado por padrão    |

Obs:
~ = referenciada, mas não apareceu no dump/sqlite_master até aqui.
Outras tabelas de suporte/utilidade podem existir e serão mapeadas conforme evolução.

---

## Regra central do domínio (“1 aba = 1 estrutura”)

- A lista de estruturas (“abas”) é obtida via:
  - `SELECT DISTINCT aba FROM rtd_analise_robo`
  - evidência: linha 38 `scripts/run_derived_pipeline.py`
- Detalhe (legs) por estrutura:
  - `rtd_analise_robo_legs`, associando `aba`, `timestamp`, detalhes das pernas

---

## Tabelas/colunas essenciais

- Chave de estrutura: coluna `aba` (string)
- Timestamp: usado para versões, histórico de legs/estrutura
- `pl_realista_total`: métrica central na pipeline

---

## Fontes importantes para pipeline/estado

- CSVs e Excel vêm pela ponte `bridge_ingest_csv.py` (constrói tabelas dinamicamente)
- Depois, normalização via pipeline e escritor/reader no derived

EOF

# === executed_v2.md ===
cat > docs/executed_v2.md <<'EOF'
# Linha do Tempo v2 — Executado

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

EOF

# === roteiro_v2.md ===
cat > docs/roteiro_v2.md <<'EOF'
# Roteiro v2 — Fluxo operacional principal

## 1. Ingestão (pré-pipeline)
- Origem: exportação por Excel, scripts `bridge_ingest_csv.py`
- DB de entrada: `app.db`
- Estruturas/abas populadas via `rtd_analise_robo`, legs em `rtd_analise_robo_legs`

## 2. Pipeline derivada
- Roda via: `scripts/run_derived_pipeline.py`
- Origem: `app.db`
- Destino: `derived.db`
- Gera tabelas: `payoff_curve_points`, `structure_decisions`
- Consultas centrais:
    - `SELECT DISTINCT aba FROM rtd_analise_robo`
    - Uso intenso de timestamp e `pl_realista_total`

## 3. UI (visualização)
- Principal: `python -m UI.main_window`
- Consome: `derived.db`
- Exibe e detalha: payoff_curve_points, decisions, logs/auditoria

## 4. (Planejado) QA automatizado
- Injetar casos em `app.db`
- Rodar pipeline derivada
- Verificar resultado na UI ou via scripts de teste

EOF

# === SQL surface map direto ===
cat > docs/SQL_SURFACE_MAP_v2.md <<'EOF'
# Mapa de Uso SQL (surface) — v2

| Tabela                  | Operação (CRUD)   | Arquivos/Modulos                                 |
|-------------------------|-------------------|--------------------------------------------------|
| rtd_analise_robo        | SELECT            | domain/decision.py, domain/payoff.py, scripts/run_derived_pipeline.py |
| rtd_analise_robo_legs   | SELECT            | domain/payoff.py                                 |
| rtd_consolidacoes       | INSERT            | services/derived_service.py                      |
| payoff_curve_points     | CREATE            | db/schema.py, db/derived_repo.py                 |
|                         | INSERT/UPDATE     | db/writer.py, db/derived_repo.py                 |
|                         | SELECT            | db/reader.py, services/derived_service.py, scripts/build_payoff_summaries.py, scripts/derived_viewer.py, UI/components/details_panel.py, UI/models/ui_data.py |
| structure_decisions     | CREATE            | db/schema.py, db/derived_repo.py                 |
|                         | INSERT/UPDATE     | db/writer.py, db/derived_repo.py                 |
|                         | SELECT            | db/reader.py, services/derived_service.py, scripts/derived_viewer.py, UI/components/details_panel.py, scripts/conferir_fechamento_v1.py |
| payoff_curve_summary    | CREATE            | create_payoff_summary_table.py                   |
|                         | INSERT            | domain/payoff_features.py                        |
| payoff_points           | CREATE            | db/schema.py                                     |
|                         | (comentário na UI)| UI/components/payoff_chart.py                    |

Obs:
- Só incluímos aqui tabelas presentes no código principal, ignorando ruídos das libs/venv.
- Operações base: CREATE TABLE, SELECT, INSERT, UPDATE, DELETE.

EOF

echo "Patch 02 (DOCS base) aplicado com sucesso. Confira arquivos em ./docs"
