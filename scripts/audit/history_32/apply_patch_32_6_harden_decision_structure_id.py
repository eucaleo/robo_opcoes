from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path(".").resolve()
TARGET = ROOT / "services" / "derived_service.py"
REPORT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "RELATORIO_32_6_HARDEN_DECISION_STRUCTURE_ID.md"


def fail(msg: str) -> None:
    raise SystemExit("ERRO: " + msg)


def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + ".bak_32_6_" + ts)
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def find_function_block(text: str, name: str) -> tuple[int, int]:
    start = text.find("def " + name + "(")
    if start == -1:
        fail("função não encontrada: " + name)

    next_def = text.find("\ndef ", start + 1)
    next_class = text.find("\nclass ", start + 1)

    candidates = [i for i in (next_def, next_class) if i != -1]
    end = min(candidates) if candidates else len(text)
    return start, end


def patch_save_decision_from_canonical_payload(text: str) -> tuple[str, bool]:
    start, end = find_function_block(text, "save_decision_from_canonical_payload")
    block = text[start:end]

    marker = "    return save_decision(\n"
    if marker not in block:
        fail("não encontrei return save_decision em save_decision_from_canonical_payload")

    already = "Patch 32.6: garante structure_id no topo antes de delegar para save_decision"
    if already in block:
        return text, False

    snippet = (
        "    # Patch 32.6: garante structure_id no topo antes de delegar para save_decision.\n"
        "    if enriched_decision.get(\"structure_id\") is None and structure_id is not None:\n"
        "        enriched_decision[\"structure_id\"] = int(structure_id)\n"
        "\n"
        "    if enriched_decision.get(\"structure_id\") is None:\n"
        "        sid_from_meta = (enriched_decision.get(\"meta\") or {}).get(\"structure_id\")\n"
        "        if sid_from_meta is not None:\n"
        "            enriched_decision[\"structure_id\"] = int(sid_from_meta)\n"
        "\n"
        "    if enriched_decision.get(\"structure_id\") is None:\n"
        "        resolved_sid = _resolve_structure_id(storage_key)\n"
        "        if resolved_sid is not None:\n"
        "            enriched_decision[\"structure_id\"] = int(resolved_sid)\n"
        "\n"
    )

    pos = start + block.find(marker)
    return text[:pos] + snippet + text[pos:], True


def patch_save_decision(text: str) -> tuple[str, bool]:
    start, end = find_function_block(text, "save_decision")
    block = text[start:end]

    marker = "    with connect_app() as conn:\n"
    if marker not in block:
        fail("não encontrei with connect_app() em save_decision")

    already = "Patch 32.6: última barreira antes do insert em structure_decisions"
    if already in block:
        return text, False

    snippet = (
        "    # Patch 32.6: última barreira antes do insert em structure_decisions.\n"
        "    if enriched_decision.get(\"structure_id\") is None:\n"
        "        sid_from_meta = (enriched_decision.get(\"meta\") or {}).get(\"structure_id\")\n"
        "        if sid_from_meta is not None:\n"
        "            enriched_decision[\"structure_id\"] = int(sid_from_meta)\n"
        "\n"
        "    if enriched_decision.get(\"structure_id\") is None:\n"
        "        resolved_sid = _resolve_structure_id(storage_key)\n"
        "        if resolved_sid is not None:\n"
        "            enriched_decision[\"structure_id\"] = int(resolved_sid)\n"
        "\n"
    )

    pos = start + block.find(marker)
    return text[:pos] + snippet + text[pos:], True


def main() -> None:
    if not TARGET.exists():
        fail("arquivo não encontrado: " + str(TARGET))

    original = TARGET.read_text(encoding="utf-8")
    backup = backup_file(TARGET)

    text, changed_1 = patch_save_decision_from_canonical_payload(original)
    text, changed_2 = patch_save_decision(text)

    if text != original:
        TARGET.write_text(text, encoding="utf-8")
        status = "patch aplicado"
    else:
        status = "sem alterações; patch já parecia aplicado"

    report = (
        "# Relatório 32.6 - Harden decision structure_id\n\n"
        "- Arquivo alterado: services/derived_service.py\n"
        "- Backup: " + str(backup.relative_to(ROOT)) + "\n"
        "- Status: " + status + "\n"
        "- Patch em save_decision_from_canonical_payload: " + str(changed_1) + "\n"
        "- Patch em save_decision: " + str(changed_2) + "\n\n"
        "Motivo:\n"
        "O patch 32.5 garantiu structure_id em DerivedPayoffPersistence, mas a decisão ainda chegou ao insert final sem structure_id no topo de decision_dict.\n\n"
        "Erro observado:\n"
        "sqlite3.IntegrityError: NOT NULL constraint failed: structure_decisions.structure_id\n\n"
        "Correção:\n"
        "Adicionar barreiras em services/derived_service.py para garantir structure_id no topo de enriched_decision antes de chamar save_decision e antes do insert final em structure_decisions.\n\n"
        "Efeito esperado:\n"
        "structure_decisions deve aumentar após execução OK, junto com payoff_curve_points.\n"
    )

    REPORT.write_text(report, encoding="utf-8")

    print("OK: " + status)
    print("OK: relatorio gerado em " + str(REPORT))
    print("OK: backup criado em " + str(backup))


if __name__ == "__main__":
    main()
