"""
alteracao_45 -- Contrato canônico de entrada para cálculo.

Define os DTOs imutáveis que o domínio recebe:
  CalculationRequest
     structure: StructureInput
          legs: List[StructureLegInput]
     market_snapshot: MarketSnapshotInput

O domínio NÃO acessa banco diretamente -- recebe estes objetos
já normalizados pelo orquestrador.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional

from domain.position_side import to_pricing_engine_side


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

    position_side : LONG | SHORT tecnico; aceita aliases COMPRADO/VENDIDO e C/V
    option_type   : CALL | PUT
    strike        : decimal positivo
    expiration_date: YYYY-MM-DD
    quantity      : inteiro positivo (direção fica em position_side)
    symbol        : código da opção (ex.: BOVAE195) -- opcional
    premium       : preço de entrada -- opcional
    multiplier    : padrão 100.0
    leg_order     : ordem para exibição
    """
    position_side:   str
    option_type:     str
    strike:          float
    expiration_date: str
    quantity:        int

    symbol:      Optional[str]   = None
    premium:     Optional[float] = None
    multiplier:  float           = 100.0
    leg_order:   int             = 0
    notes:       Optional[str]   = None

    def __post_init__(self):
        try:
            position_side = to_pricing_engine_side(self.position_side)
        except ValueError as exc:
            raise ValueError(
                f"position_side inválido: {self.position_side!r}. "
                f"Use: {VALID_POSITION_SIDES} ou COMPRADO/VENDIDO"
            ) from exc

        object.__setattr__(self, "position_side", position_side)

        if position_side not in VALID_POSITION_SIDES:
            raise ValueError(
                f"position_side inválido: {position_side!r}. "
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
    alias_legacy_aba  : compatibilidade -- NÃO é chave de cálculo
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
# CalculationRequest -- envelope completo
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class CalculationRequest:
    """
    Contrato canônico de entrada para qualquer cálculo de payoff/decisão.

    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
    e o domínio (payoff, decision) recebe SOMENTE este objeto -- sem
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

# [FRENTE 48] INICIO - validacao controlada payoff calculation request
def _frente_48_is_number(value):
    """Retorna True para int/float finitos, rejeitando bool.

    Helper local da Frente 48 para fortalecer contrato de entrada de payoff
    sem alterar fluxo operacional amplo.
    """

    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    return value == value and value not in (float("inf"), float("-inf"))


def _frente_48_positive_number(value):
    """Confere numero positivo para campos financeiros obrigatorios."""

    return _frente_48_is_number(value) and float(value) > 0.0


def _frente_48_optional_number(value):
    """Confere numero opcional preservando zero e negativos quando semanticamente aceitos."""

    return value is None or _frente_48_is_number(value)


def _frente_48_normalize_option_type(value):
    """Normaliza CALL/PUT de forma estrita.

    Valores desconhecidos nao recebem default silencioso.
    """

    if value is None:
        return None

    current = str(value).strip().upper()
    aliases = {
        "C": "CALL",
        "CALL": "CALL",
        "P": "PUT",
        "PUT": "PUT",
    }
    return aliases.get(current)


def _frente_48_normalize_position_side(value):
    """Normaliza lado operacional de forma estrita."""

    if value is None:
        return None

    current = str(value).strip().upper()
    aliases = {
        "C": "COMPRADO",
        "COMPRA": "COMPRADO",
        "COMPRADO": "COMPRADO",
        "LONG": "COMPRADO",
        "V": "VENDIDO",
        "VENDA": "VENDIDO",
        "VENDIDO": "VENDIDO",
        "SHORT": "VENDIDO",
    }
    return aliases.get(current)


def _frente_48_get_spot_reference(payload):
    """Obtém preco de referencia do payload aceitando aliases controlados."""

    if not isinstance(payload, dict):
        return None

    for key in ("spot_ref", "underlying_price", "spot", "current_underlying_price"):
        if key in payload:
            return payload.get(key)

    return None


def _frente_48_get_legs(payload):
    """Obtém lista de legs do payload aceitando aliases controlados."""

    if not isinstance(payload, dict):
        return None

    for key in ("legs", "structure_legs", "payoff_legs"):
        if key in payload:
            return payload.get(key)

    return None


def _frente_48_validate_payoff_leg(leg, index=0):
    """Valida uma leg para cálculo de payoff sem executar cálculo financeiro."""

    errors = []
    warnings = []

    if not isinstance(leg, dict):
        return {
            "valid": False,
            "errors": [f"legs[{index}] deve ser dict"],
            "warnings": warnings,
            "normalized": None,
        }

    option_type = _frente_48_normalize_option_type(
        leg.get("option_type", leg.get("call_put", leg.get("tipo")))
    )
    position_side = _frente_48_normalize_position_side(
        leg.get("position_side", leg.get("side", leg.get("cv")))
    )

    symbol = leg.get("symbol", leg.get("ativo", leg.get("ticker")))
    strike = leg.get("strike")
    quantity = leg.get("quantity", leg.get("quant", leg.get("qty")))
    multiplier = leg.get("multiplier", 100.0)

    premium = leg.get("premium", leg.get("entry_premium"))
    current_price = leg.get("current_price")

    if option_type not in ("CALL", "PUT"):
        errors.append(f"legs[{index}].option_type invalido ou ausente")

    if position_side not in ("COMPRADO", "VENDIDO"):
        errors.append(f"legs[{index}].position_side invalido ou ausente")

    if not isinstance(symbol, str) or not symbol.strip():
        warnings.append(f"legs[{index}].symbol ausente ou vazio")

    if not _frente_48_positive_number(strike):
        errors.append(f"legs[{index}].strike deve ser numero positivo")

    if not _frente_48_positive_number(quantity):
        errors.append(f"legs[{index}].quantity deve ser numero positivo")

    if not _frente_48_positive_number(multiplier):
        errors.append(f"legs[{index}].multiplier deve ser numero positivo")

    if not _frente_48_optional_number(premium):
        errors.append(f"legs[{index}].premium deve ser numerico ou None")

    if not _frente_48_optional_number(current_price):
        errors.append(f"legs[{index}].current_price deve ser numerico ou None")

    normalized = {
        "option_type": option_type,
        "position_side": position_side,
        "symbol": symbol.strip().upper() if isinstance(symbol, str) else symbol,
        "strike": float(strike) if _frente_48_is_number(strike) else strike,
        "quantity": float(quantity) if _frente_48_is_number(quantity) else quantity,
        "multiplier": float(multiplier) if _frente_48_is_number(multiplier) else multiplier,
        "premium": premium,
        "current_price": current_price,
    }

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "normalized": normalized,
    }


def _frente_48_validate_payoff_calculation_request(payload):
    """Valida contrato mínimo de entrada para payoff.

    Esta função é controlada e local:
    - não persiste dados;
    - não altera schema;
    - não executa pricing/payoff;
    - não muda fluxo operacional amplo.

    Retorno estável:
    {
        "valid": bool,
        "status": "ok" | "error" | "warning",
        "error_message": str | None,
        "errors": list[str],
        "warnings": list[str],
        "normalized_payload": dict | None,
    }
    """

    errors = []
    warnings = []

    if not isinstance(payload, dict):
        return {
            "valid": False,
            "status": "error",
            "error_message": "payload deve ser dict",
            "errors": ["payload deve ser dict"],
            "warnings": [],
            "normalized_payload": None,
        }

    spot_ref = _frente_48_get_spot_reference(payload)
    legs = _frente_48_get_legs(payload)

    if not _frente_48_positive_number(spot_ref):
        errors.append("spot_ref/underlying_price deve ser numero positivo")

    if not isinstance(legs, list) or not legs:
        errors.append("legs deve ser lista nao vazia")
        leg_results = []
    else:
        leg_results = [
            _frente_48_validate_payoff_leg(leg, index=index)
            for index, leg in enumerate(legs)
        ]

        for result in leg_results:
            errors.extend(result["errors"])
            warnings.extend(result["warnings"])

    normalized_payload = dict(payload)
    normalized_payload["spot_ref"] = float(spot_ref) if _frente_48_is_number(spot_ref) else spot_ref
    normalized_payload["legs"] = [
        result["normalized"]
        for result in leg_results
        if result.get("normalized") is not None
    ]

    if errors:
        status = "error"
        error_message = "; ".join(errors)
    elif warnings:
        status = "warning"
        error_message = None
    else:
        status = "ok"
        error_message = None

    return {
        "valid": not errors,
        "status": status,
        "error_message": error_message,
        "errors": errors,
        "warnings": warnings,
        "normalized_payload": normalized_payload,
    }


def _frente_48_assert_valid_payoff_calculation_request(payload):
    """Valida payload e levanta ValueError em caso inválido.

    Helper explícito para usos futuros, sem acoplamento automático ao fluxo atual.
    """

    result = _frente_48_validate_payoff_calculation_request(payload)
    if not result["valid"]:
        raise ValueError(result["error_message"] or "payload de payoff invalido")
    return result
# [FRENTE 48] FIM - validacao controlada payoff calculation request
