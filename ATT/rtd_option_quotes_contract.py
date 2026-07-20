"""Contrato simulado para a aba RTD_OPTION_QUOTES.

Este modulo nao abre planilha, nao usa COM, nao cria processo,
nao escreve em banco e nao altera interface grafica.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping


RTD_OPTION_QUOTES_SHEET_NAME = "RTD_OPTION_QUOTES"

INPUT_FIELD = "codigo_opcao"

RTD_FUNCTIONS: Mapping[str, str] = MappingProxyType(
    {
        "codigo_opcao": "entrada do sistema",
        "ativo_base": "QUOTE.UNDERLYING_SYMBOL",
        "call_put": "QUOTE.OPTION_TYPE",
        "strike": "QUOTE.STRIKE_PRICE",
        "vencimento": "QUOTE.MATURITYDATE",
        "ultimo_preco": "QUOTE.LAST_TRADE_PRICE",
        "ultima_quantidade": "QUOTE.LAST_TRADE_QUANTITY",
        "bid": "QUOTE.BID_PRICE",
        "ask": "QUOTE.ASK_PRICE",
        "volume": "QUOTE.VOLUME",
        "iv": "QUOTE.IMPLIED_VOLATILITY",
        "delta": "QUOTE.DELTA",
        "gamma": "QUOTE.GAMMA",
        "theta": "QUOTE.THETA",
        "vega": "QUOTE.VEGA",
        "vwap": "QUOTE.VWAP",
    }
)

REQUIRED_FIELDS = tuple(RTD_FUNCTIONS.keys())
RESULT_FIELDS = tuple(field for field in REQUIRED_FIELDS if field != INPUT_FIELD)


class RtdOptionQuotesContractError(ValueError):
    """Erro de contrato da aba RTD_OPTION_QUOTES."""


@dataclass(frozen=True)
class RtdOptionQuotesHeaderMap:
    """Mapa validado entre campo interno e indice de coluna."""

    columns: Mapping[str, int]

    def __post_init__(self) -> None:
        object.__setattr__(self, "columns", MappingProxyType(dict(self.columns)))

    def column_index(self, field: str) -> int:
        normalized = normalize_field_name(field)

        if normalized not in self.columns:
            raise RtdOptionQuotesContractError(
                f"campo nao mapeado: {normalized}"
            )

        return self.columns[normalized]

    def input_column_index(self) -> int:
        return self.column_index(INPUT_FIELD)

    def result_column_indexes(self) -> dict[str, int]:
        return {field: self.column_index(field) for field in RESULT_FIELDS}


def normalize_field_name(field: str) -> str:
    if not isinstance(field, str):
        raise RtdOptionQuotesContractError("nome de campo deve ser texto")

    normalized = field.strip().lower()

    if not normalized:
        raise RtdOptionQuotesContractError("nome de campo vazio")

    return normalized


def required_fields() -> tuple[str, ...]:
    return REQUIRED_FIELDS


def result_fields() -> tuple[str, ...]:
    return RESULT_FIELDS


def input_field() -> str:
    return INPUT_FIELD


def rtd_functions() -> dict[str, str]:
    return dict(RTD_FUNCTIONS)


def build_header_map(headers: Iterable[object]) -> RtdOptionQuotesHeaderMap:
    if headers is None:
        raise RtdOptionQuotesContractError("cabecalhos nao informados")

    columns: dict[str, int] = {}

    for index, header in enumerate(headers):
        normalized = _normalize_header(header, index)

        if normalized in columns:
            raise RtdOptionQuotesContractError(
                f"cabecalho duplicado: {normalized}"
            )

        columns[normalized] = index

    missing = [field for field in REQUIRED_FIELDS if field not in columns]

    if missing:
        raise RtdOptionQuotesContractError(
            "cabecalho obrigatorio ausente: " + ", ".join(missing)
        )

    return RtdOptionQuotesHeaderMap(columns=columns)


def validate_headers(headers: Iterable[object]) -> RtdOptionQuotesHeaderMap:
    return build_header_map(headers)


def _normalize_header(header: object, index: int) -> str:
    column_number = index + 1

    if not isinstance(header, str):
        raise RtdOptionQuotesContractError(
            f"cabecalho invalido na coluna {column_number}: esperado texto"
        )

    normalized = header.strip().lower()

    if not normalized:
        raise RtdOptionQuotesContractError(
            f"cabecalho vazio na coluna {column_number}"
        )

    return normalized
