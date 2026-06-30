from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


RTD_LIVE_OPERATIONAL_FILES = [
    "repositories/rtd_option_quotes_repository.py",
    "repositories/market_snapshot_repository.py",
    "services/structure_leg_rtd_enrichment_service.py",
    "UI/components/structure_editor_dialog.py",
    "UI/components/terminal_vwap_payoff_dark_panel.py",
    "infra/bootstrap_rtd_option_quotes_schema.py",
    "scripts/import_rtd_option_quotes_wide_csv.py",
    "scripts/refresh_rtd_symbol_to_option_quotes.py",
    "scripts/refresh_rtd_symbol_to_option_quotes_fallback.py",
]


FORBIDDEN_DERIVED_MARKERS = [
    "dados/derived.db",
    "data/derived.db",
    "derived.db",
    "DERIVED_DB_PATH",
    "connect_derived",
]


def _read_project_file(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    assert path.exists(), f"Arquivo esperado não encontrado: {relative_path}"
    return path.read_text(encoding="utf-8", errors="replace")


def test_rtd_live_operational_files_do_not_reference_derived_db():
    """
    RTD vivo operacional deve usar dados/app.db.

    A tabela rtd_option_quotes e a tabela rtd_underlying_quotes não podem voltar
    a ser lidas/escritas operacionalmente em dados/derived.db.

    derived.db permanece válido para payoff, snapshots derivados, simulações e
    artefatos regeneráveis, mas não para cache vivo RTD.
    """
    violations = []

    for relative_path in RTD_LIVE_OPERATIONAL_FILES:
        text = _read_project_file(relative_path)
        for marker in FORBIDDEN_DERIVED_MARKERS:
            if marker in text:
                violations.append(f"{relative_path}: contém marcador proibido `{marker}`")

    assert not violations, "\n".join(violations)


def test_rtd_option_quotes_repository_default_db_is_app_db():
    """
    O repositório operacional de rtd_option_quotes deve apontar por padrão para dados/app.db.
    """
    text = _read_project_file("repositories/rtd_option_quotes_repository.py")

    assert '"dados/app.db"' in text or "'dados/app.db'" in text
    assert '"dados/derived.db"' not in text
    assert "'dados/derived.db'" not in text


def test_structure_editor_rtd_refresh_and_enrichment_use_app_db():
    """
    A UI de edição de estrutura, ao atualizar/preencher leg via RTD, deve usar app.db.
    """
    text = _read_project_file("UI/components/structure_editor_dialog.py")

    assert 'project_root / "dados" / "app.db"' in text
    assert 'project_root / "dados" / "derived.db"' not in text
