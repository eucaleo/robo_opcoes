# Auditoria Payoff UI

Data de abertura:

    2026-07-06 22:05:58

Branch:

    audit/payoff-ui

Commit base:

    ef7d17d

Status:

    ABERTO

Classificacao:

    FORA_ESCOPO_BRANCH_DECISOES_DARK

Tipo de frente:

    AUDITORIA_PROPRIA_PAYOFF

## 1. Objetivo

Abrir frente propria para Payoff UI, iniciando por auditoria documental e inventario dos arquivos reais relacionados.

A etapa inicial nao autoriza correcao funcional, refatoracao ampla ou mudanca em contratos de dados.

## 2. Escopo inicial permitido

- consistencia da curva de payoff
- comparacao de curvas
- Curva A
- exportacao PNG relacionada a payoff
- contratos de payoff
- formulas e dados de entrada
- pontos de entrada usados pela UI
- dependencias com UIDataModel apenas para mapeamento

## 3. Escopos proibidos nesta etapa

- alterar banco
- alterar schema
- alterar pipeline
- alterar regra de negocio
- alterar services
- alterar repositories
- alterar controllers
- trocar entrypoint principal
- mexer em Terminal VWAP
- mexer em Decisoes dark panel
- declarar equivalencia global da UI

## 4. Arquivos inventariados inicialmente

- ATT/tests/test_payoff_canonical.py
- ATT/tests/test_payoff_chart.py
- ATT/tests/test_terminal_vwap_payoff_app_service.py
- ATT/tests/test_terminal_vwap_payoff_controller.py
- ATT/tests/test_terminal_vwap_payoff_panel.py
- ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py
- UI/components/payoff_chart.py
- UI/components/terminal_vwap_payoff_dark_panel.py
- UI/components/terminal_vwap_payoff_panel.py
- controllers/terminal_vwap_payoff_controller.py
- create_payoff_summary_table.py
- db/migrations/add_structure_id_to_payoff_curve_points.py
- docs/auditoria_ui_terminal_vwap_payoff.md
- docs/checkpoints/evidencias/fase-1-mapa-payoff-codigo-atual.txt
- docs/checkpoints/evidencias/fase-1-mapa-payoff-runtime-codigo-atual.txt
- docs/checkpoints/evidencias/fase-1-trechos-payoff-decisoes-runtime.txt
- docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md
- docs/ui_terminal_vwap_payoff_plano.md
- domain/payoff.py
- domain/payoff_features.py
- services/derived_payoff_persistence.py
- services/payoff_persistence_port.py
- services/terminal_vwap_payoff_app_service.py
- services/terminal_vwap_payoff_viewmodel_service.py

## 5. Pendencias iniciais de auditoria

- revisar arquivos inventariados
- separar UI, calculo, exportacao e origem de dados
- confirmar se ha dependencia real de UIDataModel
- identificar se a curva exibida usa dados canonicos
- identificar criterios minimos de smoke manual
- registrar decisoes sem alterar funcionalidade

## 6. Criterio de continuidade

A frente so deve avancar para ajuste funcional se houver falha reproduzivel, escopo delimitado e validacao definida.

Na duvida, manter como pendencia ou backlog.

## 7. Decisao de abertura

A frente Payoff UI fica aberta para auditoria propria.

Resultado desta etapa:

    AUDITORIA_ABERTA_SEM_PATCH_FUNCIONAL

Documento de inventario relacionado:

    docs/INVENTARIO_PAYOFF_UI.md

Documento de smoke preparado:

    docs/REGISTRO_EXECUCAO_SMOKE_PAYOFF_UI.md
