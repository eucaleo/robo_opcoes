from datetime import datetime

from dto.robo_leg_dto import RoboLegDTO, CVType, CallPutType, FonteType
from services.robo_legs_service import RoboLegsService


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


def test_service_returns_legs_when_validate_false():
    service = RoboLegsService(repo=FakeValidRepo())

    legs = service.get_legs(
        aba="TESTE",
        timestamp=datetime(2025, 1, 10, 10, 0, 0),
        validate=False,
    )

    assert len(legs) == 1
    assert legs[0].ativo == "PETR4"
