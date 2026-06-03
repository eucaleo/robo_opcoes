# scripts/tmp_audit_structure_ref_candidates.py
"""
Auditoria de candidatos a migracao para StructureRef.

Classifica ocorrencias de uso legado de 'aba' como chave de query em:
  READY        -> structure_id disponivel no mesmo escopo, pode migrar agora
  NEEDS_LOOKUP -> requer StructureRef.from_aba() com lookup no repositorio
  READONLY     -> uso somente leitura, nao migrar (ex: get_abas())

Execucao (Git Bash / Windows):
  python scripts/tmp_audit_structure_ref_candidates.py
  python scripts/tmp_audit_structure_ref_candidates.py --root src
  python scripts/tmp_audit_structure_ref_candidates.py --root src --out relatorio.txt
"""

from __future__ import annotations

import argparse
import ast
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Padroes de busca
# ---------------------------------------------------------------------------

LEGACY_PATTERNS = [
    '.get("aba")',
    ".get('aba')",
    '["aba"]',
    "['aba']",
    'WHERE aba',
    'where aba',
    '"aba"',          # strings soltas em queries SQL
]

STRUCTURE_ID_SIGNALS = [
    "structure_id",
    "StructureRef",
    "from_id(",
    "from_aba(",
]

READONLY_SIGNALS = [
    "get_abas",
    "list_abas",
    "fetch_abas",
    "return aba",
    "yield aba",
    "abas =",
    "abas=",
]

SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "env",
    "node_modules", ".mypy_cache", ".pytest_cache",
    "dist", "build", ".eggs",
}

SKIP_FILES = {
    "structure_ref.py",                        # o proprio ValueObject
    "tmp_audit_structure_ref_candidates.py",   # este script
}


# ---------------------------------------------------------------------------
# Modelo de resultado
# ---------------------------------------------------------------------------

@dataclass
class Occurrence:
    filepath: str
    lineno: int
    line: str
    pattern: str
    classification: str  # READY | NEEDS_LOOKUP | READONLY
    reason: str


@dataclass
class FileReport:
    filepath: str
    occurrences: List[Occurrence] = field(default_factory=list)

    @property
    def has_findings(self) -> bool:
        return len(self.occurrences) > 0

    def summary_by_class(self) -> dict:
        result = {"READY": 0, "NEEDS_LOOKUP": 0, "READONLY": 0}
        for occ in self.occurrences:
            result[occ.classification] = result.get(occ.classification, 0) + 1
        return result


# ---------------------------------------------------------------------------
# Logica de classificacao
# ---------------------------------------------------------------------------

