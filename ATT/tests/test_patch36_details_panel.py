# tests/test_patch36_details_panel.py
"""
Testes Patch_36 -- details_panel.py
Cobre:
  - _resolve_structure_key
  - _get_latest_snapshot_timestamp_for_structure
  - _fetch_latest_decision_from_derived
  - _fetch_payoff_points_from_derived
  - _fetch_audit_info_from_derived
  - update_decision (sem fallback aba)
  - _on_recalculate_click (sem fallback aba)

Estratégia headless:
  - Nenhum tk.Tk() é instanciado -- evita falha em ambiente sem display
    e conflito com o fake-tkinter injetado pelo patch_35.
  - DetailsPanel é criado via __new__ com widgets substituídos por MagicMock.
"""
import sys
import sqlite3
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Fixture: instância isolada de DetailsPanel sem Tkinter real
# ---------------------------------------------------------------------------

@pytest.fixture
def panel(tmp_path):
    from UI.components.details_panel import DetailsPanel

    p = DetailsPanel.__new__(DetailsPanel)

    p._on_recalculate_cb      = None
    p._recalc_in_progress     = False
    p._last_recalc_signature  = None
    p._current_decision       = None
    p._project_root           = tmp_path

    for attr in (
        "btn_recalculate", "lbl_recalc_status", "timestamp_label",
        "structure_label", "decision_label", "level_label",
        "pl_atual_label", "pl_max_label", "ratio_label", "dte_label",
        "spot_ref_label", "breakevens_label", "source_label",
        "created_at_label", "why_text",
    ):
        setattr(p, attr, MagicMock())

    yield p

    # Teardown: garante que UI.components não vaza estado tkinter
    for _k in [k for k in sys.modules if k.startswith("UI.components")]:
        sys.modules.pop(_k, None)

# ---------------------------------------------------------------------------
# Fixture: app.db com tabelas snapshot
# ---------------------------------------------------------------------------

@pytest.fixture
def app_db(tmp_path):
    db = tmp_path / "dados" / "app.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db))
    con.executescript("""
        CREATE TABLE robo_legs_snapshot (
            structure_id INTEGER,
            timestamp    TEXT
        );
        CREATE TABLE robo_snapshot (
            structure_id INTEGER,
            timestamp    TEXT
        );
        CREATE TABLE rtd_analise_robo_legs (
            structure_id INTEGER,
            timestamp    TEXT
        );
    """)
    con.commit()
    con.close()
    return db


# ---------------------------------------------------------------------------
# Fixture: derived.db com tabelas canônicas
# ---------------------------------------------------------------------------

@pytest.fixture
def derived_db(tmp_path):
    db = tmp_path / "dados" / "derived.db"
    db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db))
    con.executescript("""
        CREATE TABLE structure_decisions (
            structure_id  INTEGER,
            timestamp     TEXT,
            decision      TEXT,
            level         INTEGER,
            pl_atual      REAL,
            pl_max        REAL,
            pl_pct_of_max REAL,
            dte_min       INTEGER,
            spot_ref      REAL,
            meta_json     TEXT,
            created_at    TEXT,
            why_json      TEXT
        );
        CREATE TABLE payoff_curve_points (
            structure_id INTEGER,
            point_spot   REAL,
            point_pl     REAL
        );
    """)
    con.commit()
    con.close()
    return db


# ===========================================================================
# 1. _resolve_structure_key
# ===========================================================================

class TestResolveStructureKey:

    def test_int_passthrough(self, panel):
        assert panel._resolve_structure_key(7) == 7

    def test_string_numeric(self, panel):
        assert panel._resolve_structure_key("42") == 42

    def test_string_zero(self, panel):
        assert panel._resolve_structure_key("0") == 0

    def test_none_raises(self, panel):
        with pytest.raises(ValueError, match="structure_id inválido"):
            panel._resolve_structure_key(None)

    def test_alpha_string_raises(self, panel):
        with pytest.raises(ValueError, match="structure_id inválido"):
            panel._resolve_structure_key("WING")

    def test_float_string_raises(self, panel):
        """'3.5' não é inteiro puro -- deve lançar ValueError."""
        with pytest.raises(ValueError):
            panel._resolve_structure_key("3.5")


