from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def collect_python_files(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return [
        path
        for path in base.rglob("*.py")
        if ".git" not in path.parts
        and "FRENTE_RTD_EXCEL_BTG_ONLINE" not in path.parts
        and "__pycache__" not in path.parts
    ]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def assert_no_forbidden_ui_scope(errors: list[str]) -> None:
    ui_files = collect_python_files(ROOT / "UI")

    forbidden_literal = [
        "compute_payoff_from_canonical_input",
        "_calculate_payoff_from_legs",
        "_calculate_payoff_points_for_range",
        "_calculate_leg_payoff",
        "_collect_payoff_strikes",
        "_calculate_payoff_spot_range",
        "subprocess.run",
        "subprocess.Popen",
        "os.system",
        "os.popen",
        "popen(",
        "recalculate_payoff_curve_points_once",
    ]

    forbidden_sql_regex = [
        r"\bINSERT\s+INTO\s+payoff_curve_points\b",
        r"\bUPDATE\s+payoff_curve_points\b",
        r"\bDELETE\s+FROM\s+payoff_curve_points\b",
        r"\bINSERT\s+INTO\s+structure_decisions\b",
        r"\bUPDATE\s+structure_decisions\b",
        r"\bDELETE\s+FROM\s+structure_decisions\b",
        r"\bCREATE\s+TABLE\b[\s\S]{0,300}\bstructure_decisions\b",
        r"\bCREATE\s+TABLE\b[\s\S]{0,300}\bpayoff_curve_points\b",
    ]

    for path in ui_files:
        text = read_text(path)
        rel = path.relative_to(ROOT)

        for token in forbidden_literal:
            if token in text:
                fail(errors, f"UI contem token proibido: {rel}: {token}")

        for pattern in forbidden_sql_regex:
            if re.search(pattern, text, flags=re.IGNORECASE):
                fail(errors, f"UI contem SQL proibido: {rel}: {pattern}")


def assert_command_service_contract(errors: list[str]) -> None:
    path = ROOT / "services" / "payoff_refresh_command_service.py"
    text = read_text(path)

    if not text:
        fail(errors, "services/payoff_refresh_command_service.py nao encontrado.")
        return

    required_tokens = [
        "PricingExecutionAppService",
        "execute_pricing",
        "payoff_curve_points",
        "structure_decisions",
        "payoff_points_count",
        "latest_payoff_timestamp",
    ]

    for token in required_tokens:
        if token not in text:
            fail(errors, f"PayoffRefreshCommandService sem token esperado: {token}")

    status_tokens = ["ok", "warning", "error"]
    missing_status = [token for token in status_tokens if token not in text]
    if missing_status:
        fail(
            errors,
            "PayoffRefreshCommandService pode nao retornar contrato ok/warning/error. "
            f"Ausentes: {', '.join(missing_status)}",
        )

    if "active" not in text:
        fail(errors, "PayoffRefreshCommandService sem guard aparente de structures.status == active.")


def assert_backend_wiring(errors: list[str]) -> None:
    files = [
        ROOT / "services" / "pricing_execution_persistence_service.py",
        ROOT / "services" / "pricing_execution_orchestration_service.py",
        ROOT / "services" / "canonical_pricing_facade.py",
    ]

    combined = "\n".join(read_text(path) for path in files)

    if "DerivedPayoffPersistence" not in combined:
        fail(errors, "DerivedPayoffPersistence nao aparece no wiring backend principal.")

    if "payoff_persistence_port" not in combined:
        fail(errors, "payoff_persistence_port nao aparece no wiring backend principal.")

    if "PricingExecutionPersistenceService" not in combined:
        fail(errors, "PricingExecutionPersistenceService nao aparece no wiring backend principal.")


def assert_latest_snapshot_reading(errors: list[str]) -> None:
    files = [
        ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py",
        ROOT / "UI" / "models" / "ui_data.py",
        ROOT / "UI" / "components" / "details_panel.py",
    ]

    combined = "\n".join(read_text(path) for path in files)

    has_latest_timestamp = (
        "MAX(timestamp)" in combined
        or "ORDER BY timestamp DESC" in combined
        or "latest_payoff_timestamp" in combined
    )

    if not has_latest_timestamp:
        fail(errors, "Leitura UI nao evidencia uso de ultimo timestamp/snapshot.")


def assert_script_quarantine(errors: list[str]) -> None:
    path = ROOT / "scripts" / "recalculate_payoff_curve_points_once.py"
    text = read_text(path)

    if not text:
        return

    expected_markers = [
        "ferramenta de manutencao",
        "ferramenta de manutenção",
        "nao e fluxo oficial",
        "não é fluxo oficial",
        "PayoffRefreshCommandService",
    ]

    lowered = text.lower()

    if not any(marker in lowered for marker in expected_markers):
        fail(
            errors,
            "scripts/recalculate_payoff_curve_points_once.py existe, "
            "mas nao tem cabecalho claro de quarentena/manutencao.",
        )


def main() -> int:
    errors: list[str] = []

    assert_no_forbidden_ui_scope(errors)
    assert_command_service_contract(errors)
    assert_backend_wiring(errors)
    assert_latest_snapshot_reading(errors)
    assert_script_quarantine(errors)

    if errors:
        print("ERRO: verificacao de centro de verdade falhou.")
        print()
        for index, error in enumerate(errors, start=1):
            print(f"{index}. {error}")
        return 1

    print("OK: escopo centro de verdade payoff validado.")
    print("OK: UI sem calculo local proibido, subprocess ou escrita direta.")
    print("OK: comando oficial e wiring backend encontrados.")
    print("OK: leitura por ultimo snapshot evidenciada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
