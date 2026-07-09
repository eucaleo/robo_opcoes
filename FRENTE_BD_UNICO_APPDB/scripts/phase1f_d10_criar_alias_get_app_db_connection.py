from __future__ import annotations

import ast
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
TARGET = ROOT / "db" / "derived_repo.py"
OUT = EVID / "119_phase1f_d10_alias_get_app_db_connection.txt"


IMPORT_LINE = "from db.config import connect_app"

ALIAS_BLOCK = '''

def get_app_db_connection() -> sqlite3.Connection:
    """Retorna conexao para o banco unico da aplicacao app.db."""
    return connect_app()


def get_derived_connection() -> sqlite3.Connection:
    """Alias legado preservado temporariamente para compatibilidade."""
    return get_app_db_connection()
'''


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_function(text: str, name: str) -> bool:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False

    return any(isinstance(node, ast.FunctionDef) and node.name == name for node in ast.walk(tree))


def ast_items(path: Path, text: str) -> list[str]:
    items: list[str] = []

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"[SYNTAX_ERROR] {rel(path)}: {exc}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if module == "db.config" or alias.name in {"get_app_db_connection", "get_derived_connection"}:
                    asname = f" as {alias.asname}" if alias.asname else ""
                    items.append(f"[IMPORT_FROM] {rel(path)}:{node.lineno} from {module} import {alias.name}{asname}")

        elif isinstance(node, ast.FunctionDef):
            if node.name in {"get_app_db_connection", "get_derived_connection"}:
                items.append(f"[DEF_FUNCTION] {rel(path)}:{node.lineno} def {node.name}(...):")

    return items


def excerpt(text: str) -> list[str]:
    names = {"get_app_db_connection", "get_derived_connection", "connect_app"}
    lines = text.splitlines()
    selected: set[int] = set()

    for idx, line in enumerate(lines, start=1):
        if any(name in line for name in names):
            for n in range(max(1, idx - 4), min(len(lines), idx + 4) + 1):
                selected.add(n)

    if not selected:
        return ["Nenhum trecho relevante encontrado."]

    out: list[str] = []
    prev = None

    for n in sorted(selected):
        if prev is not None and n != prev + 1:
            out.append("...")
        out.append(f"{rel(TARGET)}:{n}: {lines[n - 1]}")
        prev = n

    return out


def insert_import(text: str) -> tuple[str, bool]:
    if IMPORT_LINE in text:
        return text, False

    marker = "import sqlite3\n"
    if marker in text:
        return text.replace(marker, marker + IMPORT_LINE + "\n", 1), True

    marker = "import json\n"
    if marker in text:
        return text.replace(marker, marker + IMPORT_LINE + "\n", 1), True

    return IMPORT_LINE + "\n" + text, True


def insert_alias_block(text: str) -> tuple[str, bool]:
    has_app = has_function(text, "get_app_db_connection")
    has_derived = has_function(text, "get_derived_connection")

    if has_app and has_derived:
        return text, False

    if has_app and not has_derived:
        block = '''

def get_derived_connection() -> sqlite3.Connection:
    """Alias legado preservado temporariamente para compatibilidade."""
    return get_app_db_connection()
'''
    elif not has_app and has_derived:
        block = '''

def get_app_db_connection() -> sqlite3.Connection:
    """Retorna conexao para o banco unico da aplicacao app.db."""
    return connect_app()
'''
    else:
        block = ALIAS_BLOCK

    marker = "\ndef _unwrap_aba("
    if marker in text:
        return text.replace(marker, block + marker, 1), True

    marker = "\ndef _table_columns("
    if marker in text:
        return text.replace(marker, block + marker, 1), True

    return text.rstrip() + block + "\n", True


def validate_import_contract() -> tuple[int, str, str]:
    code = r'''
from db.derived_repo import get_app_db_connection, get_derived_connection

assert callable(get_app_db_connection), "get_app_db_connection nao esta callable"
assert callable(get_derived_connection), "get_derived_connection nao esta callable"

print("[OK] imports callable em db.derived_repo")
'''

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        text=True,
    )

    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    before = safe_read(TARGET)

    before_has_import = IMPORT_LINE in before
    before_has_app = has_function(before, "get_app_db_connection")
    before_has_derived = has_function(before, "get_derived_connection")

    changed = False

    after, import_changed = insert_import(before)
    changed = changed or import_changed

    after, alias_changed = insert_alias_block(after)
    changed = changed or alias_changed

    ast_parse_ok = True
    syntax_error = ""

    try:
        ast.parse(after)
    except SyntaxError as exc:
        ast_parse_ok = False
        syntax_error = str(exc)

    if not ast_parse_ok:
        raise SystemExit(f"[ERRO] Alteracao geraria SyntaxError: {syntax_error}")

    if changed:
        TARGET.write_text(after, encoding="utf-8")

    final = safe_read(TARGET)

    after_has_import = IMPORT_LINE in final
    after_has_app = has_function(final, "get_app_db_connection")
    after_has_derived = has_function(final, "get_derived_connection")

    validation_rc, validation_stdout, validation_stderr = validate_import_contract()

    out: list[str] = []
    out.append("===== DATA =====")
    out.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out.append("")
    out.append("===== OBJETIVO =====")
    out.append("Criar contrato explicito get_app_db_connection em db/derived_repo.py.")
    out.append("Preservar get_derived_connection como alias legado temporario.")
    out.append("")
    out.append("===== ARQUIVO ALTERADO =====")
    out.append(f"- {rel(TARGET)}")
    out.append("")
    out.append("===== ESTADO ANTES =====")
    out.append(f"{IMPORT_LINE} presente: {before_has_import}")
    out.append(f"def get_app_db_connection presente: {before_has_app}")
    out.append(f"def get_derived_connection presente: {before_has_derived}")
    out.append("")
    out.append("===== ALTERACOES APLICADAS =====")
    out.append(f"import adicionado: {import_changed}")
    out.append(f"bloco de alias adicionado/ajustado: {alias_changed}")
    out.append(f"arquivo modificado: {changed}")
    out.append("")
    out.append("===== ESTADO DEPOIS =====")
    out.append(f"{IMPORT_LINE} presente: {after_has_import}")
    out.append(f"def get_app_db_connection presente: {after_has_app}")
    out.append(f"def get_derived_connection presente: {after_has_derived}")
    out.append("")
    out.append("===== RESUMO AST FINAL =====")
    ast_lines = ast_items(TARGET, final)
    if ast_lines:
        out.extend(ast_lines)
    else:
        out.append("Nenhum item AST relevante encontrado.")
    out.append("")
    out.append("===== TRECHO FINAL RELEVANTE =====")
    out.extend(excerpt(final))
    out.append("")
    out.append("===== VALIDACAO DE IMPORT =====")
    out.append(f"returncode: {validation_rc}")
    out.append(f"stdout: {validation_stdout}")
    out.append(f"stderr: {validation_stderr}")
    out.append("")
    out.append("===== DECISAO =====")

    if after_has_import and after_has_app and after_has_derived and validation_rc == 0:
        out.append("[OK] Contrato app_db criado e alias legado get_derived_connection preservado.")
        out.append("[OK] db.derived_repo exporta ambos os nomes esperados.")
    else:
        out.append("[ALERTA] Validacao incompleta. Revisar evidencia antes de prosseguir.")

    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")

    print("[OK] Fase 1F-D.10 concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
