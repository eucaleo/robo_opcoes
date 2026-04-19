# db/schema_excel.py

SCHEMA_EXCEL_SQL = """
-- Configurações (1 linha por parâmetro)
CREATE TABLE IF NOT EXISTS robo_config (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parametro TEXT NOT NULL,
  valor TEXT,
  descricao TEXT,
  imported_at TEXT DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_robo_config_parametro
ON robo_config(parametro);

-- Snapshot agregado por ABA (ANALISE_ROBO)
CREATE TABLE IF NOT EXISTS robo_snapshot (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT,                -- opcional (se você tiver; na planilha não tem nesta aba)
  aba TEXT NOT NULL,
  spot REAL,
  num_pernas INTEGER,
  dte_min INTEGER,
  pl_realista_total REAL,
  delta_liq REAL,
  gamma_liq REAL,
  theta_liq REAL,
  vega_liq REAL,
  spread_medio REAL,
  spread_pct_medio REAL,
  alertas_v2 TEXT,
  imported_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS ix_robo_snapshot_aba ON robo_snapshot(aba);

-- Snapshot por perna (ANALISE_ROBO_LEGS)
CREATE TABLE IF NOT EXISTS robo_legs_snapshot (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  aba TEXT NOT NULL,
  ativo TEXT,
  cv TEXT,                       -- C/V
  call_put TEXT,                 -- CALL/PUT
  quant INTEGER,
  valor_executado REAL,
  bid REAL,
  ask REAL,
  spread REAL,
  spread_pct REAL,
  iv REAL,
  delta REAL,
  gamma REAL,
  theta REAL,
  vega REAL,
  strike REAL,
  vencimento TEXT,
  dte INTEGER,
  pl_realista REAL,
  imported_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS ix_robo_legs_snapshot_ts ON robo_legs_snapshot(timestamp);
CREATE INDEX IF NOT EXISTS ix_robo_legs_snapshot_aba ON robo_legs_snapshot(aba);
CREATE INDEX IF NOT EXISTS ix_robo_legs_snapshot_ativo ON robo_legs_snapshot(ativo);

-- Histórico por perna (HIST_ROBO) (parece similar ao legs, mas sem alguns campos)
CREATE TABLE IF NOT EXISTS robo_legs_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  aba TEXT NOT NULL,
  ativo TEXT,
  cv TEXT,
  quant INTEGER,
  valor_executado REAL,
  bid REAL,
  ask REAL,
  delta REAL,
  gamma REAL,
  theta REAL,
  vega REAL,
  pl_realista REAL,
  imported_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS ix_robo_legs_history_ts ON robo_legs_history(timestamp);
CREATE INDEX IF NOT EXISTS ix_robo_legs_history_aba ON robo_legs_history(aba);

-- Encerramentos manuais
CREATE TABLE IF NOT EXISTS encerramentos_manuais (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  data TEXT,
  aba TEXT,
  codigo TEXT,
  tipo TEXT,
  qtd INTEGER,
  preco_real REAL,
  motivo TEXT,
  observacao TEXT,
  imported_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS ix_encerramentos_data ON encerramentos_manuais(data);
"""
