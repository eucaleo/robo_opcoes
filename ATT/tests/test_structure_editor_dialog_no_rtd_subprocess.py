from pathlib import Path


def test_structure_editor_dialog_does_not_call_rtd_refresh_script_via_subprocess():
    text = Path("UI/components/structure_editor_dialog.py").read_text(
        encoding="utf-8",
        errors="replace",
    )

    assert "refresh_rtd_symbol_to_option_quotes" not in text
    assert "subprocess.run(" not in text
    assert "import subprocess" not in text


def test_structure_editor_dialog_does_not_sync_rtd_excel_from_ui():
    """A UI deve consumir somente o snapshot rtd_option_quotes.

    O preenchimento de leg nao pode chamar a sincronizacao direta do Excel,
    pois essa responsabilidade pertence ao produtor externo do snapshot.
    """
    from pathlib import Path

    source_path = (
        Path(__file__).resolve().parents[2]
        / "UI"
        / "components"
        / "structure_editor_dialog.py"
    )
    source = source_path.read_text(encoding="utf-8")

    assert "rtd_option_quotes_sync_service" not in source
    assert "sync_rtd_option_quotes_from_excel" not in source
