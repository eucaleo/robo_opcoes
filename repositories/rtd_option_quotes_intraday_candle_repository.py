from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TABLE_NAME = "rtd_option_quotes_intraday_candles"


class RtdOptionQuotesIntradayCandleRepository:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                create table if not exists rtd_option_quotes_intraday_candles (
                    id integer primary key autoincrement,
                    interval_minutes integer not null,
                    bucket_start text not null,
                    symbol text not null,
                    open_price real,
                    high_price real,
                    low_price real,
                    close_price real,
                    vwap real,
                    bid real,
                    ask real,
                    spread real,
                    volume_delta real,
                    updates_count integer,
                    price_source text,
                    created_at text not null,
                    updated_at text not null,
                    unique(interval_minutes, bucket_start, symbol)
                )
                """
            )
            conn.execute(
                """
                create index if not exists idx_rtd_intraday_candles
                on rtd_option_quotes_intraday_candles(symbol, interval_minutes, bucket_start)
                """
            )

    def upsert_candle(self, candle: dict[str, Any]) -> None:
        self.upsert_many([candle])

    def upsert_many(self, candles: list[dict[str, Any]]) -> int:
        self.ensure_schema()
        now = datetime.now(timezone.utc).isoformat()
        rows = []
        for candle in candles:
            row = dict(candle)
            row.setdefault("created_at", now)
            row.setdefault("updated_at", now)
            rows.append(row)

        if not rows:
            return 0

        with self._connect() as conn:
            conn.executemany(
                """
                insert into rtd_option_quotes_intraday_candles (
                    interval_minutes, bucket_start, symbol,
                    open_price, high_price, low_price, close_price,
                    vwap, bid, ask, spread, volume_delta,
                    updates_count, price_source, created_at, updated_at
                ) values (
                    :interval_minutes, :bucket_start, :symbol,
                    :open_price, :high_price, :low_price, :close_price,
                    :vwap, :bid, :ask, :spread, :volume_delta,
                    :updates_count, :price_source, :created_at, :updated_at
                )
                on conflict(interval_minutes, bucket_start, symbol) do update set
                    open_price=excluded.open_price,
                    high_price=excluded.high_price,
                    low_price=excluded.low_price,
                    close_price=excluded.close_price,
                    vwap=excluded.vwap,
                    bid=excluded.bid,
                    ask=excluded.ask,
                    spread=excluded.spread,
                    volume_delta=excluded.volume_delta,
                    updates_count=excluded.updates_count,
                    price_source=excluded.price_source,
                    updated_at=excluded.updated_at
                """,
                rows,
            )
        return len(rows)

    def list_candles(
        self,
        symbol: str | None = None,
        interval_minutes: int | None = None,
    ) -> list[dict[str, Any]]:
        self.ensure_schema()
        query = "select * from rtd_option_quotes_intraday_candles"
        clauses = []
        params: list[Any] = []

        if symbol:
            clauses.append("symbol = ?")
            params.append(symbol)

        if interval_minutes:
            clauses.append("interval_minutes = ?")
            params.append(interval_minutes)

        if clauses:
            query += " where " + " and ".join(clauses)

        query += " order by symbol, interval_minutes, bucket_start"

        with self._connect() as conn:
            return [dict(row) for row in conn.execute(query, params).fetchall()]

    def schema_columns(self) -> list[str]:
        self.ensure_schema()
        with self._connect() as conn:
            columns = conn.execute(
                "pragma table_info(rtd_option_quotes_intraday_candles)"
            ).fetchall()
            return [str(col["name"]) for col in columns]

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
