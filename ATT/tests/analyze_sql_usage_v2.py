#!/usr/bin/env python3
import os, re, json
def find_py_files(root):
    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(dirpath, file)
tables = {}
for f in find_py_files('.'):
    rel = os.path.relpath(f)
    lines = open(f, encoding="utf-8", errors="ignore").readlines()
    found = []
    for i, line in enumerate(lines):
        for kw in ("FROM", "from", "JOIN", "join", "INSERT INTO", "insert into"):
            if kw in line:
                tbls = re.findall(r'(from|join|FROM|JOIN|INTO|into)\s+([a-zA-Z0-9_]+)', line)
                found += [ (i+1, t[1]) for t in tbls ]
    if found:
        tables[rel] = found
with open("ATT/reports/sql_report_v2.json", "w", encoding="utf-8") as f:
    json.dump(tables, f, indent=2, ensure_ascii=False)
print("[analyze_sql_usage_v2] OK - wrote ATT/reports/sql_report_v2.json")
