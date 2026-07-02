"""
Entrypoint unificado da UI moderna.

Este módulo funciona como uma camada de roteamento segura entre os launchers
modernos existentes, sem alterar o comportamento deles.

Uso:

    python -m UI.modern.app --mode dark
    python -m UI.modern.app --mode shell

Por padrão, abre o modo DARK.
"""

from __future__ import annotations

import argparse
import os
import runpy
import sys
from typing import Dict, List, Optional

from UI.modern.theme import get_theme


MODES: Dict[str, str] = {
    "dark": "UI.modern.dark_window",
    "shell": "UI.modern.main_window",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m UI.modern.app",
        description="Launcher unificado da UI moderna.",
    )

    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        default="dark",
        help="Modo de inicialização da UI moderna. Padrão: dark.",
    )

    parser.add_argument(
        "--theme",
        choices=["dark", "clean"],
        default="dark",
        help=(
            "Tema desejado. Neste checkpoint, o valor é registrado para "
            "uso futuro, mas os painéis existentes ainda preservam seus "
            "estilos próprios."
        ),
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args, passthrough_args = parser.parse_known_args(argv)

    theme = get_theme(args.theme)
    os.environ["MYHUB_UI_MODE"] = args.mode
    os.environ["MYHUB_UI_THEME"] = args.theme
    os.environ["MYHUB_UI_APPEARANCE_MODE"] = theme["appearance_mode"]

    module_name = MODES[args.mode]

    print(
        "[ModernApp] Abrindo UI moderna "
        f"mode={args.mode!r} theme={args.theme!r} module={module_name!r}"
    )

    original_argv = sys.argv[:]

    try:
        sys.argv = [f"python -m {module_name}", *passthrough_args]
        runpy.run_module(module_name, run_name="__main__")
    finally:
        sys.argv = original_argv

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
