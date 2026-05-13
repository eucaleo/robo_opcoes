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

