from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recalcula payoff das estruturas e grava em payoff_curve_points."
    )
    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do app.db. Default: dados/app.db",
    )
    parser.add_argument(
        "--structure-id",
        type=int,
        default=None,
        help="Se informado, recalcula apenas esta estrutura.",
    )
    parser.add_argument(
        "--active-only",
        action="store_true",
        help="Se possível, recalcula apenas estruturas ativas.",
    )
    return parser.parse_args()


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def _table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    try:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    except sqlite3.Error:
        return set()
    return {str(row["name"]) for row in rows}


def _load_structure_ids(
    conn: sqlite3.Connection,
    structure_id: int | None = None,
    active_only: bool = False,
) -> list[int]:
    cols = _table_columns(conn, "structures")
    if not cols:
        raise RuntimeError("Tabela structures não encontrada no app.db.")

    where = []
    params = []

    if structure_id is not None:
        where.append("id = ?")
        params.append(structure_id)

    if active_only:
        for candidate in ("is_active", "active", "enabled"):
            if candidate in cols:
                where.append(f"COALESCE({candidate}, 1) = 1")
                break

    where_sql = ""
    if where:
        where_sql = " WHERE " + " AND ".join(where)

    sql = f"SELECT id FROM structures{where_sql} ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    return [int(row["id"]) for row in rows]


def _count_payoff_points(conn: sqlite3.Connection) -> int:
    try:
        row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()
        return int(row["n"] or 0)
    except sqlite3.Error:
        return 0


def main() -> int:
    args = _parse_args()

    root = _project_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = (root / db_path).resolve()
    else:
        db_path = db_path.resolve()

    if not db_path.exists():
        print(f"[payoff-once] ERRO: banco não encontrado: {db_path}")
        return 2

    # Importante: db.config lê APP_DB_PATH no import.
    # Portanto a env precisa ser setada antes de importar os services.
    os.environ["APP_DB_PATH"] = str(db_path)

    from services.pricing_execution_app_service import PricingExecutionAppService

    print(f"[payoff-once] db={db_path}")

    with _connect(db_path) as conn:
        before = _count_payoff_points(conn)
        structure_ids = _load_structure_ids(
            conn,
            structure_id=args.structure_id,
            active_only=args.active_only,
        )

    if not structure_ids:
        print("[payoff-once] Nenhuma estrutura encontrada para recalcular.")
        return 1

    print(f"[payoff-once] estruturas={structure_ids}")

    service = PricingExecutionAppService()

    ok = 0
    fail = 0

    for sid in structure_ids:
        try:
            print(f"[payoff-once] recalculando structure_id={sid}...")
            result = service.execute_pricing(structure_id=sid)

            status = None
            if isinstance(result, dict):
                status = result.get("status") or result.get("execution_status")

            print(f"[payoff-once] OK structure_id={sid} status={status}")
            ok += 1

        except Exception as exc:
            print(f"[payoff-once] ERRO structure_id={sid}: {type(exc).__name__}: {exc}")
            fail += 1

    with _connect(db_path) as conn:
        after = _count_payoff_points(conn)

    print(f"[payoff-once] concluído. ok={ok} fail={fail} payoff_points_before={before} payoff_points_after={after}")

    return 0 if ok > 0 and fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
