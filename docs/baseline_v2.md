# Baseline v2 -- Estado do Sistema

## Tabelas por banco

| Tabela                    | AppDB (`app.db`) | DerivedDB (`derived.db`) | Observações                                            |
|---------------------------|:----------------:|:-----------------------:|--------------------------------------------------------|
| rtd_analise_robo          |        [v]         |                         | Estrutura principal dos robôs                          |
| rtd_analise_robo_legs     |        [v]         |                         | Legs (pernas) de cada estrutura                        |
| rtd_consolidacoes         |        [v]         |                         | Resultados consolidados (outputs pipeline)             |
| payoff_curve_points       |                  |           [v]            | Pontos da curva payoff (resultado calculado)           |
| structure_decisions       |                  |           [v]            | Decisão por estrutura/aba após pipeline                |
| payoff_curve_summary      |                  |           ~             | Referência no código, mas não vista em derived.db      |
| payoff_points             |                  |           ~             | Só referência na UI e schema, não criado por padrão    |

Obs:
~ = referenciada, mas não apareceu no dump/sqlite_master até aqui.
Outras tabelas de suporte/utilidade podem existir e serão mapeadas conforme evolução.

---

## Regra central do domínio ("1 aba = 1 estrutura")

- A lista de estruturas ("abas") é obtida via:
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

