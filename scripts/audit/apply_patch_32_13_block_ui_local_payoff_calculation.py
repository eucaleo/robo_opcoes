from __future__ import annotations

import ast
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
UI_FILE = ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
JSON_OUT = OUT_DIR / "RELATORIO_32_13_PATCH_BLOCK_UI_LOCAL_PAYOFF_CALCULATION.json"
MD_OUT = OUT_DIR / "RELATORIO_32_13_PATCH_BLOCK_UI_LOCAL_PAYOFF_CALCULATION.md"

FORBIDDEN_METHODS = {
    "_calculate_payoff_from_legs",
    "_calculate_payoff_points_for_range",
    "_calculate_leg_payoff",
    "_collect_payoff_strikes",
    "_calculate_payoff_spot_range",
}

BLOCK_MESSAGE = "Cálculo de payoff na UI é proibido. Use PayoffRefreshCommandService."


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def now_iso() -> str:
    return datetime.now().astimezone().isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def find_forbidden_function_ranges(source: str) -> list[dict[str, Any]]:
    tree = ast.parse(source)
    ranges: list[dict[str, Any]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in FORBIDDEN_METHODS:
                ranges.append(
                    {
                        "name": node.name,
                        "lineno": node.lineno,
                        "end_lineno": getattr(node, "end_lineno", node.lineno),
                    }
                )

    return sorted(ranges, key=lambda item: int(item["lineno"]), reverse=True)


def detect_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" "))]


def find_body_start(lines: list[str], start_index: int, end_index: int) -> int:
    for idx in range(start_index + 1, end_index + 1):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if stripped.startswith('"""') or stripped.startswith("'''"):
            quote = stripped[:3]
            if stripped.count(quote) >= 2 and len(stripped) > 3:
                continue
            for j in range(idx + 1, end_index + 1):
                if quote in lines[j]:
                    return j + 1
            return idx
        return idx
    return start_index + 1


def patch_source(source: str, ranges: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    lines = source.splitlines()
    patched: list[dict[str, Any]] = []

    for item in ranges:
        start = int(item["lineno"]) - 1
        end = int(item["end_lineno"]) - 1

        def_indent = detect_indent(lines[start])
        body_indent = def_indent + "    "
        body_start = find_body_start(lines, start, end)

        replacement = [
            body_indent + "# Bloqueio arquitetural 32.13.",
            body_indent + "# A UI nao pode calcular payoff nem manter fallback local.",
            body_indent + "raise RuntimeError(",
            body_indent + f"    {BLOCK_MESSAGE!r}",
            body_indent + ")",
        ]

        old_block = lines[start : end + 1]
        new_block = lines[start:body_start] + replacement
        lines[start : end + 1] = new_block

        patched.append(
            {
                "name": item["name"],
                "lineno": item["lineno"],
                "end_lineno": item["end_lineno"],
                "body_start": body_start + 1,
            }
        )

    return "\n".join(lines) + "\n", patched


def write_reports(report: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    JSON_OUT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md_lines = [
        "# Relatorio 32.13 - Patch bloqueio calculo local de payoff na UI",
        "",
        f"Status: {report['status']}",
        "",
        "Objetivo",
        "",
        "Bloquear metodos locais de calculo de payoff na UI com RuntimeError explicito.",
        "",
        "Arquivo alvo",
        "",
        f"- {report['ui_file']}",
        "",
        "Backup",
        "",
        f"- {report.get('backup_path')}",
        "",
        "Metodos alterados",
        "",
    ]

    patched = report.get("patched_methods") or []
    if patched:
        for item in patched:
            md_lines.append(f"- {item['name']} linhas {item['lineno']} a {item['end_lineno']}")
    else:
        md_lines.append("- Nenhum metodo alterado.")

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
        "backup_path": None,
        "patched_methods": [],
        "message": "",
        "error": None,
    }

    try:
        if not UI_FILE.exists():
            report["message"] = "Arquivo de UI nao encontrado."
            write_reports(report)
            print(f"Status 32.13 patch: {report['status']}")
            return 1

        source = read_text(UI_FILE)
        ranges = find_forbidden_function_ranges(source)

        if not ranges:
            report["status"] = "warning"
            report["message"] = "Nenhum metodo local proibido foi encontrado para bloquear."
            write_reports(report)
            print(f"Status 32.13 patch: {report['status']}")
            return 0

        backup_path = UI_FILE.with_suffix(UI_FILE.suffix + f".bak_32_13_{timestamp()}")
        shutil.copy2(UI_FILE, backup_path)

        patched_source, patched_methods = patch_source(source, ranges)
        write_text(UI_FILE, patched_source)

        report["status"] = "ok"
        report["backup_path"] = str(backup_path)
        report["patched_methods"] = patched_methods
        report["message"] = (
            "Metodos locais de calculo de payoff foram bloqueados por erro explicito."
        )

        write_reports(report)
        print(f"OK: backup criado em {backup_path}")
        print(f"OK: relatorio JSON gerado em {JSON_OUT}")
        print(f"OK: relatorio MD gerado em {MD_OUT}")
        print(f"Status 32.13 patch: {report['status']}")
        return 0

    except Exception as exc:
        report["status"] = "error"
        report["error"] = repr(exc)
        report["message"] = "Erro ao aplicar patch 32.13."
        write_reports(report)
        print(f"ERRO 32.13 patch: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
