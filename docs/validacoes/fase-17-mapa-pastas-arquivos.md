# Fase 17 — Mapa de Pastas e Arquivos

## 1. Objetivo

Registrar uma fotografia oficial da estrutura atual do repositório após a conclusão da Fase 16 — limpeza, versionamento e release.

A Fase 17 não realiza limpeza, remoção ou refatoração. Seu objetivo é mapear o estado real do projeto para servir como base confiável para próximas fases.

---

## 2. Estado Git da coleta

Dados coletados em:

~~~text
DATA_COLETA=2026-06-12 21:08:42
BRANCH=fase-17-mapa-pastas-arquivos
HEAD=8e5f1f1
~~~

Branch ativa:

~~~text
fase-17-mapa-pastas-arquivos
~~~

Commit atual:

~~~text
8e5f1f1 fase 16: consolida limpeza versionamento e release
~~~

Situação do working tree na coleta:

~~~text
git status --short: limpo
~~~

A branch da Fase 17 foi atualizada com a Fase 16 por fast-forward.

---

## 3. Resumo quantitativo

| Item | Quantidade |
|---|---:|
| Arquivos versionados | 200 |
| Arquivos não rastreados | 0 |
| Diretórios físicos mapeados | 53 |
| Arquivos físicos mapeados | 353 |
| Checks em `ATT/checks` | 7 |
| Testes em `ATT/tests` | 45 |

Arquivos de auditoria gerados localmente em:

~~~text
_repo_audit/fase17/
~~~

A pasta `_repo_audit/` está ignorada pelo Git.

---

## 4. Diretórios principais identificados

Diretórios de primeiro nível identificados no projeto:

~~~text
.git
.pytest_cache
ATT
UI
__pycache__
_repo_audit
api
bridge
dados
db
docs
domain
dto
infra
logs
reports
repositories
scripts
services
src
utils
validators
~~~

Classificação inicial:

| Diretório | Função observada |
|---|---|
| `ATT/` | Checks e testes automatizados |
| `UI/` | Interface gráfica |
| `api/` | Controllers e camada de API |
| `bridge/` | Arquivos CSV de integração/legado |
| `dados/` | Bancos, backups e dados locais não versionados |
| `db/` | Configuração, schemas, leitura, escrita e migrações de banco |
| `docs/` | Documentação técnica, histórica, decisões, migrações e validações |
| `domain/` | Camada de domínio |
| `dto/` | Objetos de transferência |
| `infra/` | Infraestrutura de banco e bootstrap |
| `logs/` | Logs locais ignorados |
| `reports/` | Diretório físico de relatórios |
| `repositories/` | Repositórios de acesso a dados |
| `scripts/` | Scripts operacionais, validações, reparos e pipelines |
| `services/` | Serviços de aplicação, domínio, pricing, eventos e legados |
| `src/` | Código complementar, atualmente com referência de domínio |
| `utils/` | Utilitários |
| `validators/` | Validadores |
| `_repo_audit/` | Auditoria local ignorada |
| `.pytest_cache/` e `__pycache__/` | Caches ignorados |

---

## 5. Arquivos relevantes na raiz

Arquivos físicos identificados na raiz:

~~~text
.gitignore
LISTA_RTD.xlsx
LISTA_RTD.xlsm
bridge_ingest_csv.py
create_payoff_summary_table.py
debug_bridge_check_after_vba.py
debug_bridge_mainwindow.py
debug_bridge_writer.py
find_structure.sh
limpar_repositorio_seguro.sh
log_execucao.txt
main.py
mapear_repositorio.sh
run_ui.py
validate_db.py
~~~

Observações:

- `LISTA_RTD.xlsm` está versionado.
- `LISTA_RTD.xlsx` está versionado.
- Scripts principais como `main.py`, `run_ui.py`, `validate_db.py`, `bridge_ingest_csv.py` e scripts auxiliares estão versionados.
- Arquivos locais de debug `debug_bridge_*.py` estão ignorados.
- `log_execucao.txt` está ignorado.

---

## 6. Arquivos críticos

