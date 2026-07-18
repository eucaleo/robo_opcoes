from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
OUT = ROOT / "FRENTE_RTD_EXCEL_BTG_ONLINE" / "AUDITORIA_CENTRO_VERDADE_34"

FILES = {
    "payoff_refresh_command_service": ROOT / "services" / "payoff_refresh_command_service.py",
    "derived_payoff_persistence": ROOT / "services" / "derived_payoff_persistence.py",
    "pricing_execution_persistence_service": ROOT / "services" / "pricing_execution_persistence_service.py",
    "pricing_execution_orchestration_service": ROOT / "services" / "pricing_execution_orchestration_service.py",
    "canonical_pricing_facade": ROOT / "services" / "canonical_pricing_facade.py",
    "terminal_vwap_payoff_dark_panel": ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py",
    "recalculate_payoff_curve_points_once": ROOT / "scripts" / "recalculate_payoff_curve_points_once.py",
}

PATTERNS = {
    "comando_pricing": [
        r"PricingExecutionAppService",
        r"execute_pricing\s*\(",
        r"_ensure_active_structure",
        r"status\s*!=\s*[\"']active[\"']",
        r"payoff_curve_points",
        r"structure_decisions",
        r"warning",
        r"error",
        r"ok",
    ],
    "persistencia_derivada": [
        r"DerivedPayoffPersistence",
        r"_is_active_structure",
        r"status\s*==\s*[\"']active[\"']",
        r"payoff_curve_points",
        r"structure_decisions",
        r"insert_payoff",
        r"persist",
    ],
    "wiring": [
        r"payoff_persistence_port",
        r"DerivedPayoffPersistence",
        r"SystemSnapshotsRepository",
        r"PricingExecutionPersistenceService",
        r"execute_and_persist",
    ],
    "ui_proibidos": [
        r"execute_pricing\s*\(",
        r"INSERT\s+INTO\s+payoff_curve_points",
        r"INSERT\s+INTO\s+structure_decisions",
        r"subprocess\.run",
        r"subprocess\.Popen",
        r"os\.system",
        r"compute_payoff_from_canonical_input",
        r"_calculate_payoff_from_legs",
        r"_calculate_payoff_points_for_range",
        r"_calculate_leg_payoff",
        r"_collect_payoff_strikes",
        r"_calculate_payoff_spot_range",
    ],
    "script_paralelo": [
        r"maintenance",
        r"manuten",
        r"emerg",
        r"payoff_curve_points",
        r"INSERT",
        r"structure_legs",
        r"rtd_option_quotes",
        r"rtd_underlying_quotes",
    ],
}


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_matches(text: str, patterns: list[str]) -> list[str]:
    lines = text.splitlines()
    findings: list[str] = []

    for index, line in enumerate(lines, start=1):
        for pattern in patterns:
            if re.search(pattern, line, flags=re.IGNORECASE):
                findings.append(f"{index}: {line.rstrip()}")
                break

    return findings


