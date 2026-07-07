# M2 - Inventario real dos arquivos Terminal VWAP

Data de geracao: 2026-07-07 20:33:19

Branch:

audit/ui-modern-terminal-vwap-m2-inventario-real

HEAD:

f1ff1e5

Status resumido:

LIMPO

## 1. Objetivo

Inventariar arquivos reais relacionados ao Terminal VWAP antes de qualquer correcao UI-only.

## 2. Regras de escopo

- Nao alterar banco.
- Nao alterar schema.
- Nao alterar pipeline.
- Nao alterar regra de negocio.
- Nao alterar services.
- Nao alterar repositories.
- Nao alterar controllers.
- Nao misturar Terminal VWAP com payoff.
- Nao misturar Terminal VWAP com UIDataModel.
- Nao declarar equivalencia global da UI moderna dark.

## 3. Arquivos rastreados com termos Terminal/VWAP

ATT/tests/test_terminal_vwap_payoff_app_service.py
ATT/tests/test_terminal_vwap_payoff_controller.py
ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py
ATT/tests/test_terminal_vwap_payoff_panel.py
ATT/tests/test_terminal_vwap_payoff_panel_helpers.py
ATT/tests/test_terminal_vwap_payoff_panel_rendering.py
ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py
UI/components/terminal_vwap_payoff_dark_panel.py
UI/components/terminal_vwap_payoff_panel.py
controllers/terminal_vwap_payoff_controller.py
docs/auditoria/UI_TERMINAL_VWAP_CLASSIFICACAO_M3.md
docs/auditoria/UI_TERMINAL_VWAP_ESCOPO_M3_CORRIGIDO.md
docs/auditoria/UI_TERMINAL_VWAP_INVENTARIO.md
docs/auditoria/UI_TERMINAL_VWAP_M3_2_TESTES_RENDER_SEM_TK.md
docs/auditoria/UI_TERMINAL_VWAP_M3_FECHAMENTO.md
docs/auditoria/UI_TERMINAL_VWAP_M3_INSPECAO_ARQUIVO_AUTORIZADO.md
docs/auditoria/UI_TERMINAL_VWAP_M3_PATCH_RENDER_SEGURO.md
docs/auditoria_ui_terminal_vwap_payoff.md
docs/ui_terminal_vwap_payoff_plano.md
services/terminal_vwap_payoff_app_service.py
services/terminal_vwap_payoff_viewmodel_service.py

## 4. Arquivos de UI moderna potencialmente relacionados

ATT/tests/test_terminal_vwap_payoff_app_service.py
ATT/tests/test_terminal_vwap_payoff_controller.py
ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py
ATT/tests/test_terminal_vwap_payoff_panel.py
ATT/tests/test_terminal_vwap_payoff_panel_helpers.py
ATT/tests/test_terminal_vwap_payoff_panel_rendering.py
ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
ATT/tests/test_ui_modern_app_launcher.py
ATT/tests/test_ui_modern_cli_env_routing.py
ATT/tests/test_ui_modern_cli_help.py
ATT/tests/test_ui_modern_cli_subprocess.py
ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py
ATT/tests/test_ui_modern_package_entrypoint.py
UI/components/terminal_vwap_payoff_dark_panel.py
UI/components/terminal_vwap_payoff_panel.py
UI/modern/__init__.py
UI/modern/__main__.py
UI/modern/app.py
UI/modern/dark_window.py
UI/modern/main_window.py
UI/modern/theme.py

## 5. Testes automatizados relacionados

ATT/tests/test_terminal_vwap_payoff_app_service.py
ATT/tests/test_terminal_vwap_payoff_controller.py
ATT/tests/test_terminal_vwap_payoff_dark_panel_operational_states.py
ATT/tests/test_terminal_vwap_payoff_panel.py
ATT/tests/test_terminal_vwap_payoff_panel_helpers.py
ATT/tests/test_terminal_vwap_payoff_panel_rendering.py
ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
ATT/tests/test_ui_modern_app_launcher.py
ATT/tests/test_ui_modern_cli_env_routing.py
ATT/tests/test_ui_modern_cli_help.py
ATT/tests/test_ui_modern_cli_subprocess.py
ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py
ATT/tests/test_ui_modern_package_entrypoint.py

## 6. Dependencias proibidas identificadas para nao alteracao nesta frente

controllers/terminal_vwap_payoff_controller.py
infra/bootstrap_rtd_option_quotes_schema.py
infra/bootstrap_structures_schema.py
repositories/rtd_option_quotes_repository.py
scripts/import_rtd_option_quotes_wide_csv.py
scripts/refresh_rtd_symbol_to_option_quotes.py
scripts/refresh_rtd_symbol_to_option_quotes_fallback.py
scripts/run_derived_pipeline.py
services/structure_leg_rtd_enrichment_service.py
services/terminal_vwap_payoff_app_service.py
services/terminal_vwap_payoff_viewmodel_service.py

## 7. Classificacao operacional

### 7.1. Permitido nesta M2

- Documentar inventario.
- Classificar arquivos.
- Identificar testes existentes.
- Identificar lacunas testaveis sem banco.
- Preparar lista priorizada para M3 UI-only.

### 7.2. Proibido nesta M2

- Alterar codigo funcional.
- Alterar banco, schema ou pipeline.
- Alterar services, repositories ou controllers.
- Alterar regra de negocio.
- Misturar Terminal VWAP com payoff.
- Misturar Terminal VWAP com UIDataModel.
- Declarar equivalencia global da UI moderna dark.

## 8. Lista preliminar para M3 UI-only

Pendencias candidatas para M3, condicionadas a nova inspecao antes de alterar:

- montagem visual do Terminal VWAP na UI moderna;
- guards de UI sem selecao;
- estados vazios;
- mensagens de status;
- comportamento com dados ausentes;
- fallback visual de inicializacao;
- testes automatizados de comportamento restritos a UI.

## 9. Criterio de encerramento M2

M2 pode ser encerrada quando houver:

- inventario criado;
- dependencias classificadas;
- arquivos de teste relacionados identificados;
- diff validado;
- commit documental registrado;
- status limpo.

## 10. Decisao

Esta frente permanece classificada como:

DOCUMENTACAO_DE_CONTROLE

AUDITORIA_TERMINAL_VWAP

CRITERIO_GLOBAL_UI

A proxima frente apos o encerramento documental de M2 sera M3, restrita a correcoes UI-only do Terminal VWAP.