# ===========================================================================
# 2. _get_latest_snapshot_timestamp_for_structure
# ===========================================================================

class TestGetLatestSnapshotTimestamp:

    def test_retorna_timestamp_de_robo_legs_snapshot(self, panel, app_db):
        con = sqlite3.connect(str(app_db))
        con.execute(
            "INSERT INTO robo_legs_snapshot VALUES (?, ?)", (5, "2025-01-10 10:00:00")
        )
        con.commit()
        con.close()

        panel._project_root = app_db.parent.parent
        ts = panel._get_latest_snapshot_timestamp_for_structure(5)
        assert ts == "2025-01-10 10:00:00"

    def test_retorna_max_quando_multiplos_registros(self, panel, app_db):
        con = sqlite3.connect(str(app_db))
        con.executemany(
            "INSERT INTO robo_legs_snapshot VALUES (?, ?)",
            [(5, "2025-01-08 08:00:00"), (5, "2025-01-10 12:00:00"), (5, "2025-01-09 09:00:00")],
        )
        con.commit()
        con.close()

        panel._project_root = app_db.parent.parent
        ts = panel._get_latest_snapshot_timestamp_for_structure(5)
        assert ts == "2025-01-10 12:00:00"

    def test_retorna_none_sem_registros(self, panel, app_db):
        panel._project_root = app_db.parent.parent
        ts = panel._get_latest_snapshot_timestamp_for_structure(99)
        assert ts is None

    def test_retorna_none_db_inexistente(self, panel, tmp_path):
        panel._project_root = tmp_path  # dados/app.db não existe
        ts = panel._get_latest_snapshot_timestamp_for_structure(1)
        assert ts is None

    def test_nao_usa_coluna_aba(self, panel, app_db):
        """
        patch_36: query usa structure_id diretamente, sem coluna aba.
        """
        con = sqlite3.connect(str(app_db))
        con.execute("INSERT INTO robo_snapshot VALUES (?, ?)", (7, "2025-03-01 00:00:00"))
        con.commit()
        con.close()

        panel._project_root = app_db.parent.parent
        ts = panel._get_latest_snapshot_timestamp_for_structure(5)
        assert ts is None

    def test_fallback_para_proxima_tabela(self, panel, app_db):
        """Se robo_legs_snapshot não tem dado, deve continuar para robo_snapshot."""
        con = sqlite3.connect(str(app_db))
        con.execute("INSERT INTO robo_snapshot VALUES (?, ?)", (3, "2025-02-20 15:30:00"))
        con.commit()
        con.close()

        panel._project_root = app_db.parent.parent
        ts = panel._get_latest_snapshot_timestamp_for_structure(3)
        assert ts == "2025-02-20 15:30:00"

    def test_aceita_structure_id_como_string(self, panel, app_db):
        con = sqlite3.connect(str(app_db))
        con.execute("INSERT INTO robo_legs_snapshot VALUES (?, ?)", (8, "2025-05-01 00:00:00"))
        con.commit()
        con.close()

        panel._project_root = app_db.parent.parent
        ts = panel._get_latest_snapshot_timestamp_for_structure("8")
        assert ts == "2025-05-01 00:00:00"


# ===========================================================================
# 3. _fetch_latest_decision_from_derived
# ===========================================================================

