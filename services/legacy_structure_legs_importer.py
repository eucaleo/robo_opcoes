# services/legacy_structure_legs_importer.py
"""
LegacyStructureLegsImporter
---------------------------

Importa pernas legadas ja normalizadas pelo LegacyStructureLegsReader
para a tabela canonica structure_legs.

Fluxo controlado:

    structures.id
      -> LegacyStructureLegsReader.read_by_structure_id(...)
      -> payload canonico de legs
      -> StructuresRepository.replace_legs(...)

Observacoes:
    - Nao faz leitura direta das tabelas legadas.
    - Nao cria audit log proprio.
    - Reaproveita o audit trail ja existente em StructuresRepository.replace_legs,
      que registra action="REPLACE_LEGS".
"""

from __future__ import annotations

from typing import Any, Protocol

from repositories.structures_repository import StructuresRepository


class LegacyStructureLegsReaderProtocol(Protocol):
    def read_by_structure_id(
        self,
        structure_id: int,
        timestamp: str,
    ) -> list[dict[str, Any]]:
        ...


class LegacyStructureLegsImporter:
    """
    Orquestra a importacao das legs legadas para structure_legs.

    Dependencias:
        reader:
            Objeto compatível com LegacyStructureLegsReaderProtocol.

        structures_repository:
            Repositório canônico de structures/structure_legs.
    """

    def __init__(
        self,
        *,
        reader: LegacyStructureLegsReaderProtocol,
        structures_repository: StructuresRepository,
    ) -> None:
        self.reader = reader
        self.structures_repository = structures_repository

    def import_by_structure_id(
        self,
        *,
        structure_id: int,
        timestamp: str,
    ) -> dict[str, Any]:
        """
        Importa legs legadas para uma estrutura canonica.

        Retorna resumo da importacao:

            {
                "structure_id": 123,
                "timestamp": "...",
                "legs_count": 2,
                "imported": True,
            }

        Levanta:
            ValueError:
                - se a structure nao existir;
                - se o reader nao encontrar legs para importar.
        """
        structure = self.structures_repository.get_structure(structure_id)
        if structure is None:
            raise ValueError(f"structure not found: {structure_id}")

        legs = self.reader.read_by_structure_id(
            structure_id=structure_id,
            timestamp=timestamp,
        )

        if not legs:
            raise ValueError(
                f"structure_id={structure_id} sem legs legadas para importar"
            )

        self.structures_repository.replace_legs(
            structure_id=structure_id,
            legs=legs,
        )

        return {
            "structure_id": structure_id,
            "timestamp": timestamp,
            "legs_count": len(legs),
            "imported": True,
        }
