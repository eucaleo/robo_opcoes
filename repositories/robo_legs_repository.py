# repositories/robo_legs_repository.py
"""
alteracao_40 -- métodos canônicos por structure_id adicionados
alteracao_62 -- _resolve_aba_from_structure_id movido para AbaResolverMixin
             (elimina duplicação com robo_legs_status_repository)
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from domain.position_side import normalize_position_side
from dto.robo_leg_dto import FonteType, RoboLegDTO
from infra.sqlite_conn import sqlite_conn
from repositories._aba_resolver_mixin import AbaResolverMixin
from src.domain.refs.structure_ref import StructureRef
from utils.leg_normalizers import parse_timestamp, parse_vencimento


def _to_aba(ref) -> str:
    """Aceita StructureRef ou str e devolve a string da aba."""
    if isinstance(ref, str):
        return ref
    return ref.aba  # StructureRef.aba (alteracao_53)


@dataclass(frozen=True)
class RoboLegsRepoConfig:
    app_db_path: str = "./dados/app.db"


class RoboLegsRepository(AbaResolverMixin):
    """
    Leitura canônica por (aba, timestamp) com regra:
      manual_analise_robo_legs > rtd_analise_robo_legs

    Observação importante:
    O banco legado pode armazenar timestamp como texto em formatos diferentes,
    principalmente:
    - ISO: YYYY-MM-DD HH:MM:SS
    - BR : DD/MM/YYYY HH:MM:SS

    Portanto a leitura precisa ser tolerante a ambas as representações.

    alteracao_62: herda AbaResolverMixin -- _resolve_aba_from_structure_id
              não é mais definido localmente.
    """

    def __init__(self, config: Optional[RoboLegsRepoConfig] = None):
        self.config = config or RoboLegsRepoConfig()

    def get_legs(self, ref: StructureRef, timestamp: Any) -> List[RoboLegDTO]:
        """
        Retorna legs para uma aba e um timestamp exatos.
        - Primeiro tenta MANUAL
        - Se vazio, tenta RTD
        """
        aba = _to_aba(ref)
        ts = parse_timestamp(timestamp)
        ts_candidates = self._timestamp_candidates(timestamp, ts)

        manual = self._query_legs(
            table="manual_analise_robo_legs",
            aba=aba,
            ts_candidates=ts_candidates,
            fonte=FonteType.MANUAL,
        )
        if manual:
            return manual

        rtd = self._query_legs(
            table="rtd_analise_robo_legs",
            aba=aba,
            ts_candidates=ts_candidates,
            fonte=FonteType.RTD,
        )
        return rtd

    def has_manual(self, ref: StructureRef, timestamp: Any) -> bool:
        aba = _to_aba(ref)
        ts = parse_timestamp(timestamp)
        ts_candidates = self._timestamp_candidates(timestamp, ts)

        placeholders = ",".join("?" for _ in ts_candidates)
        sql = f"""
            SELECT 1
            FROM manual_analise_robo_legs
            WHERE aba = ?
              AND timestamp IN ({placeholders})
            LIMIT 1
        """

        with sqlite_conn(self.config.app_db_path) as conn:
            cur = conn.execute(sql, (aba, *ts_candidates))
            return cur.fetchone() is not None

    def list_timestamps(
        self,
        ref: StructureRef,
        prefer: str = "manual_then_rtd",
    ) -> List[str]:
        """Lista timestamps disponíveis para a aba."""
        aba = _to_aba(ref)
        prefer = (prefer or "").strip().lower()
        with sqlite_conn(self.config.app_db_path) as conn:
            if prefer == "all":
                rows = conn.execute(
                    """
                    SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?
                    UNION
                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?
                    ORDER BY timestamp
                    """,
                    (aba, aba),
                ).fetchall()
                return [r["timestamp"] for r in rows]

            rows_m = conn.execute(
                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs "
                "WHERE aba = ? ORDER BY timestamp",
                (aba,),
            ).fetchall()
            if rows_m:
                return [r["timestamp"] for r in rows_m]

            rows_r = conn.execute(
                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "
                "WHERE aba = ? ORDER BY timestamp",
                (aba,),
            ).fetchall()
            return [r["timestamp"] for r in rows_r]

    def _query_legs(
        self,
        table: str,
        aba: str,
        ts_candidates: List[str],
        fonte: FonteType,
    ) -> List[RoboLegDTO]:
        placeholders = ",".join("?" for _ in ts_candidates)
        sql = f"""
            SELECT *
            FROM {table}
            WHERE aba = ?
              AND timestamp IN ({placeholders})
        """

        with sqlite_conn(self.config.app_db_path) as conn:
            rows = conn.execute(sql, (aba, *ts_candidates)).fetchall()

        out: List[RoboLegDTO] = []
        for r in rows:
            data = dict(r)
            out.append(self._row_to_dto(data, fonte=fonte))
        return out

    def _row_to_dto(self, row: Dict[str, Any], fonte: FonteType) -> RoboLegDTO:
        """Mapeia colunas -> DTO com normalização simples."""

        def pick(*keys: str, default=None):
            for k in keys:
                if k in row and row[k] is not None:
                    return row[k]
            return default

        aba       = pick("aba")
        timestamp = pick("timestamp")
        cv        = pick("cv", "lado", "c_v")
        call_put  = pick("call_put", "cp", "tipo", "callput")
        strike    = pick("strike", "k", "preco_exercicio")
        quant     = pick("quant", "qty", "qtd", "quantidade")
        ativo     = pick("ativo", "ticker", "cod_ativo")
        venc      = pick("vencimento", "vcto", "expiry", "expiracao")
        preco     = pick("preco", "price", "premium")
        leg_id    = pick("id", "leg_id")

        cv_raw  = str(cv).upper().strip()       if cv        is not None else ""
        cp_raw  = str(call_put).upper().strip() if call_put  is not None else ""

        canonical_side = normalize_position_side(cv_raw)
        cv_norm       = "C" if canonical_side == "COMPRADO" else "V"
        call_put_norm = "CALL" if cp_raw in ["CALL", "C"] else "PUT"

        return RoboLegDTO(
            aba=str(aba).strip(),
            timestamp=parse_timestamp(timestamp),
            cv=cv_norm,
            call_put=call_put_norm,
            strike=float(strike)       if strike  is not None else 0.0,
            quant=int(quant)           if quant   is not None else 0,
            ativo=str(ativo).strip().upper() if ativo is not None else "",
            vencimento=parse_vencimento(venc) if venc is not None else None,
            fonte=fonte,
            id=int(leg_id)             if leg_id  is not None else None,
            preco=float(preco)         if preco   is not None else None,
            created_at=None,
            updated_at=None,
        )

    @staticmethod
    def _timestamp_candidates(original: Any, ts: datetime) -> List[str]:
        """
        Gera representações aceitas para comparar com o banco legado.
        Ordem:
        1. valor original (se string)
        2. ISO datetime
        3. BR datetime
        4. ISO date
        5. BR date
        """
        candidates: List[str] = []

        if isinstance(original, str):
            raw = original.strip()
            if raw:
                candidates.append(raw)

        iso_dt = ts.replace(microsecond=0).isoformat(sep=" ")
        br_dt  = ts.strftime("%d/%m/%Y %H:%M:%S")
        iso_d  = ts.strftime("%Y-%m-%d")
        br_d   = ts.strftime("%d/%m/%Y")

        for v in [iso_dt, br_dt, iso_d, br_d]:
            if v not in candidates:
                candidates.append(v)

        return candidates

    # ------------------------------------------------------------------ #
    # alteracao_40: métodos canônicos por structure_id                        #
    # alteracao_62: _resolve_aba_from_structure_id herdado de AbaResolverMixin#
    # ------------------------------------------------------------------ #

    def get_legs_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
    ) -> List[RoboLegDTO]:
        """
        Ponto de entrada canônico: recebe structure_id, resolve para aba,
        delega para get_legs() existente.
        Levanta ValueError se structure_id não mapeado.
        """
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            raise ValueError(
                f"structure_id={structure_id} sem alias_legacy_aba em structures"
            )
        # alteracao_62: passa StructureRef em vez de str nua -- semântica explícita
        ref = StructureRef(aba=aba, structure_id=structure_id)
        return self.get_legs(ref=ref, timestamp=timestamp)

    def has_manual_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
    ) -> bool:
        """Versão canônica de has_manual() por structure_id."""
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            return False
        return self.has_manual(
            ref=StructureRef(aba=aba, structure_id=structure_id),
            timestamp=timestamp,
        )

    def list_timestamps_by_structure_id(
        self,
        structure_id: int,
        prefer: str = "manual_then_rtd",
    ) -> List[str]:
        """Versão canônica de list_timestamps() por structure_id."""
        aba = self._resolve_aba_from_structure_id(structure_id)
        if aba is None:
            raise ValueError(
                f"structure_id={structure_id} sem alias_legacy_aba em structures"
            )
        return self.list_timestamps(
            ref=StructureRef(aba=aba, structure_id=structure_id),
            prefer=prefer,
        )
