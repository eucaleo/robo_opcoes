from __future__ import annotations

"""
DEPRECATED.

Modulo legado aposentado pela Frente 17.

Este modulo nao deve ser usado por fluxos canonicos.
Fluxos novos devem usar repositories/services/db.derived_repo.
"""

import warnings

DEPRECATED = True
RETIREMENT_FRONT = "Frente 17"
MODULE_NAME = "db.writer.py"
CANONICAL_REPLACEMENT = "repositories/services/db.derived_repo"


def get_deprecation_status() -> dict:
    return {
        "deprecated": True,
        "status": "DEPRECATED",
        "front": RETIREMENT_FRONT,
        "module": MODULE_NAME,
        "replacement": CANONICAL_REPLACEMENT,
        "reason": "Modulo legado aposentado para uso operacional.",
    }


class PayoffWriter:
    def __init__(self, *args, **kwargs) -> None:
        raise RuntimeError(
            f"PayoffWriter está aposentado pela {RETIREMENT_FRONT}. "
            f"Use {CANONICAL_REPLACEMENT}."
        )


def _raise_retired_attribute(name: str) -> None:
    raise RuntimeError(
        f"{MODULE_NAME} foi aposentado pela {RETIREMENT_FRONT}. "
        f"O atributo operacional {name!r} nao deve ser usado. "
        f"Use {CANONICAL_REPLACEMENT}."
    )


def __getattr__(name: str):
    _raise_retired_attribute(name)


warnings.warn(
    f"{MODULE_NAME} esta aposentado para uso operacional. Use {CANONICAL_REPLACEMENT}.",
    DeprecationWarning,
    stacklevel=2,
)
DEPRECATED_REASON = "Frente 17"

def get_deprecation_status():
    """
    Retorna status explícito de aposentadoria do módulo legado.

    Frente 17 / 20H:
    - usado por guardrails;
    - não representa uso operacional do módulo.
    """
    return {
        "deprecated": True,
        "retired": True,
        "front": "Frente 17",
        "replacement": CANONICAL_REPLACEMENT,
        "module": __name__,
        "kind": "writer",
    }
