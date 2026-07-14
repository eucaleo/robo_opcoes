from services.canonical_input_service import CanonicalInputService
from services.pricing_input_service import PricingInputService


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


class FakeStatus:
    def __init__(self, chosen_ts):
        self.chosen_ts = chosen_ts


class FakeRtdRoboLegsService:
    def status(self, aba, requested_timestamp):
        return FakeStatus("2026-05-18 10:00:00")

    def get_legs(self, aba, timestamp):
        return [
            {
                "cv": "C",
                "call_put": "C",
                "ativo": "bovae195",
                "strike": 195.0,
                "vencimento": "2026-05-15",
                "quant": 5000,
                "preco": 1.23,
                "multiplier": 1.0,
                "source": "rtd_option_quotes",
            }
        ]


def test_rtd_legacy_fallback_can_feed_pricing_payload_when_no_canonical_legs_exist():
    structure = {
        "id": 7,
        "name": "BOVA11 Condor Maio/2026",
        "underlying_asset": "BOVA11",
        "alias_legacy_aba": "BOVA11",
        "legs": [],
    }

    canonical_service = CanonicalInputService(
        repository=FakeRepository(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(),
        robo_legs_service=FakeRtdRoboLegsService(),
        prefer_canonical_legs=True,
        enable_legacy_legs_fallback=True,
    )

    canonical_input = canonical_service.build_structure_market_input(
        structure_id=7,
        reference_date="2026-05-18",
    )

    assert canonical_input["meta"]["legs_source"] == "legacy_fallback"
    assert canonical_input["meta"]["legacy_timestamp"] == "2026-05-18 10:00:00"
    assert canonical_input["meta"]["legacy_aba"] == "BOVA11"
    assert canonical_input["meta"]["legacy_key_source"] == "alias_legacy_aba"
    assert "alias_legacy_aba" not in canonical_input["structure"]

    canonical_leg = canonical_input["structure"]["legs"][0]
    assert canonical_leg["position_side"] == "COMPRADO"
    assert canonical_leg["option_type"] == "CALL"
    assert canonical_leg["symbol"] == "BOVAE195"

    pricing_service = PricingInputService(
        canonical_input_service=canonical_service,
    )

    pricing_payload = pricing_service.build_pricing_payload(
        structure_id=7,
        reference_date="2026-05-18",
    )

    assert pricing_payload["structure_id"] == 7
    assert pricing_payload["structure_name"] == "BOVA11 Condor Maio/2026"
    assert pricing_payload["underlying_asset"] == "BOVA11"
    assert pricing_payload["reference_date"] == "2026-05-18"
    assert pricing_payload["spot_price"] == 198.35
    assert "alias_legacy_aba" not in pricing_payload

    assert pricing_payload["legs"] == [
        {
            "side": "LONG",
            "instrument_type": "OPTION",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-05-15",
            "quantity": 5000,
            "premium": 1.23,
            "multiplier": 1.0,
        }
    ]
