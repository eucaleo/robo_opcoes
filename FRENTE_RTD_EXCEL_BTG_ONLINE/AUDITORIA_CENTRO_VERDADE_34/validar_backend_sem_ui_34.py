from __future__ import annotations

import inspect
import json
import shutil
import sqlite3
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path.cwd()
DB_PATH = PROJECT_ROOT / "dados" / "app.db"
OUT_DIR = PROJECT_ROOT / "FRENTE_RTD_EXCEL_BTG_ONLINE" / "AUDITORIA_CENTRO_VERDADE_34"
OUT_JSON = OUT_DIR / "resultado_backend_sem_ui_34.json"
OUT_MD = OUT_DIR / "RESULTADO_BACKEND_SEM_UI_34.md"


TABLES_TO_COUNT = [
    "pricing_executions",
    "structure_snapshots",
    "payoff_curve_points",
    "structure_decisions",
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table,),
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    if not table_exists(conn, table):
        return []
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return [str(row["name"]) for row in rows]


def count_table(conn: sqlite3.Connection, table: str) -> int | None:
    if not table_exists(conn, table):
        return None
    row = conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
    return int(row["total"])


def counts(conn: sqlite3.Connection) -> dict[str, int | None]:
    return {table: count_table(conn, table) for table in TABLES_TO_COUNT}


def delta_counts(before: dict[str, int | None], after: dict[str, int | None]) -> dict[str, int | None]:
    deltas: dict[str, int | None] = {}
    for table in TABLES_TO_COUNT:
        b = before.get(table)
        a = after.get(table)
        deltas[table] = None if b is None or a is None else a - b
    return deltas


def detect_structure_id_column(conn: sqlite3.Connection) -> str:
    columns = table_columns(conn, "structures")
    for candidate in ("id", "structure_id"):
        if candidate in columns:
            return candidate
    raise RuntimeError(f"Nenhuma coluna de id encontrada em structures. Colunas: {columns}")


