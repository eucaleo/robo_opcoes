from __future__ import annotations

from collections import Counter
from datetime import datetime
from io import StringIO
from pathlib import Path
import tokenize


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "UI" / "models" / "ui_data.py"
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "71_phase1f_d1_rename_ui_data_app_db_identifiers.txt"


OLD_SIG = "def __init__(self, derived_db_path: Optional[Path] = None):"
NEW_SIG = "def __init__(self, app_db_path: Optional[Path] = None, derived_db_path: Optional[Path] = None):"

COMPAT_BLOCK = (
    "        if app_db_path is None and derived_db_path is not None:\n"
    "            app_db_path = derived_db_path\n"
)

REPLACEMENTS = [
    ("self.derived_db_path", "self.app_db_path"),
    ("Path(derived_db_path).resolve()", "Path(app_db_path).resolve()"),
    ("if derived_db_path", "if app_db_path"),
    ("_connect_derived_threadsafe", "_connect_app_threadsafe"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def count_name_tokens(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for tok in tokenize.generate_tokens(StringIO(text).readline):
        if tok.type == tokenize.NAME:
            counts[tok.string] += 1
    return counts


def insert_compat_block(text: str) -> tuple[str, bool]:
    if COMPAT_BLOCK in text:
        return text, False

    lines = text.splitlines(keepends=True)
    out: list[str] = []
    inserted = False

    for line in lines:
        out.append(line)
        if NEW_SIG in line and not inserted:
            out.append(COMPAT_BLOCK)
            inserted = True

    return "".join(out), inserted


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    before = read(TARGET)
    after = before

    changes: list[str] = []
    errors: list[str] = []

    if OLD_SIG in after:
        after = after.replace(OLD_SIG, NEW_SIG, 1)
        changes.append("assinatura __init__ migrada para app_db_path com alias derived_db_path")
    elif NEW_SIG in after:
        changes.append("assinatura __init__ ja estava migrada")
    else:
        errors.append("assinatura esperada do __init__ nao encontrada")

    after, inserted = insert_compat_block(after)
    if inserted:
        changes.append("bloco de compatibilidade derived_db_path -> app_db_path inserido")
    elif COMPAT_BLOCK in after:
        changes.append("bloco de compatibilidade ja presente")

    for old, new in REPLACEMENTS:
        count = after.count(old)
        if count:
            after = after.replace(old, new)
            changes.append(f"{old} -> {new}: {count} substituicao(oes)")
        else:
            changes.append(f"{old}: nenhuma ocorrencia encontrada")

    if errors:
        changed = False
    else:
        changed = after != before
        if changed:
            write(TARGET, after)

    final_text = read(TARGET)
    counts = count_name_tokens(final_text)

    checks = {
        "arquivo alterado ou ja conforme": not errors,
        "self.derived_db_path ausente": "self.derived_db_path" not in final_text,
        "_connect_derived_threadsafe ausente": "_connect_derived_threadsafe" not in final_text,
        "self.app_db_path presente": "self.app_db_path" in final_text,
        "_connect_app_threadsafe presente": "_connect_app_threadsafe" in final_text,
        "assinatura compat app_db_path + derived_db_path presente": NEW_SIG in final_text,
        "bloco compatibilidade presente": COMPAT_BLOCK in final_text,
        "token DERIVED_DB_PATH nao introduzido": counts["DERIVED_DB_PATH"] == 0,
    }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("===== DATA =====")
    lines.append(now)
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Renomear identificadores internos de UI/models/ui_data.py para app_db_path.")
    lines.append("Preservar compatibilidade do parametro legado derived_db_path no construtor.")
    lines.append("Nao renomear modulo, classe ou teste nesta fase.")
    lines.append("")
    lines.append("===== ALVO =====")
    lines.append(TARGET.relative_to(ROOT).as_posix())
    lines.append("")
    lines.append("===== ALTERACOES =====")
    for change in changes:
        lines.append(change)
    if not changes:
        lines.append("Nenhuma alteracao registrada.")
    lines.append("")
    lines.append("===== ERROS =====")
    if errors:
        for error in errors:
            lines.append(f"[ERRO] {error}")
    else:
        lines.append("Nenhum.")
    lines.append("")
    lines.append("===== CONTAGEM DE TOKENS RELEVANTES EM UI/models/ui_data.py =====")
    for token in [
        "derived_db_path",
        "app_db_path",
        "_connect_derived_threadsafe",
        "_connect_app_threadsafe",
        "DERIVED_DB_PATH",
    ]:
        lines.append(f"{token}: {counts[token]}")
    lines.append("")
    lines.append("===== VERIFICACOES =====")
    for name, ok in checks.items():
        lines.append(f"{'[OK]' if ok else '[FALHA]'} {name}: {ok}")
    lines.append("")
    lines.append("===== DECISAO =====")
    if errors or not all(checks.values()):
        lines.append("[BLOQUEIO] Falha na migracao interna de UIDataModel.")
    else:
        lines.append("[OK] UIDataModel usa app_db_path internamente.")
        lines.append("[OK] Parametro legado derived_db_path preservado como compatibilidade.")
        lines.append("[OK] Pode seguir para testes e compile.")
    lines.append("")

    write(OUT, "\n".join(lines))

    print("[OK] Fase 1F-D.1 renomeacao interna em UI/models/ui_data.py concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
