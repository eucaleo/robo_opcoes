"""
Normalizadores financeiros compartilhados.

Frente 19B — Preservação de gregas negativas e zeros válidos.

Regra:
- Campos de risco/gregas podem aceitar negativo e zero.
- Campos financeiros que exigem preço/volume positivo devem usar helper positivo.
- Valor vazio, inválido, NaN ou infinito vira None.
"""

from decimal import Decimal, InvalidOperation
import math
from typing import Any


_NONE_STRINGS = {
    "",
    "-",
    "--",
    "none",
    "null",
    "nan",
    "n/a",
    "na",
    "#n/a",
    "#value!",
}


def _finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError, InvalidOperation):
        return None

    if not math.isfinite(number):
        return None

    return number


def _normalize_numeric_text(value: str) -> str | None:
    text = str(value).strip()

    if not text:
        return None

    text = (
        text.replace("\xa0", "")
        .replace(" ", "")
        .replace("R$", "")
        .replace("r$", "")
        .replace("%", "")
        .replace("−", "-")
    )

    lowered = text.lower()
    if lowered in _NONE_STRINGS:
        return None

    negative_by_parentheses = text.startswith("(") and text.endswith(")")
    if negative_by_parentheses:
        text = text[1:-1].strip()

    if not text:
        return None

    if "," in text and "." in text:
        last_comma = text.rfind(",")
        last_dot = text.rfind(".")

        if last_comma > last_dot:
            # Formato BR provável: 1.234,56
            text = text.replace(".", "").replace(",", ".")
        else:
            # Formato US provável: 1,234.56
            text = text.replace(",", "")

    elif "," in text:
        # Decimal BR simples: 12,34
        text = text.replace(",", ".")

    elif text.count(".") > 1:
        # Milhar sem decimal: 1.234.567
        parts = text.split(".")
        if all(part.isdigit() for part in parts):
            text = "".join(parts)

    if negative_by_parentheses and not text.startswith("-"):
        text = "-" + text

    return text


