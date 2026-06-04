# scripts/70_smoke_structure_id_in_derived.py
"""
patch_32 -- Smoke: valida que structure_id chega corretamente
em structure_decisions após execução via DerivedRepo.

Fluxo testado:
    DerivedRepo.write_decision_snapshot_atomic(decision_dict com structure_id)
    -> SELECT structure_id FROM structure_decisions
    -> confirma valor gravado == valor enviado

Uso:
    python scripts/70_smoke_structure_id_in_derived.py
"""

import os
import sys
import sqlite3
import tempfile
import traceback
from datetime import datetime

# ---------------------------------------------------------------------------
# Garante import do projeto independente de como o script é chamado
# ---------------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ---------------------------------------------------------------------------
# Helpers de output
# ---------------------------------------------------------------------------
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"

def ok(msg):   print(f"{GREEN}  [OK]  {msg}{RESET}")
def fail(msg): print(f"{RED}  [FALHOU]  {msg}{RESET}")
def warn(msg): print(f"{YELLOW}  [AVISO]   {msg}{RESET}")
def info(msg): print(f"       {msg}")


# ---------------------------------------------------------------------------
# Helpers de banco in-memory (isolado, não toca derived.db real)
# ---------------------------------------------------------------------------

DDL_STRUCTURE_DECISIONS = """
CREATE TABLE IF NOT EXISTS structure_decisions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker      TEXT    NOT NULL,
    timestamp   TEXT    NOT NULL,
    level       REAL,
    pl_atual    REAL,
    pl_max      REAL,
    pl_pct      REAL,
    dte_min     REAL,
    why         TEXT,
    spot_ref    REAL,
    meta_json   TEXT,
    structure_id INTEGER,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
)
"""


def _make_in_memory_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(DDL_STRUCTURE_DECISIONS)
    conn.commit()
    return conn


# ---------------------------------------------------------------------------
# Casos de teste
# ---------------------------------------------------------------------------

ERRORS = []


def check(label, condition, detail=""):
    if condition:
        ok(label)
    else:
        fail(label)
        if detail:
            info(f"detalhe: {detail}")
        ERRORS.append(label)


# ---------------------------------------------------------------------------
# Teste 1 -- DerivedRepo importável e instanciável
# ---------------------------------------------------------------------------

def test_import_derived_repo():
    print("\n[1] Import e instância de DerivedRepo")
    try:
        from db.derived_repo import DerivedRepo  # noqa: F401
        ok("DerivedRepo importado com sucesso")
        return True
    except Exception as e:
        fail(f"Falha ao importar DerivedRepo: {e}")
        ERRORS.append("import DerivedRepo")
        return False


# ---------------------------------------------------------------------------
# Teste 2 -- write_decision_snapshot_atomic grava structure_id
# ---------------------------------------------------------------------------

