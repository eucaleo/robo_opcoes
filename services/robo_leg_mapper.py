from __future__ import annotations

from typing import Any


def _read_attr(obj: Any, name: str, default: Any = None) -> Any:
    if hasattr(obj, name):
        return getattr(obj, name)
    if isinstance(obj, dict):
        return obj.get(name, default)
    return default


def _enum_value(value: Any) -> Any:
    if hasattr(value, "value"):
        return value.value
    return value


def to_canonical_leg(leg: Any, multiplier: float = 1.0) -> dict[str, Any]:
    cv = _enum_value(_read_attr(leg, "cv"))
    call_put = _enum_value(_read_attr(leg, "call_put"))
    ativo = _read_attr(leg, "ativo")
    strike = _read_attr(leg, "strike")
    vencimento = _read_attr(leg, "vencimento")
    quant = _read_attr(leg, "quant")
    preco = _read_attr(leg, "preco")

    cv_str = str(cv).upper().strip() if cv is not None else ""
    call_put_str = str(call_put).upper().strip() if call_put is not None else ""

    if cv_str == "C":
        position_side = "LONG"
    elif cv_str == "V":
        position_side = "SHORT"
    else:
        raise ValueError(f"invalid cv: {cv}")

    if call_put_str == "CALL":
        option_type = "CALL"
    elif call_put_str == "PUT":
        option_type = "PUT"
    else:
        raise ValueError(f"invalid call_put: {call_put}")

    return {
        "position_side": position_side,
        "option_type": option_type,
        "symbol": str(ativo).strip().upper() if ativo else None,
        "strike": float(strike),
        "expiration_date": vencimento.strftime("%Y-%m-%d") if vencimento else None,
        "quantity": int(quant),
        "premium": float(preco) if preco is not None else None,
        "multiplier": float(multiplier),
    }
