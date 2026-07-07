# Classificacao fina Terminal VWAP para preparacao do M3

Data de consolidacao: 2026-07-07 15:56:25

Branch auditada: audit/ui-modern-terminal-vwap

HEAD atual: 104bf43

## 1. Objetivo

Este documento refina o inventario real da frente Terminal VWAP antes do primeiro pacote grande de correcao UI-only.

Documento anterior:

- `docs/auditoria/UI_TERMINAL_VWAP_INVENTARIO.md`

Motivo desta etapa:

O inventario inicial identificou muitos possiveis riscos proibidos. Esta classificacao separa falso positivo, documentacao, testes, UI candidata e itens que devem bloquear ou reclassificar o M3.

## 2. Estado Git

Branch:

audit/ui-modern-terminal-vwap

HEAD:

104bf43

Status resumido:

LIMPO

Ultimos commits:

104bf43 docs: inventory terminal vwap ui audit scope
f4faca0 docs: track macro ui audit strategy
bd08ff7 test: cover partial ui modern cli env precedence
3341dee test: document ui modern cli help options
a356a9b test: add ui modern cli invalid env fallback smoke
34a6e8d feat: honor ui modern launcher environment options
50fbf49 test: add ui modern cli help smoke
3ef66a5 test: add ui modern cli subprocess smoke
fedd676 test: add ui modern package entrypoint smoke
cf4e39c test: add ui modern launcher routing smoke
fafe28c test: add ui modern terminal vwap wiring smoke
ef7d17d docs: normalize decisions smoke record formatting
1e23db3 docs: record approved decisions ui smoke without backticks
644f73c fix: correct root ui quick launcher

## 3. Resumo quantitativo

Total de arquivos relacionados a VWAP analisados: 40

Aptos para triagem M3 UI-only: 14

Bloqueadores ou reclassificar: 8

Revisao manual necessaria: 0

Nao bloqueadores para M3, incluindo docs e testes: 18

## 4. Regra de decisao

O M3 so pode alterar arquivos classificados como:

- `APTO_PARA_TRIAGEM_M3_UI_ONLY`

Arquivos classificados como:

- `BLOQUEADOR_OU_RECLASSIFICAR`
- `REVISAR_MANUALMENTE`

nao devem ser alterados no M3 sem nova auditoria.

Arquivos classificados como:

- `NAO_BLOQUEADOR_PARA_M3`

podem servir como evidencia, documentacao ou teste, mas nao autorizam mudanca em camadas proibidas.

## 5. Arquivos aptos para triagem M3 UI-only

- `UI/components/terminal_vwap_payoff_panel.py`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `UI/modern/dark_window.py`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `controllers/terminal_vwap_payoff_controller.py`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/classificar_areas_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/criar_registro_execucao_smoke_decisoes_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/criar_smoke_manual_decisoes_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/cruzar_matriz_areas_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/documentar_matriz_equivalencia_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/documentar_pendencias_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/documentar_pendencias_ui_safe.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `scripts/inventariar_arquivos_ui.sh`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `services/terminal_vwap_payoff_viewmodel_service.py`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `tools/fix_structure_side_panel_patch.py`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM
- `tools/patch_structure_side_panel.py`
  - Area: UI_CANDIDATA
  - Classificacao: APTO_PARA_TRIAGEM_M3_UI_ONLY
  - Sinal UI: SIM

## 6. Bloqueadores ou itens que exigem reclassificacao

- `infra/bootstrap_rtd_option_quotes_schema.py`
  - Area: CODIGO_RELACIONADO
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: NAO
  - Imports proibidos ou sensiveis:
    - `sqlite3`
  - SQL ou operacao de banco detectada:
    - linha 41: `CREATE TABLE IF NOT EXISTS rtd_option_quotes (`
    - linha 101: `f'ALTER TABLE {TABLE_NAME} ADD COLUMN "{column_name}" {column_type}'`
    - linha 172: `count = conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]`
- `repositories/rtd_option_quotes_repository.py`
  - Area: CODIGO_RELACIONADO
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: NAO
  - Imports proibidos ou sensiveis:
    - `sqlite3`