| Arquivo | Existe | Versionamento |
|---|---|---|
| `LISTA_RTD.xlsm` | Sim | Versionado |
| `LISTA_RTD.xlsx` | Sim | Versionado |
| `bridge/analise_robo.csv` | Sim | Versionado |
| `bridge/analise_robo_legs.csv` | Sim | Versionado |
| `bridge/hist_robo.csv` | Sim | Versionado |
| `bridge/analise_raiox.csv` | Sim | Versionado |
| `bridge/configuracoes.csv` | Sim | Versionado |
| `bridge/encerramentos_manuais.csv` | Sim | Versionado |
| `dados/app.db` | Sim | Não versionado |
| `dados/derived.db` | Sim | Não versionado |
| `docs/validacoes/fase-16-limpeza-versionamento-release.md` | Sim | Versionado |
| `ATT/checks/run_all_checks.py` | Sim | Versionado |
| `ATT/checks/run_real_smokes.py` | Não | Não versionado |
| `scripts/run_smoke_quick.py` | Não | Não versionado |
| `scripts/run_smoke_full.py` | Não | Não versionado |
| `scripts/run_derived_pipeline.py` | Sim | Versionado |
| `scripts/validate_derived_db.py` | Sim | Versionado |

Conclusão sobre arquivos críticos:

- Os arquivos operacionais legados de Excel/CSV permanecem presentes e versionados.
- Os bancos SQLite locais existem, mas não são versionados.
- O runner principal de checks existe em `ATT/checks/run_all_checks.py`.
- Os scripts de smoke `run_real_smokes.py`, `run_smoke_quick.py` e `run_smoke_full.py` não existem no estado atual.

---

## 7. Arquivos ignorados relevantes

O status com ignorados identificou caches, dados locais, logs, auditorias locais, arquivos temporários e artefatos de debug corretamente fora do versionamento.

Principais itens ignorados:

~~~text
.pytest_cache/
__pycache__/
_repo_audit/
dados/
logs/
bridge/last_export.txt
debug_bridge_*.py
log_execucao.txt
~~~

Não foram encontrados arquivos não rastreados fora das regras de ignore.

---

## 8. Camadas principais do código

### 8.1 Interface

Principais arquivos:

~~~text
UI/main_window.py
UI/debug_utils.py
UI/components/decisions_grid.py
UI/components/details_panel.py
UI/components/filters_panel.py
UI/components/payoff_chart.py
UI/components/structure_editor_dialog.py
UI/components/structures_list_panel.py
UI/models/ui_data.py
run_ui.py
~~~

### 8.2 API

~~~text
api/pricing_execution_controller.py
api/structures_controller.py
~~~

### 8.3 Domínio

~~~text
domain/calculation_request.py
domain/canonical_validators.py
domain/contracts.py
domain/decision.py
domain/market_snapshot.py
domain/payoff.py
domain/payoff_features.py
domain/structure_metrics.py
src/domain/refs/structure_ref.py
~~~

### 8.4 Serviços

A camada `services/` concentra serviços de cálculo, canonical input, pricing, payoff, eventos de estrutura, legs, status, market snapshot e integração legada.

Principais grupos observados:

~~~text
services/canonical_*.py
services/pricing_*.py
services/structure_*.py
services/robo_*.py
services/legacy_*.py
services/market_snapshot_*.py
services/derived_*.py
~~~

### 8.5 Repositórios

A camada `repositories/` concentra acesso a dados de estruturas, eventos, pricing executions, snapshots, legs, status e RTD.

### 8.6 Banco e infraestrutura

~~~text
db/config.py
db/derived_repo.py
db/import_excel.py
db/init_db.py
db/init_excel_schema.py
db/reader.py
db/schema.py
db/schema_excel.py
db/sqlite.py
db/writer.py
db/migrations/add_structure_id_to_payoff_curve_points.py
infra/bootstrap_structures_schema.py
infra/sqlite_conn.py
~~~

---

## 9. Checks e testes

Checks identificados:

~~~text
ATT/checks/__init__.py
ATT/checks/check_api_routes.py
ATT/checks/check_cleanup_residuals.py
ATT/checks/check_end_to_end.py
ATT/checks/check_legs.py
ATT/checks/check_structures.py
ATT/checks/run_all_checks.py
~~~

Quantidade de checks: 7.

Quantidade de testes em `ATT/tests`: 45.

A suíte cobre domínio, canonical input, pricing, payoff, estruturas, eventos, legs, repositórios, UI e snapshots.

---

## 10. Documentação existente

Documentação versionada relevante:

