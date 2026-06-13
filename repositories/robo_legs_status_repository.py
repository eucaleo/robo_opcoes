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
from src.domain.refs.structure_ref import StructureRef
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

    @staticmethod
    def _latest_parsed_timestamp(values) -> Optional[datetime]:
        """
        Retorna o maior timestamp cronológico após parse.

        Evita SELECT MAX(timestamp), que é textual no SQLite e pode errar
        quando há mistura de formatos ISO e BR.
        """
        latest: Optional[datetime] = None

        for value in values:
            if value is None:
                continue

            try:
                parsed = parse_timestamp(value)
            except Exception:
                continue

            if latest is None or parsed > latest:
                latest = parsed

        return latest

    def latest_timestamps(
        self,
        ref: StructureRef,
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Retorna (manual_latest_ts, rtd_latest_ts) para a aba.
        Se não houver, retorna (None, None).

        O cálculo do maior timestamp é feito em Python, não via MAX(timestamp),
        para evitar erro de ordenação textual com formatos mistos.
        """
        aba = _to_aba(ref)

        with sqlite_conn(self.config.app_db_path) as conn:
            rows_m = conn.execute(
                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs WHERE aba = ?",
                (aba,),
            ).fetchall()
            rows_r = conn.execute(
                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs WHERE aba = ?",
                (aba,),
            ).fetchall()

        m = self._latest_parsed_timestamp([row["timestamp"] for row in rows_m])
        r = self._latest_parsed_timestamp([row["timestamp"] for row in rows_r])

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
