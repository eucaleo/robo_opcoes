# Relatorio 32.12 - Auditoria UI escopo payoff local

Status: error

Objetivo

Auditar a UI para localizar calculo local de payoff, fallback e chamadas proibidas.

Checks

- ui_root_exists: True
- terminal_panel_exists: True
- local_calc_hits_count: 9
- hard_forbidden_hits_count: 2
- sql_forbidden_hits_count: 1
- terminal_calculate_payoff_points_for_range_occurrences: 2
- execute_pricing_direct_in_ui: False
- direct_sql_write_payoff_in_ui: True

Resumo

- Ocorrencias de calculo local: 9
- Ocorrencias proibidas fortes: 2
- Escrita SQL proibida na UI: 1
- Ocorrencias de _calculate_payoff_points_for_range no painel terminal: 2

Calculo local ou fallback encontrado

- UI/components/terminal_vwap_payoff_dark_panel.py:1249 | _calculate_payoff_from_legs | def _calculate_payoff_from_legs(self, legs: List[Dict[str, Any]]) -> List[Dict[str, float]]:
- UI/components/terminal_vwap_payoff_dark_panel.py:1250 | _collect_payoff_strikes | strikes = self._collect_payoff_strikes(legs)
- UI/components/terminal_vwap_payoff_dark_panel.py:1255 | _calculate_payoff_spot_range | x_min, x_max = self._calculate_payoff_spot_range(strikes)
- UI/components/terminal_vwap_payoff_dark_panel.py:1256 | _calculate_payoff_points_for_range | return self._calculate_payoff_points_for_range(legs, x_min, x_max)
- UI/components/terminal_vwap_payoff_dark_panel.py:1258 | _collect_payoff_strikes | def _collect_payoff_strikes(self, legs: List[Dict[str, Any]]) -> List[float]:
- UI/components/terminal_vwap_payoff_dark_panel.py:1262 | _calculate_payoff_spot_range | def _calculate_payoff_spot_range(self, strikes: List[float]) -> tuple[float, float]:
- UI/components/terminal_vwap_payoff_dark_panel.py:1270 | _calculate_payoff_points_for_range | def _calculate_payoff_points_for_range(
- UI/components/terminal_vwap_payoff_dark_panel.py:1284 | _calculate_leg_payoff | total += self._calculate_leg_payoff(leg, spot)
- UI/components/terminal_vwap_payoff_dark_panel.py:1290 | _calculate_leg_payoff | def _calculate_leg_payoff(self, leg: Dict[str, Any], spot: float) -> float:

Chamadas proibidas fortes encontradas

- UI/main_window.py:404 | subprocess.run | res = subprocess.run(
- UI/main_window.py:462 | subprocess.run | res = subprocess.run(

Escrita SQL proibida encontrada

- UI/components/terminal_vwap_payoff_dark_panel.py:1937 | insert\s+into\s+structure_decisions | INSERT INTO structure_decisions (

Conclusao

A UI deve apenas chamar o comando oficial para recalcular e depois reler snapshot persistido. Calculo local e fallback devem ser removidos ou bloqueados em etapa posterior.

Proxima etapa recomendada

1. Se houver somente warning por calculo local, preparar patch de bloqueio da UI.
2. Se houver error por execute_pricing, subprocess ou SQL de escrita, corrigir antes de prosseguir.
3. Nao criar motor novo e nao alterar backend validado sem nova evidencia.
