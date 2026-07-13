from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from rtd_excel_online.fase7_alertas_decisao import (
    ParametrosAlerta,
    ResultadoAvaliacao,
    SnapshotMercado,
    avaliar_snapshot,
)


def snapshot_mercado_from_rtd_option_quote(
    quote: Mapping[str, Any] | Any,
    *,
    preco_anterior: Any = None,
    vwap_anterior: Any = None,
    payoff_anterior: Any = None,
    payoff_atual: Any = None,
    estrutura_favoravel: bool | None = None,
) -> SnapshotMercado:
    """Converte uma linha local de rtd_option_quotes em SnapshotMercado."""

    simbolo = _first_text(
        _field(quote, "codigo_opcao"),
        _field(quote, "simbolo"),
        _field(quote, "ativo"),
    )

    if not simbolo:
        raise ValueError("codigo_opcao/simbolo obrigatorio")

    return SnapshotMercado(
        simbolo=simbolo.upper(),
        ultimo_preco=_to_float(_field(quote, "ultimo_preco")),
        vwap=_to_float(_field(quote, "vwap")),
        preco_anterior=_to_float(_explicit_or_field(preco_anterior, quote, "preco_anterior")),
        vwap_anterior=_to_float(_explicit_or_field(vwap_anterior, quote, "vwap_anterior")),
        bid=_to_float(_field(quote, "bid")),
        ask=_to_float(_field(quote, "ask")),
        volume=_to_float(_field(quote, "volume")),
        payoff_anterior=_to_float(_explicit_or_field(payoff_anterior, quote, "payoff_anterior")),
        payoff_atual=_to_float(_explicit_or_field(payoff_atual, quote, "payoff_atual")),
        estrutura_favoravel=_to_bool(
            _explicit_or_field(estrutura_favoravel, quote, "estrutura_favoravel")
        ),
    )


def snapshot_mercado_from_leg_market_snapshot(
    leg: Mapping[str, Any] | Any,
    *,
    vwap: Any = None,
    preco_anterior: Any = None,
    vwap_anterior: Any = None,
    volume: Any = None,
    payoff_anterior: Any = None,
    payoff_atual: Any = None,
    estrutura_favoravel: bool | None = None,
) -> SnapshotMercado:
    """Converte uma leg local tipo LegMarketSnapshot em SnapshotMercado."""

    simbolo = _first_text(
        _field(leg, "ativo"),
        _field(leg, "simbolo"),
        _field(leg, "codigo_opcao"),
    )

    if not simbolo:
        raise ValueError("ativo/simbolo obrigatorio")

    ultimo_preco = _first_float(
        _field(leg, "valor_executado"),
        _field(leg, "mid"),
        _field(leg, "ultimo_preco"),
    )

    return SnapshotMercado(
        simbolo=simbolo.upper(),
        ultimo_preco=ultimo_preco,
        vwap=_to_float(_explicit_or_field(vwap, leg, "vwap")),
        preco_anterior=_to_float(_explicit_or_field(preco_anterior, leg, "preco_anterior")),
        vwap_anterior=_to_float(_explicit_or_field(vwap_anterior, leg, "vwap_anterior")),
        bid=_to_float(_field(leg, "bid")),
        ask=_to_float(_field(leg, "ask")),
        volume=_to_float(_explicit_or_field(volume, leg, "volume")),
        payoff_anterior=_to_float(_explicit_or_field(payoff_anterior, leg, "payoff_anterior")),
        payoff_atual=_to_float(
            _explicit_or_field(
                payoff_atual,
                leg,
                "payoff_atual",
                fallback_field="pl_realista",
            )
        ),
        estrutura_favoravel=_to_bool(
            _explicit_or_field(estrutura_favoravel, leg, "estrutura_favoravel")
        ),
    )


