# Fase 4.1 — Inventário de caminhos de banco e contratos

Data: 2026-06-17  
Branch: `fase-12-fechamento-ciclo`  
Tipo: diagnóstico documental / somente leitura funcional

## Objetivo

Inventariar os caminhos de banco SQLite usados pelo projeto e comparar:

- contrato documental;
- existência física/local dos bancos;
- resolução de caminhos no código;
- referências em testes, scripts e UI;
- riscos de divergência entre documentação e implementação.

Nenhuma alteração funcional foi realizada nesta fase.

## Contrato documental vigente

O arquivo `docs/DB_PATHS.md` declara:

- Raw DB: `dados/app.db`
- Derived DB: `dados/derived.db`
- Bridge: `bridge/*.csv` + `bridge/last_export.txt`

Leitura: o contrato conceitual principal está correto.

## Bancos locais identificados

Foram identificados bancos e artefatos relacionados a SQLite, incluindo:

- `dados/app.db`
- `dados/derived.db`
- `_resgate_db/estado_schema_atual/app_schema_atual_vazio.db`
- `_resgate_db/estado_schema_atual/derived_schema_atual_vazio.db`
- `db/init_db.py`
- `validate_db.py`
- `scripts/validate_app_db.py`
- `scripts/validate_derived_db.py`

Os bancos reais estão ignorados pelo Git via `.gitignore`.

## Scripts documentados ausentes

A documentação referencia ferramentas que não existem no estado atual do repositório:

- `scripts/db_locator.py`
- `scripts/db_path_doctor.py`
- `scripts/find_dbs.sh`

Impacto: não afeta diretamente o funcionamento, mas cria dívida documental.

## Configuração central observada

O arquivo `db/config.py` contém os caminhos mais claros e parametrizáveis:

- `APP_DB_PATH`
- `DERIVED_DB_PATH`

Com fallback para:

- `dados/app.db`
- `dados/derived.db`

Também permite override por variáveis de ambiente.

## Uso de `dados/app.db`

O banco `dados/app.db` aparece como base operacional/raw em:

- `db/init_db.py`
- `validate_db.py`
- `scripts/validate_app_db.py`
- `repositories/structures_repository.py`
- `repositories/structure_events_repository.py`
- `repositories/pricing_executions_repository.py`
- `repositories/system_snapshots_repository.py`
- `repositories/rtd_option_quotes_repository.py`
- `repositories/robo_legs_repository.py`
- `repositories/robo_legs_status_repository.py`
- `repositories/market_snapshot_repository.py`
- `services/canonical_pricing_facade.py`
- `UI/main_window.py`
- `UI/components/structure_editor_dialog.py`
- `UI/components/structures_list_panel.py`

Leitura: a camada operacional está majoritariamente ligada ao `app.db`.

## Uso de `dados/derived.db`

O banco `dados/derived.db` aparece como base derivada/recalculável em:

- `db/derived_repo.py`
- `db/reader.py`
- `db/writer.py`
- `domain/payoff_features.py`
- `UI/models/ui_data.py`
- `UI/components/details_panel.py`
- `scripts/validate_derived_db.py`
- `scripts/repair_derived_db_consistency.py`
- `scripts/purge_derived_snapshots.py`

Leitura: dados de payoff, decisões e artefatos derivados usam predominantemente `derived.db`.

## Caso especial: `rtd_option_quotes`

O arquivo `services/canonical_pricing_facade.py` possui lógica específica para resolver o banco da tabela `rtd_option_quotes`.

A função `_resolve_rtd_option_quotes_db_path` considera:

- o banco primário recebido;
- `primary_db_path.parent / "app.db"`;
- `Path("dados/app.db")`.

Leitura: existe compatibilização para fluxos em que a facade é instanciada com `derived.db`, mas a tabela `rtd_option_quotes` reside em `app.db`.

Essa lógica possui cobertura em:

- `ATT/tests/test_canonical_pricing_facade_rtd_db_path.py`

## UI

A UI utiliza ambos os bancos:

- `UI/main_window.py` define caminho operacional para `dados/app.db`;
- `UI/models/ui_data.py` usa `DERIVED_DB_PATH`;
- `UI/components/details_panel.py` possui lógica própria para separar acesso a `derived.db` e `app.db`.

Risco: há resolução de caminhos distribuída dentro da UI.

## Riscos identificados

### 1. Documentação desatualizada

`docs/DB_PATHS.md` e `docs/DATABASE_LOCATOR.md` citam scripts ausentes.

### 2. Centralização parcial

Apesar de `db/config.py` existir, vários módulos ainda usam caminhos próprios como:

- `dados/app.db`
- `./dados/app.db`
- `dados/derived.db`
- `Path("dados/app.db")`
- `PROJECT_ROOT / "dados" / "app.db"`

### 3. Caminhos relativos

Alguns pontos usam caminhos relativos, o que pode gerar risco se scripts forem executados fora da raiz do projeto.

### 4. Lógica especial espalhada

Há resolução específica em `services/canonical_pricing_facade.py` e em `UI/components/details_panel.py`.

## Conclusão

O contrato conceitual está consistente:

| Papel | Caminho |
|---|---|
| Banco operacional/raw | `dados/app.db` |
| Banco derivado/recalculável | `dados/derived.db` |
| Bridge CSV | `bridge/*.csv` + `bridge/last_export.txt` |
| Resgate/schema vazio | `_resgate_db/estado_schema_atual/*.db` |

Porém há dívida documental e técnica:

1. scripts documentados não existem;
2. docs precisam ser reconciliados;
3. paths estão parcialmente centralizados;
4. há mistura de caminhos relativos e absolutos;
5. a UI e a facade possuem resoluções próprias.

## Próxima fase recomendada

Fase 4.2 — Reconciliação documental dos caminhos de banco.

Escopo recomendado:

- atualizar `docs/DB_PATHS.md`;
- atualizar `docs/DATABASE_LOCATOR.md`;
- registrar que `db/config.py` é o candidato natural a fonte técnica central;
- não alterar comportamento funcional ainda.

## Regra preservada

Diagnóstico primeiro. Alteração funcional somente após contrato reconciliado.
