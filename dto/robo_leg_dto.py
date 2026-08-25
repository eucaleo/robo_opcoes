from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class FonteType(str, Enum):
    MANUAL = "manual"
    RTD = "rtd"


class CVType(str, Enum):
    C = "C"
    V = "V"


class CallPutType(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


@dataclass(frozen=True)
class RoboLegDTO:
    aba: str
    timestamp: datetime
    cv: CVType | str
    call_put: CallPutType | str
    strike: float
    quant: int
    ativo: str
    vencimento: Optional[datetime]
    fonte: FonteType
    id: Optional[int] = None
    preco: Optional[float] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
