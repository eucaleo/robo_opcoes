#!/usr/bin/env python3
import os
import re
import json
from _scan_utils_v2 import iter_files


cli = {}
for f in iter_files(".", (".py",)):
    rel = os.path.relpath(f)
    txt = open(f, encoding="utf-8", errors="ignore").read()
    args = re.findall(r'add_argument\(\s*[\'"]([^\'"]+)[\'"]', txt)
    if args:
        cli[rel] = args

os.makedirs("ATT/reports", exist_ok=True)
with open("ATT/reports/entrypoints_report_v2.json", "w", encoding="utf-8") as out:
    json.dump(cli, out, indent=2, ensure_ascii=False)

print("[analyze_pipeline_entrypoints_v2] OK (filtered) - wrote ATT/reports/entrypoints_report_v2.json")
