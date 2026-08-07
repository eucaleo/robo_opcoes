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


-- Resumo canônico da curva de payoff por estrutura/data de referência.
CREATE TABLE IF NOT EXISTS payoff_curve_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_id INTEGER NOT NULL,
    reference_date TEXT NOT NULL,
    timestamp TEXT,
    aba TEXT,
    spot_ref REAL,
    points_count INTEGER NOT NULL DEFAULT 0,
    pl_min REAL,
    pl_max REAL,
    pl_at_spot_ref REAL,
    breakevens_json TEXT,
    be_count INTEGER NOT NULL DEFAULT 0,
    pos_ranges_json TEXT,
    pos_ranges_count INTEGER NOT NULL DEFAULT 0,
    max_drawdown_like REAL,
    meta_json TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(structure_id, reference_date)
);

CREATE INDEX IF NOT EXISTS idx_payoff_summary_sid_ref
ON payoff_curve_summary(structure_id, reference_date);

CREATE INDEX IF NOT EXISTS idx_payoff_summary_reference_date
ON payoff_curve_summary(reference_date);

CREATE INDEX IF NOT EXISTS idx_payoff_summary_timestamp_aba
ON payoff_curve_summary(timestamp, aba);


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

-- Eventos operacionais de estruturas
CREATE TABLE IF NOT EXISTS structure_events (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_id   INTEGER NOT NULL,
    leg_id         INTEGER,
    event_type     TEXT    NOT NULL,
    event_status   TEXT    NOT NULL DEFAULT 'registered',
    event_date     TEXT    NOT NULL,
    quantity       INTEGER,
    price          REAL,
    symbol         TEXT,
    source         TEXT    NOT NULL DEFAULT 'manual',
    notes          TEXT,
    metadata_json  TEXT,
    created_at     TEXT    NOT NULL,
    updated_at     TEXT    NOT NULL,
    FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE,
    FOREIGN KEY (leg_id) REFERENCES structure_legs(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_structure_events_structure_id
ON structure_events(structure_id);

CREATE INDEX IF NOT EXISTS idx_structure_events_leg_id
ON structure_events(leg_id);

CREATE INDEX IF NOT EXISTS idx_structure_events_event_type
ON structure_events(event_type);

CREATE INDEX IF NOT EXISTS idx_structure_events_event_status
ON structure_events(event_status);

CREATE INDEX IF NOT EXISTS idx_structure_events_event_date
ON structure_events(event_date);

CREATE INDEX IF NOT EXISTS idx_structure_events_structure_date
ON structure_events(structure_id, event_date);
"""


def ensure_derived_tables(conn):
    """
    Garante que as tabelas/índices existam.
    Espera receber uma conexão sqlite3 já aberta (padrão comum no restante do projeto).
    """
    cur = conn.cursor()
    cur.executescript(SCHEMA_SQL)
    conn.commit()
