from __future__ import annotations

from datetime import datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
FRENTE = ROOT / "FRENTE_BD_UNICO_APPDB"
EVID = FRENTE / "evidencias"

OPERATIONAL_DIRS = [
    "ATT",
    "UI",
    "db",
    "domain",
    "repositories",
    "scripts",
    "services",
]

TRANSITIONAL_FILES = [
    FRENTE / "AUDITORIA.md",
    FRENTE / "GUIA_DESENVOLVIMENTO.md",
]

TRANSITIONAL_DIRS = [
    FRENTE / "scripts",
]

TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".sh",
    ".ps1",
    ".bat",
    ".cmd",
    ".yml",
    ".yaml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
}

SKIP_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "backups",
    "backups_phase1f",
    "evidencias",
}

IDENTIFIER_TOKENS = [
    "derived_db",
    "DERIVED_DB",
    "derived_repo",
    "derived_service",
    "DerivedService",
    "get_derived",
    "cleanup_derived",
    "validate_derived_db",
    "repair_derived_db",
    "purge_derived",
    "run_derived_pipeline",
]


def is_text_candidate(path: Path) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    parts = set(path.parts)
    if parts & SKIP_PARTS:
        return False
    return True


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def iter_operational_files():
    seen = set()
    for dirname in OPERATIONAL_DIRS:
        base = ROOT / dirname
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if not is_text_candidate(path):
                continue
            if path in seen:
                continue
            seen.add(path)
            yield path


def iter_transitional_files():
    seen = set()

    for path in TRANSITIONAL_FILES:
        if path.exists() and path.is_file() and is_text_candidate(path):
            seen.add(path)
            yield path

    for base in TRANSITIONAL_DIRS:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if not is_text_candidate(path):
                continue
            if path in seen:
                continue
            seen.add(path)
            yield path


def find_literal_hits(paths, literal: str):
    hits = []
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if literal in line:
                hits.append((path, line_no, line.rstrip()))
    return hits


def find_case_insensitive_hits(paths, literal: str):
    hits = []
    wanted = literal.lower()
    for path in paths:
        text = read_text(path)
        if text is None:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if wanted in line.lower():
                hits.append((path, line_no, line.rstrip()))
    return hits


def find_identifier_hits(paths):
    token_hits = defaultdict(list)

    for path in paths:
        text = read_text(path)
        if text is None:
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            for token in IDENTIFIER_TOKENS:
                if token in line:
                    token_hits[token].append((path, line_no, line.rstrip()))

    return token_hits


def format_hits(hits):
    if not hits:
        return "Nenhuma ocorrência encontrada.\n"

    lines = []
    for path, line_no, line in hits:
        lines.append(f"{rel(path)}:{line_no}: {line}")
    return "\n".join(lines) + "\n"


