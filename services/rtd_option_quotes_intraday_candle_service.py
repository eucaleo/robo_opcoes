from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from repositories.rtd_option_quotes_intraday_candle_repository import (
    RtdOptionQuotesIntradayCandleRepository,
)


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
        path = Path(db_path)
        if not path.exists():
            return []

        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        try:
            table = conn.execute(
                """
                select name
                from sqlite_master
                where type = 'table'
                  and name = 'rtd_option_quotes_intraday_history'
                """
            ).fetchone()

            if not table:
                return []

            cols = [
                str(col["name"])
                for col in conn.execute(
                    "pragma table_info(rtd_option_quotes_intraday_history)"
                ).fetchall()
            ]

            query = "select * from rtd_option_quotes_intraday_history"
            params: list[Any] = []

            if symbol:
                if "symbol" in cols:
                    query += " where symbol = ?"
                    params.append(symbol)
                elif "codigo_opcao" in cols:
                    query += " where codigo_opcao = ?"
                    params.append(symbol)

            if "captured_at" in cols:
                query += " order by captured_at"
            elif "timestamp" in cols:
                query += " order by timestamp"

            return [dict(row) for row in conn.execute(query, params).fetchall()]
        finally:
            conn.close()

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
