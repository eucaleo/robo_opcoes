import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from domain.payoff_features import compute_curve_features, upsert_curve_summary


def get_derived_db_connection():
    db_path = Path("Data/derived.db").resolve()
    return sqlite3.connect(str(db_path))


def latest_timestamp_per_aba() -> Dict[str, str]:
    conn = get_derived_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT aba, MAX(timestamp) AS ts
        FROM payoff_curve_points
        GROUP BY aba
    """)
    rows = cur.fetchall()
    conn.close()
    return {aba: ts for aba, ts in rows if aba and ts}


def load_curve_points(aba: str, timestamp: str) -> Tuple[Optional[float], List[Tuple[float, float]], Dict]:
    conn = get_derived_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT spot_ref, point_spot, point_pl, meta_json
        FROM payoff_curve_points
        WHERE aba = ? AND timestamp = ?
        ORDER BY point_spot
    """, (aba, timestamp))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return None, [], {}

    spot_ref = rows[0][0]
    points = [(float(r[1]), float(r[2])) for r in rows]

    meta = {}
    # meta_json pode variar por linha; preferir o primeiro não-nulo
    for r in rows:
        mj = r[3]
        if mj:
            try:
                meta = json.loads(mj)
            except Exception:
                meta = {"_meta_json_parse_error": True}
            break

    return spot_ref, points, meta


def main():
    latest = latest_timestamp_per_aba()
    if not latest:
        print("Nenhuma curva encontrada em payoff_curve_points.")
        return

    ok = 0
    fail = 0

    for aba, ts in latest.items():
        spot_ref, points, meta = load_curve_points(aba, ts)
        if not points:
            continue
        try:
            features = compute_curve_features(
                points=points,
                spot_ref=spot_ref,
                timestamp=ts,
                aba=aba,
                meta={"source_meta": meta}
            )
            upsert_curve_summary(features)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"[FAIL] aba={aba} ts={ts} err={e}")

    print(f"Summaries gerados: ok={ok} fail={fail}")


if __name__ == "__main__":
    main()
