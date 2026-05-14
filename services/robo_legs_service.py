from __future__ import annotations

from typing import Any, List, Optional

from dto.robo_leg_dto import RoboLegDTO
from repositories.robo_legs_repository import RoboLegsRepository, RoboLegsRepoConfig
from validators.leg_validator import validate_legs


class RoboLegsService:
    """
    Camada fina:
      - obtém legs com regra manual > rtd
      - valida (opcional) e falha cedo se inválido
    """

    def __init__(self, repo: Optional[RoboLegsRepository] = None):
        self.repo = repo or RoboLegsRepository(RoboLegsRepoConfig())

    def get_legs(self, aba: str, timestamp: Any, validate: bool = True) -> List[RoboLegDTO]:
        legs = self.repo.get_legs(aba=aba, timestamp=timestamp)
        if validate:
            report = validate_legs(legs)
            if not report.is_ok():
                # Levanta erro enxuto (você pode trocar por exceção de domínio)
                first = report.errors[0]
                raise ValueError(f"Legs inválidas: {first.code} field={first.field} aba={first.aba}")
        return legs
