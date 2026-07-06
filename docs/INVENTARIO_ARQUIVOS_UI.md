# Inventario Inicial de Arquivos Reais da UI

Data: 2026-07-03 16:11:05 -0300

Branch: refactor/decisions-dark-panel-large-block

## Objetivo

Este documento registra um inventario inicial dos arquivos do repositorio que possuem sinais de participacao na UI.

A finalidade e apoiar o preenchimento da matriz global de equivalencia da UI sem alterar comportamento, banco, services, repositories ou entrypoint principal.

Documento relacionado:

- `docs/MATRIZ_EQUIVALENCIA_UI.md`

## Escopo desta fatia

Esta etapa e somente diagnostica/documental.

Nao declara equivalencia completa de nenhuma area.

Nao autoriza substituicao da UI canonica.

Nao altera caminho principal de execucao.

## Metodo de identificacao

O inventario foi gerado por varredura estatica de arquivos com extensoes de codigo, layout, estilo e documentacao.

Foram considerados sinais como:

- nomes de caminho relacionados a UI;
- uso de bibliotecas de interface;
- termos como panel, tab, widget, view, screen e layout;
- referencias a decisoes, payoff, VWAP e tema dark;
- possiveis entrypoints.

## Resumo quantitativo

| Classificacao | Quantidade |
|---|---:|
| Provaveis arquivos de UI | 120 |
| Possiveis arquivos relacionados a UI | 42 |
| Possiveis entrypoints | 38 |
| Total com algum sinal | 162 |

## Possiveis entrypoints identificados