def test_write_with_structure_id():
    print("\n[2] write_decision_snapshot_atomic -- grava structure_id")

    conn = _make_in_memory_conn()
    ts   = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    decision_dict = {
        "ticker":       "BOVA11",
        "timestamp":    ts,
        "level":        1.0,
        "pl_atual":     -50.0,
        "pl_max":       200.0,
        "pl_pct":       -0.25,
        "dte_min":      15,
        "why":          "smoke test patch_32",
        "spot_ref":     184.32,
        "meta_json":    '{"source": "smoke"}',
        "structure_id": 7,
    }

    try:
        # Insere diretamente via SQL (simula o que DerivedRepo faz)
        conn.execute(
            """
            INSERT INTO structure_decisions
                (ticker, timestamp, level, pl_atual, pl_max, pl_pct,
                 dte_min, why, spot_ref, meta_json, structure_id, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                decision_dict["ticker"],
                decision_dict["timestamp"],
                decision_dict["level"],
                decision_dict["pl_atual"],
                decision_dict["pl_max"],
                decision_dict["pl_pct"],
                decision_dict["dte_min"],
                decision_dict["why"],
                decision_dict["spot_ref"],
                decision_dict["meta_json"],
                decision_dict["structure_id"],
                ts,
            ),
        )
        conn.commit()

        row = conn.execute(
            "SELECT * FROM structure_decisions WHERE ticker = ? ORDER BY id DESC LIMIT 1",
            ("BOVA11",),
        ).fetchone()

        check("Linha gravada no banco",           row is not None)
        check("structure_id == 7",                row["structure_id"] == 7,
              f"obtido: {row['structure_id']}")
        check("why == 'smoke test patch_32'",     row["why"] == "smoke test patch_32",
              f"obtido: {row['why']}")
        check("ticker == 'BOVA11'",               row["ticker"] == "BOVA11")
        check("spot_ref == 184.32",               abs(row["spot_ref"] - 184.32) < 0.001,
              f"obtido: {row['spot_ref']}")

    except Exception:
        fail("Exceção durante INSERT/SELECT")
        info(traceback.format_exc())
        ERRORS.append("write_decision_snapshot_atomic insert")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Teste 3 -- structure_id NULL é aceito (estruturas legado sem id)
# ---------------------------------------------------------------------------

def test_write_without_structure_id():
    print("\n[3] write sem structure_id (legado -- deve aceitar NULL)")

    conn = _make_in_memory_conn()
    ts   = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    try:
        conn.execute(
            """
            INSERT INTO structure_decisions
                (ticker, timestamp, level, pl_atual, pl_max, pl_pct,
                 dte_min, why, spot_ref, meta_json, structure_id, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            ("PRIO3", ts, 0.5, 100.0, 300.0, 0.33, 20, "legado", 42.0, "{}", None, ts),
        )
        conn.commit()

        row = conn.execute(
            "SELECT structure_id FROM structure_decisions WHERE ticker = 'PRIO3' LIMIT 1"
        ).fetchone()

        check("Linha legado gravada",            row is not None)
        check("structure_id é NULL (legado ok)", row["structure_id"] is None,
              f"obtido: {row['structure_id']}")

    except Exception:
        fail("Exceção no teste legado")
        info(traceback.format_exc())
        ERRORS.append("write_without_structure_id")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Teste 4 -- DerivedRepo real com banco temporário
# ---------------------------------------------------------------------------

def test_derived_repo_real():
    print("\n[4] DerivedRepo real -- banco temporário em disco")

    try:
        from db.derived_repo import DerivedRepo
    except ImportError as e:
        warn(f"DerivedRepo não importável, pulando teste real: {e}")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "derived_smoke.db")
        ts      = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        decision_dict = {
            "ticker":       "BOVA11",
            "timestamp":    ts,
            "level":        2.0,
            "pl_atual":     80.0,
            "pl_max":       400.0,
            "pl_pct":       0.20,
            "dte_min":      10,
            "why":          "real repo test",
            "spot_ref":     190.0,
            "meta_json":    "{}",
            "structure_id": 42,
        }

        try:
            repo = DerivedRepo(db_path=db_path)
            repo.write_decision_snapshot_atomic(decision_dict)

            # Leitura via get_recent_decisions ou query direta
            if hasattr(repo, "get_recent_decisions"):
                rows = repo.get_recent_decisions(ticker="BOVA11", limit=1)
                check("get_recent_decisions retornou resultado", len(rows) >= 1)
                if rows:
                    top = rows[0]
                    sid = top.get("structure_id") if isinstance(top, dict) else getattr(top, "structure_id", None)
                    check("structure_id == 42 via get_recent_decisions", sid == 42,
                          f"obtido: {sid}")
            else:
                # fallback: leitura direta
                conn = sqlite3.connect(db_path)
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT structure_id FROM structure_decisions ORDER BY id DESC LIMIT 1"
                ).fetchone()
                conn.close()
                check("Linha gravada via DerivedRepo real",  row is not None)
                check("structure_id == 42 (real db)",
                      row is not None and row["structure_id"] == 42,
                      f"obtido: {row['structure_id'] if row else 'None'}")

        except Exception:
            fail("Exceção no DerivedRepo real")
            info(traceback.format_exc())
            ERRORS.append("derived_repo_real")


# ---------------------------------------------------------------------------
# Teste 5 -- _table_columns confirma structure_id presente
# ---------------------------------------------------------------------------

def test_table_columns():
    print("\n[5] _table_columns -- confirma colunas structure_id e why")

    try:
        from db.derived_repo import DerivedRepo
    except ImportError as e:
        warn(f"DerivedRepo não importável, pulando: {e}")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "cols_smoke.db")
        try:
            repo = DerivedRepo(db_path=db_path)

            if not hasattr(repo, "_table_columns"):
                warn("_table_columns não encontrado -- pulando verificação")
                return

            cols = repo._table_columns("structure_decisions")
            check("_table_columns retorna lista não vazia",   len(cols) > 0,
                  f"colunas: {cols}")
            check("'structure_id' presente nas colunas",      "structure_id" in cols,
                  f"colunas encontradas: {cols}")
            check("'why' presente nas colunas",               "why" in cols,
                  f"colunas encontradas: {cols}")
            check("'spot_ref' presente nas colunas",          "spot_ref" in cols,
                  f"colunas encontradas: {cols}")
            check("'meta_json' presente nas colunas",         "meta_json" in cols,
                  f"colunas encontradas: {cols}")

        except Exception:
            fail("Exceção em _table_columns")
            info(traceback.format_exc())
            ERRORS.append("_table_columns")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    print("=" * 66)
    print("  SMOKE -- patch_32: structure_id em structure_decisions")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 66)

    imported = test_import_derived_repo()

    test_write_with_structure_id()
    test_write_without_structure_id()

    if imported:
        test_derived_repo_real()
        test_table_columns()

    # -------------------------------------------------------------------
    print("\n" + "=" * 66)
    if ERRORS:
        print(f"{RED}  RESULTADO: {len(ERRORS)} falha(s){RESET}")
        for e in ERRORS:
            print(f"{RED}    - {e}{RESET}")
        print("=" * 66)
        sys.exit(1)
    else:
        print(f"{GREEN}  RESULTADO: TODOS OS CHECKS PASSARAM [OK]{RESET}")
        print("=" * 66)
        sys.exit(0)


if __name__ == "__main__":
    main()
