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
