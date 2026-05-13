#!/usr/bin/env python3
import os
import re
import json
from _scan_utils_v2 import iter_files


# captura: from/join/into/update + opcional schema + tabela
TABLE_RE = re.compile(r'(?i)\b(from|join|into|update)\s+([a-zA-Z0-9_\.]+)')

tables = {}
for f in iter_files(".", (".py",)):
    rel = os.path.relpath(f)
    lines = open(f, encoding="utf-8", errors="ignore").read().splitlines()
    found = []
    for i, line in enumerate(lines, start=1):
        for m in TABLE_RE.finditer(line):
            found.append([i, m.group(1).lower(), m.group(2)])
    if found:
        tables[rel] = found

os.makedirs("ATT/reports", exist_ok=True)
with open("ATT/reports/sql_report_v2.json", "w", encoding="utf-8") as out:
    json.dump(tables, out, indent=2, ensure_ascii=False)

print("[analyze_sql_usage_v2] OK (filtered) - wrote ATT/reports/sql_report_v2.json")
