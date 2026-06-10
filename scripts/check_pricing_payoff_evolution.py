#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


APP_DB_DEFAULT = Path("dados/app.db")
DERIVED_DB_DEFAULT = Path("dados/derived.db")

REQUIRED_LEG_FIELDS = {
    "symbol",
    "quantity",
    "strike",
    "option_type",
    "premium",
    "expiration_date",
    "multiplier",
}

SIDE_FIELDS = {"side", "position_side"}


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def get_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row["name"] for row in rows]


def load_json_if_needed(value: Any) -> Any:
    if not isinstance(value, str):
        return value

    try:
        return json.loads(value)
    except Exception:
        return value


def fetch_latest_execution(
    app_db: Path,
    structure_id: int | None,
    reference_date: str | None,
) -> dict[str, Any] | None:
    with connect(app_db) as conn:
        if not table_exists(conn, "pricing_executions"):
            raise RuntimeError("Tabela pricing_executions não existe em dados/app.db")

        filters = []
        params: list[Any] = []

        if structure_id is not None:
            filters.append("structure_id = ?")
            params.append(structure_id)

        if reference_date is not None:
            filters.append("reference_date = ?")
            params.append(reference_date)

        where = ""
        if filters:
            where = "WHERE " + " AND ".join(filters)

        row = conn.execute(
            f"""
            SELECT *
            FROM pricing_executions
            {where}
            ORDER BY created_at DESC, id DESC
            LIMIT 1
            """,
            params,
        ).fetchone()

    if row is None:
        return None

    data = dict(row)

    if "pricing_payload" in data:
        data["pricing_payload"] = load_json_if_needed(data["pricing_payload"])

    if "result" in data:
        data["result"] = load_json_if_needed(data["result"])

    return data


def count_derived_points(
    derived_db: Path,
    execution_id: int | None,
    structure_id: int | None,
) -> tuple[int | None, str]:
    if not derived_db.exists():
        return None, f"derived.db não encontrado em {derived_db}"

    with connect(derived_db) as conn:
        if not table_exists(conn, "payoff_curve_points"):
            return None, "Tabela payoff_curve_points não existe em derived.db"

        columns = get_columns(conn, "payoff_curve_points")

        execution_cols = [
            "pricing_execution_id",
            "execution_id",
            "pricing_run_id",
            "run_id",
        ]

        for col in execution_cols:
            if execution_id is not None and col in columns:
                total = conn.execute(
                    f"""
                    SELECT COUNT(*)
                    FROM payoff_curve_points
                    WHERE {col} = ?
                    """,
                    (execution_id,),
                ).fetchone()[0]

                return int(total), f"{col}={execution_id}"

        if structure_id is not None and "structure_id" in columns:
            total = conn.execute(
                """
                SELECT COUNT(*)
                FROM payoff_curve_points
                WHERE structure_id = ?
                """,
                (structure_id,),
            ).fetchone()[0]

            return int(total), f"structure_id={structure_id}"

        total = conn.execute(
            """
            SELECT COUNT(*)
            FROM payoff_curve_points
            """
        ).fetchone()[0]

        return int(total), "sem filtro específico"


