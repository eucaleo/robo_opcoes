# db/schema.py

SCHEMA_SQL = """
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS payoff_curve_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    aba TEXT NOT NULL,
    spot_ref REAL,
    point_spot REAL NOT NULL,
    point_pl REAL NOT NULL,
    meta_json TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_payoff_timestamp_aba
ON payoff_curve_points(timestamp, aba);

CREATE INDEX IF NOT EXISTS idx_payoff_spot
ON payoff_curve_points(point_spot);

CREATE TABLE IF NOT EXISTS structure_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    aba TEXT NOT NULL,
    decision TEXT NOT NULL,
    ratio REAL,
    dte_min INTEGER,
    pl_atual REAL,
    pl_max REAL,
    pl_min REAL,
    spread_pct_medio REAL,
    why_json TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_decisions_timestamp_aba
ON structure_decisions(timestamp, aba);

CREATE INDEX IF NOT EXISTS idx_decisions_decision
ON structure_decisions(decision);

CREATE INDEX IF NOT EXISTS idx_decisions_ratio
ON structure_decisions(ratio);
"""
