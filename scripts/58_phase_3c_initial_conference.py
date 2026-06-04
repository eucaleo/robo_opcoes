from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DB = ROOT_DIR / "dados" / "app.db"
DERIVED_DB = ROOT_DIR / "dados" / "derived.db"
REPORTS_DIR = ROOT_DIR / "reports"
OUTPUT_JSON = REPORTS_DIR / "phase_3c_initial_conference.json"
OUTPUT_MD = REPORTS_DIR / "phase_3c_initial_conference.md"


@dataclass
class CheckResult:
    name: str
    status: str
    details: dict[str, Any]


def _utc_now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat()


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def _get_columns(conn: sqlite3.Connection, table_name: str) -> list[str]:
    if not _table_exists(conn, table_name):
        return []
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row["name"] for row in rows]


def _count(conn: sqlite3.Connection, table_name: str) -> int | None:
    if not _table_exists(conn, table_name):
        return None
    row = conn.execute(f"SELECT COUNT(*) AS n FROM {table_name}").fetchone()
    return int(row["n"])


def _sample_rows(
    conn: sqlite3.Connection,
    table_name: str,
    limit: int = 5,
    order_by: str | None = None,
) -> list[dict[str, Any]]:
    if not _table_exists(conn, table_name):
        return []
    query = f"SELECT * FROM {table_name}"
    if order_by:
        query += f" ORDER BY {order_by}"
    query += f" LIMIT {int(limit)}"
    rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]


def check_database_presence() -> CheckResult:
    details = {
        "app_db_exists": APP_DB.exists(),
        "derived_db_exists": DERIVED_DB.exists(),
        "app_db": str(APP_DB),
        "derived_db": str(DERIVED_DB),
    }
    status = "ok" if details["app_db_exists"] and details["derived_db_exists"] else "error"
    return CheckResult("database_presence", status, details)


def check_structures_schema() -> CheckResult:
    if not APP_DB.exists():
        return CheckResult(
            "structures_schema",
            "error",
            {"reason": "app_db_not_found"},
        )

    expected_structures_columns = {
        "id",
        "name",
        "underlying_asset",
        "alias_legacy_aba",
        "status",
        "notes",
        "created_at",
        "updated_at",
    }
    expected_structure_legs_columns = {
        "id",
        "structure_id",
        "position_side",
        "option_type",
        "symbol",
        "strike",
        "expiration_date",
        "quantity",
        "premium",
        "multiplier",
        "leg_order",
        "notes",
        "created_at",
        "updated_at",
    }

    with _connect(APP_DB) as conn:
        structures_exists = _table_exists(conn, "structures")
        structure_legs_exists = _table_exists(conn, "structure_legs")
        structures_columns = set(_get_columns(conn, "structures"))
        structure_legs_columns = set(_get_columns(conn, "structure_legs"))

    missing_structures = sorted(expected_structures_columns - structures_columns)
    missing_legs = sorted(expected_structure_legs_columns - structure_legs_columns)

    status = "ok"
    if not structures_exists or not structure_legs_exists:
        status = "error"
    elif missing_structures or missing_legs:
        status = "warning"

    return CheckResult(
        "structures_schema",
        status,
        {
            "structures_exists": structures_exists,
            "structure_legs_exists": structure_legs_exists,
            "structures_columns": sorted(structures_columns),
            "structure_legs_columns": sorted(structure_legs_columns),
            "missing_structures_columns": missing_structures,
            "missing_structure_legs_columns": missing_legs,
        },
    )


def check_structures_inventory() -> CheckResult:
    if not APP_DB.exists():
        return CheckResult("structures_inventory", "error", {"reason": "app_db_not_found"})

    with _connect(APP_DB) as conn:
        structures_count = _count(conn, "structures")
        structure_legs_count = _count(conn, "structure_legs")

        active_count = None
        archived_count = None
        structures_without_legs = []
        duplicated_aliases = []
        sample_structures = []

        if _table_exists(conn, "structures"):
            row = conn.execute(
                """
                SELECT
                    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active_count,
                    SUM(CASE WHEN status = 'archived' THEN 1 ELSE 0 END) AS archived_count
                FROM structures
                """
            ).fetchone()
            active_count = int(row["active_count"] or 0)
            archived_count = int(row["archived_count"] or 0)

            sample_structures = _sample_rows(conn, "structures", limit=10, order_by="id DESC")

            if _table_exists(conn, "structure_legs"):
                rows = conn.execute(
                    """
                    SELECT s.id, s.name, s.alias_legacy_aba
                    FROM structures s
                    LEFT JOIN structure_legs l ON l.structure_id = s.id
                    GROUP BY s.id, s.name, s.alias_legacy_aba
                    HAVING COUNT(l.id) = 0
                    ORDER BY s.id DESC
                    LIMIT 20
                    """
                ).fetchall()
                structures_without_legs = [dict(row) for row in rows]

            rows = conn.execute(
                """
                SELECT alias_legacy_aba, COUNT(*) AS n
                FROM structures
                WHERE alias_legacy_aba IS NOT NULL
                  AND TRIM(alias_legacy_aba) <> ''
                GROUP BY alias_legacy_aba
                HAVING COUNT(*) > 1
                ORDER BY n DESC, alias_legacy_aba ASC
                LIMIT 20
                """
            ).fetchall()
            duplicated_aliases = [dict(row) for row in rows]

    status = "ok"
    if structures_count in (None, 0):
        status = "warning"

    return CheckResult(
        "structures_inventory",
        status,
        {
            "structures_count": structures_count,
            "structure_legs_count": structure_legs_count,
            "active_count": active_count,
            "archived_count": archived_count,
            "structures_without_legs_count": len(structures_without_legs),
            "structures_without_legs_sample": structures_without_legs,
            "duplicated_alias_legacy_aba_count": len(duplicated_aliases),
            "duplicated_alias_legacy_aba_sample": duplicated_aliases,
            "sample_structures": sample_structures,
        },
    )


