from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


def _dict(row: sqlite3.Row) -> dict[str, Any]:
    return {k: row[k] for k in row.keys()}


def _breakevens(points: list[tuple[float, float]]) -> list[float]:
    if len(points) < 2:
        return []

    points = sorted(points, key=lambda x: x[0])
    bes: list[float] = []

    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        if y1 == 0:
            bes.append(x1)
            continue

        if y1 * y2 < 0 and x2 != x1:
            x0 = x1 + (0 - y1) * (x2 - x1) / (y2 - y1)
            bes.append(x0)

    out: list[float] = []
    for be in sorted(bes):
        if not out or abs(be - out[-1]) > 1e-6:
            out.append(be)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="dados/app.db")
    ap.add_argument("--structure-id", type=int)
    ap.add_argument("--sample", type=int, default=5)
    args = ap.parse_args()

    db = Path(args.db).resolve()
    print(f"DB: {db}")
    print(f"Existe: {db.exists()}")

    if not db.exists():
        return 2

    con = sqlite3.connect(str(db))
    con.row_factory = sqlite3.Row

    try:
        tables = {
            r["name"]
            for r in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

        if "payoff_curve_points" not in tables:
            print("ERRO: tabela payoff_curve_points não existe.")
            return 3

        print("\nSchema payoff_curve_points:")
        for r in con.execute("PRAGMA table_info(payoff_curve_points)").fetchall():
            print(f" - {r['name']}")

        where = ""
        params: tuple[Any, ...] = ()
        if args.structure_id is not None:
            where = "WHERE structure_id = ?"
            params = (args.structure_id,)

        print("\nResumo por structure_id:")
        rows = con.execute(
            f"""
            SELECT
                structure_id,
                COUNT(*) AS linhas,
                COUNT(DISTINCT timestamp) AS snapshots,
                MIN(timestamp) AS primeiro_ts,
                MAX(timestamp) AS ultimo_ts
            FROM payoff_curve_points
            {where}
            GROUP BY structure_id
            ORDER BY structure_id
            """,
            params,
        ).fetchall()

        for r in rows:
            print(_dict(r))

        print("\nÚltimo snapshot por estrutura:")
        latest_rows = con.execute(
            f"""
            WITH latest AS (
                SELECT structure_id, MAX(timestamp) AS timestamp
                FROM payoff_curve_points
                {where}
                GROUP BY structure_id
            )
            SELECT
                p.structure_id,
                p.timestamp,
                COUNT(*) AS linhas,
                MIN(p.point_spot) AS min_spot,
                MAX(p.point_spot) AS max_spot,
                MIN(p.point_pl) AS min_pl,
                MAX(p.point_pl) AS max_pl,
                AVG(p.spot_ref) AS spot_ref
            FROM payoff_curve_points p
            JOIN latest l
              ON l.structure_id = p.structure_id
             AND l.timestamp = p.timestamp
            GROUP BY p.structure_id, p.timestamp
            ORDER BY p.structure_id
            """,
            params,
        ).fetchall()

        for r in latest_rows:
            d = _dict(r)
            sid = d["structure_id"]
            ts = d["timestamp"]

            pts_rows = con.execute(
                """
                SELECT point_spot, point_pl
                FROM payoff_curve_points
                WHERE structure_id = ?
                  AND timestamp = ?
                ORDER BY point_spot
                """,
                (sid, ts),
            ).fetchall()

            pts = [(float(x["point_spot"]), float(x["point_pl"])) for x in pts_rows]
            bes = _breakevens(pts)
            d["breakevens"] = [round(x, 4) for x in bes]
            print(d)

            sample = con.execute(
                """
                SELECT point_spot, point_pl, spot_ref, meta_json
                FROM payoff_curve_points
                WHERE structure_id = ?
                  AND timestamp = ?
                ORDER BY point_spot
                LIMIT ?
                """,
                (sid, ts, args.sample),
            ).fetchall()

            print(f"  Amostra structure_id={sid}:")
            for item in sample:
                row = _dict(item)
                meta = row.get("meta_json")
                if meta:
                    try:
                        row["meta_json"] = json.loads(meta)
                    except Exception:
                        pass
                print(f"   - {row}")

        return 0
    finally:
        con.close()


if __name__ == "__main__":
    raise SystemExit(main())