def validate_payload(payload: Any) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    data: dict[str, Any] = {}

    if not isinstance(payload, dict):
        errors.append("pricing_payload ausente ou inválido")
        return errors, warnings, data

    structure_id = payload.get("structure_id")
    underlying_asset = payload.get("underlying_asset")
    spot_price = payload.get("spot_price")
    legs = payload.get("legs")

    data["payload_structure_id"] = structure_id
    data["payload_underlying_asset"] = underlying_asset
    data["payload_spot_price"] = spot_price
    data["payload_legs_count"] = len(legs) if isinstance(legs, list) else None

    if structure_id is None:
        errors.append("pricing_payload.structure_id ausente")

    if not underlying_asset:
        errors.append("pricing_payload.underlying_asset ausente ou vazio")

    try:
        spot_float = float(spot_price)
    except Exception:
        spot_float = 0.0

    if spot_float <= 0:
        errors.append(f"pricing_payload.spot_price inválido: {spot_price}")

    if not isinstance(legs, list) or not legs:
        errors.append("pricing_payload.legs vazio ou inválido")
        return errors, warnings, data

    for index, leg in enumerate(legs):
        if not isinstance(leg, dict):
            errors.append(f"leg #{index} não é dict")
            continue

        missing = sorted(REQUIRED_LEG_FIELDS - set(leg.keys()))

        if missing:
            errors.append(f"leg #{index} sem campos canônicos: {missing}")

        if not SIDE_FIELDS.intersection(leg.keys()):
            errors.append(f"leg #{index} sem side ou position_side")

        if leg.get("quantity") in (None, ""):
            errors.append(f"leg #{index} com quantity vazio")

        if leg.get("symbol") in (None, ""):
            errors.append(f"leg #{index} com symbol vazio")

        if leg.get("expiration_date") in (None, ""):
            errors.append(f"leg #{index} com expiration_date vazio")

        if leg.get("premium") in (None, ""):
            warnings.append(f"leg #{index} com premium vazio")

    return errors, warnings, data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Checagem de evolução do fluxo Pricing / Payoff"
    )

    parser.add_argument(
        "--app-db",
        default=str(APP_DB_DEFAULT),
        help="Caminho do app.db",
    )

    parser.add_argument(
        "--derived-db",
        default=str(DERIVED_DB_DEFAULT),
        help="Caminho do derived.db",
    )

    parser.add_argument(
        "--structure-id",
        type=int,
        default=None,
        help="structure_id para validar",
    )

    parser.add_argument(
        "--reference-date",
        default=None,
        help="reference_date para filtrar, formato YYYY-MM-DD",
    )

    parser.add_argument(
        "--min-points",
        type=int,
        default=1,
        help="mínimo de pontos esperados em payoff_curve_points",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="imprime relatório em JSON",
    )

    args = parser.parse_args()

    app_db = Path(args.app_db)
    derived_db = Path(args.derived_db)

    errors: list[str] = []
    warnings: list[str] = []
    ok: list[str] = []
    data: dict[str, Any] = {}

    if not app_db.exists():
        errors.append(f"app.db não encontrado: {app_db}")
    else:
        ok.append(f"app.db encontrado: {app_db}")

    execution = None

    if not errors:
        try:
            execution = fetch_latest_execution(
                app_db=app_db,
                structure_id=args.structure_id,
                reference_date=args.reference_date,
            )
        except Exception as exc:
            errors.append(str(exc))

    if execution is None and not errors:
        if args.structure_id is not None:
            errors.append(f"Nenhuma execução encontrada para structure_id={args.structure_id}")
        else:
            errors.append("Nenhuma execução encontrada em pricing_executions")

    if execution is not None:
        execution_id = execution.get("id")
        payload = execution.get("pricing_payload")
        result = execution.get("result")

        data["execution_id"] = execution_id
        data["execution_created_at"] = execution.get("created_at")
        data["execution_structure_id"] = execution.get("structure_id")
        data["execution_status"] = execution.get("execution_status")
        data["execution_engine"] = execution.get("execution_engine")

        ok.append(f"execução encontrada: id={execution_id}")

        payload_errors, payload_warnings, payload_data = validate_payload(payload)
        errors.extend(payload_errors)
        warnings.extend(payload_warnings)
        data.update(payload_data)

        if isinstance(result, dict):
            ok.append("result presente")
        else:
            errors.append("result ausente ou inválido")

        points_count, filter_used = count_derived_points(
            derived_db=derived_db,
            execution_id=execution_id,
            structure_id=args.structure_id or execution.get("structure_id"),
        )

        data["derived_points_count"] = points_count
        data["derived_points_filter"] = filter_used

        if points_count is None:
            warnings.append(filter_used)
        elif points_count < args.min_points:
            errors.append(
                f"payoff_curve_points com poucos pontos: {points_count}. "
                f"Filtro usado: {filter_used}. Mínimo esperado: {args.min_points}"
            )
        else:
            ok.append(
                f"payoff_curve_points OK: {points_count} ponto(s). "
                f"Filtro usado: {filter_used}"
            )

    report = {
        "passed": not errors,
        "ok": ok,
        "warnings": warnings,
        "errors": errors,
        "data": data,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print()
        print("=== Pricing / Payoff Evolution Check ===")
        print()

        for item in ok:
            print(f"[OK] {item}")

        for item in warnings:
            print(f"[WARN] {item}")

        for item in errors:
            print(f"[ERROR] {item}")

        print()
        print("DATA:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print()

        if errors:
            print("CHECK FAILED")
        else:
            print("CHECK PASSED")

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
