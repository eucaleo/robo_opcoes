# services/market_time.py
from datetime import datetime
from zoneinfo import ZoneInfo

B3_TIMEZONE = ZoneInfo("America/Sao_Paulo")


def now_b3() -> datetime:
    """Retorna o datetime atual no fuso oficial de Brasília/B3."""
    return datetime.now(B3_TIMEZONE)


def now_b3_iso(timespec: str = "microseconds") -> str:
    """Timestamp ISO-8601 com offset de Brasília/B3, ex: 2026-06-25T18:24:01.123456-03:00."""
    return now_b3().isoformat(timespec=timespec)


def now_b3_text() -> str:
    """Timestamp textual local para tabelas/scripts legados, ex: 2026-06-25 18:24:01."""
    return now_b3().strftime("%Y-%m-%d %H:%M:%S")
