from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from repositories.rtd_option_quotes_intraday_candle_repository import (
    RtdOptionQuotesIntradayCandleRepository,
)
from repositories.rtd_option_quotes_intraday_history_repository import fetch_intraday_history_rows_for_candles


EXCHANGE_TIMEZONE = timezone(timedelta(hours=-3), "America/Sao_Paulo")


class RtdOptionQuotesIntradayCandleService:
    def aggregate_points(
        self,
        points: list[dict[str, Any]],
        interval_minutes: int = 1,
    ) -> list[dict[str, Any]]:
        self._validate_interval(interval_minutes)

        grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}

        for point in points:
            symbol = self._extract_symbol(point)
            captured_at = self._extract_time(point)

            if not symbol or not captured_at:
                continue

            bucket_start = self._bucket_start(captured_at, interval_minutes)
            grouped.setdefault((symbol, bucket_start), []).append(point)

        candles: list[dict[str, Any]] = []

        for (symbol, bucket_start), bucket_points in grouped.items():
            ordered = sorted(
                bucket_points,
                key=lambda point: (
                    self._extract_time(point)
                    or datetime.min.replace(tzinfo=EXCHANGE_TIMEZONE)
                ),
            )

            prices: list[tuple[float, str]] = []
            for point in ordered:
                price, source = self._get_price(point)
                if price is not None:
                    prices.append((price, source))

            if not prices:
                continue

            bid = self._last_number(ordered, ["bid"])
            ask = self._last_number(ordered, ["ask"])
            spread = None
            if bid is not None and ask is not None:
                spread = ask - bid

            candle = {
                "interval_minutes": interval_minutes,
                "bucket_start": bucket_start,
                "symbol": symbol,
                "open_price": prices[0][0],
                "high_price": max(price for price, _source in prices),
                "low_price": min(price for price, _source in prices),
                "close_price": prices[-1][0],
                "vwap": self._last_number(ordered, ["vwap"]),
                "bid": bid,
                "ask": ask,
                "spread": spread,
                "volume_delta": self._volume_delta(ordered),
                "updates_count": len(ordered),
                "price_source": prices[-1][1],
            }
            candles.append(candle)

        return sorted(
            candles,
            key=lambda candle: (
                candle["symbol"],
                candle["interval_minutes"],
                candle["bucket_start"],
            ),
        )

    def build_candles_from_history(
        self,
        db_path: str | Path,
        symbol: str | None = None,
        interval_minutes: int = 1,
    ) -> list[dict[str, Any]]:
        points = self.load_history_points(db_path, symbol)
        return self.aggregate_points(points, interval_minutes)

    def persist_candles(
        self,
        db_path: str | Path,
        candles: list[dict[str, Any]],
    ) -> int:
        repository = RtdOptionQuotesIntradayCandleRepository(db_path)
        return repository.upsert_many(candles)

    def load_history_points(
        self,
        db_path: str | Path,
        symbol: str | None = None,
    ) -> list[dict[str, Any]]:
        """Load intraday history rows through repository boundary (Frente 68)."""
        params = dict(locals())
        self_obj = params.get("self")
        if "db_path" not in params and "path" not in params and self_obj is not None:
            inferred_db_path = getattr(self_obj, "db_path", None)
            if inferred_db_path is not None:
                params["db_path"] = inferred_db_path
        return fetch_intraday_history_rows_for_candles(**params)

    def _validate_interval(self, interval_minutes: int) -> None:
        if interval_minutes not in {1, 5, 15}:
            raise ValueError("Intervalo invalido. Use 1, 5 ou 15 minutos.")

    def _extract_symbol(self, point: dict[str, Any]) -> str | None:
        for key in ["symbol", "codigo_opcao"]:
            value = point.get(key)
            if value:
                return str(value).strip()
        return None

    def _extract_time(self, point: dict[str, Any]) -> datetime | None:
        for key in ["captured_at", "timestamp", "snapshot_at", "updated_at"]:
            parsed = self._parse_time(point.get(key))
            if parsed:
                return parsed
        return None

    def _parse_time(self, value: Any) -> datetime | None:
        if not value:
            return None

        if isinstance(value, datetime):
            return self._normalize_to_exchange_time(value)

        text = str(value).strip()

        if text.endswith("Z"):
            text = text[:-1] + "+00:00"

        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None

        return self._normalize_to_exchange_time(parsed)

    def _normalize_to_exchange_time(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=EXCHANGE_TIMEZONE)

        return value.astimezone(EXCHANGE_TIMEZONE)

    def _bucket_start(self, captured_at: datetime, interval_minutes: int) -> str:
        captured_at = self._normalize_to_exchange_time(captured_at)
        minute = (captured_at.minute // interval_minutes) * interval_minutes
        start = captured_at.replace(minute=minute, second=0, microsecond=0)
        return start.replace(tzinfo=None).isoformat(timespec="seconds")

    def _get_price(self, point: dict[str, Any]) -> tuple[float | None, str]:
        last_price = self._number_from_keys(
            point,
            ["last", "ultimo_preco", "last_price", "preco", "price"],
        )

        if last_price is not None and last_price > 0:
            return last_price, "last_trade"

        bid = self._number_from_keys(point, ["bid"])
        ask = self._number_from_keys(point, ["ask"])

        if bid is not None and ask is not None and bid > 0 and ask > 0:
            return (bid + ask) / 2, "mid_price"

        return None, "unavailable"

    def _last_number(
        self,
        points: list[dict[str, Any]],
        keys: list[str],
    ) -> float | None:
        for point in reversed(points):
            value = self._number_from_keys(point, keys)
            if value is not None:
                return value
        return None

    def _number_from_keys(
        self,
        point: dict[str, Any],
        keys: list[str],
    ) -> float | None:
        for key in keys:
            value = self._to_float(point.get(key))
            if value is not None:
                return value
        return None

    def _to_float(self, value: Any) -> float | None:
        if value is None or isinstance(value, bool):
            return None

        try:
            return float(str(value).replace(",", "."))
        except ValueError:
            return None

    def _volume_delta(self, points: list[dict[str, Any]]) -> float | None:
        volumes = [
            self._number_from_keys(point, ["volume"])
            for point in points
        ]
        valid = [volume for volume in volumes if volume is not None]

        if len(valid) < 2:
            return None

        delta = max(valid) - min(valid)
        if delta < 0:
            return None

        return delta

# === INICIO FRENTE 36 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT ===
# Frente 36:
# Ponte contratual local para parsers canonicos compartilhados no candle service
# de rtd_option_quotes.
#
# Esta frente apenas registra helpers defensivos para consumo futuro de:
# - utils/number_parser.py
# - utils/date_parser.py
#
# Limites preservados:
# - sem troca de persistencia;
# - sem troca de schema;
# - sem alteracao operacional abrupta do candle service;
# - option_type canonico permanece somente CALL/PUT por extenso;
# - C/V sao compra/venda legado.

try:
    from utils import number_parser as _frente36_number_parser
except Exception:
    _frente36_number_parser = None

try:
    from utils import date_parser as _frente36_date_parser
except Exception:
    _frente36_date_parser = None


def _frente36_call_parser(module, names, value, default=None):
    """Chama parser canonico quando disponivel, preservando fallback local."""
    for name in names:
        parser = getattr(module, name, None) if module is not None else None
        if callable(parser):
            try:
                parsed = parser(value)
            except Exception:
                continue
            if parsed is not None:
                return parsed
    return default


def _frente36_parse_optional_float(value, default=None):
    """Parser numerico contratual para floats opcionais."""
    return _frente36_call_parser(
        _frente36_number_parser,
        (
            "parse_optional_float",
            "parse_float_br",
            "to_optional_float",
            "to_float",
        ),
        value,
        default,
    )


def _frente36_parse_positive_float(value, default=None):
    """Parser numerico contratual para floats positivos."""
    return _frente36_call_parser(
        _frente36_number_parser,
        (
            "parse_positive_float",
            "parse_optional_positive_float",
            "parse_optional_float",
            "parse_float_br",
        ),
        value,
        default,
    )


def _frente36_parse_percent(value, default=None):
    """Parser contratual para percentuais quando disponivel."""
    return _frente36_call_parser(
        _frente36_number_parser,
        (
            "parse_percent",
            "parse_optional_percent",
            "parse_optional_float",
            "parse_float_br",
        ),
        value,
        default,
    )


def _frente36_parse_datetime_to_iso(value, default=None):
    """Parser contratual para datas/datetimes em formato ISO."""
    return _frente36_call_parser(
        _frente36_date_parser,
        (
            "parse_datetime_to_iso",
            "parse_excel_date_to_iso",
            "parse_date_to_iso",
            "to_iso_datetime",
            "to_iso_date",
        ),
        value,
        default,
    )


def _frente36_normalize_symbol(value):
    """Normalizacao contratual minima de simbolo para candles."""
    if value is None:
        return None
    text = str(value).strip().upper()
    return text or None


def _frente36_parser_bridge_contract():
    """Contrato local da Frente 36, sem mudanca operacional nesta etapa."""
    return {
        "target": "services/rtd_option_quotes_intraday_candle_service.py",
        "number_parser": "utils/number_parser.py",
        "date_parser": "utils/date_parser.py",
        "persistence_changed": False,
        "schema_changed": False,
        "operational_flow_changed": False,
        "option_type_contract": "CALL/PUT por extenso; C/V sao compra/venda legado",
    }
# === FIM FRENTE 36 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT ===

# INICIO FRENTE 41 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT
# Frente 41:
# Ponte local e defensiva para o Candle Service preferir os parsers canonicos
# utils/number_parser.py e utils/date_parser.py quando disponiveis.
# Objetivo: reduzir normalizacao numerica/data duplicada no eixo intraday/candles.
# Sem troca de persistencia.
# Sem troca de schema.
# Sem alteracao operacional ampla.
# Nenhuma operacao de versionamento executada.

try:
    from utils import number_parser as _frente41_number_parser
except Exception:  # pragma: no cover - ponte defensiva para compatibilidade local
    _frente41_number_parser = None

try:
    from utils import date_parser as _frente41_date_parser
except Exception:  # pragma: no cover - ponte defensiva para compatibilidade local
    _frente41_date_parser = None


def _frente41_parse_float_value(value, default=None):
    """Parse numerico local preferindo utils.number_parser, com fallback BR seguro."""
    if value is None:
        return default

    parser = _frente41_number_parser

    if parser is not None:
        for name in ("parse_optional_float", "parse_float_br", "parse_float"):
            func = getattr(parser, name, None)
            if callable(func):
                try:
                    parsed = func(value)
                    return default if parsed is None else parsed
                except Exception:
                    pass

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return default

    text = text.replace("%", "").strip()

    try:
        if "," in text and "." in text:
            text = text.replace(".", "").replace(",", ".")
        elif "," in text:
            text = text.replace(",", ".")
        return float(text)
    except Exception:
        return default


def _frente41_parse_positive_float_value(value, default=None):
    """Parse numerico positivo para campos como bid, ask, last, volume e VWAP."""
    parsed = _frente41_parse_float_value(value, default=default)
    if parsed is None:
        return default
    try:
        parsed_float = float(parsed)
    except Exception:
        return default
    if parsed_float < 0:
        return default
    return parsed_float


def _frente41_parse_datetime_value(value, default=None):
    """Parse defensivo de data/hora preferindo utils.date_parser."""
    if value is None:
        return default

    parser = _frente41_date_parser

    if parser is not None:
        for name in ("parse_datetime_to_iso", "parse_excel_date_to_iso", "parse_date_to_iso"):
            func = getattr(parser, name, None)
            if callable(func):
                try:
                    parsed = func(value)
                    return default if parsed is None else parsed
                except Exception:
                    pass

    try:
        if hasattr(value, "isoformat"):
            return value.isoformat()
    except Exception:
        pass

    text = str(value).strip()
    return text or default


def _frente41_normalize_symbol(value):
    """Normaliza simbolo intraday/candle sem alterar persistencia ou schema."""
    if value is None:
        return ""
    return str(value).strip().upper()


# Compatibilidade: se o service usa _to_float como helper global, a definicao final
# passa a preferir a ponte canonica sem exigir refatoracao ampla do arquivo.
def _to_float(value, default=None):
    return _frente41_parse_float_value(value, default=default)


# FIM FRENTE 41 RTD OPTION QUOTES INTRADAY CANDLE SERVICE PARSER BRIDGE CONTRACT
