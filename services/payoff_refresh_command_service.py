from __future__ import annotations

import inspect
import sqlite3
from pathlib import Path
from typing import Any

from services.pricing_execution_app_service import PricingExecutionAppService


class PayoffRefreshCommandService:
    """
    Serviço oficial para refresh operacional de payoff.

    Regra arquitetural:
    - UI não calcula payoff.
    - UI chama este serviço.
    - Este serviço chama PricingExecutionAppService.
    - A persistência derivada deve acontecer no wiring oficial.
    - Após a execução, este serviço valida se houve payoff persistido.
    """

    def __init__(
        self,
        pricing_app_service: PricingExecutionAppService | None = None,
        db_path: str | Path | None = None,
    ) -> None:
        self.pricing_app_service = pricing_app_service or PricingExecutionAppService()
        self.db_path = Path(db_path or "dados/app.db")

    def refresh_payoff_for_structure(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        structure_id = self._validate_structure_id(structure_id)

        before_ts = self._latest_payoff_timestamp(structure_id)

        try:
            pricing_result = self._execute_pricing(structure_id, reference_date)
        except Exception as exc:
            return {
                "status": "error",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": None,
                "snapshot_id": None,
                "payoff_points_count": 0,
                "latest_payoff_timestamp": before_ts,
                "decision_found": False,
                "message": f"Erro ao executar pricing: {exc}",
            }

        pricing_status = self._extract_status(pricing_result)
        pricing_execution_id = self._extract_pricing_execution_id(pricing_result)

        if pricing_status in {"error", "failed", "fail"}:
            return {
                "status": "error",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": pricing_execution_id,
                "snapshot_id": None,
                "payoff_points_count": 0,
                "latest_payoff_timestamp": before_ts,
                "decision_found": False,
                "message": "Pricing retornou erro. Payoff não será considerado atualizado.",
                "pricing_result": pricing_result,
            }

        payoff_summary = self._latest_payoff_summary(structure_id)
        after_ts = payoff_summary.get("latest_payoff_timestamp")
        points_count = int(payoff_summary.get("payoff_points_count") or 0)

        decision_found = self._decision_exists(structure_id, after_ts)
        snapshot_id = self._latest_snapshot_id(structure_id)

        if points_count <= 0:
            return {
                "status": "error",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": pricing_execution_id,
                "snapshot_id": snapshot_id,
                "payoff_points_count": 0,
                "latest_payoff_timestamp": after_ts,
                "decision_found": decision_found,
                "message": (
                    "Pricing executado, mas nenhum payoff persistido foi encontrado. "
                    "Verifique o wiring de DerivedPayoffPersistence."
                ),
                "pricing_result": pricing_result,
            }

        if before_ts == after_ts:
            return {
                "status": "warning",
                "structure_id": structure_id,
                "reference_date": reference_date,
                "pricing_execution_id": pricing_execution_id,
                "snapshot_id": snapshot_id,
                "payoff_points_count": points_count,
                "latest_payoff_timestamp": after_ts,
                "decision_found": decision_found,
                "message": (
                    "Pricing executado, mas o timestamp do payoff não mudou. "
                    "Pode haver persistência antiga, deduplicação ou falha silenciosa."
                ),
                "pricing_result": pricing_result,
            }

        return {
            "status": "ok",
            "structure_id": structure_id,
            "reference_date": reference_date,
            "pricing_execution_id": pricing_execution_id,
            "snapshot_id": snapshot_id,
            "payoff_points_count": points_count,
            "latest_payoff_timestamp": after_ts,
            "decision_found": decision_found,
            "message": "Payoff atualizado com sucesso.",
            "pricing_result": pricing_result,
        }

    def _execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None,
    ) -> Any:
        method = self.pricing_app_service.execute_pricing
        signature = inspect.signature(method)

        kwargs: dict[str, Any] = {"structure_id": structure_id}

        if reference_date is not None and "reference_date" in signature.parameters:
            kwargs["reference_date"] = reference_date

        return method(**kwargs)

    def _validate_structure_id(self, structure_id: int) -> int:
        try:
            value = int(structure_id)
        except Exception as exc:
            raise ValueError("structure_id inválido") from exc

        if value <= 0:
            raise ValueError("structure_id deve ser maior que zero")

        self._ensure_active_structure(value)

        return value

    def _ensure_active_structure(self, structure_id: int) -> None:
        """
        Bloqueia refresh/reprecificação para estruturas não ativas.

        Regra operacional:
          - apenas structures.status == 'active' pode gerar novo payoff/decisão;
          - archived/inactive não deve consumir processamento nem persistir derivados.
        """
        if not self.db_path.exists():
            raise ValueError(f"app.db não encontrado: {self.db_path}")

        with self._connect() as conn:
            cols = {row[1] for row in conn.execute("PRAGMA table_info(structures)").fetchall()}
            if "status" not in cols:
                raise ValueError("coluna structures.status não encontrada; validação de estrutura ativa impossível")

            row = conn.execute(
                """
                SELECT status
                  FROM structures
                 WHERE id = ?
                 LIMIT 1
                """,
                (structure_id,),
            ).fetchone()

        if not row:
            raise ValueError(f"structure not found: {structure_id}")

        status = str(row[0] or "").strip().lower()
        if status != "active":
            raise ValueError(
                f"estrutura inativa/arquivada não pode gerar payoff: "
                f"structure_id={structure_id}, status={status!r}"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def _latest_payoff_timestamp(self, structure_id: int) -> str | None:
        return self._latest_payoff_summary(structure_id).get("latest_payoff_timestamp")

    def _latest_payoff_summary(self, structure_id: int) -> dict[str, Any]:
        if not self.db_path.exists():
            return {
                "latest_payoff_timestamp": None,
                "payoff_points_count": 0,
            }

        query = """
            SELECT timestamp, COUNT(*) AS n
            FROM payoff_curve_points
            WHERE structure_id = ?
            GROUP BY timestamp
            ORDER BY timestamp DESC
            LIMIT 1
        """

        try:
            with self._connect() as conn:
                row = conn.execute(query, (structure_id,)).fetchone()
        except sqlite3.Error:
            return {
                "latest_payoff_timestamp": None,
                "payoff_points_count": 0,
            }

        if not row:
            return {
                "latest_payoff_timestamp": None,
                "payoff_points_count": 0,
            }

        return {
            "latest_payoff_timestamp": row[0],
            "payoff_points_count": row[1],
        }

    def _decision_exists(self, structure_id: int, timestamp: str | None) -> bool:
        if not timestamp or not self.db_path.exists():
            return False

        queries = [
            (
                """
                SELECT COUNT(*)
                FROM structure_decisions
                WHERE structure_id = ?
                  AND timestamp = ?
                """,
                (structure_id, timestamp),
            ),
            (
                """
                SELECT COUNT(*)
                FROM structure_decisions
                WHERE timestamp = ?
                """,
                (timestamp,),
            ),
        ]

        for query, params in queries:
            try:
                with self._connect() as conn:
                    count = conn.execute(query, params).fetchone()[0]
                return int(count) > 0
            except sqlite3.Error:
                continue

        return False

    def _latest_snapshot_id(self, structure_id: int) -> int | None:
        if not self.db_path.exists():
            return None

        queries = [
            """
            SELECT id
            FROM structure_snapshots
            WHERE structure_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            """
            SELECT snapshot_id
            FROM structure_snapshots
            WHERE structure_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
        ]

        for query in queries:
            try:
                with self._connect() as conn:
                    row = conn.execute(query, (structure_id,)).fetchone()
                if row:
                    return int(row[0])
            except sqlite3.Error:
                continue

        return None

    def _extract_status(self, result: Any) -> str | None:
        if isinstance(result, dict):
            value = result.get("status")
            return str(value).lower() if value is not None else None

        value = getattr(result, "status", None)
        return str(value).lower() if value is not None else None

    def _extract_pricing_execution_id(self, result: Any) -> int | None:
        keys = [
            "pricing_execution_id",
            "execution_id",
            "id",
        ]

        if isinstance(result, dict):
            for key in keys:
                value = result.get(key)
                if value is not None:
                    try:
                        return int(value)
                    except Exception:
                        return None

        for key in keys:
            value = getattr(result, key, None)
            if value is not None:
                try:
                    return int(value)
                except Exception:
                    return None

        return None
