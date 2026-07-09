from __future__ import annotations

import ast
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "123_phase1f_d12_recorte_operacional_appdb_derived.txt"

INCLUDE_TOP_LEVEL = {
    "UI",
    "db",
    "domain",
    "infra",
    "repositories",
    "scripts",
    "services",
    "tools",
}

EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "htmlcov",
    "FRENTE_BD_UNICO_APPDB",
    "ATT",
}

TOKENS = {
    "APP_DB_PATH": re.compile(r"\bAPP_DB_PATH\b"),
    "DERIVED_DB_PATH": re.compile(r"\bDERIVED_DB_PATH\b"),
    "connect_app": re.compile(r"\bconnect_app\b"),
    "connect_derived": re.compile(r"\bconnect_derived\b"),
    "get_app_db_connection": re.compile(r"\bget_app_db_connection\b"),
    "get_derived_connection": re.compile(r"\bget_derived_connection\b"),
    "sqlite3.connect": re.compile(r"\bsqlite3\.connect\s*\("),
    "dados/app.db": re.compile(r"dados[/\\]app\.db", re.IGNORECASE),
    "app.db": re.compile(r"\bapp\.db\b", re.IGNORECASE),
    "derived": re.compile(r"\bderived\b", re.IGNORECASE),
}

LEGACY_TOKENS = {
    "DERIVED_DB_PATH",
    "connect_derived",
    "get_derived_connection",
}

CANONICAL_TOKENS = {
    "APP_DB_PATH",
    "connect_app",
    "get_app_db_connection",
}

CONTRACT_FILES = {
    "db/config.py",
    "db/derived_repo.py",
}

