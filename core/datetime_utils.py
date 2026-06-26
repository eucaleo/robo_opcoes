from datetime import datetime
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("America/Sao_Paulo")


def now_local() -> datetime:
    """
    Retorna agora como datetime timezone-aware em America/Sao_Paulo.
    """
    return datetime.now(LOCAL_TZ)


def now_local_iso() -> str:
    """
    Retorna agora em ISO 8601 com offset explícito -03:00.
    """
    return now_local().isoformat()


def parse_datetime(value, assume_tz=LOCAL_TZ):
    """
    Normaliza valores de data/hora para datetime timezone-aware.

    Regras:
    - None/vazio -> None
    - datetime aware -> mantém
    - datetime naive -> assume America/Sao_Paulo
    - string com Z -> converte para +00:00
    - string ISO com +00:00 ou -03:00 -> respeita o offset
    - string ISO sem offset -> assume America/Sao_Paulo
    """
    if value in (None, ""):
        return None

    if isinstance(value, datetime):
        dt = value
    else:
        text = str(value).strip()
        if not text:
            return None

        if text.endswith("Z"):
            text = text[:-1] + "+00:00"

        try:
            dt = datetime.fromisoformat(text)
        except Exception:
            return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=assume_tz)

    return dt


def to_local_datetime(value):
    """
    Converte qualquer valor aceito por parse_datetime para America/Sao_Paulo.
    """
    dt = parse_datetime(value)
    if dt is None:
        return None
    return dt.astimezone(LOCAL_TZ)


def format_datetime_local(value, default="", fmt="%Y-%m-%d %H:%M:%S") -> str:
    """
    Formata data/hora sempre em America/Sao_Paulo.
    """
    dt = to_local_datetime(value)
    if dt is None:
        return default
    return dt.strftime(fmt)
