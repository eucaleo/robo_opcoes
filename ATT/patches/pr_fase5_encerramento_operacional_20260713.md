# Encerramento operacional da Fase 5 - RTD Excel BTG Online

## Resumo

Esta PR consolida a evolução da frente RTD Excel BTG Online até o encerramento operacional da Fase 5, com UI operacional em tempo real integrada ao fluxo RTD, snapshot, histórico intraday e candles.

Arquitetura preservada:

    Corretora / RTD -> Excel LISTA_RTD.xlsm aberto -> Coletor Python online -> Snapshot SQLite -> Histórico Intraday -> Candles -> UI / Estruturas / Alertas

## Escopo validado

    - Integração da UI dark e terminal VWAP/payoff.
    - Consumo de snapshot RTD centralizado.
    - Enriquecimento de legs sem subprocesso individual.
    - Consumo de candles intraday pela UI.
    - Status operacional.
    - Menu Ajuda com Status RTD Excel.
    - Teste operacional real com Excel/RTD ativo via COM.
    - Validação integrada das fases anteriores relacionadas.

## Evidências de teste

### Suite focada da Fase 5

Comando executado:

    python -m pytest ATT/tests/test_rtd_option_quotes_sync_service.py \
      ATT/tests/test_structure_leg_rtd_enrichment_service.py \
      ATT/tests/test_terminal_vwap_payoff_app_service.py \
      ATT/tests/test_terminal_vwap_payoff_dark_panel_app_service_integration.py \
      ATT/tests/test_ui_modern_dark_window_terminal_vwap_wiring.py \
      ATT/tests/test_ui_modern_dark_window_operational_data_status_menu.py \
      ATT/tests/test_operational_data_status_service.py \
      ATT/tests/test_ui_intraday_candle_chart_consumption.py

Resultado:

    51 passed in 3.24s

### Teste operacional real Excel/RTD

Comando executado:

    python -m pytest ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py -vv

Resultado:

    ATT/tests/test_ui_modern_dark_window_excel_rtd_status_menu.py::test_operational_dark_window_help_menu_and_live_excel_rtd_status PASSED
    1 passed in 5.07s

### Suite ampliada integrada

Comando executado:

    python -m pytest ATT/tests -k "rtd or snapshot or intraday or candle or terminal_vwap or operational_data_status"

Resultado:

    245 passed, 564 deselected in 11.25s

## Status das fases

    Fase 1: encerrada
    Fase 2: encerrada
    Fase 3: encerrada
    Fase 4: encerrada
    Fase 5: encerrada operacionalmente nesta PR
    Fase 6: próxima fase permitida
    Fase 7: não encerrada; permanece como antecipação técnica ou documental quando aplicável

## Observações

    - Artefatos de Fase 6 ou Fase 7 não devem ser interpretados como encerramento dessas fases.
    - A execução automática de ordens reais permanece fora do escopo desta frente.
    - A aba RTD_OPTION_QUOTES permanece como mecanismo auxiliar/controlado, não como arquitetura principal contínua.
    - O SQLite permanece como fonte oficial de persistência.
