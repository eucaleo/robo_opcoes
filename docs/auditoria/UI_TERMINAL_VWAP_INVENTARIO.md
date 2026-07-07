# Inventario real da frente Terminal VWAP

Data de consolidacao: 2026-07-07 15:52:06

Branch auditada: audit/ui-modern-terminal-vwap

HEAD atual: f4faca0

## 1. Objetivo

Este documento registra a auditoria real dos arquivos relacionados a Terminal VWAP.

A finalidade e preparar o primeiro pacote grande de correcao UI-only, mantendo a nova estrategia macro aprovada nos documentos:

- `docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md`
- `docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md`

Este inventario nao autoriza alteracao de banco, schema, pipeline, services, repositories, controllers ou regra de negocio.

## 2. Estado Git no momento da auditoria

Branch:

audit/ui-modern-terminal-vwap

HEAD:

f4faca0

Status resumido:

LIMPO

Ultimos commits:

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
d3846a0 fix: add root ui launcher

## 3. Arquivos candidatos relacionados a VWAP

- `ATT/tests/test_terminal_vwap_payoff_app_service.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, teste automatizado, possivel dependencia/camada proibida
  - Evidencias:
    - linha 3: `from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService`
    - linha 30: `"vwap": 100.0,`
    - linha 72: `"name": "ui-terminal-vwap-payoff",`
    - linha 84: `def build_terminal_vwap_payoff_viewmodel(`
    - linha 92: `"vwap": market_snapshot["vwap"],`
    - linha 124: `service = TerminalVWAPPayoffAppService(`
    - linha 133: `assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"`
    - linha 136: `assert result["market"]["vwap"] == 100.0`
- `ATT/tests/test_terminal_vwap_payoff_controller.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, teste automatizado, possivel dependencia/camada proibida
  - Evidencias:
    - linha 3: `from controllers.terminal_vwap_payoff_controller import (`
    - linha 4: `TerminalVWAPPayoffController,`
    - linha 8: `class FakeTerminalVWAPPayoffAppService:`
    - linha 32: `"name": "ui-terminal-vwap-payoff",`
    - linha 45: `app_service = FakeTerminalVWAPPayoffAppService()`
    - linha 46: `controller = TerminalVWAPPayoffController(app_service)`
    - linha 51: `assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"`
    - linha 57: `app_service = FakeTerminalVWAPPayoffAppService()`
- `ATT/tests/test_terminal_vwap_payoff_panel.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, teste automatizado
  - Evidencias:
    - linha 1: `from UI.components.terminal_vwap_payoff_panel import (`
    - linha 21: `"vwap": 10,`
    - linha 22: `"price_vs_vwap_percent": 10,`
    - linha 69: `assert summary["vwap"] == "10,00"`
    - linha 70: `assert summary["price_vs_vwap_percent"] == "10,00%"`
- `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, teste automatizado, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `from services.terminal_vwap_payoff_viewmodel_service import (`
    - linha 2: `TerminalVWAPPayoffViewModelService,`
    - linha 6: `def test_build_terminal_vwap_payoff_viewmodel_with_vwap_and_payoff_points():`
    - linha 7: `service = TerminalVWAPPayoffViewModelService()`
    - linha 30: `"vwap": 10.0,`
    - linha 42: `assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"`
    - linha 54: `assert result["market"]["vwap"] == 10.0`
    - linha 55: `assert result["market"]["status_vwap"] == "available"`
- `ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, teste automatizado, possivel dependencia/camada proibida
  - Evidencias:
    - linha 92: `terminal_module = types.ModuleType("UI.components.terminal_vwap_payoff_dark_panel")`
    - linha 93: `terminal_module.TerminalVWAPPayoffDarkPanel = PlaceholderWidget`
    - linha 108: `"UI.components.terminal_vwap_payoff_dark_panel",`
    - linha 136: `def test_modern_dark_window_wires_terminal_vwap_and_decisions(monkeypatch, tmp_path):`
    - linha 147: `class FakeTerminalVWAPPayoffDarkPanel:`
    - linha 160: `FakeTerminalVWAPPayoffDarkPanel.instances.append(self)`
    - linha 197: `monkeypatch.setattr(module, "TerminalVWAPPayoffDarkPanel", FakeTerminalVWAPPayoffDarkPanel)`
    - linha 203: `terminal_panel = FakeTerminalVWAPPayoffDarkPanel.instances[0]`
- `UI/components/terminal_vwap_payoff_dark_panel.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `# UI/components/terminal_vwap_payoff_dark_panel.py`
    - linha 4: `Painel operacional dark para análise VWAP e Payoff.`
    - linha 10: `- blocos grandes para VWAP e Payoff;`
    - linha 129: `class TerminalVWAPPayoffDarkPanel(ctk.CTkFrame):`
    - linha 145: `self.canvas_vwap: Optional[FigureCanvasTkAgg] = None`
    - linha 313: `text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff",`
    - linha 328: `self._create_kpi("vwap", "VWAP", "N/A", 1)`
    - linha 329: `self._create_kpi("diff", "Preço vs VWAP", "N/A", 2)`
- `UI/components/terminal_vwap_payoff_panel.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `# UI/components/terminal_vwap_payoff_panel.py`
    - linha 3: `Painel nativo Tkinter do Terminal VWAP Payoff.`
    - linha 10: `-> TerminalVWAPPayoffPanel`
    - linha 11: `-> TerminalVWAPPayoffController`
    - linha 12: `-> TerminalVWAPPayoffAppService`
    - linha 14: `-> TerminalVWAPPayoffViewModelService`
    - linha 134: `"vwap": _format_number_br(market.get("vwap"), 2),`
    - linha 135: `"price_vs_vwap_percent": _format_percent_br(`
- `UI/main_window.py`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 14: `from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel`
    - linha 115: `self._setup_terminal_vwap_payoff_tab(right_notebook)`
    - linha 698: `def _setup_terminal_vwap_payoff_tab(self, notebook: ttk.Notebook):`
    - linha 699: `"""Adiciona o Terminal VWAP Payoff como aba nativa da UI principal."""`
    - linha 702: `notebook.add(terminal_frame, text="Terminal VWAP Payoff")`
    - linha 706: `from services.terminal_vwap_payoff_app_service import (`
    - linha 707: `TerminalVWAPPayoffAppService,`
    - linha 709: `from controllers.terminal_vwap_payoff_controller import (`
- `UI/modern/dark_window.py`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 6: `Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde`
    - linha 20: `from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel`
    - linha 39: `self.root.title("Terminal de Análise Avançada - VWAP & Opções")`
    - linha 76: `terminal_tab = self.tabs.add("Terminal VWAP")`
    - linha 79: `self.panel = TerminalVWAPPayoffDarkPanel(`
    - linha 122: `Fornece as estruturas carregadas no Terminal VWAP para a aba Decisões.`
    - linha 138: `Carrega no Terminal VWAP a estrutura associada a uma decisão selecionada.`
    - linha 158: `self.set_status(f"Estrutura {structure_id} não encontrada no Terminal VWAP")`
- `UI/modern/main_window.py`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 269: `notebook.add(tab, text="Terminal VWAP Payoff")`
    - linha 272: `from controllers.terminal_vwap_payoff_controller import (`
    - linha 273: `TerminalVWAPPayoffController,`
    - linha 276: `from services.terminal_vwap_payoff_app_service import (`
    - linha 277: `TerminalVWAPPayoffAppService,`
    - linha 279: `from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel`
    - linha 282: `app_service = TerminalVWAPPayoffAppService(`
    - linha 285: `controller = TerminalVWAPPayoffController(app_service)`
- `controllers/terminal_vwap_payoff_controller.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `"""Controller do Terminal VWAP Payoff.`
    - linha 17: `class TerminalVWAPPayoffController:`
    - linha 18: `"""Controller fino para seleção e carga do Terminal VWAP Payoff."""`
- `docs/CLASSIFICACAO_AREAS_UI.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 41: `| Terminal VWAP | 46 |`
    - linha 67: `| 'reports/terminal_vwap_recovery/main_window_good_85dfbcd.py' | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
    - linha 68: `| 'reports/terminal_vwap_recovery/main_window_terminal_old.py' | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
    - linha 86: `| 'UI/components/terminal_vwap_payoff_dark_panel.py' | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
    - linha 94: `| 'docs/auditoria_ui_terminal_vwap_payoff.md' | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
    - linha 97: `| 'docs/ui_terminal_vwap_payoff_plano.md' | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
    - linha 109: `| 'reports/terminal_vwap_recovery/main_window_good_85dfbcd.py' | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
    - linha 110: `| 'reports/terminal_vwap_recovery/main_window_terminal_old.py' | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |`
- `docs/DESENVOLVIMENTO_UI.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 72: `#### 3. Terminal VWAP, payoff e UIDataModel`
    - linha 80: `- Terminal VWAP;`
    - linha 145: `abrir auditoria propria para Terminal VWAP/payoff/UIDataModel`
- `docs/INVENTARIO_ARQUIVOS_UI.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 36: `- referencias a decisoes, payoff, VWAP e tema dark;`
    - linha 52: `| 'UI/modern/dark_window.py' | 202 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel ent`
    - linha 53: `| 'UI/main_window.py' | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate`
    - linha 54: `| 'UI/modern/main_window.py' | 777 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preser`
    - linha 55: `| 'reports/terminal_vwap_recovery/main_window_terminal_old.py' | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PEND`
    - linha 56: `| 'reports/terminal_vwap_recovery/main_window_good_85dfbcd.py' | 1178 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, dark; possivel entrypoint | PENDENTE `
    - linha 57: `| 'tools/patch_structure_side_panel.py' | 726 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, decisoes, payoff, vwap; possivel entrypoint | PENDENTE - possivel entrypoi`
    - linha 58: `| 'tools/audit_rtd_ui_flow.py' | 360 | caminho/nome sugere UI; conteudo: payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |`
- `docs/MATRIZ_CRUZADA_AREAS_UI.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 36: `4. Terminal VWAP permanece fora do escopo da branch atual.`
    - linha 51: `| Terminal VWAP | 47 |`
    - linha 89: `| Decisoes | 'UI/components/terminal_vwap_payoff_dark_panel.py' | 2114 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canon`
    - linha 98: `| Decisoes | 'docs/auditoria_ui_terminal_vwap_payoff.md' | 867 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e m`
    - linha 101: `| Decisoes | 'docs/ui_terminal_vwap_payoff_plano.md' | 965 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e moder`
    - linha 113: `| Decisoes | 'reports/terminal_vwap_recovery/main_window_good_85dfbcd.py' | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qua`
    - linha 114: `| Decisoes | 'reports/terminal_vwap_recovery/main_window_terminal_old.py' | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qual`
    - linha 135: `| Terminal VWAP | 'ATT/tests/test_terminal_vwap_payoff_panel.py' | 110 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes `
- `docs/MATRIZ_EQUIVALENCIA_UI.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 53: `| Terminal VWAP | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Abrir auditoria propria |`
    - linha 124: `- auditar Terminal VWAP separadamente;`
- `docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 295: `- Terminal VWAP permanece fora do escopo desta branch;`
    - linha 360: `- Terminal VWAP fora do carregamento a partir de Decisoes;`
- `docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `# Auditoria macro de evolucao UI moderna e Terminal VWAP`
    - linha 5: `Branch auditada: audit/ui-modern-terminal-vwap`
    - linha 25: `- Terminal VWAP deve ser tratado em frente propria;`
    - linha 29: `A branch atual materializa a abertura da frente propria de Terminal VWAP e infraestrutura da UI moderna.`
    - linha 35: `audit/ui-modern-terminal-vwap`
    - linha 55: `fafe28c test: add ui modern terminal vwap wiring smoke`
    - linha 77: `- ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py: PRESENTE`
    - linha 101: `Registrar a frente Terminal VWAP como auditoria propria de evolucao macro.`
- `docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 5: `Branch auditada: audit/ui-modern-terminal-vwap`
    - linha 31: `audit/ui-modern-terminal-vwap`
    - linha 51: `fafe28c test: add ui modern terminal vwap wiring smoke`
    - linha 70: `- orientou a abertura de frente propria para Terminal VWAP.`
    - linha 95: `- nao misturar Terminal VWAP com payoff;`
    - linha 96: `- nao misturar Terminal VWAP com UIDataModel;`
    - linha 169: `- wiring inicial com Terminal VWAP.`
    - linha 188: `### M2 - Auditoria real dos arquivos Terminal VWAP`
- `docs/auditoria_ui_terminal_vwap_payoff.md`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `# Auditoria — UI Terminal VWAP Payoff`
    - linha 5: `Registrar a evolução do projeto UI Terminal VWAP Payoff, mantendo histórico de:`
    - linha 33: `feature/ui-terminal-vwap-payoff`
    - linha 37: `spike/ui-terminal-vwap-payoff`
    - linha 50: `A branch feature/ui-terminal-vwap-payoff já existe localmente. Não deve ser criada novamente sem necessidade.`
    - linha 62: `Campo VWAP confirmado documentalmente:`
    - linha 64: `=RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")`
    - linha 140: `docs/ui_terminal_vwap_payoff_plano.md`
- `docs/ui_terminal_vwap_payoff_plano.md`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `# Projeto UI Terminal VWAP Payoff`
    - linha 10: `- VWAP do ativo-base;`
    - linha 78: `Terminal VWAP Payoff`
    - linha 135: `O documento LISTA RTD FUNCOES.pdf confirma o campo VWAP:`
    - linha 137: `=RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")`
    - linha 139: `A primeira versão não deve calcular VWAP por conta própria.`
    - linha 141: `O objetivo técnico é ler, normalizar, tratar falhas, registrar fonte e exibir a VWAP recebida do RTD.`
    - linha 165: `QUOTE.VWAP`
- `infra/bootstrap_rtd_option_quotes_schema.py`
  - Classificacao inicial: possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 22: `"vwap",`
    - linha 36: `"vwap": "REAL",`
    - linha 57: `vwap REAL,`
- `reports/auditoria/UI_FRENTES_ENCERRADAS.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 87: `- Terminal VWAP Payoff;`
    - linha 163: `## 5. Frentes do painel dark de estruturas e Terminal VWAP consolidadas`
    - linha 171: `- UI/components/terminal_vwap_payoff_dark_panel.py`
    - linha 172: `- ui/components/terminal_vwap_payoff_dark_panel.py`
    - linha 254: `- UI/components/terminal_vwap_payoff_dark_panel.py`
    - linha 302: `Foi implementado callback para carregar no Terminal VWAP a estrutura associada a decisao selecionada.`
    - linha 489: `- carregamento da estrutura associada no Terminal VWAP;`
- `reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, documentacao, possivel dependencia/camada proibida
  - Evidencias:
    - linha 73: `- acao inversa Terminal VWAP para Decisoes filtradas pela estrutura selecionada;`
    - linha 131: `- separar UI canonica, UI moderna, Decisoes, Terminal VWAP, payoff, UIDataModel e banco;`
    - linha 141: `### 6.1. Terminal VWAP`
    - linha 145: `- validacoes especificas do Terminal VWAP;`
    - linha 160: `Abrir auditoria propria para Terminal VWAP.`
    - linha 285: `8. abrir frentes separadas para Terminal VWAP, payoff, UIDataModel e banco.`
    - linha 334: `- refatorar Terminal VWAP fora de Decisoes;`
    - linha 368: `Terminal VWAP:`
- `repositories/rtd_option_quotes_repository.py`
  - Classificacao inicial: possivel dependencia/camada proibida
  - Evidencias:
    - linha 43: `vwap,`
    - linha 77: `vwap,`
    - linha 110: `vwap,`
- `scripts/classificar_areas_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 114: `"Terminal VWAP": [`
    - linha 115: `r"\bvwap\b",`
    - linha 260: `"Terminal VWAP",`
    - linha 378: `### Terminal VWAP`
    - linha 494: `- Terminal VWAP permanece fora do escopo da branch atual;`
- `scripts/criar_registro_execucao_smoke_decisoes_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 365: `- Terminal VWAP permanece fora do escopo desta branch;`
    - linha 440: `- Terminal VWAP fora do escopo da branch atual;`
- `scripts/criar_smoke_manual_decisoes_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 456: `- Terminal VWAP fora do escopo da branch atual;`
- `scripts/cruzar_matriz_areas_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 111: `"Terminal VWAP",`
    - linha 128: `"Terminal VWAP": [`
    - linha 129: `r"\bvwap\b",`
    - linha 248: `if area == "Terminal VWAP":`
    - linha 457: `4. Terminal VWAP permanece fora do escopo da branch atual.`
    - linha 494: `- Terminal VWAP;`
    - linha 609: `- Terminal VWAP;`
- `scripts/documentar_matriz_equivalencia_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 80: `| Terminal VWAP | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Abrir auditoria propria |`
    - linha 151: `- auditar Terminal VWAP separadamente;`
    - linha 226: `- Terminal VWAP permanece fora do escopo da branch de Decisoes;`
- `scripts/documentar_pendencias_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 124: `#### 3. Terminal VWAP, payoff e UIDataModel`
    - linha 132: `- Terminal VWAP;`
    - linha 197: `abrir auditoria propria para Terminal VWAP/payoff/UIDataModel`
- `scripts/documentar_pendencias_ui_safe.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 153: `#### 3. Terminal VWAP, payoff e UIDataModel`
    - linha 161: `- Terminal VWAP;`
    - linha 226: `abrir auditoria propria para Terminal VWAP/payoff/UIDataModel`
- `scripts/import_rtd_option_quotes_wide_csv.py`
  - Classificacao inicial: possivel dependencia/camada proibida
  - Evidencias:
    - linha 24: `"vwap",`
    - linha 44: `"vwap",`
    - linha 194: `"vwap": parse_number(raw.get("vwap")),`
    - linha 243: `"vwap",`
- `scripts/inventariar_arquivos_ui.sh`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 113: `"vwap": r"vwap|VWAP",`
    - linha 240: `- referencias a decisoes, payoff, VWAP e tema dark;`
    - linha 281: `3. Areas Terminal VWAP, payoff curve e UIDataModel exigem auditoria propria.`
    - linha 391: `- Terminal VWAP;`
- `services/terminal_vwap_payoff_app_service.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `"""App service do Terminal VWAP Payoff.`
    - linha 14: `class TerminalVWAPPayoffAppService:`
    - linha 15: `"""Orquestra a montagem do ViewModel do Terminal VWAP Payoff.`
    - linha 22: `- viewmodel_service: opcional, por padrão usa TerminalVWAPPayoffViewModelService.`
    - linha 112: `from services.terminal_vwap_payoff_viewmodel_service import (`
    - linha 113: `TerminalVWAPPayoffViewModelService,`
    - linha 116: `return TerminalVWAPPayoffViewModelService()`
    - linha 206: `"source": "terminal_vwap_payoff_app_service",`
- `services/terminal_vwap_payoff_viewmodel_service.py`
  - Classificacao inicial: path contem vwap, relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 1: `"""ViewModel do Terminal VWAP Payoff.`
    - linha 3: `Este módulo monta um payload puro para a futura UI do Terminal VWAP Payoff.`
    - linha 18: `class TerminalVWAPPayoffViewModelService:`
    - linha 19: `"""Monta o ViewModel canônico do Terminal VWAP Payoff."""`
    - linha 55: `"name": "ui-terminal-vwap-payoff",`
    - linha 64: `"source": "terminal_vwap_payoff_viewmodel_service",`
    - linha 170: `vwap = self._to_float(`
    - linha 173: `"vwap",`
- `tools/audit_rtd_ui_flow.py`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 343: `"UI/components/terminal_vwap_payoff_dark_panel.py",`
- `tools/fix_structure_side_panel_patch.py`
  - Classificacao inicial: relacao com terminal detectada, possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 3: `path = Path("UI/components/terminal_vwap_payoff_dark_panel.py")`
    - linha 11: `backup = Path("UI/components/terminal_vwap_payoff_dark_panel.py.bak_side_actions_fix")`
- `tools/patch_structure_side_panel.py`
  - Classificacao inicial: possivel componente UI, possivel dependencia/camada proibida
  - Evidencias:
    - linha 673: `text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff"`

## 4. Testes automatizados relacionados

- ATT/tests/test_terminal_vwap_payoff_app_service.py
- ATT/tests/test_terminal_vwap_payoff_controller.py
- ATT/tests/test_terminal_vwap_payoff_panel.py
- ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py

## 5. Documentacao relacionada

- docs/CLASSIFICACAO_AREAS_UI.md
- docs/DESENVOLVIMENTO_UI.md
- docs/INVENTARIO_ARQUIVOS_UI.md
- docs/MATRIZ_CRUZADA_AREAS_UI.md
- docs/MATRIZ_EQUIVALENCIA_UI.md
- docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md
- docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md
- docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md
- docs/auditoria_ui_terminal_vwap_payoff.md
- docs/ui_terminal_vwap_payoff_plano.md
- reports/auditoria/UI_FRENTES_ENCERRADAS.md
- reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md

## 6. Possiveis componentes UI relacionados

- ATT/tests/test_terminal_vwap_payoff_app_service.py
- ATT/tests/test_terminal_vwap_payoff_panel.py
- ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py
- UI/components/terminal_vwap_payoff_dark_panel.py
- UI/components/terminal_vwap_payoff_panel.py
- UI/main_window.py
- UI/modern/dark_window.py
- UI/modern/main_window.py
- controllers/terminal_vwap_payoff_controller.py
- docs/CLASSIFICACAO_AREAS_UI.md
- docs/DESENVOLVIMENTO_UI.md
- docs/INVENTARIO_ARQUIVOS_UI.md
- docs/MATRIZ_CRUZADA_AREAS_UI.md
- docs/MATRIZ_EQUIVALENCIA_UI.md
- docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md
- docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md
- docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md
- docs/auditoria_ui_terminal_vwap_payoff.md
- docs/ui_terminal_vwap_payoff_plano.md
- infra/bootstrap_rtd_option_quotes_schema.py
- reports/auditoria/UI_FRENTES_ENCERRADAS.md
- reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md
- scripts/classificar_areas_ui.sh
- scripts/criar_registro_execucao_smoke_decisoes_ui.sh
- scripts/criar_smoke_manual_decisoes_ui.sh
- scripts/cruzar_matriz_areas_ui.sh
- scripts/documentar_matriz_equivalencia_ui.sh
- scripts/documentar_pendencias_ui.sh
- scripts/documentar_pendencias_ui_safe.sh
- scripts/inventariar_arquivos_ui.sh
- services/terminal_vwap_payoff_app_service.py
- services/terminal_vwap_payoff_viewmodel_service.py
- tools/audit_rtd_ui_flow.py
- tools/fix_structure_side_panel_patch.py
- tools/patch_structure_side_panel.py

## 7. Possiveis riscos de dependencia proibida

- `ATT/tests/test_terminal_vwap_payoff_app_service.py`
- `ATT/tests/test_terminal_vwap_payoff_controller.py`
- `ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py`
- `ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py`
- `UI/components/terminal_vwap_payoff_dark_panel.py`
- `UI/components/terminal_vwap_payoff_panel.py`
- `UI/main_window.py`
- `UI/modern/dark_window.py`
- `UI/modern/main_window.py`
- `controllers/terminal_vwap_payoff_controller.py`
- `docs/CLASSIFICACAO_AREAS_UI.md`
- `docs/DESENVOLVIMENTO_UI.md`
- `docs/INVENTARIO_ARQUIVOS_UI.md`
- `docs/MATRIZ_CRUZADA_AREAS_UI.md`
- `docs/MATRIZ_EQUIVALENCIA_UI.md`
- `docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md`
- `docs/auditoria/UI_AUDITORIA_MACRO_EVOLUCAO.md`
- `docs/auditoria/UI_COMPARATIVO_ROTA_MACRO.md`
- `docs/auditoria_ui_terminal_vwap_payoff.md`
- `docs/ui_terminal_vwap_payoff_plano.md`
- `infra/bootstrap_rtd_option_quotes_schema.py`
- `reports/auditoria/UI_FRENTES_ENCERRADAS.md`
- `reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md`
- `repositories/rtd_option_quotes_repository.py`
- `scripts/classificar_areas_ui.sh`
- `scripts/criar_registro_execucao_smoke_decisoes_ui.sh`
- `scripts/criar_smoke_manual_decisoes_ui.sh`
- `scripts/cruzar_matriz_areas_ui.sh`
- `scripts/documentar_matriz_equivalencia_ui.sh`
- `scripts/documentar_pendencias_ui.sh`
- `scripts/documentar_pendencias_ui_safe.sh`
- `scripts/import_rtd_option_quotes_wide_csv.py`
- `scripts/inventariar_arquivos_ui.sh`
- `services/terminal_vwap_payoff_app_service.py`
- `services/terminal_vwap_payoff_viewmodel_service.py`
- `tools/audit_rtd_ui_flow.py`
- `tools/fix_structure_side_panel_patch.py`
- `tools/patch_structure_side_panel.py`

## 8. Classificacao operacional da frente

A frente Terminal VWAP deve continuar separada das seguintes areas:

- banco;
- schema;
- pipeline;
- services;
- repositories;
- controllers;
- regra de negocio;
- payoff;
- UIDataModel.

Correcoes permitidas no proximo bloco devem permanecer restritas a UI.

## 9. Criterio para o proximo pacote grande UI-only

O proximo bloco pode agrupar correcoes se elas envolverem apenas:

- montagem visual;
- criacao de painel;
- wiring entre janela dark e componente Terminal VWAP;
- estado vazio;
- mensagem de ausencia de dados;
- mensagem de status;
- botoes desabilitados;
- fallback visual;
- tratamento visual de erro de inicializacao;
- testes automatizados desses comportamentos.

O bloco deve parar se exigir:

- nova query;
- novo repository;
- novo service;
- novo controller;
- migracao;
- schema;
- escrita em banco;
- sincronizacao entre bancos;
- regra de negocio nova;
- alteracao de payoff;
- alteracao de UIDataModel.

## 10. Proposta de lote M3

Nome sugerido:

M3 - Primeiro pacote grande UI-only do Terminal VWAP.

Objetivo:

Consolidar carregamento, montagem visual, estados vazios e wiring inicial do Terminal VWAP na UI moderna dark.

Escopo sugerido:

1. validar imports e construcao do componente;
2. validar abertura pela janela dark;
3. validar comportamento sem dados;
4. validar mensagens de status;
5. validar guard clauses de UI;
6. criar ou ampliar testes automatizados;
7. executar regressao acumulada da frente.

## 11. Decisao

A frente esta apta a avancar para correcao em lote somente apos revisao deste inventario.

Se os arquivos candidatos estiverem concentrados em UI e testes, o proximo passo deve ser M3.

Se os candidatos apontarem dependencia relevante de camada proibida, o proximo passo deve ser nova classificacao antes de qualquer correcao.

Classificacao:

DOCUMENTACAO_DE_CONTROLE

AUDITORIA_TERMINAL_VWAP

PREPARACAO_M3_UI_ONLY