def main():
    EVID.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    operational_files = list(iter_operational_files())
    transitional_files = list(iter_transitional_files())
    all_scanned_files = operational_files + transitional_files

    op_literal_hits = find_literal_hits(operational_files, "derived.db")
    tr_literal_hits = find_literal_hits(transitional_files, "derived.db")

    op_ci_hits = find_case_insensitive_hits(operational_files, "derived.db")
    tr_ci_hits = find_case_insensitive_hits(transitional_files, "derived.db")

    token_hits = find_identifier_hits(all_scanned_files)

    report_45 = []
    report_45.append("===== DATA =====")
    report_45.append(now)
    report_45.append("")
    report_45.append("===== OBJETIVO =====")
    report_45.append("Auditoria precisa usando busca literal fixa para derived.db.")
    report_45.append("Separar referencias fisicas reais do arquivo legado de identificadores tecnicos derived_*.")
    report_45.append("")
    report_45.append("===== ESCOPO OPERACIONAL =====")
    report_45.extend(OPERATIONAL_DIRS)
    report_45.append("")
    report_45.append("===== ESCOPO TRANSICIONAL =====")
    report_45.append("FRENTE_BD_UNICO_APPDB/AUDITORIA.md")
    report_45.append("FRENTE_BD_UNICO_APPDB/GUIA_DESENVOLVIMENTO.md")
    report_45.append("FRENTE_BD_UNICO_APPDB/scripts/*.py")
    report_45.append("")
    report_45.append("===== CONTAGEM DE ARQUIVOS VARREDOS =====")
    report_45.append(f"operacionais: {len(operational_files)}")
    report_45.append(f"transicionais: {len(transitional_files)}")
    report_45.append("")
    report_45.append("===== LITERAL EXATO derived.db EM CODIGO OPERACIONAL =====")
    report_45.append(format_hits(op_literal_hits).rstrip())
    report_45.append("")
    report_45.append("===== LITERAL EXATO derived.db EM ARTEFATOS TRANSICIONAIS =====")
    report_45.append(format_hits(tr_literal_hits).rstrip())
    report_45.append("")
    report_45.append("===== BUSCA CASE-INSENSITIVE derived.db EM CODIGO OPERACIONAL =====")
    report_45.append(format_hits(op_ci_hits).rstrip())
    report_45.append("")
    report_45.append("===== BUSCA CASE-INSENSITIVE derived.db EM ARTEFATOS TRANSICIONAIS =====")
    report_45.append(format_hits(tr_ci_hits).rstrip())
    report_45.append("")
    report_45.append("===== DECISAO =====")
    if op_literal_hits:
        report_45.append("[ATENCAO] Ainda existem referencias literais derived.db em codigo operacional.")
        report_45.append("[BLOQUEIO] Nao avancar para renomeacao tecnica antes de revisar essas ocorrencias.")
    else:
        report_45.append("[OK] Nenhuma referencia literal exata derived.db encontrada em codigo operacional.")
        report_45.append("[OK] Ocorrencias derived_* remanescentes devem ser tratadas como nomes tecnicos/compatibilidade.")
    report_45.append("")

    (EVID / "45_phase1f_b_auditoria_literal_derived_db.txt").write_text(
        "\n".join(report_45),
        encoding="utf-8",
    )

    report_46 = []
    report_46.append("===== DATA =====")
    report_46.append(now)
    report_46.append("")
    report_46.append("===== OBJETIVO =====")
    report_46.append("Mapa de identificadores tecnicos derived_* remanescentes apos Fase 1F-A.")
    report_46.append("Este mapa NAO indica dependencia fisica em derived.db por si so.")
    report_46.append("")
    report_46.append("===== TOKENS MONITORADOS =====")
    for token in IDENTIFIER_TOKENS:
        report_46.append(f"- {token}")
    report_46.append("")
    report_46.append("===== MAPA POR TOKEN =====")

    for token in IDENTIFIER_TOKENS:
        hits = token_hits.get(token, [])
        report_46.append("")
        report_46.append(f"----- {token} -----")
        report_46.append(f"count: {len(hits)}")
        if hits:
            report_46.append(format_hits(hits).rstrip())
        else:
            report_46.append("Nenhuma ocorrência encontrada.")

    report_46.append("")
    report_46.append("===== DECISAO =====")
    report_46.append("[INFO] Identificadores derived_* permanecem como superficie tecnica legada/compatibilidade.")
    report_46.append("[INFO] Proxima subfase deve decidir entre manter aliases ou renomear APIs em camadas controladas.")
    report_46.append("")

    (EVID / "46_phase1f_b_mapa_identificadores_derived.txt").write_text(
        "\n".join(report_46),
        encoding="utf-8",
    )

    print("[OK] Fase 1F-B auditoria precisa concluida.")
    print("Gerados:")
    print("  FRENTE_BD_UNICO_APPDB/evidencias/45_phase1f_b_auditoria_literal_derived_db.txt")
    print("  FRENTE_BD_UNICO_APPDB/evidencias/46_phase1f_b_mapa_identificadores_derived.txt")


if __name__ == "__main__":
    main()
