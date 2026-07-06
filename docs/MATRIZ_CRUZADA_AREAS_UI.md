# Matriz Cruzada de Areas da UI

Data: 2026-07-03 16:33:19 -0300

Branch: refactor/decisions-dark-panel-large-block

## Objetivo

Este documento cruza areas da UI com arquivos candidatos, status inicial, risco, evidencia e proxima acao.

Documentos relacionados:

- `docs/MATRIZ_EQUIVALENCIA_UI.md`
- `docs/INVENTARIO_ARQUIVOS_UI.md`
- `docs/CLASSIFICACAO_AREAS_UI.md`

## Escopo desta fatia

Esta etapa e somente diagnostica/documental.

Nao altera comportamento.

Nao altera banco.

Nao altera services, repositories ou regra de negocio.

Nao altera entrypoint principal.

Nao declara equivalencia completa de nenhuma area.

## Regras aplicadas

1. Possiveis entrypoints sao classificados como `PRESERVAR_ENTRYPOINT`.
2. Banco, dados, services, repositories e pipeline sao classificados como `FORA_ESCOPO_VISUAL`.
3. Decisoes permanece como `EQUIVALENCIA_PARCIAL_OPERACIONAL`.
4. Terminal VWAP permanece fora do escopo da branch atual.
5. Payoff curve permanece fora do escopo da branch atual.
6. UIDataModel permanece fora do escopo da branch atual.
7. Demais areas exigem classificacao fina, testes automatizados e/ou execucao assistida com acesso ao sistema antes de equivalencia.

## Resumo por area

| Area | Quantidade |
|---|---:|
| Banco/dados/pipeline - fora do escopo visual | 63 |
| Decisoes | 53 |
| Estados / mensagens / feedback | 68 |
| Navegacao / abas / layout | 55 |
| Payoff curve | 60 |
| Tema dark / UI moderna | 48 |
| Terminal VWAP | 47 |
| UI geral / pendente de classificacao fina | 4 |
| UIDataModel | 32 |


## Resumo por status

| Status | Quantidade |
|---|---:|
| EQUIVALENCIA_PARCIAL_OPERACIONAL | 46 |
| FORA_ESCOPO_BRANCH_ATUAL | 119 |
| FORA_ESCOPO_VISUAL | 51 |
| PENDENTE_CHECKLIST_ESTADOS | 55 |
| PENDENTE_CLASSIFICACAO_FINA | 44 |
| PENDENTE_VALIDACAO_ASSISTIDA | 44 |
| PRESERVAR_ENTRYPOINT | 71 |


## Resumo por risco

| Risco | Quantidade |
|---|---:|
| ALTO | 241 |
| BAIXO | 3 |
| MEDIO | 186 |


## Matriz cruzada

