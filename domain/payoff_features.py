import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any


def get_derived_db_connection():
    db_path = Path("dados/derived.db").resolve()
    return sqlite3.connect(str(db_path))


def _as_sorted_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    pts = [(float(x), float(y)) for x, y in points]
    pts.sort(key=lambda t: t[0])
    return pts


def _interp_y_at_x(points: List[Tuple[float, float]], x: float) -> Optional[float]:
    """
    Linear interpolation. Returns None if x is outside the points' x-range or insufficient points.
    """
    pts = _as_sorted_points(points)
    if len(pts) < 2:
        return None

    if x < pts[0][0] or x > pts[-1][0]:
        return None

    # find segment
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return None


def _find_breakevens(points: List[Tuple[float, float]], eps: float = 1e-12) -> List[float]:
    """
    Finds approximate x where y crosses 0 using linear interpolation between consecutive points.
    """
    pts = _as_sorted_points(points)
    if len(pts) < 2:
        return []

    bes: List[float] = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        # exact zeros at grid points
        if abs(y0) <= eps:
            bes.append(x0)

        # crossing
        if (y0 < -eps and y1 > eps) or (y0 > eps and y1 < -eps):
            # y = y0 + t*(y1-y0); set y=0 => t = -y0/(y1-y0)
            denom = (y1 - y0)
            if abs(denom) > eps:
                t = (-y0) / denom
                xz = x0 + t * (x1 - x0)
                bes.append(xz)

        # handle last point exact zero
    if abs(pts[-1][1]) <= eps:
        bes.append(pts[-1][0])

    # de-dup close values
    bes.sort()
    out: List[float] = []
    for x in bes:
        if not out or abs(x - out[-1]) > 1e-6:
            out.append(float(x))
    return out


def _positive_ranges(points: List[Tuple[float, float]], eps: float = 0.0) -> List[Tuple[float, float]]:
    """
    Returns ranges [x_start, x_end] where y >= 0 (approx) based on sign of sampled points.
    Uses breakevens to cut segments.
    """
    pts = _as_sorted_points(points)
    if len(pts) < 2:
        return []

    bes = _find_breakevens(pts)
    xs = [pts[0][0]] + bes + [pts[-1][0]]
    xs = sorted(set(float(x) for x in xs))

    ranges: List[Tuple[float, float]] = []
    curr_start: Optional[float] = None

    def mid(a: float, b: float) -> float:
        return (a + b) / 2.0

    for a, b in zip(xs, xs[1:]):
        if b <= a:
            continue
        xm = mid(a, b)
        ym = _interp_y_at_x(pts, xm)
        if ym is None:
            continue
        if ym >= -eps:
            if curr_start is None:
                curr_start = a
        else:
            if curr_start is not None:
                ranges.append((curr_start, a))
                curr_start = None

    if curr_start is not None:
        ranges.append((curr_start, xs[-1]))

    # clean small/degenerate ranges
    cleaned = []
    for a, b in ranges:
        if b - a > 1e-9:
            cleaned.append((float(a), float(b)))
    return cleaned


def compute_curve_features(
    points: List[Tuple[float, float]],
    spot_ref: Optional[float] = None,
    timestamp: Optional[str] = None,
    aba: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    pts = _as_sorted_points(points)
    if not pts:
        raise ValueError("points vazio")

    ys = [y for _, y in pts]
    pl_min = float(min(ys))
    pl_max = float(max(ys))

    pl_at_spot_ref = None
    if spot_ref is not None:
        pl_at_spot_ref = _interp_y_at_x(pts, float(spot_ref))

    bes = _find_breakevens(pts)
    pos_ranges = _positive_ranges(pts)

    features = {
        "timestamp": timestamp,
        "aba": aba,
        "spot_ref": float(spot_ref) if spot_ref is not None else None,
        "points_count": int(len(pts)),
        "pl_min": pl_min,
        "pl_max": pl_max,
        "pl_at_spot_ref": float(pl_at_spot_ref) if pl_at_spot_ref is not None else None,
        "breakevens": bes,
        "be_count": int(len(bes)),
        "pos_ranges": [[a, b] for a, b in pos_ranges],
        "pos_ranges_count": int(len(pos_ranges)),
        "max_drawdown_like": float(pl_max - pl_min),
        "meta": meta or {},
    }
    return features


def upsert_curve_summary(features: Dict[str, Any]) -> None:
    """
    Upsert por (timestamp, aba).
    """
    ts = features.get("timestamp")
    aba = features.get("aba")
    if not ts or not aba:
        raise ValueError("features precisa de timestamp e aba")

    conn = get_derived_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO payoff_curve_summary (
          timestamp, aba,
          spot_ref, points_count,
          pl_min, pl_max,
          pl_at_spot_ref,
          breakevens_json, be_count,
          pos_ranges_json, pos_ranges_count,
          max_drawdown_like,
          meta_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(timestamp, aba) DO UPDATE SET
          spot_ref=excluded.spot_ref,
          points_count=excluded.points_count,
          pl_min=excluded.pl_min,
          pl_max=excluded.pl_max,
          pl_at_spot_ref=excluded.pl_at_spot_ref,
          breakevens_json=excluded.breakevens_json,
          be_count=excluded.be_count,
          pos_ranges_json=excluded.pos_ranges_json,
          pos_ranges_count=excluded.pos_ranges_count,
          max_drawdown_like=excluded.max_drawdown_like,
          meta_json=excluded.meta_json
        """,
        (
            ts, aba,
            features.get("spot_ref"),
            features.get("points_count"),
            features.get("pl_min"),
            features.get("pl_max"),
            features.get("pl_at_spot_ref"),
            json.dumps(features.get("breakevens", []), ensure_ascii=False),
            features.get("be_count"),
            json.dumps(features.get("pos_ranges", []), ensure_ascii=False),
            features.get("pos_ranges_count"),
            features.get("max_drawdown_like"),
            json.dumps(features.get("meta", {}), ensure_ascii=False),
        )
    )

    conn.commit()
    conn.close()
