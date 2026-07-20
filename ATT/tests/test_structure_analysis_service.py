import pytest

from services.structure_analysis_service import StructureAnalysisService


class FakeCanonicalInputService:
    def __init__(self, error=None):
        self.error = error
        self.calls = []

    def build_structure_market_input(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ):
        self.calls.append(
            {
                "structure_id": structure_id,
                "reference_date": reference_date,
            }
        )

        if self.error is not None:
            raise self.error

        return {
            "structure": {
                "structure_id": structure_id,
                "name": "BOVA11 Condor Maio/2026 - Atualizada",
                "underlying_asset": "BOVA11",
                "alias_legacy_aba": "BOVA11",
                "legs": [
                    {
                        "position_side": "LONG",
                        "option_type": "PUT",
                        "symbol": "BOVAM190",
                        "strike": 190.0,
                        "expiration_date": "2026-05-15",
                        "quantity": 2000,
                        "premium": None,
                        "multiplier": 1.0,
                    },
                    {
                        "position_side": "SHORT",
                        "option_type": "PUT",
                        "symbol": "BOVAM185",
                        "strike": 185.0,
                        "expiration_date": "2026-05-15",
                        "quantity": 2000,
                        "premium": None,
                        "multiplier": 1.0,
                    },
                ],
            },
            "market": {
                "reference_date": reference_date or "2026-05-15",
                "underlying_asset": "BOVA11",
                "spot_price": 198.35,
                "interest_rate": 0.1175,
                "volatility": 0.22,
            },
            "meta": {
                "reference_date": reference_date or "2026-05-15",
                "legs_source": "canonical",
                "legacy_aba": "BOVA11",
                "legacy_timestamp": None,
            },
        }


class FakeInvalidCanonicalInputService:
    def __init__(self):
        self.calls = []

    def build_structure_market_input(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ):
        self.calls.append(
            {
                "structure_id": structure_id,
                "reference_date": reference_date,
            }
        )

        return {
            "structure": {
                "structure_id": structure_id,
                "name": "Estrutura inválida",
                "underlying_asset": "BOVA11",
                "alias_legacy_aba": "BOVA11",
                "legs": [],
            },
            "market": {
                "reference_date": reference_date or "2026-05-15",
                "underlying_asset": "BOVA11",
                "spot_price": 198.35,
                "interest_rate": 0.1175,
                "volatility": 0.22,
            },
            "meta": {
                "reference_date": reference_date or "2026-05-15",
                "legs_source": "canonical",
                "legacy_aba": "BOVA11",
                "legacy_timestamp": None,
            },
        }


def test_structure_analysis_service_analyze_returns_full_pipeline():
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputService()
    )

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
        spread_pct_medio=0.02,
    )

    assert "canonical_input" in result
    assert "metrics" in result
    assert "payoff" in result
    assert "decision" in result

    assert result["canonical_input"]["structure"]["structure_id"] == 1
    assert result["canonical_input"]["market"]["reference_date"] == "2026-05-15"

    assert result["metrics"]["dte_min_inferred"] == 0
    assert result["metrics"]["dte_min_effective"] == 0
    assert result["metrics"]["spread_pct_medio"] == 0.02

    payoff = result["payoff"]
    assert payoff is not None
    assert payoff["pl_max"] == 10000.0
    assert payoff["spot_ref"] == 198.35
    assert "points" in payoff
    assert len(payoff["points"]) > 0

    decision = result["decision"]
    assert decision is not None
    assert decision["decision"] == "HOLD"
    assert decision["dte_min"] == 0
    assert "why" in decision
    assert "why_json" in decision
    assert isinstance(decision["why"], dict)
    assert "reasons" in decision["why"]
    assert "alternatives" in decision["why"]


def test_structure_analysis_service_analyze_uses_explicit_dte_min_over_inferred():
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputService()
    )

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
        dte_min=9,
        spread_pct_medio=0.02,
    )

    assert result["metrics"]["dte_min_inferred"] == 0
    assert result["metrics"]["dte_min_effective"] == 9
    assert result["decision"]["dte_min"] == 9


