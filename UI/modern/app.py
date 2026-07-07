"""
Entrypoint unificado da UI moderna.

Este módulo funciona como uma camada de roteamento segura entre os launchers
modernos existentes, sem alterar o comportamento deles.

Uso:

    python -m UI.modern
    python -m UI.modern --mode dark
    python -m UI.modern --mode shell
    python -m UI.modern --info

Por padrão, abre o modo DARK.
"""

from __future__ import annotations

import argparse
import os
import platform
import runpy
import sys
from pathlib import Path
from typing import Dict, List, Optional

from UI.modern.theme import get_theme


MODES: Dict[str, str] = {
    "dark": "UI.modern.dark_window",
    "shell": "UI.modern.main_window",
}



def _env_default(name: str, fallback: str, allowed: set[str]) -> str:
    value = os.environ.get(name, "").strip().lower()
    if value in allowed:
        return value
    return fallback


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m UI.modern",
        description="Launcher unificado da UI moderna.",
    )

    parser.add_argument(
        "--mode",
        choices=sorted(MODES),
        default=_env_default("MYHUB_UI_MODE", "dark", {"dark", "shell"}),
        help="Modo de inicialização da UI moderna. Padrão: dark.",
    )

    parser.add_argument(
        "--theme",
        choices=["dark", "clean"],
        default=_env_default("MYHUB_UI_THEME", "dark", {"dark", "clean"}),
        help=(
            "Tema desejado. Neste estágio, o tema é propagado para o runtime "
            "e prepara a convergência futura dos componentes."
        ),
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Mostra informações do launcher moderno sem abrir a janela.",
    )

    return parser


def project_root() -> Path:
    """
    Retorna a raiz provável do projeto.

    Como este arquivo fica em UI/modern/app.py, a raiz é dois níveis acima
    do diretório UI/modern.
    """
    return Path(__file__).resolve().parents[2]


def configure_runtime(mode: str, theme_name: str) -> Dict[str, str]:
    """
    Configura variáveis de ambiente do runtime moderno.
    """
    theme = get_theme(theme_name)

    os.environ["MYHUB_UI_MODE"] = mode
    os.environ["MYHUB_UI_THEME"] = theme_name
    os.environ["MYHUB_UI_APPEARANCE_MODE"] = theme["appearance_mode"]

    return theme


def print_info(mode: str, theme_name: str, theme: Dict[str, str]) -> None:
    """
    Exibe diagnóstico do launcher moderno.
    """
    module_name = MODES[mode]

    print("[ModernApp] Informações do launcher moderno")
    print(f"  mode: {mode}")
    print(f"  theme: {theme_name}")
    print(f"  appearance_mode: {theme['appearance_mode']}")
    print(f"  module: {module_name}")
    print(f"  project_root: {project_root()}")
    print(f"  python: {sys.executable}")
    print(f"  python_version: {platform.python_version()}")
    print(f"  platform: {platform.platform()}")


def launch_module(mode: str, passthrough_args: List[str]) -> None:
    """
    Executa o módulo associado ao modo escolhido.
    """
    module_name = MODES[mode]

    print(
        "[ModernApp] Abrindo UI moderna "
        f"mode={mode!r} "
        f"theme={os.environ.get('MYHUB_UI_THEME', 'dark')!r} "
        f"module={module_name!r}"
    )

    original_argv = sys.argv[:]

    try:
        sys.argv = [f"python -m {module_name}", *passthrough_args]
        runpy.run_module(module_name, run_name="__main__")
    finally:
        sys.argv = original_argv


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args, passthrough_args = parser.parse_known_args(argv)

    theme = configure_runtime(args.mode, args.theme)

    if args.info:
        print_info(args.mode, args.theme, theme)
        return 0

    launch_module(args.mode, passthrough_args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
