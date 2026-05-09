#!/usr/bin/env python3
import os
import ast
import json
from _scan_utils_v2 import iter_files

def analyze_imports(pyfile):
    with open(pyfile, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            tree = ast.parse(f.read(), filename=pyfile)
        except Exception:
            return []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports

result = {}
for f in iter_files(".", (".py",)):
    rel = os.path.relpath(f)
    result[rel] = sorted(set(analyze_imports(f)))

os.makedirs("ATT/reports", exist_ok=True)
with open("ATT/reports/imports_report_v2.json", "w", encoding="utf-8") as out:
    json.dump(result, out, indent=2, ensure_ascii=False)

print("[analyze_code_imports_v2] OK (filtered) - wrote ATT/reports/imports_report_v2.json")
