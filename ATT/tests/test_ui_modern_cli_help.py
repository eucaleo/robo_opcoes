import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_python_m_ui_modern_help_cli_reports_available_launcher_options():
    env = os.environ.copy()
    env.pop("MYHUB_UI_MODE", None)
    env.pop("MYHUB_UI_THEME", None)
    env.pop("MYHUB_UI_APPEARANCE_MODE", None)

    result = subprocess.run(
        [sys.executable, "-m", "UI.modern", "--help"],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr

    stdout = result.stdout.lower()

    assert "usage:" in stdout
    assert "--mode" in result.stdout
    assert "--theme" in result.stdout
    assert "--info" in result.stdout
    assert "dark" in result.stdout
    assert "shell" in result.stdout


def test_python_m_ui_modern_help_documents_main_options_without_launching_ui():
    import os
    import subprocess
    import sys

    env = os.environ.copy()
    env.setdefault("PYTHONPATH", os.getcwd())

    result = subprocess.run(
        [sys.executable, "-m", "UI.modern", "--help"],
        cwd=os.getcwd(),
        env=env,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0, result.stderr
    assert "usage:" in result.stdout
    assert "--mode" in result.stdout
    assert "--theme" in result.stdout
    assert "--info" in result.stdout
    assert "[ModernApp] Informações do launcher moderno" not in result.stdout
