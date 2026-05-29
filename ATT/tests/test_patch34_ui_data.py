"""
test_patch34_ui_data.py
Valida que UIDataModel opera exclusivamente com structure_id apos patch_34.
"""
import sqlite3
import pytest
from pathlib import Path
from unittest.mock import patch as mock_patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_derived_db(path: str) -> None:
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE structure_decisions (
            id           INTEGER PRIMARY KEY,
            timestamp    TEXT NOT NULL,
            structure_id INTEGER NOT NULL,
            aba          TEXT,
            decision     TEXT,
            level        TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE payoff_curve_points (
            id           INTEGER PRIMARY KEY,
            timestamp    TEXT NOT NULL,
            structure_id INTEGER NOT NULL,
            aba          TEXT,
            point_spot   REAL,
            point_pl     REAL
        )
    """)
    conn.executemany(
        "INSERT INTO structure_decisions "
        "(timestamp, structure_id, aba, decision, level) VALUES (?,?,?,?,?)",
        [
            ("2026-01-01T10:00:00", 7,  "BOVA11", "BUY",  "1"),
            ("2026-01-01T11:00:00", 7,  "BOVA11", "SELL", "1"),
            ("2026-01-01T10:00:00", 12, "PETR4",  "BUY",  "2"),
        ],
    )
    conn.executemany(
        "INSERT INTO payoff_curve_points "
        "(timestamp, structure_id, aba, point_spot, point_pl) VALUES (?,?,?,?,?)",
        [
            ("2026-01-01T10:00:00", 7, "BOVA11", 50.0, 100.0),
            ("2026-01-01T10:00:00", 7, "BOVA11", 55.0,  80.0),
        ],
    )
    conn.commit()
    conn.close()


@pytest.fixture
def derived_db(tmp_path: Path) -> Path:
    db = tmp_path / "derived.db"
    _build_derived_db(str(db))
    return db


@pytest.fixture
def model(derived_db: Path) -> "UIDataModel":
    from UI.models.ui_data import UIDataModel
    instance = UIDataModel(derived_db_path=derived_db)
    instance.refresh()
    return instance


# ---------------------------------------------------------------------------
# _structure_filter_col
# ---------------------------------------------------------------------------

class TestStructureFilterCol:

    def test_retorna_coluna_canonica(self, model):
        col = model._structure_filter_col({"structure_id": "structure_id"})
        assert col == "structure_id"

    def test_sem_structure_id_raises(self, model):
        with pytest.raises(RuntimeError, match="structure_id"):
            model._structure_filter_col({})

    def test_aba_no_colmap_nao_e_fallback(self, model):
        # patch_34: aba sozinho nao deve ser aceito como coluna de filtro
        with pytest.raises(RuntimeError):
            model._structure_filter_col({"aba": "aba"})

    def test_retorna_str_nao_tupla(self, model):
        result = model._structure_filter_col({"structure_id": "structure_id"})
        assert isinstance(result, str)
        assert not isinstance(result, tuple)


# ---------------------------------------------------------------------------
# _resolve_structure_key
# ---------------------------------------------------------------------------

class TestResolveStructureKey:

    def test_string_numerica(self, model):
        assert model._resolve_structure_key("7") == 7

    def test_inteiro_direto(self, model):
        assert model._resolve_structure_key(7) == 7

    def test_string_nao_numerica_raises(self, model):
        with pytest.raises(ValueError, match="structure_id invalido"):
            model._resolve_structure_key("BOVA11")

    def test_none_raises(self, model):
        with pytest.raises((ValueError, TypeError)):
            model._resolve_structure_key(None)

    def test_retorna_int(self, model):
        result = model._resolve_structure_key("12")
        assert isinstance(result, int)


# ---------------------------------------------------------------------------
# _load_structures / get_structure_ids / get_abas
# ---------------------------------------------------------------------------

class TestGetStructureIds:

    def test_retorna_lista_nao_vazia(self, model):
        ids = model.get_structure_ids()
        assert isinstance(ids, list)
        assert len(ids) > 0

    def test_contem_ids_esperados(self, model):
        ids = model.get_structure_ids()
        assert "7" in ids
        assert "12" in ids

    def test_get_abas_e_alias(self, model):
        assert model.get_abas() == model.get_structure_ids()

    def test_get_structures_ainda_funciona(self, model):
        # get_structures() nao foi removido — compat
        assert model.get_structures() == model.get_structure_ids()

    def test_schema_sem_structure_id_raises(self, tmp_path):
        from UI.models.ui_data import UIDataModel
        # DB sem coluna structure_id
        db = tmp_path / "broken.db"
        conn = sqlite3.connect(str(db))
        conn.execute(
            "CREATE TABLE structure_decisions "
            "(id INTEGER PRIMARY KEY, timestamp TEXT, aba TEXT)"
        )
        conn.close()
        m = UIDataModel(derived_db_path=db)
        with pytest.raises(RuntimeError, match="structure_id"):
            m.refresh()


# ---------------------------------------------------------------------------
# get_decisions — filtro
# ---------------------------------------------------------------------------

class TestGetDecisionsFiltro:

    def test_sem_filtro_retorna_todos(self, model):
        rows = model.get_decisions(filters={})
        assert len(rows) == 3

    def test_filtro_structure_id_string_numerica(self, model):
        rows = model.get_decisions(filters={"structure_id": "7"})
        assert len(rows) == 2

    def test_filtro_structure_id_inteiro(self, model):
        rows = model.get_decisions(filters={"structure_id": 12})
        assert len(rows) == 1

    def test_filtro_structure_id_invalido_raises(self, model):
        with pytest.raises(ValueError, match="structure_id deve ser inteiro"):
            model.get_decisions(filters={"structure_id": "BOVA11"})

    def test_filtro_aba_legado_nao_filtra(self, model):
        # patch_34: "aba" no filtro nao e mais aplicado — retorna todos
        rows = model.get_decisions(filters={"aba": "BOVA11"})
        assert len(rows) == 3


# ---------------------------------------------------------------------------
# get_decisions — normalizacao pos-query
# ---------------------------------------------------------------------------

class TestGetDecisionsNormalizacao:

    def test_structure_id_nunca_nulo(self, model):
        rows = model.get_decisions(filters={})
        for r in rows:
            assert r.get("structure_id") is not None, f"structure_id nulo em: {r}"

    def test_aba_espelhado_quando_nulo(self, model):
        rows = model.get_decisions(filters={})
        for r in rows:
            assert "aba" in r

    def test_aba_nao_e_none(self, model):
        rows = model.get_decisions(filters={})
        for r in rows:
            assert r["aba"] is not None, f"aba nulo em: {r}"


# ---------------------------------------------------------------------------
# get_payoff_curve
# ---------------------------------------------------------------------------

class TestGetPayoffCurve:

    def test_retorna_pontos_por_structure_id(self, model):
        pts = model.get_payoff_curve("7", "2026-01-01T10:00:00")
        assert len(pts) == 2
        assert all("spot" in p and "pl" in p for p in pts)

    def test_structure_id_inexistente_retorna_vazio(self, model):
        pts = model.get_payoff_curve("999", "2026-01-01T10:00:00")
        assert pts == []

    def test_structure_id_invalido_raises(self, model):
        with pytest.raises(ValueError):
            model.get_payoff_curve("BOVA11", "2026-01-01T10:00:00")


# ---------------------------------------------------------------------------
# check_database_status
# ---------------------------------------------------------------------------

class TestCheckDatabaseStatus:

    def test_retorna_string(self, model):
        status = model.check_database_status()
        assert isinstance(status, str)

    def test_sem_key_type_no_status(self, model):
        status = model.check_database_status()
        assert "mode=canonical" in status
        assert "mode=aba" not in status
        assert "mode=id" not in status
