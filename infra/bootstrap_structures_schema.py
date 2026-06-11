# infra/bootstrap_structures_schema.py
"""
Garante o schema SQLite da aplicação (idempotente).
Cria tabelas e índices se ainda não existirem.

alteracao_72: adicionada tabela structure_audit_log para rastreabilidade de mudancas.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path("dados/app.db")


# ---------------------------------------------------------------------------
# DDL principal
# ---------------------------------------------------------------------------

def ensure_structures_schema(db_path: Path = DB_PATH) -> None:
    """Cria todas as tabelas e índices necessários (idempotente)."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        # ------------------------------------------------------------------ #
        # structures                                                           #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structures (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                name             TEXT    NOT NULL,
                underlying_asset TEXT    NOT NULL,
                alias_legacy_aba TEXT,
                status           TEXT    NOT NULL DEFAULT 'active',
                notes            TEXT,
                created_at       TEXT    NOT NULL,
                updated_at       TEXT    NOT NULL
            )
            """
        )

        # ------------------------------------------------------------------ #
        # structure_legs                                                       #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structure_legs (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id    INTEGER NOT NULL,
                position_side   TEXT    NOT NULL,
                option_type     TEXT    NOT NULL,
                symbol          TEXT,
                strike          REAL    NOT NULL,
                expiration_date TEXT    NOT NULL,
                quantity        INTEGER NOT NULL,
                premium         REAL,
                multiplier      REAL    NOT NULL DEFAULT 1,
                leg_order       INTEGER NOT NULL,
                notes           TEXT,
                created_at      TEXT    NOT NULL,
                updated_at      TEXT    NOT NULL,
                FOREIGN KEY (structure_id) REFERENCES structures(id) ON DELETE CASCADE
            )
            """
        )

        # ------------------------------------------------------------------ #
        # pricing_executions                                                   #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pricing_executions (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at        TEXT    NOT NULL,
                structure_id      INTEGER,
                underlying_asset  TEXT,
                reference_date    TEXT,
                execution_status  TEXT,
                execution_engine  TEXT,
                error_message     TEXT,
                duration_ms       INTEGER,
                number_of_legs    INTEGER,
                total_quantity    INTEGER,
                theoretical_value REAL,
                pricing_payload   TEXT,
                result            TEXT,
                FOREIGN KEY (structure_id) REFERENCES structures(id)
            )
            """
        )

        # ------------------------------------------------------------------ #
        # structure_audit_log  [alteracao_72]                                      #
        # Rastreia toda mutacao em structures: CREATE, UPDATE, ARCHIVE,        #
        # ADD_LEG, REPLACE_LEGS.                                               #
        # before_json / after_json sao snapshots do estado da estrutura        #
        # (sem legs) serializado em JSON.                                      #
        # changed_by e reservado para autenticacao futura; NULL por ora.       #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS structure_audit_log (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                structure_id INTEGER NOT NULL,
                action       TEXT    NOT NULL,
                changed_by   TEXT,
                changed_at   TEXT    NOT NULL,
                before_json  TEXT,
                after_json   TEXT,
                notes        TEXT,
                FOREIGN KEY (structure_id) REFERENCES structures(id)
            )
            """
        )

        # ------------------------------------------------------------------ #
        # Indices -- structures                                                #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structures_underlying_asset
            ON structures(underlying_asset)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structures_alias_legacy_aba
            ON structures(alias_legacy_aba)
            """
        )

        # ------------------------------------------------------------------ #
        # Indices -- structure_legs                                            #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_legs_structure_id
            ON structure_legs(structure_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_structure_legs_structure_id_leg_order
            ON structure_legs(structure_id, leg_order)
            """
        )

        # ------------------------------------------------------------------ #
        # Indices -- pricing_executions                                        #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_pricing_executions_structure_id
            ON pricing_executions(structure_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_pricing_executions_created_at
            ON pricing_executions(created_at)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_pricing_executions_status
            ON pricing_executions(execution_status)
            """
        )

        # ------------------------------------------------------------------ #
        # Indices -- structure_audit_log  [alteracao_72]                          #
        # ------------------------------------------------------------------ #
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_audit_log_structure_id
            ON structure_audit_log(structure_id)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at
            ON structure_audit_log(changed_at)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_audit_log_action
            ON structure_audit_log(action)
            """
        )

        conn.commit()


# ---------------------------------------------------------------------------
# Bootstrap auxiliar de pricing_executions (alteracao_23)
# Mantido como função independente para uso em migrações pontuais.
# ---------------------------------------------------------------------------

_PRICING_EXECUTIONS_DDL = """
CREATE TABLE IF NOT EXISTS pricing_executions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_id    INTEGER NOT NULL,
    reference_date  TEXT    NOT NULL,
    status          TEXT    NOT NULL DEFAULT 'ok',
    canonical_input TEXT    NULL,
    engine_result   TEXT    NULL,
    error_message   TEXT    NULL,
    executed_at     TEXT    NOT NULL,
    created_at      TEXT    NOT NULL
);
"""

_PRICING_EXECUTIONS_INDEXES: list[str] = [
    "CREATE INDEX IF NOT EXISTS idx_pricing_executions_structure_id   ON pricing_executions (structure_id);",
    "CREATE INDEX IF NOT EXISTS idx_pricing_executions_reference_date ON pricing_executions (reference_date);",
    "CREATE INDEX IF NOT EXISTS idx_pricing_executions_status         ON pricing_executions (status);",
    "CREATE INDEX IF NOT EXISTS idx_pricing_executions_structure_date ON pricing_executions (structure_id, reference_date);",
]


def bootstrap_pricing_executions(conn: sqlite3.Connection) -> None:
    """Garante tabela pricing_executions e seus índices (idempotente)."""
    cur = conn.cursor()
    cur.executescript(_PRICING_EXECUTIONS_DDL)
    for idx in _PRICING_EXECUTIONS_INDEXES:
        cur.execute(idx)
    conn.commit()
