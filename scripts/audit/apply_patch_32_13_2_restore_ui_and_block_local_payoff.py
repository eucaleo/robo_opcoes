from __future__ import annotations

import ast
import json
import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py"
OUT_DIR = ROOT / "AUDITORIA_POS_PATCH_32"
JSON_OUT = OUT_DIR / "RELATORIO_32_13_2_PATCH_RESTORE_UI_AND_BLOCK_LOCAL_PAYOFF.json"
MD_OUT = OUT_DIR / "RELATORIO_32_13_2_PATCH_RESTORE_UI_AND_BLOCK_LOCAL_PAYOFF.md"

FUNC_NAME = "_calculate_payoff_points_for_range"
MARKER = "PAYOFF_LOCAL_CALCULATION_BLOCKED_32_13_2"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def write_reports(payload: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    JSON_OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    lines = [
        "# Relatorio 32.13.2 - Patch restaurar UI e bloquear payoff local",
        "",
        f"Gerado em: {payload['generated_at']}",
        f"Status: {payload['status']}",
        "",
        "## Acoes",
    ]

    for action in payload["actions"]:
        lines.append("")
        lines.append(f"- Nome: {action['name']}")
        lines.append(f"  - Status: {action['status']}")
        lines.append(f"  - Detalhe: {action['detail']}")

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


def compiles(path: Path) -> tuple[bool, str]:
    try:
        py_compile.compile(str(path), doraise=True)
        return True, "ok"
    except Exception as exc:
        return False, str(exc).replace("\n", " ")


def find_good_backup(actions: list[dict]) -> Path | None:
    backup_patterns = [
        "terminal_vwap_payoff_dark_panel.py.bak_32_13_20*",
        "terminal_vwap_payoff_dark_panel.py.bak_32_12*",
        "terminal_vwap_payoff_dark_panel.py.bak*",
    ]

    candidates: list[Path] = []
    for pattern in backup_patterns:
        candidates.extend(sorted(TARGET.parent.glob(pattern), reverse=True))

    seen = set()
    unique_candidates = []
    for item in candidates:
        key = str(item.resolve())
        if key not in seen:
            seen.add(key)
            unique_candidates.append(item)

    for candidate in unique_candidates:
        ok, detail = compiles(candidate)
        actions.append(
            {
                "name": "avaliar_backup",
                "status": "ok" if ok else "warning",
                "detail": f"{candidate.name}: {detail}",
            }
        )
        if ok:
            return candidate

    return None


def get_indent(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" "))]


def replace_function_body_using_ast(source: str) -> tuple[str, str]:
    tree = ast.parse(source)
    target_node = None

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == FUNC_NAME:
            target_node = node
            break

    if target_node is None:
        raise RuntimeError(f"Funcao {FUNC_NAME} nao encontrada para bloqueio.")

    lines = source.splitlines()
    start_idx = target_node.lineno - 1
    end_idx = target_node.end_lineno or target_node.lineno

    paren_balance = 0
    header_end_idx = start_idx

    for idx in range(start_idx, len(lines)):
        line = lines[idx]
        paren_balance += line.count("(") - line.count(")")
        if line.rstrip().endswith(":") and paren_balance <= 0:
            header_end_idx = idx
            break

    header_lines = lines[start_idx: header_end_idx + 1]
    fn_indent = get_indent(lines[start_idx])
    body_indent = fn_indent + "    "

    new_body = [
        f'{body_indent}"""',
        f"{body_indent}{MARKER}",
        f"{body_indent}Calculo local de payoff desabilitado na UI.",
        f"{body_indent}A curva deve ser obtida exclusivamente do backend ou da persistencia oficial.",
        f'{body_indent}"""',
        f"{body_indent}return []",
    ]

    new_lines = (
        lines[:start_idx]
        + header_lines
        + new_body
        + lines[end_idx:]
    )

    return "\n".join(new_lines) + "\n", f"Funcao {FUNC_NAME} substituida por bloqueio seguro."


