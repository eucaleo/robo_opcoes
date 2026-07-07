import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_ui_modern_info(*args):
    env = os.environ.copy()
    env.pop("MYHUB_UI_MODE", None)
    env.pop("MYHUB_UI_THEME", None)
    env.pop("MYHUB_UI_APPEARANCE_MODE", None)

    return subprocess.run(
        [sys.executable, "-m", "UI.modern", *args, "--info"],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
    )


def test_python_m_ui_modern_info_cli_reports_default_dark_launcher():
    result = run_ui_modern_info()

    assert result.returncode == 0, result.stderr
    assert "[ModernApp] Informações do launcher moderno" in result.stdout
    assert "mode: dark" in result.stdout
    assert "theme: dark" in result.stdout
    assert "module: UI.modern.dark_window" in result.stdout


def test_python_m_ui_modern_info_cli_accepts_explicit_dark_mode():
    result = run_ui_modern_info("--mode", "dark", "--theme", "dark")

    assert result.returncode == 0, result.stderr
    assert "mode: dark" in result.stdout
    assert "theme: dark" in result.stdout
    assert "module: UI.modern.dark_window" in result.stdout


def test_python_m_ui_modern_info_cli_accepts_shell_mode_without_opening_ui():
    result = run_ui_modern_info("--mode", "shell", "--theme", "clean")

    assert result.returncode == 0, result.stderr
    assert "mode: shell" in result.stdout
    assert "theme: clean" in result.stdout
