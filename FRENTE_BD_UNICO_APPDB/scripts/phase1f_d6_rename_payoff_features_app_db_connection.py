from __future__ import annotations

from collections import Counter
from datetime import datetime
from io import StringIO
from pathlib import Path
import tokenize


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "domain" / "payoff_features.py"
EVID = ROOT / "FRENTE_BD_UNICO_APPDB" / "evidencias"
OUT = EVID / "106_phase1f_d6_rename_payoff_features_app_db_connection.txt"


REPLACEMENTS = [
    ("get_derived_db_connection", "get_app_db_connection"),
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

    if after != before:
        write(TARGET, after)

    final_text = read(TARGET)
    counts = count_name_tokens(final_text)

    checks = {
        "get_derived_db_connection ausente": counts["get_derived_db_connection"] == 0,
        "get_app_db_connection presente": counts["get_app_db_connection"] >= 1,
        "DERIVED_DB_PATH nao introduzido no arquivo": counts["DERIVED_DB_PATH"] == 0,
    }

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("===== DATA =====")
    lines.append(now)
    lines.append("")
    lines.append("===== OBJETIVO =====")
    lines.append("Renomear helper interno em domain/payoff_features.py.")
    lines.append("Trocar get_derived_db_connection por get_app_db_connection.")
    lines.append("Nao alterar nomes de modulo, contratos publicos, aliases de config ou compatibilidade.")
    lines.append("")
    lines.append("===== ALVO =====")
    lines.append(TARGET.relative_to(ROOT).as_posix())
    lines.append("")
    lines.append("===== ALTERACOES =====")
    for change in changes:
        lines.append(change)
    lines.append("")
    lines.append("===== CONTAGEM DE TOKENS RELEVANTES EM domain/payoff_features.py =====")
    for token in [
        "get_derived_db_connection",
        "get_app_db_connection",
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
        lines.append("[OK] payoff_features.py usa get_app_db_connection no helper migrado.")
        lines.append("[OK] Nenhum DERIVED_DB_PATH foi introduzido.")
        lines.append("[OK] Pode seguir para testes, compile e reauditoria.")
    else:
        lines.append("[BLOQUEIO] Falha na renomeacao controlada do helper.")
    lines.append("")

    write(OUT, "\n".join(lines))

    print("[OK] Fase 1F-D.6 renomeacao interna em domain/payoff_features.py concluida.")
    print(f"Gerado: {OUT.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