class TestFetchLatestDecision:

    def _insert_decision(self, db, structure_id, timestamp, decision="HOLD",
                         level=1, created_at=None, why_json=None):
        con = sqlite3.connect(str(db))
        con.execute(
            """INSERT INTO structure_decisions
               (structure_id, timestamp, decision, level, pl_atual, pl_max,
                pl_pct_of_max, dte_min, spot_ref, meta_json, created_at, why_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (structure_id, timestamp, decision, level,
             1000.0, 2000.0, 0.5, 10, 50.0, None, created_at, why_json),
        )
        con.commit()
        con.close()

    def test_retorna_decisao_mais_recente(self, panel, derived_db):
        self._insert_decision(derived_db, 1, "2025-01-01 08:00:00", created_at="2025-01-01 08:00:00")
        self._insert_decision(derived_db, 1, "2025-01-02 09:00:00", created_at="2025-01-02 09:00:00")

        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived(1)
        assert d is not None
        assert d["timestamp"] == "2025-01-02 09:00:00"

    def test_retorna_none_sem_registro(self, panel, derived_db):
        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived(99)
        assert d is None

    def test_why_json_mapeado_para_why(self, panel, derived_db):
        self._insert_decision(derived_db, 2, "2025-01-01", why_json='{"motivo": "teste"}')
        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived(2)
        assert d["why"] == '{"motivo": "teste"}'

    def test_spot_ref_renomeado_para_spot_reference(self, panel, derived_db):
        self._insert_decision(derived_db, 3, "2025-01-01")
        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived(3)
        assert "spot_reference" in d
        assert "spot_ref" not in d

    def test_structure_id_presente_no_retorno(self, panel, derived_db):
        self._insert_decision(derived_db, 4, "2025-01-01")
        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived(4)
        assert d["structure_id"] == 4

    def test_nao_filtra_por_aba(self, panel, derived_db):
        """patch_36: sem coluna aba -- query não deve lançar OperationalError."""
        self._insert_decision(derived_db, 5, "2025-01-01")
        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived(99)
        assert d is None

    def test_aceita_structure_id_string(self, panel, derived_db):
        self._insert_decision(derived_db, 6, "2025-01-01")
        panel._derived_db_path = lambda: derived_db
        d = panel._fetch_latest_decision_from_derived("6")
        assert d is not None
        assert d["structure_id"] == 6


# ===========================================================================
# 4. _fetch_payoff_points_from_derived
# ===========================================================================

class TestFetchPayoffPoints:

    def _insert_points(self, db, structure_id, points):
        con = sqlite3.connect(str(db))
        con.executemany(
            "INSERT INTO payoff_curve_points VALUES (?,?,?)",
            [(structure_id, s, p) for s, p in points],
        )
        con.commit()
        con.close()

    def test_retorna_lista_de_tuplas(self, panel, derived_db):
        self._insert_points(derived_db, 1, [(45.0, -100.0), (50.0, 0.0), (55.0, 200.0)])
        panel._derived_db_path = lambda: derived_db
        pts = panel._fetch_payoff_points_from_derived(1)
        assert len(pts) == 3
        assert pts[0] == (45.0, -100.0)

    def test_ordenado_por_spot_asc(self, panel, derived_db):
        self._insert_points(derived_db, 2, [(55.0, 200.0), (45.0, -100.0), (50.0, 0.0)])
        panel._derived_db_path = lambda: derived_db
        pts = panel._fetch_payoff_points_from_derived(2)
        spots = [p[0] for p in pts]
        assert spots == sorted(spots)

    def test_retorna_lista_vazia_sem_registros(self, panel, derived_db):
        panel._derived_db_path = lambda: derived_db
        pts = panel._fetch_payoff_points_from_derived(99)
        assert pts == []

    def test_ignora_registros_de_outra_estrutura(self, panel, derived_db):
        self._insert_points(derived_db, 10, [(50.0, 100.0)])
        self._insert_points(derived_db, 11, [(60.0, 200.0)])
        panel._derived_db_path = lambda: derived_db
        pts = panel._fetch_payoff_points_from_derived(10)
        assert len(pts) == 1
        assert pts[0][0] == 50.0

    def test_aceita_structure_id_string(self, panel, derived_db):
        self._insert_points(derived_db, 7, [(48.0, -50.0), (52.0, 50.0)])
        panel._derived_db_path = lambda: derived_db
        pts = panel._fetch_payoff_points_from_derived("7")
        assert len(pts) == 2

    def test_ignora_pontos_com_null(self, panel, derived_db):
        con = sqlite3.connect(str(derived_db))
        con.execute("INSERT INTO payoff_curve_points VALUES (?, ?, ?)", (12, None, 100.0))
        con.execute("INSERT INTO payoff_curve_points VALUES (?, ?, ?)", (12, 50.0, None))
        con.execute("INSERT INTO payoff_curve_points VALUES (?, ?, ?)", (12, 55.0, 200.0))
        con.commit()
        con.close()
        panel._derived_db_path = lambda: derived_db
        pts = panel._fetch_payoff_points_from_derived(12)
        assert len(pts) == 1
        assert pts[0] == (55.0, 200.0)


# ===========================================================================
# 5. _fetch_audit_info_from_derived
# ===========================================================================

class TestFetchAuditInfo:

    def _setup_data(self, db, structure_id, created_at, n_points):
        con = sqlite3.connect(str(db))
        con.execute(
            """INSERT INTO structure_decisions
               (structure_id, timestamp, decision, level, pl_atual, pl_max,
                pl_pct_of_max, dte_min, spot_ref, meta_json, created_at, why_json)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (structure_id, "2025-01-01", "HOLD", 1, 0, 0, 0, 0, 0, None, created_at, None),
        )
        for i in range(n_points):
            con.execute(
                "INSERT INTO payoff_curve_points VALUES (?,?,?)",
                (structure_id, float(i), float(i * 10)),
            )
        con.commit()
        con.close()

    def test_retorna_created_at(self, panel, derived_db):
        self._setup_data(derived_db, 1, "2025-03-15 10:00:00", 5)
        panel._derived_db_path = lambda: derived_db
        info = panel._fetch_audit_info_from_derived(1)
        assert info["created_at"] == "2025-03-15 10:00:00"

    def test_retorna_count_points(self, panel, derived_db):
        self._setup_data(derived_db, 2, "2025-03-15", 7)
        panel._derived_db_path = lambda: derived_db
        info = panel._fetch_audit_info_from_derived(2)
        assert info["count_points"] == 7

    def test_fallback_false(self, panel, derived_db):
        self._setup_data(derived_db, 3, "2025-03-15", 3)
        panel._derived_db_path = lambda: derived_db
        info = panel._fetch_audit_info_from_derived(3)
        assert info["fallback"] is False

    def test_source_table_correto(self, panel, derived_db):
        self._setup_data(derived_db, 4, "2025-03-15", 1)
        panel._derived_db_path = lambda: derived_db
        info = panel._fetch_audit_info_from_derived(4)
        assert "structure_decisions" in info["source_table"]
        assert "payoff_curve_points" in info["source_table"]

    def test_created_at_none_quando_sem_registro(self, panel, derived_db):
        panel._derived_db_path = lambda: derived_db
        info = panel._fetch_audit_info_from_derived(99)
        assert info["created_at"] is None
        assert info["count_points"] == 0

    def test_aceita_structure_id_string(self, panel, derived_db):
        self._setup_data(derived_db, 5, "2025-04-01", 4)
        panel._derived_db_path = lambda: derived_db
        info = panel._fetch_audit_info_from_derived("5")
        assert info["count_points"] == 4


