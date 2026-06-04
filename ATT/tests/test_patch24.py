"""
ATT/tests/test_patch24.py

Patch 24 -- Testes de validação das correções de acoplamento legado.

Cobre:
  1. decision.py   compute_decision_for_aba ausente
  2. decision.py   __main__ sem get_app_db_connection / rtd_analise_robo
  3. decision.py   interfaces canônicas intactas e funcionais
  4. payoff_features.py  upsert usa (structure_id, reference_date)
  5. payoff_features.py  compute_curve_features aceita novos parâmetros
  6. payoff_features.py  ValueError sem structure_id/reference_date
  7. Regressão: compute_decision_from_inputs ainda produz saída correta
"""

import importlib
import inspect
import json
import sqlite3
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


#  helpers 

def _load_decision():
    """Importa domain.decision isolado (sem side-effects de BD)."""
    if "domain.decision" in sys.modules:
        return sys.modules["domain.decision"]
    return importlib.import_module("domain.decision")


def _load_payoff_features():
    if "domain.payoff_features" in sys.modules:
        return sys.modules["domain.payoff_features"]
    return importlib.import_module("domain.payoff_features")


# 
# 1. decision.py -- remoção do legado
# 

class TestDecisionLegacyRemoval:

    def test_patch24_compute_decision_for_aba_does_not_exist(self):
        """compute_decision_for_aba() deve ter sido removida do módulo."""
        mod = _load_decision()
        assert not hasattr(mod, "compute_decision_for_aba"), (
            "compute_decision_for_aba ainda existe em domain/decision.py -- "
            "patch_24 não foi aplicado."
        )

    def test_patch24_get_app_db_connection_not_imported(self):
        """get_app_db_connection não deve aparecer em nenhum import do módulo."""
        source_path = Path("domain/decision.py")
        assert source_path.exists(), "domain/decision.py não encontrado"
        source = source_path.read_text(encoding="utf-8")
        assert "get_app_db_connection" not in source, (
            "get_app_db_connection ainda referenciado em domain/decision.py"
        )

    def test_patch24_rtd_analise_robo_not_in_decision(self):
        """Nenhuma query a rtd_analise_robo deve existir em decision.py."""
        source_path = Path("domain/decision.py")
        source = source_path.read_text(encoding="utf-8")
        assert "rtd_analise_robo" not in source, (
            "Referência a rtd_analise_robo ainda presente em domain/decision.py"
        )

    def test_patch24_compute_payoff_for_aba_not_imported(self):
        """compute_payoff_for_aba não deve ser importado em decision.py."""
        source_path = Path("domain/decision.py")
        source = source_path.read_text(encoding="utf-8")
        assert "compute_payoff_for_aba" not in source, (
            "compute_payoff_for_aba ainda importado em domain/decision.py"
        )

    def test_patch24_read_structure_summary_not_imported(self):
        """read_structure_summary não deve ser importado em decision.py."""
        source_path = Path("domain/decision.py")
        source = source_path.read_text(encoding="utf-8")
        assert "read_structure_summary" not in source, (
            "read_structure_summary ainda importado em domain/decision.py"
        )


# 
# 2. decision.py -- interfaces canônicas intactas
# 

