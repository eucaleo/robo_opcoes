from datetime import datetime
from types import SimpleNamespace

import pytest
import services.robo_legs_service as robo_legs_service
from dto.robo_leg_dto import RoboLegDTO, CVType, CallPutType, FonteType
from services.robo_legs_service import LegValidationError, RoboLegsService


class FakeValidRepo:
    def get_legs(self, aba, timestamp):
        return [
            RoboLegDTO(
                aba="TESTE",
                timestamp=datetime(2025, 1, 10, 10, 0, 0),
                ativo="PETR4",
                vencimento=datetime(2025, 2, 10, 10, 0, 0),
                strike=30.0,
                quant=1,
                cv=CVType.C,
                call_put=CallPutType.CALL,
                fonte=FonteType.MANUAL,
            )
        ]


class FakeEmptyRepo:
    def get_legs(self, aba, timestamp):
        return []


def test_service_returns_legs_for_valid_input(monkeypatch):
    service = RoboLegsService(repo=FakeValidRepo())

    class FakeReport:
        def is_ok(self):
            return True

    def fake_validate_legs(legs):
        return FakeReport()

    monkeypatch.setattr(robo_legs_service, "validate_legs", fake_validate_legs)

    result = service.get_legs(
        aba="TESTE",
        timestamp=datetime(2025, 1, 10, 10, 0, 0),
        validate=True,
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].aba == "TESTE"
    assert result[0].ativo == "PETR4"
    assert result[0].strike == 30.0


def test_service_returns_empty_list_when_repo_finds_no_match(monkeypatch):
    service = RoboLegsService(repo=FakeEmptyRepo())

    class FakeReport:
        def is_ok(self):
            return True

    def fake_validate_legs(legs):
        return FakeReport()

    monkeypatch.setattr(robo_legs_service, "validate_legs", fake_validate_legs)

    result = service.get_legs(
        aba="TESTE",
        timestamp=datetime(2025, 1, 10, 10, 0, 0),
        validate=True,
    )

    assert result == []


def test_service_skips_validation_when_validate_is_false(monkeypatch):
    service = RoboLegsService(repo=FakeValidRepo())

    def fake_validate_legs(legs):
        raise AssertionError("validate_legs should not be called when validate=False")

    monkeypatch.setattr(robo_legs_service, "validate_legs", fake_validate_legs)

    result = service.get_legs(
        aba="TESTE",
        timestamp=datetime(2025, 1, 10, 10, 0, 0),
        validate=False,
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].ativo == "PETR4"


def test_service_raises_leg_validation_error_when_validator_reports_invalid(monkeypatch):
    service = RoboLegsService(repo=FakeValidRepo())

    fake_error = SimpleNamespace(
        field="strike",
        row_index=0,
        error_message="Strike inconsistente",
    )

    class FakeReport:
        def __init__(self):
            self.errors = [fake_error]

        def is_ok(self):
            return False

    def fake_validate_legs(legs):
        return FakeReport()

    monkeypatch.setattr(robo_legs_service, "validate_legs", fake_validate_legs)

    with pytest.raises(LegValidationError) as exc:
        service.get_legs(
            aba="TESTE",
            timestamp=datetime(2025, 1, 10, 10, 0, 0),
            validate=True,
        )

    msg = str(exc.value)
    assert "aba=TESTE" in msg
    assert "timestamp=2025-01-10 10:00:00" in msg
    assert "field=strike" in msg
    assert "row_index=0" in msg
    assert "Strike inconsistente" in msg
