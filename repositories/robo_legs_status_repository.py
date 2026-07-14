# repositories/robo_legs_status_repository.py
"""
alteracao_40 -- método canônico por structure_id adicionado
alteracao_62 -- _resolve_aba_from_structure_id movido para AbaResolverMixin
             (elimina duplicação com robo_legs_repository)
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from infra.sqlite_conn import sqlite_conn
from repositories._aba_resolver_mixin import AbaResolverMixin
from domain.refs.structure_ref import StructureRef
from utils.leg_normalizers import parse_timestamp


def _to_aba(ref) -> str:
    """Aceita StructureRef ou str e devolve a string da aba."""
    if isinstance(ref, str):
        return ref
    return ref.aba


@dataclass(frozen=True)
class RoboLegsStatusRepoConfig:
    app_db_path: str = "./dados/app.db"


class RoboLegsStatusRepository(AbaResolverMixin):
    """
    Repository de status de legs do robô.

    alteracao_62: herda AbaResolverMixin -- _resolve_aba_from_structure_id
              não é mais definido localmente.
    """

    def __init__(self, config: Optional[RoboLegsStatusRepoConfig] = None):
        self.config = config or RoboLegsStatusRepoConfig()

    def latest_timestamps(
        self,
        ref: StructureRef,
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Retorna (manual_latest_ts, rtd_latest_ts) para a aba.
        Se não houver, retorna (None, None).
        """
        aba = _to_aba(ref)
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

    # ------------------------------------------------------------------ #
    # alteracao_40: método canônico por structure_id                          #
    # alteracao_62: _resolve_aba_from_structure_id herdado de AbaResolverMixin#
    # ------------------------------------------------------------------ #

    def latest_timestamps_by_structure_id(
        self,
        structure_id: int,
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Versão canônica de latest_timestamps() por structure_id.
        Retorna (manual_latest_ts, rtd_latest_ts).
        """
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            return (None, None)
        return self.latest_timestamps(
            ref=StructureRef(aba=aba, structure_id=structure_id),
        )
