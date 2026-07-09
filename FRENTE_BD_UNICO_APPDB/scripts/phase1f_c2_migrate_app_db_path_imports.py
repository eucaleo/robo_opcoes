from __future__ import annotations

from datetime import datetime
from io import StringIO
from pathlib import Path
import ast
import tokenize


ROOT = Path(__file__).resolve().parents[2]
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"

OPERATIONAL_DIRS = [
    "ATT",
    "UI",
    "db",
    "domain",
    "repositories",
    "scripts",
    "services",
]

CONFIG = ROOT / "db" / "config.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def iter_py_files() -> list[Path]:
    files: list[Path] = []
    for rel in OPERATIONAL_DIRS:
        base = ROOT / rel
        if not base.exists():
            continue
        files.extend(
            p for p in base.rglob("*.py")
            if "__pycache__" not in p.parts
        )
    return sorted(set(files))


def imports_derived_db_path_from_config(path: Path, text: str) -> bool:
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module == "db.config":
                for alias in node.names:
                    if alias.name == "DERIVED_DB_PATH":
                        return True
    return False


def replace_name_token(text: str, old: str, new: str) -> tuple[str, int]:
    stream = StringIO(text)
    tokens = []
    count = 0

    for tok in tokenize.generate_tokens(stream.readline):
        if tok.type == tokenize.NAME and tok.string == old:
            tok = tokenize.TokenInfo(
                tok.type,
                new,
                tok.start,
                tok.end,
                tok.line,
            )
            count += 1
        tokens.append(tok)

    return tokenize.untokenize(tokens), count


def find_token_hits(path: Path, token_name: str) -> list[str]:
    hits: list[str] = []

    try:
        text = read(path)
    except UnicodeDecodeError:
        return hits

    stream = StringIO(text)
    try:
        for tok in tokenize.generate_tokens(stream.readline):
            if tok.type == tokenize.NAME and tok.string == token_name:
                line = tok.start[0]
                snippet = text.splitlines()[line - 1].strip()
                rel = path.relative_to(ROOT).as_posix()
                hits.append(f"{rel}:{line}: {snippet}")
    except tokenize.TokenError:
        return hits

    return hits


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    report: list[str] = []
    report.append("===== DATA =====")
    report.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    report.append("")
    report.append("===== OBJETIVO =====")
    report.append("Migrar imports internos controlados de DERIVED_DB_PATH para APP_DB_PATH.")
    report.append("Preservar DERIVED_DB_PATH apenas como alias legado em db/config.py.")
    report.append("Nao alterar strings/comentarios; substituicao feita apenas em tokens Python NAME.")
    report.append("Nao renomear arquivos, modulos, classes ou funcoes.")
    report.append("")

    py_files = iter_py_files()

    report.append("===== ESCOPO OPERACIONAL =====")
    for rel in OPERATIONAL_DIRS:
        report.append(rel)
    report.append("")
    report.append("===== TOTAL PY VARREDOS =====")
    report.append(str(len(py_files)))
    report.append("")

    changed_files: list[str] = []
    skipped_syntax: list[str] = []
    candidates: list[str] = []

    for path in py_files:
        if path == CONFIG:
            continue

        text = read(path)

        try:
            ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            skipped_syntax.append(f"{path.relative_to(ROOT).as_posix()}: {exc}")
            continue

        if not imports_derived_db_path_from_config(path, text):
            continue

        rel = path.relative_to(ROOT).as_posix()
        candidates.append(rel)

        new_text, replacements = replace_name_token(
            text,
            "DERIVED_DB_PATH",
            "APP_DB_PATH",
        )

        if replacements > 0 and new_text != text:
            write(path, new_text)
            changed_files.append(f"{rel} ({replacements} tokens)")

    report.append("===== CANDIDATOS COM IMPORT DE DERIVED_DB_PATH A PARTIR DE db.config =====")
    if candidates:
        report.extend(candidates)
    else:
        report.append("Nenhum candidato encontrado.")
    report.append("")

    report.append("===== ARQUIVOS ALTERADOS =====")
    if changed_files:
        report.extend(changed_files)
    else:
        report.append("Nenhum arquivo alterado.")
    report.append("")

    report.append("===== ARQUIVOS IGNORADOS POR SYNTAXERROR =====")
    if skipped_syntax:
        report.extend(skipped_syntax)
    else:
        report.append("Nenhum.")
    report.append("")

    # Revalida config canonico.
    config_text = read(CONFIG) if CONFIG.exists() else ""
    checks = {
        "APP_DB_PATH presente em db/config.py": "APP_DB_PATH" in config_text,
        "DERIVED_DB_PATH alias legado preservado": "DERIVED_DB_PATH = APP_DB_PATH" in config_text,
        "dados/app.db presente em db/config.py": "dados/app.db" in config_text,
    }

    report.append("===== VERIFICACOES DE db/config.py =====")
    for name, ok in checks.items():
        report.append(f"{'[OK]' if ok else '[FALHA]'} {name}: {ok}")
    report.append("")

    # Auditoria de token remanescente fora de db/config.py.
    remaining_hits: list[str] = []
    for path in py_files:
        if path == CONFIG:
            continue
        remaining_hits.extend(find_token_hits(path, "DERIVED_DB_PATH"))

    remaining_out = EVID / "62_phase1f_c2_remaining_derived_db_path_tokens.txt"
    remaining_report: list[str] = []
    remaining_report.append("===== DATA =====")
    remaining_report.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    remaining_report.append("")
    remaining_report.append("===== OBJETIVO =====")
    remaining_report.append("Listar tokens Python remanescentes DERIVED_DB_PATH em codigo operacional, exceto db/config.py.")
    remaining_report.append("db/config.py e excecao esperada porque preserva alias legado DERIVED_DB_PATH = APP_DB_PATH.")
    remaining_report.append("")
    remaining_report.append("===== RESULTADO =====")
    if remaining_hits:
        remaining_report.extend(remaining_hits)
    else:
        remaining_report.append("Nenhum token DERIVED_DB_PATH remanescente fora de db/config.py.")
    remaining_report.append("")
    remaining_out.write_text("\n".join(remaining_report), encoding="utf-8")

    report.append("===== TOKENS DERIVED_DB_PATH REMANESCENTES FORA DE db/config.py =====")
    if remaining_hits:
        report.extend(remaining_hits)
    else:
        report.append("Nenhum token DERIVED_DB_PATH remanescente fora de db/config.py.")
    report.append("")

    report.append("===== DECISAO =====")
    if all(checks.values()) and not remaining_hits:
        report.append("[OK] Imports internos controlados migrados para APP_DB_PATH.")
        report.append("[OK] DERIVED_DB_PATH permanece somente como alias legado em db/config.py.")
        report.append("[OK] Pode seguir para testes, compile e auditoria literal.")
    else:
        report.append("[BLOQUEIO] Existem falhas ou tokens remanescentes. Revisar antes de prosseguir.")
    report.append("")

    out = EVID / "61_phase1f_c2_migrate_app_db_path_imports.txt"
    out.write_text("\n".join(report), encoding="utf-8")

    print("[OK] Fase 1F-C.2 migracao de imports executada.")
    print(f"Gerado: {out.relative_to(ROOT).as_posix()}")
    print(f"Gerado: {remaining_out.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