def _load_context_lines(filepath: str, center: int, window: int = 10) -> List[str]:
    """Retorna as linhas ao redor de 'center' para analise de contexto."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            all_lines = fh.readlines()
        start = max(0, center - window)
        end = min(len(all_lines), center + window)
        return [l.rstrip() for l in all_lines[start:end]]
    except OSError:
        return []


def classify(
    filepath: str,
    lineno: int,
    line: str,
    pattern: str,
) -> tuple[str, str]:
    """
    Retorna (classification, reason).

    Logica:
      1. Se a linha ou contexto proximo contem sinais READONLY -> READONLY
      2. Se o contexto contem structure_id ou StructureRef     -> READY
      3. Caso contrario                                        -> NEEDS_LOOKUP
    """
    context = _load_context_lines(filepath, lineno - 1, window=8)
    context_blob = "\n".join(context).lower()
    line_lower = line.lower()

    # Verifica READONLY primeiro (maior prioridade)
    for sig in READONLY_SIGNALS:
        if sig.lower() in context_blob:
            return "READONLY", f"sinal readonly detectado: '{sig}'"

    # Verifica READY
    for sig in STRUCTURE_ID_SIGNALS:
        if sig.lower() in context_blob:
            return "READY", f"structure_id disponivel no contexto: '{sig}'"

    return "NEEDS_LOOKUP", "sem structure_id no contexto imediato"


# ---------------------------------------------------------------------------
# Scanner de arquivo
# ---------------------------------------------------------------------------

def scan_file(filepath: str) -> FileReport:
    report = FileReport(filepath=filepath)

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print(f"[AVISO] Nao foi possivel ler {filepath}: {exc}", file=sys.stderr)
        return report

    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip()
        for pattern in LEGACY_PATTERNS:
            if pattern in line:
                classification, reason = classify(filepath, lineno, line, pattern)
                report.occurrences.append(
                    Occurrence(
                        filepath=filepath,
                        lineno=lineno,
                        line=line.strip(),
                        pattern=pattern,
                        classification=classification,
                        reason=reason,
                    )
                )
                break  # evita duplicar a mesma linha por multiplos patterns

    return report


# ---------------------------------------------------------------------------
# Varredura de diretorio
# ---------------------------------------------------------------------------

def scan_directory(root: Path) -> List[FileReport]:
    reports: List[FileReport] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Remove diretorios a ignorar in-place (afeta os.walk)
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            if filename in SKIP_FILES:
                continue
            if not filename.endswith(".py"):
                continue

            full_path = os.path.join(dirpath, filename)
            report = scan_file(full_path)
            if report.has_findings:
                reports.append(report)

    return reports


# ---------------------------------------------------------------------------
# Formatacao de saida
# ---------------------------------------------------------------------------

SEPARATOR = "-" * 72
HEADER    = "=" * 72


def format_report(reports: List[FileReport], root: Path) -> str:
    lines: List[str] = []

    lines.append(HEADER)
    lines.append("AUDITORIA: candidatos a migracao para StructureRef")
    lines.append(f"Raiz analisada : {root.resolve()}")
    lines.append(HEADER)
    lines.append("")

    if not reports:
        lines.append("Nenhuma ocorrencia de uso legado de 'aba' encontrada.")
        return "\n".join(lines)

    total_ready        = 0
    total_needs_lookup = 0
    total_readonly     = 0

    for rep in reports:
        summary = rep.summary_by_class()
        total_ready        += summary["READY"]
        total_needs_lookup += summary["NEEDS_LOOKUP"]
        total_readonly     += summary["READONLY"]

        lines.append(SEPARATOR)
        lines.append(f"ARQUIVO: {rep.filepath}")
        lines.append(
            f"  READY={summary['READY']}  "
            f"NEEDS_LOOKUP={summary['NEEDS_LOOKUP']}  "
            f"READONLY={summary['READONLY']}"
        )
        lines.append("")

        for occ in rep.occurrences:
            lines.append(f"  Linha {occ.lineno:>4} [{occ.classification:<12}]")
            lines.append(f"    pattern  : {occ.pattern}")
            lines.append(f"    conteudo : {occ.line[:120]}")
            lines.append(f"    motivo   : {occ.reason}")
            lines.append("")

    lines.append(HEADER)
    lines.append("TOTAIS GERAIS")
    lines.append(HEADER)
    lines.append(f"  Arquivos com ocorrencias : {len(reports)}")
    lines.append(f"  READY                   : {total_ready}")
    lines.append(f"  NEEDS_LOOKUP            : {total_needs_lookup}")
    lines.append(f"  READONLY                : {total_readonly}")
    lines.append(f"  TOTAL                   : {total_ready + total_needs_lookup + total_readonly}")
    lines.append("")
    lines.append("PROXIMO PASSO SUGERIDO")
    lines.append("  1. Migrar todos os READY primeiro (impacto zero, sem lookup)")
    lines.append("  2. Criar adaptadores com StructureRef.from_aba() para NEEDS_LOOKUP")
    lines.append("  3. Manter READONLY sem alteracao ate decisao explicita")
    lines.append(HEADER)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audita candidatos a migracao para StructureRef."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Diretorio raiz da varredura (default: diretorio atual)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Arquivo de saida para o relatorio (default: stdout)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root)

    if not root.exists():
        print(f"[ERRO] Diretorio nao encontrado: {root}", file=sys.stderr)
        sys.exit(1)

    print(f"Varrendo: {root.resolve()} ...", file=sys.stderr)
    reports = scan_directory(root)
    output  = format_report(reports, root)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"Relatorio salvo em: {out_path}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
