"""
StructureRef — Referência unificada de estrutura (patch_53).

Encapsula o campo legado `aba` e a chave nova `structure_id`.
Quando o banco estiver migrado (patch_54), basta remover `alias_legacy_aba`
deste dataclass — ZERO mudança nos callers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class StructureRef:
    structure_id: int
    alias_legacy_aba: Optional[str] = field(default=None)

    # ------------------------------------------------------------------
    # Factories
    # ------------------------------------------------------------------

    @classmethod
    def from_aba(cls, aba: str, structure_id: int) -> "StructureRef":
        """Cria a partir do campo legado. Usar apenas em adaptadores/bridges."""
        return cls(structure_id=structure_id, alias_legacy_aba=aba)

    @classmethod
    def from_id(cls, structure_id: int) -> "StructureRef":
        """Cria sem legado — uso padrão no código novo."""
        return cls(structure_id=structure_id)

    # ------------------------------------------------------------------
    # Resolução de chave (banco ainda não migrado → usa alias_legacy_aba)
    # ------------------------------------------------------------------

    def db_key(self) -> str | int:
        """
        Retorna a chave correta para queries no banco.

        - Antes da migração do schema (patch_54): retorna alias_legacy_aba
        - Depois da migração do schema: retorna structure_id
        Remove este fallback quando patch_54 for aplicado.
        """
        if self.alias_legacy_aba is not None:
            return self.alias_legacy_aba   # legado: WHERE aba = ?
        return self.structure_id           # novo:   WHERE structure_id = ?

    def db_column(self) -> str:
        """Nome da coluna correspondente ao db_key()."""
        if self.alias_legacy_aba is not None:
            return "aba"
        return "structure_id"

    # ------------------------------------------------------------------
    # Utilitários
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        if self.alias_legacy_aba:
            return f"StructureRef(id={self.structure_id}, legacy='{self.alias_legacy_aba}')"
        return f"StructureRef(id={self.structure_id})"

    def __repr__(self) -> str:
        return self.__str__()
