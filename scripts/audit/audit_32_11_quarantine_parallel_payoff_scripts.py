from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = ROOT / "scripts" / "recalculate_payoff_curve_points_once.py"
UI_ROOT = ROOT / "UI"

REPORT_JSON = OUT_DIR / "RELATORIO_32_11_AUDIT_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.json"
REPORT_MD = OUT_DIR / "RELATORIO_32_11_AUDIT_QUARANTINE_PARALLEL_PAYOFF_SCRIPTS.md"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def find_occurrences(base: Path, needles: list[str]) -> list[dict]:
    results: list[dict] = []
    if not base.exists():
        return results

    for path in sorted(base.rglob("*.py")):
        text = read_text(path)
        if not text:
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines, start=1):
            normalized = line.lower()
            for needle in needles:
                if needle.lower() in normalized:
                    results.append(
                        {
                            "file": rel(path),
                            "line": index,
                            "needle": needle,
                            "text": line.strip()[:240],
                        }
                    )
    return results


target_text = read_text(TARGET)

script_checks = {
    "target_exists": TARGET.exists(),
    "has_maintenance_header": "ATENCAO - MANUTENCAO / EMERGENCIA" in target_text,
    "mentions_not_official_flow": "NAO E FLUXO OFICIAL" in target_text,
    "mentions_payoff_refresh_command_service": "PayoffRefreshCommandService" in target_text,
    "reads_structure_legs": "structure_legs" in target_text,
    "reads_rtd_option_quotes": "rtd_option_quotes" in target_text,
    "reads_rtd_underlying_quotes": "rtd_underlying_quotes" in target_text,
    "mentions_payoff_curve_points": "payoff_curve_points" in target_text,
    "mentions_structure_decisions": "structure_decisions" in target_text,
    "has_active_guard": "status" in target_text and "active" in target_text,
}

ui_references = find_occurrences(
    UI_ROOT,
    [
        "recalculate_payoff_curve_points_once",
        "subprocess.run",
        "subprocess.Popen",
        "os.system",
    ],
)

ui_calls_parallel_script = [
    item
    for item in ui_references
    if item["needle"] == "recalculate_payoff_curve_points_once"
]

ui_subprocess_usage = [
    item
    for item in ui_references
    if item["needle"] in {"subprocess.run", "subprocess.Popen", "os.system"}
]

status = "ok"
notes: list[str] = []

if not TARGET.exists():
    status = "error"
    notes.append("Script paralelo nao encontrado.")
elif not script_checks["has_maintenance_header"]:
    status = "warning"
    notes.append("Script existe, mas ainda nao possui cabecalho formal de quarentena.")

if ui_calls_parallel_script:
    status = "error"
    notes.append("UI referencia diretamente o script paralelo.")

if ui_subprocess_usage:
    if status != "error":
        status = "warning"
    notes.append("UI contem uso de subprocess ou os.system. Validar se nao chama fluxo paralelo.")

report = {
    "status": status,
    "objective": "Auditar script paralelo de payoff e confirmar se deve ser tratado como manutencao ou emergencia.",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "target": rel(TARGET),
    "checks": script_checks,
    "ui_references": ui_references,
    "ui_calls_parallel_script": ui_calls_parallel_script,
    "ui_subprocess_usage": ui_subprocess_usage,
    "notes": notes,
    "conclusion": (
        "Script paralelo deve permanecer fora do fluxo oficial. "
        "Fluxo oficial: UI -> PayoffRefreshCommandService -> PricingExecutionAppService."
    ),
}

REPORT_JSON.write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

md_lines = [
    "# Relatorio 32.11 - Auditoria quarentena scripts paralelos de payoff",
    "",
    f"Status: {status}",
    "",
    "Objetivo",
    "",
    "Auditar o script paralelo de payoff e confirmar se ele esta isolado do fluxo oficial.",
    "",
    "Arquivo auditado",
    "",
    f"- {rel(TARGET)}",
    "",
    "Checks",
    "",
]

for key, value in script_checks.items():
    md_lines.append(f"- {key}: {value}")

md_lines.extend(
    [
        "",
        "Referencias na UI",
        "",
        f"- Total encontradas: {len(ui_references)}",
        f"- Chamadas diretas ao script paralelo: {len(ui_calls_parallel_script)}",
        f"- Uso de subprocess ou os.system na UI: {len(ui_subprocess_usage)}",
        "",
    ]
)

if ui_references:
    md_lines.append("Ocorrencias principais")
    md_lines.append("")
    for item in ui_references[:80]:
        md_lines.append(
            f"- {item['file']}:{item['line']} | {item['needle']} | {item['text']}"
        )
    md_lines.append("")

md_lines.extend(
    [
        "Conclusao",
        "",
        report["conclusion"],
        "",
        "Proxima etapa recomendada",
        "",
        "1. Se nao houver cabecalho de quarentena, aplicar patch 32.11.",
        "2. Confirmar que a UI nao chama script paralelo.",
        "3. Avancar para auditoria 32.12 da UI antes de qualquer limpeza.",
        "",
    ]
)

REPORT_MD.write_text("\n".join(md_lines), encoding="utf-8")

print(f"OK: relatorio JSON gerado em {REPORT_JSON}")
print(f"OK: relatorio MD gerado em {REPORT_MD}")
print(f"Status 32.11 audit: {status}")
