from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from dto.robo_leg_dto import FonteType


class DataFreshness(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    MISSING = "missing"


@dataclass(frozen=True)
class RoboLegsStatusDTO:
    aba: str
    requested_ts: datetime
    ttl: timedelta

    chosen_fonte: Optional[FonteType]
    chosen_ts: Optional[datetime]

    manual_latest_ts: Optional[datetime]
    rtd_latest_ts: Optional[datetime]

    freshness: DataFreshness
    reason: str
