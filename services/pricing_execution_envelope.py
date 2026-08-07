from __future__ import annotations

from copy import deepcopy
from typing import Any


ALLOWED_PRICING_EXECUTION_STATUSES = frozenset({"ok", "error", "warning"})

PRICING_EXECUTION_ENVELOPE_KEYS = (
    "status",
    "error_message",
    "pricing_payload",
    "engine_result",
    "persisted",
    "pricing_execution_id",
    "warnings",
    "metadata",
)


def _copy_mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return deepcopy(value)
    raise TypeError("expected dict or None")


def _copy_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return deepcopy(value)
    if isinstance(value, tuple):
        return list(deepcopy(value))
    raise TypeError("expected list, tuple or None")


def normalize_pricing_execution_status(
    status: str | None,
    *,
    error_message: str | None = None,
) -> str:
    normalized = (status or "").strip().lower()

    if not normalized:
        normalized = "error" if error_message else "ok"

    if normalized not in ALLOWED_PRICING_EXECUTION_STATUSES:
        raise ValueError(
            "invalid pricing execution status: "
            f"{status!r}. Expected one of: "
            f"{sorted(ALLOWED_PRICING_EXECUTION_STATUSES)!r}"
        )

    return normalized


def build_pricing_execution_envelope(
    *,
    status: str | None = "ok",
    error_message: str | None = None,
    pricing_payload: dict[str, Any] | None = None,
    engine_result: dict[str, Any] | None = None,
    persisted: dict[str, Any] | None = None,
    pricing_execution_id: int | str | None = None,
    warnings: list[Any] | tuple[Any, ...] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized_status = normalize_pricing_execution_status(
        status,
        error_message=error_message,
    )

    persisted_payload = _copy_mapping(persisted)
    persisted_payload.setdefault("record", None)
    persisted_payload.setdefault("snapshot_id", None)

    envelope = {
        "status": normalized_status,
        "error_message": error_message,
        "pricing_payload": _copy_mapping(pricing_payload),
        "engine_result": _copy_mapping(engine_result),
        "persisted": persisted_payload,
        "pricing_execution_id": pricing_execution_id,
        "warnings": _copy_list(warnings),
        "metadata": _copy_mapping(metadata),
    }

    return envelope


def is_pricing_execution_envelope(value: Any) -> bool:
    if not isinstance(value, dict):
        return False

    if tuple(value.keys()) != PRICING_EXECUTION_ENVELOPE_KEYS:
        return False

    status = value.get("status")
    if status not in ALLOWED_PRICING_EXECUTION_STATUSES:
        return False

    if not isinstance(value.get("pricing_payload"), dict):
        return False

    if not isinstance(value.get("engine_result"), dict):
        return False

    persisted = value.get("persisted")
    if not isinstance(persisted, dict):
        return False

    if "record" not in persisted:
        return False

    if "snapshot_id" not in persisted:
        return False

    if not isinstance(value.get("warnings"), list):
        return False

    if not isinstance(value.get("metadata"), dict):
        return False

    return True


def merge_pricing_execution_envelope(
    envelope: dict[str, Any],
    **updates: Any,
) -> dict[str, Any]:
    if not is_pricing_execution_envelope(envelope):
        raise ValueError("base value is not a pricing execution envelope")

    data = deepcopy(envelope)
    data.update(updates)

    rebuilt = build_pricing_execution_envelope(
        status=data.get("status"),
        error_message=data.get("error_message"),
        pricing_payload=data.get("pricing_payload"),
        engine_result=data.get("engine_result"),
        persisted=data.get("persisted"),
        pricing_execution_id=data.get("pricing_execution_id"),
        warnings=data.get("warnings"),
        metadata=data.get("metadata"),
    )

    return rebuilt
