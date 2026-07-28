#!/usr/bin/env bash
set -euo pipefail

mkdir -p tools/reports

echo "== Auditoria UI Payoff Bridge ==" > tools/reports/payoff_ui_bridge_audit.txt
echo "" >> tools/reports/payoff_ui_bridge_audit.txt

echo "## Botões / command=" >> tools/reports/payoff_ui_bridge_audit.txt
grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
  "command=.*recalc\|command=.*refresh\|command=.*payoff\|command=.*load\|command=.*update\|command=.*reload" \
  UI services app core 2>/dev/null >> tools/reports/payoff_ui_bridge_audit.txt || true

echo "" >> tools/reports/payoff_ui_bridge_audit.txt
echo "## Textos de botões relevantes" >> tools/reports/payoff_ui_bridge_audit.txt
grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
  "Recalcular\|Recalculo\|recalcular\|Atualizar payoff\|Atualizar\|payoff" \
  UI services app core 2>/dev/null >> tools/reports/payoff_ui_bridge_audit.txt || true

echo "" >> tools/reports/payoff_ui_bridge_audit.txt
echo "## Serviço oficial / PayoffRefreshCommandService" >> tools/reports/payoff_ui_bridge_audit.txt
grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
  "PayoffRefreshCommandService\|RefreshCommand\|recalculate_selected_structure\|_on_recalculate_cb\|on_recalculate" \
  . 2>/dev/null >> tools/reports/payoff_ui_bridge_audit.txt || true

echo "" >> tools/reports/payoff_ui_bridge_audit.txt
echo "## Possíveis cálculos indevidos dentro da UI" >> tools/reports/payoff_ui_bridge_audit.txt
grep -RIn --exclude-dir=.git --exclude-dir=__pycache__ \
  "calcula\|calcular\|estimated\|estimad\|fallback\|breakeven\|_breakevens\|point_pl\|point_spot" \
  UI 2>/dev/null >> tools/reports/payoff_ui_bridge_audit.txt || true

echo "" >> tools/reports/payoff_ui_bridge_audit.txt
echo "Relatório gerado em tools/reports/payoff_ui_bridge_audit.txt"
