# repositories/_aba_resolver_mixin.py
"""
AbaResolverMixin
----------------
Mixin compartilhado entre repositories que precisam resolver
structure_id -> alias_legacy_aba via tabela structures (app.db).

Requisito para uso em produção:
    A classe que herdar este mixin deve expor:
        self.config.app_db_path: str

Para testes, sobrescreva _get_resolver_conn() retornando
a conexão desejada (ex: sqlite3 in-memory).

Histórico:
    patch_40 -- método criado em robo_legs_repository e robo_legs_status_repository
    patch_62 -- extraído para mixin, eliminando duplicação
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AbaResolverMixin:
    """
    Fornece _resolve_aba_from_structure_id() de forma centralizada.

    Contrato:
        - Em produção: a classe concreta deve ter self.config.app_db_path (str)
        - Em testes:   sobrescreva _get_resolver_conn() com a conexão desejada
    """

    def _get_resolver_conn(self):
        """
        Retorna o context manager de conexão para o banco app.db.

        Implementação padrão usa sqlite_conn(self.config.app_db_path).
        Sobrescreva em testes para injetar uma conexão in-memory.
        """
        from infra.sqlite_conn import sqlite_conn
        return sqlite_conn(self.config.app_db_path)

    def _resolve_aba_from_structure_id(
        self,
        structure_id: int,
    ) -> Optional[str]:
        """
        Resolve structure_id -> alias_legacy_aba via tabela structures.

        Retorna:
            str   -- alias_legacy_aba quando encontrado e não-vazio
            None  -- quando não encontrado, campo vazio ou NULL

        Nunca propaga exceção: erros são logados e retornam None,
        deixando o chamador decidir como tratar a ausência.
        """
        if structure_id is None:
            logger.debug(
                "_resolve_aba_from_structure_id: structure_id=None, retornando None"
            )
            return None

        sql = """
            SELECT alias_legacy_aba
              FROM structures
             WHERE id = ?
               AND alias_legacy_aba IS NOT NULL
               AND alias_legacy_aba != ''
             LIMIT 1
        """
        try:
            with self._get_resolver_conn() as conn:
                row = conn.execute(sql, (structure_id,)).fetchone()

            result = row["alias_legacy_aba"] if row else None

            if result is None:
                logger.debug(
                    "_resolve_aba_from_structure_id: structure_id=%s "
                    "sem alias_legacy_aba em structures",
                    structure_id,
                )
            return result

        except Exception:
            logger.exception(
                "_resolve_aba_from_structure_id falhou para structure_id=%s",
                structure_id,
            )
            return None
