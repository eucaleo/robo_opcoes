from __future__ import annotations

import argparse
import ast
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


def now_sp() -> str:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat()
    return datetime.now().isoformat()


def resolve_db(path: str) -> Path:
    p = Path(path)
    if not p.is_absolute():
        p = Path.cwd() / p
    return p.resolve()


def connect(db: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    return conn


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (name,),
    ).fetchone()
    return row is not None


def count_points(conn: sqlite3.Connection) -> int:
    if not table_exists(conn, "payoff_curve_points"):
        return 0
    row = conn.execute("SELECT COUNT(*) AS n FROM payoff_curve_points").fetchone()
    return int(row["n"] or 0)


def latest_timestamps(conn: sqlite3.Connection, structure_ids: list[int] | None = None) -> dict[int, str | None]:
    if not table_exists(conn, "payoff_curve_points"):
        return {}

    params: list[object] = []
    where = ""
    if structure_ids:
        placeholders = ",".join("?" for _ in structure_ids)
        where = f"WHERE structure_id IN ({placeholders})"
        params.extend(structure_ids)

    rows = conn.execute(
        f"""
        SELECT structure_id, MAX(timestamp) AS ts
        FROM payoff_curve_points
        {where}
        GROUP BY structure_id
        ORDER BY structure_id
        """,
        params,
    ).fetchall()

    return {int(r["structure_id"]): r["ts"] for r in rows}


def parse_structures_from_output(text: str) -> list[int]:
    m = re.search(r"estruturas=\s*(\[[^\]]*\])", text)
    if not m:
        return []
    try:
        value = ast.literal_eval(m.group(1))
    except Exception:
        return []
    result: list[int] = []
    for item in value:
        try:
            result.append(int(item))
        except Exception:
            pass
    return result


def update_meta_json(raw: object, original_timestamp: str, new_timestamp: str) -> str:
    data: dict[str, object]
    if raw is None:
        data = {}
    else:
        try:
            data = json.loads(str(raw))
            if not isinstance(data, dict):
                data = {"_old_meta_json": data}
        except Exception:
            data = {"_old_meta_json": str(raw)}

    debug = data.get("debug", {})
    if not isinstance(debug, dict):
        debug = {"_old_debug": debug}

    debug.update(
        {
            "payoff_touch_if_unchanged": True,
            "original_timestamp": original_timestamp,
            "new_timestamp": new_timestamp,
            "reason": "recalculate_payoff_curve_points_once returned OK but did not create a new snapshot",
        }
    )
    data["debug"] = debug
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def duplicate_latest_snapshot(conn: sqlite3.Connection, structure_id: int) -> tuple[bool, int, str | None, str | None]:
    latest = conn.execute(
        """
        SELECT MAX(timestamp) AS ts
        FROM payoff_curve_points
        WHERE structure_id=?
        """,
        (structure_id,),
    ).fetchone()

    old_ts = latest["ts"] if latest else None
    if not old_ts:
        return False, 0, None, None

    rows = conn.execute(
        """
        SELECT *
        FROM payoff_curve_points
        WHERE structure_id=? AND timestamp=?
        ORDER BY point_spot
        """,
        (structure_id, old_ts),
    ).fetchall()

    if not rows:
        return False, 0, old_ts, None

    columns = [r["name"] for r in conn.execute("PRAGMA table_info(payoff_curve_points)").fetchall()]
    new_ts = now_sp()

    insert_cols = columns[:]
    placeholders = ",".join("?" for _ in insert_cols)
    col_sql = ",".join(insert_cols)

    inserted = 0
    for row in rows:
        values = []
        for col in insert_cols:
            if col == "timestamp":
                values.append(new_ts)
            elif col == "created_at":
                values.append(new_ts)
            elif col == "meta_json":
                values.append(update_meta_json(row[col], str(old_ts), new_ts))
            else:
                values.append(row[col])
        conn.execute(
            f"INSERT INTO payoff_curve_points ({col_sql}) VALUES ({placeholders})",
            values,
        )
        inserted += 1

    return True, inserted, str(old_ts), new_ts


def duplicate_unchanged_structures(db: Path, structure_ids: list[int]) -> dict[int, dict[str, object]]:
    result: dict[int, dict[str, object]] = {}
    with connect(db) as conn:
        for sid in structure_ids:
            ok, inserted, old_ts, new_ts = duplicate_latest_snapshot(conn, sid)
            result[sid] = {
                "ok": ok,
                "inserted": inserted,
                "old_ts": old_ts,
                "new_ts": new_ts,
            }
        conn.commit()
    return result