HIGH_PRIORITY_HINTS = {
    "services/derived_service.py",
    "scripts/run_derived_pipeline.py",
    "db/writer.py",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_operational_file(path: Path) -> bool:
    if not path.is_file():
        return False

    if path.suffix.lower() != ".py":
        return False

    parts = set(path.relative_to(ROOT).parts)

    if parts & EXCLUDE_PARTS:
        return False

    top = path.relative_to(ROOT).parts[0]

    return top in INCLUDE_TOP_LEVEL


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def ast_details(path: Path, text: str) -> list[str]:
    details: list[str] = []

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"[SYNTAX_ERROR] {rel(path)}: {exc}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                name = alias.name
                if name in TOKENS or module in {"db.config", "db.derived_repo"}:
                    asname = f" as {alias.asname}" if alias.asname else ""
                    details.append(
                        f"[IMPORT_FROM] {rel(path)}:{node.lineno} "
                        f"from {module} import {name}{asname}"
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"sqlite3", "db.config", "db.derived_repo"}:
                    asname = f" as {alias.asname}" if alias.asname else ""
                    details.append(
                        f"[IMPORT] {rel(path)}:{node.lineno} import {alias.name}{asname}"
                    )

        elif isinstance(node, ast.FunctionDef):
            if node.name in TOKENS:
                details.append(
                    f"[DEF_FUNCTION] {rel(path)}:{node.lineno} def {node.name}(...):"
                )

        elif isinstance(node, ast.Call):
            func = node.func

            if isinstance(func, ast.Name) and func.id in TOKENS:
                details.append(
                    f"[CALL] {rel(path)}:{node.lineno} {func.id}(...)"
                )

            elif isinstance(func, ast.Attribute):
                base = ""
                if isinstance(func.value, ast.Name):
                    base = func.value.id

                if base == "sqlite3" and func.attr == "connect":
                    details.append(
                        f"[CALL] {rel(path)}:{node.lineno} sqlite3.connect(...)"
                    )

                if func.attr in TOKENS:
                    details.append(
                        f"[CALL_ATTR] {rel(path)}:{node.lineno} .{func.attr}(...)"
                    )

        elif isinstance(node, ast.Name):
            if node.id in TOKENS:
                ctx = type(node.ctx).__name__
                details.append(
                    f"[NAME_{ctx}] {rel(path)}:{node.lineno} {node.id}"
                )

    return details


def line_details(path: Path, text: str) -> list[str]:
    details: list[str] = []

    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue

        for label, pattern in TOKENS.items():
            if pattern.search(line):
                preview = stripped
                if len(preview) > 180:
                    preview = preview[:177] + "..."
                details.append(f"[TEXT:{label}] {rel(path)}:{lineno}: {preview}")

    return details


def classify_file(tokens_found: set[str], file_rel: str) -> list[str]:
    labels: list[str] = []

    if file_rel in CONTRACT_FILES:
        labels.append("CONTRATO_COMPATIBILIDADE")

    if file_rel in HIGH_PRIORITY_HINTS:
        labels.append("ALTA_PRIORIDADE_OPERACIONAL")

    if tokens_found & LEGACY_TOKENS:
        labels.append("USA_LEGADO_DERIVED")

    if tokens_found & CANONICAL_TOKENS:
        labels.append("USA_CANONICO_APPDB")

    if "sqlite3.connect" in tokens_found:
        labels.append("ABERTURA_MANUAL_SQLITE")

    if "dados/app.db" in tokens_found:
        labels.append("REFERENCIA_LITERAL_DADOS_APPDB")

    if "app.db" in tokens_found:
        labels.append("REFERENCIA_APPDB")

    if "derived" in tokens_found:
        labels.append("REFERENCIA_SEMANTICA_DERIVED")

    if not labels:
        labels.append("SEM_TOKEN_MONITORADO")

    return labels


def git_grep_operational(pattern: str) -> list[str]:
    cmd = [
        "git",
        "grep",
        "-n",
        pattern,
        "--",
        "UI/*.py",
        "UI/**/*.py",
        "db/*.py",
        "db/**/*.py",
        "domain/*.py",
        "domain/**/*.py",
        "infra/*.py",
        "infra/**/*.py",
        "repositories/*.py",
        "repositories/**/*.py",
        "scripts/*.py",
        "scripts/**/*.py",
        "services/*.py",
        "services/**/*.py",
        "tools/*.py",
        "tools/**/*.py",
    ]

    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )

    lines: list[str] = []
    lines.append(f"--- git grep operacional {pattern!r} returncode={proc.returncode} ---")

    if proc.stdout.strip():
        lines.extend(proc.stdout.strip().splitlines())
    elif proc.returncode == 1:
        lines.append("(sem ocorrencias)")
    else:
        lines.append("(sem stdout)")

    if proc.stderr.strip():
        lines.append(f"[stderr] {proc.stderr.strip()}")

    lines.append("")
    return lines


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    files = sorted(
        [p for p in ROOT.rglob("*.py") if is_operational_file(p)],
        key=lambda p: rel(p),
    )

    per_file_tokens: dict[str, set[str]] = defaultdict(set)
    per_file_counts: dict[str, int] = defaultdict(int)
    token_counts: dict[str, int] = defaultdict(int)
    classification: dict[str, list[str]] = {}

    ast_found: list[str] = []
    text_found: list[str] = []

    for path in files:
        text = read_text(path)
        file_rel = rel(path)

        for token, pattern in TOKENS.items():
            matches = pattern.findall(text)
            if matches:
                per_file_tokens[file_rel].add(token)
                per_file_counts[file_rel] += len(matches)
                token_counts[token] += len(matches)

        ast_items = ast_details(path, text)
        text_items = line_details(path, text)

        ast_found.extend(ast_items)
        text_found.extend(text_items)

        classification[file_rel] = classify_file(per_file_tokens[file_rel], file_rel)

    legacy_files = [
        file for file, tokens in per_file_tokens.items()
        if tokens & LEGACY_TOKENS
    ]

    manual_sqlite_files = [
        file for file, tokens in per_file_tokens.items()
        if "sqlite3.connect" in tokens
    ]

    canonical_files = [
        file for file, tokens in per_file_tokens.items()
        if tokens & CANONICAL_TOKENS
    ]

    only_semantic_derived_files = [
        file for file, tokens in per_file_tokens.items()
        if "derived" in tokens and not (tokens & LEGACY_TOKENS)
    ]

    next_candidates: list[str] = []

    for file in sorted(legacy_files):
        if file in CONTRACT_FILES:
            continue
        if file in {"services/derived_service.py", "scripts/run_derived_pipeline.py", "db/writer.py"}:
            next_candidates.append(file)

    for file in sorted(legacy_files):
        if file not in next_candidates and file not in CONTRACT_FILES:
            next_candidates.append(file)

    grep_patterns = [
        "connect_derived",
        "get_derived_connection",
        "DERIVED_DB_PATH",
        "connect_app",
        "get_app_db_connection",
        "APP_DB_PATH",
        "sqlite3.connect",
        "dados/app.db",
        "app.db",
    ]

    grep_lines: list[str] = []
    for pattern in grep_patterns:
        grep_lines.extend(git_grep_operational(pattern))

    out: list[str] = []

    out.append("===== DATA =====")
    out.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out.append("")
    out.append("===== OBJETIVO =====")
    out.append("Recorte operacional limpo de consumidores AppDB/Derived.")
    out.append("Esta fase nao altera codigo operacional.")
    out.append("")
    out.append("===== ESCOPO OPERACIONAL =====")
    out.append("Incluidos apenas arquivos .py sob:")
    for item in sorted(INCLUDE_TOP_LEVEL):
        out.append(f"- {item}/")
    out.append("")
    out.append("Excluidos:")
    for item in sorted(EXCLUDE_PARTS):
        out.append(f"- {item}")
    out.append("")
    out.append(f"Arquivos operacionais analisados: {len(files)}")
    out.append("")
    out.append("===== TOKENS MONITORADOS =====")
    for token in sorted(TOKENS):
        out.append(f"- {token}")
    out.append("")
    out.append("===== CONTAGEM OPERACIONAL POR TOKEN =====")
    if token_counts:
        for token, count in sorted(token_counts.items()):
            out.append(f"{token}: {count}")
    else:
        out.append("Nenhum token encontrado no recorte operacional.")
    out.append("")
    out.append("===== CLASSIFICACAO POR ARQUIVO =====")
    for file in sorted(classification):
        labels = ", ".join(classification[file])
        count = per_file_counts.get(file, 0)
        tokens = ", ".join(sorted(per_file_tokens.get(file, set()))) or "-"
        out.append(f"{file}: ocorrencias={count}; labels=[{labels}]; tokens=[{tokens}]")
    out.append("")
    out.append("===== ARQUIVOS COM LEGADO DERIVED OPERACIONAL =====")
    if legacy_files:
        for file in sorted(legacy_files):
            labels = ", ".join(classification[file])
            tokens = ", ".join(sorted(per_file_tokens[file]))
            out.append(f"- {file} | labels=[{labels}] | tokens=[{tokens}]")
    else:
        out.append("Nenhum arquivo operacional com legado derived.")
    out.append("")
    out.append("===== ARQUIVOS COM USO CANONICO APPDB =====")
    if canonical_files:
        for file in sorted(canonical_files):
            tokens = ", ".join(sorted(per_file_tokens[file]))
            out.append(f"- {file} | tokens=[{tokens}]")
    else:
        out.append("Nenhum arquivo operacional com uso canonico AppDB.")
    out.append("")
    out.append("===== ARQUIVOS COM ABERTURA MANUAL SQLITE =====")
    if manual_sqlite_files:
        for file in sorted(manual_sqlite_files):
            tokens = ", ".join(sorted(per_file_tokens[file]))
            out.append(f"- {file} | tokens=[{tokens}]")
    else:
        out.append("Nenhum arquivo operacional com sqlite3.connect.")
    out.append("")
    out.append("===== ARQUIVOS COM APENAS SEMANTICA DERIVED =====")
    out.append("Arquivos que mencionam derived semanticamente, mas nao usam connect_derived/get_derived_connection/DERIVED_DB_PATH.")
    if only_semantic_derived_files:
        for file in sorted(only_semantic_derived_files):
            tokens = ", ".join(sorted(per_file_tokens[file]))
            out.append(f"- {file} | tokens=[{tokens}]")
    else:
        out.append("Nenhum arquivo apenas semantico.")
    out.append("")
    out.append("===== CANDIDATOS PARA PROXIMA FASE =====")
    if next_candidates:
        for file in next_candidates:
            if file == "services/derived_service.py":
                reason = "maior consumidor operacional de connect_derived"
            elif file == "scripts/run_derived_pipeline.py":
                reason = "pipeline operacional usa connect_derived"
            elif file == "db/writer.py":
                reason = "usa get_derived_connection alias legado"
            else:
                reason = "possui tokens legados derived no recorte operacional"
            out.append(f"- {file}: {reason}")
    else:
        out.append("Nenhum candidato identificado.")
    out.append("")
    out.append("===== ACHADOS AST OPERACIONAIS =====")
    if ast_found:
        out.extend(ast_found)
    else:
        out.append("Nenhum achado AST operacional.")
    out.append("")
    out.append("===== ACHADOS TEXTUAIS OPERACIONAIS =====")
    if text_found:
        out.extend(text_found)
    else:
        out.append("Nenhum achado textual operacional.")
    out.append("")
    out.append("===== GIT GREP OPERACIONAL =====")
    out.extend(grep_lines)
    out.append("")
    out.append("===== LEITURA PRELIMINAR =====")
    out.append("- db/config.py e db/derived_repo.py devem ser tratados como contratos de compatibilidade, nao como alvo imediato de remocao.")
    out.append("- services/derived_service.py tende a ser o principal candidato para renomeacao controlada de connect_derived para connect_app.")
    out.append("- scripts/run_derived_pipeline.py e db/writer.py tambem aparecem como consumidores legados importantes.")
    out.append("- sqlite3.connect deve ser analisado separadamente; nem toda abertura manual e problema nesta fase.")
    out.append("")
    out.append("===== DECISAO =====")
    out.append("[OK] Recorte operacional concluido. Usar esta evidencia para planejar a proxima fase de alteracao minima.")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")

    print("[OK] Fase 1F-D.12 concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
