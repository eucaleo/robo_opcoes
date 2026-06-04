"""
StructureRef -- encapsula a identidade de uma estrutura.

patch_53:  introdução do tipo
patch_54:  from_aba() resolve alias  structure_id via lookup real
           from_id() cria ref canônica diretamente por structure_id
           db_column() retorna coluna correta conforme disponibilidade

Regra de compatibilidade (rota_v2b.pdf -- Fase 2, decisão 1):
  - structure_id é a chave canônica REAL
  - aba é alias legado de compatibilidade APENAS
  - db_column() retorna 'structure_id' se disponível, 'aba' como fallback
"""
from __future__ import annotations


import sqlite3
import os
from dataclasses import dataclass, field
from typing import Optional


#  Path canônico (mesmo padrão usado em todo o projeto) 
_BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
_APP_DB_DEFAULT = os.path.join(_BASE_DIR, "dados", "app.db")


@dataclass(frozen=True)
class StructureRef:
    """
    Referência canônica a uma estrutura.

    Invariantes:
      - structure_id (int) é a identidade primária quando disponível
      - aba (str) é fallback legado -- nunca deve ser PK lógica nova
      - Pelo menos um dos dois deve estar preenchido (validado no __post_init__)
    """

    structure_id: Optional[int] = None
    aba:          Optional[str] = None

    # Metadado de diagnóstico -- não participa de == nem hash (frozen exclui)
    _resolved_via: str = field(default="direct", compare=False, hash=False)

    def __post_init__(self) -> None:
        if self.structure_id is None and not self.aba:
            raise ValueError(
                "StructureRef exige ao menos structure_id (int) ou aba (str)."
            )
        if self.structure_id is not None and not isinstance(self.structure_id, int):
            raise TypeError(
                f"structure_id deve ser int, recebido: {type(self.structure_id)}"
            )

    #  Factories 

    @classmethod
    def from_id(cls, structure_id: int) -> "StructureRef":
        """Cria ref canônica diretamente por structure_id."""
        return cls(structure_id=structure_id, _resolved_via="from_id")

    @classmethod
    def from_aba(
        cls,
        aba: str,
        app_db: Optional[str] = None,
    ) -> "StructureRef":
        """
        Cria ref a partir do alias legado (aba).

        Tenta resolver structure_id via structures.alias_legacy_aba em app.db.
        Se não encontrar, retorna ref com aba apenas (fallback seguro).

        Nunca lança exceção por ausência de match -- degradação graciosa.
        """
        if not aba:
            raise ValueError("aba não pode ser vazia para StructureRef.from_aba()")

        db_path = app_db or _APP_DB_DEFAULT
        structure_id: Optional[int] = None
        resolved_via = "aba_only"

        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                try:
                    row = conn.execute(
                        "SELECT id FROM structures "
                        "WHERE alias_legacy_aba = ? LIMIT 1",
                        (aba,),
                    ).fetchone()
                    if row:
                        structure_id = int(row[0])
                        resolved_via = "alias_lookup"
                finally:
                    conn.close()
            except sqlite3.OperationalError:
                # tabela structures ainda não existe -- fallback silencioso
                resolved_via = "aba_only_no_table"

        return cls(
            structure_id=structure_id,
            aba=aba,
            _resolved_via=resolved_via,
        )

    @classmethod
    def from_dict(cls, d: dict) -> "StructureRef":
        """
        Constrói a partir de dict (payload de decisão, etc.).
        Tenta structure_id primeiro, depois aba.
        """
        sid = d.get("structure_id")
        aba = d.get("aba") or d.get("ticker")
        if sid is not None:
            return cls(structure_id=int(sid), aba=aba or None, _resolved_via="from_dict")
        if aba:
            return cls(aba=aba, _resolved_via="from_dict_aba")
        raise ValueError(f"dict sem structure_id nem aba: {d}")

    #  Interface para camada DB 

    def db_column(self) -> str:
        """
        Retorna o nome da coluna a usar em queries SQL.

        Regra (patch_54):
          - Se tiver structure_id  'structure_id'  (canônico)
          - Senão                'aba'             (fallback legado)
        """
        return "structure_id" if self.structure_id is not None else "aba"

    def db_value(self):
        """
        Retorna o valor correspondente à coluna retornada por db_column().
        Usar em conjunto com db_column() para montar queries parametrizadas.
        """
        return self.structure_id if self.structure_id is not None else self.aba

    def db_pair(self) -> tuple[str, object]:
        """Atalho: retorna (coluna, valor) para WHERE clause."""
        return self.db_column(), self.db_value()

    #  Utilitários 

    def is_canonical(self) -> bool:
        """True se tem structure_id resolvido (identidade canônica real)."""
        return self.structure_id is not None

    def label(self) -> str:
        """Label humano para logs/debug."""
        if self.structure_id and self.aba:
            return f"id={self.structure_id}|aba={self.aba}"
        if self.structure_id:
            return f"id={self.structure_id}"
        return f"aba={self.aba}"

    def __repr__(self) -> str:
        return (
            f"StructureRef(structure_id={self.structure_id!r}, "
            f"aba={self.aba!r}, via={self._resolved_via!r})"
        )
