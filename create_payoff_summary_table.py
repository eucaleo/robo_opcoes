import sqlite3
db = sqlite3.connect('Data/derived.db')
db.execute("""
CREATE TABLE IF NOT EXISTS payoff_curve_summary (
  timestamp      TEXT NOT NULL,
  aba            TEXT NOT NULL,
  spot_ref       REAL,
  points_count   INTEGER NOT NULL,
  pl_min         REAL NOT NULL,
  pl_max         REAL NOT NULL,
  pl_at_spot_ref REAL,
  breakevens_json TEXT,
  be_count        INTEGER NOT NULL,
  pos_ranges_json TEXT,
  pos_ranges_count INTEGER NOT NULL,
  max_drawdown_like REAL,
  meta_json        TEXT,
  created_at       TEXT DEFAULT (datetime('now')),
  PRIMARY KEY (timestamp, aba)
);
""")
db.execute("""
CREATE INDEX IF NOT EXISTS idx_payoff_curve_summary_aba_ts
ON payoff_curve_summary (aba, timestamp);
""")
db.commit()
db.close()
print("Tabela payoff_curve_summary criada.")
