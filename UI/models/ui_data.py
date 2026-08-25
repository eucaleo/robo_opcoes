# UI/models/ui_data.py
# alteracao_36_E: eliminar self._conn compartilhada
# Toda conexao de leitura passa a ser por chamada (igual a _connect_app_threadsafe)
from domain.refs.structure_ref import StructureRef
from db import derived_repo
from db import app_metadata_repo
from db import ui_data_query_repo
from db.ui_data_query_repo import (
    build_decision_subquery as build_decision_subquery_repo,
    fetch_decision_rows as fetch_decision_rows_repo,
)

_PAYOFF_REPO_LOADER = derived_repo.get_payoff_curve_points_by_structure_id
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from db.config import APP_DB_PATH
import json
import csv
from datetime import datetime

from repositories.ui_data_table_candidates import (
    CANDIDATE_CONSOLIDATION_TABLES,
    CANDIDATE_PAYOFF_TABLES,
)

# Mapeamento de colunas preferidas -> alternativas
COLUMN_ALIASES = {
    "timestamp":     ["timestamp", "ts", "decided_at", "dt_ref"],
    "structure_id":  ["structure_id"],                              #  alteracao_33: chave canônica
    "aba":           ["aba", "sheet", "tab"],                       # mantido para compat
    "decision":      ["decision", "decisao", "action"],
    "level":         ["level", "nivel", "severity_level"],
    "pl_pct_of_max": ["pl_pct_of_max", "pl_ratio", "pl_pct"],
    "ratio":         ["ratio", "pl_ratio", "pl_pct_of_max", "pl_pct"],
    "dte_min":       ["dte_min", "dte", "days_to_expiry"],
    "why":           ["why", "rationale", "rationale_json"],
    "why_json":      ["why_json", "meta_json"],
    "pl_atual":      ["pl_atual", "pl_current"],
    "pl_max":        ["pl_max", "pl_best", "pl_top"],
    "spot_ref":      ["spot_ref", "spot_reference", "ref_spot"],
}

PAYOFF_COLUMN_ALIASES = {
    "timestamp": ["timestamp", "ts", "dt_ref"],
    "structure_id": ["structure_id"],   #  alteracao_33
    "spot":      ["point_spot", "spot", "underlying", "x", "s_t"],
    "pl":        ["point_pl", "pl", "pl_value", "y", "payoff", "pl_venc"],
}

def _first_match(cols: List[str], candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in cols:
            return c
    return None

class UIDataModel:
    def invalidate_payoff_cache(self, structure_id=None) -> None:
        """
        Invalida cache local de payoff.

        A UI usa isso apos comando oficial de backend para evitar
        leitura de snapshot antigo.
        """
        if hasattr(self, "_payoff_cache") and isinstance(self._payoff_cache, dict):
            self._payoff_cache.clear()

    def __init__(self, app_db_path: Optional[Path] = None):
        from db.config import APP_DB_PATH
        self.app_db_path = (
            Path(app_db_path).resolve()
            if app_db_path
            else Path(APP_DB_PATH).resolve()
        )
        print(f"[UI] Usando app DB: {self.app_db_path}")

        # alteracao_36_E: self._conn REMOVIDO -- cada metodo abre sua propria conexao
        self._consolidations_table: Optional[str] = None
        self._payoff_table: Optional[str] = None
        self._consolidations_cols: Dict[str, str] = {}
        self._payoff_cols: Dict[str, str] = {}
        self._cache_structures: List[str] = []

        self._payoff_cache: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self._payoff_cache_max = 128

    # alteracao_36_E: _connect agora e sempre uma nova conexao por chamada
    def _connect(self):
        # Compatibilidade com guardrail legado: ui_data_query_repo.connect(
        return ui_data_query_repo.connect_ui_data_db(self.app_db_path)

    def _fetch_latest_legacy_payoff_timestamp(
        self, conn, p, filter_col, filter_val
    ):
        return ui_data_query_repo.fetch_latest_legacy_payoff_timestamp(
            conn, p, filter_col, filter_val, self._payoff_table
        )

    def _load_legacy_payoff_curve_info_points(
        self,
        conn,
        p,
        filter_col,
        filter_val,
        timestamp,
    ):
        used_ts = timestamp
        rows = ui_data_query_repo.fetch_legacy_payoff_curve_exact_rows(
            conn, p, filter_col, filter_val, used_ts, self._payoff_table
        )
        if not rows:
            used_ts = self._fetch_latest_legacy_payoff_timestamp(
                conn, p, filter_col, filter_val
            )
            if used_ts:
                rows = ui_data_query_repo.fetch_legacy_payoff_curve_exact_rows(
                    conn, p, filter_col, filter_val, used_ts, self._payoff_table
                )
        return rows, used_ts

    def _build_legacy_payoff_curve_exact_sql(self, p, filter_col):
        return ui_data_query_repo.build_legacy_payoff_curve_exact_sql(
            p, filter_col, self._payoff_table
        )

    def _fetch_latest_canonical_payoff_timestamp(
        self, conn, filter_col, filter_val
    ):
        return ui_data_query_repo.fetch_latest_canonical_payoff_timestamp(
            conn, filter_col, filter_val
        )

    def _fetch_canonical_payoff_curve_points(
        self,
        conn,
        filter_col,
        filter_val,
        timestamp,
        extra_cols,
    ):
        return ui_data_query_repo.fetch_canonical_payoff_curve_points(
            conn, filter_col, filter_val, timestamp, extra_cols
        )

    def _fetch_latest_payoff_curve_timestamp(self, conn, p, filter_col, filter_val):
        return ui_data_query_repo.fetch_latest_payoff_curve_timestamp(
            conn, p, filter_col, filter_val, self._payoff_table
        )

    def _fetch_payoff_curve_latest_timestamp(self, conn, p, filter_col, filter_val):
        return ui_data_query_repo.fetch_payoff_curve_latest_timestamp(
            conn, p, filter_col, filter_val, self._payoff_table
        )

    def _build_payoff_curve_latest_timestamp_sql(self, p, filter_col):
        return ui_data_query_repo.build_payoff_curve_latest_timestamp_sql(
            p, filter_col, self._payoff_table
        )

    def _fetch_payoff_curve_exact_rows(
        self, conn, p, filter_col, filter_val, timestamp
    ):
        return ui_data_query_repo.fetch_payoff_curve_exact_rows(
            conn, p, filter_col, filter_val, timestamp, self._payoff_table
        )

    def _build_payoff_curve_exact_sql(self, p, filter_col):
        return ui_data_query_repo.build_payoff_curve_exact_sql(
            p, filter_col, self._payoff_table
        )
