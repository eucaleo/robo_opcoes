from pathlib import Path
import re
from datetime import datetime

ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_FILES = [
    "services/payoff_refresh_command_service.py",
    "services/derived_payoff_persistence.py",
    "services/pricing_execution_persistence_service.py",
    "services/pricing_execution_orchestration_service.py",
    "services/canonical_pricing_facade.py",
    "UI/components/terminal_vwap_payoff_dark_panel.py",
    "scripts/recalculate_payoff_curve_points_once.py",
]

UI_FORBIDDEN_PATTERNS = [
    r"compute_payoff_from_canonical_input",
    r"_calculate_payoff_from_legs",
    r"_calculate_payoff_points_for_range",
    r"_calculate_leg_payoff",
    r"_collect_payoff_strikes",
    r"_calculate_payoff_spot_range",
    r"subprocess\.run",
    r"subprocess\.Popen",
    r"os\.system",
    r"INSERT\s+INTO\s+payoff_curve_points",
    r"INSERT\s+INTO\s+structure_decisions",
]

BACKEND_EXPECTED_PATTERNS = {
    "services/payoff_refresh_command_service.py": [
        r"PricingExecutionAppService",
        r"execute_pricing\s*\(",
        r"payoff_curve_points",
        r"structure_decisions",
        r"MAX\s*\(\s*timestamp\s*\)|ORDER\s+BY\s+timestamp\s+DESC",
        r"status",
        r"warning",
        r"error",
    ],
    "services/derived_payoff_persistence.py": [
        r"payoff_curve_points",
        r"structure_decisions",
        r"INSERT\s+INTO\s+payoff_curve_points",
        r"INSERT\s+INTO\s+structure_decisions",
        r"status\s*=\s*[\"']active[\"']|status.*active",
    ],
    "services/pricing_execution_persistence_service.py": [
        r"payoff_persistence_port",
        r"DerivedPayoffPersistence|payoff_persistence",
        r"pricing_executions",
        r"structure_snapshots|system_snapshots",
    ],
    "services/pricing_execution_orchestration_service.py": [
        r"DerivedPayoffPersistence",
        r"PricingExecutionPersistenceService",
        r"payoff_persistence_port",
    ],
}

def read_file(rel_path: str) -> str:
    path = ROOT / rel_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")

def grep_context(text: str, pattern: str, context: int = 2):
    lines = text.splitlines()
    regex = re.compile(pattern, re.IGNORECASE)
    hits = []

    for idx, line in enumerate(lines, start=1):
        if regex.search(line):
            start = max(1, idx - context)
            end = min(len(lines), idx + context)
            snippet = []
            for line_no in range(start, end + 1):
                marker = ">>" if line_no == idx else "  "
                snippet.append(f"{marker} {line_no}: {lines[line_no - 1]}")
            hits.append("\n".join(snippet))

    return hits

def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))

def write_text(path: Path, content: str):
    path.write_text(content, encoding="utf-8")

def audit_file_existence():
    rows = []
    for rel_path in TARGET_FILES:
        path = ROOT / rel_path
        rows.append(
            f"| `{rel_path}` | {'OK' if path.exists() else 'NÃO ENCONTRADO'} |"
        )
    return "\n".join(rows)

def audit_backend_contracts():
    sections = []

    for rel_path, patterns in BACKEND_EXPECTED_PATTERNS.items():
        text = read_file(rel_path)
        sections.append(f"## `{rel_path}`\n")

        if not text:
            sections.append("Arquivo não encontrado.\n")
            continue

        for pattern in patterns:
            hits = count_pattern(text, pattern)
            status = "OK" if hits > 0 else "NÃO ENCONTRADO"
            sections.append(f"- `{pattern}`: **{status}** ({hits})")

        sections.append("")

    return "\n".join(sections)

def audit_ui_forbidden():
    rel_path = "UI/components/terminal_vwap_payoff_dark_panel.py"
    text = read_file(rel_path)
    sections = [f"## `{rel_path}`\n"]

    if not text:
        return "Arquivo de UI não encontrado.\n"

    total_hits = 0

    for pattern in UI_FORBIDDEN_PATTERNS:
        hits = grep_context(text, pattern, context=2)
        total_hits += len(hits)

        sections.append(f"### Padrão proibido: `{pattern}`")
        sections.append(f"Ocorrências: **{len(hits)}**\n")

        for i, hit in enumerate(hits[:10], start=1):
            sections.append(f"#### Ocorrência {i}")
            sections.append("```text")
            sections.append(hit)
            sections.append("```")

        if len(hits) > 10:
            sections.append(f"_Mais {len(hits) - 10} ocorrência(s) omitida(s)._")

        sections.append("")

    sections.insert(
        1,
        f"Total de ocorrências proibidas ou suspeitas na UI: **{total_hits}**\n",
    )

    return "\n".join(sections)