# ===========================================================================
# 6. update_decision -- sem fallback aba
# ===========================================================================

class TestUpdateDecision:

    def test_usa_structure_id_quando_presente(self, panel):
        panel.update_decision({
            "structure_id": 10,
            "aba": "WING_LEGADO",
            "timestamp": "2025-01-01",
            "decision": "HOLD",
        })
        call_args = panel.structure_label.config.call_args
        assert call_args[1]["text"] == "10"

    def test_exibe_na_quando_structure_id_ausente(self, panel):
        """patch_36: sem structure_id  exibe N/A (não usa aba)."""
        panel.update_decision({
            "aba": "WING_LEGADO",
            "timestamp": "2025-01-01",
            "decision": "HOLD",
        })
        call_args = panel.structure_label.config.call_args
        assert call_args[1]["text"] == "N/A"

    def test_nao_usa_aba_como_fallback(self, panel):
        """Confirma explicitamente que aba não é usado como fallback."""
        panel.update_decision({
            "aba": "QUALQUER_ABA",
            "timestamp": "2025-01-01",
        })
        call_args = panel.structure_label.config.call_args
        assert call_args[1]["text"] != "QUALQUER_ABA"

    def test_armazena_current_decision(self, panel):
        data = {"structure_id": 7, "timestamp": "2025-01-01", "decision": "BUY"}
        panel.update_decision(data)
        assert panel._current_decision["structure_id"] == 7

    def test_why_json_renderizado(self, panel):
        panel.update_decision({
            "structure_id": 1,
            "timestamp": "2025-01-01",
            "why_json": '{"score": 0.9}',
        })
        panel.why_text.insert.assert_called()

    def test_pl_pct_of_max_formatado(self, panel):
        panel.update_decision({
            "structure_id": 1,
            "timestamp": "2025-01-01",
            "pl_pct_of_max": 0.75,
        })
        panel.ratio_label.config.assert_called_with(text="75.0%")


