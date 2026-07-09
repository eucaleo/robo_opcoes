from __future__ import annotations

from collections import Counter
from datetime import datetime
from io import StringIO
from pathlib import Path
import tokenize


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "scripts" / "validate_derived_db.py"
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "92_phase1f_d4_rename_validate_script_find_app_db.txt"


REPLACEMENTS = [
    ("_find_derived_db", "_find_app_db"),
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


def main() -> None:
    EVID.mkdir(parents=True, exist_ok=True)

    before = read(TARGET)
    after = before

    changes: list[str] = []

    for old, new in REPLACEMENTS:
        count = after.count(old)
        if count:
            after = after.replace(old, new)
        changes.append(f"{old} -> {new}: {count} substituicao(oes)")

    changed = after != before
    if changed:
        write(TARGET, after)

    final_text = read(TARGET)
    counts = count_name_tokens(final_text)

    checks = {
        "_find_derived_db ausente": counts["_find_derived_db"] == 0,
        "_find_app_db presente": counts["_find_app_db"] >= 1,
        "DERIVED_DB_PATH nao introduzido no arquivo": counts["DERIVED_DB_PATH"] == 0,
    }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("===== DATA =====")
    lines.append(now)
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Renomear helper privado em scripts/validate_derived_db.py.")
    lines.append("Trocar _find_derived_db por _find_app_db em ponto interno isolado.")
    lines.append("Nao alterar nomes de modulo, contratos publicos, aliases de config ou compatibilidade.")
    lines.append("")
    lines.append("===== ALVO =====")
    lines.append(TARGET.relative_to(ROOT).as_posix())
    lines.append("")
    lines.append("===== ALTERACOES =====")
    for change in changes:
        lines.append(change)
    lines.append("")
    lines.append("===== CONTAGEM DE TOKENS RELEVANTES EM scripts/validate_derived_db.py =====")
    for token in [
        "_find_derived_db",
        "_find_app_db",
        "DERIVED_DB_PATH",
    ]:
        lines.append(f"{token}: {counts[token]}")
    lines.append("")
    lines.append("===== VERIFICACOES =====")
    for name, ok in checks.items():
        lines.append(f"{'[OK]' if ok else '[FALHA]'} {name}: {ok}")
    lines.append("")
    lines.append("===== DECISAO =====")
    if all(checks.values()):
        lines.append("[OK] validate_derived_db.py usa _find_app_db no helper privado migrado.")
        lines.append("[OK] Nenhum DERIVED_DB_PATH foi introduzido.")
        lines.append("[OK] Pode seguir para testes, compile e reauditoria.")
    else:
        lines.append("[BLOQUEIO] Falha na renomeacao controlada do helper privado.")
    lines.append("")

    write(OUT, "\n".join(lines))

    print("[OK] Fase 1F-D.4 renomeacao interna em scripts/validate_derived_db.py concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
