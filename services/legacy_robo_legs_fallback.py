from typing import Any

from services.robo_leg_mapper import to_canonical_leg


class LegacyRoboLegsFallback:
    def __init__(self, robo_legs_service: Any | None = None):
        self.robo_legs_service = robo_legs_service

    def load(
        self,
        structure: dict[str, Any],
        reference_date: str | None = None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        if self.robo_legs_service is None:
            return [], {"legs_source": "empty"}

        legacy_key = self._resolve_legacy_key(structure)
        if not legacy_key:
            return [], {"legs_source": "empty"}

        selected_timestamp = self._select_legacy_timestamp(
            aba=legacy_key,
            reference_date=reference_date,
        )

        if not selected_timestamp:
            return [], {"legs_source": "empty"}

        try:
            robo_legs = self.robo_legs_service.get_legs(
                aba=legacy_key,
                timestamp=selected_timestamp,
                validate=False,
            )
        except Exception:
            robo_legs = []

        canonical_robo_legs = []
        for leg in robo_legs:
            try:
                canonical_leg = to_canonical_leg(leg)
                if canonical_leg.get("expiration_date") is None:
                    continue
                canonical_robo_legs.append(canonical_leg)
            except Exception:
                continue

        if not canonical_robo_legs:
            return [], {"legs_source": "empty"}

        return canonical_robo_legs, {
            "legs_source": "legacy_robo",
            "legacy_timestamp": selected_timestamp,
        }

    def _resolve_legacy_key(self, structure: dict[str, Any]) -> str | None:
        alias_legacy_aba = self._clean_text(structure.get("alias_legacy_aba"))
        if alias_legacy_aba:
            return alias_legacy_aba

        return self._clean_text(structure.get("name"))

    def _select_legacy_timestamp(
        self,
        aba: str,
        reference_date: str | None = None,
    ) -> str | None:
        try:
            timestamps = self.robo_legs_service.repo.list_timestamps(aba)
        except Exception:
            timestamps = []

        if not timestamps:
            return None

        normalized = [str(ts) for ts in timestamps if ts]
        if not normalized:
            return None

        if reference_date:
            exact_prefix_matches = [ts for ts in normalized if ts.startswith(reference_date)]
            if exact_prefix_matches:
                return sorted(exact_prefix_matches)[-1]

        return sorted(normalized)[-1]

    def _clean_text(self, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value
