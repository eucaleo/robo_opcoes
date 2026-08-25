from __future__ import annotations

import math
import re
from typing import Any


# --- INICIO FRENTE 29 UTILS NUMBER PARSER CONTRACT ---
# Frente 29: contrato local de normalizacao numerica.
#
# Objetivo: criar ponto unico e reutilizavel para parsing numerico BR/Excel/CSV,
# sem trocar consumo operacional nesta frente.
#
# Esta frente nao altera persistencia.
# Esta frente nao altera sync RTD.
# Esta frente nao altera contratos financeiros.
#
# Funcoes publicas:
# - parse_float_br
# - parse_optional_float
# - parse_positive_float
# - parse_percent


_MISSING_TEXTS = {
    "",
    "-",
    "--",
    "nan",
    "none",
    "null",
    "n/a",
    "na",
}


def _is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def _clean_numeric_text(value: Any) -> str | None:
    if value is None:
        return None

    if _is_finite_number(value):
        return str(float(value))

    text = str(value).strip()
    if not text:
        return None

    lowered = text.lower().strip()
    if lowered in _MISSING_TEXTS:
        return None

    text = text.replace("\xa0", " ")
    text = text.replace("R$", "")
    text = text.replace("%", "")
    text = re.sub(r"\s+", "", text)

    negative_by_parentheses = text.startswith("(") and text.endswith(")")
    if negative_by_parentheses:
        text = text[1:-1]

    text = re.sub(r"[^0-9,.+\-]", "", text)

    if not text:
        return None

    sign = ""
    if text[0] in "+-":
        sign = text[0]
        text = text[1:]

    text = text.replace("+", "").replace("-", "")

    if not text:
        return None

    if "," in text and "." in text:
        last_comma = text.rfind(",")
        last_dot = text.rfind(".")

        if last_comma > last_dot:
            text = text.replace(".", "")
            text = text.replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")
    elif "." in text:
        parts = text.split(".")
        if len(parts) > 2:
            text = "".join(parts[:-1]) + "." + parts[-1]
        elif len(parts) == 2:
            left, right = parts
            if left.isdigit() and right.isdigit() and 1 <= len(left) <= 3 and len(right) == 3:
                text = left + right

    if negative_by_parentheses and sign != "-":
        sign = "-"

    return sign + text


def parse_float_br(value: Any, default: float | None = None) -> float | None:
    """Converte valores numericos BR/Excel/CSV para float.

    Exemplos aceitos:
    - "1.234,56" -> 1234.56
    - "1,234.56" -> 1234.56
    - "12,5" -> 12.5
    - "R$ 1.234,56" -> 1234.56
    - "(1.234,56)" -> -1234.56
    """

    if _is_finite_number(value):
        return float(value)

    text = _clean_numeric_text(value)
    if text is None:
        return default

    try:
        number = float(text)
    except (TypeError, ValueError):
        return default

    if not math.isfinite(number):
        return default

    return number


def parse_optional_float(value: Any, default: float | None = None) -> float | None:
    """Alias explicito para parsing numerico opcional."""

    return parse_float_br(value, default=default)


def parse_positive_float(
    value: Any,
    default: float | None = None,
    *,
    allow_zero: bool = False,
) -> float | None:
    """Converte para float positivo.

    Por padrao, zero e negativos retornam default.
    Quando allow_zero=True, zero e aceito.
    """

    number = parse_float_br(value, default=None)
    if number is None:
        return default

    if allow_zero:
        return number if number >= 0 else default

    return number if number > 0 else default


def parse_percent(value: Any, default: float | None = None) -> float | None:
    """Converte percentual para fracao decimal.

    Exemplos:
    - "12,5%" -> 0.125
    - "12,5" -> 0.125
    - 12.5 -> 0.125
    - 0.125 -> 0.125
    """

    if value is None:
        return default

    has_percent_symbol = "%" in str(value)
    number = parse_float_br(value, default=None)

    if number is None:
        return default

    if has_percent_symbol or abs(number) > 1:
        return number / 100.0

    return number


__all__ = [
    "parse_float_br",
    "parse_optional_float",
    "parse_positive_float",
    "parse_percent",
]
# --- FIM FRENTE 29 UTILS NUMBER PARSER CONTRACT ---