def parse_float_br(value: Any) -> float | None:
    """Converte número em formatos comuns BR/US para float.

    Exemplos:
    - "1.234,56" -> 1234.56
    - "1,234.56" -> 1234.56
    - "-0,25" -> -0.25
    - "0" -> 0.0

    Não aplica semântica de percentual. O símbolo "%" é apenas removido.
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float, Decimal)):
        return _finite_float(value)

    text = _normalize_numeric_text(str(value))
    if text is None:
        return None

    try:
        decimal_value = Decimal(text)
    except InvalidOperation:
        return None

    return _finite_float(decimal_value)


def to_optional_float_allow_negative(value: Any) -> float | None:
    """Normalizador para gregas, variações e campos de risco.

    Preserva:
    - valores negativos;
    - zero válido;
    - positivos válidos.
    """

    return parse_float_br(value)


def to_optional_non_negative_float(value: Any) -> float | None:
    """Normalizador para campos que aceitam zero, mas não negativo."""

    number = parse_float_br(value)
    if number is None:
        return None
    if number < 0:
        return None
    return number


def to_optional_positive_float(value: Any) -> float | None:
    """Normalizador para campos que exigem valor estritamente positivo."""

    number = parse_float_br(value)
    if number is None:
        return None
    if number <= 0:
        return None
    return number


__all__ = [
    "parse_float_br",
    "to_optional_float_allow_negative",
    "to_optional_non_negative_float",
    "to_optional_positive_float",
]

# ---------------------------------------------------------------------------
# Frente 19C — API publica estavel para normalizadores financeiros
# ---------------------------------------------------------------------------
# Estes helpers separam semantica financeira:
#
# - parse_optional_risk_float:
#   aceita negativo e zero; usado para gregas, variacoes e campos de risco.
#
# - parse_optional_non_negative_float:
#   aceita zero, rejeita negativo; usado quando zero e valido mas negativo nao.
#
# - parse_optional_positive_float:
#   exige valor estritamente positivo; usado para campos como bid, ask, vwap,
#   volume e ultimo preco quando aplicavel.
#
# Mantido de forma idempotente para permitir evolucoes pequenas e testaveis.

from typing import Any, Optional


_MISSING_FINANCIAL_VALUES = {None, "", "-", "--", "None", "none", "NULL", "null", "nan", "NaN"}


def _parse_financial_float_19c(value: Any) -> Optional[float]:
    """Converte numero financeiro tolerando formato BR e retornando None para vazio/invalido."""
    if value in _MISSING_FINANCIAL_VALUES:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return None
        if parsed != parsed:
            return None
        return parsed

    text = str(value).strip()
    if text in _MISSING_FINANCIAL_VALUES:
        return None

    # Remove simbolos comuns sem assumir moeda como contrato.
    text = text.replace("R$", "").replace("%", "").strip()

    # Formato brasileiro: 1.234,56 -> 1234.56
    if "," in text:
        text = text.replace(".", "").replace(",", ".")

    try:
        parsed = float(text)
    except (TypeError, ValueError):
        return None

    if parsed != parsed:
        return None

    return parsed


def parse_optional_risk_float(value: Any) -> Optional[float]:
    """Aceita negativo e zero. Uso: delta, gamma, theta, vega, variacoes e risco."""
    return _parse_financial_float_19c(value)


def parse_optional_non_negative_float(value: Any) -> Optional[float]:
    """Aceita zero, rejeita negativo."""
    parsed = _parse_financial_float_19c(value)
    if parsed is None:
        return None
    if parsed < 0:
        return None
    return parsed


def parse_optional_positive_float(value: Any) -> Optional[float]:
    """Exige valor estritamente positivo."""
    parsed = _parse_financial_float_19c(value)
    if parsed is None:
        return None
    if parsed <= 0:
        return None
    return parsed


def parse_optional_greek_float(value: Any) -> Optional[float]:
    """Alias explicito para gregas. Preserva negativos e zero."""
    return parse_optional_risk_float(value)


def parse_optional_variation_float(value: Any) -> Optional[float]:
    """Alias explicito para variacoes. Preserva negativos e zero."""
    return parse_optional_risk_float(value)


def parse_optional_price_float(value: Any) -> Optional[float]:
    """Alias para preco financeiro operacional positivo."""
    return parse_optional_positive_float(value)

# --- Frente 19D: aliases estaveis de normalizacao financeira ---
#
# Estes aliases consolidam a API minima esperada pela Frente 19.
# Eles preservam compatibilidade com os normalizadores ja existentes e
# evitam que novas chamadas voltem a usar um conversor generico que descarte
# negativos ou zero em campos de risco.

def _frente19d_parse_number(value):
    import math

    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        number = float(value)
        if math.isnan(number) or math.isinf(number):
            return None
        return number

    text = str(value).strip()
    if not text:
        return None

    lowered = text.lower()
    if lowered in {"none", "null", "nan", "-", "--"}:
        return None

    text = (
        text.replace("\xa0", "")
        .replace("R$", "")
        .replace("%", "")
        .replace(" ", "")
        .strip()
    )

    if not text:
        return None

    # Suporte simples para formatos BR e US:
    # 1.234,56 -> 1234.56
    # 1,234.56 -> 1234.56
    # -0,25   -> -0.25
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "").replace(",", ".")

    try:
        number = float(text)
    except (TypeError, ValueError):
        return None

    if math.isnan(number) or math.isinf(number):
        return None

    return number


try:
    parse_optional_financial_float
except NameError:
    def parse_optional_financial_float(value):
        """Converte numero financeiro sem regra de sinal."""
        return _frente19d_parse_number(value)


try:
    parse_optional_risk_float
except NameError:
    def parse_optional_risk_float(value):
        """Converte campos de risco/gregas preservando negativo e zero."""
        return _frente19d_parse_number(value)


try:
    parse_risk_float
except NameError:
    parse_risk_float = parse_optional_risk_float


try:
    parse_optional_float_allow_negative
except NameError:
    parse_optional_float_allow_negative = parse_optional_risk_float


try:
    parse_optional_positive_float
except NameError:
    def parse_optional_positive_float(value):
        """Converte campos que exigem valor estritamente positivo."""
        number = _frente19d_parse_number(value)
        if number is None:
            return None
        if number <= 0:
            return None
        return number


try:
    parse_positive_float
except NameError:
    parse_positive_float = parse_optional_positive_float


try:
    parse_optional_non_negative_float
except NameError:
    def parse_optional_non_negative_float(value):
        """Converte campos que aceitam zero, mas nao aceitam negativo."""
        number = _frente19d_parse_number(value)
        if number is None:
            return None
        if number < 0:
            return None
        return number
