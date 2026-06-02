# db/schema.py

SCHEMA_SQL = """
PRAGMA journal_mode = WAL;

-- Curva de payoff (por ponto) usada no seu projeto
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

-- Decisões estruturais
CREATE TABLE IF NOT EXISTS structure_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    aba TEXT NOT NULL,
    decision TEXT NOT NULL,
    level INTEGER,
    ratio REAL,
    pl_pct_of_max REAL,
    dte_min INTEGER,
    pl_atual REAL,
    pl_max REAL,
    pl_min REAL,
    spread_pct_medio REAL,
    why TEXT,
    why_json TEXT,
    spot_ref REAL,
    meta_json TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_decisions_timestamp_aba
ON structure_decisions(timestamp, aba);

CREATE INDEX IF NOT EXISTS idx_decisions_decision
ON structure_decisions(decision);

CREATE INDEX IF NOT EXISTS idx_decisions_ratio
ON structure_decisions(ratio);

-- Compat: tabela esperada por código antigo/viewers (payoff_points)
-- Vamos mapear para o mesmo conceito (pontos de payoff).
CREATE TABLE IF NOT EXISTS payoff_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    underlying_price REAL NOT NULL,
    payoff_value REAL NOT NULL,
    strategy_type TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_payoff_points_created_at
ON payoff_points(created_at);

CREATE INDEX IF NOT EXISTS idx_payoff_points_strategy
ON payoff_points(strategy_type);
"""


def ensure_derived_tables(conn):
    """
    Garante que as tabelas/índices existam.
    Espera receber uma conexão sqlite3 já aberta (padrão comum no restante do projeto).
    """
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()
