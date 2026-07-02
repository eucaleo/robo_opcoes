"""
Execução direta do pacote UI.modern.

Permite abrir a UI moderna com:

    python -m UI.modern

Equivalente a:

    python -m UI.modern.app

Por padrão, o app abre no modo DARK.
"""

from __future__ import annotations

from UI.modern.app import main


if __name__ == "__main__":
    raise SystemExit(main())
