from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PHASE1_FILES = [
    PROJECT_ROOT / "services" / "excel_rtd_com_access.py",
    PROJECT_ROOT / "services" / "excel_rtd_reader.py",
    PROJECT_ROOT / "services" / "excel_rtd_workbook_probe.py",
    PROJECT_ROOT / "services" / "rtd_excel_probe_service.py",
    PROJECT_ROOT / "rtd_bridge" / "excel_rtd_connection_status.py",
    PROJECT_ROOT / "rtd_bridge" / "excel_rtd_connection_status_presenter.py",
    PROJECT_ROOT / "UI" / "modern" / "dark_window.py",
]

COM_GATEWAY = PROJECT_ROOT / "services" / "excel_rtd_com_access.py"

FORBIDDEN_IMPORT_ROOTS = {
    "subprocess",
    "xlwings",
}

COM_IMPORT_ROOT = "win32com"

FORBIDDEN_CALL_ATTRS = {
    "Dispatch",
    "DispatchEx",
}

FORBIDDEN_SUBPROCESS_CALLS = {
    ("subprocess", "run"),
    ("subprocess", "Popen"),
    ("subprocess", "check_output"),
    ("os", "system"),
}


def _relative(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def _dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        base = _dotted_name(node.value)
        if base:
            return f"{base}.{node.attr}"
        return node.attr

    return None


def _parse(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_phase1_files_exist() -> None:
    missing = [path for path in PHASE1_FILES if not path.exists()]

    assert not missing, "Arquivos esperados da Fase 1 não encontrados: " + ", ".join(
        _relative(path) for path in missing
    )


def test_phase1_does_not_import_subprocess_or_xlwings() -> None:
    violations: list[str] = []

    for path in PHASE1_FILES:
        if not path.exists():
            continue

        tree = _parse(path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root in FORBIDDEN_IMPORT_ROOTS:
                        violations.append(
                            f"{_relative(path)}:{node.lineno}: import {alias.name}"
                        )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                root = module.split(".")[0]
                if root in FORBIDDEN_IMPORT_ROOTS:
                    violations.append(
                        f"{_relative(path)}:{node.lineno}: from {module} import ..."
                    )

    assert not violations, "Imports proibidos na Fase 1:\n" + "\n".join(violations)


def test_phase1_win32com_import_is_restricted_to_com_gateway() -> None:
    violations: list[str] = []

    for path in PHASE1_FILES:
        if not path.exists():
            continue

        tree = _parse(path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root == COM_IMPORT_ROOT and path != COM_GATEWAY:
                        violations.append(
                            f"{_relative(path)}:{node.lineno}: import {alias.name}"
                        )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                root = module.split(".")[0]
                if root == COM_IMPORT_ROOT and path != COM_GATEWAY:
                    violations.append(
                        f"{_relative(path)}:{node.lineno}: from {module} import ..."
                    )

    assert not violations, (
        "win32com deve ser importado diretamente apenas no gateway COM:\n"
        + "\n".join(violations)
    )


def test_phase1_does_not_call_dispatch_or_subprocess() -> None:
    violations: list[str] = []

    for path in PHASE1_FILES:
        if not path.exists():
            continue

        tree = _parse(path)

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            name = _dotted_name(node.func)
            if not name:
                continue

            parts = name.split(".")

            if parts[-1] in FORBIDDEN_CALL_ATTRS:
                violations.append(f"{_relative(path)}:{node.lineno}: call {name}(...)")

            if len(parts) >= 2:
                pair = (parts[-2], parts[-1])
                if pair in FORBIDDEN_SUBPROCESS_CALLS:
                    violations.append(
                        f"{_relative(path)}:{node.lineno}: call {name}(...)"
                    )

    assert not violations, (
        "Chamadas proibidas na Fase 1 encontradas:\n" + "\n".join(violations)
    )


def test_phase1_get_active_object_is_restricted_to_com_gateway() -> None:
    violations: list[str] = []

    for path in PHASE1_FILES:
        if not path.exists():
            continue

        tree = _parse(path)

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            name = _dotted_name(node.func)
            if not name:
                continue

            if name.split(".")[-1] == "GetActiveObject" and path != COM_GATEWAY:
                violations.append(f"{_relative(path)}:{node.lineno}: call {name}(...)")

    assert not violations, (
        "GetActiveObject deve ser chamado diretamente apenas no gateway COM:\n"
        + "\n".join(violations)
    )
