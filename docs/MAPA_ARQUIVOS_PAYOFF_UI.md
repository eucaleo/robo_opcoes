# Mapa de arquivos Payoff UI

Data de geracao:

    2026-07-06 22:10:24

Branch:

    audit/payoff-ui

Commit de referencia:

    85e455b

Status:

    MAPA_INICIAL_CLASSIFICADO

## 1. Objetivo

Classificar os arquivos inventariados da frente Payoff UI antes de qualquer alteracao funcional.

Esta etapa e documental e nao altera comportamento do sistema.

## 2. Resumo por categoria

- UI: 3
- TESTE: 6
- CONTROLLER: 1
- SERVICE: 4
- DOMAIN: 2
- BANCO_MIGRATION: 1
- DOCUMENTACAO: 6
- SCRIPT_PYTHON: 1
- OUTRO: 0

Total classificado: 24

## 3. Classificacao detalhada

### 3.1. UI

Regra de escopo:

    Pode ser revisado nesta frente, mas alteracao visual ou funcional exige falha reproduzivel e validacao definida.

Arquivos:

- UI/components/payoff_chart.py
- UI/components/terminal_vwap_payoff_dark_panel.py
- UI/components/terminal_vwap_payoff_panel.py

### 3.2. TESTE

Regra de escopo:

    Pode orientar smoke e regressao, mas nao deve expandir escopo sem decisao documental.

Arquivos:

- ATT/tests/test_payoff_canonical.py
- ATT/tests/test_payoff_chart.py
- ATT/tests/test_terminal_vwap_payoff_app_service.py
- ATT/tests/test_terminal_vwap_payoff_controller.py
- ATT/tests/test_terminal_vwap_payoff_panel.py
- ATT/tests/test_terminal_vwap_payoff_viewmodel_service.py

### 3.3. CONTROLLER

Regra de escopo:

    Somente mapear nesta etapa. Alteracao proibida sem reclassificacao.

Arquivos:

- controllers/terminal_vwap_payoff_controller.py

### 3.4. SERVICE

Regra de escopo:

    Somente mapear nesta etapa. Alteracao proibida sem reclassificacao.

Arquivos:

- services/derived_payoff_persistence.py
- services/payoff_persistence_port.py
- services/terminal_vwap_payoff_app_service.py
- services/terminal_vwap_payoff_viewmodel_service.py

### 3.5. DOMAIN

Regra de escopo:

    Somente mapear nesta etapa. Alteracao proibida sem reclassificacao.

Arquivos:

- domain/payoff.py
- domain/payoff_features.py

### 3.6. BANCO_MIGRATION

Regra de escopo:

    Fora do escopo desta etapa. Nao alterar banco, schema ou migration.

Arquivos:

- db/migrations/add_structure_id_to_payoff_curve_points.py

### 3.7. DOCUMENTACAO

Regra de escopo:

    Pode ser atualizada para controle de auditoria.

Arquivos:

- docs/auditoria_ui_terminal_vwap_payoff.md
- docs/checkpoints/evidencias/fase-1-mapa-payoff-codigo-atual.txt
- docs/checkpoints/evidencias/fase-1-mapa-payoff-runtime-codigo-atual.txt
- docs/checkpoints/evidencias/fase-1-trechos-payoff-decisoes-runtime.txt
- docs/evolucoes de fases/EVOLUCAO_PRICING_PAYOFF.md
- docs/ui_terminal_vwap_payoff_plano.md

### 3.8. SCRIPT_PYTHON

Regra de escopo:

    Somente mapear nesta etapa. Alteracao exige escopo delimitado.

Arquivos:

- create_payoff_summary_table.py

### 3.9. OUTRO

Regra de escopo:

    Revisar manualmente antes de qualquer decisao.

Arquivos:

Nenhum arquivo nesta categoria.

## 4. Leitura inicial de risco

A frente Payoff UI possui dependencias que atravessam UI, testes, dominio, services, controller, scripts e banco.

Por isso, a etapa atual deve permanecer como auditoria e classificacao.

Qualquer ajuste fora de UI ou documentacao deve parar e ser reclassificado antes de implementacao.

## 5. Proxima decisao recomendada

Revisar primeiro os arquivos de UI e testes para montar checklist de smoke manual.

Nao alterar services, controllers, domain, migration, banco ou pipeline nesta fase.

Resultado desta etapa:

    MAPA_PAYOFF_UI_GERADO_SEM_PATCH_FUNCIONAL