def test_structure_analysis_service_analyze_returns_structured_decision_for_invalid_payoff():
    service = StructureAnalysisService(
        canonical_input_service=FakeInvalidCanonicalInputService()
    )

    result = service.analyze(
        structure_id=999,
        reference_date="2026-05-15",
    )

    assert "payoff" in result
    assert "decision" in result
    assert result["decision"] is not None
    assert result["decision"]["decision"] == "HOLD"
    assert result["decision"]["level"] == 0
    assert result["decision"]["why"]["error"] == "payoff is required"
    assert "validation_errors" in result["decision"]["why"]


def test_structure_analysis_service_analyze_propagates_custom_thresholds_and_dte_gate():
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputService()
    )

    thresholds = {
        "watch": 0.10,
        "prepare": 0.20,
        "close": 0.30,
    }

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
        thresholds=thresholds,
        dte_gate=10,
    )

    decision = result["decision"]

    assert decision is not None
    assert "why" in decision
    assert decision["why"]["thresholds_used"] == thresholds
    assert decision["why"]["dte_gate"] == 10


def test_structure_analysis_service_analyze_propagates_spread_warning():
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputService()
    )

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
        spread_pct_medio=0.02,
    )

    assert any(
        "Spread alto" in alternative
        for alternative in result["decision"]["why"]["alternatives"]
    )


def test_structure_analysis_service_forwards_reference_date_to_canonical_service():
    fake_canonical_service = FakeCanonicalInputService()
    service = StructureAnalysisService(
        canonical_input_service=fake_canonical_service
    )

    service.analyze(
        structure_id=77,
        reference_date="2026-06-01",
    )

    assert fake_canonical_service.calls == [
        {
            "structure_id": 77,
            "reference_date": "2026-06-01",
        }
    ]


def test_structure_analysis_service_propagates_canonical_input_service_error():
    fake_canonical_service = FakeCanonicalInputService(
        error=ValueError("structure not found: 404")
    )
    service = StructureAnalysisService(
        canonical_input_service=fake_canonical_service
    )

    with pytest.raises(ValueError, match="structure not found: 404"):
        service.analyze(structure_id=404)


def test_structure_analysis_service_passes_effective_dte_to_decision(monkeypatch):
    fake_canonical_service = FakeCanonicalInputService()
    service = StructureAnalysisService(
        canonical_input_service=fake_canonical_service
    )

    captured = {}

    def fake_compute_dte_min_from_canonical_input(canonical_input):
        return 3

    def fake_compute_payoff_from_canonical_input(canonical_input):
        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}

    def fake_compute_decision_from_payoff(
        payoff,
        dte_min,
        spread_pct_medio,
        thresholds,
        dte_gate,
    ):
        captured["payoff"] = payoff
        captured["dte_min"] = dte_min
        captured["spread_pct_medio"] = spread_pct_medio
        captured["thresholds"] = thresholds
        captured["dte_gate"] = dte_gate
        return {
            "decision": "HOLD",
            "dte_min": dte_min,
            "why": {},
            "why_json": "{}",
        }

    monkeypatch.setattr(
        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
        fake_compute_dte_min_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_payoff_from_canonical_input",
        fake_compute_payoff_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_decision_from_payoff",
        fake_compute_decision_from_payoff,
    )

    result = service.analyze(
        structure_id=1,
        spread_pct_medio=0.015,
        thresholds={"watch": 0.1},
        dte_gate=5,
    )

    assert captured == {
        "payoff": {"pl_max": 1.0, "spot_ref": 198.35, "points": []},
        "dte_min": 3,
        "spread_pct_medio": 0.015,
        "thresholds": {"watch": 0.1},
        "dte_gate": 5,
    }
    assert result["metrics"]["dte_min_inferred"] == 3
    assert result["metrics"]["dte_min_effective"] == 3
    assert result["decision"]["dte_min"] == 3


