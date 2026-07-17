# Relatorio 32.13 - Patch bloqueio calculo local de payoff na UI

Status: ok

Objetivo

Bloquear metodos locais de calculo de payoff na UI com RuntimeError explicito.

Arquivo alvo

- C:\users\eucal\projeto\UI\components\terminal_vwap_payoff_dark_panel.py

Backup

- C:\users\eucal\projeto\UI\components\terminal_vwap_payoff_dark_panel.py.bak_32_13_20260717_203810

Metodos alterados

- _calculate_leg_payoff linhas 1290 a 1309
- _calculate_payoff_points_for_range linhas 1270 a 1288
- _calculate_payoff_spot_range linhas 1262 a 1268
- _collect_payoff_strikes linhas 1258 a 1260
- _calculate_payoff_from_legs linhas 1249 a 1256

Conclusao

Metodos locais de calculo de payoff foram bloqueados por erro explicito.

