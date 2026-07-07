# Auditoria UI Terminal VWAP

Data de abertura: 2026-07-06

Branch:

    audit/terminal-vwap-ui

Classificacao:

    REGRESSAO_UI

## 1. Objetivo

Abrir frente propria para auditar Terminal VWAP sem misturar escopo com Decisoes dark panel, payoff, UIDataModel, banco, regra de negocio, services, repositories ou controllers.

## 2. Situacao inicial

A fatia Decisoes dark panel foi concluida como entrega parcial operacional.

Terminal VWAP permanece fora do escopo da branch Decisoes dark panel e deve ser tratado em frente propria.

## 3. Escopo permitido desta fase

Esta fase pode avaliar:

- abertura da UI pelo caminho atual do projeto;
- acesso ao Terminal VWAP;
- fluxo completo de estruturas;
- fluxo completo de pernas;
- alertas;
- KPIs;
- graficos;
- estados vazios;
- acoes operacionais proprias do terminal;
- mensagens de status;
- validacao visual em dark mode;
- pontos de regressao manual especificos do terminal.

## 4. Escopos proibidos nesta fase

Nao esta autorizado nesta fase:

- alterar banco;
- alterar schema;
- alterar regra de negocio;
- alterar services;
- alterar repositories;
- alterar controllers;
- alterar pipeline de dados;
- sincronizar app.db com derived.db;
- sincronizar derived.db com app.db;
- resolver payoff fora do necessario para observacao visual;
- declarar equivalencia global da UI moderna dark;
- alterar o entrypoint principal;
- eliminar a UI atual.

## 5. Primeira etapa autorizada

A primeira etapa desta frente e somente auditoria e inventario.

Nenhuma correcao funcional deve ser aplicada antes de registrar:

- arquivos envolvidos;
- componentes de UI relacionados;
- fluxos observados;
- pontos de validacao manual;
- pendencias encontradas;
- criterio minimo para smoke manual do Terminal VWAP.

## 6. Criterio minimo de continuidade

Antes de qualquer patch, esta auditoria deve responder:

- qual componente renderiza o Terminal VWAP;
- qual modelo de dados alimenta o terminal;
- quais acoes sao apenas UI;
- quais acoes dependem de regra de negocio;
- quais validacoes podem ser feitas sem banco ou pipeline;
- quais riscos exigem frente propria fora da UI.

## 7. Status

ABERTO

<!-- INVENTARIO_INICIAL_TERMINAL_VWAP_2026_07_06 -->

## 8. Inventario inicial de arquivos relacionados

Data: 2026-07-06

Metodo:

    Busca textual local por termos relacionados a Terminal VWAP.

Termos buscados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Arquivos encontrados:

### _auditoria_next/docs_smoke_refs/referencias_smoke_manual.txt

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 27: docs/MATRIZ_CRUZADA_AREAS_UI.md:89:| Decisoes | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminh...
- linha 33: docs/MATRIZ_CRUZADA_AREAS_UI.md:98:| Decisoes | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e cont...
- linha 36: docs/MATRIZ_CRUZADA_AREAS_UI.md:101:| Decisoes | docs/ui_terminal_vwap_payoff_plano.md | 965 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteud...
- linha 74: docs/MATRIZ_CRUZADA_AREAS_UI.md:333:| Navegacao / abas / layout | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de...
- linha 75: docs/MATRIZ_CRUZADA_AREAS_UI.md:334:| Navegacao / abas / layout | UI/components/terminal_vwap_payoff_panel.py | 538 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de camin...
- linha 82: docs/MATRIZ_CRUZADA_AREAS_UI.md:344:| Navegacao / abas / layout | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de caminho...
- linha 86: docs/MATRIZ_CRUZADA_AREAS_UI.md:348:| Navegacao / abas / layout | docs/ui_terminal_vwap_payoff_plano.md | 965 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de caminho e c...

### _auditoria_next/frentes_pendentes_20260706_154320/00_contexto_git.txt

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 48: docs/auditoria_ui_terminal_vwap_payoff.md
- linha 164: docs/ui_terminal_vwap_payoff_plano.md

### _auditoria_next/frentes_pendentes_20260706_154320/00_INDICE.txt

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 8: _auditoria_next/frentes_pendentes_20260706_154320/05_terminal_vwap.txt

### _auditoria_next/frentes_pendentes_20260706_154320/01_documentos_controle.txt

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 47: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:89:| Decisoes | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de cami...
- linha 53: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:98:| Decisoes | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e co...
- linha 56: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:101:| Decisoes | docs/ui_terminal_vwap_payoff_plano.md | 965 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conte...
- linha 94: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:333:| Navegacao / abas / layout | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica ...
- linha 95: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:334:| Navegacao / abas / layout | UI/components/terminal_vwap_payoff_panel.py | 538 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de cam...
- linha 102: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:344:| Navegacao / abas / layout | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de camin...
- linha 106: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:348:| Navegacao / abas / layout | docs/ui_terminal_vwap_payoff_plano.md | 965 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de caminho e...

### _auditoria_next/frentes_pendentes_20260706_154320/02_decisoes_dark_panel.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 15: UI/components/__pycache__/terminal_vwap_payoff_dark_panel.cpython-313.pyc
- linha 18: UI/components/terminal_vwap_payoff_dark_panel.py
- linha 35: .\controllers\terminal_vwap_payoff_controller.py:25:    def load_structure(self, structure_id: Any) -> dict[str, Any]:
- linha 36: .\controllers\terminal_vwap_payoff_controller.py:32:        if hasattr(self._app_service, "load_structure"):
- linha 37: .\controllers\terminal_vwap_payoff_controller.py:33:            return self._app_service.load_structure(normalized_structure_id)
- linha 38: .\controllers\terminal_vwap_payoff_controller.py:36:            "app_service deve expor build_for_structure_id ou load_structure"
- linha 39: .\controllers\terminal_vwap_payoff_controller.py:41:        return self.load_structure(structure_id)
- linha 40: .\controllers\terminal_vwap_payoff_controller.py:45:        return self.load_structure(structure_id)
- linha 135: .\UI\modern\dark_window.py:20:from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
- linha 148: .\UI\modern\dark_window.py:122:        Fornece as estruturas carregadas no Terminal VWAP para a aba Decisões.
- linha 305: .\ATT\tests\test_terminal_vwap_payoff_controller.py:10:        self.loaded_structure_ids = []
- linha 306: .\ATT\tests\test_terminal_vwap_payoff_controller.py:29:        self.loaded_structure_ids.append(structure_id)

