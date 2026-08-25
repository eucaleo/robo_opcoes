from __future__ import annotations

import re
from typing import Any, Dict, Optional


DEFAULT_WORKBOOK_NAME = "LISTA_RTD.xlsm"
DEFAULT_SHEET_NAME = "RTD_OPTION_QUOTES"


RTD_OPTION_QUOTES_MAP: Dict[str, Dict[str, Optional[str]]] = {
    "codigo_opcao": {
        "role": "input",
        "rtd": None,
        "db_field": "codigo_opcao",
    },
    "ativo_base": {
        "role": "rtd",
        "rtd": "QUOTE.UNDERLYING_SYMBOL",
        "db_field": "ativo_base",
    },
    "call_put": {
        "role": "rtd",
        "rtd": "QUOTE.OPTION_TYPE",
        "db_field": "call_put",
    },
    "strike": {
        "role": "rtd",
        "rtd": "QUOTE.STRIKE_PRICE",
        "db_field": "strike",
    },
    "vencimento": {
        "role": "rtd",
        "rtd": "QUOTE.MATURITYDATE",
        "db_field": "vencimento",
    },
    "ultimo_preco": {
        "role": "rtd",
        "rtd": "QUOTE.LAST_TRADE_PRICE",
        "db_field": "ultimo_preco",
    },
    "ultima_quantidade": {
        "role": "rtd",
        "rtd": "QUOTE.LAST_TRADE_QUANTITY",
        "db_field": "ultima_quantidade",
    },
    "bid": {
        "role": "rtd",
        "rtd": "QUOTE.BID_PRICE",
        "db_field": "bid",
    },
    "ask": {
        "role": "rtd",
        "rtd": "QUOTE.ASK_PRICE",
        "db_field": "ask",
    },
    "volume": {
        "role": "rtd",
        "rtd": "QUOTE.VOLUME",
        "db_field": "volume",
    },
    "iv": {
        "role": "rtd",
        "rtd": "QUOTE.IMPLIED_VOLATILITY",
        "db_field": "iv",
    },
    "delta": {
        "role": "rtd",
        "rtd": "QUOTE.DELTA",
        "db_field": "delta",
    },
    "gamma": {
        "role": "rtd",
        "rtd": "QUOTE.GAMMA",
        "db_field": "gamma",
    },
    "theta": {
        "role": "rtd",
        "rtd": "QUOTE.THETA",
        "db_field": "theta",
    },
    "vega": {
        "role": "rtd",
        "rtd": "QUOTE.VEGA",
        "db_field": "vega",
    },
    "vwap": {
        "role": "rtd",
        "rtd": "QUOTE.VWAP",
        "db_field": "vwap",
    },
}


REQUIRED_OPTION_HEADERS = list(RTD_OPTION_QUOTES_MAP.keys())


