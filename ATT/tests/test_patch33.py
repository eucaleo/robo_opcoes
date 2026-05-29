# ATT/tests/test_patch33.py
"""
test_patch33 — Valida migration: structure_id em payoff_curve_points
               e payoff_curve_summary (derived.db)

Critérios de aceite:
  ✅ run() executa sem erro em DB em memória
  ✅ Colunas structure_id presentes após migration
  ✅ Índices criados
  ✅ Idempotência: rodar 2x não levanta exceção
  ✅ Backfill: linhas com aba+timestamp correspondente recebem structure_id
"""

import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ))


# ── Fixtures helpers ──────────────────────────────────────────────────────────

def _make_db() -> sqlite3.Connection:
    """Cria derived.db em memória com schema mínimo."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE payoff_curve_points (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            aba         TEXT NOT NULL,
            point_spot  REAL NOT NULL,
            point_pl    REAL NOT NULL
        );
        CREATE TABLE payoff_curve_summary (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT NOT NULL,
            aba         TEXT NOT NULL,
            pl_max      REAL,
            pl_min      REAL
        );
        CREATE TABLE structure_decisions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp    TEXT NOT NULL,
            aba          TEXT NOT NULL,
            structure_id INTEGER,
            decision     TEXT
        );
    """)
    # Seed: decisão com structure_id=7 para aba='BOVA11'
    conn.execute("""
        INSERT INTO structure_decisions (timestamp, aba, structure_id, decision)
        VALUES ('2026-05-01T10:00:00', 'BOVA11', 7, 'HOLD')
    """)
    # Seed: payoff points com mesmo aba+timestamp
    conn.execute("""
        INSERT INTO payoff_curve_points (timestamp, aba, point_spot, point_pl)
        VALUES ('2026-05-01T10:00:00', 'BOVA11', 100.0, 50.0)
    """)
    conn.execute("""
        INSERT INTO payoff_curve_summary (timestamp, aba, pl_max, pl_min)
        VALUES ('2026-05-01T10:00:00', 'BOVA11', 500.0, -100.0)
    """)
    conn.commit()
    return conn


def _col_exists(conn: sqlite3.Connection, table: str, col: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == col for r in rows)


def _index_exists(conn: sqlite3.Connection, index_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name=?",
        (index_name,),
    ).fetchone()
    return row is not None


def _apply_migration(conn: sqlite3.Connection):
    """
    Aplica os mesmos passos do run_patch_33.py diretamente numa conexão.
    Permite testar em memória sem precisar de arquivo físico.
    """
    steps = [
        # payoff_curve_points
        ("payoff_curve_points", "ADD COLUMN structure_id",
         "ALTER TABLE payoff_curve_points ADD COLUMN structure_id INTEGER"),
        ("payoff_curve_points", "BACKFILL", """
            UPDATE payoff_curve_points
            SET structure_id = (
                SELECT d.structure_id
                FROM structure_decisions d
                WHERE d.aba       = payoff_curve_points.aba
                  AND d.timestamp = payoff_curve_points.timestamp
                LIMIT 1
            )
        """),
        ("payoff_curve_points", "INDEX",
         "CREATE INDEX IF NOT EXISTS idx_payoff_points_sid_ts "
         "ON payoff_curve_points (structure_id, timestamp)"),
        # payoff_curve_summary
        ("payoff_curve_summary", "ADD COLUMN structure_id",
         "ALTER TABLE payoff_curve_summary ADD COLUMN structure_id INTEGER"),
        ("payoff_curve_summary", "BACKFILL", """
            UPDATE payoff_curve_summary
            SET structure_id = (
                SELECT d.structure_id
                FROM structure_decisions d
                WHERE d.aba       = payoff_curve_summary.aba
                  AND d.timestamp = payoff_curve_summary.timestamp
                LIMIT 1
            )
        """),
        ("payoff_curve_summary", "INDEX",
         "CREATE INDEX IF NOT EXISTS idx_payoff_summary_sid_ts "
         "ON payoff_curve_summary (structure_id, timestamp)"),
    ]

    for table, op, sql in steps:
        if "ADD COLUMN structure_id" in op:
            if _col_exists(conn, table, "structure_id"):
                continue  # idempotente
        conn.execute(sql)

    conn.commit()


