from __future__ import annotations

from collections import Counter
from datetime import datetime
from io import StringIO
from pathlib import Path
import tokenize


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "UI" / "components" / "details_panel.py"
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "78_phase1f_d2_rename_details_panel_app_db_path_identifiers.txt"


REPLACEMENTS = [
    ("_is_derived_db_path", "_is_app_db_path"),
    ("_derived_db_path", "_app_db_path"),
    ("derived_explicit", "app_explicit"),
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
        "_derived_db_path ausente": counts["_derived_db_path"] == 0,
        "_app_db_path presente": counts["_app_db_path"] >= 1,
        "_is_derived_db_path ausente": counts["_is_derived_db_path"] == 0,
        "_is_app_db_path presente": counts["_is_app_db_path"] >= 1,
        "derived_explicit ausente": counts["derived_explicit"] == 0,
        "app_explicit presente": counts["app_explicit"] >= 1,
        "DERIVED_DB_PATH nao introduzido no arquivo": counts["DERIVED_DB_PATH"] == 0,
    }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("===== DATA =====")
    lines.append(now)
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Renomear identificadores privados/locais em UI/components/details_panel.py.")
    lines.append("Trocar nomenclatura derived_db_path para app_db_path nos pontos internos seguros.")
    lines.append("Nao alterar classes publicas, modulos, aliases de config ou contratos de compatibilidade.")
    lines.append("")
    lines.append("===== ALVO =====")
    lines.append(TARGET.relative_to(ROOT).as_posix())
    lines.append("")
    lines.append("===== ALTERACOES =====")
    for change in changes:
        lines.append(change)
    lines.append("")
    lines.append("===== CONTAGEM DE TOKENS RELEVANTES EM UI/components/details_panel.py =====")
    for token in [
        "_derived_db_path",
        "_app_db_path",
        "_is_derived_db_path",
        "_is_app_db_path",
        "derived_explicit",
        "app_explicit",
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
        lines.append("[OK] DetailsPanel usa app_db_path nos identificadores privados/locais migrados.")
        lines.append("[OK] Nenhum DERIVED_DB_PATH foi introduzido.")
        lines.append("[OK] Pode seguir para testes, compile e reauditoria.")
    else:
        lines.append("[BLOQUEIO] Falha na renomeacao controlada de DetailsPanel.")
    lines.append("")

    write(OUT, "\n".join(lines))

    print("[OK] Fase 1F-D.2 renomeacao interna em UI/components/details_panel.py concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
