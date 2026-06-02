"""
test_patch31.py — Pytest para validação do patch_31
"""

import importlib
import sys
from pathlib import Path

RAIZ      = Path(__file__).resolve().parent.parent.parent  # → projeto/
sys.path.insert(0, str(RAIZ))

UI_MODELS = RAIZ / "UI" / "models"


def test_init_existe():
    """__init__.py deve existir"""
    assert (UI_MODELS / "__init__.py").exists(), \
        "UI/models/__init__.py não encontrado"


def test_typo_removido():
    """__ini__.py (typo) NÃO deve existir"""
    assert not (UI_MODELS / "__ini__.py").exists(), \
        "UI/models/__ini__.py ainda existe — typo não removido"


def test_import_ui_models():
    """import UI.models deve funcionar sem erro"""
    mod = importlib.import_module("UI.models")
    assert mod is not None
