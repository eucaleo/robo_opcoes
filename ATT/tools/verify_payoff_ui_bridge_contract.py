from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(errors: list[str], msg: str) -> None:
    errors.append(f"FAIL: {msg}")


def ok(lines: list[str], msg: str) -> None:
    lines.append(f"OK: {msg}")


def main() -> int:
    errors: list[str] = []
    lines: list[str] = []

    terminal_path = ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
    main_window_path = ROOT / "UI" / "main_window.py"
    ui_data_path = ROOT / "UI" / "models" / "ui_data.py"
    global_service_path = ROOT / "services" / "system_recalculation_command_service.py"

    for path in [terminal_path, main_window_path, ui_data_path, global_service_path]:
        if not path.exists():
            fail(errors, f"arquivo ausente: {path.relative_to(ROOT)}")

    if terminal_path.exists():
        text = terminal_path.read_text(encoding="utf-8")
        if "PayoffRefreshCommandService" in text:
            ok(lines, "painel terminal chama PayoffRefreshCommandService")
        else:
            fail(errors, "painel terminal nao chama PayoffRefreshCommandService")

        if "_refresh_open_structure_payoff_via_backend" in text:
            ok(lines, "painel terminal possui ponte explicita UI para backend")
        else:
            fail(errors, "painel terminal sem ponte explicita UI para backend")

        if "compute_payoff_from_canonical_input" in text:
            fail(errors, "UI terminal importa ou chama calculo de payoff local")
        else:
            ok(lines, "UI terminal sem compute_payoff_from_canonical_input")

    if main_window_path.exists():
        text = main_window_path.read_text(encoding="utf-8")
        if "PayoffRefreshCommandService" in text and "refresh_payoff_for_structure" in text:
            ok(lines, "MainWindow.recalculate_structure usa comando oficial")
        else:
            fail(errors, "MainWindow.recalculate_structure nao usa comando oficial")

    if ui_data_path.exists():
        text = ui_data_path.read_text(encoding="utf-8")
        if "def invalidate_payoff_cache(" in text:
            ok(lines, "UIData expoe invalidate_payoff_cache")
        else:
            fail(errors, "UIData nao expoe invalidate_payoff_cache")

    if global_service_path.exists():
        text = global_service_path.read_text(encoding="utf-8")
        if "SystemRecalculationCommandService" in text and "recalculate_all" in text:
            ok(lines, "servico global de recalculo existe")
        else:
            fail(errors, "servico global sem contrato minimo")

        if "PayoffRefreshCommandService" in text:
            ok(lines, "servico global delega ao comando oficial por estrutura")
        else:
            fail(errors, "servico global nao delega ao PayoffRefreshCommandService")

    print("== Verificacao contrato UI payoff bridge ==")
    for line in lines:
        print(line)

    if errors:
        print("")
        for error in errors:
            print(error)
        return 1

    print("")
    print("OK: contrato UI payoff bridge atendido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
