from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "dados" / "app.db"


DDL = """
CREATE TABLE IF NOT EXISTS rtd_option_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    codigo_opcao TEXT NOT NULL,
    ativo_base TEXT,

    call_put TEXT,
    strike REAL,
    vencimento TEXT,

    ultimo_preco REAL,
    ultima_quantidade REAL,

    bid REAL,
    ask REAL,
    volume REAL,

    iv REAL,
    delta REAL,
    gamma REAL,
    theta REAL,
    vega REAL,

    source TEXT NOT NULL DEFAULT 'rtd_links',
    raw_json TEXT,

    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(codigo_opcao)
);

CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo
ON rtd_option_quotes(codigo_opcao);

CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_ativo_base
ON rtd_option_quotes(ativo_base);

CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_vencimento
ON rtd_option_quotes(vencimento);

CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_call_put
ON rtd_option_quotes(call_put);
"""


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(DDL)
        conn.commit()

    print(f"[OK] Tabela rtd_option_quotes criada/verificada em: {DB_PATH}")


if __name__ == "__main__":
    main()
