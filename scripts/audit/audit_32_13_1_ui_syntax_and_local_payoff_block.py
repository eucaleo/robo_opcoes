from __future__ import annotations

import ast
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET = PROJECT_ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
OUT_DIR = PROJECT_ROOT / "AUDITORIA_POS_PATCH_32"

REPORT_JSON = OUT_DIR / "RELATORIO_32_13_1_AUDIT_UI_SYNTAX_AND_LOCAL_PAYOFF_BLOCK.json"
REPORT_MD = OUT_DIR / "RELATORIO_32_13_1_AUDIT_UI_SYNTAX_AND_LOCAL_PAYOFF_BLOCK.md"

PROHIBITED_FUNCTIONS = [
    "_calculate_payoff_from_legs",
    "_calculate_payoff_points_for_range",
    "_calculate_leg_payoff",
    "_collect_payoff_strikes",
    "_calculate_payoff_spot_range",
]

BLOCK_MESSAGE = "Cálculo de payoff na UI é proibido. Use PayoffRefreshCommandService."


def now_iso() -> str:
    return datetime.now().astimezone().isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_reports(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    REPORT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = []
    lines.append("# Relatório 32.13.1 - Auditoria sintaxe UI e bloqueio cálculo local")
    lines.append("")
    lines.append(f"Gerado em: {payload['generated_at']}")
    lines.append(f"Status: {payload['status']}")
    lines.append("")
    lines.append("## Arquivo auditado")
    lines.append("")
    lines.append(str(payload["target"]))
    lines.append("")
    lines.append("## Sintaxe")
    lines.append("")
    lines.append(f"Syntax OK: {payload['syntax_ok']}")
    if payload.get("syntax_error"):
        lines.append("")
        lines.append("Erro de sintaxe:")
        lines.append("")
        lines.append(payload["syntax_error"])
    lines.append("")
    lines.append("## Funções proibidas")
    lines.append("")

    for item in payload["functions"]:
        lines.append(f"- {item['name']}: found={item['found']}; blocked={item['blocked']}; line={item.get('line')}")

    lines.append("")
    lines.append("## Chamadas ainda encontradas")
    lines.append("")

    if payload["calls"]:
        for call in payload["calls"]:
            lines.append(f"- {call['name']} em linha {call['line']}")
    else:
        lines.append("Nenhuma chamada local proibida encontrada via AST.")

    lines.append("")
    lines.append("## Observação")
    lines.append("")
    lines.append("A UI não deve calcular payoff localmente. O fluxo oficial é UI para PayoffRefreshCommandService.")

    text = "\n".join(lines) + "\n"
    text = text.replace("`", "'")
    REPORT_MD.write_text(text, encoding="utf-8")

    print(f"OK: relatorio JSON gerado em {REPORT_JSON}")
    print(f"OK: relatorio MD gerado em {REPORT_MD}")


def function_is_blocked(source_segment: str) -> bool:
    return BLOCK_MESSAGE in source_segment and "raise RuntimeError" in source_segment


def main() -> int:
    payload = {
        "generated_at": now_iso(),
        "target": str(TARGET),
        "status": "error",
        "syntax_ok": False,
        "syntax_error": None,
        "functions": [],
        "calls": [],
    }

    if not TARGET.exists():
        payload["syntax_error"] = f"Arquivo não encontrado: {TARGET}"
        write_reports(payload)
        print("Status 32.13.1 audit: error")
        return 2

    source = read_text(TARGET)

    try:
        tree = ast.parse(source, filename=str(TARGET))
        payload["syntax_ok"] = True
    except SyntaxError as exc:
        payload["syntax_error"] = f"{exc.msg} em linha {exc.lineno}, coluna {exc.offset}"
        write_reports(payload)
        print("Status 32.13.1 audit: error")
        return 2

    found_by_name = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in PROHIBITED_FUNCTIONS:
            segment = ast.get_source_segment(source, node) or ""
            found_by_name[node.name] = {
                "name": node.name,
                "found": True,
                "blocked": function_is_blocked(segment),
                "line": node.lineno,
            }

    for name in PROHIBITED_FUNCTIONS:
        payload["functions"].append(
            found_by_name.get(
                name,
                {
                    "name": name,
                    "found": False,
                    "blocked": False,
                    "line": None,
                },
            )
        )

    class CallVisitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            call_name = None

            if isinstance(node.func, ast.Attribute):
                call_name = node.func.attr
            elif isinstance(node.func, ast.Name):
                call_name = node.func.id

            if call_name in PROHIBITED_FUNCTIONS:
                payload["calls"].append(
                    {
                        "name": call_name,
                        "line": getattr(node, "lineno", None),
                    }
                )

            self.generic_visit(node)

    CallVisitor().visit(tree)

    missing = [f for f in payload["functions"] if not f["found"]]
    unblocked = [f for f in payload["functions"] if f["found"] and not f["blocked"]]

    if missing:
        payload["status"] = "warning"
    elif unblocked:
        payload["status"] = "error"
    else:
        payload["status"] = "ok"

    write_reports(payload)
    print(f"Status 32.13.1 audit: {payload['status']}")

    return 0 if payload["status"] in {"ok", "warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
