from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "117_phase1f_d9_auditoria_derived_repo_contract.txt"

TARGET_FILES = [
    "db/derived_repo.py",
    "db/writer.py",
    "db/config.py",
    "domain/payoff_features.py",
    "services/derived_service.py",
    "scripts/run_derived_pipeline.py",
]

TARGET_NAMES = {
    "get_derived_connection",
    "get_app_db_connection",
    "connect_derived",
    "connect_app",
    "connect_app_db",
    "DERIVED_DB_PATH",
    "APP_DB_PATH",
}


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def ast_summary(path: Path, text: str) -> list[str]:
    lines: list[str] = []

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"[SYNTAX_ERROR] {rel(path)}: {exc}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name in TARGET_NAMES or path.as_posix().endswith("db/derived_repo.py"):
                lines.append(f"[DEF_FUNCTION] {rel(path)}:{node.lineno} def {node.name}(...):")

        elif isinstance(node, ast.AsyncFunctionDef):
            if node.name in TARGET_NAMES or path.as_posix().endswith("db/derived_repo.py"):
                lines.append(f"[DEF_ASYNC_FUNCTION] {rel(path)}:{node.lineno} async def {node.name}(...):")

        elif isinstance(node, ast.ClassDef):
            if path.as_posix().endswith("db/derived_repo.py"):
                lines.append(f"[DEF_CLASS] {rel(path)}:{node.lineno} class {node.name}:")

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name in TARGET_NAMES or alias.asname in TARGET_NAMES or path.as_posix().endswith("db/derived_repo.py"):
                    asname = f" as {alias.asname}" if alias.asname else ""
                    lines.append(
                        f"[IMPORT_FROM] {rel(path)}:{node.lineno} from {module} import {alias.name}{asname}"
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                if any(name in alias.name for name in TARGET_NAMES) or path.as_posix().endswith("db/derived_repo.py"):
                    asname = f" as {alias.asname}" if alias.asname else ""
                    lines.append(f"[IMPORT] {rel(path)}:{node.lineno} import {alias.name}{asname}")

        elif isinstance(node, ast.Assign):
            target_names: list[str] = []
            for target in node.targets:
                if isinstance(target, ast.Name):
                    target_names.append(target.id)
                elif isinstance(target, ast.Tuple):
                    for item in target.elts:
                        if isinstance(item, ast.Name):
                            target_names.append(item.id)

            for name in target_names:
                if name in TARGET_NAMES or name == "__all__" or path.as_posix().endswith("db/derived_repo.py"):
                    lines.append(f"[ASSIGN] {rel(path)}:{node.lineno} {name} = ...")

        elif isinstance(node, ast.Call):
            func_name = None
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr

            if func_name in TARGET_NAMES:
                lines.append(f"[CALL] {rel(path)}:{node.lineno} {func_name}(...)")

    return lines


def text_hits(path: Path, text: str) -> list[str]:
    lines: list[str] = []

    for lineno, line in enumerate(text.splitlines(), start=1):
        if any(name in line for name in TARGET_NAMES):
            lines.append(f"{rel(path)}:{lineno}: {line.rstrip()}")

    return lines


def source_excerpt(path: Path, text: str, radius: int = 5) -> list[str]:
    raw_lines = text.splitlines()
    hit_lines = set()

    for idx, line in enumerate(raw_lines, start=1):
        if any(name in line for name in TARGET_NAMES):
            for n in range(max(1, idx - radius), min(len(raw_lines), idx + radius) + 1):
                hit_lines.add(n)

    if not hit_lines:
        return ["Nenhum trecho relevante encontrado."]

    out: list[str] = []
    previous = None

    for n in sorted(hit_lines):
        if previous is not None and n != previous + 1:
            out.append("...")
        out.append(f"{rel(path)}:{n}: {raw_lines[n - 1]}")
        previous = n

    return out


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    out: list[str] = []
    out.append("===== DATA =====")
    out.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    out.append("")
    out.append("===== OBJETIVO =====")
    out.append("Auditar contrato real de db.derived_repo.get_derived_connection.")
    out.append("Esta fase nao altera codigo operacional.")
    out.append("")
    out.append("===== ARQUIVOS-ALVO =====")
    for item in TARGET_FILES:
        out.append(f"- {item}")
    out.append("")
    out.append("===== NOMES AUDITADOS =====")
    for name in sorted(TARGET_NAMES):
        out.append(f"- {name}")
    out.append("")

    found_files: list[Path] = []
    missing_files: list[str] = []

    for item in TARGET_FILES:
        path = ROOT / item
        if path.exists():
            found_files.append(path)
        else:
            missing_files.append(item)

    out.append("===== EXISTENCIA DOS ARQUIVOS =====")
    for path in found_files:
        out.append(f"[OK] {rel(path)}")
    for item in missing_files:
        out.append(f"[MISSING] {item}")
    out.append("")

    out.append("===== RESUMO AST =====")
    any_ast = False
    for path in found_files:
        text = safe_read(path)
        lines = ast_summary(path, text)
        if lines:
            any_ast = True
            out.append("")
            out.append(f"--- {rel(path)} ---")
            out.extend(lines)
    if not any_ast:
        out.append("Nenhum item AST relevante encontrado.")
    out.append("")

    out.append("===== OCORRENCIAS TEXTUAIS =====")
    any_hit = False
    for path in found_files:
        text = safe_read(path)
        lines = text_hits(path, text)
        if lines:
            any_hit = True
            out.append("")
            out.append(f"--- {rel(path)} ---")
            out.extend(lines)
    if not any_hit:
        out.append("Nenhuma ocorrencia textual encontrada.")
    out.append("")

    out.append("===== TRECHOS RELEVANTES =====")
    for path in found_files:
        text = safe_read(path)
        lines = source_excerpt(path, text)
        out.append("")
        out.append(f"--- {rel(path)} ---")
        out.extend(lines)
    out.append("")

    derived_repo = ROOT / "db" / "derived_repo.py"
    writer = ROOT / "db" / "writer.py"

    derived_repo_text = safe_read(derived_repo) if derived_repo.exists() else ""
    writer_text = safe_read(writer) if writer.exists() else ""

    has_def_get_derived = "def get_derived_connection" in derived_repo_text
    has_get_app_in_repo = "get_app_db_connection" in derived_repo_text
    has_connect_app_in_repo = "connect_app" in derived_repo_text
    has_connect_derived_in_repo = "connect_derived" in derived_repo_text
    writer_imports_get_derived = "from db.derived_repo import get_derived_connection" in writer_text
    writer_calls_get_derived = "get_derived_connection()" in writer_text

    out.append("===== ANALISE PRELIMINAR =====")
    out.append(f"db/derived_repo.py define get_derived_connection: {has_def_get_derived}")
    out.append(f"db/derived_repo.py menciona get_app_db_connection: {has_get_app_in_repo}")
    out.append(f"db/derived_repo.py menciona connect_app: {has_connect_app_in_repo}")
    out.append(f"db/derived_repo.py menciona connect_derived: {has_connect_derived_in_repo}")
    out.append(f"db/writer.py importa get_derived_connection de db.derived_repo: {writer_imports_get_derived}")
    out.append(f"db/writer.py chama get_derived_connection(): {writer_calls_get_derived}")
    out.append("")

    out.append("===== RECOMENDACAO =====")
    if has_def_get_derived and has_connect_app_in_repo:
        out.append("[CANDIDATO] get_derived_connection provavelmente pode virar alias legado para nome app_db, apos fase pequena com testes.")
    elif has_def_get_derived and has_connect_derived_in_repo:
        out.append("[CUIDADO] get_derived_connection existe, mas parece depender de connect_derived; renomeacao deve preservar alias legado.")
    elif not has_def_get_derived and writer_imports_get_derived:
        out.append("[ALERTA] db/writer.py importa get_derived_connection, mas a definicao nao foi detectada textualmente em db/derived_repo.py.")
        out.append("[ACAO] Verificar se ha import dinamico, reexport, erro latente ou definicao nao convencional.")
    else:
        out.append("[INFO] Situacao requer leitura da evidencia antes da proxima alteracao.")
    out.append("")

    out.append("===== DECISAO =====")
    out.append("[OK] Auditoria concluida sem alteracao operacional.")
    out.append("[PENDENTE] Decidir se D.10 cria alias app_db ou apenas documenta manutencao do contrato legado.")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")

    print("[OK] Fase 1F-D.9 auditoria concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
