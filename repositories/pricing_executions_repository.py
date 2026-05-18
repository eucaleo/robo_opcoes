import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class PricingExecutionsRepository:
    def __init__(self, file_path: str = "dados/pricing_executions.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self._write_all([])

    def list_executions(self) -> list[dict[str, Any]]:
        return self._read_all()

    def save_execution(
        self,
        pricing_payload: dict[str, Any] | None,
        result: dict[str, Any],
        execution_status: str | None = None,
        execution_engine: str | None = None,
        error_message: str | None = None,
        duration_ms: int | None = None,
        number_of_legs: int | None = None,
        total_quantity: int | None = None,
        theoretical_value: float | None = None,
    ) -> dict[str, Any]:
        if not result:
            raise ValueError("result is required")

        records = self._read_all()
        next_id = self._next_id(records)

        record = {
            "id": next_id,
            "created_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "structure_id": pricing_payload.get("structure_id") if pricing_payload else None,
            "underlying_asset": pricing_payload.get("underlying_asset") if pricing_payload else None,
            "reference_date": pricing_payload.get("reference_date") if pricing_payload else None,
            "execution_status": execution_status,
            "execution_engine": execution_engine,
            "error_message": error_message,
            "duration_ms": duration_ms,
            "number_of_legs": number_of_legs,
            "total_quantity": total_quantity,
            "theoretical_value": theoretical_value,
            "pricing_payload": pricing_payload,
            "result": result,
        }

        records.append(record)
        self._write_all(records)

        return record

    def get_execution(self, execution_id: int) -> dict[str, Any] | None:
        records = self._read_all()
        for record in records:
            if record["id"] == execution_id:
                return record
        return None

    def _read_all(self) -> list[dict[str, Any]]:
        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("pricing executions storage must contain a list")

        return data

    def _write_all(self, records: list[dict[str, Any]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

    def _next_id(self, records: list[dict[str, Any]]) -> int:
        if not records:
            return 1
        return max(int(record["id"]) for record in records) + 1
