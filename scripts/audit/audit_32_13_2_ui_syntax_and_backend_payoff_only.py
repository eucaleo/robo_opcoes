from __future__ import annotations

import ast
import json
import py_compile
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
JSON_OUT = OUT_DIR / "RELATORIO_32_13_2_AUDIT_UI_SYNTAX_AND_BACKEND_PAYOFF_ONLY.json"
MD_OUT = OUT_DIR / "RELATORIO_32_13_2_AUDIT_UI_SYNTAX_AND_BACKEND_PAYOFF_ONLY.md"

MARKER = "PAYOFF_LOCAL_CALCULATION_BLOCKED_32_13_2"
FUNC_NAME = "_calculate_payoff_points_for_range"


def write_reports(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    JSON_OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    lines = [
        "# Relatorio 32.13.2 - Auditoria UI sintaxe e payoff somente backend",
        "",
        f"Gerado em: {payload['generated_at']}",
        f"Status: {payload['status']}",
        "",
        "## Checks",
    ]

    for check in payload["checks"]:
        lines.append("")
        lines.append(f"- Nome: {check['name']}")
        lines.append(f"  - Status: {check['status']}")
        lines.append(f"  - Detalhe: {check['detail']}")

    lines.extend(
        [
            "",
            "## Conclusao",
            payload["conclusion"],
            "",
        ]
    )

    text = "\n".join(lines)
    text = text.replace(chr(96), "'")
    MD_OUT.write_text(text, encoding="utf-8", newline="\n")


def check_py_compile(checks: list[dict]) -> bool:
    try:
        py_compile.compile(str(TARGET), doraise=True)
        checks.append(
            {
                "name": "py_compile",
                "status": "ok",
                "detail": "Arquivo UI compila sem erro de sintaxe.",
            }
        )
        return True
    except Exception as exc:
        checks.append(
            {
                "name": "py_compile",
                "status": "error",
                "detail": str(exc).replace("\n", " "),
            }
        )
        return False


def check_ast_and_marker(checks: list[dict]) -> bool:
    try:
        source = TARGET.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = TARGET.read_text(encoding="latin-1")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        checks.append(
            {
                "name": "ast_parse",
                "status": "error",
                "detail": f"SyntaxError linha {exc.lineno}: {exc.msg}",
            }
        )
        return False

    checks.append(
        {
            "name": "ast_parse",
            "status": "ok",
            "detail": "AST carregada com sucesso.",
        }
    )

    functions = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == FUNC_NAME
    ]

    if not functions:
        checks.append(
            {
                "name": "funcao_payoff_local",
                "status": "warning",
                "detail": f"Funcao {FUNC_NAME} nao encontrada.",
            }
        )
        return False

    fn = functions[0]
    fn_source = "\n".join(source.splitlines()[fn.lineno - 1: fn.end_lineno or fn.lineno])

    has_marker = MARKER in fn_source
    has_return_empty = "return []" in fn_source or "return list()" in fn_source

    blocked = has_marker and has_return_empty

    checks.append(
        {
            "name": "bloqueio_calculo_local_payoff",
            "status": "ok" if blocked else "error",
            "detail": (
                "Funcao local de payoff bloqueada com marcador e retorno vazio."
                if blocked
                else "Funcao local de payoff ainda nao esta bloqueada conforme esperado."
            ),
        }
    )

    forbidden_terms = [
        "np.linspace",
        "numpy.linspace",
        "for x in",
        "for price in",
        "calculate_payoff",
        "payoff_points.append",
    ]

    found_forbidden = [
        term for term in forbidden_terms
        if term in fn_source and term not in ["calculate_payoff"]
    ]

    checks.append(
        {
            "name": "escopo_funcao_bloqueada",
            "status": "ok" if not found_forbidden else "warning",
            "detail": (
                "Nao foram encontrados sinais fortes de calculo local dentro da funcao bloqueada."
                if not found_forbidden
                else "Termos suspeitos encontrados: " + ", ".join(found_forbidden)
            ),
        }
    )

    return blocked


def main() -> int:
    checks: list[dict] = []

    if not TARGET.exists():
        checks.append(
            {
                "name": "arquivo_ui",
                "status": "error",
                "detail": f"Arquivo nao encontrado: {TARGET}",
            }
        )
        ok = False
    else:
        checks.append(
            {
                "name": "arquivo_ui",
                "status": "ok",
                "detail": f"Arquivo encontrado: {TARGET}",
            }
        )
        compile_ok = check_py_compile(checks)
        ast_ok = check_ast_and_marker(checks) if compile_ok else False
        ok = compile_ok and ast_ok

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "ok" if ok else "error",
        "target": str(TARGET),
        "checks": checks,
        "conclusion": (
            "UI compila e calculo local de payoff permanece bloqueado."
            if ok
            else "Ainda existem pendencias de sintaxe ou bloqueio local de payoff."
        ),
    }

    write_reports(payload)

    print(f"OK: relatorio JSON gerado em {JSON_OUT}")
    print(f"OK: relatorio MD gerado em {MD_OUT}")
    print(f"Status 32.13.2 audit: {payload['status']}")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