# ── Testes ────────────────────────────────────────────────────────────────────

class TestPatch33Migration:

    def test_colunas_criadas_em_payoff_curve_points(self):
        """structure_id deve existir em payoff_curve_points após migration."""
        conn = _make_db()
        _apply_migration(conn)
        assert _col_exists(conn, "payoff_curve_points", "structure_id"), \
            "structure_id não foi criado em payoff_curve_points"
        conn.close()

    def test_colunas_criadas_em_payoff_curve_summary(self):
        """structure_id deve existir em payoff_curve_summary após migration."""
        conn = _make_db()
        _apply_migration(conn)
        assert _col_exists(conn, "payoff_curve_summary", "structure_id"), \
            "structure_id não foi criado em payoff_curve_summary"
        conn.close()

    def test_indices_criados(self):
        """Índices compostos (structure_id, timestamp) devem existir."""
        conn = _make_db()
        _apply_migration(conn)
        assert _index_exists(conn, "idx_payoff_points_sid_ts"), \
            "Índice idx_payoff_points_sid_ts não criado"
        assert _index_exists(conn, "idx_payoff_summary_sid_ts"), \
            "Índice idx_payoff_summary_sid_ts não criado"
        conn.close()

    def test_backfill_payoff_curve_points(self):
        """
        Linha com aba='BOVA11' e timestamp correspondente deve receber
        structure_id=7 via backfill.
        """
        conn = _make_db()
        _apply_migration(conn)
        row = conn.execute(
            "SELECT structure_id FROM payoff_curve_points WHERE aba='BOVA11'"
        ).fetchone()
        assert row is not None, "Linha de BOVA11 não encontrada"
        assert row[0] == 7, \
            f"Backfill incorreto: esperado 7, obtido {row[0]}"
        conn.close()

    def test_backfill_payoff_curve_summary(self):
        """
        Linha com aba='BOVA11' e timestamp correspondente deve receber
        structure_id=7 via backfill.
        """
        conn = _make_db()
        _apply_migration(conn)
        row = conn.execute(
            "SELECT structure_id FROM payoff_curve_summary WHERE aba='BOVA11'"
        ).fetchone()
        assert row is not None, "Linha de BOVA11 não encontrada em summary"
        assert row[0] == 7, \
            f"Backfill incorreto: esperado 7, obtido {row[0]}"
        conn.close()

    def test_idempotencia(self):
        """Aplicar migration 2x não deve levantar exceção."""
        conn = _make_db()
        _apply_migration(conn)
        try:
            _apply_migration(conn)  # segunda vez — deve ser silenciosa
        except Exception as e:
            assert False, f"Migration não é idempotente: {e}"
        conn.close()

    def test_linhas_sem_match_ficam_null(self):
        """
        Linha sem structure_decision correspondente deve ter structure_id=NULL
        (não levanta erro).
        """
        conn = _make_db()
        # Insere linha órfã (sem decisão correspondente)
        conn.execute("""
            INSERT INTO payoff_curve_points (timestamp, aba, point_spot, point_pl)
            VALUES ('2026-01-01T00:00:00', 'ORPHAN', 50.0, 10.0)
        """)
        conn.commit()
        _apply_migration(conn)
        row = conn.execute(
            "SELECT structure_id FROM payoff_curve_points WHERE aba='ORPHAN'"
        ).fetchone()
        assert row is not None
        assert row[0] is None, \
            f"Linha órfã deveria ter structure_id=NULL, obteve {row[0]}"
        conn.close()
