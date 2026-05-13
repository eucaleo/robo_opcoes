#!/usr/bin/env bash
set -euo pipefail

echo "[patch_01] rodando scripts de análise automática..."

python ATT/tests/analyze_code_imports_v2.py
python ATT/tests/analyze_pipeline_entrypoints_v2.py
python ATT/tests/analyze_sql_usage_v2.py

echo "[patch_01] agregando relatório markdown/JSON..."
python - << 'PY'
import json, os

def loadj(fn):
    with open(fn, encoding="utf-8") as f:
        return json.load(f)

base = "ATT/reports/"
imports = loadj(base + "imports_report_v2.json")
entrypts = loadj(base + "entrypoints_report_v2.json")
sqls = loadj(base + "sql_report_v2.json")

def fmt_section(name, mapping):
    out = [f"## {name}"]
    for k, v in sorted(mapping.items()):
        out.append(f"- `{k}`:")
        if isinstance(v, list):
            for t in v:
                out.append(f"  - {t}")
        elif isinstance(v, dict):
            for s, val in v.items():
                out.append(f"  - {s}: {val}")
        else:
            out.append(f"  {v}")
    out.append("")
    return "\n".join(out)

md = [
  "# Baseline_v2 – Análise de Código e Estruturas (auto)",
  "",
  "Relatório gerado por scripts de análise (v2):",
  "",
  fmt_section("Imports entre módulos", imports),
  fmt_section("CLI EntryPoints encontrados (add_argument)", entrypts),
  fmt_section("Tabelas SQL usadas", sqls),
]

with open(base + "report_v2.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))

# Salva tudo junto para consumo futuro
combo = dict(imports=imports, entrypoints=entrypts, sql_tables=sqls)
with open(base + "report_v2.json", "w", encoding="utf-8") as f:
    json.dump(combo, f, indent=2)

print("[patch_01] relatório salvo: ATT/reports/report_v2.md + ATT/reports/report_v2.json")
PY

echo "[patch_01] pronto."
