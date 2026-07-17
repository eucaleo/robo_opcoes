from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re


ROOT = Path(".").resolve()
TARGET = ROOT / "services" / "pricing_execution_orchestration_service.py"
REPORT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
REPORT = REPORT_DIR / "RELATORIO_32_4_PATCH_WIRE_DERIVED_PAYOFF.md"


def fail(msg: str) -> None:
    raise SystemExit(f"ERRO: {msg}")


def backup_file(path: Path) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak_32_4_{ts}")
    backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return backup


def ensure_import(text: str) -> tuple[str, bool]:
    import_line = "from services.derived_payoff_persistence import DerivedPayoffPersistence\n"

    if import_line.strip() in text:
        return text, False

    marker = "from services.pricing_execution_persistence_service import"
    idx = text.find(marker)
    if idx == -1:
        fail("nao encontrei import de PricingExecutionPersistenceService")

    after = text.find("\n", idx)
    if after == -1:
        after = len(text)

    first_line = text[idx:after]
    insert_pos = after + 1

    if "(" in first_line and ")" not in first_line:
        depth = 0
        pos = idx
        while pos < len(text):
            ch = text[pos]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    nl = text.find("\n", pos)
                    insert_pos = len(text) if nl == -1 else nl + 1
                    break
            pos += 1

    text = text[:insert_pos] + import_line + text[insert_pos:]
    return text, True


def find_matching_paren(text: str, open_idx: int) -> int:
    depth = 0
    in_single = False
    in_double = False
    escaped = False

    for i in range(open_idx, len(text)):
        ch = text[i]

        if escaped:
            escaped = False
            continue

        if ch == "\\":
            escaped = True
            continue

        if ch == "'" and not in_double:
            in_single = not in_single
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            continue

        if in_single or in_double:
            continue

        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i

    fail("nao consegui localizar fechamento de PricingExecutionPersistenceService")


def patch_constructor_call(text: str) -> tuple[str, bool]:
    needle = "or PricingExecutionPersistenceService("
    idx = text.find(needle)

    if idx == -1:
        fail("nao encontrei chamada default or PricingExecutionPersistenceService")

    open_idx = idx + len("or PricingExecutionPersistenceService")
    close_idx = find_matching_paren(text, open_idx)

    call = text[idx:close_idx + 1]

    if "payoff_persistence_port" in call:
        return text, False

    line_start = text.rfind("\n", 0, idx) + 1
    line_end = text.find("\n", idx)
    if line_end == -1:
        line_end = len(text)

    line = text[line_start:line_end]
    base_indent = re.match(r"^(\s*)", line).group(1)
    arg_indent = base_indent + "    "

    compact = "or PricingExecutionPersistenceService()"

    if call.strip() == compact:
        replacement = (
            "or PricingExecutionPersistenceService(\n"
            f"{arg_indent}payoff_persistence_port=DerivedPayoffPersistence(),\n"
            f"{base_indent})"
        )
        return text[:idx] + replacement + text[close_idx + 1:], True

    insert_pos = text.find("\n", open_idx)

    if insert_pos == -1 or insert_pos > close_idx:
        replacement = (
            "or PricingExecutionPersistenceService(\n"
            f"{arg_indent}payoff_persistence_port=DerivedPayoffPersistence(),\n"
            f"{base_indent})"
        )
        return text[:idx] + replacement + text[close_idx + 1:], True

    insertion = f"\n{arg_indent}payoff_persistence_port=DerivedPayoffPersistence(),"
    return text[:insert_pos] + insertion + text[insert_pos:], True


def main() -> None:
    if not TARGET.exists():
        fail(f"arquivo nao encontrado: {TARGET}")

    original = TARGET.read_text(encoding="utf-8")
    backup = backup_file(TARGET)

    text, import_changed = ensure_import(original)
    text, call_changed = patch_constructor_call(text)

    if text == original:
        status = "sem alteracoes; wiring ja parecia aplicado"
    else:
        TARGET.write_text(text, encoding="utf-8")
        status = "patch aplicado"

    report = f"""# Relatorio 32.4 - Patch wiring DerivedPayoffPersistence

Arquivo alterado:
{TARGET.relative_to(ROOT)}

Backup:
{backup.relative_to(ROOT)}

Status:
{status}

Import DerivedPayoffPersistence inserido:
{import_changed}

Chamada PricingExecutionPersistenceService alterada:
{call_changed}

Intencao:

Conectar o fluxo atual:

PayoffRefreshCommandService
  -> PricingExecutionAppService
    -> PricingExecutionOrchestrationService
      -> PricingExecutionPersistenceService
        -> DerivedPayoffPersistence
          -> payoff_curve_points
          -> structure_decisions

Motivo:

PricingExecutionAppService usa PricingExecutionOrchestrationService.
O CanonicalPricingFacade ja tinha DerivedPayoffPersistence conectado, mas ele nao esta no caminho principal atual.
Este patch conecta DerivedPayoffPersistence no default wiring de PricingExecutionOrchestrationService.
"""

    REPORT.write_text(report, encoding="utf-8")
    print(f"OK: {status}")
    print(f"OK: relatorio gerado em {REPORT}")
    print(f"OK: backup criado em {backup}")


if __name__ == "__main__":
    main()
