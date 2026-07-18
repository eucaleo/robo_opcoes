from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re


ROOT = Path(".").resolve()
TARGET = ROOT / "services" / "derived_payoff_persistence.py"
REPORT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "RELATORIO_32_5_FIX_DECISION_STRUCTURE_ID.md"


def fail(msg: str) -> None:
    raise SystemExit("ERRO: " + msg)


def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + ".bak_32_5_" + ts)
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def find_persist_decision_region(text: str) -> tuple[int, int]:
    m = re.search(r"^[ \t]*def _persist_decision\(", text, flags=re.MULTILINE)
    if not m:
        fail("nao encontrei def _persist_decision em derived_payoff_persistence.py")

    start = m.start()
    line_start = text.rfind("\n", 0, start) + 1
    def_line = text[line_start:text.find("\n", start)]
    indent = re.match(r"^([ \t]*)", def_line).group(1)

    next_m = re.search(
        r"^" + re.escape(indent) + r"def\s+",
        text[m.end():],
        flags=re.MULTILINE,
    )

    if next_m:
        end = m.end() + next_m.start()
    else:
        end = len(text)

    return start, end


def patch_text(text: str) -> tuple[str, bool]:
    start, end = find_persist_decision_region(text)
    region = text[start:end]

    if 'decision_dict["structure_id"] = structure_id' in region:
        return text, False

    if "decision_dict.setdefault(\"structure_id\"" in region:
        return text, False

    marker = "save_decision_from_canonical_payload("
    rel_call = region.find(marker)
    if rel_call == -1:
        fail("nao encontrei chamada save_decision_from_canonical_payload dentro de _persist_decision")

    call_abs = start + rel_call
    insert_abs = text.rfind("\n", 0, call_abs) + 1

    call_line_end = text.find("\n", call_abs)
    if call_line_end == -1:
        call_line_end = len(text)

    call_line = text[insert_abs:call_line_end]
    indent = re.match(r"^([ \t]*)", call_line).group(1)

    block = (
        indent + "if isinstance(decision_dict, dict) and decision_dict.get(\"structure_id\") is None:\n"
        + indent + "    decision_dict[\"structure_id\"] = structure_id\n"
        + "\n"
    )

    return text[:insert_abs] + block + text[insert_abs:], True


def main() -> None:
    if not TARGET.exists():
        fail("arquivo nao encontrado: " + str(TARGET))

    original = TARGET.read_text(encoding="utf-8")
    backup = backup_file(TARGET)

    patched, changed = patch_text(original)

    if changed:
        TARGET.write_text(patched, encoding="utf-8")
        status = "patch aplicado"
    else:
        status = "sem alteracoes; structure_id ja parecia tratado"

    report = (
        "# Relatorio 32.5 - Fix decision structure_id\n\n"
        "- Arquivo alterado: " + str(TARGET.relative_to(ROOT)) + "\n"
        "- Backup: " + str(backup.relative_to(ROOT)) + "\n"
        "- Status: " + status + "\n"
        "- Correcao: garantir decision_dict structure_id antes de salvar structure_decisions\n\n"
        "Motivo:\n"
        "O payoff passou a ser salvo apos o patch 32.4, mas a decisao falhou com NOT NULL constraint failed em structure_decisions.structure_id.\n\n"
        "Efeito esperado:\n"
        "A chamada save_decision_from_canonical_payload passa a receber decision_dict com structure_id preenchido.\n"
    )

    REPORT.write_text(report, encoding="utf-8")

    print("OK: " + status)
    print("OK: relatorio gerado em " + str(REPORT))
    print("OK: backup criado em " + str(backup))


if __name__ == "__main__":
    main()
