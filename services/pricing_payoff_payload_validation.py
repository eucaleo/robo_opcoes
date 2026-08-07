from __future__ import annotations

from datetime import datetime
from typing import Any


_ALLOWED_OPTION_TYPES = {"CALL", "PUT"}
_ALLOWED_POSITION_SIDES = {"COMPRADO", "VENDIDO", "LONG", "SHORT"}

_OPTION_TYPE_ALIASES = {
    "C": "CALL",
    "CALL": "CALL",
    "P": "PUT",
    "PUT": "PUT",
}

_POSITION_SIDE_ALIASES = {
    "C": "COMPRADO",
    "COMPRA": "COMPRADO",
    "COMPRADO": "COMPRADO",
    "LONG": "LONG",
    "V": "VENDIDO",
    "VENDA": "VENDIDO",
    "VENDIDO": "VENDIDO",
    "SHORT": "SHORT",
}


def _issue(code: str, message: str, path: str, severity: str = "error") -> dict[str, str]:
    return {
        "code": code,
        "message": message,
        "path": path,
        "severity": severity,
    }


def _as_upper_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    return text or None


def normalize_option_type(value: Any) -> str | None:
    """Normaliza CALL/PUT sem assumir default perigoso.

    Entradas aceitas:
    - C -> CALL
    - CALL -> CALL
    - P -> PUT
    - PUT -> PUT

    Valor desconhecido retorna None.
    """

    text = _as_upper_text(value)
    if text is None:
        return None
    return _OPTION_TYPE_ALIASES.get(text)


def normalize_position_side(value: Any) -> str | None:
    """Normaliza lado de posição sem assumir default perigoso.

    Entradas aceitas:
    - C, COMPRA, COMPRADO -> COMPRADO
    - V, VENDA, VENDIDO -> VENDIDO
    - LONG -> LONG
    - SHORT -> SHORT

    Valor desconhecido retorna None.
    """

    text = _as_upper_text(value)
    if text is None:
        return None
    return _POSITION_SIDE_ALIASES.get(text)


def _is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int | float):
        return True
    if isinstance(value, str):
        text = value.strip().replace(",", ".")
        if not text:
            return False
        try:
            float(text)
            return True
        except ValueError:
            return False
    return False


def _to_float(value: Any) -> float | None:
    if not _is_number(value):
        return None
    if isinstance(value, str):
        return float(value.strip().replace(",", "."))
    return float(value)


