from pathlib import Path


def test_structure_editor_dialog_does_not_call_rtd_refresh_script_via_subprocess():
    text = Path("UI/components/structure_editor_dialog.py").read_text(
        encoding="utf-8",
        errors="replace",
    )

    assert "refresh_rtd_symbol_to_option_quotes" not in text
    assert "subprocess.run(" not in text
    assert "import subprocess" not in text