def normalize_header(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = text.replace("\ufeff", "")
    text = re.sub(r"\s+", "_", text)
    text = text.replace("-", "_")
    text = text.replace(".", "_")
    text = re.sub(r"[^a-z0-9_]+", "", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")

# --- Frente 20B: contrato canonico RTD Option Quotes BEGIN ---
#
# Objetivo:
#   Expor um contrato canônico e estável para RTD Option Quotes a partir
#   deste próprio módulo, sem trocar fluxo operacional nesta etapa.
#
# Regra de contenção:
#   Este bloco não substitui sincronizadores, bridges, importadores ou
#   persistência. Ele apenas torna explícito o contrato que as próximas
#   frentes poderão consumir de forma controlada.

import re as _front20b_re
import unicodedata as _front20b_unicodedata
from typing import Any as _Front20BAny


def _front20b_slug(value: _Front20BAny) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = _front20b_unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not _front20b_unicodedata.combining(ch))
    text = _front20b_re.sub(r"[^a-z0-9]+", "_", text)
    text = _front20b_re.sub(r"_+", "_", text)
    return text.strip("_")


if "normalize_header" not in globals():

    def normalize_header(value: _Front20BAny) -> str:
        return _front20b_slug(value)


def _front20b_normalize_header(value: _Front20BAny) -> str:
    normalizer = globals().get("normalize_header")
    if callable(normalizer):
        try:
            normalized = normalizer(value)
        except Exception:
            normalized = _front20b_slug(value)
    else:
        normalized = _front20b_slug(value)

    normalized_text = "" if normalized is None else str(normalized)
    normalized_text = normalized_text.strip()
    return normalized_text or _front20b_slug(value)


def _front20b_existing_sequence(*names: str) -> tuple[_Front20BAny, ...]:
    for name in names:
        value = globals().get(name)
        if isinstance(value, dict):
            items = tuple(value.keys())
        elif isinstance(value, (list, tuple, set, frozenset)):
            items = tuple(value)
        else:
            continue

        cleaned = tuple(item for item in items if item is not None and str(item).strip())
        if cleaned:
            return cleaned

    return ()


def _front20b_unique_texts(values: tuple[_Front20BAny, ...]) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        text = "" if value is None else str(value).strip()
        if not text:
            continue
        if text in seen:
            continue
        seen.add(text)
        result.append(text)

    return tuple(result)


def _front20b_unique_headers(values: tuple[_Front20BAny, ...]) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()

    for value in values:
        header = _front20b_normalize_header(value)
        if not header:
            continue
        if header in seen:
            continue
        seen.add(header)
        result.append(header)

    return tuple(result)


_FRONT20B_DEFAULT_HEADERS = (
    "ticker",
    "symbol",
    "option_type",
    "strike",
    "expiration_date",
    "bid",
    "ask",
    "last",
    "last_price",
    "volume",
    "vwap",
    "delta",
    "gamma",
    "theta",
    "vega",
    "captured_at",
)

_FRONT20B_DEFAULT_REQUIRED_HEADERS = (
    "ticker",
    "bid",
    "ask",
)

_front20b_source_headers = _front20b_existing_sequence(
    "RTD_OPTION_QUOTES_HEADERS",
    "OPTION_QUOTES_HEADERS",
    "DEFAULT_HEADERS",
    "HEADERS",
    "COLUMNS",
)

_front20b_source_required_headers = _front20b_existing_sequence(
    "RTD_OPTION_QUOTES_REQUIRED_HEADERS",
    "REQUIRED_RTD_HEADERS",
    "REQUIRED_HEADERS",
)

_front20b_source_rtd_fields = _front20b_existing_sequence(
    "RTD_OPTION_QUOTES_RTD_FIELDS",
    "RTD_FIELDS",
    "FIELDS",
)

CANONICAL_RTD_OPTION_QUOTES_REQUIRED_HEADERS = _front20b_unique_headers(
    _front20b_source_required_headers or _FRONT20B_DEFAULT_REQUIRED_HEADERS
)

CANONICAL_RTD_OPTION_QUOTES_HEADERS = _front20b_unique_headers(
    (_front20b_source_headers or _FRONT20B_DEFAULT_HEADERS)
    + CANONICAL_RTD_OPTION_QUOTES_REQUIRED_HEADERS
)

CANONICAL_RTD_OPTION_QUOTES_RTD_FIELDS = _front20b_unique_texts(
    _front20b_source_rtd_fields or CANONICAL_RTD_OPTION_QUOTES_HEADERS
)

CANONICAL_RTD_OPTION_QUOTES_WORKBOOK_NAME = str(
    globals().get(
        "DEFAULT_WORKBOOK_NAME",
        globals().get(
            "WORKBOOK_NAME",
            globals().get("RTD_OPTION_QUOTES_WORKBOOK_NAME", "LISTA_RTD.xlsm"),
        ),
    )
).strip()

CANONICAL_RTD_OPTION_QUOTES_SHEET_NAME = str(
    globals().get(
        "DEFAULT_SHEET_NAME",
        globals().get(
            "SHEET_NAME",
            globals().get("RTD_OPTION_QUOTES_SHEET_NAME", "RTD_OPTION_QUOTES"),
        ),
    )
).strip()

RTD_OPTION_QUOTES_SCHEMA_SOURCE = "services.rtd_option_quotes_schema"


def get_rtd_option_quotes_contract() -> dict[str, _Front20BAny]:
    """Retorna o contrato canônico RTD Option Quotes sem executar sync operacional."""
    return {
        "source": RTD_OPTION_QUOTES_SCHEMA_SOURCE,
        "workbook_name": CANONICAL_RTD_OPTION_QUOTES_WORKBOOK_NAME,
        "sheet_name": CANONICAL_RTD_OPTION_QUOTES_SHEET_NAME,
        "headers": CANONICAL_RTD_OPTION_QUOTES_HEADERS,
        "required_headers": CANONICAL_RTD_OPTION_QUOTES_REQUIRED_HEADERS,
        "rtd_fields": CANONICAL_RTD_OPTION_QUOTES_RTD_FIELDS,
        "normalize_header": normalize_header,
        "operational_switch": False,
    }


__all__ = tuple(
    dict.fromkeys(
        list(globals().get("__all__", ()))
        + [
            "CANONICAL_RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "CANONICAL_RTD_OPTION_QUOTES_SHEET_NAME",
            "CANONICAL_RTD_OPTION_QUOTES_HEADERS",
            "CANONICAL_RTD_OPTION_QUOTES_REQUIRED_HEADERS",
            "CANONICAL_RTD_OPTION_QUOTES_RTD_FIELDS",
            "RTD_OPTION_QUOTES_SCHEMA_SOURCE",
            "normalize_header",
            "get_rtd_option_quotes_contract",
        ]
    )
)
# --- Frente 20B: contrato canonico RTD Option Quotes END ---

# --- Frente 20B local fix: stable header normalizer ---
import re as _front20b_fix_re
import unicodedata as _front20b_fix_unicodedata


def normalize_header(value):
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = _front20b_fix_unicodedata.normalize("NFKD", text)
    text = "".join(
        ch for ch in text
        if not _front20b_fix_unicodedata.combining(ch)
    )
    text = _front20b_fix_re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")
    return text

# --- Frente 21C: API publica minima de headers RTD Option Quotes ---

def _frente21c_extract_header_strings(value, depth=0):
    """Extrai tokens textuais de estruturas simples sem assumir formato interno."""
    if depth > 6:
        return []

    if value is None:
        return []

    if isinstance(value, str):
        token = value.strip()
        return [token] if token else []

    if isinstance(value, dict):
        items = []
        for key, val in value.items():
            items.extend(_frente21c_extract_header_strings(key, depth + 1))
            items.extend(_frente21c_extract_header_strings(val, depth + 1))
        return items

    if isinstance(value, (list, tuple, set, frozenset)):
        items = []
        for item in value:
            items.extend(_frente21c_extract_header_strings(item, depth + 1))
        return items

    return []


def _frente21c_clean_header_token(value):
    token = str(value).strip()
    if not token:
        return None

    # Evita capturar nomes de arquivo, paths e textos claramente documentais.
    lowered = token.lower()
    if "\n" in token or "\r" in token:
        return None
    if len(token) > 120:
        return None
    if lowered.endswith((".xls", ".xlsx", ".xlsm", ".csv", ".db", ".sqlite")):
        return None
    if "\\" in token or "/" in token:
        return None

    return token


def _frente21c_unique_headers(values):
    seen = set()
    headers = []

    for value in values:
        token = _frente21c_clean_header_token(value)
        if token is None:
            continue

        key = token.casefold()
        if key in seen:
            continue

        seen.add(key)
        headers.append(token)

    return tuple(headers)


def _frente21c_headers_from_named_candidates(candidate_names):
    namespace = globals()

    for name in candidate_names:
        value = namespace.get(name)
        headers = _frente21c_unique_headers(_frente21c_extract_header_strings(value))
        if headers:
            return headers

    return tuple()


def _frente21c_discover_headers_from_schema():
    namespace = globals()
    best = tuple()

    ignored_names = {
        "datetime",
        "Path",
        "Any",
        "Iterable",
        "Sequence",
        "Mapping",
    }

    for name, value in namespace.items():
        if name.startswith("__") or name in ignored_names:
            continue
        if callable(value):
            continue

        headers = _frente21c_unique_headers(_frente21c_extract_header_strings(value))
        if len(headers) > len(best):
            best = headers

    return best


def rtd_option_quotes_headers():
    """
    Retorna headers RTD Option Quotes a partir do contrato canonico local.

    Frente 21C:
    - expõe uma API pequena e estável para consumidores;
    - preserva `services/rtd_option_quotes_schema.py` como fonte do contrato;
    - não exige que consumidores conheçam nomes internos de constantes.
    """
    candidate_names = (
        "HEADERS",
        "RTD_OPTION_QUOTES_HEADERS",
        "CANONICAL_HEADERS",
        "OPTION_QUOTES_HEADERS",
        "RTD_HEADERS",
        "COLUMNS",
        "CANONICAL_COLUMNS",
        "FIELDS",
        "RTD_FIELDS",
    )

    headers = _frente21c_headers_from_named_candidates(candidate_names)
    if headers:
        return headers

    headers = _frente21c_discover_headers_from_schema()
    if headers:
        return headers

    raise RuntimeError(
        "Contrato RTD Option Quotes sem headers consumiveis em "
        "services/rtd_option_quotes_schema.py."
    )


def rtd_option_quotes_required_headers():
    """
    Retorna headers obrigatorios RTD Option Quotes a partir do contrato canonico.

    Quando o schema local nao diferencia explicitamente obrigatorios e totais,
    retorna os headers canonicos disponiveis, mantendo compatibilidade local.
    """
    candidate_names = (
        "REQUIRED_HEADERS",
        "RTD_OPTION_QUOTES_REQUIRED_HEADERS",
        "REQUIRED_RTD_OPTION_QUOTES_HEADERS",
        "CANONICAL_REQUIRED_HEADERS",
        "REQUIRED_COLUMNS",
        "REQUIRED_FIELDS",
    )

    headers = _frente21c_headers_from_named_candidates(candidate_names)
    if headers:
        return headers

    return rtd_option_quotes_headers()


# --- fim Frente 21C ---


# Frente 21D - API publica minima workbook/sheet
def _rtd_option_quotes_first_defined_text(candidate_names, default):
    """
    Retorna o primeiro texto não vazio encontrado no namespace do schema.

    Esta função existe para manter compatibilidade com nomes internos históricos
    sem obrigar troca ampla de constantes nesta frente.
    """
    namespace = globals()
    for name in candidate_names:
        value = namespace.get(name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return str(default).strip()


def rtd_option_quotes_workbook_name():
    """
    API pública mínima para o nome da pasta de trabalho RTD Option Quotes.

    Mantém o contrato centralizado em services/rtd_option_quotes_schema.py sem
    exigir que consumidores conheçam o nome interno da constante.
    """
    return _rtd_option_quotes_first_defined_text(
        (
            "RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "DEFAULT_RTD_OPTION_QUOTES_WORKBOOK_NAME",
            "DEFAULT_WORKBOOK_NAME",
            "WORKBOOK_NAME",
            "EXCEL_WORKBOOK_NAME",
            "DEFAULT_EXCEL_WORKBOOK_NAME",
        ),
        "LISTA_RTD.xlsm",
    )


def rtd_option_quotes_sheet_name():
    """
    API pública mínima para o nome da planilha RTD Option Quotes.

    Mantém o contrato centralizado em services/rtd_option_quotes_schema.py sem
    exigir que consumidores conheçam o nome interno da constante.
    """
    return _rtd_option_quotes_first_defined_text(
        (
            "RTD_OPTION_QUOTES_SHEET_NAME",
            "DEFAULT_RTD_OPTION_QUOTES_SHEET_NAME",
            "DEFAULT_SHEET_NAME",
            "SHEET_NAME",
            "EXCEL_SHEET_NAME",
            "DEFAULT_EXCEL_SHEET_NAME",
        ),
        "RTD_OPTION_QUOTES",
    )
