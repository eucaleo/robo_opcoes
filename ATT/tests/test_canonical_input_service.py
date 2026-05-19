import unittest
from unittest.mock import patch

from services.canonical_input_service import CanonicalInputService


class FakeRepository:
    def __init__(self, structure):
        self.structure = structure

    def get_structure(self, structure_id):
        if self.structure and self.structure.get("id") == structure_id:
            return self.structure
        return None


class FakeMarketSnapshotProvider:
    def get_snapshot(self, underlying_asset, reference_date=None):
        return {
            "reference_date": reference_date or "2026-05-18",
            "underlying_asset": underlying_asset,
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        }


class FakeRoboRepo:
    def __init__(self, timestamps):
        self._timestamps = timestamps

    def list_timestamps(self, aba):
        return self._timestamps


class FakeRoboLegsService:
    def __init__(self, timestamps=None, legs=None):
        self.repo = FakeRoboRepo(timestamps or [])
        self._legs = legs or []

    def get_legs(self, aba, timestamp, validate=False):
        return self._legs


class CanonicalInputServiceTests(unittest.TestCase):
    def test_should_always_prefer_canonical_legs_when_structure_already_has_legs(self):
        structure = {
            "id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "legs": [
                {
                    "position_side": "LONG",
                    "option_type": "CALL",
                    "symbol": "BOVAE195",
                    "strike": 195.0,
                    "expiration_date": "2026-05-15",
                    "quantity": 5000,
                    "premium": None,
                    "multiplier": 1.0,
                }
            ],
        }

        service = CanonicalInputService(
            repository=FakeRepository(structure),
            market_snapshot_provider=FakeMarketSnapshotProvider(),
            robo_legs_service=FakeRoboLegsService(
                timestamps=["2026-05-18 10:00:00"],
                legs=[{"any": "value"}],
            ),
            prefer_canonical_legs=False,
            enable_legacy_legs_fallback=True,
        )

        result = service.build_structure_market_input(
            structure_id=7,
            reference_date="2026-05-18",
        )

        self.assertEqual(result["meta"]["legs_source"], "canonical")
        self.assertNotIn("legacy_timestamp", result["meta"])
        self.assertEqual(len(result["structure"]["legs"]), 1)
        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
        self.assertNotIn("alias_legacy_aba", result["structure"])

    @patch("services.legacy_robo_legs_fallback.to_canonical_leg")
    def test_should_use_legacy_robo_only_when_no_canonical_legs_exist(self, mock_to_canonical_leg):
        structure = {
            "id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "legs": [],
        }

        mock_to_canonical_leg.return_value = {
            "position_side": "LONG",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-05-15",
            "quantity": 5000,
            "premium": None,
            "multiplier": 1.0,
        }

        service = CanonicalInputService(
            repository=FakeRepository(structure),
            market_snapshot_provider=FakeMarketSnapshotProvider(),
            robo_legs_service=FakeRoboLegsService(
                timestamps=["2026-05-18 10:00:00"],
                legs=[{"legacy": "raw-leg"}],
            ),
            enable_legacy_legs_fallback=True,
        )

        result = service.build_structure_market_input(
            structure_id=7,
            reference_date="2026-05-18",
        )

        self.assertEqual(result["meta"]["legs_source"], "legacy_robo")
        self.assertEqual(result["meta"]["legacy_timestamp"], "2026-05-18 10:00:00")
        self.assertEqual(len(result["structure"]["legs"]), 1)
        self.assertEqual(result["structure"]["legs"][0]["symbol"], "BOVAE195")
        self.assertNotIn("alias_legacy_aba", result["structure"])

    def test_should_return_empty_when_no_canonical_legs_and_fallback_disabled(self):
        structure = {
            "id": 7,
            "name": "BOVA11 Condor Maio/2026",
            "underlying_asset": "BOVA11",
            "alias_legacy_aba": "BOVA11",
            "legs": [],
        }

        service = CanonicalInputService(
            repository=FakeRepository(structure),
            market_snapshot_provider=FakeMarketSnapshotProvider(),
            robo_legs_service=FakeRoboLegsService(
                timestamps=["2026-05-18 10:00:00"],
                legs=[],
            ),
            enable_legacy_legs_fallback=False,
        )

        result = service.build_structure_market_input(
            structure_id=7,
            reference_date="2026-05-18",
        )

        self.assertEqual(result["meta"]["legs_source"], "empty")
        self.assertNotIn("legacy_timestamp", result["meta"])
        self.assertEqual(result["structure"]["legs"], [])
        self.assertNotIn("alias_legacy_aba", result["structure"])


if __name__ == "__main__":
    unittest.main()
