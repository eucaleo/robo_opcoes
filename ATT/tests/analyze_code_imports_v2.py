#!/usr/bin/env python3
import os, ast, json

def find_py_files(root):
    for dirpath, _, files in os.walk(root):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(dirpath, file)

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
for f in find_py_files('.'):
    rel = os.path.relpath(f)
    imps = analyze_imports(f)
    result[rel] = sorted(set(imps))

with open("ATT/reports/imports_report_v2.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print("[analyze_code_imports_v2] OK - wrote ATT/reports/imports_report_v2.json")