| Arquivo | Linhas | Sinais | Observacao inicial |
|---|---:|---|---|
| `UI/modern/dark_window.py` | 202 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/main_window.py` | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/main_window.py` | 777 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `tools/patch_structure_side_panel.py` | 726 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, decisoes, payoff, vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `tools/audit_rtd_ui_flow.py` | 360 | caminho/nome sugere UI; conteudo: payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_editor_dialog.py` | 533 | caminho/nome sugere UI; conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/validate_derived_db.py` | 93 | conteudo: ui_terms, decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/conftest.py` | 287 | conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_payoff_chart.py` | 477 | conteudo: tkinter, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_editor_integration.py` | 568 | conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structures_archive_wiring.py` | 603 | conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/__main__.py` | 22 | caminho/nome sugere UI; conteudo: dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/app.py` | 146 | caminho/nome sugere UI; conteudo: dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/migrations/add_structure_id_to_payoff_curve_points.py` | 130 | conteudo: decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `run_ui.py` | 6 | caminho/nome sugere UI; conteudo: tkinter; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/check_rota_desenvolvimento.py` | 426 | conteudo: textual/rich, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/import_rtd_option_quotes_wide_csv.py` | 343 | conteudo: textual/rich, vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/purge_derived_snapshots.py` | 176 | conteudo: decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/repair_derived_db_consistency.py` | 311 | conteudo: decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_cleanup_residuals.py` | 246 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_end_to_end.py` | 113 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_structures.py` | 104 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `infra/bootstrap_rtd_option_quotes_schema.py` | 185 | conteudo: vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/run_derived_pipeline.py` | 75 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_api_routes.py` | 72 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_legs.py` | 93 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/run_all_checks.py` | 46 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_canonical_input_service.py` | 319 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_pricing_payload_adapter.py` | 122 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_market_input_assembler.py` | 97 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/import_excel.py` | 113 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/init_db.py` | 16 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/init_excel_schema.py` | 15 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/import_legacy_structure_legs.py` | 145 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/refresh_rtd_symbol_to_option_quotes.py` | 330 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py` | 164 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |


## Provaveis arquivos de UI

| Arquivo | Linhas | Sinais | Observacao inicial |
|---|---:|---|---|
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, matplotlib_ui, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, matplotlib_ui, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `UI/modern/dark_window.py` | 202 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4217 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `UI/main_window.py` | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/main_window.py` | 777 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | caminho/nome sugere UI; conteudo: matplotlib_ui, textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `tools/patch_structure_side_panel.py` | 726 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, decisoes, payoff, vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/components/decisions_dark_panel.py` | 1464 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, textual/rich, ui_terms, decisoes, dark | PENDENTE |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | caminho/nome sugere UI; conteudo: tkinter, matplotlib_ui, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `tools/fix_structure_side_panel_patch.py` | 181 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, payoff, vwap, dark | PENDENTE |
| `docs/DESENVOLVIMENTO_UI.md` | 182 | caminho/nome sugere UI; conteudo: ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 134 | caminho/nome sugere UI; conteudo: ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | caminho/nome sugere UI; conteudo: ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | caminho/nome sugere UI; conteudo: ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | caminho/nome sugere UI; conteudo: ui_terms, decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, payoff, dark | PENDENTE |
| `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | caminho/nome sugere UI; conteudo: textual/rich, ui_terms, decisoes, vwap, dark | PENDENTE |
| `tools/audit_rtd_ui_flow.py` | 360 | caminho/nome sugere UI; conteudo: payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, payoff, vwap | PENDENTE |
| `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | caminho/nome sugere UI; conteudo: decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | caminho/nome sugere UI; conteudo: decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | caminho/nome sugere UI; conteudo: decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | caminho/nome sugere UI; conteudo: decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | caminho/nome sugere UI; conteudo: decisoes, payoff, vwap, dark | PENDENTE |
| `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | caminho/nome sugere UI; conteudo: textual/rich, decisoes, payoff, dark | PENDENTE |
| `ATT/tests/test_structure_editor_dialog.py` | 533 | caminho/nome sugere UI; conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/validate_derived_db.py` | 93 | conteudo: ui_terms, decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/components/details_panel.py` | 1270 | caminho/nome sugere UI; conteudo: tkinter, decisoes, payoff | PENDENTE |
| `UI/components/payoff_chart.py` | 553 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, payoff | PENDENTE |
| `UI/models/ui_data.py` | 949 | caminho/nome sugere UI; conteudo: ui_terms, decisoes, payoff | PENDENTE |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | conteudo: tkinter, decisoes, payoff, dark | PENDENTE |
| `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | caminho/nome sugere UI; conteudo: decisoes, payoff, dark | PENDENTE |
| `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | caminho/nome sugere UI; conteudo: customtkinter, ui_terms, dark | PENDENTE |
| `ATT/tests/conftest.py` | 287 | conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_payoff_chart.py` | 477 | conteudo: tkinter, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_editor_integration.py` | 568 | conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structures_archive_wiring.py` | 603 | conteudo: tkinter, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/__main__.py` | 22 | caminho/nome sugere UI; conteudo: dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/app.py` | 146 | caminho/nome sugere UI; conteudo: dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/migrations/add_structure_id_to_payoff_curve_points.py` | 130 | conteudo: decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `run_ui.py` | 6 | caminho/nome sugere UI; conteudo: tkinter; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/check_rota_desenvolvimento.py` | 426 | conteudo: textual/rich, ui_terms; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/import_rtd_option_quotes_wide_csv.py` | 343 | conteudo: textual/rich, vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/purge_derived_snapshots.py` | 176 | conteudo: decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/repair_derived_db_consistency.py` | 311 | conteudo: decisoes, payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | caminho/nome sugere UI; conteudo: payoff, vwap | PENDENTE |
| `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | caminho/nome sugere UI; conteudo: payoff, vwap | PENDENTE |
| `ATT/tests/test_ui_data_migration.py` | 199 | caminho/nome sugere UI; conteudo: decisoes, payoff | PENDENTE |
| `UI/components/decisions_grid.py` | 216 | caminho/nome sugere UI; conteudo: tkinter, decisoes | PENDENTE |
| `UI/components/filters_panel.py` | 159 | caminho/nome sugere UI; conteudo: tkinter, decisoes | PENDENTE |
| `UI/components/structure_editor_dialog.py` | 647 | caminho/nome sugere UI; conteudo: tkinter, ui_terms | PENDENTE |
| `UI/components/structures_list_panel.py` | 352 | caminho/nome sugere UI; conteudo: tkinter, ui_terms | PENDENTE |
| `UI/modern/theme.py` | 76 | caminho/nome sugere UI; conteudo: customtkinter, dark | PENDENTE |
| `db/writer.py` | 153 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/ROTA_REVISAO_FUNCIONAL_POS_USO_REAL.md` | 440 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/evolucoes de fases/FASE_3_CLASSIFICACAO_FONTES_DADOS.md` | 389 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/evolucoes de fases/FASE_6_CAMADA_CANONICA_LEITURA.md` | 261 | conteudo: textual/rich, decisoes, payoff | PENDENTE |
| `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | conteudo: ui_terms, decisoes, payoff | PENDENTE |
| `docs/evolucoes de fases/baseline_v1a.md` | 128 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/evolucoes de fases/baseline_v2.md` | 44 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/evolucoes de fases/executed_v1.md` | 272 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/evolucoes de fases/fase_8_banco_fonte_verdade_auditoria.md` | 479 | conteudo: decisoes, payoff, dark | PENDENTE |
| `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | caminho/nome sugere UI; conteudo: decisoes, payoff | PENDENTE |
| `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | caminho/nome sugere UI; conteudo: payoff, dark | PENDENTE |
| `repositories/ui_data_table_candidates.py` | 25 | caminho/nome sugere UI; conteudo: decisoes, payoff | PENDENTE |
| `services/terminal_vwap_payoff_app_service.py` | 370 | conteudo: tkinter, payoff, vwap | PENDENTE |
| `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | caminho/nome sugere UI; conteudo: payoff, vwap | PENDENTE |
| `ATT/checks/check_cleanup_residuals.py` | 246 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_end_to_end.py` | 113 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_structures.py` | 104 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `infra/bootstrap_rtd_option_quotes_schema.py` | 185 | conteudo: vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/run_derived_pipeline.py` | 75 | conteudo: payoff; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_decision.py` | 28 | conteudo: decisoes, payoff | PENDENTE |
| `ATT/tests/test_terminal_vwap_payoff_app_service.py` | 187 | conteudo: payoff, vwap | PENDENTE |
| `ATT/tests/test_terminal_vwap_payoff_controller.py` | 119 | conteudo: payoff, vwap | PENDENTE |
| `UI/debug_utils.py` | 32 | caminho/nome sugere UI; conteudo: payoff | PENDENTE |
| `controllers/terminal_vwap_payoff_controller.py` | 154 | conteudo: payoff, vwap | PENDENTE |
| `create_payoff_summary_table.py` | 29 | caminho/nome sugere UI; conteudo: payoff | PENDENTE |
| `db/derived_repo.py` | 927 | conteudo: decisoes, payoff | PENDENTE |
| `db/reader.py` | 158 | conteudo: decisoes, payoff | PENDENTE |
| `db/schema.py` | 118 | conteudo: decisoes, payoff | PENDENTE |
| `docs/EVOLUCAO_REVISAO_FUNCIONAL_POS_USO_REAL.md` | 106 | conteudo: payoff, dark | PENDENTE |
| `docs/checkpoints/evidencias/fase-1-fechamento-mapa-runtime-codigo-atual.md` | 395 | conteudo: decisoes, payoff | PENDENTE |
| `docs/checkpoints/evidencias/fase-9-encerramento-enriquecimento-legs-rtd-e-position-side.md` | 300 | conteudo: decisoes, dark | PENDENTE |
| `docs/decisions/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` | 182 | conteudo: decisoes, dark | PENDENTE |
| `docs/evolucoes de fases/10.1_normalizacao_comprado_vendido.md` | 194 | conteudo: decisoes, payoff | PENDENTE |
| `docs/evolucoes de fases/3B_CLOSURE_REPORT.md` | 158 | conteudo: decisoes, payoff | PENDENTE |
| `docs/evolucoes de fases/AUDITORIA_ROTA_MESTRE_3.md` | 578 | conteudo: decisoes, dark | PENDENTE |
| `docs/evolucoes de fases/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md` | 544 | conteudo: payoff, dark | PENDENTE |
| `docs/evolucoes de fases/SQL_SURFACE_MAP_v2.md` | 23 | conteudo: decisoes, payoff | PENDENTE |
| `docs/evolucoes de fases/roteiro_v2.md` | 27 | conteudo: decisoes, payoff | PENDENTE |
| `docs/validacoes/fase-15-validacao-integrada.md` | 130 | conteudo: decisoes, payoff | PENDENTE |
| `domain/calculation_request.py` | 233 | conteudo: decisoes, payoff | PENDENTE |
| `domain/decision.py` | 214 | conteudo: decisoes, payoff | PENDENTE |
| `infra/bootstrap_structures_schema.py` | 347 | conteudo: payoff, dark | PENDENTE |
| `reports/ui_refactor/apply_55_refactor.py` | 105 | caminho/nome sugere UI; conteudo: payoff | PENDENTE |
| `repositories/system_snapshots_repository.py` | 294 | conteudo: payoff, dark | PENDENTE |
| `services/calculation_orchestrator.py` | 519 | conteudo: decisoes, payoff | PENDENTE |
| `services/derived_payoff_persistence.py` | 222 | conteudo: decisoes, payoff | PENDENTE |
| `services/derived_service.py` | 530 | conteudo: decisoes, payoff | PENDENTE |
| `services/payoff_persistence_port.py` | 19 | conteudo: decisoes, payoff | PENDENTE |
| `services/pricing_execution_persistence_service.py` | 165 | conteudo: decisoes, payoff | PENDENTE |
| `services/structure_analysis_service.py` | 122 | conteudo: decisoes, payoff | PENDENTE |


## Possiveis arquivos relacionados a UI

| Arquivo | Linhas | Sinais | Observacao inicial |
|---|---:|---|---|
| `ATT/checks/check_api_routes.py` | 72 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/check_legs.py` | 93 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/checks/run_all_checks.py` | 46 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_canonical_input_service.py` | 319 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_pricing_payload_adapter.py` | 122 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_market_input_assembler.py` | 97 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/import_excel.py` | 113 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/init_db.py` | 16 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `db/init_excel_schema.py` | 15 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/import_legacy_structure_legs.py` | 145 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/refresh_rtd_symbol_to_option_quotes.py` | 330 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/refresh_rtd_symbol_to_option_quotes_fallback.py` | 164 | possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_derived_service.py` | 156 | conteudo: payoff | PENDENTE |
| `ATT/tests/test_orchestrator_run_methods.py` | 264 | conteudo: payoff | PENDENTE |
| `ATT/tests/test_payoff_canonical.py` | 44 | conteudo: payoff | PENDENTE |
| `ATT/tests/test_pricing_execution_persistence_service.py` | 374 | conteudo: payoff | PENDENTE |
| `ATT/tests/test_structure_analysis_service.py` | 638 | conteudo: payoff | PENDENTE |
| `ATT/tests/test_system_snapshots_repository.py` | 275 | conteudo: payoff | PENDENTE |
| `ATT/tests/test_system_snapshots_schema.py` | 124 | conteudo: payoff | PENDENTE |
| `UI/__init__.py` | 0 | caminho/nome sugere UI | PENDENTE |
| `UI/components/__init__.py` | 0 | caminho/nome sugere UI | PENDENTE |
| `UI/models/__init__.py` | 0 | caminho/nome sugere UI | PENDENTE |
| `UI/modern/__init__.py` | 2 | caminho/nome sugere UI | PENDENTE |
| `docs/auditoria_rtd_nova_ui_bovak900.md` | 99 | caminho/nome sugere UI | PENDENTE |
| `docs/checkpoints/evidencias/fase-12-fechamento-rota-mestre-3.md` | 92 | conteudo: decisoes | PENDENTE |
| `docs/checkpoints/fase-6-11-retomada-funcional-pos-restauracao-documental.md` | 188 | conteudo: decisoes | PENDENTE |
| `docs/checkpoints/fase-6-7-consolidacao-diagnostico-rtd-canonical.md` | 166 | conteudo: decisoes | PENDENTE |
| `docs/decisions/structure_ref_created_at.md` | 57 | conteudo: decisoes | PENDENTE |
| `docs/evolucoes de fases/AUDITORIA_FASE_11_SNAPSHOTS_HISTORICO.md` | 14 | conteudo: dark | PENDENTE |
| `docs/evolucoes de fases/DATABASE_LOCATOR.md` | 22 | caminho/nome sugere UI | PENDENTE |
| `docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md` | 21 | conteudo: payoff | PENDENTE |
| `docs/evolucoes de fases/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md` | 412 | conteudo: dark | PENDENTE |
| `docs/evolucoes de fases/FASE_5_ISOLAMENTO_BRIDGE_EXCEL_ADAPTADOR_LEGADO.md` | 395 | conteudo: decisoes | PENDENTE |
| `docs/evolucoes de fases/auditoria_fase_9_cadastro_estruturas.md` | 65 | conteudo: dark | PENDENTE |
| `domain/payoff.py` | 176 | conteudo: payoff | PENDENTE |
| `domain/payoff_features.py` | 242 | conteudo: payoff | PENDENTE |
| `repositories/rtd_option_quotes_repository.py` | 128 | conteudo: vwap | PENDENTE |
| `repositories/structure_events_repository.py` | 545 | conteudo: dark | PENDENTE |
| `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | conteudo: tkinter | PENDENTE |
| `services/canonical_input_service.py` | 426 | conteudo: payoff | PENDENTE |
| `services/canonical_pricing_facade.py` | 427 | conteudo: payoff | PENDENTE |
| `src/domain/refs/structure_ref.py` | 165 | conteudo: decisoes | PENDENTE |


## Leitura operacional inicial

Os arquivos listados acima devem ser tratados como candidatos.

Cada candidato ainda precisa ser classificado na matriz global como:

- CANONICA;
- EQUIVALENTE;
- EQUIVALENCIA_PARCIAL_OPERACIONAL;
- EXPERIMENTAL;
- PENDENTE;
- FORA_ESCOPO.

## Regras de seguranca

1. Possiveis entrypoints nao devem ser alterados nesta frente.
2. Arquivos de banco/dados/pipeline nao devem ser misturados com refactor visual.
3. Areas Terminal VWAP, payoff curve e UIDataModel exigem auditoria propria.
4. A UI canonica permanece preservada ate decisao explicita.
5. Este inventario nao substitui testes automatizados, revisao tecnica ou execucao assistida com acesso ao sistema.

## Proxima acao recomendada

Cruzar este inventario com a matriz global para abrir uma tabela por area/aba/fluxo.

A proxima fatia recomendada e documentar:

- arquivos candidatos da UI canonica;
- arquivos candidatos da UI moderna/dark;
- lacunas por aba;
- areas que exigem auditoria propria.