### _auditoria_next/frentes_pendentes_20260706_154320/03_testes_decisoes.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 69: ATT/tests/__pycache__/test_terminal_vwap_payoff_app_service.cpython-313-pytest-9.0.3.pyc
- linha 70: ATT/tests/__pycache__/test_terminal_vwap_payoff_controller.cpython-313-pytest-9.0.3.pyc
- linha 71: ATT/tests/__pycache__/test_terminal_vwap_payoff_panel.cpython-313-pytest-9.0.3.pyc
- linha 72: ATT/tests/__pycache__/test_terminal_vwap_payoff_viewmodel_service.cpython-313-pytest-9.0.3.pyc
- linha 125: ATT/tests/test_terminal_vwap_payoff_app_service.py
- linha 126: ATT/tests/test_terminal_vwap_payoff_controller.py
- linha 127: ATT/tests/test_terminal_vwap_payoff_panel.py
- linha 128: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 228: .\scripts\inventariar_arquivos_ui.sh:240:- referencias a decisoes, payoff, VWAP e tema dark;
- linha 361: .\scripts\documentar_matriz_equivalencia_ui.sh:226:- Terminal VWAP permanece fora do escopo da branch de Decisoes;
- linha 467: .\scripts\auditoria_ui\01_localizar_frentes_pendentes.sh:157:section "12_arquivos_python_candidatos.txt" "Python relacionados a UI e frentes pendentes" "search_files_by_name '\\...
- linha 476: .\UI\components\terminal_vwap_payoff_dark_panel.py:113:# BEGIN AUTO STRUCTURE DECISION HELPERS