def _is_iso_date(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    if not text:
        return False
    try:
        datetime.fromisoformat(text[:10])
        return True
    except ValueError:
        return False


def validate_leg_for_pricing_payoff(leg: Any, index: int = 0) -> dict[str, Any]:
    """Valida uma leg para uso seguro em pricing/payoff.

    A funcao apenas valida e normaliza informacoes minimas.
    Nao grava dados, nao consulta banco e nao altera fluxo operacional.
    """

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    path = f"legs[{index}]"

    if not isinstance(leg, dict):
        return {
            "valid": False,
            "normalized": None,
            "errors": [
                _issue(
                    "leg_not_dict",
                    "Leg deve ser um dicionario.",
                    path,
                )
            ],
            "warnings": [],
        }

    option_type_raw = leg.get("option_type", leg.get("call_put"))
    option_type = normalize_option_type(option_type_raw)
    if option_type not in _ALLOWED_OPTION_TYPES:
        errors.append(
            _issue(
                "invalid_option_type",
                "option_type deve ser CALL ou PUT; C/P sao aceitos apenas como aliases explicitos.",
                f"{path}.option_type",
            )
        )

    position_side_raw = leg.get("position_side", leg.get("side", leg.get("cv")))
    position_side = normalize_position_side(position_side_raw)
    if position_side not in _ALLOWED_POSITION_SIDES:
        errors.append(
            _issue(
                "invalid_position_side",
                "position_side deve ser COMPRADO/VENDIDO ou LONG/SHORT; C/V sao aceitos apenas como aliases explicitos.",
                f"{path}.position_side",
            )
        )

    quantity = _to_float(leg.get("quantity", leg.get("quant")))
    if quantity is None or quantity <= 0:
        errors.append(
            _issue(
                "invalid_quantity",
                "quantity deve ser numerico e maior que zero.",
                f"{path}.quantity",
            )
        )

    strike = _to_float(leg.get("strike"))
    if strike is None or strike <= 0:
        errors.append(
            _issue(
                "invalid_strike",
                "strike deve ser numerico e maior que zero.",
                f"{path}.strike",
            )
        )

    expiration_date = leg.get("expiration_date", leg.get("vencimento"))
    if not _is_iso_date(expiration_date):
        errors.append(
            _issue(
                "invalid_expiration_date",
                "expiration_date deve existir e estar em formato ISO YYYY-MM-DD.",
                f"{path}.expiration_date",
            )
        )

    multiplier = _to_float(leg.get("multiplier"))
    if multiplier is None:
        warnings.append(
            _issue(
                "missing_multiplier",
                "multiplier nao informado; validacao nao assume default implicito.",
                f"{path}.multiplier",
                severity="warning",
            )
        )
    elif multiplier <= 0:
        errors.append(
            _issue(
                "invalid_multiplier",
                "multiplier deve ser maior que zero.",
                f"{path}.multiplier",
            )
        )

    for field_name in ("premium", "entry_premium", "current_price"):
        if field_name in leg:
            value = _to_float(leg.get(field_name))
            if value is None or value < 0:
                errors.append(
                    _issue(
                        f"invalid_{field_name}",
                        f"{field_name} deve ser numerico e maior ou igual a zero quando informado.",
                        f"{path}.{field_name}",
                    )
                )

    if "price" in leg:
        warnings.append(
            _issue(
                "ambiguous_price_field",
                "Campo price e ambiguo; prefira premium/entry_premium ou current_price.",
                f"{path}.price",
                severity="warning",
            )
        )

    normalized = {
        "option_type": option_type,
        "position_side": position_side,
        "quantity": quantity,
        "strike": strike,
        "expiration_date": str(expiration_date).strip() if expiration_date is not None else None,
        "multiplier": multiplier,
    }

    return {
        "valid": not errors,
        "normalized": normalized,
        "errors": errors,
        "warnings": warnings,
    }


def validate_pricing_payoff_payload(payload: Any) -> dict[str, Any]:
    """Valida payload minimo de pricing/payoff de forma controlada.

    Contrato desta frente:
    - nao altera persistencia;
    - nao altera schema;
    - nao executa pricing;
    - nao executa payoff;
    - apenas retorna diagnostico estruturado.
    """

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    normalized_legs: list[dict[str, Any]] = []

    if not isinstance(payload, dict):
        return {
            "status": "error",
            "valid": False,
            "errors": [
                _issue(
                    "payload_not_dict",
                    "Payload de pricing/payoff deve ser um dicionario.",
                    "payload",
                )
            ],
            "warnings": [],
            "normalized": {},
        }

    structure_id = payload.get("structure_id")
    if structure_id is None:
        warnings.append(
            _issue(
                "missing_structure_id",
                "structure_id nao informado; permitido nesta validacao, mas recomendado para rastreabilidade canonica.",
                "payload.structure_id",
                severity="warning",
            )
        )

    legs = payload.get("legs")
    if not isinstance(legs, list) or not legs:
        errors.append(
            _issue(
                "invalid_legs",
                "payload.legs deve ser uma lista nao vazia.",
                "payload.legs",
            )
        )
    else:
        for index, leg in enumerate(legs):
            leg_result = validate_leg_for_pricing_payoff(leg, index=index)
            errors.extend(leg_result["errors"])
            warnings.extend(leg_result["warnings"])
            if leg_result["normalized"] is not None:
                normalized_legs.append(leg_result["normalized"])

    valid = not errors

    return {
        "status": "ok" if valid else "error",
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
        "normalized": {
            "structure_id": structure_id,
            "legs": normalized_legs,
        },
    }


__all__ = [
    "normalize_option_type",
    "normalize_position_side",
    "validate_leg_for_pricing_payoff",
    "validate_pricing_payoff_payload",
]