def test_structure_analysis_service_uses_zero_when_inferred_dte_is_none(monkeypatch):
    fake_canonical_service = FakeCanonicalInputService()
    service = StructureAnalysisService(
        canonical_input_service=fake_canonical_service
    )

    def fake_compute_dte_min_from_canonical_input(canonical_input):
        return None

    def fake_compute_payoff_from_canonical_input(canonical_input):
        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}

    def fake_compute_decision_from_payoff(
        payoff,
        dte_min,
        spread_pct_medio,
        thresholds,
        dte_gate,
    ):
        return {
            "decision": "HOLD",
            "dte_min": dte_min,
            "why": {},
            "why_json": "{}",
        }

    monkeypatch.setattr(
        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
        fake_compute_dte_min_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_payoff_from_canonical_input",
        fake_compute_payoff_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_decision_from_payoff",
        fake_compute_decision_from_payoff,
    )

    result = service.analyze(structure_id=1)

    assert result["metrics"]["dte_min_inferred"] is None
    assert result["metrics"]["dte_min_effective"] == 0
    assert result["decision"]["dte_min"] == 0


def test_structure_analysis_service_explicit_dte_overrides_inferred_value(monkeypatch):
    fake_canonical_service = FakeCanonicalInputService()
    service = StructureAnalysisService(
        canonical_input_service=fake_canonical_service
    )

    captured = {}

    def fake_compute_dte_min_from_canonical_input(canonical_input):
        return 2

    def fake_compute_payoff_from_canonical_input(canonical_input):
        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}

    def fake_compute_decision_from_payoff(
        payoff,
        dte_min,
        spread_pct_medio,
        thresholds,
        dte_gate,
    ):
        captured["dte_min"] = dte_min
        return {
            "decision": "HOLD",
            "dte_min": dte_min,
            "why": {},
            "why_json": "{}",
        }

    monkeypatch.setattr(
        "services.structure_analysis_service.compute_dte_min_from_canonical_input",
        fake_compute_dte_min_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_payoff_from_canonical_input",
        fake_compute_payoff_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_decision_from_payoff",
        fake_compute_decision_from_payoff,
    )

    result = service.analyze(
        structure_id=1,
        dte_min=9,
    )

    assert captured["dte_min"] == 9
    assert result["metrics"]["dte_min_inferred"] == 2
    assert result["metrics"]["dte_min_effective"] == 9
    assert result["decision"]["dte_min"] == 9
class FakeCanonicalInputServiceWithMarketMetrics:
    def __init__(self):
        self.calls = []

    def build_structure_market_input(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ):
        self.calls.append(
            {
                "structure_id": structure_id,
                "reference_date": reference_date,
            }
        )

        return {
            "structure": {
                "structure_id": structure_id,
                "name": "BOVA11 Condor com Mercado",
                "underlying_asset": "BOVA11",
                "alias_legacy_aba": "BOVA11",
                "legs": [
                    {
                        "position_side": "LONG",
                        "option_type": "PUT",
                        "symbol": "BOVAM190",
                        "strike": 190.0,
                        "expiration_date": "2026-05-20",
                        "quantity": 10,
                        "execution_price": 1.00,
                        "bid": 1.20,
                        "ask": 1.40,
                        "delta": 0.40,
                        "gamma": 0.01,
                        "theta": -0.02,
                        "vega": 0.03,
                        "multiplier": 1.0,
                    },
                    {
                        "position_side": "SHORT",
                        "option_type": "PUT",
                        "symbol": "BOVAM185",
                        "strike": 185.0,
                        "expiration_date": "2026-05-17",
                        "quantity": 10,
                        "execution_price": 1.00,
                        "bid": 0.70,
                        "ask": 0.80,
                        "delta": 0.40,
                        "gamma": 0.01,
                        "theta": -0.02,
                        "vega": 0.03,
                        "multiplier": 1.0,
                    },
                ],
            },
            "market": {
                "reference_date": reference_date or "2026-05-15",
                "underlying_asset": "BOVA11",
                "spot_price": 198.35,
                "interest_rate": 0.1175,
                "volatility": 0.22,
            },
            "meta": {
                "reference_date": reference_date or "2026-05-15",
                "legs_source": "canonical",
                "legacy_aba": "BOVA11",
                "legacy_timestamp": None,
            },
        }


