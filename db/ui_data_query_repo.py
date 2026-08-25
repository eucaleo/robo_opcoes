from __future__ import annotations
import sqlite3
def connect(app_db_path):
    return connect_ui_data_db(app_db_path)
"""Repositorio local para consultas de leitura usadas por UIDataModel."""



def list_distinct_structure_ids(conn, table: str, sid_col: str) -> list[str]:
    """Retorna structure_ids distintos de uma tabela local ja detectada."""
    query = (
        f"SELECT DISTINCT CAST({sid_col} AS TEXT) AS structure_id "
        f"FROM {table} "
        f"WHERE {sid_col} IS NOT NULL "
        f"ORDER BY structure_id"
    )
    rows = conn.execute(query).fetchall()
    return [row["structure_id"] for row in rows]


def build_decision_subquery(select_parts, table: str) -> str:
    """Monta subquery de decisoes/consolidacoes para UIDataModel."""
    return f"(SELECT {', '.join(select_parts)} FROM {table}) t"


def fetch_decision_rows(conn, sql: str, params):
    """Executa consulta de decisoes/consolidacoes para UIDataModel."""
    return conn.execute(sql, params).fetchall()

# <!-- INICIO FRENTE 54G BUILD DECISIONS SQL REPO -->
def build_decisions_sql(subq: str, where_sql: str) -> str:
    # WHERE_SQL: marcador de guardrail para preservar interpolacao do parametro where_sql.
    return f"""
        SELECT
            t.timestamp, t.structure_id, t.aba, t.decision, t.level,
            t.pl_pct_of_max, t.dte_min, t.why, t.why_json,
            t.pl_atual, t.pl_max, t.spot_ref
        FROM {subq}
        {where_sql}
        ORDER BY t.timestamp DESC
    """

# <!-- FIM FRENTE 54G BUILD DECISIONS SQL REPO -->


# <!-- INICIO FRENTE 54H ISOLAR PAYOFF CURVE EXACT UI DATA -->

def build_payoff_curve_exact_sql(p, filter_col, payoff_table):
    return f"""
        SELECT {p['spot']} AS spot, {p['pl']} AS pl
        FROM {payoff_table}
        WHERE {filter_col} = ? AND {p['timestamp']} = ?
        ORDER BY spot
    """


def fetch_payoff_curve_exact_rows(
    conn,
    p,
    filter_col,
    filter_val,
    timestamp,
    payoff_table,
):
    sql_exact = build_payoff_curve_exact_sql(p, filter_col, payoff_table)
    return conn.execute(sql_exact, (filter_val, timestamp)).fetchall()

# <!-- FIM FRENTE 54H ISOLAR PAYOFF CURVE EXACT UI DATA -->


def build_payoff_curve_latest_timestamp_sql(p, filter_col, payoff_table):
    return f"""
            SELECT {p['timestamp']} AS ts
            FROM {payoff_table}
            WHERE {filter_col} = ?
            ORDER BY {p['timestamp']} DESC
            LIMIT 1
        """


def fetch_payoff_curve_latest_timestamp(conn, p, filter_col, filter_val, payoff_table):
    sql_ts = build_payoff_curve_latest_timestamp_sql(p, filter_col, payoff_table)
    return conn.execute(sql_ts, (filter_val,)).fetchone()


def build_canonical_payoff_curve_points_sql(filter_col, extra_cols=""):
    return (
        f"SELECT point_spot AS spot, point_pl AS pl{extra_cols} "
        f"FROM payoff_curve_points "
        f"WHERE {filter_col} = ? AND timestamp = ? "
        f"ORDER BY point_spot"
    )


def fetch_canonical_payoff_curve_points(
    conn,
    filter_col,
    filter_val,
    timestamp,
    extra_cols="",
):
    sql = build_canonical_payoff_curve_points_sql(filter_col, extra_cols)
    return conn.execute(sql, (filter_val, timestamp)).fetchall()


def build_latest_canonical_payoff_timestamp_sql(filter_col):
    return (
        f"SELECT timestamp FROM payoff_curve_points "
        f"WHERE {filter_col} = ? ORDER BY timestamp DESC LIMIT 1"
    )


def fetch_latest_canonical_payoff_timestamp(conn, filter_col, filter_val):
    sql_ts = build_latest_canonical_payoff_timestamp_sql(filter_col)
    row_ts = conn.execute(sql_ts, (filter_val,)).fetchone()
    if row_ts and row_ts["timestamp"]:
        return row_ts["timestamp"]
    return None


def build_legacy_payoff_curve_exact_sql(p, filter_col, payoff_table):
    return (
        f"SELECT {p['spot']} AS spot, {p['pl']} AS pl "
        f"FROM {payoff_table} "
        f"WHERE {filter_col} = ? AND {p['timestamp']} = ? "
        f"ORDER BY spot"
    )


def fetch_legacy_payoff_curve_exact_rows(
    conn, p, filter_col, filter_val, timestamp, payoff_table
):
    sql_exact = build_legacy_payoff_curve_exact_sql(p, filter_col, payoff_table)
    return conn.execute(sql_exact, (filter_val, timestamp)).fetchall()


def build_latest_legacy_payoff_timestamp_sql(p, filter_col, payoff_table):
    return (
        f"SELECT {p['timestamp']} AS ts FROM {payoff_table} "
        f"WHERE {filter_col} = ? ORDER BY ts DESC LIMIT 1"
    )


def fetch_latest_legacy_payoff_timestamp(conn, p, filter_col, filter_val, payoff_table):
    sql_ts = build_latest_legacy_payoff_timestamp_sql(p, filter_col, payoff_table)
    rts = conn.execute(sql_ts, (filter_val,)).fetchone()
    if rts and rts["ts"]:
        return rts["ts"]
    return None


def connect_ui_data_db(app_db_path):
    conn = sqlite3.connect(str(app_db_path))
    conn.row_factory = sqlite3.Row
    return conn

def fetch_latest_payoff_curve_timestamp(conn, p, filter_col, filter_val, payoff_table):
    sql_ts = build_payoff_curve_latest_timestamp_sql(p, filter_col, payoff_table)
    row = conn.execute(sql_ts, (filter_val,)).fetchone()
    if row and row["ts"]:
        return row["ts"]
    return None
