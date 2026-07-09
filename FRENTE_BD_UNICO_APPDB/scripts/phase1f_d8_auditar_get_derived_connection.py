from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "115_phase1f_d8_auditoria_get_derived_connection.txt"

TARGETS = {
    "get_derived_connection",
    "get_app_db_connection",
    "connect_derived",
    "connect_app_db",
    "connect_app",
}


def iter_py_files() -> list[Path]:
    ignored_parts = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        "node_modules",
    }

    files: list[Path] = []
    for path in ROOT.rglob("*.py"):
        if any(part in ignored_parts for part in path.parts):
            continue
        files.append(path)

    return sorted(files)


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def collect_text_hits(files: list[Path]) -> dict[str, list[tuple[Path, int, str]]]:
    hits: dict[str, list[tuple[Path, int, str]]] = {name: [] for name in TARGETS}

    for path in files:
        text = safe_read(path)
        for lineno, line in enumerate(text.splitlines(), start=1):
            for name in TARGETS:
                if name in line:
                    hits[name].append((path, lineno, line.rstrip()))

    return hits


def collect_defs_and_imports(files: list[Path]) -> list[str]:
    lines: list[str] = []

    for path in files:
        text = safe_read(path)
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            rel = path.relative_to(ROOT).as_posix()
            lines.append(f"[SYNTAX_ERROR] {rel}: {exc}")
            continue

        rel = path.relative_to(ROOT).as_posix()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name in TARGETS:
                lines.append(f"[DEF_FUNCTION] {rel}:{node.lineno} def {node.name}(...):")

            elif isinstance(node, ast.AsyncFunctionDef) and node.name in TARGETS:
                lines.append(f"[DEF_ASYNC_FUNCTION] {rel}:{node.lineno} async def {node.name}(...):")

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    if alias.name in TARGETS or alias.asname in TARGETS:
                        imported = alias.name
                        asname = f" as {alias.asname}" if alias.asname else ""
                        lines.append(
                            f"[IMPORT_FROM] {rel}:{node.lineno} from {module} import {imported}{asname}"
                        )

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if any(name in alias.name for name in TARGETS):
                        asname = f" as {alias.asname}" if alias.asname else ""
                        lines.append(f"[IMPORT] {rel}:{node.lineno} import {alias.name}{asname}")

            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in TARGETS:
                        lines.append(f"[ASSIGN] {rel}:{node.lineno} {target.id} = ...")

    return lines


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    files = iter_py_files()
    hits = collect_text_hits(files)
    defs_imports = collect_defs_and_imports(files)

    out: list[str] = []

    out.append("===== DATA =====")
    out.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out.append("")
    out.append("===== OBJETIVO =====")
    out.append("Auditar contrato de get_derived_connection antes de qualquer renomeacao.")
    out.append("Esta fase nao altera codigo operacional.")
    out.append("")
    out.append("===== ALVOS AUDITADOS =====")
    for name in sorted(TARGETS):
        out.append(f"- {name}")
    out.append("")

    out.append("===== DEFINICOES / IMPORTS / ASSIGNMENTS AST =====")
    if defs_imports:
        out.extend(defs_imports)
    else:
        out.append("Nenhuma definicao/import/assignment AST encontrada para os alvos.")
    out.append("")

    out.append("===== OCORRENCIAS TEXTUAIS =====")
    for name in sorted(TARGETS):
        items = hits[name]
        out.append("")
        out.append(f"--- {name}: {len(items)} ocorrencia(s) textual(is) ---")
        if not items:
            out.append("Nenhuma.")
            continue

        for path, lineno, line in items:
            rel = path.relative_to(ROOT).as_posix()
            out.append(f"{rel}:{lineno}: {line}")

    out.append("")
    out.append("===== ANALISE PRELIMINAR =====")
    gd = hits["get_derived_connection"]
    ga = hits["get_app_db_connection"]

    if gd and not ga:
        out.append("[INFO] get_derived_connection existe, mas nao foi encontrado get_app_db_connection.")
        out.append("[RECOMENDACAO] Antes de renomear consumidores, criar funcao nova app_db com alias legado.")
    elif gd and ga:
        out.append("[INFO] get_derived_connection e get_app_db_connection aparecem no codigo.")
        out.append("[RECOMENDACAO] Verificar se get_derived_connection ja pode ser reduzido a alias legado.")
    elif not gd:
        out.append("[INFO] get_derived_connection nao foi encontrado em arquivos Python auditados.")
        out.append("[RECOMENDACAO] Nada a migrar neste alvo.")
    else:
        out.append("[INFO] Situacao inconclusiva.")

    out.append("")
    out.append("===== DECISAO =====")
    out.append("[OK] Auditoria concluida sem alteracao operacional.")
    out.append("[PENDENTE] Decidir proxima fase com base nesta evidencia.")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")

    print("[OK] Fase 1F-D.8 auditoria concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
