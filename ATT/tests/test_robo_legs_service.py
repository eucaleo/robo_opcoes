from datetime import datetime

import pytest

from dto.robo_leg_dto import FonteType, RoboLegDTO
from services.robo_legs_service import RoboLegsService


class FakeRepo:
    def __init__(self, legs):
        self._legs = legs

    def get_legs(self, aba, timestamp):
        return self._legs


def make_valid_leg():
    return RoboLegDTO(
        aba="BOVA11",
        timestamp=datetime(2026, 5, 16, 10, 0, 0),
        cv="C",
        call_put="CALL",
        strike=120.0,
        quant=1,
        ativo="BOVA11C120",
        vencimento=datetime(2026, 6, 20),
        fonte=FonteType.MANUAL,
        preco=1.23,
    )


def test_get_legs_returns_repo_legs_when_validation_disabled():
    legs = [make_valid_leg()]
    service = RoboLegsService(repo=FakeRepo(legs))

    result = service.get_legs("BOVA11", datetime(2026, 5, 16, 10, 0, 0), validate=False)

    assert result == legs


def test_get_legs_returns_repo_legs_when_validation_passes():
    legs = [make_valid_leg()]
    service = RoboLegsService(repo=FakeRepo(legs))

    result = service.get_legs("BOVA11", datetime(2026, 5, 16, 10, 0, 0), validate=True)

    assert result == legs


def test_get_legs_raises_value_error_when_validation_fails():
    invalid_leg = RoboLegDTO(
        aba="BOVA11",
        timestamp=datetime(2026, 5, 16, 10, 0, 0),
        cv="X",
        call_put="CALL",
        strike=120.0,
        quant=1,
        ativo="BOVA11C120",
        vencimento=datetime(2026, 6, 20),
        fonte=FonteType.MANUAL,
        preco=1.23,
    )
    service = RoboLegsService(repo=FakeRepo([invalid_leg]))

    with pytest.raises(ValueError, match=r"Legs inválidas: invalid_cv field=cv aba=BOVA11"):
        service.get_legs("BOVA11", datetime(2026, 5, 16, 10, 0, 0), validate=True)
