from __future__ import annotations

from typing import Any

from repositories.robo_legs_repository import RoboLegsRepository
from services.robo_leg_mapper import to_canonical_leg


class LegacyStructureLegsReader:
    """
    Leitor canônico de pernas legadas para estruturas.

    Responsabilidade:
      - receber structure_id e timestamp de referência;
      - resolver alias_legacy_aba via RoboLegsRepository;
      - ler pernas legadas manual/rtd;
      - converter para payload compatível com structure_legs;
      - NÃO gravar em structure_legs.

    Fonte:
      structures.alias_legacy_aba -> *_analise_robo_legs.aba
    """

    def __init__(self, robo_legs_repository: RoboLegsRepository | None = None):
        self.robo_legs_repository = robo_legs_repository or RoboLegsRepository()

    def read_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
        *,
        multiplier: float = 1.0,
    ) -> list[dict[str, Any]]:
        legacy_legs = self.robo_legs_repository.get_legs_by_structure_id(
            structure_id=structure_id,
            timestamp=timestamp,
        )

        canonical_legs: list[dict[str, Any]] = []

        for index, legacy_leg in enumerate(legacy_legs, start=1):
            canonical_leg = to_canonical_leg(
                legacy_leg,
                multiplier=multiplier,
            )
            canonical_leg["leg_order"] = index
            canonical_legs.append(canonical_leg)

        return canonical_legs
