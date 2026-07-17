# Relatorio 32.11 - Auditoria quarentena scripts paralelos de payoff

Status: warning

Objetivo

Auditar o script paralelo de payoff e confirmar se ele esta isolado do fluxo oficial.

Arquivo auditado

- scripts/recalculate_payoff_curve_points_once.py

Checks

- target_exists: True
- has_maintenance_header: True
- mentions_not_official_flow: True
- mentions_payoff_refresh_command_service: True
- reads_structure_legs: False
- reads_rtd_option_quotes: False
- reads_rtd_underlying_quotes: False
- mentions_payoff_curve_points: True
- mentions_structure_decisions: False
- has_active_guard: True

Referencias na UI

- Total encontradas: 2
- Chamadas diretas ao script paralelo: 0
- Uso de subprocess ou os.system na UI: 2

Ocorrencias principais

- UI/main_window.py:404 | subprocess.run | res = subprocess.run(
- UI/main_window.py:462 | subprocess.run | res = subprocess.run(

Conclusao

Script paralelo deve permanecer fora do fluxo oficial. Fluxo oficial: UI -> PayoffRefreshCommandService -> PricingExecutionAppService.

Proxima etapa recomendada

1. Se nao houver cabecalho de quarentena, aplicar patch 32.11.
2. Confirmar que a UI nao chama script paralelo.
3. Avancar para auditoria 32.12 da UI antes de qualquer limpeza.