~~~text
docs/migracoes/fase-14-migracao-dados-legados.md
docs/validacoes/fase-15-validacao-integrada.md
docs/validacoes/fase-16-limpeza-versionamento-release.md
~~~

Este documento adiciona:

~~~text
docs/validacoes/fase-17-mapa-pastas-arquivos.md
~~~

A pasta `docs/` também contém documentação histórica de baseline, auditoria, decisões, SQL surface map, roteiro e fases anteriores.

---

## 11. Referências legadas

Foram identificadas referências aos seguintes termos legados:

~~~text
ANALISE_ROBO
ANALISE_ROBO_LEGS
HIST_ROBO
ENCERRAMENTOS_MANUAIS
~~~

Arquivos de código com referências diretas:

~~~text
db/import_excel.py
db/schema_excel.py
~~~

Conclusão sobre legados:

- As referências legadas ainda existem.
- Elas estão concentradas em importação/schema Excel e documentação histórica.
- Não devem ser removidas nesta fase.
- Devem ser tratadas em fase futura específica, com validação operacional.

---

## 12. Dados locais

O diretório `dados/` existe fisicamente e está ignorado pelo Git.

Arquivos locais identificados incluem:

~~~text
dados/app.db
dados/derived.db
dados/pricing_executions.json
dados/RTD_LINKS.csv
dados/backups/
dados/migrations/004_pricing_executions_new_columns.sql
~~~

Conclusão sobre `dados/`:

- Bancos e backups locais não são versionados.
- Essa situação é compatível com a estratégia atual de versionamento.
- A migração local `dados/migrations/004_pricing_executions_new_columns.sql` deve ser avaliada futuramente para decidir se precisa ser promovida para uma área versionada.

---

## 13. Conclusões da Fase 17

A Fase 17 consolidou o mapa real de pastas e arquivos do projeto após a Fase 16.

Conclusões principais:

1. O repositório está limpo no momento da coleta.
2. A branch `fase-17-mapa-pastas-arquivos` está atualizada com o commit `8e5f1f1` da Fase 16.
3. Existem 200 arquivos versionados.
4. Não existem arquivos não rastreados.
5. Existem 53 diretórios físicos mapeados.
6. Existem 353 arquivos físicos mapeados.
7. Os artefatos locais estão corretamente ignorados pelo Git.
8. Os bancos `dados/app.db` e `dados/derived.db` existem localmente e não são versionados.
9. Os arquivos Excel/CSV críticos seguem presentes e versionados.
10. A estrutura do projeto está organizada em camadas reconhecíveis: UI, API, domínio, serviços, repositórios, banco, scripts, testes e documentação.
11. Ainda existem referências legadas a `ANALISE_ROBO`, `ANALISE_ROBO_LEGS`, `HIST_ROBO` e `ENCERRAMENTOS_MANUAIS`.
12. As referências legadas em código estão concentradas em `db/import_excel.py` e `db/schema_excel.py`.
13. A Fase 17 não removeu nem alterou código operacional.
14. O documento desta fase passa a ser a fotografia oficial da estrutura atual.

---

## 14. Pendências recomendadas para fases futuras

Pendências mapeadas, sem execução nesta fase:

1. Avaliar consolidação entre `domain/` e `src/domain/refs/`.
2. Avaliar destino de `reports/`.
3. Avaliar se scripts locais de debug devem ser removidos, documentados ou promovidos.
4. Avaliar se `dados/migrations/004_pricing_executions_new_columns.sql` deve ser versionado.
5. Avaliar tratamento futuro das referências legadas em `db/import_excel.py` e `db/schema_excel.py`.
6. Avaliar criação formal dos scripts ausentes:
   - `ATT/checks/run_real_smokes.py`
   - `scripts/run_smoke_quick.py`
   - `scripts/run_smoke_full.py`
7. Manter `dados/`, `_repo_audit/`, caches e logs fora do versionamento.
8. Não remover arquivos Excel/CSV de bridge sem fase específica de substituição validada.

---

## 15. Encerramento

A Fase 17 está documentalmente concluída quando este arquivo for versionado.

O projeto possui agora uma referência oficial do estado estrutural do repositório, permitindo que próximas fases sejam conduzidas com menor risco de remoções indevidas, perda de rastreabilidade ou confusão entre código ativo, legado, dados locais e documentação histórica.
