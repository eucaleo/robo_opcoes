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

    # ──────────────────────────────────────────────────────────────────────
    # Estado efetivo da estrutura
    # ──────────────────────────────────────────────────────────────────────

    def apply_events_to_structure(
        self,
        structure: dict[str, Any],
        events: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Aplica eventos operacionais sobre uma estrutura e retorna uma cópia
        com quantidades efetivas nas legs.

        Regras:
        - Eventos cancelados são ignorados.
        - note, opening, adjustment e rollover não alteram quantidade.
        - partial_close reduz quantidade.
        - full_close zera a perna alvo ou a estrutura inteira.
        - manual_close reduz se quantity foi informado; senão zera.
        - assignment, exercise e expiration zeram a perna alvo ou estrutura.
        - Eventos legados roll/open/total_close são aceitos por compatibilidade.
        """
        if not isinstance(structure, dict):
            raise ValueError("structure must be a dict")

        structure_id = self._extract_structure_id(structure)

        if events is None:
            events = self.list_events_for_structure(
                structure_id=structure_id,
                include_cancelled=True,
            )

        effective = {
            **structure,
            "legs": [
                {
                    **leg,
                    "_original_quantity": self._extract_leg_quantity(leg),
                }
                for leg in (structure.get("legs") or [])
            ],
        }

        sorted_events = sorted(
            events or [],
            key=lambda event: (
                str(event.get("event_date") or ""),
                int(event.get("id") or 0),
            ),
        )

        applied_count = 0
        ignored_cancelled_count = 0

        for event in sorted_events:
            status = str(event.get("event_status", "registered")).strip().lower()

            if status == "cancelled":
                ignored_cancelled_count += 1
                continue

            event_type = str(event.get("event_type", "")).strip().lower()

            if event_type in {"note", "opening", "open", "adjustment", "rollover", "roll"}:
                applied_count += 1
                continue

            target_legs = self._target_legs_for_event(effective["legs"], event)

            if not target_legs:
                applied_count += 1
                continue

            if event_type == "partial_close":
                self._reduce_target_legs(target_legs, event.get("quantity"))
                applied_count += 1
                continue

            if event_type in {"full_close", "total_close"}:
                self._zero_target_legs(target_legs)
                applied_count += 1
                continue

            if event_type == "manual_close":
                if event.get("quantity") is None:
                    self._zero_target_legs(target_legs)
                else:
                    self._reduce_target_legs(target_legs, event.get("quantity"))
                applied_count += 1
                continue

            if event_type in {"assignment", "exercise", "expiration"}:
                self._zero_target_legs(target_legs)
                applied_count += 1
                continue

        all_closed = all(
            self._extract_leg_quantity(leg) == 0
            for leg in effective.get("legs", [])
        ) if effective.get("legs") else False

        effective["operational_state"] = {
            "events_applied": applied_count,
            "events_ignored_cancelled": ignored_cancelled_count,
            "is_closed": all_closed,
        }

        return effective

    def _extract_structure_id(self, structure: dict[str, Any]) -> int:
        raw = structure.get("id", structure.get("structure_id"))

        try:
            structure_id = int(raw)
        except Exception as exc:
            raise ValueError("structure_id is required to apply events") from exc

        if structure_id <= 0:
            raise ValueError("structure_id must be greater than zero")

        return structure_id

    def _extract_leg_quantity(self, leg: dict[str, Any]) -> int:
        raw = leg.get("quantity", leg.get("quant", 0))

        try:
            quantity = int(raw or 0)
        except Exception:
            return 0

        return max(quantity, 0)

    def _set_leg_quantity(self, leg: dict[str, Any], quantity: int) -> None:
        quantity = max(int(quantity), 0)

        if "quantity" in leg:
            leg["quantity"] = quantity
        elif "quant" in leg:
            leg["quant"] = quantity
        else:
            leg["quantity"] = quantity

        leg["operational_status"] = "closed" if quantity == 0 else "open"

    def _target_legs_for_event(
        self,
        legs: list[dict[str, Any]],
        event: dict[str, Any],
    ) -> list[dict[str, Any]]:
        leg_id = event.get("leg_id")
        symbol = self._normalize_optional_text(event.get("symbol"))

        if leg_id is None and symbol is None:
            return legs

        targets = []

        for leg in legs:
            if leg_id is not None:
                leg_raw_id = leg.get("id", leg.get("leg_id"))
                try:
                    if leg_raw_id is not None and int(leg_raw_id) == int(leg_id):
                        targets.append(leg)
                        continue
                except Exception:
                    pass

            if symbol is not None:
                leg_symbol = self._normalize_optional_text(leg.get("symbol"))
                if leg_symbol == symbol:
                    targets.append(leg)

        return targets

    def _reduce_target_legs(
        self,
        target_legs: list[dict[str, Any]],
        quantity: Any,
    ) -> None:
        if quantity is None:
            return

        try:
            quantity_to_reduce = int(quantity)
        except Exception as exc:
            raise ValueError("event quantity must be integer") from exc

        if quantity_to_reduce < 0:
            raise ValueError("event quantity must be greater than or equal to zero")

        for leg in target_legs:
            current_quantity = self._extract_leg_quantity(leg)
            self._set_leg_quantity(
                leg,
                max(current_quantity - quantity_to_reduce, 0),
            )

    def _zero_target_legs(self, target_legs: list[dict[str, Any]]) -> None:
        for leg in target_legs:
            self._set_leg_quantity(leg, 0)

