from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class CallPutType(Enum):
    CALL = "CALL"
    PUT = "PUT"


class CVType(Enum):
    C = "C"  # Compra
    V = "V"  # Venda


class FonteType(Enum):
    MANUAL = "manual"
    RTD = "rtd"


@dataclass
class RoboLegDTO:
    aba: str
    timestamp: datetime
    cv: CVType
    call_put: CallPutType
    strike: float
    quant: int
    ativo: str
    vencimento: datetime
    fonte: FonteType

    # Campos opcionais
    id: Optional[int] = None
    preco: Optional[float] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not str(self.aba).strip():
            raise ValueError("Aba não pode estar vazia")

        if not str(self.ativo).strip():
            raise ValueError("Ativo não pode estar vazio")

        if self.quant <= 0:
            raise ValueError("Quantidade deve ser positiva")

        if self.strike <= 0:
            raise ValueError("Strike deve ser positivo")

        if self.vencimento is None:
            raise ValueError("Vencimento não pode ser nulo")

        if self.vencimento <= self.timestamp:
            raise ValueError("Vencimento deve ser posterior ao timestamp")