- `scripts/import_rtd_option_quotes_wide_csv.py`
  - Area: CODIGO_RELACIONADO
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: NAO
  - Imports proibidos ou sensiveis:
    - `infra.bootstrap_rtd_option_quotes_schema`
    - `sqlite3`
  - SQL ou operacao de banco detectada:
    - linha 271: `"SELECT id FROM rtd_option_quotes WHERE codigo_opcao = ? ORDER BY id DESC LIMIT 1",`
    - linha 293: `f"UPDATE rtd_option_quotes SET {set_clause} WHERE id = ?",`
    - linha 307: `f"INSERT INTO rtd_option_quotes ({columns_sql}) VALUES ({placeholders})",`
- `UI/components/terminal_vwap_payoff_dark_panel.py`
  - Area: UI_CANDIDATA
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `repositories.structures_repository`
    - `sqlite3`
  - SQL ou operacao de banco detectada:
    - linha 474: `rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()`
    - linha 529: `sql = f"SELECT {', '.join(select_parts)} FROM {_q(table)} ORDER BY {_q(id_col)}"`
    - linha 1411: `CREATE TABLE IF NOT EXISTS structure_decisions (`
    - linha 1440: `INSERT INTO structure_decisions (`
- `UI/main_window.py`
  - Area: UI_CANDIDATA
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `controllers.terminal_vwap_payoff_controller`
    - `repositories.structures_repository`
    - `services.terminal_vwap_payoff_app_service`
- `UI/modern/main_window.py`
  - Area: UI_CANDIDATA
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `controllers.terminal_vwap_payoff_controller`
    - `repositories.structures_repository`
    - `services.terminal_vwap_payoff_app_service`
- `services/terminal_vwap_payoff_app_service.py`
  - Area: UI_CANDIDATA
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `services.terminal_vwap_payoff_viewmodel_service`
- `tools/audit_rtd_ui_flow.py`
  - Area: UI_CANDIDATA
  - Classificacao: BLOQUEADOR_OU_RECLASSIFICAR
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `repositories.rtd_option_quotes_repository`
    - `services.structure_leg_rtd_enrichment_service`
    - `sqlite3`
  - SQL ou operacao de banco detectada:
    - linha 69: `"select name from sqlite_master where type='table' order by name"`
    - linha 108: `total = conn.execute("select count(*) as n from rtd_option_quotes").fetchone()["n"]`

## 7. Itens que exigem revisao manual

Nenhum item localizado.

## 8. Itens nao bloqueadores para M3

- `docs/CLASSIFICACAO_AREAS_UI.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/DESENVOLVIMENTO_UI.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/INVENTARIO_ARQUIVOS_UI.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/MATRIZ_CRUZADA_AREAS_UI.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/MATRIZ_EQUIVALENCIA_UI.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/auditoria/UI_TERMINAL_VWAP_INVENTARIO.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/auditoria_ui_terminal_vwap_payoff.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `docs/ui_terminal_vwap_payoff_plano.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `reports/auditoria/UI_FRENTES_ENCERRADAS.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md`
  - Area: DOCUMENTACAO
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `ATT/tests/test_terminal_vwap_payoff_app_service.py`
  - Area: TESTE
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `services.terminal_vwap_payoff_app_service`
- `ATT/tests/test_terminal_vwap_payoff_controller.py`
  - Area: TESTE
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `controllers.terminal_vwap_payoff_controller`
- `ATT/tests/test_terminal_vwap_payoff_panel.py`
  - Area: TESTE
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
- `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py`
  - Area: TESTE
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM
  - Imports proibidos ou sensiveis:
    - `services.terminal_vwap_payoff_viewmodel_service`
- `ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py`
  - Area: TESTE
  - Classificacao: NAO_BLOQUEADOR_PARA_M3
  - Sinal UI: SIM

## 9. Decisao operacional

A proxima etapa M3 deve ser limitada aos arquivos aptos para triagem UI-only.

Escopo permitido no M3:

- montagem visual;
- wiring da janela moderna dark com Terminal VWAP;
- estado vazio;
- mensagem de status;
- fallback visual;
- guard de UI;
- teste automatizado de comportamento visual.

Escopo proibido no M3:

- banco;
- schema;
- pipeline;
- query;
- service;
- repository;
- controller;
- regra de negocio;
- payoff;
- UIDataModel.

Classificacao:

AUDITORIA_TERMINAL_VWAP

TRIAGEM_RISCO_M3

PREPARACAO_UI_ONLY
