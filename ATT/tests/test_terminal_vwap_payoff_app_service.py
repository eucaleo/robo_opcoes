import pytest

from services.terminal_vwap_payoff_app_service import TerminalVWAPPayoffAppService


class FakeStructureRepository:
    def __init__(self, structure):
        self.structure = structure
        self.calls = []

    def get_structure(self, structure_id):
        self.calls.append(structure_id)
        return self.structure


class FakeMarketSnapshotProvider:
    def __init__(self):
        self.calls = []

    def get_market_snapshot(self, structure_id, structure, reference_date=None):
        self.calls.append(
            {
                "structure_id": structure_id,
                "structure": structure,
                "reference_date": reference_date,
            }
        )
        return {
            "last_price": 110.0,
            "vwap": 100.0,
            "source": "fake_market",
        }


class FakePayoffProvider:
    def __init__(self):
        self.calls = []

    def compute_payoff(self, structure, market, reference_date=None):
        self.calls.append(
            {
                "structure": structure,
                "market": market,
                "reference_date": reference_date,
            }
        )
        return {
            "points": [
                {"spot": 90.0, "result": -100.0},
                {"spot": 100.0, "result": 0.0},
                {"spot": 110.0, "result": 100.0},
            ],
            "meta": {"source": "fake_payoff"},
        }


class FakeViewModelService:
    def __init__(self):
        self.calls = []

    def build(self, structure, market, payoff_points, payoff=None):
        self.calls.append(
            {
                "structure": structure,
                "market": market,
                "payoff_points": payoff_points,
                "payoff": payoff,
            }
        )
        return {
            "terminal": {
                "name": "ui-terminal-vwap-payoff",
                "ready": True,
            },
            "structure": structure,
            "market": market,
            "payoff": {
                "points_count": len(payoff_points),
            },
        }


class FakeLegacyNamedViewModelService:
    def build_terminal_vwap_payoff_viewmodel(
        self,
        structure,
        market_snapshot,
        payoff_points,
    ):
        return {
            "structure_id": structure["structure_id"],
            "vwap": market_snapshot["vwap"],
            "points_count": len(payoff_points),
        }


def _structure():
    return {
        "structure_id": 7,
        "name": "Estrutura BOVA11",
        "underlying_asset": "BOVA11",
        "legs": [
            {
                "position_side": "COMPRADO",
                "option_type": "CALL",
                "symbol": "BOVAE195",
                "strike": 195.0,
                "expiration_date": "2026-12-18",
                "quantity": 100,
                "premium": 1.25,
                "multiplier": 1.0,
                "leg_order": 1,
            }
        ],
    }


def test_build_for_structure_id_orchestrates_structure_market_payoff_and_viewmodel():
    structure_repo = FakeStructureRepository(_structure())
    market_provider = FakeMarketSnapshotProvider()
    payoff_provider = FakePayoffProvider()
    viewmodel_service = FakeViewModelService()

    service = TerminalVWAPPayoffAppService(
        structure_repository=structure_repo,
        market_snapshot_provider=market_provider,
        payoff_provider=payoff_provider,
        viewmodel_service=viewmodel_service,
    )

    result = service.build_for_structure_id(7, reference_date="2026-06-29")

    assert result["terminal"]["name"] == "ui-terminal-vwap-payoff"
    assert result["terminal"]["ready"] is True
    assert result["structure"]["structure_id"] == 7
    assert result["market"]["vwap"] == 100.0
    assert result["payoff"]["points_count"] == 3

    assert structure_repo.calls == [7]
    assert market_provider.calls[0]["structure_id"] == 7
    assert market_provider.calls[0]["reference_date"] == "2026-06-29"
    assert payoff_provider.calls[0]["market"]["source"] == "fake_market"

    vm_call = viewmodel_service.calls[0]
    assert vm_call["structure"]["underlying_asset"] == "BOVA11"
    assert len(vm_call["payoff_points"]) == 3
    assert vm_call["payoff"]["meta"]["source"] == "fake_payoff"


def test_build_for_structure_id_raises_when_structure_is_missing():
    service = TerminalVWAPPayoffAppService(
        structure_repository=FakeStructureRepository(None),
        market_snapshot_provider=FakeMarketSnapshotProvider(),
        payoff_provider=FakePayoffProvider(),
        viewmodel_service=FakeViewModelService(),
    )

    with pytest.raises(ValueError, match="structure not found: 404"):
        service.build_for_structure_id(404)


def test_build_for_structure_id_accepts_viewmodel_with_legacy_method_name():
    service = TerminalVWAPPayoffAppService(
        structure_repository=FakeStructureRepository(_structure()),
        market_snapshot_provider=FakeMarketSnapshotProvider(),
        payoff_provider=FakePayoffProvider(),
        viewmodel_service=FakeLegacyNamedViewModelService(),
    )

    result = service.build_for_structure_id(7)

    assert result == {
        "structure_id": 7,
        "vwap": 100.0,
        "points_count": 3,
    }


def test_build_for_structure_id_validates_structure_id():
    service = TerminalVWAPPayoffAppService(
        structure_repository=FakeStructureRepository(_structure()),
        viewmodel_service=FakeViewModelService(),
    )

    with pytest.raises(ValueError, match="structure_id must be positive integer"):
        service.build_for_structure_id(0)



def test_build_for_structure_id_uses_injected_rtd_enrichment_before_payoff():
    class FakeRtdLegEnrichmentService:
        def enrich_legs(self, legs, strict=False, apply_live_price=True):
            enriched = []
            for leg in legs:
                new_leg = dict(leg)
                new_leg["premium"] = 2.5
                new_leg["source"] = "rtd_option_quotes"
                new_leg["price_source"] = "rtd_option_quotes.ultimo_preco"
                enriched.append(new_leg)
            return enriched

    structure = {
        "structure_id": 8,
        "name": "Estrutura RTD",
        "underlying_asset": "BOVA11",
        "legs": [],
    }

    class RepoWithLegs(FakeStructureRepository):
        def get_structure_legs(self, structure_id):
            return [
                {
                    "symbol": "BOVAE195",
                    "position_side": "COMPRADO",
                    "option_type": "CALL",
                    "strike": 195.0,
                    "quantity": 100,
                    "premium": 1.25,
                    "multiplier": 1.0,
                }
            ]

    payoff_provider = FakePayoffProvider()
    viewmodel_service = FakeViewModelService()

    service = TerminalVWAPPayoffAppService(
        structure_repository=RepoWithLegs(structure),
        market_snapshot_provider=FakeMarketSnapshotProvider(),
        payoff_provider=payoff_provider,
        viewmodel_service=viewmodel_service,
        rtd_leg_enrichment_service=FakeRtdLegEnrichmentService(),
    )

    service.build_for_structure_id(8)

    payoff_leg = payoff_provider.calls[0]["structure"]["legs"][0]
    assert payoff_leg["premium"] == 2.5
    assert payoff_leg["source"] == "rtd_option_quotes"
    assert payoff_leg["price_source"] == "rtd_option_quotes.ultimo_preco"


def test_extract_payoff_points_normalizes_tuple_points_from_domain_payoff():
    points = TerminalVWAPPayoffAppService._extract_payoff_points(
        {
            "points": [
                (90.0, -100.0),
                (100.0, 0.0),
            ]
        }
    )

    assert points == [
        {
            "spot": 90.0,
            "pl": -100.0,
            "underlying_price": 90.0,
            "result": -100.0,
        },
        {
            "spot": 100.0,
            "pl": 0.0,
            "underlying_price": 100.0,
            "result": 0.0,
        },
    ]
