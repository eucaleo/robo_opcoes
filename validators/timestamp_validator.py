from __future__ import annotations

from datetime import timedelta


def validate_ttl(ttl: timedelta) -> None:
    if ttl.total_seconds() <= 0:
        raise ValueError("ttl must be > 0 seconds")
    if ttl.total_seconds() > 24 * 60 * 60:
        raise ValueError("ttl too large (max 24h)")
