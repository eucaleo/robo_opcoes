# db/writer.py
"""
Writer para persistência de dados derivados no SQLite.
"""
from __future__ import annotations

import json
import sqlite3
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.domain.refs.structure_ref import StructureRef
from db.config import ensure_parent_dir, get_derived_db_path


_STRUCTURE_DECISION_COLUMNS = [
    "id",
    "timestamp",
    "aba",
    "structure_id",
    "decision",
    "level",
    "ratio",
    "pl_pct_of_max",
    "dte_min",
    "pl_atual",
    "pl_max",
    "pl_min",
    "spread_pct_medio",
    "why",
    "why_json",
    "spot_ref",
    "meta_json",
    "created_at",
]

_PAYOFF_HISTORY_COLUMNS = [
    "id",
    "timestamp",
    "spot_ref",
    "point_spot",
    "point_pl",
    "meta_json",
]


class PayoffWriter:
    """Escritor para pontos do payoff curve e decisões estruturais."""

    def __init__(self, db_path: str | Path | None = None):
        resolved_path = (
            Path(db_path).expanduser().resolve()
            if db_path is not None
            else get_derived_db_path()
        )
        self.db_path = ensure_parent_dir(resolved_path)
        self._init_db()

    def _init_db(self):
        """Inicializa o banco com o schema."""
        from .schema import SCHEMA_SQL

        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA_SQL)

    def _get_table_columns(
        self,
        conn: sqlite3.Connection,
        table_name: str,
    ) -> List[str]:
        rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        return [row[1] for row in rows]

    def _resolve_ref_filter(
        self,
        conn: sqlite3.Connection,
        table_name: str,
        ref: StructureRef,
    ) -> Tuple[str, Any]:
        """
        Resolve coluna/valor para StructureRef respeitando o schema real.
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

    def save_payoff_points(
        self,
        timestamp: str,
        ref: StructureRef,
        points: List[Dict[str, Any]],
        spot_ref: Optional[float] = None,
        meta: Optional[Dict] = None,
    ) -> int:
        """
        Salva pontos do payoff curve.

        Args:
            timestamp: Timestamp da captura.
            ref: Referência canônica/legada da estrutura.
            points: Lista de pontos [(spot, pl), ...] ou dicts.
            spot_ref: Spot de referência.
            meta: Metadados adicionais.

        Returns:
            Número de pontos inseridos.
        """
        if not points:
            return 0

        if not ref.aba:
            raise ValueError(
                "PayoffWriter.save_payoff_points exige ref.aba, "
                "pois payoff_curve_points.aba é coluna obrigatória de compatibilidade."
            )

        meta = dict(meta) if meta else {}
        if spot_ref is not None:
            meta.setdefault("spot_ref", spot_ref)
        if ref.structure_id is not None:
            meta.setdefault("structure_id", ref.structure_id)

        meta_json = json.dumps(meta, ensure_ascii=False) if meta else None

        with sqlite3.connect(self.db_path) as conn:
            columns = set(self._get_table_columns(conn, "payoff_curve_points"))
            has_structure_id = "structure_id" in columns

            records = []
            for point in points:
                if isinstance(point, (list, tuple)) and len(point) >= 2:
                    spot, pl = point[0], point[1]
                elif isinstance(point, dict):
                    spot = point.get("spot", point.get("x"))
                    pl = point.get("pl", point.get("y"))
                else:
                    continue

                if spot is None or pl is None:
                    continue

                if has_structure_id:
                    records.append(
                        (
                            timestamp,
                            ref.aba,
                            ref.structure_id,
                            float(spot),
                            float(pl),
                            meta_json,
                        )
                    )
                else:
                    records.append(
                        (
                            timestamp,
                            ref.aba,
                            float(spot),
                            float(pl),
                            meta_json,
                        )
                    )

            if not records:
                return 0

            cursor = conn.cursor()

            if has_structure_id:
                cursor.executemany(
                    """
                    INSERT INTO payoff_curve_points
                    (timestamp, aba, structure_id, point_spot, point_pl, meta_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    records,
                )
            else:
                cursor.executemany(
                    """
                    INSERT INTO payoff_curve_points
                    (timestamp, aba, point_spot, point_pl, meta_json)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    records,
                )

            return len(records)

    def save_structure_decision(
        self,
        timestamp: str,
        ref: StructureRef,
        decision: str,
        ratio: Optional[float] = None,
        dte_min: Optional[int] = None,
        pl_atual: Optional[float] = None,
        pl_max: Optional[float] = None,
        pl_min: Optional[float] = None,
        spread_pct_medio: Optional[float] = None,
        why: Optional[Dict] = None,
    ) -> int:
        """
        DEPRECATED: Use db.derived_repo.write_decision_snapshot_atomic().
        Mantido para compatibilidade, usando StructureRef corretamente.
        """
        warnings.warn(
            "PayoffWriter.save_structure_decision está deprecated. "
            "Use db.derived_repo.write_decision_snapshot_atomic() diretamente.",
            DeprecationWarning,
            stacklevel=2,
        )

        from db.derived_repo import get_derived_connection, write_decision_snapshot_atomic

        decision_dict = {
            "decision": decision,
            "ratio": ratio,
            "dte_min": dte_min,
            "pl_atual": pl_atual,
            "pl_max": pl_max,
            "pl_min": pl_min,
            "spread_pct_medio": spread_pct_medio,
            "why": why,
        }

        if ref.structure_id is not None:
            decision_dict["structure_id"] = ref.structure_id

        conn = get_derived_connection()
        try:
            return write_decision_snapshot_atomic(conn, timestamp, ref, decision_dict)
        finally:
            conn.close()

    def get_latest_decision(self, ref: StructureRef) -> Optional[Dict]:
        """Retorna a última decisão para uma estrutura."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            column, value = self._resolve_ref_filter(conn, "structure_decisions", ref)

            existing_columns = self._get_table_columns(conn, "structure_decisions")
            selected_cols = [
                col for col in _STRUCTURE_DECISION_COLUMNS
                if col in existing_columns
            ]

            rows = conn.execute(
                f"""
                SELECT {", ".join(selected_cols)}
                FROM structure_decisions
                WHERE {column} = ?
                """,
                (value,),
            ).fetchall()

            data = [dict(row) for row in rows]
            if not data:
                return None

            return max(
                data,
                key=lambda row: (
                    self._timestamp_sort_key(row.get("timestamp")),
                    int(row.get("id") or 0),
                ),
            )

    def get_payoff_history(
        self,
        ref: StructureRef,
        limit: int = 100,
    ) -> List[Dict]:
        """Retorna histórico de payoff points para uma estrutura."""
        limit = int(limit)
        if limit <= 0:
            raise ValueError("limit deve ser maior que zero")

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            column, value = self._resolve_ref_filter(conn, "payoff_curve_points", ref)

            existing_columns = self._get_table_columns(conn, "payoff_curve_points")
            selected_cols = [
                col for col in _PAYOFF_HISTORY_COLUMNS
                if col in existing_columns
            ]

            rows = conn.execute(
                f"""
                SELECT {", ".join(selected_cols)}
                FROM payoff_curve_points
                WHERE {column} = ?
                """,
                (value,),
            ).fetchall()

            data = [dict(row) for row in rows]
            data.sort(
                key=lambda row: (
                    self._timestamp_sort_key(row.get("timestamp")),
                    int(row.get("id") or 0),
                ),
                reverse=True,
            )

            result = data[:limit]
            for row in result:
                row.pop("id", None)

            return result