| Area | Arquivo | Linhas | Status inicial | Risco | Evidencia | Proxima acao |
|---|---|---:|---|---|---|---|
| Decisoes | `ATT/tests/test_payoff_chart.py` | 477 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Decisoes | `ATT/tests/test_ui_data_migration.py` | 199 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/components/decisions_dark_panel.py` | 1464 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/components/decisions_grid.py` | 216 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/components/details_panel.py` | 1270 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/components/filters_panel.py` | 159 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/components/payoff_chart.py` | 553 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Decisoes | `UI/models/ui_data.py` | 949 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Decisoes | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Decisoes | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/DESENVOLVIMENTO_UI.md` | 214 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/evolucoes de fases/baseline_v1.md` | 601 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Decisoes | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Decisoes | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `repositories/ui_data_table_candidates.py` | 25 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e modernos; validar por testes automatizados e/ou execucao assistida com acesso ao sistema |
| Decisoes | `tools/patch_structure_side_panel.py` | 726 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `docs/DESENVOLVIMENTO_UI.md` | 214 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `tools/audit_rtd_ui_flow.py` | 360 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Terminal VWAP | `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qualquer refactor |
| Terminal VWAP | `tools/patch_structure_side_panel.py` | 726 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `ATT/tests/test_payoff_chart.py` | 477 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/debug_utils.py` | 32 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `UI/models/ui_data.py` | 949 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `create_payoff_summary_table.py` | 29 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/DESENVOLVIMENTO_UI.md` | 214 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_refactor/apply_55_refactor.py` | 105 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `repositories/ui_data_table_candidates.py` | 25 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `tools/audit_rtd_ui_flow.py` | 360 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Payoff curve | `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria de fluxo, colmap e renderizacao |
| Payoff curve | `tools/patch_structure_side_panel.py` | 726 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UIDataModel | `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `UI/components/decisions_dark_panel.py` | 1464 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UIDataModel | `UI/models/ui_data.py` | 949 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UIDataModel | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UIDataModel | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `docs/DESENVOLVIMENTO_UI.md` | 214 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UIDataModel | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UIDataModel | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| UIDataModel | `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Mapear consumidores e contratos antes de alterar |
| Tema dark / UI moderna | `UI/components/decisions_dark_panel.py` | 1464 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `UI/modern/__init__.py` | 2 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `UI/modern/__main__.py` | 22 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `UI/modern/app.py` | 146 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `UI/modern/theme.py` | 76 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/DESENVOLVIMENTO_UI.md` | 214 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/evolucoes de fases/baseline_v1.md` | 601 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/08_classificacao_acoes_laterais_estruturas_dark_panel.md` | 120 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Tema dark / UI moderna | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | PENDENTE_CLASSIFICACAO_FINA | MEDIO | Varredura estatica de caminho e conteudo | Identificar se o arquivo pertence a UI moderna/dark ou suporte visual |
| Navegacao / abas / layout | `ATT/tests/test_payoff_chart.py` | 477 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `ATT/tests/test_structure_editor_dialog.py` | 533 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `ATT/tests/test_structure_editor_integration.py` | 568 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `ATT/tests/test_structures_archive_wiring.py` | 603 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `ATT/tests/test_ui_data_migration.py` | 199 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/decisions_dark_panel.py` | 1464 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/decisions_grid.py` | 216 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/details_panel.py` | 1270 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/payoff_chart.py` | 553 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/structure_editor_dialog.py` | 647 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/structures_list_panel.py` | 352 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/components/terminal_vwap_payoff_panel.py` | 538 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `UI/models/ui_data.py` | 949 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `create_payoff_summary_table.py` | 29 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/DESENVOLVIMENTO_UI.md` | 214 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/evolucoes de fases/DATABASE_LOCATOR.md` | 22 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/evolucoes de fases/baseline_v1.md` | 601 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_refactor/apply_55_refactor.py` | 105 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | PENDENTE_VALIDACAO_ASSISTIDA | MEDIO | Varredura estatica de caminho e conteudo | Criar validacao automatizada ou roteiro de execucao assistida entre abas antes de declarar equivalencia |
| Navegacao / abas / layout | `scripts/check_rota_desenvolvimento.py` | 426 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Navegacao / abas / layout | `tools/patch_structure_side_panel.py` | 726 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `ATT/tests/conftest.py` | 287 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `ATT/tests/test_payoff_chart.py` | 477 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `ATT/tests/test_structure_editor_dialog.py` | 533 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `ATT/tests/test_structure_editor_integration.py` | 568 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `ATT/tests/test_structures_archive_wiring.py` | 603 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `ATT/tests/test_terminal_vwap_payoff_panel.py` | 110 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `ATT/tests/test_ui_data_migration.py` | 199 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/decisions_dark_panel.py` | 1464 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/decisions_grid.py` | 216 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/details_panel.py` | 1270 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/filters_panel.py` | 159 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/payoff_chart.py` | 553 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/structure_editor_dialog.py` | 647 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/structures_list_panel.py` | 352 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/components/terminal_vwap_payoff_panel.py` | 538 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `UI/models/ui_data.py` | 949 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `UI/modern/theme.py` | 76 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/DESENVOLVIMENTO_UI.md` | 214 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/auditoria_rtd_nova_ui_bovak900.md` | 99 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/evolucoes de fases/baseline_v1.md` | 601 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/02_validacao_manual_modo_dark.md` | 121 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/05_exportacao_png_dark_panel.md` | 49 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/06_validacao_exportacao_png_dark_panel.md` | 45 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/09_validacao_manual_acoes_laterais_estruturas_dark_panel.md` | 68 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_refactor/apply_55_refactor.py` | 105 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `scripts/check_rota_desenvolvimento.py` | 426 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `services/terminal_vwap_payoff_app_service.py` | 370 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `tools/audit_rtd_ui_flow.py` | 360 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Estados / mensagens / feedback | `tools/fix_structure_side_panel_patch.py` | 181 | PENDENTE_CHECKLIST_ESTADOS | MEDIO | Varredura estatica de caminho e conteudo | Validar estados vazios, erro, selecao invalida e mensagens |
| Estados / mensagens / feedback | `tools/patch_structure_side_panel.py` | 726 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `ATT/tests/conftest.py` | 287 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `ATT/tests/test_structure_editor_dialog.py` | 533 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `ATT/tests/test_structure_editor_integration.py` | 568 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `ATT/tests/test_structures_archive_wiring.py` | 603 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py` | 116 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `ATT/tests/test_ui_data_migration.py` | 199 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/components/details_panel.py` | 1270 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/components/payoff_chart.py` | 553 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/components/structure_editor_dialog.py` | 647 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/components/structures_list_panel.py` | 352 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/components/terminal_vwap_payoff_dark_panel.py` | 2114 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/components/terminal_vwap_payoff_panel.py` | 538 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/main_window.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `UI/models/ui_data.py` | 949 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `UI/modern/dark_window.py` | 202 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `UI/modern/main_window.py` | 777 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `create_payoff_summary_table.py` | 29 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/CLASSIFICACAO_AREAS_UI.md` | 582 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/DESENVOLVIMENTO_UI.md` | 214 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/INVENTARIO_ARQUIVOS_UI.md` | 297 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/MATRIZ_EQUIVALENCIA_UI.md` | 162 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/auditoria_rtd_nova_ui_bovak900.md` | 99 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/auditoria_ui_terminal_vwap_payoff.md` | 867 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/evolucoes de fases/DATABASE_LOCATOR.md` | 22 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/evolucoes de fases/MAPA_MODULOS_FUNCOES.md` | 497 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/evolucoes de fases/baseline_v1.md` | 601 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/ui_terminal_vwap_payoff_plano.md` | 965 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `docs/validacoes/fase-17-mapa-pastas-arquivos.md` | 422 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/AUDITORIA_REFACTOR_UI.md` | 4281 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/BLOQUEADORES_ENCERRAMENTO_UI_20260703_152810.md` | 1220 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md` | 49769 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_V2_20260703_153338.md` | 4859 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152430.md` | 2236 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/LOCALIZACAO_DESENVOLVIMENTO_UI_20260703_152455.md` | 2312 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/TRIAGEM_FORMAL_UI_DECISOES_DARK_20260703_153859.md` | 97 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.canonical-before-merge.20260703_143400.1b6c5fb140cff08d.md` | 2183 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-before-merge.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/auditoria/_merge_backups/AUDITORIA_REFACTOR_UI.root-merged.20260703_143400.718f536a1e94ec2b.md` | 1625 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/terminal_vwap_recovery/main_window_good_85dfbcd.py` | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `reports/terminal_vwap_recovery/main_window_terminal_old.py` | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/01_mapa_equivalencia_funcional_ui_moderna.md` | 206 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/03_inventario_exportacao_png.md` | 1737 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/04_inventario_focado_exportacao_png.md` | 131 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/07_acoes_laterais_estruturas_dark_panel.md` | 638 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/10_patch_acoes_laterais_estruturas_dark_panel.md` | 57 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/11_inventario_decisoes_filtros_tabela_dark.md` | 1200 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/12_classificacao_lacunas_decisoes_dark.md` | 224 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/13_historico_decisoes_dark_panel.md` | 100 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/14_decisions_flow_dark_inventory.md` | 589 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/36_decisions_detail_rich_dark.md` | 93 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/37_decisions_copy_detail_dark.md` | 73 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/38_inventario_filtros_avancados_decisoes_dark.md` | 96 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_equivalence/39_classificacao_filtros_avancados_decisoes_dark.md` | 963 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_modern_theme/01_inventario_tokens_visuais_dark.md` | 310 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `reports/ui_visual_audit/01_prints_visual_controls.md` | 409 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `repositories/ui_data_table_candidates.py` | 25 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `scripts/apply_fase9_update_tests_atomic_create.py` | 168 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `scripts/check_rota_desenvolvimento.py` | 426 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `services/terminal_vwap_payoff_app_service.py` | 370 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `services/terminal_vwap_payoff_viewmodel_service.py` | 355 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `tools/audit_rtd_ui_flow.py` | 360 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| Banco/dados/pipeline - fora do escopo visual | `tools/fix_structure_side_panel_patch.py` | 181 | FORA_ESCOPO_VISUAL | ALTO | Sinais de dados/services/repositories/pipeline | Nao misturar com refactor visual; abrir auditoria propria se necessario |
| Banco/dados/pipeline - fora do escopo visual | `tools/patch_structure_side_panel.py` | 726 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |
| UI geral / pendente de classificacao fina | `UI/__init__.py` | 0 | PENDENTE_CLASSIFICACAO_FINA | BAIXO | Varredura estatica de caminho e conteudo | Classificar manualmente contra UI canonica |
| UI geral / pendente de classificacao fina | `UI/components/__init__.py` | 0 | PENDENTE_CLASSIFICACAO_FINA | BAIXO | Varredura estatica de caminho e conteudo | Classificar manualmente contra UI canonica |
| UI geral / pendente de classificacao fina | `UI/models/__init__.py` | 0 | PENDENTE_CLASSIFICACAO_FINA | BAIXO | Varredura estatica de caminho e conteudo | Classificar manualmente contra UI canonica |
| UI geral / pendente de classificacao fina | `run_ui.py` | 6 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qualquer alteracao |


## Leitura operacional

A matriz cruzada mostra que ha sobreposicao entre areas.

Um mesmo arquivo pode aparecer em mais de uma area quando contem sinais de multiplos fluxos.

Essa sobreposicao nao autoriza refactor conjunto.

Cada alteracao futura deve escolher uma fatia pequena e preservar as demais areas.

## Decisao operacional

A branch atual continua adequada para documentar e estabilizar a frente de Decisoes.

As areas abaixo continuam protegidas contra alteracao nesta branch:

- Terminal VWAP;
- Payoff curve;
- UIDataModel;
- banco/dados/pipeline;
- possiveis entrypoints.

## Proxima fatia recomendada

Criar checklist de smoke manual para a area Decisoes, usando os arquivos classificados como candidatos e preservando entrypoints.

Esse checklist deve cobrir:

- abertura da tela;
- estados vazios;
- selecao invalida;
- carregamento com dados;
- mensagens de status;
- comparacao com UI canonica;
- rollback simples.
