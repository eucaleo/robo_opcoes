"""
Contrato financeiro canonico de uma leg.

Este modulo centraliza a semantica minima de uma leg financeira para
pricing, payoff e viewmodel.

Regras principais:
- multiplier canonico de opcoes: 100.0
- premium: preco de entrada
- current_price: preco atual de mercado
- price: campo legado ambiguo, aceito apenas quando explicitamente permitido
"""

from typing import Any


CANONICAL_OPTION_MULTIPLIER = 100.0

CANONICAL_LEG_FIELDS = (
    "position_side",
    "pricing_side",
    "option_type",
    "symbol",
    "strike",
    "expiration_date",
    "quantity",
    "premium",
    "current_price",
    "multiplier",
)


class LegFinancialContractError(ValueError):
    """Erro de contrato financeiro de leg."""


def normalize_position_side(value: Any) -> str:
    text = _required_text(value, "position_side").upper()

    bought = {"C", "COMPRA", "COMPRADO", "LONG", "BUY", "B"}
    sold = {"V", "VENDA", "VENDIDO", "SHORT", "SELL", "S"}

    if text in bought:
        return "COMPRADO"
    if text in sold:
        return "VENDIDO"

    raise LegFinancialContractError(
        f"position_side invalido: {value!r}. Use COMPRADO ou VENDIDO."
    )


def pricing_side_from_position(position_side: Any) -> str:
    normalized = normalize_position_side(position_side)
    if normalized == "COMPRADO":
        return "LONG"
    if normalized == "VENDIDO":
        return "SHORT"
    raise LegFinancialContractError(f"position_side invalido: {position_side!r}")


def normalize_option_type(value: Any) -> str:
    text = _required_text(value, "option_type").upper()

    if text in {"C", "CALL"}:
        return "CALL"
    if text in {"P", "PUT"}:
        return "PUT"

    raise LegFinancialContractError(
        f"option_type invalido: {value!r}. Use CALL ou PUT."
    )


def normalize_symbol(value: Any) -> str:
    return _required_text(value, "symbol").upper()


def normalize_multiplier(
    value: Any = None,
    *,
    allow_non_standard_multiplier: bool = False,
) -> float:
    if value is None or value == "":
        multiplier = CANONICAL_OPTION_MULTIPLIER
    else:
        multiplier = _to_float(value, "multiplier")

    if multiplier <= 0:
        raise LegFinancialContractError("multiplier deve ser positivo.")

    if (
        not allow_non_standard_multiplier
        and abs(multiplier - CANONICAL_OPTION_MULTIPLIER) > 0.000000001
    ):
        raise LegFinancialContractError(
            "multiplier nao canonico detectado. "
            "Para opcoes, use 100.0 ou habilite allow_non_standard_multiplier."
        )

    return float(multiplier)


def canonicalize_leg(
    raw_leg: dict[str, Any],
    *,
    allow_legacy_price: bool = False,
    allow_non_standard_multiplier: bool = False,
) -> dict[str, Any]:
    if not isinstance(raw_leg, dict):
        raise LegFinancialContractError("raw_leg deve ser dict.")

    warnings: list[str] = []

    position_source = _first_present(
        raw_leg,
        "position_side",
        "side",
        "cv",
        "compra_venda",
    )
    option_source = _first_present(
        raw_leg,
        "option_type",
        "call_put",
        "tipo",
    )

    position_side = normalize_position_side(position_source)
    pricing_side = pricing_side_from_position(position_side)
    option_type = normalize_option_type(option_source)

    symbol = normalize_symbol(_first_present(raw_leg, "symbol", "ativo", "ticker"))
    strike = _to_positive_float(_first_present(raw_leg, "strike", "preco_exercicio"), "strike")
    expiration_date = _required_text(
        _first_present(raw_leg, "expiration_date", "vencimento"),
        "expiration_date",
    )
    quantity = _to_positive_int(_first_present(raw_leg, "quantity", "quant", "qtd"), "quantity")

    premium = _to_optional_float(
        _first_present(raw_leg, "premium", "entry_premium"),
        "premium",
    )
    current_price = _to_optional_float(
        _first_present(raw_leg, "current_price"),
        "current_price",
    )

    legacy_price_present = "price" in raw_leg and raw_leg.get("price") not in (None, "")
    if legacy_price_present:
        if not allow_legacy_price:
            raise LegFinancialContractError(
                "Campo legado price detectado. Use premium ou current_price."
            )

        legacy_price = _to_optional_float(raw_leg.get("price"), "price")
        if current_price is None:
            current_price = legacy_price
            warnings.append("legacy_price_usado_como_current_price")
        else:
            warnings.append("legacy_price_ignorado_por_current_price_explicito")

    multiplier = normalize_multiplier(
        raw_leg.get("multiplier"),
        allow_non_standard_multiplier=allow_non_standard_multiplier,
    )

    canonical = {
        "position_side": position_side,
        "pricing_side": pricing_side,
        "option_type": option_type,
        "symbol": symbol,
        "strike": strike,
        "expiration_date": expiration_date,
        "quantity": quantity,
        "premium": premium,
        "current_price": current_price,
        "multiplier": multiplier,
    }

    if warnings:
        canonical["contract_warnings"] = warnings

    return canonical


