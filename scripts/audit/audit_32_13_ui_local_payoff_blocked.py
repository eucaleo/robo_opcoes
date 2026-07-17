from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
UI_FILE = ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
JSON_OUT = OUT_DIR / "RELATORIO_32_13_AUDIT_UI_LOCAL_PAYOFF_BLOCKED.json"
MD_OUT = OUT_DIR / "RELATORIO_32_13_AUDIT_UI_LOCAL_PAYOFF_BLOCKED.md"

FORBIDDEN_METHODS = {
    "_calculate_payoff_from_legs",
    "_calculate_payoff_points_for_range",
    "_calculate_leg_payoff",
    "_collect_payoff_strikes",
    "_calculate_payoff_spot_range",
}

FORBIDDEN_TOKENS = {
    "compute_payoff_from_canonical_input",
    "subprocess.run",
    "subprocess.Popen",
    "os.system",
    "INSERT INTO payoff_curve_points",
    "INSERT INTO structure_decisions",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_has_explicit_runtime_block(lines: list[str], start: int, end: int) -> bool:
    body = "\n".join(lines[start - 1:end])
    return (
        "RuntimeError" in body
        and "Cálculo de payoff na UI é proibido" in body
        and "PayoffRefreshCommandService" in body
    )


def find_function_defs(source: str) -> list[dict[str, Any]]:
    tree = ast.parse(source)
    found: list[dict[str, Any]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found.append(
                {
                    "name": node.name,
                    "lineno": node.lineno,
                    "end_lineno": getattr(node, "end_lineno", node.lineno),
                }
            )

    return sorted(found, key=lambda item: int(item["lineno"]))


def collect_calls(source: str, method_names: set[str]) -> list[dict[str, Any]]:
    tree = ast.parse(source)
    calls: list[dict[str, Any]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = None

            if isinstance(func, ast.Name):
                name = func.id
            elif isinstance(func, ast.Attribute):
                name = func.attr

            if name in method_names:
                calls.append(
                    {
                        "name": name,
                        "lineno": getattr(node, "lineno", None),
                    }
                )

    return sorted(calls, key=lambda item: int(item.get("lineno") or 0))


def write_reports(report: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    JSON_OUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    checks = report["checks"]
    methods = report["methods"]
    calls = report["calls"]
    token_hits = report["token_hits"]

    md_lines = [
        "# Relatorio 32.13 - Auditoria bloqueio calculo local de payoff na UI",
        "",
        f"Status: {report['status']}",
        "",
        "Objetivo",
        "",
        "Confirmar se metodos locais de calculo de payoff na UI estao bloqueados por erro explicito.",
        "",
        "Arquivo analisado",
        "",
        f"- {report['ui_file']}",
        "",
        "Checks",
        "",
    ]

    for key, value in checks.items():
        prefix = "OK" if value else "FALHA"
        md_lines.append(f"- {prefix}: {key} = {value}")

    md_lines.extend(
        [
            "",
            "Metodos proibidos encontrados",
            "",
        ]
    )

    if methods:
        for item in methods:
            md_lines.append(
                f"- {item['name']} linhas {item['lineno']} a {item['end_lineno']} bloqueado={item['blocked']}"
            )
    else:
        md_lines.append("- Nenhum metodo proibido encontrado.")

    md_lines.extend(
        [
            "",
            "Chamadas aos metodos proibidos",
            "",
        ]
    )

    if calls:
        for item in calls:
            md_lines.append(f"- {item['name']} linha {item['lineno']}")
    else:
        md_lines.append("- Nenhuma chamada encontrada.")

    md_lines.extend(
        [
            "",
            "Tokens proibidos encontrados",
            "",
        ]
    )

    if token_hits:
        for item in token_hits:
            md_lines.append(f"- {item['token']} linha {item['line']}")
    else:
        md_lines.append("- Nenhum token proibido encontrado.")

    md_lines.extend(
        [
            "",
            "Conclusao",
            "",
            report["message"],
            "",
        ]
    )

    MD_OUT.write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def main() -> int:
    report: dict[str, Any] = {
        "status": "error",
        "created_at": now_iso(),
        "ui_file": str(UI_FILE),
        "methods": [],
        "calls": [],
        "token_hits": [],
        "checks": {},
        "message": "",
        "error": None,
    }

    try:
        if not UI_FILE.exists():
            report["message"] = "Arquivo de UI nao encontrado."
            report["checks"] = {
                "ui_file_exists": False,
                "all_forbidden_methods_blocked": False,
                "no_forbidden_tokens": False,
            }
            write_reports(report)
            print(f"Status 32.13 audit: {report['status']}")
            return 1

        source = read_text(UI_FILE)
        lines = source.splitlines()
        defs = find_function_defs(source)
        calls = collect_calls(source, FORBIDDEN_METHODS)

        forbidden_defs = [
            item for item in defs if item["name"] in FORBIDDEN_METHODS
        ]

        methods_report = []
        for item in forbidden_defs:
            blocked = line_has_explicit_runtime_block(
                lines,
                int(item["lineno"]),
                int(item["end_lineno"]),
            )
            methods_report.append(
                {
                    **item,
                    "blocked": blocked,
                }
            )

        token_hits = []
        for idx, line in enumerate(lines, start=1):
            for token in FORBIDDEN_TOKENS:
                if token in line:
                    token_hits.append(
                        {
                            "token": token,
                            "line": idx,
                            "text": line.strip(),
                        }
                    )

        all_methods_blocked = all(item["blocked"] for item in methods_report)
        no_forbidden_tokens = len(token_hits) == 0

        report["methods"] = methods_report
        report["calls"] = calls
        report["token_hits"] = token_hits
        report["checks"] = {
            "ui_file_exists": True,
            "forbidden_methods_present": bool(methods_report),
            "all_forbidden_methods_blocked": all_methods_blocked,
            "no_forbidden_tokens": no_forbidden_tokens,
        }

        if all_methods_blocked and no_forbidden_tokens:
            report["status"] = "ok"
            report["message"] = (
                "Metodos locais de calculo de payoff encontrados, mas bloqueados por erro explicito."
            )
        elif methods_report:
            report["status"] = "error"
            report["message"] = (
                "Ainda ha metodos locais de calculo de payoff sem bloqueio explicito."
            )
        else:
            report["status"] = "warning"
            report["message"] = (
                "Nenhum metodo proibido foi encontrado. Validar se foram removidos ou renomeados."
            )

        write_reports(report)
        print(f"OK: relatorio JSON gerado em {JSON_OUT}")
        print(f"OK: relatorio MD gerado em {MD_OUT}")
        print(f"Status 32.13 audit: {report['status']}")
        return 0 if report["status"] == "ok" else 1

    except Exception as exc:
        report["status"] = "error"
        report["error"] = repr(exc)
        report["message"] = "Erro ao auditar bloqueio de calculo local de payoff na UI."
        write_reports(report)
        print(f"ERRO 32.13 audit: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