def test_structure_analysis_service_infers_spread_pct_medio_from_internal_metrics(monkeypatch):
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
    )

    captured = {}

    def fake_compute_payoff_from_canonical_input(canonical_input):
        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}

    def fake_compute_decision_from_payoff(
        payoff,
        dte_min,
        spread_pct_medio,
        thresholds,
        dte_gate,
    ):
        captured["spread_pct_medio"] = spread_pct_medio
        return {
            "decision": "HOLD",
            "dte_min": dte_min,
            "why": {},
            "why_json": "{}",
        }

    monkeypatch.setattr(
        "services.structure_analysis_service.compute_payoff_from_canonical_input",
        fake_compute_payoff_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_decision_from_payoff",
        fake_compute_decision_from_payoff,
    )

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
    )

    expected_spread_pct_medio = ((0.20 / 1.30) + (0.10 / 0.75)) / 2

    assert result["metrics"]["spread_pct_medio"] == pytest.approx(expected_spread_pct_medio)
    assert result["metrics"]["spread_pct_medio_inferred"] == pytest.approx(expected_spread_pct_medio)
    assert captured["spread_pct_medio"] == pytest.approx(expected_spread_pct_medio)


def test_structure_analysis_service_explicit_spread_pct_overrides_internal_metrics(monkeypatch):
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
    )

    captured = {}

    def fake_compute_payoff_from_canonical_input(canonical_input):
        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}

    def fake_compute_decision_from_payoff(
        payoff,
        dte_min,
        spread_pct_medio,
        thresholds,
        dte_gate,
    ):
        captured["spread_pct_medio"] = spread_pct_medio
        return {
            "decision": "HOLD",
            "dte_min": dte_min,
            "why": {},
            "why_json": "{}",
        }

    monkeypatch.setattr(
        "services.structure_analysis_service.compute_payoff_from_canonical_input",
        fake_compute_payoff_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_decision_from_payoff",
        fake_compute_decision_from_payoff,
    )

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
        spread_pct_medio=0.015,
    )

    expected_spread_pct_medio_inferred = ((0.20 / 1.30) + (0.10 / 0.75)) / 2

    assert result["metrics"]["spread_pct_medio"] == 0.015
    assert result["metrics"]["spread_pct_medio_inferred"] == pytest.approx(
        expected_spread_pct_medio_inferred
    )
    assert captured["spread_pct_medio"] == 0.015


def test_structure_analysis_service_exposes_internal_structure_metrics(monkeypatch):
    service = StructureAnalysisService(
        canonical_input_service=FakeCanonicalInputServiceWithMarketMetrics()
    )

    def fake_compute_payoff_from_canonical_input(canonical_input):
        return {"pl_max": 1.0, "spot_ref": 198.35, "points": []}

    def fake_compute_decision_from_payoff(
        payoff,
        dte_min,
        spread_pct_medio,
        thresholds,
        dte_gate,
    ):
        return {
            "decision": "HOLD",
            "dte_min": dte_min,
            "why": {},
            "why_json": "{}",
        }

    monkeypatch.setattr(
        "services.structure_analysis_service.compute_payoff_from_canonical_input",
        fake_compute_payoff_from_canonical_input,
    )
    monkeypatch.setattr(
        "services.structure_analysis_service.compute_decision_from_payoff",
        fake_compute_decision_from_payoff,
    )

    result = service.analyze(
        structure_id=1,
        reference_date="2026-05-15",
    )

    structure_metrics = result["metrics"]["structure_metrics"]

    assert structure_metrics["num_pernas"] == 2
    assert structure_metrics["pl_realista_total"] == pytest.approx(4.0)
    assert structure_metrics["delta_liq"] == pytest.approx(0.0)
    assert structure_metrics["gamma_liq"] == pytest.approx(0.0)
    assert structure_metrics["theta_liq"] == pytest.approx(0.0)
    assert structure_metrics["vega_liq"] == pytest.approx(0.0)
    assert structure_metrics["dte_min"] == 2
    assert len(structure_metrics["legs"]) == 2
