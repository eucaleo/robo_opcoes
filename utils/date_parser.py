from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Any


_EXCEL_EPOCH = datetime(1899, 12, 30)


def _is_blank(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    return False


def _excel_serial_to_datetime(value: float) -> datetime | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None

    if numeric <= 0:
        return None

    return _EXCEL_EPOCH + timedelta(days=numeric)


def _parse_numeric_string(value: str) -> float | None:
    text = value.strip()

    if not re_fullmatch_number(text):
        return None

    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def re_fullmatch_number(value: str) -> bool:
    if not value:
        return False

    normalized = value.replace(",", ".")
    if normalized.count(".") > 1:
        return False

    if normalized.startswith(("+", "-")):
        normalized = normalized[1:]

    if not normalized:
        return False

    return all(ch.isdigit() or ch == "." for ch in normalized)


def parse_excel_date_to_iso(value: Any) -> str | None:
    """Converte datas Excel, datas Python e strings comuns para YYYY-MM-DD.

    Contrato local:
    - vazio ou invalido retorna None;
    - serial Excel usa epoch 1899-12-30;
    - datetime/date Python retorna somente a data;
    - aceita ISO, dd/mm/YYYY, dd-mm-YYYY, YYYY/mm/dd.
    """

    if _is_blank(value):
        return None

    if isinstance(value, datetime):
        return value.date().isoformat()

    if isinstance(value, date):
        return value.isoformat()

    if isinstance(value, (int, float)):
        parsed = _excel_serial_to_datetime(float(value))
        return parsed.date().isoformat() if parsed else None

    if isinstance(value, str):
        text = value.strip()

        numeric = _parse_numeric_string(text)
        if numeric is not None:
            parsed = _excel_serial_to_datetime(numeric)
            return parsed.date().isoformat() if parsed else None

        iso_text = text.replace("Z", "+00:00")

        try:
            return date.fromisoformat(iso_text[:10]).isoformat()
        except ValueError:
            pass

        try:
            return datetime.fromisoformat(iso_text).date().isoformat()
        except ValueError:
            pass

        for fmt in (
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%d/%m/%y",
            "%d-%m-%y",
        ):
            try:
                return datetime.strptime(text, fmt).date().isoformat()
            except ValueError:
                continue

    return None


def parse_datetime_to_iso(value: Any) -> str | None:
    """Converte datetime, data, serial Excel ou string para ISO datetime.

    Contrato local:
    - vazio ou invalido retorna None;
    - datetime preserva timezone quando informado;
    - date vira meia-noite;
    - serial Excel com fracao preserva hora;
    - strings ISO com timezone sao aceitas.
    """

    if _is_blank(value):
        return None

    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")

    if isinstance(value, date):
        return datetime.combine(value, time.min).isoformat(timespec="seconds")

    if isinstance(value, (int, float)):
        parsed = _excel_serial_to_datetime(float(value))
        return parsed.isoformat(timespec="seconds") if parsed else None

    if isinstance(value, str):
        text = value.strip()

        numeric = _parse_numeric_string(text)
        if numeric is not None:
            parsed = _excel_serial_to_datetime(numeric)
            return parsed.isoformat(timespec="seconds") if parsed else None

        iso_text = text.replace("Z", "+00:00")

        try:
            return datetime.fromisoformat(iso_text).isoformat(timespec="seconds")
        except ValueError:
            pass

        try:
            parsed_date = date.fromisoformat(iso_text[:10])
            return datetime.combine(parsed_date, time.min).isoformat(timespec="seconds")
        except ValueError:
            pass

        for fmt in (
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y %H:%M",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ):
            try:
                return datetime.strptime(text, fmt).isoformat(timespec="seconds")
            except ValueError:
                continue

    return None


__all__ = [
    "parse_excel_date_to_iso",
    "parse_datetime_to_iso",
]
