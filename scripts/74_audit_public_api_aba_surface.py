"""
Auditoria de candidatos a migracao para StructureRef.
Classifica ocorrencias de uso legado de 'aba' em: READY, NEEDS_LOOKUP, READONLY.

Uso:
  python scripts/74_audit_public_api_aba_surface.py
  python scripts/74_audit_public_api_aba_surface.py --root src
  python scripts/74_audit_public_api_aba_surface.py --out ATT/reports/patch57_surface.md

patch_57c -- from __future__ REMOVIDO (incompativel com importlib.exec_module
             sem registro previo em sys.modules no Python 3.13).
"""


import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# ──────────────────────────────────────────────────────────────────────
# Tipos e constantes
# ──────────────────────────────────────────────────────────────────────
@dataclass
class AuditEntry:
    file:           str
    line:           int
    text:           str
    classification: str  # READY | NEEDS_LOOKUP | READONLY


_ABA_PATTERN = re.compile(r'\baba\b')


def _classify(line_text: str, full_src: str) -> str:
    """Heurística de classificação por contexto."""
    lt = line_text.lower()
    if "ref.aba" in lt:
        return "READY"

    if "structure_ref" in full_src.lower():
        return "NEEDS_LOOKUP"
    return "READONLY"


# ──────────────────────────────────────────────────────────────────────
# API pública (exigida pelos testes patch_57d)
# ──────────────────────────────────────────────────────────────────────
def scan_directory(root, extensions: tuple = (".py",)) -> List[AuditEntry]:
    """Varre *root* recursivamente e retorna lista de AuditEntry.

    Parâmetros
    ----------
    root:       diretório raiz a ser varrido
    extensions: extensões de arquivo a considerar (padrão: .py)

    Retorna
    -------
    Lista de AuditEntry com campo classification em
    {READY, NEEDS_LOOKUP, READONLY}.
    """
    root = Path(root)
    entries: List[AuditEntry] = []
    for filepath in sorted(root.rglob("*")):
        if filepath.suffix not in extensions:
            continue
        if not filepath.is_file():
            continue
        try:
            text = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines_src = text.splitlines()
        for match in _ABA_PATTERN.finditer(text):
            line_no   = text[: match.start()].count("\n") + 1
            line_text = lines_src[line_no - 1].strip() if line_no <= len(lines_src) else ""
            entries.append(
                AuditEntry(
                    file=str(filepath),
                    line=line_no,
                    text=line_text,
                    classification=_classify(line_text, text),
                )
            )
    return entries



def format_report(entries) -> str:
    """Formata lista de AuditEntry em relatório texto."""
    lines = []
    for e in entries:
        lines.append(f"{e.filepath}:{e.lineno} [{e.classification}] {e.line_text.rstrip()}")
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auditoria de uso legado de 'aba'")
    parser.add_argument("--root", default=".", help="Diretório raiz")
    parser.add_argument("--out", default=None, help="Arquivo de saída (.md)")
    args = parser.parse_args()

    entries = scan_directory(args.root)
    summary = {}
    for e in entries:
        summary[e.classification] = summary.get(e.classification, 0) + 1

    lines = ["# Audit: uso legado de `aba`", ""]
    for cls in ("READY", "NEEDS_LOOKUP", "READONLY"):
        lines.append(f"## {cls} ({summary.get(cls, 0)})")
    lines += ["", f"Total: {len(entries)} ocorrências"]

    report = "\n".join(lines)
    if args.out:
        pathlib.Path(args.out).write_text(report, encoding="utf-8")
        print(f"Relatório salvo em {args.out}")
    else:
        print(report)

classify = _classify  # alias público exigido pelos testes
