from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from infra.sqlite_conn import sqlite_conn
from utils.leg_normalizers import parse_timestamp


@dataclass(frozen=True)
class RoboLegsStatusRepoConfig:
    app_db_path: str = "./dados/app.db"


class RoboLegsStatusRepository:
    def __init__(self, config: Optional[RoboLegsStatusRepoConfig] = None):
        self.config = config or RoboLegsStatusRepoConfig()

    def latest_timestamps(self, aba: str) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Retorna (manual_latest_ts, rtd_latest_ts) para a aba.
        Se não houver, retorna (None, None).
        """
        with sqlite_conn(self.config.app_db_path) as conn:
            row_m = conn.execute(
                "SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",
                (aba,),
            ).fetchone()
            row_r = conn.execute(
                "SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",
                (aba,),
            ).fetchone()

        m = parse_timestamp(row_m["ts"]) if row_m and row_m["ts"] else None
        r = parse_timestamp(row_r["ts"]) if row_r and row_r["ts"] else None
        return (m, r)
