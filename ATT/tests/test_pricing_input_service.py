import pytest

from services.pricing_input_service import PricingInputService


class FakeCanonicalInputService:
    def __init__(self, canonical_input=None, error=None):
        self.canonical_input = canonical_input
        self.error = error
        self.calls = []

    def build_structure_market_input(self, structure_id: int, reference_date: str | None = None):
        self.calls.append(
            {
                "structure_id": structure_id,
                "reference_date": reference_date,
            }
        )

        if self.error is not None:
            raise self.error

        return self.canonical_input


def test_build_pricing_payload_calls_canonical_input_service(monkeypatch):
    canonical_input = {
        "structure": {
            "structure_id": 123,
            "name": "Fence BOVA11",
            "underlying_asset": "BOVA11",
            "legs": [],
        },
        "market": {
            "reference_date": "2026-05-16",
            "underlying_asset": "BOVA11",
            "spot_price": 198.35,
            "interest_rate": 0.1175,
            "volatility": 0.22,
        },
    }

    fake_canonical_service = FakeCanonicalInputService(canonical_input)

    def fake_to_pricing_payload(value):
        return {
            "structure_id": value["structure"]["structure_id"],
            "reference_date": value["market"]["reference_date"],
            "payload_source": "fake_adapter",
        }

    monkeypatch.setattr(
        "services.pricing_input_service.to_pricing_payload",
        fake_to_pricing_payload,
    )

    service = PricingInputService(canonical_input_service=fake_canonical_service)

    result = service.build_pricing_payload(
        structure_id=123,
        reference_date="2026-05-16",
    )

    assert fake_canonical_service.calls == [
        {
            "structure_id": 123,
            "reference_date": "2026-05-16",
        }
    ]
    assert result == {
        "structure_id": 123,
        "reference_date": "2026-05-16",
        "payload_source": "fake_adapter",
    }


def test_build_pricing_payload_from_canonical_input_delegates_to_adapter(monkeypatch):
    canonical_input = {
        "structure": {"structure_id": 999},
        "market": {"reference_date": "2026-05-17"},
    }

    calls = []

    def fake_to_pricing_payload(value):
        calls.append(value)
        return {"ok": True, "structure_id": 999}

    monkeypatch.setattr(
        "services.pricing_input_service.to_pricing_payload",
        fake_to_pricing_payload,
    )

    service = PricingInputService(canonical_input_service=None)

    result = service.build_pricing_payload_from_canonical_input(canonical_input)

    assert calls == [canonical_input]
    assert result == {"ok": True, "structure_id": 999}


def test_build_pricing_payload_passes_none_reference_date(monkeypatch):
    canonical_input = {
        "structure": {"structure_id": 321},
        "market": {"reference_date": "2026-05-18"},
    }

    fake_canonical_service = FakeCanonicalInputService(canonical_input)

    def fake_to_pricing_payload(value):
        return {
            "structure_id": value["structure"]["structure_id"],
            "reference_date": value["market"]["reference_date"],
        }

    monkeypatch.setattr(
        "services.pricing_input_service.to_pricing_payload",
        fake_to_pricing_payload,
    )

    service = PricingInputService(canonical_input_service=fake_canonical_service)

    result = service.build_pricing_payload(structure_id=321)

    assert fake_canonical_service.calls == [
        {
            "structure_id": 321,
            "reference_date": None,
        }
    ]
    assert result == {
        "structure_id": 321,
        "reference_date": "2026-05-18",
    }


def test_build_pricing_payload_propagates_canonical_input_service_error(monkeypatch):
    fake_canonical_service = FakeCanonicalInputService(
        error=ValueError("structure not found: 404")
    )

    adapter_calls = []

    def fake_to_pricing_payload(value):
        adapter_calls.append(value)
        return {"should_not_happen": True}

    monkeypatch.setattr(
        "services.pricing_input_service.to_pricing_payload",
        fake_to_pricing_payload,
    )

    service = PricingInputService(canonical_input_service=fake_canonical_service)

    with pytest.raises(ValueError, match="structure not found: 404"):
        service.build_pricing_payload(structure_id=404)

    assert fake_canonical_service.calls == [
        {
            "structure_id": 404,
            "reference_date": None,
        }
    ]
    assert adapter_calls == []


def test_build_pricing_payload_from_canonical_input_propagates_adapter_error(monkeypatch):
    canonical_input = {
        "structure": {"structure_id": 888},
        "market": {"reference_date": "2026-05-19"},
    }

    def fake_to_pricing_payload(value):
        raise ValueError("invalid canonical input")

    monkeypatch.setattr(
        "services.pricing_input_service.to_pricing_payload",
        fake_to_pricing_payload,
    )

    service = PricingInputService(canonical_input_service=None)

    with pytest.raises(ValueError, match="invalid canonical input"):
        service.build_pricing_payload_from_canonical_input(canonical_input)