### _auditoria_next/frentes_pendentes_20260706_154320/04_matriz_global_ui.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 40: .\UI\modern\dark_window.py:6:Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde
- linha 41: .\UI\modern\dark_window.py:20:from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
- linha 46: .\UI\modern\dark_window.py:79:        self.panel = TerminalVWAPPayoffDarkPanel(
- linha 62: .\UI\components\terminal_vwap_payoff_dark_panel.py:1:# UI/components/terminal_vwap_payoff_dark_panel.py
- linha 63: .\UI\components\terminal_vwap_payoff_dark_panel.py:4:Painel operacional dark para análise VWAP e Payoff.
- linha 64: .\UI\components\terminal_vwap_payoff_dark_panel.py:45:DARK_BG = "#121212"
- linha 65: .\UI\components\terminal_vwap_payoff_dark_panel.py:129:class TerminalVWAPPayoffDarkPanel(ctk.CTkFrame):
- linha 66: .\UI\components\terminal_vwap_payoff_dark_panel.py:136:        super().__init__(parent, fg_color=DARK_BG)
- linha 67: .\UI\components\terminal_vwap_payoff_dark_panel.py:163:            "Dark.Treeview",
- linha 68: .\UI\components\terminal_vwap_payoff_dark_panel.py:171:            "Dark.Treeview.Heading",
- linha 69: .\UI\components\terminal_vwap_payoff_dark_panel.py:177:            "Dark.Treeview",
- linha 70: .\UI\components\terminal_vwap_payoff_dark_panel.py:303:            fg_color=DARK_BG,

### _auditoria_next/frentes_pendentes_20260706_154320/05_terminal_vwap.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: # Frente Terminal VWAP
- linha 24: ATT/tests/__pycache__/test_terminal_vwap_payoff_app_service.cpython-313-pytest-9.0.3.pyc
- linha 25: ATT/tests/__pycache__/test_terminal_vwap_payoff_controller.cpython-313-pytest-9.0.3.pyc
- linha 26: ATT/tests/__pycache__/test_terminal_vwap_payoff_panel.cpython-313-pytest-9.0.3.pyc
- linha 27: ATT/tests/__pycache__/test_terminal_vwap_payoff_viewmodel_service.cpython-313-pytest-9.0.3.pyc
- linha 40: ATT/tests/test_terminal_vwap_payoff_app_service.py
- linha 41: ATT/tests/test_terminal_vwap_payoff_controller.py
- linha 42: ATT/tests/test_terminal_vwap_payoff_panel.py
- linha 43: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 44: UI/components/__pycache__/terminal_vwap_payoff_dark_panel.cpython-313.pyc
- linha 45: UI/components/__pycache__/terminal_vwap_payoff_panel.cpython-313.pyc
- linha 46: UI/components/terminal_vwap_payoff_dark_panel.py

### _auditoria_next/frentes_pendentes_20260706_154320/06_payoff.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 14: ATT/tests/__pycache__/test_terminal_vwap_payoff_app_service.cpython-313-pytest-9.0.3.pyc
- linha 15: ATT/tests/__pycache__/test_terminal_vwap_payoff_controller.cpython-313-pytest-9.0.3.pyc
- linha 16: ATT/tests/__pycache__/test_terminal_vwap_payoff_panel.cpython-313-pytest-9.0.3.pyc
- linha 17: ATT/tests/__pycache__/test_terminal_vwap_payoff_viewmodel_service.cpython-313-pytest-9.0.3.pyc
- linha 20: ATT/tests/test_terminal_vwap_payoff_app_service.py
- linha 21: ATT/tests/test_terminal_vwap_payoff_controller.py
- linha 22: ATT/tests/test_terminal_vwap_payoff_panel.py
- linha 23: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 25: UI/components/__pycache__/terminal_vwap_payoff_dark_panel.cpython-313.pyc
- linha 26: UI/components/__pycache__/terminal_vwap_payoff_panel.cpython-313.pyc
- linha 28: UI/components/terminal_vwap_payoff_dark_panel.py
- linha 29: UI/components/terminal_vwap_payoff_panel.py

### _auditoria_next/frentes_pendentes_20260706_154320/07_uidatamodel.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 11: ATT/tests/__pycache__/test_terminal_vwap_payoff_viewmodel_service.cpython-313-pytest-9.0.3.pyc
- linha 12: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 17: services/__pycache__/terminal_vwap_payoff_viewmodel_service.cpython-313.pyc
- linha 18: services/terminal_vwap_payoff_viewmodel_service.py
- linha 57: .\UI\components\terminal_vwap_payoff_dark_panel.py:755:            query = self._build_market_query(conn)
- linha 58: .\UI\components\terminal_vwap_payoff_dark_panel.py:756:            if not query:
- linha 59: .\UI\components\terminal_vwap_payoff_dark_panel.py:759:            rows = conn.execute(query["sql"], (asset,)).fetchall()
- linha 60: .\UI\components\terminal_vwap_payoff_dark_panel.py:760:            return self._market_result_from_rows(result, rows, query)
- linha 61: .\UI\components\terminal_vwap_payoff_dark_panel.py:790:    def _build_market_query(self, conn: Any) -> Dict[str, Any]:
- linha 62: .\UI\components\terminal_vwap_payoff_dark_panel.py:889:        query: Dict[str, Any],
- linha 63: .\UI\components\terminal_vwap_payoff_dark_panel.py:913:        result["source_table"] = query["table"]
- linha 64: .\UI\components\terminal_vwap_payoff_dark_panel.py:914:        result["vwap_source"] = query["table"] if query.get("has_vwap") else None

### _auditoria_next/frentes_pendentes_20260706_154320/08_banco_dados_pipeline.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 614: .\UI\components\terminal_vwap_payoff_dark_panel.py:14:O painel lê dados do banco dados/app.db com introspecção defensiva de schema.
- linha 615: .\UI\components\terminal_vwap_payoff_dark_panel.py:24:import sqlite3
- linha 616: .\UI\components\terminal_vwap_payoff_dark_panel.py:465:    def _connect(self) -> sqlite3.Connection:
- linha 617: .\UI\components\terminal_vwap_payoff_dark_panel.py:468:            raise FileNotFoundError(f"Banco app.db não encontrado em: {db}")
- linha 618: .\UI\components\terminal_vwap_payoff_dark_panel.py:469:        conn = sqlite3.connect(str(db))
- linha 619: .\UI\components\terminal_vwap_payoff_dark_panel.py:470:        conn.row_factory = sqlite3.Row
- linha 620: .\UI\components\terminal_vwap_payoff_dark_panel.py:473:    def _tables_cols(self, conn: sqlite3.Connection) -> Dict[str, List[str]]:
- linha 621: .\UI\components\terminal_vwap_payoff_dark_panel.py:474:        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
- linha 622: .\UI\components\terminal_vwap_payoff_dark_panel.py:485:    def _find_structures_table(self, schema: Dict[str, List[str]]) -> Optional[str]:
- linha 623: .\UI\components\terminal_vwap_payoff_dark_panel.py:493:            if table in schema:
- linha 624: .\UI\components\terminal_vwap_payoff_dark_panel.py:496:        for table, cols in schema.items():
- linha 625: .\UI\components\terminal_vwap_payoff_dark_panel.py:506:        conn = self._connect()

### _auditoria_next/frentes_pendentes_20260706_154320/09_guardrails_services_repositories_controllers.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 32: ATT/tests/__pycache__/test_terminal_vwap_payoff_app_service.cpython-313-pytest-9.0.3.pyc
- linha 33: ATT/tests/__pycache__/test_terminal_vwap_payoff_controller.cpython-313-pytest-9.0.3.pyc
- linha 34: ATT/tests/__pycache__/test_terminal_vwap_payoff_viewmodel_service.cpython-313-pytest-9.0.3.pyc
- linha 56: ATT/tests/test_terminal_vwap_payoff_app_service.py
- linha 57: ATT/tests/test_terminal_vwap_payoff_controller.py
- linha 58: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 65: controllers/__pycache__/terminal_vwap_payoff_controller.cpython-313.pyc
- linha 66: controllers/terminal_vwap_payoff_controller.py
- linha 121: services/__pycache__/terminal_vwap_payoff_app_service.cpython-313.pyc
- linha 122: services/__pycache__/terminal_vwap_payoff_viewmodel_service.cpython-313.pyc
- linha 150: services/terminal_vwap_payoff_app_service.py
- linha 151: services/terminal_vwap_payoff_viewmodel_service.py

### _auditoria_next/frentes_pendentes_20260706_154320/10_testes_existentes.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 69: ATT/tests/__pycache__/test_terminal_vwap_payoff_app_service.cpython-313-pytest-9.0.3.pyc
- linha 70: ATT/tests/__pycache__/test_terminal_vwap_payoff_controller.cpython-313-pytest-9.0.3.pyc
- linha 71: ATT/tests/__pycache__/test_terminal_vwap_payoff_panel.cpython-313-pytest-9.0.3.pyc
- linha 72: ATT/tests/__pycache__/test_terminal_vwap_payoff_viewmodel_service.cpython-313-pytest-9.0.3.pyc
- linha 125: ATT/tests/test_terminal_vwap_payoff_app_service.py
- linha 126: ATT/tests/test_terminal_vwap_payoff_controller.py
- linha 127: ATT/tests/test_terminal_vwap_payoff_panel.py
- linha 128: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 172: .\docs\ui_terminal_vwap_payoff_plano.md:127:- validação de structure_id;
- linha 173: .\docs\ui_terminal_vwap_payoff_plano.md:320:### Fase 0 — Preparação, busca e proteção contra regressão
- linha 174: .\docs\ui_terminal_vwap_payoff_plano.md:575:- testes de regressão passam.
- linha 175: .\docs\ui_terminal_vwap_payoff_plano.md:712:### Risco 3 — Regressão no payoff atual

### _auditoria_next/frentes_pendentes_20260706_154320/11_todos_fixmes_pendencias.txt

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 16: .\docs\ui_terminal_vwap_payoff_plano.md:28:Estas regras se aplicam a todos os projetos, fases e alterações.
- linha 17: .\docs\ui_terminal_vwap_payoff_plano.md:42:F. Após o encerramento de cada fase, o teste deve compor todas as fases encerradas, evitando pendências acumuladas.
- linha 18: .\docs\ui_terminal_vwap_payoff_plano.md:52:K. Criar e manter arquivo de auditoria atualizado com testes, conclusões, pendências e evolução.
- linha 19: .\docs\ui_terminal_vwap_payoff_plano.md:240:- dependência de CSVs antigos;
- linha 20: .\docs\ui_terminal_vwap_payoff_plano.md:476:- impedir dependência de CSV antigo.
- linha 21: .\docs\ui_terminal_vwap_payoff_plano.md:615:- não há dependência de CSV antigo.
- linha 22: .\docs\ui_terminal_vwap_payoff_plano.md:670:- todos os testes da fase atual passam;
- linha 23: .\docs\ui_terminal_vwap_payoff_plano.md:671:- todos os testes das fases anteriores passam;
- linha 24: .\docs\ui_terminal_vwap_payoff_plano.md:706:### Risco 2 — Dependência indevida do Excel
- linha 25: .\docs\ui_terminal_vwap_payoff_plano.md:730:### Risco 6 — CSV antigo voltar como dependência
- linha 26: .\docs\ui_terminal_vwap_payoff_plano.md:820:    Não usar CSV derivado antigo como dependência da UI.
- linha 27: .\docs\ui_terminal_vwap_payoff_plano.md:956:    Não houve dependência de CSV derivado antigo.

### _auditoria_next/frentes_pendentes_20260706_154320/12_arquivos_python_candidatos.txt

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 35: ATT/tests/test_terminal_vwap_payoff_app_service.py
- linha 36: ATT/tests/test_terminal_vwap_payoff_controller.py
- linha 37: ATT/tests/test_terminal_vwap_payoff_panel.py
- linha 38: ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- linha 49: UI/components/terminal_vwap_payoff_dark_panel.py
- linha 50: UI/components/terminal_vwap_payoff_panel.py
- linha 64: controllers/terminal_vwap_payoff_controller.py
- linha 108: services/terminal_vwap_payoff_app_service.py
- linha 109: services/terminal_vwap_payoff_viewmodel_service.py

### _auditoria_next/frentes_pendentes_20260706_154320/13_resumo_para_proxima_decisao.md

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 30: 9. Seguir para frentes separadas: Terminal VWAP, payoff, UIDataModel e banco.

### _auditoria_next/referencias_smoke_manual_20260706_154452.txt

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 59: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:89:| Decisoes | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de cami...
- linha 65: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:98:| Decisoes | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e co...
- linha 68: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:101:| Decisoes | docs/ui_terminal_vwap_payoff_plano.md | 965 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conte...
- linha 106: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:333:| Navegacao / abas / layout | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica ...
- linha 107: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:334:| Navegacao / abas / layout | UI/components/terminal_vwap_payoff_panel.py | 538 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de cam...
- linha 114: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:344:| Navegacao / abas / layout | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de camin...
- linha 118: .\docs\MATRIZ_CRUZADA_AREAS_UI.md:348:| Navegacao / abas / layout | docs/ui_terminal_vwap_payoff_plano.md | 965 | PENDENTE_SMOKE_MANUAL | MEDIO | Varredura estatica de caminho e...

### _auditoria_next/validacao_escopo_20260706_153923.txt

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 23: Se aparecer service, repository, controller, banco, pipeline, Terminal VWAP, payoff ou UIDataModel, parar e reclassificar antes de continuar.

### _auditoria_next/validacao_escopo_20260706_154529.txt

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 22: Se aparecer service, repository, controller, banco, pipeline, Terminal VWAP, payoff ou UIDataModel, parar e reclassificar antes de continuar.

### ATT/tests/test_terminal_vwap_payoff_app_service.py

Termos encontrados:

- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 3: from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService
- linha 30: "vwap": 100.0,
- linha 72: "name": "ui-terminal-vwap-payoff",
- linha 84: def build_terminal_vwap_payoff_viewmodel(
- linha 92: "vwap": market_snapshot["vwap"],
- linha 124: service = TerminalVWAPPayoffAppService(
- linha 133: assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"
- linha 136: assert result["market"]["vwap"] == 100.0
- linha 151: service = TerminalVWAPPayoffAppService(
- linha 163: service = TerminalVWAPPayoffAppService(
- linha 174: "vwap": 100.0,
- linha 180: service = TerminalVWAPPayoffAppService(

### ATT/tests/test_terminal_vwap_payoff_controller.py

Termos encontrados:

- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 3: from controllers.terminal_vwap_payoff_controller import (
- linha 4: TerminalVWAPPayoffController,
- linha 8: class FakeTerminalVWAPPayoffAppService:
- linha 32: "name": "ui-terminal-vwap-payoff",
- linha 45: app_service = FakeTerminalVWAPPayoffAppService()
- linha 46: controller = TerminalVWAPPayoffController(app_service)
- linha 51: assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"
- linha 57: app_service = FakeTerminalVWAPPayoffAppService()
- linha 58: controller = TerminalVWAPPayoffController(app_service)
- linha 73: controller = TerminalVWAPPayoffController(
- linha 74: FakeTerminalVWAPPayoffAppService()
- linha 82: controller = TerminalVWAPPayoffController(

### ATT/tests/test_terminal_vwap_payoff_panel.py

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 1: from UI.components.terminal_vwap_payoff_panel import (
- linha 21: "vwap": 10,
- linha 22: "price_vs_vwap_percent": 10,
- linha 69: assert summary["vwap"] == "10,00"
- linha 70: assert summary["price_vs_vwap_percent"] == "10,00%"

### ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py

Termos encontrados:

- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: from services.terminal_vwap_payoff_viewmodel_service import (
- linha 2: TerminalVWAPPayoffViewModelService,
- linha 6: def test_build_terminal_vwap_payoff_viewmodel_with_vwap_and_payoff_points():
- linha 7: service = TerminalVWAPPayoffViewModelService()
- linha 30: "vwap": 10.0,
- linha 42: assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"
- linha 54: assert result["market"]["vwap"] == 10.0
- linha 55: assert result["market"]["status_vwap"] == "available"
- linha 56: assert result["market"]["price_vs_vwap_percent"] == 10.0
- linha 67: def test_build_terminal_vwap_payoff_viewmodel_handles_missing_vwap_and_empty_payoff():
- linha 68: service = TerminalVWAPPayoffViewModelService()
- linha 73: "name": "Estrutura sem VWAP",

### controllers/terminal_vwap_payoff_controller.py

Termos encontrados:

- terminal vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: """Controller do Terminal VWAP Payoff.
- linha 17: class TerminalVWAPPayoffController:
- linha 18: """Controller fino para seleção e carga do Terminal VWAP Payoff."""

### docs/auditoria_ui_terminal_vwap_payoff.md

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 1: # Auditoria — UI Terminal VWAP Payoff
- linha 5: Registrar a evolução do projeto UI Terminal VWAP Payoff, mantendo histórico de:
- linha 33: feature/ui-terminal-vwap-payoff
- linha 37: spike/ui-terminal-vwap-payoff
- linha 50: A branch feature/ui-terminal-vwap-payoff já existe localmente. Não deve ser criada novamente sem necessidade.
- linha 62: Campo VWAP confirmado documentalmente:
- linha 64: =RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")
- linha 140: docs/ui_terminal_vwap_payoff_plano.md
- linha 141: docs/auditoria_ui_terminal_vwap_payoff.md
- linha 213: - separação entre preço, VWAP, PL e payoff;
- linha 236: vwap
- linha 237: diferenca_preco_vwap_percentual

### docs/CLASSIFICACAO_AREAS_UI.md

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 41: | Terminal VWAP | 46 |
- linha 67: | reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 68: | reports/terminal_vwap_recovery/main_window_terminal_old.py | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 86: | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 94: | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 97: | docs/ui_terminal_vwap_payoff_plano.md | 965 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 109: | reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1178 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 110: | reports/terminal_vwap_recovery/main_window_terminal_old.py | 763 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 132: ## Terminal VWAP
- linha 136: | ATT/tests/test_terminal_vwap_payoff_panel.py | 110 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 137: | ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 116 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |
- linha 139: | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | FORA_ESCOPO_VISUAL - nao misturar com refactor de UI |

### docs/DESENVOLVIMENTO_UI.md

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 72: #### 3. Terminal VWAP, payoff e UIDataModel
- linha 80: - Terminal VWAP;
- linha 145: abrir auditoria propria para Terminal VWAP/payoff/UIDataModel

### docs/INVENTARIO_ARQUIVOS_UI.md

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 36: - referencias a decisoes, payoff, VWAP e tema dark;
- linha 52: | UI/modern/dark_window.py | 202 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel en...
- linha 53: | UI/main_window.py | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar at...
- linha 54: | UI/modern/main_window.py | 777 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, prese...
- linha 55: | reports/terminal_vwap_recovery/main_window_terminal_old.py | 763 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, vwap, dark; possivel entrypoint | PEN...
- linha 56: | reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1178 | caminho/nome sugere UI; conteudo: tkinter, ui_terms, decisoes, payoff, dark; possivel entrypoint | PENDENTE...
- linha 57: | tools/patch_structure_side_panel.py | 726 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, decisoes, payoff, vwap; possivel entrypoint | PENDENTE - possivel entrypo...
- linha 58: | tools/audit_rtd_ui_flow.py | 360 | caminho/nome sugere UI; conteudo: payoff, vwap, dark; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
- linha 70: | scripts/import_rtd_option_quotes_wide_csv.py | 343 | conteudo: textual/rich, vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
- linha 76: | infra/bootstrap_rtd_option_quotes_schema.py | 185 | conteudo: vwap; possivel entrypoint | PENDENTE - possivel entrypoint, preservar ate auditoria propria |
- linha 96: | reports/auditoria/LISTA_MESTRE_PENDENCIAS_UI_20260703_153050.md | 49769 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, matplotlib_ui, textual/rich, ui_terms, deci...
- linha 97: | reports/ui_modern_equivalence/03_inventario_exportacao_png.md | 1737 | caminho/nome sugere UI; conteudo: tkinter, customtkinter, matplotlib_ui, textual/rich, ui_terms, decisoe...

### docs/MATRIZ_CRUZADA_AREAS_UI.md

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 36: 4. Terminal VWAP permanece fora do escopo da branch atual.
- linha 51: | Terminal VWAP | 47 |
- linha 89: | Decisoes | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos cano...
- linha 98: | Decisoes | docs/auditoria_ui_terminal_vwap_payoff.md | 867 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e ...
- linha 101: | Decisoes | docs/ui_terminal_vwap_payoff_plano.md | 965 | EQUIVALENCIA_PARCIAL_OPERACIONAL | MEDIO | Varredura estatica de caminho e conteudo | Cruzar arquivos canonicos e mode...
- linha 113: | Decisoes | reports/terminal_vwap_recovery/main_window_good_85dfbcd.py | 1178 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qu...
- linha 114: | Decisoes | reports/terminal_vwap_recovery/main_window_terminal_old.py | 763 | PRESERVAR_ENTRYPOINT | ALTO | Sinais estaticos de entrypoint | Auditar separadamente antes de qua...
- linha 135: | Terminal VWAP | ATT/tests/test_terminal_vwap_payoff_panel.py | 110 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes...
- linha 136: | Terminal VWAP | ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py | 116 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria p...
- linha 137: | Terminal VWAP | UI/components/decisions_dark_panel.py | 1464 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes de qu...
- linha 138: | Terminal VWAP | UI/components/terminal_vwap_payoff_dark_panel.py | 2114 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria ...
- linha 139: | Terminal VWAP | UI/components/terminal_vwap_payoff_panel.py | 538 | FORA_ESCOPO_BRANCH_ATUAL | ALTO | Varredura estatica de caminho e conteudo | Abrir auditoria propria antes ...

### docs/MATRIZ_EQUIVALENCIA_UI.md

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 53: | Terminal VWAP | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Abrir auditoria propria |
- linha 124: - auditar Terminal VWAP separadamente;

### docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 295: - Terminal VWAP permanece fora do escopo desta branch;
- linha 360: - Terminal VWAP fora do carregamento a partir de Decisoes;

### docs/ui_terminal_vwap_payoff_plano.md

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: # Projeto UI Terminal VWAP Payoff
- linha 10: - VWAP do ativo-base;
- linha 78: Terminal VWAP Payoff
- linha 135: O documento LISTA RTD FUNCOES.pdf confirma o campo VWAP:
- linha 137: =RTD("btg_pro_rtd";"";"QUOTE.VWAP";"BPAC11")
- linha 139: A primeira versão não deve calcular VWAP por conta própria.
- linha 141: O objetivo técnico é ler, normalizar, tratar falhas, registrar fonte e exibir a VWAP recebida do RTD.
- linha 165: QUOTE.VWAP
- linha 225: - VWAP do ativo-base;
- linha 249: UI Terminal VWAP Payoff
- linha 250: TerminalVwapPayoffController
- linha 251: TerminalVwapPayoffViewModelBuilder

### infra/bootstrap_rtd_option_quotes_schema.py

Termos encontrados:

- vwap
- VWAP

Primeiras ocorrencias:

- linha 22: "vwap",
- linha 36: "vwap": "REAL",
- linha 57: vwap REAL,

### reports/auditoria/TERMINAL_VWAP_AUDITORIA.md

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 1: # Auditoria UI Terminal VWAP
- linha 7: audit/terminal-vwap-ui
- linha 15: Abrir frente propria para auditar Terminal VWAP sem misturar escopo com Decisoes dark panel, payoff, UIDataModel, banco, regra de negocio, services, repositories ou controllers.
- linha 21: Terminal VWAP permanece fora do escopo da branch Decisoes dark panel e deve ser tratado em frente propria.
- linha 28: - acesso ao Terminal VWAP;
- linha 69: - criterio minimo para smoke manual do Terminal VWAP.
- linha 75: - qual componente renderiza o Terminal VWAP;

### reports/auditoria/UI_FRENTES_ENCERRADAS.md

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 87: - Terminal VWAP Payoff;
- linha 163: ## 5. Frentes do painel dark de estruturas e Terminal VWAP consolidadas
- linha 171: - UI/components/terminal_vwap_payoff_dark_panel.py
- linha 172: - ui/components/terminal_vwap_payoff_dark_panel.py
- linha 254: - UI/components/terminal_vwap_payoff_dark_panel.py
- linha 302: Foi implementado callback para carregar no Terminal VWAP a estrutura associada a decisao selecionada.
- linha 489: - carregamento da estrutura associada no Terminal VWAP;

### reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 73: - acao inversa Terminal VWAP para Decisoes filtradas pela estrutura selecionada;
- linha 131: - separar UI canonica, UI moderna, Decisoes, Terminal VWAP, payoff, UIDataModel e banco;
- linha 141: ### 6.1. Terminal VWAP
- linha 145: - validacoes especificas do Terminal VWAP;
- linha 160: Abrir auditoria propria para Terminal VWAP.
- linha 285: 8. abrir frentes separadas para Terminal VWAP, payoff, UIDataModel e banco.
- linha 334: - refatorar Terminal VWAP fora de Decisoes;
- linha 368: Terminal VWAP:
- linha 426: - Terminal VWAP e Decisoes;
- linha 466: Se uma alteracao exigir mexer em Terminal VWAP fora do carregamento a partir de Decisoes, a alteracao deve parar e ser reclassificada.
- linha 490: 8. abrir frentes separadas para Terminal VWAP, payoff, UIDataModel e banco, se necessario.
- linha 575: - resolver Terminal VWAP fora do carregamento a partir de Decisoes;

### repositories/rtd_option_quotes_repository.py

Termos encontrados:

- vwap
- VWAP

Primeiras ocorrencias:

- linha 43: vwap,
- linha 77: vwap,
- linha 110: vwap,

### scripts/auditoria_ui/01_localizar_frentes_pendentes.sh

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 128: header "05_terminal_vwap.txt" "Frente Terminal VWAP"
- linha 129: section "05_terminal_vwap.txt" "Arquivos por nome" "search_files_by_name 'terminal|vwap|estrutura|perna|leg|legs|alert|kpi'"
- linha 130: section "05_terminal_vwap.txt" "Ocorrencias no conteudo" "search_text 'Terminal VWAP|terminal_vwap|VWAP|estrutura|estruturas|perna|pernas|legs|alertas|KPIs|graficos|gráficos'"
- linha 157: section "12_arquivos_python_candidatos.txt" "Python relacionados a UI e frentes pendentes" "search_files_by_name '\\.py$' | grep -Ei 'ui|window|panel|view|model|decision|decis|t...
- linha 189: 9. Seguir para frentes separadas: Terminal VWAP, payoff, UIDataModel e banco.

### scripts/auditoria_ui/02_validar_escopo_branch_atual.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 37: | grep -Ei '(^|/)(services?|repositories?|controllers?|migrations?|pipeline|dados|data|database|db)(/|$)|app\.db|derived\.db|schema|terminal|vwap|payoff|get_payoff_curve|uidatam...
- linha 42: echo "Se aparecer service, repository, controller, banco, pipeline, Terminal VWAP, payoff ou UIDataModel, parar e reclassificar antes de continuar."

### scripts/classificar_areas_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 114: "Terminal VWAP": [
- linha 115: r"\bvwap\b",
- linha 260: "Terminal VWAP",
- linha 378: ### Terminal VWAP
- linha 494: - Terminal VWAP permanece fora do escopo da branch atual;

### scripts/criar_registro_execucao_smoke_decisoes_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 365: - Terminal VWAP permanece fora do escopo desta branch;
- linha 440: - Terminal VWAP fora do escopo da branch atual;

### scripts/criar_smoke_manual_decisoes_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 456: - Terminal VWAP fora do escopo da branch atual;

### scripts/cruzar_matriz_areas_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 111: "Terminal VWAP",
- linha 128: "Terminal VWAP": [
- linha 129: r"\bvwap\b",
- linha 248: if area == "Terminal VWAP":
- linha 457: 4. Terminal VWAP permanece fora do escopo da branch atual.
- linha 494: - Terminal VWAP;
- linha 609: - Terminal VWAP;

### scripts/documentar_matriz_equivalencia_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 80: | Terminal VWAP | Sim | Parcial/indefinido | FORA_ESCOPO | AUDITORIA_REFACTOR_UI.md | Abrir auditoria propria |
- linha 151: - auditar Terminal VWAP separadamente;
- linha 226: - Terminal VWAP permanece fora do escopo da branch de Decisoes;

### scripts/documentar_pendencias_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 124: #### 3. Terminal VWAP, payoff e UIDataModel
- linha 132: - Terminal VWAP;
- linha 197: abrir auditoria propria para Terminal VWAP/payoff/UIDataModel

### scripts/documentar_pendencias_ui_safe.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 153: #### 3. Terminal VWAP, payoff e UIDataModel
- linha 161: - Terminal VWAP;
- linha 226: abrir auditoria propria para Terminal VWAP/payoff/UIDataModel

### scripts/import_rtd_option_quotes_wide_csv.py

Termos encontrados:

- vwap
- VWAP

Primeiras ocorrencias:

- linha 24: "vwap",
- linha 44: "vwap",
- linha 194: "vwap": parse_number(raw.get("vwap")),
- linha 243: "vwap",

### scripts/inventariar_arquivos_ui.sh

Termos encontrados:

- terminal vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 113: "vwap": r"vwap|VWAP",
- linha 240: - referencias a decisoes, payoff, VWAP e tema dark;
- linha 281: 3. Areas Terminal VWAP, payoff curve e UIDataModel exigem auditoria propria.
- linha 391: - Terminal VWAP;

### services/terminal_vwap_payoff_app_service.py

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: """App service do Terminal VWAP Payoff.
- linha 14: class TerminalVWAPPayoffAppService:
- linha 15: """Orquestra a montagem do ViewModel do Terminal VWAP Payoff.
- linha 22: - viewmodel_service: opcional, por padrão usa TerminalVWAPPayoffViewModelService.
- linha 112: from services.terminal_vwap_payoff_viewmodel_service import (
- linha 113: TerminalVWAPPayoffViewModelService,
- linha 116: return TerminalVWAPPayoffViewModelService()
- linha 206: "source": "terminal_vwap_payoff_app_service",
- linha 285: "build_terminal_vwap_payoff_viewmodel",

### services/terminal_vwap_payoff_viewmodel_service.py

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: """ViewModel do Terminal VWAP Payoff.
- linha 3: Este módulo monta um payload puro para a futura UI do Terminal VWAP Payoff.
- linha 18: class TerminalVWAPPayoffViewModelService:
- linha 19: """Monta o ViewModel canônico do Terminal VWAP Payoff."""
- linha 55: "name": "ui-terminal-vwap-payoff",
- linha 64: "source": "terminal_vwap_payoff_viewmodel_service",
- linha 170: vwap = self._to_float(
- linha 173: "vwap",
- linha 174: "VWAP",
- linha 175: "quote_vwap",
- linha 181: if current_price is not None and vwap not in (None, 0):
- linha 182: difference = ((current_price - vwap) / vwap) * 100

### tools/audit_rtd_ui_flow.py

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 343: "UI/components/terminal_vwap_payoff_dark_panel.py",

### tools/fix_structure_side_panel_patch.py

Termos encontrados:

- terminal_vwap
- vwap
- VWAP

Primeiras ocorrencias:

- linha 3: path = Path("UI/components/terminal_vwap_payoff_dark_panel.py")
- linha 11: backup = Path("UI/components/terminal_vwap_payoff_dark_panel.py.bak_side_actions_fix")

### tools/patch_structure_side_panel.py

Termos encontrados:

- vwap
- VWAP

Primeiras ocorrencias:

- linha 673: text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff"

### UI/components/terminal_vwap_payoff_dark_panel.py

Termos encontrados:

- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: # UI/components/terminal_vwap_payoff_dark_panel.py
- linha 4: Painel operacional dark para análise VWAP e Payoff.
- linha 10: - blocos grandes para VWAP e Payoff;
- linha 129: class TerminalVWAPPayoffDarkPanel(ctk.CTkFrame):
- linha 145: self.canvas_vwap: Optional[FigureCanvasTkAgg] = None
- linha 313: text="Selecione uma estrutura no menu lateral para carregar a VWAP e Payoff",
- linha 328: self._create_kpi("vwap", "VWAP", "N/A", 1)
- linha 329: self._create_kpi("diff", "Preço vs VWAP", "N/A", 2)
- linha 335: self.frame_vwap = ctk.CTkFrame(
- linha 340: self.frame_vwap.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=5)
- linha 768: "vwap": None,
- linha 781: "vwap_source": None,

### UI/components/terminal_vwap_payoff_panel.py

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 1: # UI/components/terminal_vwap_payoff_panel.py
- linha 3: Painel nativo Tkinter do Terminal VWAP Payoff.
- linha 10: -> TerminalVWAPPayoffPanel
- linha 11: -> TerminalVWAPPayoffController
- linha 12: -> TerminalVWAPPayoffAppService
- linha 14: -> TerminalVWAPPayoffViewModelService
- linha 134: "vwap": _format_number_br(market.get("vwap"), 2),
- linha 135: "price_vs_vwap_percent": _format_percent_br(
- linha 136: market.get("price_vs_vwap_percent"),
- linha 151: class TerminalVWAPPayoffPanel(ttk.Frame):
- linha 152: """Aba nativa do Terminal VWAP Payoff na UI principal."""
- linha 191: self._status_var = tk.StringVar(value="Terminal VWAP Payoff pronto")

### UI/main_window.py

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 14: from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel
- linha 115: self._setup_terminal_vwap_payoff_tab(right_notebook)
- linha 698: def _setup_terminal_vwap_payoff_tab(self, notebook: ttk.Notebook):
- linha 699: """Adiciona o Terminal VWAP Payoff como aba nativa da UI principal."""
- linha 702: notebook.add(terminal_frame, text="Terminal VWAP Payoff")
- linha 706: from services.terminal_vwap_payoff_app_service import (
- linha 707: TerminalVWAPPayoffAppService,
- linha 709: from controllers.terminal_vwap_payoff_controller import (
- linha 710: TerminalVWAPPayoffController,
- linha 721: app_service = TerminalVWAPPayoffAppService(
- linha 724: controller = TerminalVWAPPayoffController(app_service)
- linha 726: self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel(

### UI/modern/dark_window.py

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 6: Ele abre diretamente o TerminalVWAPPayoffDarkPanel, que corresponde
- linha 20: from UI.components.terminal_vwap_payoff_dark_panel import TerminalVWAPPayoffDarkPanel
- linha 39: self.root.title("Terminal de Análise Avançada - VWAP & Opções")
- linha 76: terminal_tab = self.tabs.add("Terminal VWAP")
- linha 79: self.panel = TerminalVWAPPayoffDarkPanel(
- linha 122: Fornece as estruturas carregadas no Terminal VWAP para a aba Decisões.
- linha 138: Carrega no Terminal VWAP a estrutura associada a uma decisão selecionada.
- linha 158: self.set_status(f"Estrutura {structure_id} não encontrada no Terminal VWAP")
- linha 161: f"Estrutura {structure_id} não foi encontrada na lista do Terminal VWAP.",
- linha 169: self.tabs.set("Terminal VWAP")

### UI/modern/main_window.py

Termos encontrados:

- terminal vwap
- terminal_vwap
- vwap
- TerminalVWAP
- VWAP

Primeiras ocorrencias:

- linha 269: notebook.add(tab, text="Terminal VWAP Payoff")
- linha 272: from controllers.terminal_vwap_payoff_controller import (
- linha 273: TerminalVWAPPayoffController,
- linha 276: from services.terminal_vwap_payoff_app_service import (
- linha 277: TerminalVWAPPayoffAppService,
- linha 279: from UI.components.terminal_vwap_payoff_panel import TerminalVWAPPayoffPanel
- linha 282: app_service = TerminalVWAPPayoffAppService(
- linha 285: controller = TerminalVWAPPayoffController(app_service)
- linha 287: self.terminal_vwap_payoff_panel = TerminalVWAPPayoffPanel(
- linha 292: self.terminal_vwap_payoff_panel.pack(
- linha 303: "Terminal VWAP Payoff indisponível neste shell.\n\n"

## 9. Leitura inicial da auditoria

Resultado inicial:

    Inventario textual criado sem alteracao funcional.

Classificacao:

    REGRESSAO_UI

Proxima acao recomendada:

    Identificar o componente principal do Terminal VWAP e montar roteiro de smoke manual especifico.

<!-- CLASSIFICACAO_ESTRUTURAL_TERMINAL_VWAP_2026_07_06 -->

## 10. Classificacao estrutural inicial do Terminal VWAP

Data: 2026-07-06

Metodo:

    Busca textual local em arquivos reais, seguida de classificacao por caminho, score e leitura estrutural de Python via AST.

Resultado:

    Arquivos relacionados encontrados fora da propria auditoria: 57
    Arquivos de componentes UI encontrados: 2
    Arquivos de modelo UI encontrados: 0

### 10.1. Componente principal provavel

Arquivo:

    UI/components/terminal_vwap_payoff_dark_panel.py

Classificacao:

    UI_COMPONENT

Justificativa:

    Arquivo em UI/components com maior aderencia textual ao Terminal VWAP.

Classes encontradas no componente principal:

- linha 129: TerminalVWAPPayoffDarkPanel

Funcoes e metodos encontrados no componente principal:

- linha 59: _q
- linha 63: _norm
- linha 67: _first_col
- linha 75: _to_float
- linha 99: _money
- linha 106: _number
- linha 122: decision_label
- linha 130: __init__
- linha 155: _setup_style
- linha 182: _setup_layout
- linha 195: _configure_layout_grid
- linha 201: _build_rail_panel
- linha 209: _build_rail_container
- linha 219: _build_rail_toggle_button
- linha 233: _build_rail_reload_button
- linha 247: _build_rail_new_button
- linha 261: _build_rail_actions_button
- linha 275: _build_rail_open_button
- linha 290: _build_side_panel
- linha 300: _build_main_panel
- linha 310: _build_main_header
- linha 319: _build_kpi_panel
- linha 334: _build_chart_panels
- linha 349: _build_bottom_panel
- linha 376: _build_legs_table
- linha 412: _build_alerts_box
- linha 423: _create_kpi
- linha 449: toggle_structures_panel
- linha 460: reload_structures
- linha 465: _connect
- linha 473: _tables_cols
- linha 485: _find_structures_table
- linha 505: _load_structures
- linha 545: _render_structures_list
- linha 558: _render_structures_list_actions
- linha 570: _render_structures_list_header
- linha 589: _build_structures_scroll
- linha 597: _render_empty_structures_message
- linha 606: _render_structure_list_item
- linha 624: select_structure
- linha 655: _find_legs_table
- linha 676: _load_legs
- linha 700: _load_legs_schema
- linha 705: _resolve_legs_columns
- linha 719: _build_legs_select_parts
- linha 731: _fetch_legs_rows
- linha 746: _load_market
- linha 765: _empty_market_result
- linha 784: _normalize_market_asset
- linha 790: _build_market_query
- linha 817: _market_column_map
- linha 850: _market_select_parts
- linha 872: _market_order_sql
- linha 885: _market_result_from_rows
- linha 918: _market_series_from_rows
- linha 937: _load_payoff_points
- linha 947: _load_persisted_payoff_points
- linha 981: _calculate_payoff_from_legs
- linha 990: _collect_payoff_strikes
- linha 994: _calculate_payoff_spot_range
- linha 1002: _calculate_payoff_points_for_range
- linha 1022: _calculate_leg_payoff
- linha 1043: _is_short_payoff_leg
- linha 1051: _breakevens
- linha 1074: _update_kpis
- linha 1114: _render_legs
- linha 1134: _set_alerts
- linha 1141: _render_alerts
- linha 1163: _clear_canvas
- linha 1172: _figure
- linha 1183: _render_empty_charts
- linha 1187: _render_charts
- linha 1196: _render_vwap_chart
- linha 1201: _render_vwap_chart_stage_1
- linha 1208: _render_vwap_chart_stage_2
- linha 1246: _render_vwap_chart_stage_3
- linha 1256: _render_payoff_chart
- linha 1295: _build_payoff_export_button
- linha 1315: export_payoff_png
- linha 1354: _safe_status
- demais metodos omitidos nesta visao: 54

Imports observados no componente principal:

- UI.components.structure_editor_dialog
- __future__
- customtkinter
- math
- matplotlib.backends.backend_tkagg
- matplotlib.figure
- pathlib
- repositories.structures_repository
- sqlite3
- tkinter
- typing

### 10.2. Arquivos UI candidatos

- UI/components/terminal_vwap_payoff_dark_panel.py | categoria: UI_COMPONENT | score: 1622 | ocorrencias: 122
- UI/components/terminal_vwap_payoff_panel.py | categoria: UI_COMPONENT | score: 1554 | ocorrencias: 54
- UI/main_window.py | categoria: UI | score: 348 | ocorrencias: 48
- UI/modern/main_window.py | categoria: UI | score: 339 | ocorrencias: 39
- UI/modern/dark_window.py | categoria: UI | score: 332 | ocorrencias: 32

### 10.3. Documentos e reports relacionados

- docs/ui_terminal_vwap_payoff_plano.md | categoria: DOCUMENTACAO | score: 686 | ocorrencias: 186
- docs/auditoria_ui_terminal_vwap_payoff.md | categoria: DOCUMENTACAO | score: 684 | ocorrencias: 184
- docs/MATRIZ_CRUZADA_AREAS_UI.md | categoria: DOCUMENTACAO | score: 342 | ocorrencias: 342
- docs/CLASSIFICACAO_AREAS_UI.md | categoria: DOCUMENTACAO | score: 210 | ocorrencias: 210
- docs/INVENTARIO_ARQUIVOS_UI.md | categoria: DOCUMENTACAO | score: 162 | ocorrencias: 162
- reports/auditoria/UI_PENDENCIAS_REMANESCENTES.md | categoria: REPORT_HISTORICO | score: 42 | ocorrencias: 42
- reports/auditoria/UI_FRENTES_ENCERRADAS.md | categoria: REPORT_HISTORICO | score: 21 | ocorrencias: 21
- docs/DESENVOLVIMENTO_UI.md | categoria: DOCUMENTACAO | score: 9 | ocorrencias: 9
- docs/MATRIZ_EQUIVALENCIA_UI.md | categoria: DOCUMENTACAO | score: 6 | ocorrencias: 6
- docs/REGISTRO_EXECUCAO_SMOKE_DECISOES_UI.md | categoria: DOCUMENTACAO | score: 6 | ocorrencias: 6

## 11. Separacao inicial de responsabilidades

### 11.1. Area UI

Arquivos classificados como UI ou componente UI devem ser tratados apenas para validacao visual e operacional nesta fase.

Permitido:

- observar renderizacao do Terminal VWAP;
- observar navegacao;
- observar mensagens de status;
- observar acoes disponiveis;
- registrar falhas visuais ou operacionais;
- preparar smoke manual.

Nao permitido nesta etapa:

- alterar comportamento funcional;
- alterar banco;
- alterar pipeline;
- alterar regra de negocio;
- alterar services, repositories ou controllers.

### 11.2. Area de dados

Qualquer dependencia de dados deve ser registrada como observacao.
Se a validacao exigir alteracao de banco, schema, pipeline, service, repository ou controller, a acao deve parar e ser reclassificada.

### 11.3. Payoff

Se o Terminal VWAP depender visualmente de payoff, a observacao pode ser registrada.
Correcoes de payoff devem permanecer fora desta frente, salvo comportamento ja validado e estritamente necessario para smoke observacional.

## 12. Roteiro minimo de smoke manual Terminal VWAP

Classificacao:

    REGRESSAO_UI

Tipo de validacao:

    smoke manual observacional

Pre-condicoes:

- branch audit/terminal-vwap-ui ativa;
- arvore Git limpa;
- UI aberta pelo caminho atual do projeto;
- nenhuma alteracao em banco, schema, pipeline, services, repositories ou controllers.

Checklist:

1. Abrir a UI pelo entrypoint atual do projeto.
2. Confirmar que a UI atual continua sendo o caminho principal.
3. Acessar a area ou painel Terminal VWAP.
4. Confirmar carregamento inicial sem excecao visivel.
5. Validar presenca de estruturas quando houver dados.
6. Validar comportamento quando nao houver estrutura selecionada.
7. Validar fluxo de selecao de estrutura.
8. Validar exibicao de pernas associadas quando aplicavel.
9. Validar comportamento sem pernas associadas.
10. Validar alertas visiveis quando aplicavel.
11. Validar KPIs visiveis quando aplicavel.
12. Validar graficos visiveis quando aplicavel.
13. Validar estados vazios.
14. Validar mensagens de status.
15. Validar botoes e acoes operacionais sem selecao.
16. Validar botoes e acoes operacionais com selecao.
17. Validar navegacao de ida e volta entre Decisoes e Terminal VWAP, se existir carregamento associado.
18. Validar dark mode sem quebra visual evidente.
19. Registrar evidencias minimas.
20. Registrar pendencias encontradas sem aplicar patch imediato.

Resultado esperado para encerramento desta etapa:

    Roteiro de smoke definido e pronto para execucao manual controlada.

## 13. Decisao de continuidade

A auditoria estrutural inicial nao autoriza patch funcional amplo.

Proxima acao autorizada:

    Executar smoke manual observacional do Terminal VWAP e registrar evidencia neste documento ou em documento de controle ja existente, sem criar nova frente desnecessaria.

Criterio para parar:

    Se a validacao exigir alteracao de banco, pipeline, regra de negocio, services, repositories ou controllers, parar e reclassificar antes de qualquer patch.

<!-- PREPARACAO_SMOKE_TERMINAL_VWAP_2026_07_06 -->

## 14. Preparacao do smoke manual Terminal VWAP

Data: 2026-07-06

Documento de roteiro:

    docs/SMOKE_MANUAL_TERMINAL_VWAP_UI.md

Documento de registro de execucao:

    docs/REGISTRO_EXECUCAO_SMOKE_TERMINAL_VWAP_UI.md

Commit base:

    a19cbf1

Status:

    PENDENTE_EXECUCAO_MANUAL

Componente principal provavel:

    UI/components/terminal_vwap_payoff_dark_panel.py

Decisao:

    Smoke manual observacional preparado. Proxima acao autorizada e abrir a UI pelo caminho atual do projeto e preencher o registro de execucao.

<!-- CONCLUSAO_VALIDACAO_MINIMA_TERMINAL_VWAP_2026_07_06 -->

## 15. Conclusao da validacao minima Terminal VWAP

Data: 2026-07-06

Horario de conclusao:

    2026-07-06 21:51:31

Branch:

    audit/terminal-vwap-ui

Commit base validado:

    76f07d5

Resultado:

    APROVADO_COM_RESSALVA_OPERACIONAL

Status:

    CONCLUIDO_VALIDACAO_MINIMA

Registro atualizado:

    docs/REGISTRO_EXECUCAO_SMOKE_TERMINAL_VWAP_UI.md

Relato do operador:

    Sistema abriu normalmente, sem alteracao e sem problema visivel observado.

Ressalva:

    Nao houve smoke manual detalhado item a item. Esta conclusao registra validacao operacional minima de abertura da UI.

Decisao:

    Frente Terminal VWAP UI concluida nesta etapa de auditoria e controle, sem patch funcional.

Garantia de escopo:

    Nao houve alteracao em banco, schema, pipeline, regra de negocio, services, repositories, controllers ou entrypoint principal.
