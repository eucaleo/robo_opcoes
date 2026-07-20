from __future__ import annotations

from pathlib import Path
from datetime import datetime

ROOT = Path(".").resolve()
TARGET = ROOT / "services" / "derived_service.py"
REPORT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "RELATORIO_32_7_RECOVER_STRUCTURE_ID_IN_SAVE_DECISION.md"

def fail(msg: str) -> None:
    raise SystemExit("ERRO: " + msg)

def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + ".bak_32_7_" + ts)
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

    if "Patch 32.7: espelha structure_id no meta antes de delegar para save_decision" in block:
        return text, False

    marker = "    return save_decision(\n"
    if marker not in block:
        fail("não encontrei return save_decision em save_decision_from_canonical_payload")

    snippet = '''    # Patch 32.7: espelha structure_id no meta antes de delegar para save_decision.
    if enriched_decision.get("structure_id") is not None:
        _sid_32_7 = int(enriched_decision.get("structure_id"))
        enriched_decision["structure_id"] = _sid_32_7

        _meta_32_7 = enriched_decision.get("meta")
        if not isinstance(_meta_32_7, dict):
            _meta_32_7 = {}
            enriched_decision["meta"] = _meta_32_7

        _meta_32_7["structure_id"] = _sid_32_7

    '''

    pos = start + block.find(marker)
    return text[:pos] + snippet + text[pos:], True

def patch_save_decision(text: str) -> tuple[str, bool]:
    start, end = find_function_block(text, "save_decision")
    block = text[start:end]

    if "Patch 32.7: recupera structure_id do payload original antes do insert" in block:
        return text, False

    marker = "    with connect_app() as conn:\n"
    if marker not in block:
        fail("não encontrei with connect_app() em save_decision")

    snippet = '''    # Patch 32.7: recupera structure_id do payload original antes do insert.
    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision")
        if isinstance(_src_32_7, dict):
            _sid_32_7 = _src_32_7.get("structure_id")
            if _sid_32_7 is not None:
                enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision_dict")
        if isinstance(_src_32_7, dict):
            _sid_32_7 = _src_32_7.get("structure_id")
            if _sid_32_7 is not None:
                enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision")
        if isinstance(_src_32_7, dict):
            _meta_32_7 = _src_32_7.get("meta")
            if isinstance(_meta_32_7, dict):
                _sid_32_7 = _meta_32_7.get("structure_id")
                if _sid_32_7 is not None:
                    enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _src_32_7 = locals().get("decision_dict")
        if isinstance(_src_32_7, dict):
            _meta_32_7 = _src_32_7.get("meta")
            if isinstance(_meta_32_7, dict):
                _sid_32_7 = _meta_32_7.get("structure_id")
                if _sid_32_7 is not None:
                    enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is None:
        _sid_32_7 = None
        try:
            _sid_32_7 = _resolve_structure_id(storage_key)
        except Exception:
            _sid_32_7 = None

        if _sid_32_7 is not None:
            enriched_decision["structure_id"] = int(_sid_32_7)

    if enriched_decision.get("structure_id") is not None:
        _sid_32_7 = int(enriched_decision.get("structure_id"))
        enriched_decision["structure_id"] = _sid_32_7

        _meta_32_7 = enriched_decision.get("meta")
        if not isinstance(_meta_32_7, dict):
            _meta_32_7 = {}
            enriched_decision["meta"] = _meta_32_7

        _meta_32_7["structure_id"] = _sid_32_7

    '''

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

    report = "# Relatório 32.7 - Recover structure_id in save_decision\n\n"
    report += "Arquivo alterado: services/derived_service.py\n"
    report += "Backup: " + str(backup.relative_to(ROOT)) + "\n"
    report += "Status: " + status + "\n"
    report += "Patch em save_decision_from_canonical_payload: " + str(changed_1) + "\n"
    report += "Patch em save_decision: " + str(changed_2) + "\n\n"
    report += "Motivo:\n"
    report += "O patch 32.6 ainda permitiu que structure_id se perdesse dentro de save_decision.\n\n"
    report += "Correção:\n"
    report += "Recuperar structure_id diretamente do payload original decision, de decision_dict, de meta e por último via _resolve_structure_id.\n\n"
    report += "Efeito esperado:\n"
    report += "structure_decisions deve aumentar após execução OK.\n"

    REPORT.write_text(report, encoding="utf-8")

    print("OK: " + status)
    print("OK: relatorio gerado em " + str(REPORT))
    print("OK: backup criado em " + str(backup))

if __name__ == "__main__":
    main()
