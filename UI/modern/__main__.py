"""Entrypoint do pacote UI.modern.

Permite executar:

    python -m UI.modern

A delegacao passa pelo modulo UI.modern.app para manter compatibilidade
com testes que monkeypatcham app.main, inclusive quando a suite completa
altera sys.modules durante outros testes.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import ModuleType


def _load_package_app_attribute() -> ModuleType | None:
    package_name = __package__ or "UI.modern"
    package = sys.modules.get(package_name)

    if package is None and package_name != "__main__":
        try:
            package = importlib.import_module(package_name)
        except Exception:
            package = None

    app_module = getattr(package, "app", None) if package is not None else None
    if isinstance(app_module, ModuleType) and hasattr(app_module, "main"):
        return app_module

    return None


def _load_app_module() -> ModuleType:
    patched_app = _load_package_app_attribute()
    if patched_app is not None:
        return patched_app

    if __package__:
        return importlib.import_module(f"{__package__}.app")

    project_root = Path(__file__).resolve().parents[2]
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    return importlib.import_module("UI.modern.app")


def main() -> int:
    app_module = _load_app_module()
    return app_module.main()


if __name__ == "__main__":
    raise SystemExit(main())
