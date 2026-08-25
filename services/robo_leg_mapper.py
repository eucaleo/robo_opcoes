from __future__ import annotations

from typing import Any

from utils.leg_normalizers import normalize_option_type, normalize_position_side, normalize_option_multiplier


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


def _safe_upper_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text.upper() if text else None


def _to_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {field_name}: {value}") from exc


def _to_int(value: Any, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {field_name}: {value}") from exc


def _normalize_expiration_date(value: Any) -> str | None:
    if value is None:
        return None

    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")

    text = str(value).strip()
    if not text:
        return None

    if "T" in text:
        return text.split("T", 1)[0]

    if " " in text:
        return text.split(" ", 1)[0]

    return text


def to_canonical_leg(leg: Any, multiplier: float | None = None) -> dict[str, Any]:
    cv = _enum_value(_read_attr(leg, "cv"))
    call_put = _enum_value(_read_attr(leg, "call_put"))
    ativo = _read_attr(leg, "ativo")
    strike = _read_attr(leg, "strike")
    vencimento = _read_attr(leg, "vencimento")
    quant = _read_attr(leg, "quant")
    preco = _read_attr(leg, "preco")

    cv_str = str(cv).upper().strip() if cv is not None else ""
    call_put_str = str(call_put).upper().strip() if call_put is not None else ""

    try:
        position_side = normalize_position_side(cv_str)
    except ValueError as exc:
        raise ValueError(f"invalid cv: {cv}") from exc

    try:
        option_type = normalize_option_type(call_put_str)
    except ValueError as exc:
        raise ValueError(f"invalid call_put: {call_put}") from exc

    return {
        "position_side": position_side,
        "option_type": option_type,
        "symbol": _safe_upper_text(ativo),
        "strike": _to_float(strike, "strike"),
        "expiration_date": _normalize_expiration_date(vencimento),
        "quantity": _to_int(quant, "quant"),
        "premium": float(preco) if preco is not None else None,
        "multiplier": normalize_option_multiplier(multiplier),
    }
