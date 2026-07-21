# services/system_recalculation_command_service.py
"""
Comando oficial para recalculo global do sistema.

A UI não calcula nada e não deve implementar loop de cálculo.
Este serviço centraliza o recalculo global e delega cada estrutura
ao fluxo oficial já existente.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from services.payoff_refresh_command_service import PayoffRefreshCommandService


class SystemRecalculationCommandService:
    """
    Serviço de comando para recalculo global.

    Responsabilidade:
    - localizar estruturas ativas/elegíveis;
    - chamar o fluxo oficial por estrutura;
    - consolidar resultado operacional.

    Não é responsabilidade da UI:
    - calcular payoff;
    - calcular decisão;
    - cruzar dados;
    - persistir derivados diretamente.
    """

    def __init__(
        self,
        db_path: str | Path | None = None,
        payoff_refresh_service: PayoffRefreshCommandService | None = None,
    ) -> None:
        self.db_path = Path(db_path) if db_path else self._default_db_path()
        self.payoff_refresh_service = payoff_refresh_service or PayoffRefreshCommandService()

    def recalculate_all(self) -> dict[str, Any]:
        """
        Recalcula todas as estruturas ativas/elegíveis.

        Retorna contrato operacional simples para a UI:
        - status
        - total
        - ok
        - warning
        - error
        - results
        """
        structure_ids = self._load_active_structure_ids()

        results: list[dict[str, Any]] = []
        ok_count = 0
        warning_count = 0
        error_count = 0

        for structure_id in structure_ids:
            try:
                result = self.payoff_refresh_service.refresh_payoff_for_structure(
                    int(structure_id)
                )
            except Exception as exc:
                result = {
                    "structure_id": structure_id,
                    "status": "error",
                    "message": str(exc),
                }

            status = str(result.get("status") or "").lower()
            if status == "ok":
                ok_count += 1
            elif status == "warning":
                warning_count += 1
            else:
                error_count += 1

            results.append(result)

        global_status = "ok"
        if error_count:
            global_status = "error"
        elif warning_count:
            global_status = "warning"

        return {
            "status": global_status,
            "total": len(structure_ids),
            "ok": ok_count,
            "warning": warning_count,
            "error": error_count,
            "results": results,
        }

    def _load_active_structure_ids(self) -> list[int]:
        if not self.db_path.exists():
            return []

        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute(
                """
                SELECT id
                  FROM structures
                 WHERE COALESCE(status, 'active') = 'active'
                 ORDER BY id
                """
            ).fetchall()

        return [int(row[0]) for row in rows if row and row[0] is not None]

    @staticmethod
    def _default_db_path() -> Path:
        return Path(__file__).resolve().parents[1] / "dados" / "app.db"