def replace_broken_function_by_text(source: str) -> tuple[str, str]:
    lines = source.splitlines()
    start_idx = None

    for idx, line in enumerate(lines):
        if line.lstrip().startswith(f"def {FUNC_NAME}("):
            start_idx = idx
            break

    if start_idx is None:
        raise RuntimeError(f"Funcao {FUNC_NAME} nao encontrada por texto.")

    fn_indent = get_indent(lines[start_idx])
    end_idx = len(lines)

    for idx in range(start_idx + 1, len(lines)):
        stripped = lines[idx].lstrip()
        same_or_less_indent = len(get_indent(lines[idx])) <= len(fn_indent)
        if same_or_less_indent and (stripped.startswith("def ") or stripped.startswith("class ")):
            end_idx = idx
            break

    replacement = [
        f"{fn_indent}def {FUNC_NAME}(*args, **kwargs):",
        f'{fn_indent}    """',
        f"{fn_indent}    {MARKER}",
        f"{fn_indent}    Calculo local de payoff desabilitado na UI.",
        f"{fn_indent}    A curva deve ser obtida exclusivamente do backend ou da persistencia oficial.",
        f'{fn_indent}    """',
        f"{fn_indent}    return []",
    ]

    new_lines = lines[:start_idx] + replacement + lines[end_idx:]
    return "\n".join(new_lines) + "\n", "Funcao quebrada substituida por assinatura defensiva."


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    actions: list[dict] = []

    ok = False

    if not TARGET.exists():
        actions.append(
            {
                "name": "arquivo_ui",
                "status": "error",
                "detail": f"Arquivo nao encontrado: {TARGET}",
            }
        )
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safety_backup = TARGET.with_name(TARGET.name + f".bak_32_13_2_{timestamp}")
        shutil.copy2(TARGET, safety_backup)
        actions.append(
            {
                "name": "backup_seguranca",
                "status": "ok",
                "detail": f"Backup criado: {safety_backup}",
            }
        )

        before_ok, before_detail = compiles(TARGET)
        actions.append(
            {
                "name": "compilacao_antes",
                "status": "ok" if before_ok else "warning",
                "detail": before_detail,
            }
        )

        if not before_ok:
            backup = find_good_backup(actions)
            if backup is not None:
                shutil.copy2(backup, TARGET)
                actions.append(
                    {
                        "name": "restaurar_backup_bom",
                        "status": "ok",
                        "detail": f"Restaurado a partir de {backup.name}",
                    }
                )
            else:
                actions.append(
                    {
                        "name": "restaurar_backup_bom",
                        "status": "warning",
                        "detail": "Nenhum backup compilavel encontrado. Sera tentado reparo textual.",
                    }
                )

        source = read_text(TARGET)

        try:
            parsed_source = ast.parse(source)
            del parsed_source
            new_source, detail = replace_function_body_using_ast(source)
            actions.append(
                {
                    "name": "bloquear_funcao_por_ast",
                    "status": "ok",
                    "detail": detail,
                }
            )
        except Exception as ast_exc:
            try:
                new_source, detail = replace_broken_function_by_text(source)
                actions.append(
                    {
                        "name": "bloquear_funcao_por_texto",
                        "status": "ok",
                        "detail": f"{detail} AST indisponivel: {ast_exc}",
                    }
                )
            except Exception as text_exc:
                new_source = source
                actions.append(
                    {
                        "name": "bloquear_funcao",
                        "status": "error",
                        "detail": f"Falha AST: {ast_exc}. Falha texto: {text_exc}",
                    }
                )

        write_text(TARGET, new_source)

        after_ok, after_detail = compiles(TARGET)
        actions.append(
            {
                "name": "compilacao_depois",
                "status": "ok" if after_ok else "error",
                "detail": after_detail,
            }
        )

        marker_present = MARKER in read_text(TARGET)
        actions.append(
            {
                "name": "marcador_bloqueio",
                "status": "ok" if marker_present else "error",
                "detail": (
                    "Marcador de bloqueio encontrado no arquivo UI."
                    if marker_present
                    else "Marcador de bloqueio nao encontrado no arquivo UI."
                ),
            }
        )

        ok = after_ok and marker_present

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": "ok" if ok else "error",
        "target": str(TARGET),
        "actions": actions,
        "conclusion": (
            "Patch aplicado com UI compilavel e calculo local de payoff bloqueado."
            if ok
            else "Patch finalizado com pendencias. Verifique o relatorio e o trecho da UI."
        ),
    }

    write_reports(payload)

    print(f"OK: relatorio JSON gerado em {JSON_OUT}")
    print(f"OK: relatorio MD gerado em {MD_OUT}")
    print(f"Status 32.13.2 patch: {payload['status']}")

    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
