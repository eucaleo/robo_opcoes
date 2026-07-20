from __future__ import annotations

import ast
import json
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET = PROJECT_ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
OUT_DIR = PROJECT_ROOT / "AUDITORIA_POS_PATCH_32"

REPORT_JSON = OUT_DIR / "RELATORIO_32_13_1_PATCH_FIX_UI_LOCAL_PAYOFF_BLOCK_SYNTAX.json"
REPORT_MD = OUT_DIR / "RELATORIO_32_13_1_PATCH_FIX_UI_LOCAL_PAYOFF_BLOCK_SYNTAX.md"

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


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_source(source: str) -> tuple[bool, ast.Module | None, str | None]:
    try:
        return True, ast.parse(source, filename=str(TARGET)), None
    except SyntaxError as exc:
        return False, None, f"{exc.msg} em linha {exc.lineno}, coluna {exc.offset}"


def latest_backup() -> Path | None:
    candidates = sorted(
        TARGET.parent.glob("terminal_vwap_payoff_dark_panel.py.bak_32_13_*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def function_is_blocked(segment: str) -> bool:
    return BLOCK_MESSAGE in segment and "raise RuntimeError" in segment


def block_functions(source: str, tree: ast.Module) -> tuple[str, list[dict]]:
    newline = detect_newline(source)
    lines = source.splitlines(keepends=True)

    targets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in PROHIBITED_FUNCTIONS:
            if not node.body:
                continue

            segment = ast.get_source_segment(source, node) or ""
            already_blocked = function_is_blocked(segment)

            first_body = node.body[0]
            start_idx = first_body.lineno - 1
            end_idx = node.end_lineno

            body_line = lines[start_idx] if 0 <= start_idx < len(lines) else ""
            indent = body_line[: len(body_line) - len(body_line.lstrip(" \t"))]
            if not indent:
                indent = " " * 8

            replacement = [
                f'{indent}"""{BLOCK_MESSAGE}"""' + newline,
                f'{indent}raise RuntimeError(' + newline,
                f'{indent}    "{BLOCK_MESSAGE}"' + newline,
                f'{indent})' + newline,
            ]

            targets.append(
                {
                    "name": node.name,
                    "line": node.lineno,
                    "start_idx": start_idx,
                    "end_idx": end_idx,
                    "replacement": replacement,
                    "already_blocked": already_blocked,
                }
            )

    targets.sort(key=lambda item: item["start_idx"], reverse=True)

    changes = []
    for item in targets:
        lines[item["start_idx"] : item["end_idx"]] = item["replacement"]
        changes.append(
            {
                "name": item["name"],
                "line": item["line"],
                "already_blocked": item["already_blocked"],
                "blocked_now": True,
            }
        )

    return "".join(lines), changes


def write_reports(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    REPORT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = []
    lines.append("# Relatório 32.13.1 - Patch correção sintaxe bloqueio UI")
    lines.append("")
    lines.append(f"Gerado em: {payload['generated_at']}")
    lines.append(f"Status: {payload['status']}")
    lines.append("")
    lines.append("## Arquivo")
    lines.append("")
    lines.append(str(payload["target"]))
    lines.append("")
    lines.append("## Ações")
    lines.append("")

    for action in payload["actions"]:
        lines.append(f"- {action}")

    lines.append("")
    lines.append("## Funções bloqueadas")
    lines.append("")

    if payload["changes"]:
        for change in payload["changes"]:
            lines.append(f"- {change['name']} na linha {change['line']}")
    else:
        lines.append("Nenhuma função alterada.")

    lines.append("")
    lines.append("## Validação")
    lines.append("")
    lines.append(f"Sintaxe final OK: {payload['final_syntax_ok']}")
    if payload.get("final_syntax_error"):
        lines.append(f"Erro final: {payload['final_syntax_error']}")

    lines.append("")
    lines.append("Fluxo oficial preservado: UI para PayoffRefreshCommandService.")

    text = "\n".join(lines) + "\n"
    text = text.replace("`", "'")
    REPORT_MD.write_text(text, encoding="utf-8")

    print(f"OK: relatorio JSON gerado em {REPORT_JSON}")
    print(f"OK: relatorio MD gerado em {REPORT_MD}")


def main() -> int:
    payload = {
        "generated_at": now_iso(),
        "target": str(TARGET),
        "status": "error",
        "actions": [],
        "changes": [],
        "final_syntax_ok": False,
        "final_syntax_error": None,
    }

    if not TARGET.exists():
        payload["actions"].append(f"Arquivo não encontrado: {TARGET}")
        write_reports(payload)
        print("Status 32.13.1 patch: error")
        return 2

    before_backup = TARGET.with_name(f"{TARGET.name}.bak_32_13_1_{timestamp()}")
    shutil.copy2(TARGET, before_backup)
    payload["actions"].append(f"Backup do estado atual criado em {before_backup}")

    source = read_text(TARGET)
    syntax_ok, tree, syntax_error = parse_source(source)

    if not syntax_ok:
        payload["actions"].append(f"Arquivo atual com erro de sintaxe: {syntax_error}")
        backup = latest_backup()

        if not backup:
            payload["actions"].append("Nenhum backup 32.13 encontrado para restauração automática.")
            payload["final_syntax_error"] = syntax_error
            write_reports(payload)
            print("Status 32.13.1 patch: error")
            return 2

        backup_source = read_text(backup)
        backup_ok, backup_tree, backup_error = parse_source(backup_source)

        if not backup_ok:
            payload["actions"].append(f"Backup também possui erro de sintaxe: {backup_error}")
            payload["final_syntax_error"] = backup_error
            write_reports(payload)
            print("Status 32.13.1 patch: error")
            return 2

        source = backup_source
        tree = backup_tree
        payload["actions"].append(f"Fonte restaurada em memória a partir de {backup}")
    else:
        payload["actions"].append("Arquivo atual possui sintaxe válida antes do patch.")

    assert tree is not None

    new_source, changes = block_functions(source, tree)
    payload["changes"] = changes

    final_ok, final_tree, final_error = parse_source(new_source)
    payload["final_syntax_ok"] = final_ok
    payload["final_syntax_error"] = final_error

    if not final_ok:
        payload["actions"].append("Patch gerou sintaxe inválida. Arquivo original preservado.")
        write_reports(payload)
        print("Status 32.13.1 patch: error")
        return 2

    write_text(TARGET, new_source)
    payload["actions"].append("Arquivo atualizado com bloqueio seguro das funções locais de payoff.")
    payload["status"] = "ok"

    write_reports(payload)
    print("Status 32.13.1 patch: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
