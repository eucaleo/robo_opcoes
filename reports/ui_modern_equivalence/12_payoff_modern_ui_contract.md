# Contrato da Payoff UI moderna

Data: 2026-07-07

Branch: feat/payoff-modern-ui-next

## 1. Classificacao

Frente propria de Payoff.

Esta alteracao deriva da pendencia registrada como Payoff fora do escopo da branch Decisoes dark panel.

## 2. Objetivo

Registrar contrato minimo automatizado para confirmar que a UI moderna expoe Payoff em modo paralelo e opt-in, sem promover substituicao da UI atual.

## 3. Escopo validado

O teste automatizado valida:

- o launcher moderno continua roteando modos explicitamente;
- o modo dark aponta para UI.modern.dark_window;
- o modo shell aponta para UI.modern.main_window;
- o modo dark expoe TerminalVWAPPayoffDarkPanel;
- o modo shell expoe PayoffChart;
- o carregamento de curva usa contrato existente get_payoff_curve_info;
- a UI moderna permanece declarada como paralela;
- a UI antiga permanece preservada;
- nao ha declaracao de equivalencia completa da UI moderna.

## 4. Escopos nao alterados

Nao foi alterado:

- banco de dados;
- schema;
- regra de negocio;
- services;
- repositories;
- controllers;
- pipeline;
- entrypoint principal legado;
- comportamento operacional do Terminal VWAP;
- calculo canonico de payoff.

## 5. Evidencia automatizada

Teste criado:

- ATT/tests/test_payoff_modern_ui_contract.py

Validacao executavel recomendada:

- python -m pytest ATT/tests/test_payoff_modern_ui_contract.py
- python -m pytest ATT/tests/test_payoff_canonical.py ATT/tests/test_payoff_chart.py
- git diff --check

## 6. Decisao

A Payoff UI moderna permanece como caminho paralelo e controlado.

Este contrato nao encerra a frente UI global e nao declara equivalencia completa da UI moderna.
