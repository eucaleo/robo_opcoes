"""Normalizacao canonica de lado da posicao em estruturas.

Contrato canonico de negocio:
- COMPRADO
- VENDIDO

Aliases aceitos por compatibilidade:
- C, COMPRA, COMPRADO, LONG
- V, VENDA, VENDIDO, SHORT
"""

from __future__ import annotations

from typing import Any


CANONICAL_POSITION_SIDES: frozenset[str] = frozenset({
    "COMPRADO",
    "VENDIDO",
})


_POSITION_SIDE_ALIASES: dict[str, str] = {
    "C": "COMPRADO",
    "COMPRA": "COMPRADO",
    "COMPRADO": "COMPRADO",
    "LONG": "COMPRADO",

    "V": "VENDIDO",
    "VENDA": "VENDIDO",
    "VENDIDO": "VENDIDO",
    "SHORT": "VENDIDO",
}


def normalize_position_side(value: Any) -> str:
    """Normaliza o lado da posicao para COMPRADO/VENDIDO."""
    if value is None:
        raise ValueError("position_side é obrigatório")

    text = str(value).strip().upper()
    if not text:
        raise ValueError("position_side é obrigatório")

    canonical = _POSITION_SIDE_ALIASES.get(text)
    if canonical is None:
        raise ValueError(
            "position_side inválido. Use COMPRADO/VENDIDO ou C/V."
        )

    return canonical


def to_pricing_engine_side(value: Any) -> str:
    """Converte COMPRADO/VENDIDO para LONG/SHORT nas bordas técnicas."""
    canonical = normalize_position_side(value)
    return {
        "COMPRADO": "LONG",
        "VENDIDO": "SHORT",
    }[canonical]
