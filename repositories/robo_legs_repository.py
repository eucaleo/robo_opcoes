from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from dto.robo_leg_dto import FonteType, RoboLegDTO
from infra.sqlite_conn import sqlite_conn
from utils.leg_normalizers import (
    normalize_call_put,
    normalize_cv,
    parse_timestamp,
    parse_vencimento,
)



@dataclass(frozen=True)
class RoboLegsRepoConfig:
    app_db_path: str = "./dados/app.db"


class RoboLegsRepository:

    @staticmethod
    def _parse_float(value):
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)

        s = str(value).strip()
        if not s:
            return None

        try:
            if "," in s:
                s = s.replace(".", "").replace(",", ".")
            return float(s)
        except ValueError:
            return None

    @staticmethod
    def _parse_int(value):
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)

        s = str(value).strip()
        if not s:
            return None

        try:
            if "," in s:
                s = s.replace(".", "").replace(",", ".")
            return int(float(s))
        except ValueError:
            return None

    """
    Leitura canônica por (aba, timestamp) com regra:
      manual_analise_robo_legs > rtd_analise_robo_legs

    Observação importante:
    O banco legado pode armazenar timestamp como texto em formatos diferentes,
    principalmente:
    - ISO: YYYY-MM-DD HH:MM:SS
    - BR : DD/MM/YYYY HH:MM:SS

    Portanto a leitura precisa ser tolerante a ambas as representações.
    """

    def __init__(self, config: Optional[RoboLegsRepoConfig] = None):
        self.config = config or RoboLegsRepoConfig()

    def get_legs(self, aba: str, timestamp: Any) -> List[RoboLegDTO]:
        """
        Retorna legs para uma aba e um timestamp exatos.
        - Primeiro tenta MANUAL
        - Se vazio, tenta RTD
        """
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

    def has_manual(self, aba: str, timestamp: Any) -> bool:
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

    def list_timestamps(self, aba: str, prefer: str = "manual_then_rtd") -> List[str]:
        """Lista timestamps disponíveis para a aba."""
        prefer = (prefer or "").strip().lower()

        with sqlite_conn(self.config.app_db_path) as conn:
            rows_m = conn.execute(
                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs WHERE aba = ? ORDER BY timestamp",
                (aba,),
            ).fetchall()
            manual = [r["timestamp"] for r in rows_m]

            rows_r = conn.execute(
                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs WHERE aba = ? ORDER BY timestamp",
                (aba,),
            ).fetchall()
            rtd = [r["timestamp"] for r in rows_r]

        if prefer == "manual_only":
            return manual

        if prefer == "rtd_only":
            return rtd

        if prefer == "manual_then_rtd":
            return manual if manual else rtd

        if prefer == "all":
            return sorted(set(manual) | set(rtd))

        raise ValueError(
            "prefer must be one of: 'manual_then_rtd', 'manual_only', 'rtd_only', 'all'"
        )


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
        """Mapeia colunas -> DTO com normalização simples"""

        def pick(*keys: str, default=None):
            for k in keys:
                if k in row and row[k] is not None:
                    return row[k]
            return default

        aba = pick("aba")
        timestamp = pick("timestamp")
        cv = pick("cv", "lado", "c_v")
        call_put = pick("call_put", "cp", "tipo", "callput")
        strike = pick("strike", "k", "preco_exercicio")
        quant = pick("quant", "qty", "qtd", "quantidade")
        ativo = pick("ativo", "ticker", "cod_ativo")
        venc = pick("vencimento", "vcto", "expiry", "expiracao")
        preco = pick("preco", "price", "premium")
        leg_id = pick("id", "leg_id")

        cv_norm = normalize_cv(cv).value
        call_put_norm = normalize_call_put(call_put).value

        dto = RoboLegDTO(
            aba=str(aba).strip(),
            timestamp=parse_timestamp(timestamp),
            cv=cv_norm,
            call_put=call_put_norm,
            strike=self._parse_float(strike) if self._parse_float(strike) is not None else 0.0,
            quant=self._parse_int(quant) if self._parse_int(quant) is not None else 0,
            ativo=str(ativo).strip().upper() if ativo is not None else "",
            vencimento=parse_vencimento(venc) if venc is not None else None,
            fonte=fonte,
            id=int(leg_id) if leg_id is not None else None,
            preco=float(preco) if preco is not None else None,
            created_at=None,
            updated_at=None,
        )
        return dto

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
        br_dt = ts.strftime("%d/%m/%Y %H:%M:%S")
        iso_d = ts.strftime("%Y-%m-%d")
        br_d = ts.strftime("%d/%m/%Y")

        for v in [iso_dt, br_dt, iso_d, br_d]:
            if v not in candidates:
                candidates.append(v)

        return candidates
