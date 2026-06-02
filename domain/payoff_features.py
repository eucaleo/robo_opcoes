import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

"""
Patch 24: chave de upsert migrada de (timestamp, aba)
          para (structure_id, reference_date).
          aba e timestamp mantidos como colunas opcionais de rastreabilidade.
"""


def get_derived_db_connection() -> sqlite3.Connection:
    db_path = Path("dados/derived.db").resolve()
    return sqlite3.connect(str(db_path))


def _as_sorted_points(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    pts = [(float(x), float(y)) for x, y in points]
    pts.sort(key=lambda t: t[0])
    return pts


def _interp_y_at_x(points: List[Tuple[float, float]], x: float) -> Optional[float]:
    pts = _as_sorted_points(points)
    if len(pts) < 2:
        return None
    if x < pts[0][0] or x > pts[-1][0]:
        return None
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return None


def _find_breakevens(points: List[Tuple[float, float]], eps: float = 1e-12) -> List[float]:
    pts = _as_sorted_points(points)
    if len(pts) < 2:
        return []
    bes: List[float] = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if abs(y0) <= eps:
            bes.append(x0)
        if (y0 < -eps and y1 > eps) or (y0 > eps and y1 < -eps):
            denom = y1 - y0
            if abs(denom) > eps:
                t = (-y0) / denom
                bes.append(x0 + t * (x1 - x0))
    if abs(pts[-1][1]) <= eps:
        bes.append(pts[-1][0])
    bes.sort()
    out: List[float] = []
    for x in bes:
        if not out or abs(x - out[-1]) > 1e-6:
            out.append(float(x))
    return out


def _positive_ranges(
    points: List[Tuple[float, float]],
    eps: float = 0.0,
) -> List[Tuple[float, float]]:
    pts = _as_sorted_points(points)
    if len(pts) < 2:
        return []
    bes = _find_breakevens(pts)
    xs = sorted(set(float(x) for x in [pts[0][0]] + bes + [pts[-1][0]]))
    ranges: List[Tuple[float, float]] = []
    curr_start: Optional[float] = None

    def mid(a: float, b: float) -> float:
        return (a + b) / 2.0

    for a, b in zip(xs, xs[1:]):
        if b <= a:
            continue
        ym = _interp_y_at_x(pts, mid(a, b))
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
    return [(float(a), float(b)) for a, b in ranges if b - a > 1e-9]


def compute_curve_features(
    points: List[Tuple[float, float]],
    spot_ref: Optional[float] = None,
    structure_id: Optional[str] = None,
    reference_date: Optional[str] = None,
    timestamp: Optional[str] = None,
    aba: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Computa features da curva de payoff.

    Chave canônica : structure_id + reference_date  → upsert no derived.db.
    timestamp + aba               → rastreabilidade opcional (legado RTD).
    """
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

    return {
        "structure_id":      structure_id,
        "reference_date":    reference_date,
        "timestamp":         timestamp,
        "aba":               aba,
        "spot_ref":          float(spot_ref) if spot_ref is not None else None,
        "points_count":      int(len(pts)),
        "pl_min":            pl_min,
        "pl_max":            pl_max,
        "pl_at_spot_ref":    float(pl_at_spot_ref) if pl_at_spot_ref is not None else None,
        "breakevens":        bes,
        "be_count":          int(len(bes)),
        "pos_ranges":        [[a, b] for a, b in pos_ranges],
        "pos_ranges_count":  int(len(pos_ranges)),
        "max_drawdown_like": float(pl_max - pl_min),
        "meta":              meta or {},
    }


_SQL_UPSERT = """
    INSERT INTO payoff_curve_summary (
        structure_id, reference_date,
        timestamp, aba,
        spot_ref, points_count,
        pl_min, pl_max, pl_at_spot_ref,
        breakevens_json, be_count,
        pos_ranges_json, pos_ranges_count,
        max_drawdown_like, meta_json
    ) VALUES (
        :structure_id, :reference_date,
        :timestamp, :aba,
        :spot_ref, :points_count,
        :pl_min, :pl_max, :pl_at_spot_ref,
        :breakevens_json, :be_count,
        :pos_ranges_json, :pos_ranges_count,
        :max_drawdown_like, :meta_json
    )
    ON CONFLICT(structure_id, reference_date) DO UPDATE SET
        timestamp          = excluded.timestamp,
        aba                = excluded.aba,
        spot_ref           = excluded.spot_ref,
        points_count       = excluded.points_count,
        pl_min             = excluded.pl_min,
        pl_max             = excluded.pl_max,
        pl_at_spot_ref     = excluded.pl_at_spot_ref,
        breakevens_json    = excluded.breakevens_json,
        be_count           = excluded.be_count,
        pos_ranges_json    = excluded.pos_ranges_json,
        pos_ranges_count   = excluded.pos_ranges_count,
        max_drawdown_like  = excluded.max_drawdown_like,
        meta_json          = excluded.meta_json
"""


def upsert_curve_summary(
    features: Dict[str, Any],
    _conn_override: Optional[sqlite3.Connection] = None,
) -> None:
    """
    Upsert por (structure_id, reference_date) — chave canônica.

    Patch 24: substituída chave legada (timestamp, aba)
              pela chave canônica (structure_id, reference_date).
              As colunas aba e timestamp permanecem na tabela como
              rastreabilidade opcional, sem participar da constraint UNIQUE.

    Patch 20: conexão própria (quando não há _conn_override) gerenciada
              internamente com try/finally, garantindo conn.close() mesmo
              em caso de exceção (ResourceWarning fix).

    Args:
        features       : dict retornado por compute_curve_features().
        _conn_override : conexão SQLite para injeção em testes. Quando
                         fornecida, o ciclo de vida da conexão é
                         responsabilidade do caller — esta função NÃO
                         fecha a conexão injetada.
    """
    structure_id   = features.get("structure_id")
    reference_date = features.get("reference_date")

    if not structure_id or not reference_date:
        raise ValueError(
            "features precisa de structure_id e reference_date para upsert canônico"
        )

    _owns_conn = _conn_override is None
    conn = _conn_override if _conn_override is not None else get_derived_db_connection()

    try:
        cur = conn.cursor()
        cur.execute(
            _SQL_UPSERT,
            {
                "structure_id":      structure_id,
                "reference_date":    reference_date,
                "timestamp":         features.get("timestamp"),
                "aba":               features.get("aba"),
                "spot_ref":          features.get("spot_ref"),
                "points_count":      features.get("points_count"),
                "pl_min":            features.get("pl_min"),
                "pl_max":            features.get("pl_max"),
                "pl_at_spot_ref":    features.get("pl_at_spot_ref"),
                "breakevens_json":   json.dumps(features.get("breakevens", [])),
                "be_count":          features.get("be_count"),
                "pos_ranges_json":   json.dumps(features.get("pos_ranges", [])),
                "pos_ranges_count":  features.get("pos_ranges_count"),
                "max_drawdown_like": features.get("max_drawdown_like"),
                "meta_json":         json.dumps(features.get("meta", {})),
            },
        )
        conn.commit()
    finally:
        # Fecha apenas conexões criadas por esta função.
        # Conexões injetadas via _conn_override são responsabilidade do caller.
        if _owns_conn:
            conn.close()
