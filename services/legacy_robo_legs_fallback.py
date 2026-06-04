from src.domain.refs.structure_ref import StructureRef
from typing import Any


class LegacyRoboLegsFallback:
    def __init__(
        self,
        robo_legs_service: Any | None = None,
        allow_name_fallback: bool = False,
    ):
        self.robo_legs_service = robo_legs_service
        self.allow_name_fallback = allow_name_fallback

    def load(
        self,
        structure: dict[str, Any],
        reference_date: str | None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        legacy_aba, key_source, fallback_reason = self._resolve_legacy_aba(structure)

        if not legacy_aba:
            return [], {
                "legs_source": "empty",
                "legacy_timestamp": None,
                "legacy_aba": None,
                "legacy_key_source": key_source,
                "fallback_reason": fallback_reason or "missing_legacy_key",
            }

        if self.robo_legs_service is None:
            return [], {
                "legs_source": "empty",
                "legacy_timestamp": None,
                "legacy_aba": legacy_aba,
                "legacy_key_source": key_source,
                "fallback_reason": "robo_legs_service_unavailable",
            }

        legacy_timestamp = self._resolve_reference_timestamp(
            aba=legacy_aba,
            reference_date=reference_date,
        )

        if legacy_timestamp is None:
            return [], {
                "legs_source": "empty",
                "legacy_timestamp": None,
                "legacy_aba": legacy_aba,
                "legacy_key_source": key_source,
                "fallback_reason": "no_legacy_timestamp_available",
            }

        legacy_legs = self._load_legacy_legs(
            aba=legacy_aba,
            reference_timestamp=legacy_timestamp,
        )

        if not legacy_legs:
            return [], {
                "legs_source": "empty",
                "legacy_timestamp": str(legacy_timestamp),
                "legacy_aba": legacy_aba,
                "legacy_key_source": key_source,
                "fallback_reason": "no_legacy_legs_found",
            }

        canonical_legs = []
        for leg in legacy_legs:
            adapted = self._adapt_legacy_leg_to_canonical(leg)
            if adapted:
                canonical_legs.append(adapted)

        if not canonical_legs:
            return [], {
                "legs_source": "empty",
                "legacy_timestamp": str(legacy_timestamp),
                "legacy_aba": legacy_aba,
                "legacy_key_source": key_source,
                "fallback_reason": "legacy_legs_not_convertible",
            }

        return canonical_legs, {
            "legs_source": "legacy_fallback",
            "legacy_timestamp": str(legacy_timestamp),
            "legacy_aba": legacy_aba,
            "legacy_key_source": key_source,
            "fallback_reason": fallback_reason,
        }

    def _resolve_legacy_aba(
        self,
        structure: dict[str, Any],
    ) -> tuple[str | None, str | None, str | None]:
        alias_legacy_aba = self._clean_text(structure.get("alias_legacy_aba"))
        if alias_legacy_aba:
            return alias_legacy_aba, "alias_legacy_aba", None

        structure_name = self._clean_text(structure.get("name"))
        if structure_name and self.allow_name_fallback:
            return structure_name, "structure_name_fallback", "alias_missing_name_fallback_used"

        if structure_name and not self.allow_name_fallback:
            return None, "name_fallback_disabled", "alias_missing_name_fallback_disabled"

        return None, "missing", "alias_and_name_missing"

    def _resolve_reference_timestamp(
        self,
        aba: str,
        reference_date: str | None,
    ) -> Any | None:
        if self.robo_legs_service is None:
            return None

        candidate_methods = [
            "resolve_reference_timestamp",
            "get_reference_timestamp",
            "find_reference_timestamp",
            "get_latest_timestamp",
            "latest_timestamp",
        ]

        for method_name in candidate_methods:
            method = getattr(self.robo_legs_service, method_name, None)
            if callable(method):
                try:
                    return method(aba=aba, reference_date=reference_date)
                except TypeError:
                    try:
                        return method(aba, reference_date)
                    except Exception:
                        continue
                except Exception:
                    continue

        candidate_status_methods = [
            "status",
            "get_status",
        ]

        for method_name in candidate_status_methods:
            method = getattr(self.robo_legs_service, method_name, None)
            if callable(method):
                try:
                    status = method(aba=aba, requested_timestamp=reference_date)
                except TypeError:
                    try:
                        status = method(aba, reference_date)
                    except Exception:
                        continue
                except Exception:
                    continue

                chosen_ts = getattr(status, "chosen_ts", None)
                if chosen_ts is not None:
                    return chosen_ts

                if isinstance(status, dict):
                    if status.get("chosen_ts") is not None:
                        return status.get("chosen_ts")
                    if status.get("timestamp") is not None:
                        return status.get("timestamp")

        return None

    def _load_legacy_legs(
        self,
        aba: str,
        reference_timestamp: Any,
    ) -> list[Any]:
        if self.robo_legs_service is None:
            return []

        candidate_methods = [
            "get_legs",
            "load_legs",
            "fetch_legs",
            "read_legs",
        ]

        for method_name in candidate_methods:
            method = getattr(self.robo_legs_service, method_name, None)
            if callable(method):
                try:
                    result = method(aba=aba, timestamp=reference_timestamp)
                except TypeError:
                    try:
                        result = method(aba, reference_timestamp)
                    except Exception:
                        continue
                except Exception:
                    continue

                if result:
                    return list(result)

        return []

    def _adapt_legacy_leg_to_canonical(
        self,
        leg: Any,
    ) -> dict[str, Any] | None:
        data = self._to_dict(leg)
        if not data:
            return None

        position_side = self._normalize_position_side(
            data.get("cv") or data.get("position_side") or data.get("side")
        )
        option_type = self._normalize_option_type(
            data.get("call_put") or data.get("option_type")
        )

        expiration_date = (
            data.get("expiration_date")
            or data.get("vencimento")
            or data.get("expiry")
            or data.get("expiracao")
        )

        if expiration_date is not None:
            expiration_date = str(expiration_date)

        return {
            "position_side": position_side,
            "option_type": option_type,
            "symbol": self._clean_upper_text(
                data.get("ativo") or data.get("symbol") or data.get("ticker")
            ),
            "strike": float(data.get("strike") or 0.0),
            "expiration_date": expiration_date,
            "quantity": int(data.get("quant") or data.get("quantity") or 0),
            "premium": float(data["preco"]) if data.get("preco") is not None else (
                float(data["premium"]) if data.get("premium") is not None else None
            ),
            "multiplier": float(data.get("multiplier") or 1.0),
        }

    def _to_dict(self, value: Any) -> dict[str, Any]:
        if value is None:
            return {}

        if isinstance(value, dict):
            return value

        if hasattr(value, "__dict__"):
            return {
                key: val
                for key, val in vars(value).items()
                if not key.startswith("_")
            }

        return {}

    def _normalize_position_side(self, value: Any) -> str:
        text = self._clean_upper_text(value) or ""
        if text in {"C", "BUY", "LONG", "COMPRA", "COMPRADO"}:
            return "LONG"
        return "SHORT"

    def _normalize_option_type(self, value: Any) -> str:
        text = self._clean_upper_text(value) or ""
        if text in {"C", "CALL"}:
            return "CALL"
        return "PUT"

    def _clean_text(self, value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def _clean_upper_text(self, value: Any) -> str | None:
        text = self._clean_text(value)
        return text.upper() if text is not None else None