def has(text: str, pattern: str) -> bool:
    return bool(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def write_excerpt(name: str, path: Path, patterns: list[str]) -> None:
    text = read(path)
    target = OUT / f"{name}_achados.txt"

    if not path.exists():
        target.write_text(f"Arquivo nao encontrado: {path}\n", encoding="utf-8")
        return

    findings = find_matches(text, patterns)
    content = [
        f"Arquivo: {path}",
        f"Gerado em: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "Achados:",
        "",
    ]

    if findings:
        content.extend(findings)
    else:
        content.append("Nenhum achado para os padroes informados.")

    target.write_text("\n".join(content) + "\n", encoding="utf-8")


def status_line(ok: bool, label: str, detail: str = "") -> str:
    marker = "OK" if ok else "ATENCAO"
    suffix = f" — {detail}" if detail else ""
    return f"- [{marker}] {label}{suffix}"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    texts = {name: read(path) for name, path in FILES.items()}

    write_excerpt(
        "01_payoff_refresh_command_service",
        FILES["payoff_refresh_command_service"],
        PATTERNS["comando_pricing"],
    )
    write_excerpt(
        "02_derived_payoff_persistence",
        FILES["derived_payoff_persistence"],
        PATTERNS["persistencia_derivada"],
    )
    write_excerpt(
        "03_pricing_execution_persistence_service",
        FILES["pricing_execution_persistence_service"],
        PATTERNS["wiring"],
    )
    write_excerpt(
        "04_pricing_execution_orchestration_service",
        FILES["pricing_execution_orchestration_service"],
        PATTERNS["wiring"],
    )
    write_excerpt(
        "05_canonical_pricing_facade",
        FILES["canonical_pricing_facade"],
        PATTERNS["wiring"],
    )
    write_excerpt(
        "06_terminal_vwap_payoff_dark_panel_ui",
        FILES["terminal_vwap_payoff_dark_panel"],
        PATTERNS["ui_proibidos"],
    )
    write_excerpt(
        "07_recalculate_payoff_curve_points_once_script",
        FILES["recalculate_payoff_curve_points_once"],
        PATTERNS["script_paralelo"],
    )

    svc = texts["payoff_refresh_command_service"]
    derived = texts["derived_payoff_persistence"]
    persistence = texts["pricing_execution_persistence_service"]
    orchestration = texts["pricing_execution_orchestration_service"]
    facade = texts["canonical_pricing_facade"]
    ui = texts["terminal_vwap_payoff_dark_panel"]
    script = texts["recalculate_payoff_curve_points_once"]

    checks: list[str] = []

    checks.append(status_line(
        FILES["payoff_refresh_command_service"].exists(),
        "PayoffRefreshCommandService existe",
        str(FILES["payoff_refresh_command_service"]),
    ))
    checks.append(status_line(
        has(svc, r"PricingExecutionAppService"),
        "PayoffRefreshCommandService referencia PricingExecutionAppService",
    ))
    checks.append(status_line(
        has(svc, r"execute_pricing\s*\("),
        "PayoffRefreshCommandService chama execute_pricing()",
    ))
    checks.append(status_line(
        has(svc, r"_ensure_active_structure") and has(svc, r"status\s*!=\s*[\"']active[\"']"),
        "PayoffRefreshCommandService bloqueia status diferente de active",
    ))
    checks.append(status_line(
        has(svc, r"payoff_curve_points"),
        "PayoffRefreshCommandService consulta payoff_curve_points",
    ))
    checks.append(status_line(
        has(svc, r"structure_decisions"),
        "PayoffRefreshCommandService consulta/valida structure_decisions",
    ))
    checks.append(status_line(
        has(svc, r"warning") and has(svc, r"error") and has(svc, r"ok"),
        "PayoffRefreshCommandService possui estados ok/warning/error",
    ))

    checks.append(status_line(
        has(derived, r"_is_active_structure") and has(derived, r"status\s*==\s*[\"']active[\"']"),
        "DerivedPayoffPersistence tem guard active",
    ))
    checks.append(status_line(
        has(derived, r"payoff_curve_points"),
        "DerivedPayoffPersistence referencia payoff_curve_points",
    ))
    checks.append(status_line(
        has(derived, r"structure_decisions"),
        "DerivedPayoffPersistence referencia structure_decisions",
    ))

    checks.append(status_line(
        has(persistence, r"payoff_persistence_port"),
        "PricingExecutionPersistenceService possui payoff_persistence_port",
    ))
    checks.append(status_line(
        has(orchestration, r"PricingExecutionPersistenceService"),
        "PricingExecutionOrchestrationService usa PricingExecutionPersistenceService",
    ))
    checks.append(status_line(
        has(facade, r"DerivedPayoffPersistence"),
        "canonical_pricing_facade referencia DerivedPayoffPersistence",
    ))

    ui_direct_pricing = has(ui, r"execute_pricing\s*\(")
    ui_direct_insert_payoff = has(ui, r"INSERT\s+INTO\s+payoff_curve_points")
    ui_direct_insert_decision = has(ui, r"INSERT\s+INTO\s+structure_decisions")
    ui_subprocess = has(ui, r"subprocess\.run|subprocess\.Popen|os\.system")

    checks.append(status_line(
        not ui_direct_pricing,
        "UI nao chama execute_pricing diretamente",
    ))
    checks.append(status_line(
        not ui_direct_insert_payoff,
        "UI nao faz INSERT direto em payoff_curve_points",
    ))
    checks.append(status_line(
        not ui_direct_insert_decision,
        "UI nao faz INSERT direto em structure_decisions",
    ))
    checks.append(status_line(
        not ui_subprocess,
        "UI nao chama subprocess/os.system",
    ))

    ui_local_calc_patterns = [
        r"_calculate_payoff_from_legs",
        r"_calculate_payoff_points_for_range",
        r"_calculate_leg_payoff",
        r"_collect_payoff_strikes",
        r"_calculate_payoff_spot_range",
    ]
    local_calc_found = any(has(ui, pattern) for pattern in ui_local_calc_patterns)

    checks.append(status_line(
        not local_calc_found,
        "UI sem metodos locais de calculo de payoff",
        "se ATENCAO, limpar somente apos backend validado",
    ))

    script_has_quarantine_header = has(script, r"maintenance|manuten|emerg|nao e fluxo oficial|não é fluxo oficial")

    checks.append(status_line(
        script_has_quarantine_header,
        "Script recalculate_payoff_curve_points_once possui aviso de manutencao/emergencia",
    ))

    summary = [
        "# Auditoria Centro de Verdade 34",
        "",
        f"Projeto: `{ROOT}`",
        f"Saida: `{OUT}`",
        f"Gerado em: `{datetime.now().isoformat(timespec='seconds')}`",
        "",
        "## Resultado dos checks",
        "",
        *checks,
        "",
        "## Leitura recomendada",
        "",
        "1. Abrir `01_payoff_refresh_command_service_achados.txt`.",
        "2. Confirmar se o comando chama `PricingExecutionAppService.execute_pricing()`.",
        "3. Abrir `02_derived_payoff_persistence_achados.txt`.",
        "4. Confirmar se a persistencia derivada gera/persiste `payoff_curve_points` e `structure_decisions`.",
        "5. Abrir `06_terminal_vwap_payoff_dark_panel_ui_achados.txt`.",
        "6. Se houver metodos `_calculate_*`, nao corrigir ainda antes do teste backend sem UI.",
        "",
        "## Regra de seguimento",
        "",
        "Nao criar novo motor de payoff.",
        "Nao criar outro comando paralelo.",
        "Nao mexer na UI antes de validar backend/comando oficial.",
        "",
    ]

    (OUT / "RESUMO_AUDITORIA_CENTRO_VERDADE_34.md").write_text(
        "\n".join(summary) + "\n",
        encoding="utf-8",
    )

    print(f"OK: auditoria gerada em {OUT}")
    print(f"Resumo: {OUT / 'RESUMO_AUDITORIA_CENTRO_VERDADE_34.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