def check_legacy_tables_inventory() -> CheckResult:
    if not APP_DB.exists():
        return CheckResult("legacy_tables_inventory", "error", {"reason": "app_db_not_found"})

    with _connect(APP_DB) as conn:
        tables = [
            "manual_analise_robo_legs",
            "rtd_analise_robo_legs",
            "rtd_analise_robo",
        ]
        details: dict[str, Any] = {}

        for table in tables:
            details[table] = {
                "exists": _table_exists(conn, table),
                "count": _count(conn, table),
                "columns": _get_columns(conn, table),
                "sample": _sample_rows(conn, table, limit=5, order_by="rowid DESC")
                if _table_exists(conn, table)
                else [],
            }

    status = "ok"
    if not details["rtd_analise_robo_legs"]["exists"]:
        status = "warning"

    return CheckResult("legacy_tables_inventory", status, details)


def check_alias_coverage_against_legacy() -> CheckResult:
    if not APP_DB.exists():
        return CheckResult("alias_coverage_against_legacy", "error", {"reason": "app_db_not_found"})

    with _connect(APP_DB) as conn:
        required_tables = {"structures", "rtd_analise_robo_legs"}
        if not all(_table_exists(conn, t) for t in required_tables):
            return CheckResult(
                "alias_coverage_against_legacy",
                "warning",
                {"reason": "required_tables_missing", "required_tables": sorted(required_tables)},
            )

        rows = conn.execute(
            """
            SELECT DISTINCT aba
            FROM rtd_analise_robo_legs
            WHERE aba IS NOT NULL AND TRIM(aba) <> ''
            ORDER BY aba
            """
        ).fetchall()
        legacy_abas = [row["aba"] for row in rows]

        rows = conn.execute(
            """
            SELECT DISTINCT alias_legacy_aba
            FROM structures
            WHERE alias_legacy_aba IS NOT NULL AND TRIM(alias_legacy_aba) <> ''
            ORDER BY alias_legacy_aba
            """
        ).fetchall()
        canonical_aliases = [row["alias_legacy_aba"] for row in rows]

    legacy_set = set(legacy_abas)
    canonical_set = set(canonical_aliases)

    missing_in_structures = sorted(legacy_set - canonical_set)[:50]
    aliases_without_legacy_match = sorted(canonical_set - legacy_set)[:50]

    status = "ok"
    if missing_in_structures:
        status = "warning"

    return CheckResult(
        "alias_coverage_against_legacy",
        status,
        {
            "legacy_aba_count": len(legacy_set),
            "canonical_alias_count": len(canonical_set),
            "missing_in_structures_count": len(legacy_set - canonical_set),
            "missing_in_structures_sample": missing_in_structures,
            "aliases_without_legacy_match_count": len(canonical_set - legacy_set),
            "aliases_without_legacy_match_sample": aliases_without_legacy_match,
        },
    )


def check_derived_identity_surface() -> CheckResult:
    if not DERIVED_DB.exists():
        return CheckResult("derived_identity_surface", "error", {"reason": "derived_db_not_found"})

    with _connect(DERIVED_DB) as conn:
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()
        tables = [row["name"] for row in rows]

        identity_surface = {}
        for table in tables:
            columns = _get_columns(conn, table)
            interesting = [c for c in columns if c in {"aba", "structure_id", "reference_date", "timestamp"}]
            if interesting:
                identity_surface[table] = interesting

    status = "ok"
    return CheckResult(
        "derived_identity_surface",
        status,
        {
            "tables_with_identity_columns": identity_surface,
        },
    )


def build_markdown_report(results: list[CheckResult]) -> str:
    lines: list[str] = []
    lines.append("# Phase 3C -- Initial Conference Report")
    lines.append("")
    lines.append(f"Generated at: `{_utc_now_iso()}`")
    lines.append("")

    for result in results:
        lines.append(f"## {result.name}")
        lines.append("")
        lines.append(f"- status: **{result.status}**")
        for key, value in result.details.items():
            lines.append(f"- **{key}**: `{json.dumps(value, ensure_ascii=False, default=str)}`")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    results = [
        check_database_presence(),
        check_structures_schema(),
        check_structures_inventory(),
        check_legacy_tables_inventory(),
        check_alias_coverage_against_legacy(),
        check_derived_identity_surface(),
    ]

    payload = {
        "generated_at": _utc_now_iso(),
        "app_db": str(APP_DB),
        "derived_db": str(DERIVED_DB),
        "results": [asdict(result) for result in results],
    }

    OUTPUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    OUTPUT_MD.write_text(build_markdown_report(results), encoding="utf-8")

    print("OK: initial conference generated")
    print(f"JSON: {OUTPUT_JSON}")
    print(f"MD:   {OUTPUT_MD}")

    overall = "ok"
    if any(r.status == "error" for r in results):
        overall = "error"
    elif any(r.status == "warning" for r in results):
        overall = "warning"

    print(f"OVERALL_STATUS={overall}")
    return 0 if overall in {"ok", "warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
