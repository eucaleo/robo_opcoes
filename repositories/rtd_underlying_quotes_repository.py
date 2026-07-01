# repositories/rtd_underlying_quotes_repository.py

from __future__ import annotations

import math
import sqlite3
from pathlib import Path
from typing import Any, Sequence


def _q(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def _norm(name: str) -> str:
    return str(name or "").strip().lower()


def _first_col(cols: Sequence[str], candidates: Sequence[str]) -> str | None:
    lookup = {_norm(c): c for c in cols}
    for cand in candidates:
        if _norm(cand) in lookup:
            return lookup[_norm(cand)]
    return None


def _to_float(value: Any, default: float | None = None) -> float | None:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        if math.isfinite(float(value)):
            return float(value)
        return default

    text = str(value).strip()
    if not text:
        return default

    text = text.replace("R$", "").replace(" ", "")
    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        val = float(text)
        if math.isfinite(val):
            return val
    except Exception:
        pass

    return default


class RtdUnderlyingQuotesRepository:
    """
    Leitura da tabela rtd_underlying_quotes.

    A tabela rtd_underlying_quotes pertence ao banco operacional dados/app.db
    e funciona como cache vivo alimentado pelo fluxo RTD/Excel externo à UI.

    Este repository concentra a leitura defensiva do snapshot do ativo-base,
    evitando que componentes de interface consultem diretamente a tabela RTD.
    """

    TABLE = "rtd_underlying_quotes"

    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = Path(db_path)

    def _empty_market(self) -> dict[str, Any]:
        return {
            "current_price": None,
            "vwap": None,
            "bid": None,
            "ask": None,
            "close_price": None,
            "prev_close": None,
            "open_price": None,
            "high_price": None,
            "low_price": None,
            "volume": None,
            "change_percent": None,
            "updated_at": None,
            "series": [],
            "source_table": None,
            "vwap_source": None,
        }

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _table_cols(self, conn: sqlite3.Connection, table: str) -> list[str]:
        exists = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (table,),
        ).fetchone()
        if not exists:
            return []

        rows = conn.execute(f"PRAGMA table_info({_q(table)})").fetchall()
        return [row["name"] for row in rows]

    def get_latest_by_asset(self, asset: Any) -> dict[str, Any]:
        result = self._empty_market()

        asset = str(asset or "").strip().upper()
        if not asset or asset == "N/A":
            return result

        table = self.TABLE

        with self._connect() as conn:
            cols = self._table_cols(conn, table)
            if not cols:
                return result

            ativo_col = _first_col(
                cols,
                ["ativo", "underlying_asset", "asset", "ticker", "symbol"],
            )
            price_col = _first_col(
                cols,
                [
                    "ultimo_preco",
                    "current_price",
                    "preco_atual",
                    "price",
                    "last_price",
                    "last",
                ],
            )
            vwap_col = _first_col(cols, ["vwap", "vwap_price", "preco_medio"])
            bid_col = _first_col(cols, ["bid"])
            ask_col = _first_col(cols, ["ask"])
            close_col = _first_col(cols, ["close_price", "close", "fechamento"])
            prev_close_col = _first_col(
                cols,
                ["prev_close", "previous_close", "fechamento_anterior"],
            )
            open_col = _first_col(cols, ["open_price", "open", "abertura"])
            high_col = _first_col(cols, ["high_price", "high", "maxima"])
            low_col = _first_col(cols, ["low_price", "low", "minima"])
            volume_col = _first_col(cols, ["volume"])
            change_col = _first_col(
                cols,
                ["change_percent", "variation_percent", "variacao_percentual"],
            )
            ts_col = _first_col(
                cols,
                ["updated_at", "created_at", "timestamp", "datetime", "dt_ref"],
            )
            id_col = _first_col(cols, ["id"])

            if not ativo_col or not price_col:
                return result

            select_parts = [
                f"{_q(price_col)} AS current_price",
                f"{_q(vwap_col)} AS vwap" if vwap_col else "NULL AS vwap",
                f"{_q(bid_col)} AS bid" if bid_col else "NULL AS bid",
                f"{_q(ask_col)} AS ask" if ask_col else "NULL AS ask",
                f"{_q(close_col)} AS close_price" if close_col else "NULL AS close_price",
                f"{_q(prev_close_col)} AS prev_close" if prev_close_col else "NULL AS prev_close",
                f"{_q(open_col)} AS open_price" if open_col else "NULL AS open_price",
                f"{_q(high_col)} AS high_price" if high_col else "NULL AS high_price",
                f"{_q(low_col)} AS low_price" if low_col else "NULL AS low_price",
                f"{_q(volume_col)} AS volume" if volume_col else "NULL AS volume",
                f"{_q(change_col)} AS change_percent" if change_col else "NULL AS change_percent",
                f"{_q(ts_col)} AS updated_at" if ts_col else "NULL AS updated_at",
            ]

            order_parts = []
            if ts_col:
                order_parts.append(f"{_q(ts_col)} DESC")
            if id_col:
                order_parts.append(f"{_q(id_col)} DESC")

            order_sql = ""
            if order_parts:
                order_sql = " ORDER BY " + ", ".join(order_parts)

            sql = (
                f"SELECT {', '.join(select_parts)} "
                f"FROM {_q(table)} "
                f"WHERE UPPER(CAST({_q(ativo_col)} AS TEXT)) = UPPER(?)"
                f"{order_sql} "
                f"LIMIT 200"
            )

            rows = conn.execute(sql, (asset,)).fetchall()

        if not rows:
            return result

        first = dict(rows[0])

        result["current_price"] = first.get("current_price")
        result["vwap"] = first.get("vwap")
        result["bid"] = first.get("bid")
        result["ask"] = first.get("ask")
        result["close_price"] = first.get("close_price")
        result["prev_close"] = first.get("prev_close")
        result["open_price"] = first.get("open_price")
        result["high_price"] = first.get("high_price")
        result["low_price"] = first.get("low_price")
        result["volume"] = first.get("volume")
        result["change_percent"] = first.get("change_percent")
        result["updated_at"] = first.get("updated_at")
        result["source_table"] = table
        result["vwap_source"] = table if vwap_col else None

        series = []
        for idx, row in enumerate(reversed(rows)):
            r = dict(row)
            price = _to_float(r.get("current_price"))
            vwap = _to_float(r.get("vwap"))

            if price is not None or vwap is not None:
                series.append(
                    {
                        "x": idx + 1,
                        "price": price,
                        "vwap": vwap,
                    }
                )

        result["series"] = series

        return result
