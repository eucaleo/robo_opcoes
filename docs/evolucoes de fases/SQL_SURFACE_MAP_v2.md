# Mapa de Uso SQL (surface) -- v2

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