def audit_latest_snapshot_reads():
    patterns = [
        r"MAX\s*\(\s*timestamp\s*\)",
        r"ORDER\s+BY\s+timestamp\s+DESC",
        r"latest.*timestamp",
        r"_fetch_latest_canonical_payoff_timestamp",
        r"_load_persisted_payoff_points",
    ]

    files = [
        "UI/models/ui_data.py",
        "UI/components/details_panel.py",
        "UI/components/terminal_vwap_payoff_dark_panel.py",
    ]

    sections = []

    for rel_path in files:
        text = read_file(rel_path)
        sections.append(f"## `{rel_path}`\n")

        if not text:
            sections.append("Arquivo não encontrado.\n")
            continue

        for pattern in patterns:
            hits = count_pattern(text, pattern)
            status = "OK" if hits > 0 else "NÃO ENCONTRADO"
            sections.append(f"- `{pattern}`: **{status}** ({hits})")

        sections.append("")

    return "\n".join(sections)

def audit_script_quarantine():
    rel_path = "scripts/recalculate_payoff_curve_points_once.py"
    text = read_file(rel_path)

    if not text:
        return "Script não encontrado.\n"

    patterns = [
        r"structure_legs",
        r"rtd_option_quotes",
        r"rtd_underlying_quotes",
        r"payoff_curve_points",
        r"INSERT\s+INTO\s+payoff_curve_points",
        r"calculate|calcular|payoff",
        r"maintenance|legacy|emergência|emergencia",
        r"não é fluxo oficial|nao e fluxo oficial",
    ]

    sections = [f"## `{rel_path}`\n"]

    for pattern in patterns:
        hits = count_pattern(text, pattern)
        status = "OK" if hits > 0 else "NÃO ENCONTRADO"
        sections.append(f"- `{pattern}`: **{status}** ({hits})")

    return "\n".join(sections)

def audit_duplicate_terminal_blocks():
    rel_path = "UI/components/terminal_vwap_payoff_dark_panel.py"
    text = read_file(rel_path)

    if not text:
        return "Arquivo de UI não encontrado.\n"

    patterns = [
        r"payoff_points\s*=\s*payload\s*\[\s*[\"']payoff_points[\"']\s*\]",
        r"self\._update_kpis\s*\(",
        r"self\._render_charts\s*\(",
        r"self\._render_alerts\s*\(",
        r"def\s+_load_payoff_points\s*\(",
        r"def\s+_calculate_payoff_points_for_range\s*\(",
    ]

    sections = [f"## `{rel_path}`\n"]

    for pattern in patterns:
        hits = grep_context(text, pattern, context=1)
        sections.append(f"### `{pattern}`")
        sections.append(f"Ocorrências: **{len(hits)}**\n")

        for i, hit in enumerate(hits[:20], start=1):
            sections.append(f"#### Ocorrência {i}")
            sections.append("```text")
            sections.append(hit)
            sections.append("```")

        sections.append("")

    return "\n".join(sections)

def main():
    now = datetime.now().isoformat(timespec="seconds")

    report = []
    report.append("# Rodada 32.1 — Auditoria Pós-Patch / Centro de Verdade")
    report.append("")
    report.append(f"Gerado em: `{now}`")
    report.append("")
    report.append("## Arquivos auditados")
    report.append("")
    report.append("| Arquivo | Status |")
    report.append("|---|---|")
    report.append(audit_file_existence())
    report.append("")
    report.append("# 1. Contratos backend")
    report.append(audit_backend_contracts())
    report.append("")
    report.append("# 2. Padrões proibidos ou suspeitos na UI")
    report.append(audit_ui_forbidden())
    report.append("")
    report.append("# 3. Leituras de último snapshot/timestamp")
    report.append(audit_latest_snapshot_reads())
    report.append("")
    report.append("# 4. Script paralelo de recálculo")
    report.append(audit_script_quarantine())
    report.append("")
    report.append("# 5. Possível duplicação no painel terminal")
    report.append(audit_duplicate_terminal_blocks())
    report.append("")
    report.append("# Conclusão operacional")
    report.append("")
    report.append("- Se o backend não gerar `payoff_curve_points`, corrigir contrato de persistência antes da UI.")
    report.append("- Se o backend gerar payoff corretamente, bloquear/remover cálculo local da UI.")
    report.append("- O script `recalculate_payoff_curve_points_once.py` deve ser manutenção/legado, não fluxo oficial.")
    report.append("- Não criar outro serviço de comando se `PayoffRefreshCommandService` já existir.")
    report.append("")

    write_text(OUT_DIR / "RELATORIO_32_1_AUDITORIA_POS_PATCH.md", "\n".join(report))

    print("OK: auditoria gerada em AUDITORIA_POS_PATCH_32/RELATORIO_32_1_AUDITORIA_POS_PATCH.md")

if __name__ == "__main__":
    main()
