import json
from datetime import datetime
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
        pricing_payload: dict[str, Any],
        result: dict[str, Any],
    ) -> dict[str, Any]:
        if not pricing_payload:
            raise ValueError("pricing_payload is required")

        if not result:
            raise ValueError("result is required")

        records = self._read_all()
        next_id = self._next_id(records)

        record = {
            "id": next_id,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "structure_id": pricing_payload["structure_id"],
            "underlying_asset": pricing_payload["underlying_asset"],
            "reference_date": pricing_payload["reference_date"],
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
