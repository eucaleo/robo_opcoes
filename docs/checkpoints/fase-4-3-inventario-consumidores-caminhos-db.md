# Fase 4.3 — Inventário técnico de consumidores de caminhos de banco

## Status

Concluída.

## Tipo

Diagnóstico documental/técnico.

Sem alteração funcional.

## Objetivo

Mapear consumidores funcionais de caminhos de banco SQLite no projeto, com foco em:

- `dados/app.db`;
- `dados/derived.db`;
- `APP_DB_PATH`;
- `DERIVED_DB_PATH`;
- `connect_app()`;
- `connect_derived()`;
- chamadas diretas a `sqlite3.connect()`.

## Fonte técnica atual

O arquivo `db/config.py` é a fonte técnica atual para resolução centralizada de caminhos de banco:

- `APP_DB_PATH`;
- `DERIVED_DB_PATH`;
- `connect_app()`;
- `connect_derived()`.

Ele resolve os caminhos padrão para:

| Banco | Caminho padrão |
|---|---|
| Operacional/raw | `dados/app.db` |
| Derivado/recalculável | `dados/derived.db` |

## Consumidores já aderentes ou parcialmente aderentes a `db/config.py`

| Arquivo | Classificação |
|---|---|
| `services/derived_service.py` | Usa `connect_app()` e `connect_derived()` |
| `scripts/run_derived_pipeline.py` | Usa `connect_derived()` |
| `bridge_ingest_csv.py` | Usa `APP_DB_PATH`, mas ainda possui menção literal em descrição de CLI |
| `UI/models/ui_data.py` | Usa `DERIVED_DB_PATH`, mas mantém conexão direta via `sqlite3.connect()` |

## Consumidores funcionais com caminho literal

Foram identificados consumidores funcionais ainda com defaults ou caminhos literais para `dados/app.db` ou `dados/derived.db`.

### UI

- `UI/components/structure_editor_dialog.py`

### DB interno

- `create_payoff_summary_table.py`
- `db/derived_repo.py`
- `db/init_db.py`
- `db/migrations/add_structure_id_to_payoff_curve_points.py`
- `db/reader.py`
- `db/writer.py`
- `validate_db.py`

### Domínio e infraestrutura

- `domain/payoff_features.py`
- `infra/bootstrap_structures_schema.py`

### Repositórios

- `repositories/pricing_executions_repository.py`
- `repositories/robo_legs_repository.py`
- `repositories/robo_legs_status_repository.py`
- `repositories/rtd_option_quotes_repository.py`
- `repositories/structure_events_repository.py`
- `repositories/structures_repository.py`

### Serviços

- `services/canonical_pricing_facade.py`
- `services/pricing_execution_app_service.py`

### Scripts operacionais

Há scripts operacionais com argumento `--db` ou defaults literais, incluindo:

- `scripts/audit_rtd_option_quotes.py`
- `scripts/import_legacy_structure_legs.py`
- `scripts/import_lista_rtd_excel_to_option_quotes.py`
- `scripts/import_rtd_links_to_option_quotes.py`
- `scripts/purge_derived_snapshots.py`
- `scripts/repair_derived_db_consistency.py`
- `scripts/run_lista_rtd_option_quotes_pipeline.py`
- `scripts/run_rtd_option_quotes_pipeline.py`
- `scripts/seed_current_rtd_option_quotes.py`
- `scripts/validate_app_db.py`
- `scripts/validate_derived_db.py`

## Conexões SQLite diretas

Foram encontradas chamadas diretas a `sqlite3.connect()` em múltiplas camadas.

Esta constatação não implica erro por si só.

A conexão direta é aceitável quando o caminho já foi recebido por parâmetro ou resolvido por fonte centralizada. O risco arquitetural está em:

- caminho literal fixo;
- default duplicado;
- fallback manual fora de `db/config.py`;
- ambiguidade entre `dados/app.db` e `dados/derived.db`.

## Bridge, last_export e resgate

Foram encontradas referências funcionais a:

- `bridge/`;
- `bridge/last_export.txt`;
- fluxo de ingestão via `bridge_ingest_csv.py`.

O ponto funcional principal continua sendo:

- `bridge_ingest_csv.py`.

## Classificação preliminar para fases futuras

| Classe | Descrição | Exemplos |
|---|---|---|
| Centralizador | Define caminhos e conexões oficiais | `db/config.py` |
| Aderente | Usa conexão/path de `db/config.py` | `services/derived_service.py`, `scripts/run_derived_pipeline.py` |
| Parcialmente aderente | Usa constantes centralizadas, mas mantém conexão direta ou texto literal | `bridge_ingest_csv.py`, `UI/models/ui_data.py` |
| Descentralizado funcional | Usa caminho literal ou default duplicado | repositórios, serviços, scripts e módulos DB listados acima |
| Histórico/documental/teste | Ocorrências fora do escopo funcional imediato | `docs/**`, checkpoints, testes |

## Conclusão

A Fase 4.3 confirma que o projeto já possui uma fonte técnica candidata para centralização em `db/config.py`, mas ainda há consumidores funcionais descentralizados.

Nenhuma alteração funcional foi realizada nesta fase.

Próxima etapa recomendada:

- classificar quais consumidores devem ser migrados primeiro;
- priorizar módulos de runtime sobre scripts históricos;
- preservar compatibilidade de argumentos `--db` nos scripts operacionais;
- evitar alteração de comportamento sem testes ou validação específica.
