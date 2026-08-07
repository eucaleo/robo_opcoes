from __future__ import annotations

from pathlib import Path
from typing import Any

from repositories.rtd_option_quotes_intraday_candle_repository import (
    RtdOptionQuotesIntradayCandleRepository,
)


SOURCE_TABLE = "rtd_option_quotes_intraday_candles"


class RtdOptionQuotesIntradayCandleChartService:
    """
    Adapta candles intraday persistidos para o formato consumido pelos gráficos da UI.

    A camada de UI não precisa conhecer o schema físico da tabela de candles.
    Ela recebe uma série normalizada contendo timestamp, preço, VWAP e OHLC.
    """

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.repository = RtdOptionQuotesIntradayCandleRepository(self.db_path)

    def get_chart_series(
        self,
        symbol: str | None = None,
        interval_minutes: int = 1,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        candles = self.repository.list_candles(
            symbol=symbol,
            interval_minutes=interval_minutes,
        )

        if limit is not None and limit > 0:
            candles = candles[-limit:]

        series: list[dict[str, Any]] = []
        for candle in candles:
            item = self._candle_to_chart_point(candle)
            if item is not None:
                series.append(item)

        return series

    def get_vwap_price_series(
        self,
        symbol: str | None = None,
        interval_minutes: int = 1,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Retorna a série no contrato já esperado por TerminalVWAPPayoffDarkPanel:

            {
                "timestamp": "...",
                "price": close_price,
                "vwap": vwap,
                ...
            }
        """
        return self.get_chart_series(
            symbol=symbol,
            interval_minutes=interval_minutes,
            limit=limit,
        )

    def _candle_to_chart_point(self, candle: dict[str, Any]) -> dict[str, Any] | None:
        price = self._first_number(
            candle,
            [
                "close_price",
                "open_price",
                "vwap",
            ],
        )

        bid = self._to_float(candle.get("bid"))
        ask = self._to_float(candle.get("ask"))

        if price is None and bid is not None and ask is not None:
            price = (bid + ask) / 2

        vwap = self._to_float(candle.get("vwap"))

        if price is None and vwap is None:
            return None

        bucket_start = candle.get("bucket_start")

        return {
            "timestamp": bucket_start,
            "bucket_start": bucket_start,
            "symbol": candle.get("symbol"),
            "interval_minutes": candle.get("interval_minutes"),
            "price": price,
            "vwap": vwap,
            "open": self._to_float(candle.get("open_price")),
            "high": self._to_float(candle.get("high_price")),
            "low": self._to_float(candle.get("low_price")),
            "close": self._to_float(candle.get("close_price")),
            "bid": bid,
            "ask": ask,
            "spread": self._to_float(candle.get("spread")),
            "volume_delta": self._to_float(candle.get("volume_delta")),
            "updates_count": candle.get("updates_count"),
            "price_source": candle.get("price_source"),
            "source_table": SOURCE_TABLE,
        }

    def _first_number(
        self,
        row: dict[str, Any],
        keys: list[str],
    ) -> float | None:
        for key in keys:
            value = self._to_float(row.get(key))
            if value is not None:
                return value
        return None

    def _to_float(self, value: Any) -> float | None:
        if value is None:
            return None

        if isinstance(value, bool):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        text = str(value).strip()
        if not text:
            return None

        text = text.replace("R$", "").replace(" ", "")

        if "," in text and "." in text:
            text = text.replace(".", "").replace(",", ".")
        elif "," in text:
            text = text.replace(",", ".")

        try:
            return float(text)
        except Exception:
            return None

# INICIO FRENTE 37 RTD OPTION QUOTES INTRADAY CANDLE CHART PARSER BRIDGE CONTRACT
# Sem troca de persistencia.
# Sem troca de schema.
# Sem alteracao operacional abrupta do candle chart service.
# Ponte contratual local para parsers canonicos compartilhados.
# Esta frente registra o contrato de normalizacao para o chart de candles RTD,
# sem alterar fluxo operacional, sem trocar persistencia e sem trocar schema.

try:
    from utils import number_parser as _frente37_number_parser
except Exception:  # pragma: no cover - fallback defensivo de compatibilidade local
    _frente37_number_parser = None

try:
    from utils import date_parser as _frente37_date_parser
except Exception:  # pragma: no cover - fallback defensivo de compatibilidade local
    _frente37_date_parser = None


def _frente37_parse_optional_float(value):
    """Ponte contratual para parse numerico opcional canonico."""
    parser = getattr(_frente37_number_parser, "parse_optional_float", None)
    if callable(parser):
        return parser(value)
    parser = getattr(_frente37_number_parser, "parse_float_br", None)
    if callable(parser):
        return parser(value)
    return value


def _frente37_parse_positive_float(value):
    """Ponte contratual para parse numerico positivo canonico."""
    parser = getattr(_frente37_number_parser, "parse_positive_float", None)
    if callable(parser):
        return parser(value)
    return _frente37_parse_optional_float(value)


def _frente37_parse_datetime_to_iso(value):
    """Ponte contratual para parse canonico de data/hora."""
    parser = getattr(_frente37_date_parser, "parse_datetime_to_iso", None)
    if callable(parser):
        return parser(value)
    parser = getattr(_frente37_date_parser, "parse_excel_date_to_iso", None)
    if callable(parser):
        return parser(value)
    return value
# FIM FRENTE 37 RTD OPTION QUOTES INTRADAY CANDLE CHART PARSER BRIDGE CONTRACT
