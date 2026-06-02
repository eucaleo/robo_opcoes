"""
patch_45 — Contrato canônico de entrada para cálculo.

Define os DTOs imutáveis que o domínio recebe:
  CalculationRequest
    ├── structure: StructureInput
    │     └── legs: List[StructureLegInput]
    └── market_snapshot: MarketSnapshotInput

O domínio NÃO acessa banco diretamente — recebe estes objetos
já normalizados pelo orquestrador.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


# ---------------------------------------------------------------------------
# Constantes de domínio
# ---------------------------------------------------------------------------
VALID_POSITION_SIDES = {"LONG", "SHORT"}
VALID_OPTION_TYPES   = {"CALL", "PUT"}
VALID_SOURCES        = {"rtd", "manual", "ui"}
_DATE_RE             = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# Helpers de validação
# ---------------------------------------------------------------------------
def _require_nonempty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} não pode ser vazio")
    return value.strip()


def _require_positive(value: float | int, field_name: str) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} deve ser numérico, recebeu: {value!r}")
    if v <= 0:
        raise ValueError(f"{field_name} deve ser positivo, recebeu: {v}")
    return v


def _require_date_str(value: str, field_name: str) -> str:
    """Aceita string 'YYYY-MM-DD' e valida."""
    if not isinstance(value, str) or not _DATE_RE.match(value):
        raise ValueError(
            f"{field_name} deve estar no formato YYYY-MM-DD, recebeu: {value!r}"
        )
    # Valida calendário
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"{field_name} é uma data inválida: {value!r}")
    return value


# ---------------------------------------------------------------------------
# StructureLegInput
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class StructureLegInput:
    """
    Representa uma perna (leg) da estrutura, já normalizada.

    position_side : LONG | SHORT
    option_type   : CALL | PUT
    strike        : decimal positivo
    expiration_date: YYYY-MM-DD
    quantity      : inteiro positivo (direção fica em position_side)
    symbol        : código da opção (ex.: BOVAE195) — opcional
    premium       : preço de entrada — opcional
    multiplier    : padrão 1.0
    leg_order     : ordem para exibição
    """
    position_side:   str
    option_type:     str
    strike:          float
    expiration_date: str
    quantity:        int

    symbol:      Optional[str]   = None
    premium:     Optional[float] = None
    multiplier:  float           = 1.0
    leg_order:   int             = 0
    notes:       Optional[str]   = None

    def __post_init__(self):
        if self.position_side not in VALID_POSITION_SIDES:
            raise ValueError(
                f"position_side inválido: {self.position_side!r}. "
                f"Use: {VALID_POSITION_SIDES}"
            )
        if self.option_type not in VALID_OPTION_TYPES:
            raise ValueError(
                f"option_type inválido: {self.option_type!r}. "
                f"Use: {VALID_OPTION_TYPES}"
            )
        # strike deve ser positivo
        object.__setattr__(self, "strike", _require_positive(self.strike, "strike"))
        # quantity deve ser inteiro positivo
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValueError(f"quantity deve ser inteiro positivo, recebeu: {self.quantity!r}")
        # expiration_date: formato canônico
        object.__setattr__(
            self, "expiration_date",
            _require_date_str(self.expiration_date, "expiration_date")
        )
        # multiplier
        if self.multiplier <= 0:
            raise ValueError(f"multiplier deve ser positivo, recebeu: {self.multiplier}")


# ---------------------------------------------------------------------------
# StructureInput
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class StructureInput:
    """
    Representa a estrutura completa pronta para cálculo.

    structure_id      : PK canônica (INTEGER do DB)
    underlying_asset  : ativo base (ex.: BOVA11)
    legs              : pernas já normalizadas
    name              : label amigável
    alias_legacy_aba  : compatibilidade — NÃO é chave de cálculo
    """
    structure_id:     int
    underlying_asset: str
    legs:             List[StructureLegInput]

    name:             Optional[str] = None
    alias_legacy_aba: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.structure_id, int) or self.structure_id <= 0:
            raise ValueError(
                f"structure_id deve ser inteiro positivo, recebeu: {self.structure_id!r}"
            )
        _require_nonempty(self.underlying_asset, "underlying_asset")
        if not isinstance(self.legs, list) or len(self.legs) == 0:
            raise ValueError("legs não pode ser lista vazia")
        for i, leg in enumerate(self.legs):
            if not isinstance(leg, StructureLegInput):
                raise TypeError(
                    f"legs[{i}] deve ser StructureLegInput, recebeu: {type(leg)}"
                )


# ---------------------------------------------------------------------------
# MarketSnapshotInput
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class MarketSnapshotInput:
    """
    Representa o estado de mercado no momento do cálculo.

    snapshot_timestamp : ISO-8601 string (ex.: '2026-06-02T20:49:43')
    underlying_asset   : deve coincidir com StructureInput.underlying_asset
    spot_price         : preço spot positivo
    source             : 'rtd' | 'manual' | 'ui'
    snapshot_id        : referência interna opcional
    """
    snapshot_timestamp: str
    underlying_asset:   str
    spot_price:         float
    source:             str

    snapshot_id:         Optional[int]   = None
    option_quotes:       Optional[dict]  = None   # bid/ask por símbolo
    greeks:              Optional[dict]  = None
    volatility_context:  Optional[dict]  = None

    def __post_init__(self):
        _require_nonempty(self.snapshot_timestamp, "snapshot_timestamp")
        _require_nonempty(self.underlying_asset,   "underlying_asset")
        object.__setattr__(
            self, "spot_price",
            _require_positive(self.spot_price, "spot_price")
        )
        if self.source not in VALID_SOURCES:
            raise ValueError(
                f"source inválido: {self.source!r}. Use: {VALID_SOURCES}"
            )
        # Tenta parsear timestamp para garantir que é válido
        try:
            datetime.fromisoformat(self.snapshot_timestamp)
        except ValueError:
            raise ValueError(
                f"snapshot_timestamp não é ISO-8601 válido: {self.snapshot_timestamp!r}"
            )


# ---------------------------------------------------------------------------
# CalculationRequest — envelope completo
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CalculationRequest:
    """
    Contrato canônico de entrada para qualquer cálculo de payoff/decisão.

    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
    e o domínio (payoff, decision) recebe SOMENTE este objeto — sem
    acessar banco diretamente.
    """
    structure:       StructureInput
    market_snapshot: MarketSnapshotInput

    def __post_init__(self):
        if self.structure.underlying_asset != self.market_snapshot.underlying_asset:
            raise ValueError(
                f"underlying_asset diverge entre structure "
                f"({self.structure.underlying_asset!r}) "
                f"e market_snapshot ({self.market_snapshot.underlying_asset!r})"
            )
