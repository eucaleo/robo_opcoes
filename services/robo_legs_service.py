from __future__ import annotations
# services/robo_legs_service.py
"""
patch_40 -- get_legs_by_structure_id() como ponto de entrada canonico.
patch_57 -- correcoes:
  - from __future__ movido para primeira linha (SyntaxError fix)
  - get_legs(): parametro renomeado para ref: StructureRef; aba extraida de ref
"""


from typing import Any, List, Optional

from dto.robo_leg_dto import RoboLegDTO
from repositories.robo_legs_repository import RoboLegsRepository, RoboLegsRepoConfig
from src.domain.refs.structure_ref import StructureRef
from validators.leg_validator import validate_legs


class RoboLegsService:
    """
    Camada fina:
      - obtém legs com regra manual > rtd
      - valida (opcional) e falha cedo se invalido
    """

    def __init__(self, repo: Optional[RoboLegsRepository] = None):
        self.repo = repo or RoboLegsRepository(RoboLegsRepoConfig())

    def get_legs(
        self,
        ref: StructureRef,
        timestamp: Any,
        validate: bool = True,
    ) -> List[RoboLegDTO]:
        """
        Wrapper de compatibilidade legado.
        patch_57: extrai aba do StructureRef; nao usa 'aba' como variavel solta.
        """
        # bridge legado: selector ainda opera por aba
        aba = ref.aba if isinstance(ref, StructureRef) else str(ref)
        legs = self.repo.get_legs(ref=ref, timestamp=timestamp)
        if validate:
            report = validate_legs(legs)
            if not report.is_ok():
                first = report.errors[0]
                raise ValueError(
                    f"Legs inválidas: {first.code} field={first.field} aba={aba}"
                )
        return legs

    def get_legs_by_structure_id(
        self,
        structure_id: int,
        timestamp: Any,
        validate: bool = True,
    ) -> List[RoboLegDTO]:
        """
        patch_40: ponto de entrada canonico por structure_id.
        Delega para repo.get_legs_by_structure_id() e valida.
        """
        legs = self.repo.get_legs_by_structure_id(
            structure_id=structure_id,
            timestamp=timestamp,
        )
        if validate:
            report = validate_legs(legs)
            if not report.is_ok():
                first = report.errors[0]
                raise ValueError(
                    f"Legs inválidas: {first.code} field={first.field} "
                    f"structure_id={structure_id}"
                )
        return legs
