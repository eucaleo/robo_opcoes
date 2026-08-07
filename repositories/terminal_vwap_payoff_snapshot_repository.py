from __future__ import annotations

"""
Boundary/repositório de snapshots para o Terminal VWAP Payoff.

Criado na Frente 55b para retirar acesso direto a sqlite/queries da camada de UI.

Este módulo concentra leitura defensiva de dados persistidos. Não altera schema,
não executa migrações e não acessa Web/API/HTTP.
"""

import math
import sqlite3
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    from db import derived_repo
except Exception:
    derived_repo = None


def _q(name: str) -> str:
    return '"' + str(name).replace('"', '""') + '"'


def _norm(name: str) -> str:
    return str(name or "").strip().lower()


def _first_col(cols: Sequence[str], candidates: Sequence[str]) -> Optional[str]:
    lookup = {_norm(c): c for c in cols}
    for cand in candidates:
        if _norm(cand) in lookup:
            return lookup[_norm(cand)]
    return None


def _to_float(value: Any, default: Optional[float] = None) -> Optional[float]:
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


class TerminalVWAPPayoffSnapshotRepository:
    """Leitor persistido para snapshots operacionais do terminal."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)

    def _connect(self) -> Any:
            db = Path(self.db_path)
            if not db.exists():
                raise FileNotFoundError(f"Banco app.db não encontrado em: {db}")
            conn = sqlite3.connect(str(db))
            conn.row_factory = sqlite3.Row
            return conn

    def _tables_cols(self, conn: Any) -> Dict[str, List[str]]:
            rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            result: Dict[str, List[str]] = {}
            for row in rows:
                table = row["name"]
                try:
                    cols = conn.execute(f"PRAGMA table_info({_q(table)})").fetchall()
                    result[table] = [c["name"] for c in cols]
                except Exception:
                    pass
            return result

    def _find_structures_table(self, schema: Dict[str, List[str]]) -> Optional[str]:
            preferred = [
                "structures",
                "structure",
                "option_structures",
                "estruturas",
            ]
            for table in preferred:
                if table in schema:
                    return table

            for table, cols in schema.items():
                id_col = _first_col(cols, ["id", "structure_id"])
                name_col = _first_col(cols, ["name", "nome", "structure_name"])
                asset_col = _first_col(cols, ["underlying_asset", "ativo", "asset", "underlying"])
                if id_col and (name_col or asset_col):
                    return table

            return None

    def _load_structures(self) -> List[Dict[str, Any]]:
            conn = self._connect()
            try:
                schema = self._tables_cols(conn)
                table = self._find_structures_table(schema)
                if not table:
                    return []

                cols = schema[table]
                id_col = _first_col(cols, ["id", "structure_id"])
                name_col = _first_col(cols, ["name", "nome", "structure_name"])
                asset_col = _first_col(cols, ["underlying_asset", "ativo", "asset", "underlying"])
                status_col = _first_col(cols, ["status", "state", "situacao"])

                if not id_col:
                    return []

                select_parts = [
                    f"{_q(id_col)} AS id",
                    f"{_q(name_col)} AS name" if name_col else "NULL AS name",
                    f"{_q(asset_col)} AS underlying_asset" if asset_col else "NULL AS underlying_asset",
                    f"{_q(status_col)} AS status" if status_col else "NULL AS status",
                ]

                sql = f"SELECT {', '.join(select_parts)} FROM {_q(table)} ORDER BY {_q(id_col)}"
                rows = conn.execute(sql).fetchall()

                structures: List[Dict[str, Any]] = []
                for row in rows:
                    item = dict(row)
                    item["id"] = item.get("id")
                    item["name"] = item.get("name") or f"Estrutura {item.get('id')}"
                    item["underlying_asset"] = item.get("underlying_asset") or "N/A"
                    item["status"] = item.get("status") or "N/A"
                    structures.append(item)

                return structures
            finally:
                conn.close()

    def _fetch_legs_rows(
            self,
            conn: Any,
            table: str,
            sid_col: str,
            select_parts: List[str],
            structure_id: Any,
        ) -> List[Any]:
            sql = (
                f"SELECT {', '.join(select_parts)} "
                f"FROM {_q(table)} "
                f"WHERE {_q(sid_col)} = ?"
            )
            return conn.execute(sql, (structure_id,)).fetchall()

    def _load_market(self, asset: Any) -> Dict[str, Any]:
            result = self._empty_market_result()
            asset = self._normalize_market_asset(asset)

            if not asset:
                return result

            conn = self._connect()
            try:
                query = self._build_market_query(conn)
                if not query:
                    return result

                rows = conn.execute(query["sql"], (asset,)).fetchall()
                return self._market_result_from_rows(result, rows, query)

            finally:
                conn.close()

    def _empty_market_result(self) -> Dict[str, Any]:
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

    def _normalize_market_asset(self, asset: Any) -> str:
            asset = str(asset or "").strip().upper()
            if not asset or asset == "N/A":
                return ""
            return asset

    def _build_market_query(self, conn: Any) -> Dict[str, Any]:
            table = "rtd_underlying_quotes"
            schema = self._tables_cols(conn)
            if table not in schema:
                return {}

            colmap = self._market_column_map(schema[table])
            if not colmap.get("asset") or not colmap.get("current_price"):
                return {}

            select_parts = self._market_select_parts(colmap)
            order_sql = self._market_order_sql(colmap)

            sql = (
                f"SELECT {', '.join(select_parts)} "
                f"FROM {_q(table)} "
                f"WHERE UPPER(CAST({_q(colmap['asset'])} AS TEXT)) = UPPER(?)"
                f"{order_sql} "
                f"LIMIT 200"
            )

            return {
                "sql": sql,
                "table": table,
                "has_vwap": bool(colmap.get("vwap")),
            }

    def _market_column_map(self, cols: Sequence[str]) -> Dict[str, Any]:
            return {
                "asset": _first_col(
                    cols,
                    ["ativo", "underlying_asset", "asset", "ticker", "symbol"],
                ),
                "current_price": _first_col(
                    cols,
                    ["ultimo_preco", "current_price", "preco_atual", "price", "last_price", "last"],
                ),
                "vwap": _first_col(cols, ["vwap", "vwap_price", "preco_medio"]),
                "bid": _first_col(cols, ["bid"]),
                "ask": _first_col(cols, ["ask"]),
                "close_price": _first_col(cols, ["close_price", "close", "fechamento"]),
                "prev_close": _first_col(
                    cols,
                    ["prev_close", "previous_close", "fechamento_anterior"],
                ),
                "open_price": _first_col(cols, ["open_price", "open", "abertura"]),
                "high_price": _first_col(cols, ["high_price", "high", "maxima"]),
                "low_price": _first_col(cols, ["low_price", "low", "minima"]),
                "volume": _first_col(cols, ["volume"]),
                "change_percent": _first_col(
                    cols,
                    ["change_percent", "variation_percent", "variacao_percentual"],
                ),
                "updated_at": _first_col(
                    cols,
                    ["updated_at", "created_at", "timestamp", "datetime", "dt_ref"],
                ),
                "id": _first_col(cols, ["id"]),
            }

    def _market_select_parts(self, colmap: Dict[str, Any]) -> List[str]:
            specs = [
                ("current_price", "current_price"),
                ("vwap", "vwap"),
                ("bid", "bid"),
                ("ask", "ask"),
                ("close_price", "close_price"),
                ("prev_close", "prev_close"),
                ("open_price", "open_price"),
                ("high_price", "high_price"),
                ("low_price", "low_price"),
                ("volume", "volume"),
                ("change_percent", "change_percent"),
                ("updated_at", "updated_at"),
            ]

            parts = []
            for key, alias in specs:
                col = colmap.get(key)
                parts.append(f"{_q(col)} AS {alias}" if col else f"NULL AS {alias}")
            return parts

    def _market_order_sql(self, colmap: Dict[str, Any]) -> str:
            order_parts = []

            if colmap.get("updated_at"):
                order_parts.append(f"{_q(colmap['updated_at'])} DESC")
            if colmap.get("id"):
                order_parts.append(f"{_q(colmap['id'])} DESC")

            if not order_parts:
                return ""

            return " ORDER BY " + ", ".join(order_parts)

    def _market_result_from_rows(
            self,
            result: Dict[str, Any],
            rows: Any,
            query: Dict[str, Any],
        ) -> Dict[str, Any]:
            if not rows:
                return result

            first = dict(rows[0])
            market_fields = [
                "current_price",
                "vwap",
                "bid",
                "ask",
                "close_price",
                "prev_close",
                "open_price",
                "high_price",
                "low_price",
                "volume",
                "change_percent",
                "updated_at",
            ]

            for field in market_fields:
                result[field] = first.get(field)

            result["source_table"] = query["table"]
            result["vwap_source"] = query["table"] if query.get("has_vwap") else None
            result["series"] = self._market_series_from_rows(rows)
            return result

    def _market_series_from_rows(self, rows: Any) -> List[Dict[str, Any]]:
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

            return series

    def _render_legs(self, legs: List[Dict[str, Any]]) -> None:
            for item in self.legs_table.get_children():
                self.legs_table.delete(item)

            for idx, leg in enumerate(legs, 1):
                self.legs_table.insert(
                    "",
                    "end",
                    values=(
                        idx,
                        leg.get("symbol") or "--",
                        leg.get("position_side") or "--",
                        leg.get("option_type") or "--",
                        _number(leg.get("strike")),
                        leg.get("expiration_date") or "--",
                        _number(leg.get("quantity")),
                        _money(leg.get("premium")),
                        _money(
                            leg.get("current_price")
                            if leg.get("current_price") is not None
                            else leg.get("ultimo_preco")
                            if leg.get("ultimo_preco") is not None
                            else leg.get("last_price")
                            if leg.get("last_price") is not None
                            else leg.get("price")
                        ),
                    ),
                )

    def _set_alerts(self, alerts: List[str]) -> None:
            self.alerts_box.configure(state="normal")
            self.alerts_box.delete("1.0", "end")
            for alert in alerts:
                self.alerts_box.insert("end", "- " + alert + "\n")
            self.alerts_box.configure(state="disabled")
