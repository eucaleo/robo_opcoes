from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path.cwd()
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
OUT_DIR.mkdir(parents=True, exist_ok=True)

UI_ROOT = ROOT / "UI"
TERMINAL_PANEL = UI_ROOT / "components" / "terminal_vwap_payoff_dark_panel.py"

REPORT_JSON = OUT_DIR / "RELATORIO_32_12_AUDIT_UI_LOCAL_PAYOFF_SCOPE.json"
REPORT_MD = OUT_DIR / "RELATORIO_32_12_AUDIT_UI_LOCAL_PAYOFF_SCOPE.md"

LOCAL_CALC_TOKENS = [
    "_calculate_payoff_from_legs",
    "_calculate_payoff_points_for_range",
    "_calculate_leg_payoff",
    "_collect_payoff_strikes",
    "_calculate_payoff_spot_range",
    "compute_payoff_from_canonical_input",
]

HARD_FORBIDDEN_TOKENS = [
    "execute_pricing(",
    "subprocess.run",
    "subprocess.Popen",
    "os.system",
]

SQL_FORBIDDEN_PATTERNS = [
    re.compile(r"insert\s+into\s+payoff_curve_points", re.IGNORECASE),
    re.compile(r"insert\s+into\s+structure_decisions", re.IGNORECASE),
    re.compile(r"update\s+payoff_curve_points", re.IGNORECASE),
    re.compile(r"update\s+structure_decisions", re.IGNORECASE),
    re.compile(r"delete\s+from\s+payoff_curve_points", re.IGNORECASE),
    re.compile(r"delete\s+from\s+structure_decisions", re.IGNORECASE),
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        return str(path).replace("\\", "/")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def scan_ui() -> tuple[list[dict], list[dict], list[dict]]:
    local_hits: list[dict] = []
    hard_hits: list[dict] = []
    sql_hits: list[dict] = []

    if not UI_ROOT.exists():
        return local_hits, hard_hits, sql_hits

    for path in sorted(UI_ROOT.rglob("*.py")):
        text = read_text(path)
        lines = text.splitlines()

        for index, line in enumerate(lines, start=1):
            low = line.lower()

            for token in LOCAL_CALC_TOKENS:
                if token.lower() in low:
                    local_hits.append(
                        {
                            "file": rel(path),
                            "line": index,
                            "token": token,
                            "text": line.strip()[:240],
                        }
                    )

            for token in HARD_FORBIDDEN_TOKENS:
                if token.lower() in low:
                    hard_hits.append(
                        {
                            "file": rel(path),
                            "line": index,
                            "token": token,
                            "text": line.strip()[:240],
                        }
                    )

            for pattern in SQL_FORBIDDEN_PATTERNS:
                if pattern.search(line):
                    sql_hits.append(
                        {
                            "file": rel(path),
                            "line": index,
                            "pattern": pattern.pattern,
                            "text": line.strip()[:240],
                        }
                    )

    return local_hits, hard_hits, sql_hits


def find_callers_in_terminal() -> list[dict]:
    text = read_text(TERMINAL_PANEL)
    if not text:
        return []

    callers: list[dict] = []
    lines = text.splitlines()
    for index, line in enumerate(lines, start=1):
        if "_calculate_payoff_points_for_range(" in line:
            callers.append(
                {
                    "file": rel(TERMINAL_PANEL),
                    "line": index,
                    "text": line.strip()[:240],
                }
            )
    return callers


local_hits, hard_hits, sql_hits = scan_ui()
terminal_callers = find_callers_in_terminal()

status = "ok"
notes: list[str] = []

if hard_hits or sql_hits:
    status = "error"
    notes.append("UI possui chamadas ou escritas proibidas para o fluxo oficial.")

if local_hits:
    if status != "error":
        status = "warning"
    notes.append("UI ainda possui calculo local ou fallback de payoff.")

checks = {
    "ui_root_exists": UI_ROOT.exists(),
    "terminal_panel_exists": TERMINAL_PANEL.exists(),
    "local_calc_hits_count": len(local_hits),
    "hard_forbidden_hits_count": len(hard_hits),
    "sql_forbidden_hits_count": len(sql_hits),
    "terminal_calculate_payoff_points_for_range_occurrences": len(terminal_callers),
    "execute_pricing_direct_in_ui": any(item["token"] == "execute_pricing(" for item in hard_hits),
    "direct_sql_write_payoff_in_ui": bool(sql_hits),
}

report = {
    "status": status,
    "objective": "Auditar UI para localizar calculo local de payoff, fallback e chamadas proibidas.",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "checks": checks,
    "local_calc_hits": local_hits,
    "hard_forbidden_hits": hard_hits,
    "sql_forbidden_hits": sql_hits,
    "terminal_callers": terminal_callers,
    "notes": notes,
    "conclusion": (
        "A UI deve apenas chamar o comando oficial para recalcular e depois reler snapshot persistido. "
        "Calculo local e fallback devem ser removidos ou bloqueados em etapa posterior."
    ),
}

REPORT_JSON.write_text(
    json.dumps(report, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

md_lines = [
    "# Relatorio 32.12 - Auditoria UI escopo payoff local",
    "",
    f"Status: {status}",
    "",
    "Objetivo",
    "",
    "Auditar a UI para localizar calculo local de payoff, fallback e chamadas proibidas.",
    "",
    "Checks",
    "",
]

for key, value in checks.items():
    md_lines.append(f"- {key}: {value}")

md_lines.extend(
    [
        "",
        "Resumo",
        "",
        f"- Ocorrencias de calculo local: {len(local_hits)}",
        f"- Ocorrencias proibidas fortes: {len(hard_hits)}",
        f"- Escrita SQL proibida na UI: {len(sql_hits)}",
        f"- Ocorrencias de _calculate_payoff_points_for_range no painel terminal: {len(terminal_callers)}",
        "",
    ]
)

if local_hits:
    md_lines.append("Calculo local ou fallback encontrado")
    md_lines.append("")
    for item in local_hits[:120]:
        md_lines.append(
            f"- {item['file']}:{item['line']} | {item['token']} | {item['text']}"
        )
    md_lines.append("")

if hard_hits:
    md_lines.append("Chamadas proibidas fortes encontradas")
    md_lines.append("")
    for item in hard_hits[:120]:
        md_lines.append(
            f"- {item['file']}:{item['line']} | {item['token']} | {item['text']}"
        )
    md_lines.append("")

if sql_hits:
    md_lines.append("Escrita SQL proibida encontrada")
    md_lines.append("")
    for item in sql_hits[:120]:
        md_lines.append(
            f"- {item['file']}:{item['line']} | {item['pattern']} | {item['text']}"
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
        "1. Se houver somente warning por calculo local, preparar patch de bloqueio da UI.",
        "2. Se houver error por execute_pricing, subprocess ou SQL de escrita, corrigir antes de prosseguir.",
        "3. Nao criar motor novo e nao alterar backend validado sem nova evidencia.",
        "",
    ]
)

REPORT_MD.write_text("\n".join(md_lines), encoding="utf-8")

print(f"OK: relatorio JSON gerado em {REPORT_JSON}")
print(f"OK: relatorio MD gerado em {REPORT_MD}")
print(f"Status 32.12 audit: {status}")
