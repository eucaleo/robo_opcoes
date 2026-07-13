from pathlib import Path


def test_modern_dark_window_operational_data_status_menu_contract():
    source = Path("UI/modern/dark_window.py").read_text(encoding="utf-8")

    assert (
        "from services.operational_data_status_service import "
        "build_operational_data_status"
    ) in source
    assert 'label="Status dados operacionais"' in source
    assert "command=self._show_operational_data_status" in source
    assert "def _show_operational_data_status" in source
    assert "def _format_operational_data_status_message" in source

    method_start = source.index("    def _show_operational_data_status")
    method_end = source.index("    def _show_excel_rtd_status")
    method = source[method_start:method_end]

    assert "build_operational_data_status(APP_DB_PATH)" in method

    forbidden_terms = [
        "subprocess",
        "win32com",
        "Dispatch",
        "GetObject",
        "while True",
    ]

    for term in forbidden_terms:
        assert term not in method


def test_modern_dark_window_operational_data_status_formatter_contract():
    source = Path("UI/modern/dark_window.py").read_text(encoding="utf-8")

    assert "Resumo operacional dos dados" in source
    assert "Status:" in source
    assert "Banco:" in source
    assert "_format_operational_data_status_dict" in source
    assert "_format_operational_data_status_label" in source