def avaliar_rtd_option_quote(
    quote: Mapping[str, Any] | Any,
    parametros: ParametrosAlerta | None = None,
    *,
    preco_anterior: Any = None,
    vwap_anterior: Any = None,
    payoff_anterior: Any = None,
    payoff_atual: Any = None,
    estrutura_favoravel: bool | None = None,
) -> ResultadoAvaliacao:
    """Avalia uma linha local de rtd_option_quotes no motor da Fase 7."""

    snapshot = snapshot_mercado_from_rtd_option_quote(
        quote,
        preco_anterior=preco_anterior,
        vwap_anterior=vwap_anterior,
        payoff_anterior=payoff_anterior,
        payoff_atual=payoff_atual,
        estrutura_favoravel=estrutura_favoravel,
    )

    return avaliar_snapshot(
        snapshot,
        parametros,
        timestamp=_timestamp_from(quote),
    )


def avaliar_leg_market_snapshot(
    leg: Mapping[str, Any] | Any,
    parametros: ParametrosAlerta | None = None,
    *,
    vwap: Any = None,
    preco_anterior: Any = None,
    vwap_anterior: Any = None,
    volume: Any = None,
    payoff_anterior: Any = None,
    payoff_atual: Any = None,
    estrutura_favoravel: bool | None = None,
) -> ResultadoAvaliacao:
    """Avalia uma leg local tipo LegMarketSnapshot no motor da Fase 7."""

    snapshot = snapshot_mercado_from_leg_market_snapshot(
        leg,
        vwap=vwap,
        preco_anterior=preco_anterior,
        vwap_anterior=vwap_anterior,
        volume=volume,
        payoff_anterior=payoff_anterior,
        payoff_atual=payoff_atual,
        estrutura_favoravel=estrutura_favoravel,
    )

    return avaliar_snapshot(
        snapshot,
        parametros,
        timestamp=_timestamp_from(leg),
    )


def _field(source: Mapping[str, Any] | Any, name: str) -> Any:
    if isinstance(source, Mapping):
        return source.get(name)

    return getattr(source, name, None)


def _explicit_or_field(
    explicit: Any,
    source: Mapping[str, Any] | Any,
    field_name: str,
    *,
    fallback_field: str | None = None,
) -> Any:
    if explicit is not None:
        return explicit

    value = _field(source, field_name)
    if value is not None:
        return value

    if fallback_field is not None:
        return _field(source, fallback_field)

    return None


def _clean_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    lowered = text.lower()
    if lowered in {
        "none",
        "null",
        "nan",
        "#n/a",
        "#n/d",
        "#value!",
        "#valor!",
    }:
        return None

    return text


def _first_text(*values: Any) -> str | None:
    for value in values:
        text = _clean_text(value)
        if text:
            return text

    return None


def _to_float(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return float(value)

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return float(value)

    text = _clean_text(value)
    if text is None:
        return None

    text = text.replace("\u00a0", "")
    text = text.replace("R$", "")
    text = text.replace("%", "")
    text = text.strip()

    if "," in text and "." in text:
        text = text.replace(".", "")
        text = text.replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        number = float(text)
    except ValueError:
        return None

    if math.isnan(number) or math.isinf(number):
        return None

    return number


def _first_float(*values: Any) -> float | None:
    for value in values:
        number = _to_float(value)
        if number is not None:
            return number

    return None


def _to_bool(value: Any) -> bool:
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    text = _clean_text(value)
    if text is None:
        return False

    return text.lower() in {"1", "true", "t", "yes", "y", "sim", "s"}


def _timestamp_from(source: Mapping[str, Any] | Any) -> str | None:
    return _first_text(
        _field(source, "updated_at"),
        _field(source, "timestamp"),
        _field(source, "created_at"),
        _field(source, "captured_at"),
    )


__all__ = [
    "avaliar_leg_market_snapshot",
    "avaliar_rtd_option_quote",
    "snapshot_mercado_from_leg_market_snapshot",
    "snapshot_mercado_from_rtd_option_quote",
]
