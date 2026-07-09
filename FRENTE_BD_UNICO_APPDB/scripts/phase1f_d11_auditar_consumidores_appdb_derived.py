from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "121_phase1f_d11_auditoria_consumidores_appdb_derived.txt"

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
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
}

SKIP_PARTS = {
    "FRENTE_BD_UNICO_APPDB/evidencias",
}

PY_NAMES = {
    "connect_derived",
    "get_derived_connection",
    "get_app_db_connection",
    "connect_app",
    "DERIVED_DB_PATH",
    "APP_DB_PATH",
}

TEXT_PATTERNS = {
    "dados/app.db": re.compile(r"dados[/\\]app\.db", re.IGNORECASE),
    "app.db": re.compile(r"\bapp\.db\b", re.IGNORECASE),
    "derived": re.compile(r"\bderived\b", re.IGNORECASE),
    "sqlite3.connect": re.compile(r"\bsqlite3\.connect\s*\(", re.IGNORECASE),
    "connect_derived": re.compile(r"\bconnect_derived\b"),
    "get_derived_connection": re.compile(r"\bget_derived_connection\b"),
    "get_app_db_connection": re.compile(r"\bget_app_db_connection\b"),
    "connect_app": re.compile(r"\bconnect_app\b"),
    "DERIVED_DB_PATH": re.compile(r"\bDERIVED_DB_PATH\b"),
    "APP_DB_PATH": re.compile(r"\bAPP_DB_PATH\b"),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    r = rel(path)

    for part in SKIP_PARTS:
        if r.startswith(part + "/") or r == part:
            return True

    return any(part in SKIP_DIRS for part in path.parts)


def iter_files() -> list[Path]:
    files: list[Path] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in {".py", ".txt", ".md", ".toml", ".ini", ".cfg", ".json", ".yaml", ".yml"}:
            continue
        files.append(path)

    return sorted(files, key=lambda p: rel(p))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def ast_scan_python(path: Path, text: str) -> list[str]:
    items: list[str] = []

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"[SYNTAX_ERROR] {rel(path)}: {exc}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name in PY_NAMES or module in {"db.config", "db.derived_repo"}:
                    asname = f" as {alias.asname}" if alias.asname else ""
                    items.append(
                        f"[IMPORT_FROM] {rel(path)}:{node.lineno} "
                        f"from {module} import {alias.name}{asname}"
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"db.config", "db.derived_repo", "sqlite3"}:
                    asname = f" as {alias.asname}" if alias.asname else ""
                    items.append(
                        f"[IMPORT] {rel(path)}:{node.lineno} import {alias.name}{asname}"
                    )

        elif isinstance(node, ast.FunctionDef):
            if node.name in PY_NAMES:
                items.append(
                    f"[DEF_FUNCTION] {rel(path)}:{node.lineno} def {node.name}(...):"
                )

        elif isinstance(node, ast.Name):
            if node.id in PY_NAMES:
                ctx = type(node.ctx).__name__
                items.append(
                    f"[NAME_{ctx}] {rel(path)}:{node.lineno} {node.id}"
                )

        elif isinstance(node, ast.Call):
            func = node.func

            if isinstance(func, ast.Name) and func.id in PY_NAMES:
                items.append(
                    f"[CALL] {rel(path)}:{node.lineno} {func.id}(...)"
                )

            elif isinstance(func, ast.Attribute):
                attr = func.attr
                base = ""

                if isinstance(func.value, ast.Name):
                    base = func.value.id
                elif isinstance(func.value, ast.Attribute):
                    base = func.value.attr

                if attr == "connect" and base == "sqlite3":
                    items.append(
                        f"[CALL] {rel(path)}:{node.lineno} sqlite3.connect(...)"
                    )

                if attr in PY_NAMES:
                    items.append(
                        f"[CALL_ATTR] {rel(path)}:{node.lineno} .{attr}(...)"
                    )

    return items


def text_scan(path: Path, text: str) -> list[str]:
    items: list[str] = []
    lines = text.splitlines()

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        for label, pattern in TEXT_PATTERNS.items():
            if pattern.search(line):
                preview = stripped
                if len(preview) > 180:
                    preview = preview[:177] + "..."
                items.append(f"[TEXT:{label}] {rel(path)}:{lineno}: {preview}")

    return items


def git_grep(pattern: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", "grep", "-n", pattern, "--", "*.py"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    files = iter_files()

    ast_items: list[str] = []
    text_items: list[str] = []

    counts_by_file: dict[str, int] = defaultdict(int)
    counts_by_token: dict[str, int] = defaultdict(int)

    for path in files:
        text = read_text(path)

        if path.suffix.lower() == ".py":
            found_ast = ast_scan_python(path, text)
            ast_items.extend(found_ast)

            for item in found_ast:
                counts_by_file[rel(path)] += 1
                for token in PY_NAMES:
                    if token in item:
                        counts_by_token[token] += 1

        found_text = text_scan(path, text)
        text_items.extend(found_text)

        for item in found_text:
            counts_by_file[rel(path)] += 1
            for token in TEXT_PATTERNS:
                if f"[TEXT:{token}]" in item:
                    counts_by_token[token] += 1

    git_grep_patterns = [
        "connect_derived",
        "get_derived_connection",
        "get_app_db_connection",
        "connect_app",
        "DERIVED_DB_PATH",
        "APP_DB_PATH",
        "sqlite3.connect",
        "app.db",
    ]

    git_grep_results: list[str] = []

    for pattern in git_grep_patterns:
        rc, stdout, stderr = git_grep(pattern)
        git_grep_results.append(f"--- git grep {pattern!r} returncode={rc} ---")
        if stdout:
            git_grep_results.extend(stdout.splitlines())
        if stderr:
            git_grep_results.append(f"[stderr] {stderr}")
        if not stdout and not stderr:
            git_grep_results.append("(sem ocorrencias)")
        git_grep_results.append("")

    out: list[str] = []
    out.append("===== DATA =====")
    out.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out.append("")
    out.append("===== OBJETIVO =====")
    out.append("Auditar consumidores e referencias de conexao AppDB/Derived.")
    out.append("Esta fase nao altera codigo operacional.")
    out.append("")
    out.append("===== ESCOPO DA AUDITORIA =====")
    out.append(f"Arquivos analisados: {len(files)}")
    out.append("Tipos analisados: .py, .txt, .md, .toml, .ini, .cfg, .json, .yaml, .yml")
    out.append("Diretorios de evidencia foram excluidos para evitar ruido de fases anteriores.")
    out.append("")
    out.append("===== TOKENS MONITORADOS =====")
    for token in sorted(set(PY_NAMES) | set(TEXT_PATTERNS)):
        out.append(f"- {token}")
    out.append("")
    out.append("===== CONTAGEM POR TOKEN =====")
    if counts_by_token:
        for token, count in sorted(counts_by_token.items()):
            out.append(f"{token}: {count}")
    else:
        out.append("Nenhum token monitorado encontrado.")
    out.append("")
    out.append("===== ARQUIVOS COM OCORRENCIAS =====")
    if counts_by_file:
        for file, count in sorted(counts_by_file.items()):
            out.append(f"{file}: {count}")
    else:
        out.append("Nenhum arquivo com ocorrencias.")
    out.append("")
    out.append("===== ACHADOS AST PYTHON =====")
    if ast_items:
        out.extend(ast_items)
    else:
        out.append("Nenhum achado AST relevante.")
    out.append("")
    out.append("===== ACHADOS TEXTUAIS =====")
    if text_items:
        out.extend(text_items)
    else:
        out.append("Nenhum achado textual relevante.")
    out.append("")
    out.append("===== GIT GREP PYTHON =====")
    out.extend(git_grep_results)
    out.append("")
    out.append("===== LEITURA PRELIMINAR =====")
    out.append("- Ocorrencias de get_derived_connection indicam consumidores do alias legado.")
    out.append("- Ocorrencias de connect_derived/DERIVED_DB_PATH indicam nomenclatura antiga que pode precisar de alias ou renomeacao posterior.")
    out.append("- Ocorrencias de sqlite3.connect/app.db podem indicar abertura manual que deve ser avaliada antes de padronizar.")
    out.append("- Esta fase e apenas auditoria; nenhuma troca automatica foi aplicada.")
    out.append("")
    out.append("===== DECISAO =====")
    out.append("[OK] Auditoria concluida. Usar esta evidencia para planejar a proxima fase de compatibilidade/renomeacao.")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")

    print("[OK] Fase 1F-D.11 concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
