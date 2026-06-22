import services.canonical_pricing_facade as facade_module


class FakePricingInputService:
    def __init__(self, *args, **kwargs):
        pass

    def build_pricing_payload(self, structure_id: int, reference_date: str | None = None):
        return {
            "structure_id": structure_id,
            "underlying_asset": "BOVA11",
            "reference_date": reference_date,
            "spot_price": 124.66,
            "interest_rate": 0.0,
            "volatility": 0.0,
            "legs": [],
            "meta": {
                "source": "fake_pricing_input_service",
            },
        }


class FakePricingExecutionService:
    def execute_payload(self, pricing_payload):
        return {
            "result": {
                "engine": "fake",
                "status": "ok",
                "valuation": {
                    "theoretical_value": 0,
                },
            }
        }


class FakePersistenceService:
    def __init__(self):
        self.calls = []

    def persist_execution(
        self,
        pricing_payload,
        result,
        duration_ms=None,
        error_message=None,
    ):
        self.calls.append(
            {
                "pricing_payload": pricing_payload,
                "result": result,
                "duration_ms": duration_ms,
                "error_message": error_message,
            }
        )
        return {
            "ok": True,
            "structure_id": pricing_payload["structure_id"] if pricing_payload else None,
        }


def test_facade_falls_back_to_pricing_input_service_when_alias_legacy_aba_is_null(monkeypatch, tmp_path):
    def fake_get_structure_info(structure_id, db_path):
        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")

    monkeypatch.setattr(
        facade_module,
        "_get_structure_info",
        fake_get_structure_info,
    )

    monkeypatch.setattr(
        facade_module,
        "PricingInputService",
        FakePricingInputService,
    )

    persister = FakePersistenceService()

    db_path = tmp_path / "app.db"
    db_path.touch()

    facade = facade_module.CanonicalPricingFacade(
        db_path=db_path,
        pricing_execution_service=FakePricingExecutionService(),
        persistence_service=persister,
    )

    response = facade.execute_pricing(
        structure_id=2,
        reference_date="2026-06-21",
    )

    assert response["status"] == "ok"
    assert response["pricing_payload"]["structure_id"] == 2
    assert response["pricing_payload"]["reference_date"] == "2026-06-21"
    assert response["pricing_payload"]["meta"]["snapshot_source"] == "canonical_manual_without_alias"
    assert response["pricing_payload"]["meta"]["alias_legacy_aba"] is None
    assert "alias_legacy_aba is null" in response["pricing_payload"]["meta"]["fallback_reason"]

    assert len(persister.calls) == 1
    assert persister.calls[0]["pricing_payload"]["structure_id"] == 2
    assert persister.calls[0]["result"]["status"] == "ok"
