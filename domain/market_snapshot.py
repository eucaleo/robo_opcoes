# domain/market_snapshot.py
"""
Objetos de domínio para snapshots de mercado.

alteracao_12: LegMarketSnapshot, SnapshotSource
alteracao_13: StructureMarketSnapshot (agrega legs + cabeçalho RTD)
"""
from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


#  Enum de origem 

class SnapshotSource(str, Enum):
    RTD    = "rtd"
    MANUAL = "manual"


#  Leg individual 

@dataclass
class LegMarketSnapshot:
    """Representa uma perna (leg) de uma estrutura de opções."""

    aba             : str
    ativo           : str
    cv              : Optional[str]   = None
    call_put        : Optional[str]   = None
    quant           : Optional[float] = None
    valor_executado : Optional[float] = None
    bid             : Optional[float] = None
    ask             : Optional[float] = None
    mid             : Optional[float] = None   # calculado: (bid + ask) / 2
    spread          : Optional[float] = None
    spread_pct      : Optional[float] = None
    iv              : Optional[float] = None
    delta           : Optional[float] = None
    gamma           : Optional[float] = None
    theta           : Optional[float] = None
    vega            : Optional[float] = None
    strike          : Optional[float] = None
    vencimento      : Optional[str]   = None
    dte             : Optional[float] = None
    pl_realista     : Optional[float] = None
    timestamp       : Optional[str]   = None
    source          : SnapshotSource  = SnapshotSource.RTD


#  Estrutura completa (cabeçalho + legs) 

@dataclass
class StructureMarketSnapshot:
    """
    Agrega o cabeçalho da estrutura (rtd_analise_robo) e suas legs.

    Atributos do cabeçalho (todos opcionais -- podem vir de RTD ou manual):
      aba, spot, num_pernas, dte_min, pl_realista_total,
      delta_liq, gamma_liq, theta_liq, vega_liq,
      spread_medio, spread_pct_medio, alertas_v2

    Atributo agregado:
      legs  -- lista de LegMarketSnapshot
      source -- origem predominante dos dados
    """

    aba                : str
    legs               : list[LegMarketSnapshot]        = field(default_factory=list)
    source             : SnapshotSource                 = SnapshotSource.RTD

    #  cabeçalho RTD / summary 
    spot               : Optional[float] = None
    num_pernas         : Optional[int]   = None
    dte_min            : Optional[int]   = None
    pl_realista_total  : Optional[float] = None
    delta_liq          : Optional[float] = None
    gamma_liq          : Optional[float] = None
    theta_liq          : Optional[float] = None
    vega_liq           : Optional[float] = None
    spread_medio       : Optional[float] = None
    spread_pct_medio   : Optional[float] = None
    alertas_v2         : Optional[str]   = None

    #  helpers de conveniência 

    @property
    def num_legs(self) -> int:
        return len(self.legs)

    @property
    def has_summary(self) -> bool:
        """True se os dados de cabeçalho foram populados."""
        return self.spot is not None

    def __repr__(self) -> str:
        return (
            f"StructureMarketSnapshot("
            f"aba={self.aba!r}, "
            f"num_legs={self.num_legs}, "
            f"spot={self.spot}, "
            f"source={self.source.value!r})"
        )