class TestDecisionCanonicalIntact:

    def test_patch24_compute_decision_from_contract_exists(self):
        mod = _load_decision()
        assert hasattr(mod, "compute_decision_from_contract"), (
            "compute_decision_from_contract ausente -- regressão crítica"
        )

    def test_patch24_compute_decision_from_payoff_exists(self):
        mod = _load_decision()
        assert hasattr(mod, "compute_decision_from_payoff")

    def test_patch24_compute_decision_from_inputs_exists(self):
        mod = _load_decision()
        assert hasattr(mod, "compute_decision_from_inputs")

    def test_patch24_compute_decision_from_inputs_hold(self):
        """Ratio baixo  HOLD nível 0."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=10.0,
            pl_max=100.0,
            dte_min=30,
        )
        assert result["decision"] == "HOLD"
        assert result["level"] == 0
        assert result["pl_pct_of_max"] == pytest.approx(0.10)

    def test_patch24_compute_decision_from_inputs_watch(self):
        """Ratio 35%  HOLD nível 1 (watch)."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=35.0,
            pl_max=100.0,
            dte_min=30,
        )
        assert result["decision"] == "HOLD"
        assert result["level"] == 1

    def test_patch24_compute_decision_from_inputs_prepare(self):
        """Ratio 65%  PREPARE_ROLL nível 2."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=65.0,
            pl_max=100.0,
            dte_min=30,
        )
        assert result["decision"] == "PREPARE_ROLL"
        assert result["level"] == 2

    def test_patch24_compute_decision_from_inputs_close(self):
        """Ratio 85%  CLOSE_REOPEN nível 3."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=85.0,
            pl_max=100.0,
            dte_min=30,
        )
        assert result["decision"] == "CLOSE_REOPEN"
        assert result["level"] == 3

    def test_patch24_dte_gate_promotes_prepare_to_close(self):
        """DTE baixo com ratio >= prepare  promovido para CLOSE_REOPEN."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=65.0,
            pl_max=100.0,
            dte_min=5,
            dte_gate=7,
        )
        assert result["decision"] == "CLOSE_REOPEN"
        assert result["level"] == 3

    def test_patch24_why_json_is_valid_json(self):
        """why_json deve ser JSON válido e parseable."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=50.0,
            pl_max=100.0,
            dte_min=20,
        )
        parsed = json.loads(result["why_json"])
        assert "reasons" in parsed
        assert "thresholds_used" in parsed

    def test_patch24_spread_alto_gera_alternativa(self):
        """Spread > 1.5% deve gerar aviso em alternatives."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=50.0,
            pl_max=100.0,
            dte_min=20,
            spread_pct_medio=0.025,
        )
        alternatives = result["why"]["alternatives"]
        assert any("Spread" in alt for alt in alternatives)

    def test_patch24_pl_max_zero_returns_ratio_zero(self):
        """pl_max=0 não deve lançar ZeroDivisionError."""
        mod = _load_decision()
        result = mod.compute_decision_from_inputs(
            pl_atual=50.0,
            pl_max=0.0,
            dte_min=20,
        )
        assert result["pl_pct_of_max"] == 0.0

    def test_patch24_compute_decision_from_payoff_invalid_returns_hold(self):
        """Payoff inválido (sem points)  HOLD com erro."""
        mod = _load_decision()
        result = mod.compute_decision_from_payoff(
            payoff={},
            dte_min=10,
        )
        assert result["decision"] == "HOLD"
        assert "error" in result["why"]

    def test_patch24_interp_payoff_extrapolation_low(self):
        """Spot abaixo do mínimo  retorna primeiro valor."""
        mod = _load_decision()
        pts = [(100.0, -10.0), (110.0, 0.0), (120.0, 20.0)]
        assert mod._interp_payoff(pts, 90.0) == pytest.approx(-10.0)

    def test_patch24_interp_payoff_extrapolation_high(self):
        """Spot acima do máximo  retorna último valor."""
        mod = _load_decision()
        pts = [(100.0, -10.0), (110.0, 0.0), (120.0, 20.0)]
        assert mod._interp_payoff(pts, 130.0) == pytest.approx(20.0)

    def test_patch24_interp_payoff_midpoint(self):
        """Spot no meio do intervalo  interpolação linear correta."""
        mod = _load_decision()
        pts = [(100.0, 0.0), (120.0, 20.0)]
        assert mod._interp_payoff(pts, 110.0) == pytest.approx(10.0)


# 
# 3. payoff_features.py -- chave canônica
# 

class TestPayoffFeaturesCanonicalKey:

    def test_patch24_compute_curve_features_accepts_structure_id(self):
        """compute_curve_features deve aceitar structure_id e reference_date."""
        mod = _load_payoff_features()
        sig = inspect.signature(mod.compute_curve_features)
        params = set(sig.parameters.keys())
        assert "structure_id"   in params, "structure_id ausente em compute_curve_features"
        assert "reference_date" in params, "reference_date ausente em compute_curve_features"

    def test_patch24_compute_curve_features_returns_canonical_keys(self):
        """Resultado deve conter structure_id e reference_date."""
        mod    = _load_payoff_features()
        pts    = [(100.0, -5.0), (110.0, 0.0), (120.0, 10.0)]
        result = mod.compute_curve_features(
            points=pts,
            spot_ref=110.0,
            structure_id="struct-001",
            reference_date="2026-05-28",
        )
        assert result["structure_id"]   == "struct-001"
        assert result["reference_date"] == "2026-05-28"

    def test_patch24_compute_curve_features_legacy_fields_optional(self):
        """aba e timestamp devem estar no resultado quando fornecidos."""
        mod    = _load_payoff_features()
        pts    = [(100.0, 0.0), (120.0, 10.0)]
        result = mod.compute_curve_features(
            points=pts,
            structure_id="struct-001",
            reference_date="2026-05-28",
            aba="PETR4_001",
            timestamp="2026-05-28T20:00:00",
        )
        assert result["aba"]       == "PETR4_001"
        assert result["timestamp"] == "2026-05-28T20:00:00"

    def test_patch24_upsert_raises_without_structure_id(self):
        """upsert sem structure_id deve lançar ValueError."""
        mod = _load_payoff_features()
        with pytest.raises(ValueError, match="structure_id"):
            mod.upsert_curve_summary({
                "reference_date": "2026-05-28",
                "pl_min": -5.0,
                "pl_max": 10.0,
            })

    def test_patch24_upsert_raises_without_reference_date(self):
        """upsert sem reference_date deve lançar ValueError."""
        mod = _load_payoff_features()
        with pytest.raises(ValueError, match="reference_date"):
            mod.upsert_curve_summary({
                "structure_id": "struct-001",
                "pl_min": -5.0,
                "pl_max": 10.0,
            })

    def test_patch24_upsert_conflict_key_is_canonical(self):
        """
        O SQL de upsert deve usar ON CONFLICT(structure_id, reference_date),
        não ON CONFLICT(timestamp, aba).
        """
        source_path = Path("domain/payoff_features.py")
        source = source_path.read_text(encoding="utf-8")
        assert "ON CONFLICT(structure_id, reference_date)" in source, (
            "Chave legada (timestamp, aba) ainda usada no ON CONFLICT"
        )
        assert "ON CONFLICT(timestamp, aba)" not in source, (
            "ON CONFLICT(timestamp, aba) ainda presente -- patch_24 incompleto"
        )

    def test_patch24_upsert_executes_with_in_memory_db(self):
        """
        Smoke test end-to-end: upsert em BD in-memory com schema correto.
        Valida que o SQL gerado executa sem erro sintático.
        """
        mod = _load_payoff_features()

        # Cria BD temporário com schema esperado (post-patch_24)
        conn = sqlite3.connect(":memory:")
        conn.execute(
            """
            CREATE TABLE payoff_curve_summary (
                structure_id       TEXT NOT NULL,
                reference_date     TEXT NOT NULL,
                timestamp          TEXT,
                aba                TEXT,
                spot_ref           REAL,
                points_count       INTEGER,
                pl_min             REAL,
                pl_max             REAL,
                pl_at_spot_ref     REAL,
                breakevens_json    TEXT,
                be_count           INTEGER,
                pos_ranges_json    TEXT,
                pos_ranges_count   INTEGER,
                max_drawdown_like  REAL,
                meta_json          TEXT,
                PRIMARY KEY (structure_id, reference_date)
            )
            """
        )
        conn.commit()

        pts = [(90.0, -10.0), (100.0, 0.0), (110.0, 15.0)]
        features = mod.compute_curve_features(
            points=pts,
            spot_ref=100.0,
            structure_id="struct-smoke-001",
            reference_date="2026-05-28",
            aba="PETR4_001",
            timestamp="2026-05-28T20:00:00",
        )

        # Injeta conexão in-memory via _conn_override (sem fechar a conn)
        mod.upsert_curve_summary(features, _conn_override=conn)

        cur = conn.execute(
            "SELECT structure_id, reference_date, aba, pl_max "
            "FROM payoff_curve_summary"
        )
        row = cur.fetchone()
        conn.close()

        assert row is not None,              "Nenhuma linha inserida"
        assert row[0] == "struct-smoke-001", "structure_id incorreto"
        assert row[1] == "2026-05-28",       "reference_date incorreto"
        assert row[2] == "PETR4_001",        "aba (rastreabilidade) incorreto"
        assert row[3] == pytest.approx(15.0), "pl_max incorreto"

    def test_patch24_upsert_idempotent_in_memory_db(self):
        """
        Segundo upsert com mesma chave deve atualizar, não duplicar.
        """
        mod = _load_payoff_features()

        conn = sqlite3.connect(":memory:")
        conn.execute(
            """
            CREATE TABLE payoff_curve_summary (
                structure_id       TEXT NOT NULL,
                reference_date     TEXT NOT NULL,
                timestamp          TEXT,
                aba                TEXT,
                spot_ref           REAL,
                points_count       INTEGER,
                pl_min             REAL,
                pl_max             REAL,
                pl_at_spot_ref     REAL,
                breakevens_json    TEXT,
                be_count           INTEGER,
                pos_ranges_json    TEXT,
                pos_ranges_count   INTEGER,
                max_drawdown_like  REAL,
                meta_json          TEXT,
                PRIMARY KEY (structure_id, reference_date)
            )
            """
        )
        conn.commit()

        base_features = {
            "structure_id":      "struct-idem-001",
            "reference_date":    "2026-05-28",
            "spot_ref":          100.0,
            "points_count":      3,
            "pl_min":            -10.0,
            "pl_max":            15.0,
            "pl_at_spot_ref":    0.0,
            "breakevens":        [100.0],
            "be_count":          1,
            "pos_ranges":        [[100.0, 110.0]],
            "pos_ranges_count":  1,
            "max_drawdown_like": 25.0,
            "meta":              {},
        }

        mod.upsert_curve_summary(base_features, _conn_override=conn)

        # Atualiza pl_max e faz segundo upsert
        updated = {**base_features, "pl_max": 99.0}
        mod.upsert_curve_summary(updated, _conn_override=conn)

        cur  = conn.execute("SELECT COUNT(*), pl_max FROM payoff_curve_summary")
        cnt, pl = cur.fetchone()
        conn.close()

        assert cnt == 1,                  "Upsert duplicou a linha"
        assert pl  == pytest.approx(99.0), "pl_max não foi atualizado"


# 
# 4. Ausência de importações legadas no source
# 

class TestSourceAuditRegressionPatch24:

    def test_patch24_decision_source_no_legacy_imports(self):
        source = Path("domain/decision.py").read_text(encoding="utf-8")
        forbidden = [
            "compute_decision_for_aba",
            "compute_payoff_for_aba",
            "read_structure_summary",
            "get_app_db_connection",
            "rtd_analise_robo",
        ]
        violations = [t for t in forbidden if t in source]
        assert not violations, (
            f"Termos legados ainda presentes em decision.py: {violations}"
        )

    def test_patch24_payoff_features_source_no_legacy_conflict_key(self):
        source = Path("domain/payoff_features.py").read_text(encoding="utf-8")
        assert "ON CONFLICT(timestamp, aba)" not in source
        assert "ON CONFLICT(structure_id, reference_date)" in source
