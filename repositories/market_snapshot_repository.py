# repositories/market_snapshot_repository.py
"""
patch_13 - Repositorio canonico de snapshots de mercado.

Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),
normaliza os campos e retorna objetos LegMarketSnapshot prontos para uso.

Schema real confirmado por 62_inspect_snapshot_tables.py (2026-05-27):
  - Nao existe coluna 'last'; mid = (bid + ask) / 2 calculado aqui.
  - Valores armazenados como TEXT com virgula decimal (pt-BR).
  - rtd_analise_robo_legs   : colunas [0-19]
  - manual_analise_robo_legs: colunas [0-21] + source + created_at
"""

from src.domain.refs.structure_ref import StructureRef
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from domain.market_snapshot import LegMarketSnapshot, SnapshotSource, StructureMarketSnapshot

# --- Caminhos ----------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_DB   = _PROJECT_ROOT / "dados" / "app.db"

# --- SQL ---------------------------------------------------------------------

_SQL_RTD_LEGS = """
    SELECT
        timestamp,
        aba,
        ativo,
        cv,
        call_put,
        quant,
        valor_executado,
        bid,
        ask,
        spread,
        spread_pct,
        iv,
        delta,
        gamma,
        theta,
        vega,
        strike,
        vencimento,
        dte,
        pl_realista
    FROM rtd_analise_robo_legs
    WHERE {ref.db_column()} = ?
    ORDER BY timestamp DESC
"""

_SQL_MANUAL_LEGS = """
    SELECT
        timestamp,
        aba,
        ativo,
        cv,
        call_put,
        quant,
        valor_executado,
        bid,
        ask,
        spread,
        spread_pct,
        iv,
        delta,
        gamma,
        theta,
        vega,
        strike,
        vencimento,
        dte,
        pl_realista,
        source,
        created_at
    FROM manual_analise_robo_legs
    WHERE {ref.db_column()} = ?
    ORDER BY timestamp DESC
"""

_SQL_RTD_SUMMARY = """
    SELECT
        aba,
        spot,
        num_pernas,
        dte_min,
        pl_realista_total,
        delta_liq,
        gamma_liq,
        theta_liq,
        vega_liq,
        spread_medio,
        spread_pct_medio,
        alertas_v2
    FROM rtd_analise_robo
    WHERE {ref.db_column()} = ?
    ORDER BY rowid DESC
    LIMIT 1
"""

# --- Helpers -----------------------------------------------------------------

def _parse_br_float(value) -> Optional[float]:
    # Converte string pt-BR ('1,38' ou '1,38E-02') para float.
    if value is None:
        return None
    try:
        normalized = str(value).strip().replace(",", ".")
        return float(normalized)
    except (ValueError, TypeError):
        return None


def _mid_price(bid: Optional[float], ask: Optional[float]) -> Optional[float]:
    # Calcula mid price. Nao usa coluna 'last' - nao existe no schema.
    if bid is not None and ask is not None:
        return round((bid + ask) / 2.0, 6)
    if bid is not None:
        return bid
    if ask is not None:
        return ask
    return None


def _row_to_leg(row: sqlite3.Row, source: SnapshotSource) -> LegMarketSnapshot:
    # Converte uma linha do banco em LegMarketSnapshot.
    bid = _parse_br_float(row["bid"])
    ask = _parse_br_float(row["ask"])
    mid = _mid_price(bid, ask)

    return LegMarketSnapshot(
        aba             = row["aba"],
        ativo           = row["ativo"],
        cv              = row["cv"],
        call_put        = row["call_put"],
        quant           = _parse_br_float(row["quant"]),
        valor_executado = _parse_br_float(row["valor_executado"]),
        bid             = bid,
        ask             = ask,
        mid             = mid,
        spread          = _parse_br_float(row["spread"]),
        spread_pct      = _parse_br_float(row["spread_pct"]),
        iv              = _parse_br_float(row["iv"]),
        delta           = _parse_br_float(row["delta"]),
        gamma           = _parse_br_float(row["gamma"]),
        theta           = _parse_br_float(row["theta"]),
        vega            = _parse_br_float(row["vega"]),
        strike          = _parse_br_float(row["strike"]),
        vencimento      = row["vencimento"],
        dte             = _parse_br_float(row["dte"]),
        pl_realista     = _parse_br_float(row["pl_realista"]),
        timestamp       = row["timestamp"],
        source          = source,
    )


