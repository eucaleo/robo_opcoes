#!/usr/bin/env bash
set -euo pipefail

FILE="UI/components/details_panel.py"

echo "== Showing timestamp-related functions in $FILE =="
rg -n "def _get_latest_snapshot_timestamp_for_aba|MAX\(timestamp\)|robo_legs_snapshot|robo_snapshot|rtd_analise_robo_legs|manual_analise_robo_legs" "$FILE" -n

echo
echo "== Context (function body) =="
python - <<'PY'
import re
from pathlib import Path

p = Path("UI/components/details_panel.py")
s = p.read_text(encoding="utf-8", errors="replace").splitlines()

targets = [i for i,l in enumerate(s) if re.search(r"def _get_latest_snapshot_timestamp_for_aba", l)]
if not targets:
    print("Function not found")
    raise SystemExit(1)

start = targets[0]
# print ~120 lines from start (good enough to capture both defs if duplicated)
for i in range(start, min(start+140, len(s))):
    print(f"{i+1:4d}: {s[i]}")
PY