def pick_active_structure_id(conn: sqlite3.Connection) -> int:
    if not table_exists(conn, "structures"):
        raise RuntimeError("Tabela structures não existe.")

    id_col = detect_structure_id_column(conn)
    columns = table_columns(conn, "structures")

    if "status" in columns:
        row = conn.execute(
            f"""
            SELECT {id_col} AS structure_id
            FROM structures
            WHERE LOWER(COALESCE(status, '')) = 'active'
            ORDER BY {id_col}
            LIMIT 1
            """
        ).fetchone()
        if row is not None:
            return int(row["structure_id"])

    row = conn.execute(
        f"""
        SELECT {id_col} AS structure_id
        FROM structures
        ORDER BY {id_col}
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        raise RuntimeError("Nenhuma estrutura encontrada em structures.")

    return int(row["structure_id"])


def latest_payoff_summary(conn: sqlite3.Connection, structure_id: int) -> dict[str, Any]:
    if not table_exists(conn, "payoff_curve_points"):
        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": 0,
            "decision_found": False,
        }

    payoff_columns = table_columns(conn, "payoff_curve_points")

    structure_filter_col = None
    for candidate in ("structure_id", "estrutura_id"):
        if candidate in payoff_columns:
            structure_filter_col = candidate
            break

    if structure_filter_col is None:
        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": 0,
            "decision_found": False,
            "warning": f"payoff_curve_points sem coluna de estrutura. Colunas: {payoff_columns}",
        }

    if "timestamp" not in payoff_columns:
        row = conn.execute(
            f"""
            SELECT COUNT(*) AS total
            FROM payoff_curve_points
            WHERE {structure_filter_col} = ?
            """,
            (structure_id,),
        ).fetchone()

        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": int(row["total"] or 0),
            "decision_found": False,
            "warning": "payoff_curve_points sem coluna timestamp.",
        }

    ts_row = conn.execute(
        f"""
        SELECT MAX(timestamp) AS latest_payoff_timestamp
        FROM payoff_curve_points
        WHERE {structure_filter_col} = ?
        """,
        (structure_id,),
    ).fetchone()

    latest_ts = ts_row["latest_payoff_timestamp"] if ts_row else None

    if not latest_ts:
        return {
            "latest_payoff_timestamp": None,
            "payoff_points_count": 0,
            "decision_found": False,
        }

    points_row = conn.execute(
        f"""
        SELECT COUNT(*) AS total
        FROM payoff_curve_points
        WHERE {structure_filter_col} = ?
          AND timestamp = ?
        """,
        (structure_id, latest_ts),
    ).fetchone()

    points_count = int(points_row["total"] or 0)

    decision_found = False
    if table_exists(conn, "structure_decisions"):
        decision_columns = table_columns(conn, "structure_decisions")

        decision_structure_col = None
        for candidate in ("structure_id", "estrutura_id"):
            if candidate in decision_columns:
                decision_structure_col = candidate
                break

        if decision_structure_col and "timestamp" in decision_columns:
            decision_row = conn.execute(
                f"""
                SELECT 1
                FROM structure_decisions
                WHERE {decision_structure_col} = ?
                  AND timestamp = ?
                LIMIT 1
                """,
                (structure_id, latest_ts),
            ).fetchone()
            decision_found = decision_row is not None

    return {
        "latest_payoff_timestamp": latest_ts,
        "payoff_points_count": points_count,
        "decision_found": decision_found,
    }


def instantiate_command_service() -> Any:
    from services.payoff_refresh_command_service import PayoffRefreshCommandService

    try:
        return PayoffRefreshCommandService()
    except TypeError:
        pass

    for kwargs in (
        {"db_path": DB_PATH},
        {"database_path": DB_PATH},
        {"app_db_path": DB_PATH},
    ):
        try:
            return PayoffRefreshCommandService(**kwargs)
        except TypeError:
            continue

    raise RuntimeError(
        "Não foi possível instanciar PayoffRefreshCommandService com construtor padrão "
        "nem com db_path/database_path/app_db_path."
    )


def call_command_service(service: Any, structure_id: int) -> Any:
    candidates = [
        "refresh_payoff_for_structure",
        "refresh_payoff",
        "execute",
        "run",
    ]

    for method_name in candidates:
        method = getattr(service, method_name, None)
        if method is None:
            continue

        signature = inspect.signature(method)
        params = signature.parameters

        if "structure_id" in params:
            return method(structure_id=structure_id)

        if len(params) >= 1:
            return method(structure_id)

        return method()

    available = [
        name
        for name in dir(service)
        if not name.startswith("_") and callable(getattr(service, name))
    ]

    raise RuntimeError(
        "Nenhum método oficial encontrado no PayoffRefreshCommandService. "
        f"Tentados: {candidates}. Disponíveis: {available}"
    )


def write_reports(payload: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )

    status = payload.get("status", "error")
    deltas = payload.get("deltas", {})
    command_result = payload.get("command_result")

    md = [
        "# Resultado Backend Sem UI 34",
        "",
        f"Gerado em: `{payload.get('generated_at')}`",
        f"Projeto: `{PROJECT_ROOT}`",
        f"Banco: `{DB_PATH}`",
        f"Backup: `{payload.get('backup_path')}`",
        "",
        f"Status geral: `{status}`",
        "",
        "## Estrutura usada",
        "",
        f"- `structure_id`: `{payload.get('structure_id')}`",
        "",
        "## Contagens antes",
        "",
    ]

    for table, value in payload.get("before_counts", {}).items():
        md.append(f"- `{table}`: `{value}`")

    md.extend(["", "## Contagens depois", ""])

    for table, value in payload.get("after_counts", {}).items():
        md.append(f"- `{table}`: `{value}`")

    md.extend(["", "## Deltas", ""])

    for table, value in deltas.items():
        md.append(f"- `{table}`: `{value}`")

    md.extend(
        [
            "",
            "## Último payoff da estrutura",
            "",
        ]
    )

    for key, value in payload.get("latest_payoff_summary_after", {}).items():
        md.append(f"- `{key}`: `{value}`")

    md.extend(
        [
            "",
            "## Retorno do PayoffRefreshCommandService",
            "",
            "```json",
            json.dumps(command_result, indent=2, ensure_ascii=False, default=str),
            "```",
            "",
            "## Erro, se houver",
            "",
            "```text",
            str(payload.get("error") or ""),
            "```",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(md), encoding="utf-8")


def classify_result(payload: dict[str, Any]) -> str:
    if payload.get("error"):
        return "error"

    deltas = payload.get("deltas", {})
    latest = payload.get("latest_payoff_summary_after", {})

    pricing_delta = deltas.get("pricing_executions")
    snapshot_delta = deltas.get("structure_snapshots")
    payoff_delta = deltas.get("payoff_curve_points")
    decisions_delta = deltas.get("structure_decisions")

    points_count = int(latest.get("payoff_points_count") or 0)
    decision_found = bool(latest.get("decision_found"))

    if (
        pricing_delta is not None
        and pricing_delta > 0
        and payoff_delta is not None
        and payoff_delta > 0
        and points_count > 0
        and decision_found
    ):
        return "ok"

    if (
        pricing_delta is not None
        and pricing_delta > 0
        and (payoff_delta is None or payoff_delta <= 0 or points_count <= 0)
    ):
        return "warning"

    if (
        pricing_delta is not None
        and pricing_delta > 0
        and decisions_delta is not None
        and decisions_delta <= 0
    ):
        return "warning"

    if snapshot_delta is not None and snapshot_delta < 0:
        return "error"

    return "warning"


def main() -> None:
    payload: dict[str, Any] = {
        "generated_at": now_iso(),
        "project_root": str(PROJECT_ROOT),
        "db_path": str(DB_PATH),
        "backup_path": None,
        "structure_id": None,
        "before_counts": {},
        "after_counts": {},
        "deltas": {},
        "latest_payoff_summary_before": {},
        "latest_payoff_summary_after": {},
        "command_result": None,
        "status": "error",
        "error": None,
    }

    try:
        if not DB_PATH.exists():
            raise RuntimeError(f"Banco não encontrado: {DB_PATH}")

        backup_path = DB_PATH.with_name(
            f"app.backup_backend_sem_ui_34_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        )
        shutil.copy2(DB_PATH, backup_path)
        payload["backup_path"] = str(backup_path)

        with connect() as conn:
            structure_id = pick_active_structure_id(conn)
            payload["structure_id"] = structure_id
            payload["before_counts"] = counts(conn)
            payload["latest_payoff_summary_before"] = latest_payoff_summary(conn, structure_id)

        service = instantiate_command_service()
        result = call_command_service(service, int(payload["structure_id"]))
        payload["command_result"] = result

        with connect() as conn:
            payload["after_counts"] = counts(conn)
            payload["latest_payoff_summary_after"] = latest_payoff_summary(
                conn,
                int(payload["structure_id"]),
            )

        payload["deltas"] = delta_counts(
            payload["before_counts"],
            payload["after_counts"],
        )
        payload["status"] = classify_result(payload)

    except Exception as exc:
        payload["error"] = "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        )
        payload["status"] = "error"

    write_reports(payload)

    print("")
    print("===== RESULTADO BACKEND SEM UI 34 =====")
    print(f"Status: {payload['status']}")
    print(f"Structure ID: {payload.get('structure_id')}")
    print(f"Backup: {payload.get('backup_path')}")
    print("")
    print("Deltas:")
    for table, value in payload.get("deltas", {}).items():
        print(f"  {table}: {value}")
    print("")
    print(f"Resumo MD: {OUT_MD}")
    print(f"JSON: {OUT_JSON}")

    if payload["status"] == "ok":
        raise SystemExit(0)

    if payload["status"] == "warning":
        raise SystemExit(2)

    raise SystemExit(1)


if __name__ == "__main__":
    main()
