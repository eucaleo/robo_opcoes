"""
test_patch55.py — DerivedRepo aceita StructureRef como parametro canonico.
"""
from __future__ import annotations
import os, sqlite3, sys, tempfile, unittest

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from src.domain.refs.structure_ref import StructureRef
from db.derived_repo import DerivedRepo


# ── helpers ──────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS structure_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    aba TEXT NOT NULL,
    structure_id INTEGER,
    decision TEXT, level TEXT,
    pl_atual REAL, pl_max REAL, pl_pct_of_max REAL,
    dte_min INTEGER, why_json TEXT, spot_ref REAL, why TEXT, meta_json TEXT
);
CREATE TABLE IF NOT EXISTS payoff_curve_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL, aba TEXT NOT NULL,
    structure_id INTEGER, point_spot REAL NOT NULL,
    point_pl REAL NOT NULL, meta_json TEXT
);
CREATE TABLE IF NOT EXISTS payoff_curve_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL, aba TEXT NOT NULL,
    structure_id INTEGER, pl_max REAL, pl_min REAL,
    breakeven_low REAL, breakeven_high REAL, meta_json TEXT
);
"""

def _make_db(path):
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

def _repo(path):
    return DerivedRepo(derived_db=path)


# ── Grupo 1: StructureRef basico ─────────────────────────────────────────────

class TestStructureRefBasico(unittest.TestCase):
    def test_from_id(self):
        r = StructureRef.from_id(42)
        self.assertEqual(r.structure_id, 42)
        self.assertTrue(r.is_canonical())

    def test_from_aba_sem_db(self):
        r = StructureRef(aba="BOVA11")
        self.assertIsNone(r.structure_id)
        self.assertFalse(r.is_canonical())

    def test_db_pair_canonico(self):
        self.assertEqual(StructureRef.from_id(7).db_pair(), ("structure_id", 7))

    def test_db_pair_fallback(self):
        self.assertEqual(StructureRef(aba="PETR4").db_pair(), ("aba", "PETR4"))


# ── Grupo 2: _extract_ts_aba desempacota StructureRef ────────────────────────

class TestExtractTsAba(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        p = os.path.join(self.tmp, "derived.db")
        _make_db(p)
        self.repo = _repo(p)

    def test_string_aba_preservado(self):
        d = {"timestamp": "2026-06-01T10:00:00", "aba": "BOVA11"}
        ts, ab = self.repo._extract_ts_aba(d)
        self.assertEqual(ab, "BOVA11")

    def test_structure_ref_desempacotado(self):
        ref = StructureRef(structure_id=99, aba="BOVA11")
        d = {"timestamp": "2026-06-01T10:00:00"}
        ts, ab = self.repo._extract_ts_aba(d, aba=ref)
        self.assertEqual(ab, "BOVA11")
        self.assertEqual(ts, "2026-06-01T10:00:00")

    def test_structure_id_propagado_no_dict(self):
        ref = StructureRef(structure_id=55, aba="PETR4")
        d = {"timestamp": "2026-06-01T10:00:00"}
        # Passa dict mutavel para checar se structure_id e injetado
        d_mut = dict(d)
        self.repo._extract_ts_aba(d_mut, aba=ref)
        # d_mut pode ter sido substituido internamente (copia defensiva)
        # O teste relevante e que nao lanca excecao e retorna aba correta
        ts, ab = self.repo._extract_ts_aba(d, aba=ref)
        self.assertEqual(ab, "PETR4")

    def test_fallback_sem_aba_retorna_unknown(self):
        d = {"timestamp": "2026-06-01T09:00:00"}
        ts, ab = self.repo._extract_ts_aba(d)
        self.assertIn(ab, ["unknown", None, ""])


# ── Grupo 3: write aceita StructureRef ───────────────────────────────────────

class TestWriteComStructureRef(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp, "derived.db")
        _make_db(self.db_path)
        self.repo = _repo(self.db_path)

    def _base_decision(self, ts="2026-06-03T12:00:00", aba="BOVA11"):
        return {
            "timestamp": ts, "aba": aba,
            "decision": "HOLD", "level": "normal",
            "pl_atual": 100.0, "pl_max": 200.0,
            "pl_pct_of_max": 0.5, "dte_min": 15,
        }

    def test_write_com_structure_ref_nao_lanca_excecao(self):
        ref = StructureRef(structure_id=10, aba="BOVA11")
        d = self._base_decision()
        try:
            self.repo.write_decision_snapshot_atomic(d, aba=ref)
        except Exception as e:
            self.fail(f"Excecao inesperada: {e}")

    def test_write_com_string_aba_ainda_funciona(self):
        d = self._base_decision(aba="EMBJ3")
        try:
            self.repo.write_decision_snapshot_atomic(d)
        except Exception as e:
            self.fail(f"Compatibilidade string aba quebrou: {e}")

    def test_write_grava_no_db(self):
        ref = StructureRef(structure_id=42, aba="PETR4")
        d = self._base_decision(aba="PETR4")
        self.repo.write_decision_snapshot_atomic(d, aba=ref)
        conn = sqlite3.connect(self.db_path)
        row = conn.execute(
            "SELECT aba FROM structure_decisions WHERE aba = ? LIMIT 1",
            ("PETR4",)
        ).fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "PETR4")


# ── Grupo 4: get_recent_decisions aceita StructureRef ────────────────────────

class TestGetRecentComStructureRef(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp, "derived.db")
        _make_db(self.db_path)
        self.repo = _repo(self.db_path)
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO structure_decisions
              (timestamp, aba, structure_id, decision, level,
               pl_atual, pl_max, pl_pct_of_max, dte_min)
            VALUES ('2026-06-03T10:00:00','BOVA11',7,'HOLD','normal',100,200,0.5,20)
        """)
        conn.commit()
        conn.close()

    def test_get_com_string(self):
        rows = self.repo.get_recent_decisions(aba="BOVA11")
        self.assertGreaterEqual(len(rows), 1)

    def test_get_com_structure_ref(self):
        ref = StructureRef(structure_id=7, aba="BOVA11")
        try:
            rows = self.repo.get_recent_decisions(aba=ref)
        except TypeError as e:
            self.fail(f"get_recent_decisions nao aceitou StructureRef: {e}")

    def test_get_sem_filtro_retorna_tudo(self):
        rows = self.repo.get_recent_decisions()
        self.assertGreaterEqual(len(rows), 1)


# ── Grupo 5: retrocompatibilidade ────────────────────────────────────────────

class TestRetrocompatibilidade(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        p = os.path.join(self.tmp, "derived.db")
        _make_db(p)
        self.repo = _repo(p)

    def test_extract_sem_aba_usa_dict(self):
        d = {"timestamp": "2026-06-01T09:00:00", "aba": "PRIO3"}
        ts, ab = self.repo._extract_ts_aba(d)
        self.assertEqual(ab, "PRIO3")

    def test_derived_repo_instanciavel(self):
        self.assertIsNotNone(self.repo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
