# Classificacao Inicial dos Arquivos UI por Area

Data: 2026-07-03 16:29:47 -0300

Branch: refactor/decisions-dark-panel-large-block

## Objetivo

Este documento classifica, de forma inicial e diagnostica, os arquivos candidatos de UI por area da matriz global de equivalencia.

Documentos relacionados:

- `docs/INVENTARIO_ARQUIVOS_UI.md`
- `docs/MATRIZ_EQUIVALENCIA_UI.md`

## Escopo desta fatia

Esta etapa apenas organiza candidatos por area.

Nao altera comportamento.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa de nenhuma area.

## Metodo

A classificacao foi gerada por varredura estatica de caminhos e conteudo.

Os grupos abaixo sao candidatos iniciais e ainda exigem revisao manual.

## Resumo por area

| Area | Quantidade de candidatos |
|---|---:|
| Decisoes | 52 |
| Terminal VWAP | 46 |
| Payoff curve | 59 |
| UIDataModel | 31 |
| Tema dark / UI moderna | 47 |
| Navegacao / abas / layout | 54 |
| Estados / mensagens / feedback | 67 |
| Banco/dados/pipeline - fora do escopo visual | 67 |
| UI geral / pendente de classificacao fina | 3 |
| Possiveis entrypoints | 16 |

## Possiveis entrypoints

Regra: preservar estes arquivos ate auditoria propria e plano de rollback.

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/conftest.py` | 287 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_payoff_chart.py` | 477 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_editor_dialog.py` | 533 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structure_editor_integration.py` | 568 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structures_archive_wiring.py` | 603 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/__main__.py` | 22 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/app.py` | 146 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `run_ui.py` | 6 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `scripts/check_rota_desenvolvimento.py` | 426 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/audit_rtd_ui_flow.py` | 360 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |


## Decisoes

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/test_payoff_chart.py` | 477 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_grid.py` | 216 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/filters_panel.py` | 159 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `repositories/ui_data_table_candidates.py` | 25 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## Terminal VWAP

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/audit_rtd_ui_flow.py` | 360 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## Payoff curve

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/test_payoff_chart.py` | 477 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/debug_utils.py` | 32 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `create_payoff_summary_table.py` | 29 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_refactor/apply_55_refactor.py` | 105 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `repositories/ui_data_table_candidates.py` | 25 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/audit_rtd_ui_flow.py` | 360 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## UIDataModel

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## Tema dark / UI moderna

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/__init__.py` | 2 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/modern/__main__.py` | 22 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/app.py` | 146 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/theme.py` | 76 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## Navegacao / abas / layout

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/test_payoff_chart.py` | 477 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_editor_dialog.py` | 533 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structure_editor_integration.py` | 568 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structures_archive_wiring.py` | 603 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_grid.py` | 216 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/structure_editor_dialog.py` | 647 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/structures_list_panel.py` | 352 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `create_payoff_summary_table.py` | 29 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/DATABASE_LOCATOR.md` | 22 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_refactor/apply_55_refactor.py` | 105 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `scripts/check_rota_desenvolvimento.py` | 426 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## Estados / mensagens / feedback

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/conftest.py` | 287 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_payoff_chart.py` | 477 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
| `ATT/tests/test_structure_editor_dialog.py` | 533 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structure_editor_integration.py` | 568 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structures_archive_wiring.py` | 603 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_grid.py` | 216 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/filters_panel.py` | 159 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/structure_editor_dialog.py` | 647 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/structures_list_panel.py` | 352 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/theme.py` | 76 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_rtd_nova_ui_bovak900.md` | 99 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | PENDENTE - classificar manualmente contra UI canonica |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_refactor/apply_55_refactor.py` | 105 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `scripts/check_rota_desenvolvimento.py` | 426 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/audit_rtd_ui_flow.py` | 360 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## Banco/dados/pipeline - fora do escopo visual

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `ATT/tests/conftest.py` | 287 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structure_editor_dialog.py` | 533 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structure_editor_integration.py` | 568 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_structures_archive_wiring.py` | 603 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/structure_editor_dialog.py` | 647 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/structures_list_panel.py` | 352 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/main_window.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/__init__.py` | 0 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/dark_window.py` | 202 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/main_window.py` | 777 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `UI/modern/theme.py` | 76 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `create_payoff_summary_table.py` | 29 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/DESENVOLVIMENTO_UI.md` | 198 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/MATRIZ_EQUIVALENCIA_UI.md` | 148 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_rtd_nova_ui_bovak900.md` | 99 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/DATABASE_LOCATOR.md` | 22 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4251 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_refactor/apply_55_refactor.py` | 105 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `repositories/ui_data_table_candidates.py` | 25 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `scripts/check_rota_desenvolvimento.py` | 426 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/audit_rtd_ui_flow.py` | 360 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
| `tools/patch_structure_side_panel.py` | 726 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

## UI geral / pendente de classificacao fina

| Arquivo | Linhas | Observacao inicial |
|---|---:|---|
| `UI/__init__.py` | 0 | PENDENTE - classificar manualmente contra UI canonica |
| `UI/components/__init__.py` | 0 | PENDENTE - classificar manualmente contra UI canonica |
| `run_ui.py` | 6 | PENDENTE - possivel entrypoint, preservar ate auditoria propria |

## Leitura operacional

Esta classificacao inicial deve ser usada para preencher a matriz global por area, aba e fluxo.

### Decisoes

A frente Decisoes permanece como area com equivalencia parcial operacional, conforme auditoria ja registrada.

### Terminal VWAP

Permanece fora do escopo da branch atual ate auditoria propria.

### Payoff curve

Permanece fora do escopo da branch atual ate auditoria propria.

### UIDataModel

Permanece fora do escopo da branch atual ate mapeamento de consumidores e contratos.

### Banco/dados/pipeline

Itens classificados como banco, dados, services, repositories ou pipeline nao devem ser tratados como refactor visual.

## Proxima acao recomendada

Criar uma matriz cruzada por area contendo:

- area;
- arquivos candidatos;
- status atual;
- evidencia;
- risco;
- proxima acao.

Essa matriz cruzada deve orientar a escolha da proxima fatia pequena de desenvolvimento.