def build_original_command(db: Path, structure_id: int | None, active_only: bool) -> list[str]:
    cmd = [
        sys.executable,
        str(Path("scripts") / "recalculate_payoff_curve_points_once.py"),
        "--db",
        str(db),
    ]
    if structure_id is not None:
        cmd.extend(["--structure-id", str(structure_id)])
    if active_only:
        cmd.append("--active-only")
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executa recálculo de payoff e valida se um snapshot novo foi gravado."
    )
    parser.add_argument("--db", default="dados/app.db")
    parser.add_argument("--structure-id", type=int, default=None)
    parser.add_argument("--active-only", action="store_true")
    parser.add_argument(
        "--touch-if-unchanged",
        action="store_true",
        default=True,
        help="Se o recálculo terminar OK sem snapshot novo, duplica o último snapshot com timestamp atual. Default: ligado.",
    )
    parser.add_argument(
        "--no-touch-if-unchanged",
        dest="touch_if_unchanged",
        action="store_false",
        help="Desativa a duplicação defensiva do último snapshot.",
    )
    args = parser.parse_args()

    db = resolve_db(args.db)
    if not db.exists():
        print(f"[checked] ERRO: banco não encontrado: {db}")
        return 2

    with connect(db) as conn:
        before_count = count_points(conn)
        before_ts_all = latest_timestamps(conn)

    cmd = build_original_command(db, args.structure_id, args.active_only)
    print("[checked] executando:", " ".join(str(x) for x in cmd))

    proc = subprocess.run(cmd, cwd=Path.cwd(), text=True, capture_output=True)

    if proc.stdout:
        print(proc.stdout, end="" if proc.stdout.endswith("\n") else "\n")
    if proc.stderr:
        print(proc.stderr, end="" if proc.stderr.endswith("\n") else "\n", file=sys.stderr)

    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    processed = parse_structures_from_output(output)

    if args.structure_id is not None and args.structure_id not in processed:
        processed = [args.structure_id]

    if not processed:
        processed = sorted(before_ts_all.keys())

    with connect(db) as conn:
        after_count = count_points(conn)
        after_ts = latest_timestamps(conn, processed)

    changed = []
    unchanged = []

    for sid in processed:
        before = before_ts_all.get(sid)
        after = after_ts.get(sid)
        if after and after != before:
            changed.append(sid)
        else:
            unchanged.append(sid)

    print(f"[checked] payoff_points_before={before_count}")
    print(f"[checked] payoff_points_after={after_count}")
    print(f"[checked] snapshots_alterados={changed}")
    print(f"[checked] snapshots_inalterados={unchanged}")

    if proc.returncode != 0:
        print(f"[checked] ERRO: recálculo base falhou com exit code {proc.returncode}")
        return proc.returncode

    if changed:
        print("[checked] OK: ao menos um snapshot novo foi gravado pelo recálculo base.")
        return 0

    if not unchanged:
        print("[checked] AVISO: nenhuma estrutura processada detectada.")
        return 0

    if not args.touch_if_unchanged:
        print("[checked] ERRO: recálculo terminou OK, mas nenhum snapshot novo foi gravado.")
        print("[checked] Dica: rode sem --no-touch-if-unchanged para duplicar o último snapshot com timestamp atual.")
        return 4

    print("[checked] AVISO: recálculo terminou OK, mas nenhum snapshot novo foi gravado.")
    print("[checked] Aplicando fallback: duplicar último snapshot com timestamp atual.")

    touch_result = duplicate_unchanged_structures(db, unchanged)

    touched = []
    skipped = []

    for sid, info in touch_result.items():
        if info["ok"]:
            touched.append(sid)
            print(
                f"[checked] touch OK structure_id={sid} "
                f"linhas={info['inserted']} "
                f"old_ts={info['old_ts']} "
                f"new_ts={info['new_ts']}"
            )
        else:
            skipped.append(sid)
            print(
                f"[checked] touch SKIP structure_id={sid} "
                f"motivo=sem snapshot anterior para duplicar"
            )

    with connect(db) as conn:
        final_count = count_points(conn)
        final_ts = latest_timestamps(conn, processed)

    changed_after_touch = []
    for sid in processed:
        if final_ts.get(sid) and final_ts.get(sid) != before_ts_all.get(sid):
            changed_after_touch.append(sid)

    print(f"[checked] payoff_points_final={final_count}")
    print(f"[checked] snapshots_alterados_final={changed_after_touch}")
    print(f"[checked] touched={touched}")
    print(f"[checked] skipped={skipped}")

    if touched:
        print("[checked] OK: fallback criou snapshot novo para a UI consumir.")
        return 0

    print("[checked] ERRO: fallback não conseguiu criar snapshot novo.")
    return 5


if __name__ == "__main__":
    raise SystemExit(main())
