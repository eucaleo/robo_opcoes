from __future__ import annotations

import argparse
import importlib
import os
import platform
import sys
from pathlib import Path
from typing import Sequence


OFFICIAL_UI = "modern"
OFFICIAL_STYLE = "modernDarkUI"
OFFICIAL_MODULE = "UI.modern.dark_window"


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def configure_runtime() -> dict[str, str]:
    os.environ["MYHUB_UI"] = OFFICIAL_UI
    os.environ["MYHUB_UI_STYLE"] = OFFICIAL_STYLE
    os.environ["MYHUB_UI_MODULE"] = OFFICIAL_MODULE

    os.environ.pop("MYHUB_UI_THEME", None)
    os.environ.pop("MYHUB_UI_MODE", None)

    return {
        "ui": OFFICIAL_UI,
        "style": OFFICIAL_STYLE,
        "module": OFFICIAL_MODULE,
        "project_root": str(get_project_root()),
        "python": sys.executable,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m UI.modern",
        description="Launcher da UI modernDarkUI.",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Mostra informações do launcher sem abrir a janela.",
    )
    return parser


def print_info(runtime: dict[str, str]) -> None:
    print("[ModernApp] Informações do launcher")
    print(f"  ui: {runtime['ui']}")
    print(f"  style: {runtime['style']}")
    print(f"  module: {runtime['module']}")
    print(f"  project_root: {runtime['project_root']}")
    print(f"  python: {runtime['python']}")
    print(f"  python_version: {runtime['python_version']}")
    print(f"  platform: {runtime['platform']}")


def launch_modern() -> int:
    module = importlib.import_module(OFFICIAL_MODULE)

    if hasattr(module, "main"):
        result = module.main()
        return int(result or 0)

    if hasattr(module, "run"):
        result = module.run()
        return int(result or 0)

    raise RuntimeError(f"Módulo oficial sem entrypoint main/run: {OFFICIAL_MODULE}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runtime = configure_runtime()

    if args.info:
        print_info(runtime)
        return 0

    return launch_modern()


if __name__ == "__main__":
    raise SystemExit(main())
