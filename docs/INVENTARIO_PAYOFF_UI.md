# Inventario Payoff UI

Data de abertura:

    2026-07-06

Branch:

    audit/payoff-ui

Classificacao:

    FORA_ESCOPO_BRANCH_DECISOES_DARK

Tipo:

    AUDITORIA_DOCUMENTAL_E_INVENTARIO

## 1. Objetivo

Inventariar arquivos e referencias relacionadas a Payoff UI antes de qualquer alteracao funcional.

Esta etapa nao altera banco, schema, pipeline, regra de negocio, services, repositories, controllers ou entrypoint principal.

## 2. Termos pesquisados

- payoff
- curve
- curva
- curvaa
- curva_a
- png
- export

## 3. Arquivos encontrados

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

## 4. Observacao de controle

Este inventario e ponto de partida. A classificacao final depende da revisao dos arquivos reais encontrados.

Nao houve alteracao funcional nesta etapa.