def assert_canonical_leg(leg: dict[str, Any]) -> None:
    missing = [field for field in CANONICAL_LEG_FIELDS if field not in leg]
    if missing:
        raise LegFinancialContractError(
            "Leg canonica incompleta. Campos ausentes: " + ", ".join(missing)
        )

    normalize_position_side(leg["position_side"])
    pricing_side = leg["pricing_side"]
    if pricing_side not in {"LONG", "SHORT"}:
        raise LegFinancialContractError("pricing_side deve ser LONG ou SHORT.")

    expected_pricing_side = pricing_side_from_position(leg["position_side"])
    if pricing_side != expected_pricing_side:
        raise LegFinancialContractError(
            "pricing_side inconsistente com position_side."
        )

    normalize_option_type(leg["option_type"])
    normalize_symbol(leg["symbol"])
    _to_positive_float(leg["strike"], "strike")
    _required_text(leg["expiration_date"], "expiration_date")
    _to_positive_int(leg["quantity"], "quantity")
    _to_optional_float(leg["premium"], "premium")
    _to_optional_float(leg["current_price"], "current_price")
    normalize_multiplier(leg["multiplier"])

    if "price" in leg:
        raise LegFinancialContractError(
            "price nao e campo canonico de leg. Use premium ou current_price."
        )


def financial_value_from_unit_price(
    unit_price: Any,
    quantity: Any,
    *,
    multiplier: Any = None,
) -> float:
    normalized_price = _to_float(unit_price, "unit_price")
    normalized_quantity = _to_positive_int(quantity, "quantity")
    normalized_multiplier = normalize_multiplier(multiplier)
    return normalized_price * normalized_quantity * normalized_multiplier


def _first_present(source: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in source and source[key] not in (None, ""):
            return source[key]
    return None


def _required_text(value: Any, field_name: str) -> str:
    if value is None:
        raise LegFinancialContractError(f"{field_name} obrigatorio.")

    text = str(value).strip()
    if not text:
        raise LegFinancialContractError(f"{field_name} obrigatorio.")

    return text


def _to_float(value: Any, field_name: str) -> float:
    if value is None or value == "":
        raise LegFinancialContractError(f"{field_name} obrigatorio.")

    if isinstance(value, bool):
        raise LegFinancialContractError(f"{field_name} invalido: {value!r}")

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().replace(" ", "")
    if not text:
        raise LegFinancialContractError(f"{field_name} obrigatorio.")

    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError as exc:
        raise LegFinancialContractError(
            f"{field_name} numerico invalido: {value!r}"
        ) from exc


def _to_optional_float(value: Any, field_name: str) -> float | None:
    if value is None or value == "":
        return None
    return _to_float(value, field_name)


def _to_positive_float(value: Any, field_name: str) -> float:
    number = _to_float(value, field_name)
    if number <= 0:
        raise LegFinancialContractError(f"{field_name} deve ser positivo.")
    return number


def _to_positive_int(value: Any, field_name: str) -> int:
    number = _to_float(value, field_name)
    if number <= 0:
        raise LegFinancialContractError(f"{field_name} deve ser positivo.")

    integer = int(number)
    if abs(number - integer) > 0.000000001:
        raise LegFinancialContractError(f"{field_name} deve ser inteiro.")

    return integer