# --- Repositorio -------------------------------------------------------------

class MarketSnapshotRepository:
    # Acesso de leitura aos snapshots de mercado.
    #
    # Metodos:
    #   get_rtd_legs(aba)     -> lista de LegMarketSnapshot (source=RTD)
    #   get_manual_legs(aba)  -> lista de LegMarketSnapshot (source=MANUAL)
    #   get_rtd_summary(aba)  -> dict com cabecalho RTD (ou None)
    #   get_structure(aba)    -> StructureMarketSnapshot completo

    def __init__(self, db_path: Path | str = _DEFAULT_DB) -> None:
        self._db_path = Path(db_path)
        if not self._db_path.exists():
            raise FileNotFoundError(f"Banco nao encontrado: {self._db_path}")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    # -- RTD ------------------------------------------------------------------

    def get_rtd_legs(self, ref: StructureRef) -> list[LegMarketSnapshot]:
        # Retorna as legs RTD mais recentes para uma aba.
        with self._connect() as conn:
            rows = conn.execute(_SQL_RTD_LEGS, (aba,)).fetchall()
        return [_row_to_leg(r, SnapshotSource.RTD) for r in rows]

    def get_rtd_summary(self, ref: StructureRef) -> Optional[dict]:
        # Retorna o cabecalho RTD da estrutura (linha mais recente).
        with self._connect() as conn:
            row = conn.execute(_SQL_RTD_SUMMARY, (aba,)).fetchone()
        if row is None:
            return None
        return dict(row)

    # -- Manual ---------------------------------------------------------------

    def get_manual_legs(self, ref: StructureRef) -> list[LegMarketSnapshot]:
        # Retorna as legs manuais mais recentes para uma aba.
        with self._connect() as conn:
            rows = conn.execute(_SQL_MANUAL_LEGS, (aba,)).fetchall()
        return [_row_to_leg(r, SnapshotSource.MANUAL) for r in rows]

    # -- Estrutura completa ---------------------------------------------------

    def get_structure(
        self,
        ref: StructureRef,
        source: SnapshotSource = SnapshotSource.RTD,
    ) -> StructureMarketSnapshot:
        # Retorna um StructureMarketSnapshot completo para a aba informada.
        #   source=RTD    -> legs de rtd_analise_robo_legs + summary de rtd_analise_robo
        #   source=MANUAL -> legs de manual_analise_robo_legs (sem summary)
        if source == SnapshotSource.RTD:
            legs    = self.get_rtd_legs(aba)
            summary = self.get_rtd_summary(aba)
        else:
            legs    = self.get_manual_legs(aba)
            summary = None

        def _f(key: str) -> Optional[float]:
            return _parse_br_float(summary[key]) if summary and summary.get(key) is not None else None

        return StructureMarketSnapshot(
            aba               = aba,
            legs              = legs,
            source            = source,
            spot              = _f("spot"),
            num_pernas        = int(_f("num_pernas"))  if _f("num_pernas") is not None else None,
            dte_min           = int(_f("dte_min"))     if _f("dte_min")    is not None else None,
            pl_realista_total = _f("pl_realista_total"),
            delta_liq         = _f("delta_liq"),
            gamma_liq         = _f("gamma_liq"),
            theta_liq         = _f("theta_liq"),
            vega_liq          = _f("vega_liq"),
            spread_medio      = _f("spread_medio"),
            spread_pct_medio  = _f("spread_pct_medio"),
            alertas_v2        = summary.get("alertas_v2") if summary else None,
        )
