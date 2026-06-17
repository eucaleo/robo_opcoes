# db/reader.py
"""
Reader para análise de dados derivados do SQLite.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from db.config import get_derived_db_path

from src.domain.refs.structure_ref import StructureRef


_STRUCTURE_DECISION_COLUMNS = [
    "timestamp",
    "decision",
    "dte_min",
    "pl_atual",
    "pl_max",
    "created_at",
    "pl_pct_of_max",
    "ratio",
    "pl_min",
    "spread_pct_medio",
    "why",
    "why_json",
]


class PayoffReader:
    """Leitor para análise de pontos do payoff curve e decisões estruturais."""

    def __init__(self, db_path: str | Path | None = None):
        self.db_path = (
            Path(db_path).expanduser().resolve()
            if db_path is not None
            else get_derived_db_path()
        )

    def _get_connection(self):
        """Retorna conexão com row factory configurada."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _get_table_columns(self, conn, table_name: str) -> List[str]:
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        return [row["name"] for row in cursor.fetchall()]

    def _resolve_ref_filter(
        self,
        conn: sqlite3.Connection,
        table_name: str,
        ref: StructureRef,
    ) -> Tuple[str, Any]:
        """
        Resolve coluna/valor para StructureRef respeitando o schema real.

        Preferência:
          - structure_id quando ref é canônico e a coluna existe;
          - aba como fallback legado quando necessário/disponível.
        """
        columns = set(self._get_table_columns(conn, table_name))
        column, value = ref.db_pair()

        if column in columns:
            return column, value

        if column == "structure_id" and "aba" in columns and ref.aba is not None:
            return "aba", ref.aba

        raise ValueError(
            f"Não foi possível consultar {table_name} com {ref!r}. "
            f"Coluna preferida={column!r}; colunas disponíveis={sorted(columns)!r}."
        )

    def _parse_json_maybe(self, value):
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                return None
        return None

    @staticmethod
    def _parse_timestamp(value: Any) -> datetime:
        if value is None:
            return datetime.min

        text = str(value).strip()
        if not text:
            return datetime.min

        normalized = text.replace("Z", "+00:00")

        try:
            dt = datetime.fromisoformat(normalized)
        except ValueError:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"):
                try:
                    dt = datetime.strptime(text, fmt)
                    break
                except ValueError:
                    continue
            else:
                return datetime.min

        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)

        return dt

    @classmethod
    def _timestamp_sort_key(cls, value: Any) -> Tuple[datetime, str]:
        return cls._parse_timestamp(value), "" if value is None else str(value)

    def _latest_timestamp(
        self,
        conn: sqlite3.Connection,
        table_name: str,
        column: str,
        value: Any,
    ) -> Optional[str]:
        rows = conn.execute(
            f"""
            SELECT DISTINCT timestamp
            FROM {table_name}
            WHERE {column} = ?
            """,
            (value,),
        ).fetchall()

        timestamps = [row["timestamp"] for row in rows]
        if not timestamps:
            return None

        return max(timestamps, key=self._timestamp_sort_key)

    def get_payoff_curve(
        self,
        ref: StructureRef,
        timestamp: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Retorna pontos do payoff curve como DataFrame.

        Args:
            ref: Referência canônica/legada da estrutura.
            timestamp: Timestamp específico. Se None, usa o mais recente por comparação em Python.

        Returns:
            DataFrame com colunas [spot, pl, timestamp, spot_ref, meta].
        """
        with self._get_connection() as conn:
            column, value = self._resolve_ref_filter(conn, "payoff_curve_points", ref)

            if timestamp is None:
                timestamp = self._latest_timestamp(
                    conn,
                    "payoff_curve_points",
                    column,
                    value,
                )
                if timestamp is None:
                    return pd.DataFrame(columns=["spot", "pl", "timestamp", "spot_ref", "meta"])

            query = f"""
                SELECT point_spot AS spot,
                       point_pl AS pl,
                       timestamp,
                       spot_ref,
                       meta_json
                FROM payoff_curve_points
                WHERE {column} = ? AND timestamp = ?
                ORDER BY point_spot
            """
            df = pd.read_sql_query(query, conn, params=(value, timestamp))

            if "meta_json" in df.columns:
                df["meta"] = df["meta_json"].apply(self._parse_json_maybe)
                df = df.drop("meta_json", axis=1)

            return df

    def get_decision_history(
        self,
        ref: StructureRef,
        days_back: int = 30,
    ) -> pd.DataFrame:
        """
        Retorna histórico de decisões como DataFrame.

        Args:
            ref: Referência canônica/legada da estrutura.
            days_back: Número de dias para retroceder.

        Returns:
            DataFrame com histórico de decisões.
        """
        cutoff_dt = datetime.now() - timedelta(days=days_back)

        with self._get_connection() as conn:
            column, value = self._resolve_ref_filter(conn, "structure_decisions", ref)
            columns = self._get_table_columns(conn, "structure_decisions")

            selected_cols = [
                col for col in _STRUCTURE_DECISION_COLUMNS
                if col in columns
            ]

            query = f"""
                SELECT {", ".join(selected_cols)}
                FROM structure_decisions
                WHERE {column} = ?
            """

            df = pd.read_sql_query(query, conn, params=(value,))

            if df.empty:
                return df

            if "timestamp" in df.columns:
                df["_ts_sort"] = df["timestamp"].apply(self._parse_timestamp)
                df = df[df["_ts_sort"] >= cutoff_dt]
                df = df.sort_values("_ts_sort", ascending=False)
                df = df.drop("_ts_sort", axis=1)
                df = df.reset_index(drop=True)

            if "pl_pct_of_max" not in df.columns and "ratio" in df.columns:
                df["pl_pct_of_max"] = df["ratio"]

            why_series = None

            if "why" in df.columns:
                why_series = df["why"].apply(self._parse_json_maybe)

            if "why_json" in df.columns:
                why_json_series = df["why_json"].apply(self._parse_json_maybe)
                if why_series is None:
                    why_series = why_json_series
                else:
                    why_series = why_series.where(why_series.notna(), why_json_series)

            if why_series is not None:
                df["why"] = why_series

            if "why_json" in df.columns:
                df = df.drop("why_json", axis=1)

            return df
