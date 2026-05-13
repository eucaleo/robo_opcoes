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

