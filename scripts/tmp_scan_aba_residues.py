"""
tmp_scan_aba_residues.py  —  TEMPORÁRIO (remover após patch_53)

Varre o projeto em busca de todos os resíduos do campo 'aba'.
Gera relatório em scripts/tmp_aba_residues_report.txt
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".mypy_cache"}
EXCLUDE_FILES = {"run_patch_33.py"}  # frozen — NÃO tocar

PATTERNS = [
    (r"\baba\b\s*=",           "atribuição direta de 'aba'"),
    (r"['\"]aba['\"]",         "string literal 'aba'"),
    (r"def\s+\w+.*\baba\b",    "parâmetro 'aba' em assinatura"),
    (r"WHERE\s+aba\s*=",       "SQL raw com 'aba'"),
    (r"params.*\[.*aba",       "params list com 'aba'"),
    (r"self\.aba\b",           "atributo self.aba"),
    (r"\.get\(['\"]aba['\"]",  "dict.get('aba')"),
    (r"\[[\"\']aba[\"\']\]",   "dict access ['aba']"),
]

findings = []

for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
    for fname in files:
        if fname in EXCLUDE_FILES:
            continue
        if not fname.endswith(".py"):
            continue
        fpath = Path(root) / fname
        rel = fpath.relative_to(ROOT)
        try:
            lines = fpath.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for lineno, line in enumerate(lines, 1):
            for pattern, label in PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append({
                        "file": str(rel),
                        "line": lineno,
                        "label": label,
                        "content": line.strip(),
                    })
                    break  # evita duplicata por linha

report_path = ROOT / "scripts" / "tmp_aba_residues_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"RELATÓRIO DE RESÍDUOS 'aba' — {len(findings)} ocorrências\n")
    f.write("=" * 70 + "\n\n")
    current_file = None
    for item in findings:
        if item["file"] != current_file:
            current_file = item["file"]
            f.write(f"\n📄 {current_file}\n")
            f.write("-" * 60 + "\n")
        f.write(f"  L{item['line']:>4} [{item['label']}]\n")
        f.write(f"         {item['content']}\n")

print(f"✅ {len(findings)} resíduos encontrados.")
print(f"📄 Relatório: {report_path}")
sys.exit(0 if findings else 1)
