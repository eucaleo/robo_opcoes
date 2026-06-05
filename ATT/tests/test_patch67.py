# ATT/tests/test_patch67.py
"""
patch_67 -- Testes formais da auditoria baseline fase 8.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_TESTS_DIR   = Path(__file__).resolve().parent   # ATT/tests/
_ATT_ROOT    = _TESTS_DIR.parent                 # ATT/
PROJECT_ROOT = _ATT_ROOT.parent                  # projeto/

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Import dinâmico — registra em sys.modules ANTES de exec_module
# (obrigatório no Python 3.13: @dataclass usa cls.__module__ para resolver tipos)
# ---------------------------------------------------------------------------

_MODULE_NAME = "audit_fase8"

def _load_audit_module():
    script_path = PROJECT_ROOT / "scripts" / "75_audit_fase8_baseline.py"
    if not script_path.exists():
        pytest.fail(f"Script não encontrado: {script_path}")

    spec   = importlib.util.spec_from_file_location(_MODULE_NAME, script_path)
    module = importlib.util.module_from_spec(spec)

    # ⚠️  CRÍTICO: registrar ANTES de exec_module
    # Sem isso, @dataclass falha no Python 3.13 porque sys.modules.get(cls.__module__)
    # retorna None e o dataclasses tenta chamar .__dict__ em None
    sys.modules[_MODULE_NAME] = module

    spec.loader.exec_module(module)
    return module


_audit = _load_audit_module()

# Expõe símbolos (equivalente a 'from audit_fase8 import ...')
run_audit                    = _audit.run_audit
gerar_markdown               = _audit.gerar_markdown
gerar_json                   = _audit.gerar_json
AuditReport                  = _audit.AuditReport
REPORTS_DIR                  = _audit.REPORTS_DIR
check_databases              = _audit.check_databases
check_structures_repository  = _audit.check_structures_repository
check_derived_repo           = _audit.check_derived_repo
check_derived_service        = _audit.check_derived_service
check_bootstrap_schema       = _audit.check_bootstrap_schema
check_audit_artifacts        = _audit.check_audit_artifacts
check_att_patches            = _audit.check_att_patches

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

EXPECTED_CATEGORIES = {
    "infra_db",
    "structures_repo",
    "derived_repo",
    "derived_service",
    "bootstrap_schema",
    "audit_artifacts",
    "att_patches",
}

# ---------------------------------------------------------------------------
# Testes do runner principal
# ---------------------------------------------------------------------------

class TestRunAudit:
    def test_run_audit_nao_lanca_excecao(self):
        report = run_audit()
        assert isinstance(report, AuditReport)

    def test_report_tem_gerado_em(self):
        report = run_audit()
        assert report.gerado_em
        assert "T" in report.gerado_em

    def test_report_tem_raiz(self):
        report = run_audit()
        assert report.raiz
        assert Path(report.raiz).exists()

    def test_total_checks_maior_que_zero(self):
        report = run_audit()
        total = report.total_ok + report.total_warn + report.total_fail
        assert total > 0

    def test_total_ok_maior_que_zero(self):
        report = run_audit()
        assert report.total_ok > 0, (
            f"Nenhum check OK. WARN={report.total_warn} FAIL={report.total_fail}"
        )

    def test_todas_categorias_presentes(self):
        report = run_audit()
        cats    = {c["categoria"] for c in report.checks}
        missing = EXPECTED_CATEGORIES - cats
        assert not missing, f"Categorias ausentes: {missing}"

    def test_checks_tem_campos_obrigatorios(self):
        report = run_audit()
        for check in report.checks:
            assert "categoria" in check
            assert "check"     in check
            assert "status"    in check
            assert check["status"] in ("OK", "WARN", "FAIL")

    def test_contadores_consistentes(self):
        report = run_audit()
        assert report.total_ok   == sum(1 for c in report.checks if c["status"] == "OK")
        assert report.total_warn == sum(1 for c in report.checks if c["status"] == "WARN")
        assert report.total_fail == sum(1 for c in report.checks if c["status"] == "FAIL")


# ---------------------------------------------------------------------------
# Testes dos checkers individuais
# ---------------------------------------------------------------------------

class TestCheckersIndividuais:
    CHECKERS = [
        check_databases,
        check_structures_repository,
        check_derived_repo,
        check_derived_service,
        check_bootstrap_schema,
        check_audit_artifacts,
        check_att_patches,
    ]

    @pytest.mark.parametrize("checker_fn", CHECKERS)
    def test_checker_retorna_lista_nao_vazia(self, checker_fn):
        result = checker_fn()
        assert isinstance(result, list)
        assert len(result) > 0, f"{checker_fn.__name__} retornou lista vazia"

    @pytest.mark.parametrize("checker_fn", CHECKERS)
    def test_checker_items_tem_status_valido(self, checker_fn):
        for item in checker_fn():
            assert item.status in ("OK", "WARN", "FAIL"), (
                f"{checker_fn.__name__}: status inválido '{item.status}'"
            )

    @pytest.mark.parametrize("checker_fn", CHECKERS)
    def test_checker_items_tem_categoria_preenchida(self, checker_fn):
        for item in checker_fn():
            assert item.categoria, (
                f"{checker_fn.__name__}: categoria vazia em '{item.check}'"
            )


# ---------------------------------------------------------------------------
# Testes de geração de artefatos
# ---------------------------------------------------------------------------

class TestGeracaoArtefatos:
    def test_gerar_markdown_cria_arquivo(self):
        report = run_audit()
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "fase8_baseline.md"
            gerar_markdown(report, dest)
            assert dest.exists()
            assert len(dest.read_text(encoding="utf-8")) > 100

    def test_gerar_markdown_contem_secoes_obrigatorias(self):
        report = run_audit()
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "fase8_baseline.md"
            gerar_markdown(report, dest)
            content = dest.read_text(encoding="utf-8")
            for secao in ("patch_67", "Resumo", "OK"):
                assert secao in content, f"Seção '{secao}' ausente no markdown"

    def test_gerar_json_valido(self):
        report = run_audit()
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "fase8_baseline.json"
            gerar_json(report, dest)
            assert dest.exists()
            data = json.loads(dest.read_text(encoding="utf-8"))
            assert "gerado_em" in data
            assert "checks"    in data
            assert isinstance(data["checks"], list)

    def test_gerar_json_contem_todos_checks(self):
        report = run_audit()
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir) / "fase8_baseline.json"
            gerar_json(report, dest)
            data = json.loads(dest.read_text(encoding="utf-8"))
            assert len(data["checks"]) == len(report.checks)

    def test_reports_dir_configurado_corretamente(self):
        assert "ATT"     in str(REPORTS_DIR)
        assert "reports" in str(REPORTS_DIR)

    def test_arquivo_real_existe_apos_execucao(self):
        md = PROJECT_ROOT / "ATT" / "reports" / "fase8_baseline.md"
        assert md.exists(), "Execute: python scripts/75_audit_fase8_baseline.py"
        assert md.stat().st_size > 0

    def test_json_real_existe_apos_execucao(self):
        json_f = PROJECT_ROOT / "ATT" / "reports" / "fase8_baseline.json"
        assert json_f.exists(), "Execute: python scripts/75_audit_fase8_baseline.py"
        data = json.loads(json_f.read_text(encoding="utf-8"))
        assert len(data["checks"]) > 0


# ---------------------------------------------------------------------------
# Regressão patch_65
# ---------------------------------------------------------------------------

class TestRegressaoPatch65:
    def test_check_remocao_get_payoff_by_aba_presente_na_auditoria(self):
        results = check_derived_service()
        removal_check = next(
            (r for r in results if "get_payoff_by_aba" in r.check), None
        )
        assert removal_check is not None, (
            "check_derived_service() não verifica remoção de get_payoff_by_aba"
        )

    def test_get_payoff_by_aba_removida_status_ok(self):
        results = check_derived_service()
        removal_check = next(
            (r for r in results if "get_payoff_by_aba" in r.check), None
        )
        assert removal_check is not None
        assert removal_check.status == "OK", (
            f"get_payoff_by_aba ainda presente — regressão patch_65. "
            f"Status: {removal_check.status}"
        )


# ---------------------------------------------------------------------------
# Smoke test de integridade geral
# ---------------------------------------------------------------------------

class TestIntegridadeGeral:
    def test_sem_fail_critico_em_infra_db(self):
        results = check_databases()
        fails   = [r for r in results if r.status == "FAIL"]
        assert not fails, (
            f"FAIL em infra_db: {[(r.check, r.detalhe) for r in fails]}"
        )

    def test_derived_service_tem_funcoes_canonicas(self):
        results   = check_derived_service()
        ok_checks = {r.check for r in results if r.status == "OK"}
        canonicas = ["save_payoff_curve", "save_decision", "cleanup_derived"]
        for fn in canonicas:
            assert any(fn in c for c in ok_checks), (
                f"função canônica '{fn}' não está OK em check_derived_service()"
            )
