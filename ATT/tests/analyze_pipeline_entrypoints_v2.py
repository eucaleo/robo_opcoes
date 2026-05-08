#!/usr/bin/env python3
import os, re, json
def find_py_files(root):
    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(dirpath, file)
cli = {}
for f in find_py_files('.'):
    rel = os.path.relpath(f)
    txt = open(f, encoding="utf-8", errors="ignore").read()
    args = re.findall(r'add_argument\(\s*[\'\"]([^\'\"]+)[\'\"]', txt)
    if args:
        cli[rel] = args
with open("ATT/reports/entrypoints_report_v2.json", "w", encoding="utf-8") as f:
    json.dump(cli, f, indent=2, ensure_ascii=False)
print("[analyze_pipeline_entrypoints_v2] OK - wrote ATT/reports/entrypoints_report_v2.json")
