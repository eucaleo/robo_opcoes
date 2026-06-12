from __future__ import annotations

from datetime import datetime
from typing import Any

from repositories.structure_events_repository import StructureEventsRepository


class StructureEventsService:
    ALLOWED_EVENT_TYPES = {
        "opening",
        "adjustment",
        "rollover",
        "partial_close",
        "full_close",
        "manual_close",
        "note",
        "assignment",
        "exercise",
        "expiration",
    }

    ALLOWED_EVENT_STATUSES = {
        "registered",
        "confirmed",
        "cancelled",
    }

    ALLOWED_SOURCES = {
        "manual",
        "system",
        "import",
        "broker",
    }

    def __init__(
        self,
        structure_events_repository: StructureEventsRepository | None = None,
    ):
        self.structure_events_repository = (
            structure_events_repository or StructureEventsRepository()
        )

    def _validate_positive_int(self, value: int, field_name: str) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} must be greater than zero")

    def _validate_optional_positive_int(
        self,
        value: int | None,
        field_name: str,
    ) -> None:
        if value is not None:
            self._validate_positive_int(value, field_name)

    def _validate_event_type(self, event_type: str) -> None:
        if event_type not in self.ALLOWED_EVENT_TYPES:
            allowed = ", ".join(sorted(self.ALLOWED_EVENT_TYPES))
            raise ValueError(f"event_type must be one of: {allowed}")

    def _validate_event_status(self, event_status: str) -> None:
        if event_status not in self.ALLOWED_EVENT_STATUSES:
            allowed = ", ".join(sorted(self.ALLOWED_EVENT_STATUSES))
            raise ValueError(f"event_status must be one of: {allowed}")

    def _validate_source(self, source: str) -> None:
        if source not in self.ALLOWED_SOURCES:
            allowed = ", ".join(sorted(self.ALLOWED_SOURCES))
            raise ValueError(f"source must be one of: {allowed}")

    def _validate_event_date(self, event_date: str) -> None:
        if not isinstance(event_date, str) or not event_date.strip():
            raise ValueError("event_date must not be empty")

        try:
            datetime.strptime(event_date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("event_date must be in YYYY-MM-DD format") from exc

    def _validate_quantity(self, quantity: int | None) -> None:
        if quantity is None:
            return

        if not isinstance(quantity, int):
            raise ValueError("quantity must be an integer")

        if quantity < 0:
            raise ValueError("quantity must be greater than or equal to zero")

    def _validate_price(self, price: float | int | None) -> None:
        if price is None:
            return

        if not isinstance(price, int | float):
            raise ValueError("price must be numeric")

        if price < 0:
            raise ValueError("price must be greater than or equal to zero")

    def _normalize_optional_text(self, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = str(value).strip()
        return normalized or None

    def record_event(
        self,
        *,
        structure_id: int,
        event_type: str,
        event_date: str,
        leg_id: int | None = None,
        event_status: str = "registered",
        quantity: int | None = None,
        price: float | int | None = None,
        symbol: str | None = None,
        source: str = "manual",
        notes: str | None = None,
        metadata: dict[str, Any] | list[Any] | None = None,
    ) -> dict[str, Any]:
        self._validate_positive_int(structure_id, "structure_id")
        self._validate_optional_positive_int(leg_id, "leg_id")
        self._validate_event_type(event_type)
        self._validate_event_status(event_status)
        self._validate_event_date(event_date)
        self._validate_quantity(quantity)
        self._validate_price(price)
        self._validate_source(source)

        data = {
            "structure_id": structure_id,
            "leg_id": leg_id,
            "event_type": event_type,
            "event_status": event_status,
            "event_date": event_date,
            "quantity": quantity,
            "price": float(price) if price is not None else None,
            "symbol": self._normalize_optional_text(symbol),
            "source": source,
            "notes": self._normalize_optional_text(notes),
            "metadata": metadata,
        }

        return self.structure_events_repository.create_event(data)

    def register_opening(self, **kwargs) -> dict[str, Any]:
        return self.record_event(event_type="opening", **kwargs)

    def register_adjustment(self, **kwargs) -> dict[str, Any]:
        return self.record_event(event_type="adjustment", **kwargs)

    def register_rollover(self, **kwargs) -> dict[str, Any]:
        return self.record_event(event_type="rollover", **kwargs)

    def register_partial_close(self, **kwargs) -> dict[str, Any]:
        return self.record_event(event_type="partial_close", **kwargs)

    def register_full_close(self, **kwargs) -> dict[str, Any]:
        return self.record_event(event_type="full_close", **kwargs)

    def register_manual_close(
        self,
        *,
        structure_id: int,
        event_date: str,
        leg_id: int | None = None,
        quantity: int | None = None,
        price: float | int | None = None,
        symbol: str | None = None,
        notes: str | None = None,
        metadata: dict[str, Any] | list[Any] | None = None,
    ) -> dict[str, Any]:
        return self.record_event(
            structure_id=structure_id,
            leg_id=leg_id,
            event_type="manual_close",
            event_date=event_date,
            quantity=quantity,
            price=price,
            symbol=symbol,
            source="manual",
            notes=notes,
            metadata=metadata,
        )

    def register_note(
        self,
        *,
        structure_id: int,
        event_date: str,
        notes: str,
        source: str = "manual",
        metadata: dict[str, Any] | list[Any] | None = None,
    ) -> dict[str, Any]:
        if not isinstance(notes, str) or not notes.strip():
            raise ValueError("notes must not be empty")

        return self.record_event(
            structure_id=structure_id,
            event_type="note",
            event_date=event_date,
            source=source,
            notes=notes,
            metadata=metadata,
        )

    def cancel_event(
        self,
        event_id: int,
        notes: str | None = None,
    ) -> dict[str, Any]:
        self._validate_positive_int(event_id, "event_id")
        return self.structure_events_repository.cancel_event(
            event_id=event_id,
            notes=self._normalize_optional_text(notes),
        )

    def get_event(self, event_id: int) -> dict[str, Any] | None:
        self._validate_positive_int(event_id, "event_id")
        return self.structure_events_repository.get_event(event_id)

    def list_events(
        self,
        *,
        structure_id: int | None = None,
        event_type: str | None = None,
        event_status: str | None = None,
        include_cancelled: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        self._validate_optional_positive_int(structure_id, "structure_id")

        if event_type is not None:
            self._validate_event_type(event_type)

        if event_status is not None:
            self._validate_event_status(event_status)

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        if offset < 0:
            raise ValueError("offset must be greater than or equal to zero")

        return self.structure_events_repository.list_events(
            structure_id=structure_id,
            event_type=event_type,
            event_status=event_status,
            include_cancelled=include_cancelled,
            limit=limit,
            offset=offset,
        )

    def list_events_for_structure(
        self,
        structure_id: int,
        include_cancelled: bool = False,
    ) -> list[dict[str, Any]]:
        self._validate_positive_int(structure_id, "structure_id")
        return self.structure_events_repository.list_events_for_structure(
            structure_id=structure_id,
            include_cancelled=include_cancelled,
        )

    def count_events(
        self,
        *,
        structure_id: int | None = None,
        event_type: str | None = None,
        include_cancelled: bool = False,
    ) -> int:
        self._validate_optional_positive_int(structure_id, "structure_id")

        if event_type is not None:
            self._validate_event_type(event_type)

        return self.structure_events_repository.count_events(
            structure_id=structure_id,
            event_type=event_type,
            include_cancelled=include_cancelled,
        )