# ===========================================================================
# 7. _on_recalculate_click -- sem fallback aba
# ===========================================================================

class TestOnRecalculateClick:

    def test_usa_structure_id(self, panel):
        cb = MagicMock()
        panel._on_recalculate_cb = cb
        panel._current_decision = {"structure_id": 42, "timestamp": "2025-01-01"}

        panel._compute_recalc_signature = MagicMock(return_value=(42, "ts"))
        panel._last_recalc_signature = None

        panel._on_recalculate_click()
        cb.assert_called_once_with(42)

    def test_nao_usa_aba_como_fallback(self, panel):
        """patch_36: sem structure_id  erro, mesmo com aba presente."""
        panel._current_decision = {"aba": "WING", "timestamp": "2025-01-01"}
        panel._on_recalculate_click()
        panel.lbl_recalc_status.config.assert_called_with(
            text="Estrutura não identificada", foreground="red"
        )

    def test_sem_decisao_exibe_erro(self, panel):
        panel._current_decision = None
        panel._on_recalculate_click()
        panel.lbl_recalc_status.config.assert_called_with(
            text="Nenhuma decisão selecionada", foreground="red"
        )

    def test_recalc_em_andamento_bloqueia(self, panel):
        cb = MagicMock()
        panel._on_recalculate_cb = cb
        panel._current_decision = {"structure_id": 1, "timestamp": "2025-01-01"}
        panel._recalc_in_progress = True
        panel._compute_recalc_signature = MagicMock(return_value=(1, "ts"))

        panel._on_recalculate_click()
        cb.assert_not_called()

    def test_assinatura_igual_nao_recalcula(self, panel):
        cb = MagicMock()
        panel._on_recalculate_cb = cb
        panel._current_decision = {"structure_id": 3, "timestamp": "2025-01-01"}
        sig = (3, "2025-01-01 10:00:00")
        panel._compute_recalc_signature = MagicMock(return_value=sig)
        panel._last_recalc_signature = sig

        panel._on_recalculate_click()
        cb.assert_not_called()

    def test_callback_none_exibe_mensagem(self, panel):
        panel._on_recalculate_cb = None
        panel._current_decision = {"structure_id": 5, "timestamp": "2025-01-01"}
        panel._compute_recalc_signature = MagicMock(return_value=(5, "ts"))
        panel._last_recalc_signature = None

        panel._on_recalculate_click()
        panel.lbl_recalc_status.config.assert_called_with(
            text="Recalc indisponível: callback não configurado",
            foreground="red",
        )
