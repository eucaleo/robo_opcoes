# db/reader.py
"""
Reader para análise de dados consolidados do SQLite.
"""
from domain.refs.structure_ref import StructureRef
import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class PayoffReader:
    """Leitor para análise de pontos do payoff curve e decisões estruturais."""

    def __init__(self, db_path: str = "dados/app.db"):
        self.db_path = Path(db_path)

    def _get_connection(self):
        """Retorna conexão com row factory configurada."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _get_table_columns(self, conn, table_name: str) -> List[str]:
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        return [row["name"] for row in cursor.fetchall()]

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

    def get_payoff_curve(self, ref: StructureRef, timestamp: Optional[str] = None) -> pd.DataFrame:
        """
        Retorna pontos do payoff curve como DataFrame.

        Args:
            aba: Nome da aba/estratégia
            timestamp: Timestamp específico (None = mais recente)

        Returns:
            DataFrame com colunas [spot, pl, timestamp, spot_ref]
        """
        with self._get_connection() as conn:
            if timestamp:
                query = """
                    SELECT point_spot as spot, point_pl as pl,
                           timestamp, spot_ref, meta_json
                    FROM payoff_curve_points
                    WHERE {ref.db_column()} = ? AND timestamp = ?
                    ORDER BY point_spot
                """
                params = (aba, timestamp)
            else:
                query = """
                    SELECT point_spot as spot, point_pl as pl,
                           timestamp, spot_ref, meta_json
                    FROM payoff_curve_points
                    WHERE {ref.db_column()} = ? AND timestamp = (
                        SELECT MAX(timestamp) FROM payoff_curve_points WHERE {ref.db_column()} = ?
                    )
                    ORDER BY point_spot
                """
                params = (aba, aba)

            df = pd.read_sql_query(query, conn, params=params)

            if "meta_json" in df.columns:
                df["meta"] = df["meta_json"].apply(
                    lambda x: json.loads(x) if x else None
                )
                df = df.drop("meta_json", axis=1)

            return df

    def get_decision_history(self, ref: StructureRef, days_back: int = 30) -> pd.DataFrame:
        """
        Retorna histórico de decisões como DataFrame.

        Args:
            aba: Nome da aba/estratégia
            days_back: Número de dias para retroceder

        Returns:
            DataFrame com histórico de decisões
        """
        cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()

        with self._get_connection() as conn:
            columns = self._get_table_columns(conn, "structure_decisions")

            selected_cols = [
                "timestamp",
                "decision",
                "dte_min",
                "pl_atual",
                "pl_max",
                "created_at",
            ]

            if "pl_pct_of_max" in columns:
                selected_cols.append("pl_pct_of_max")

            if "ratio" in columns and "pl_pct_of_max" not in columns:
                selected_cols.append("ratio")

            if "pl_min" in columns:
                selected_cols.append("pl_min")

            if "spread_pct_medio" in columns:
                selected_cols.append("spread_pct_medio")

            if "why" in columns:
                selected_cols.append("why")
            if "why_json" in columns:
                selected_cols.append("why_json")

            query = f"""
                SELECT {", ".join(selected_cols)}
                FROM structure_decisions
                WHERE {ref.db_column()} = ? AND timestamp >= ?
                ORDER BY timestamp DESC
            """

            df = pd.read_sql_query(query, conn, params=(aba, cutoff_date))

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
