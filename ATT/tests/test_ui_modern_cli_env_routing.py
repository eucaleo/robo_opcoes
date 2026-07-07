import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_ui_modern_info_with_env(env_overrides=None, *args):
    env = os.environ.copy()

    env.pop("MYHUB_UI_MODE", None)
    env.pop("MYHUB_UI_THEME", None)
    env.pop("MYHUB_UI_APPEARANCE_MODE", None)

    if env_overrides:
        env.update(env_overrides)

    return subprocess.run(
        [sys.executable, "-m", "UI.modern", *args, "--info"],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
    )


def test_python_m_ui_modern_info_uses_mode_and_theme_from_environment():
    result = run_ui_modern_info_with_env(
        {
            "MYHUB_UI_MODE": "shell",
            "MYHUB_UI_THEME": "clean",
        }
    )

    assert result.returncode == 0, result.stderr
    assert "[ModernApp] Informações do launcher moderno" in result.stdout
    assert "mode: shell" in result.stdout
    assert "theme: clean" in result.stdout


def test_python_m_ui_modern_info_cli_arguments_override_environment():
    result = run_ui_modern_info_with_env(
        {
            "MYHUB_UI_MODE": "shell",
            "MYHUB_UI_THEME": "clean",
        },
        "--mode",
        "dark",
        "--theme",
        "dark",
    )

    assert result.returncode == 0, result.stderr
    assert "mode: dark" in result.stdout
    assert "theme: dark" in result.stdout
    assert "module: UI.modern.dark_window" in result.stdout


def test_python_m_ui_modern_info_ignores_invalid_environment_values():
    result = run_ui_modern_info_with_env(
        {
            "MYHUB_UI_MODE": "banana",
            "MYHUB_UI_THEME": "neon",
        }
    )

    assert result.returncode == 0, result.stderr
    assert "[ModernApp] Informações do launcher moderno" in result.stdout
    assert "mode: dark" in result.stdout
    assert "theme: dark" in result.stdout
    assert "module: UI.modern.dark_window" in result.stdout


def test_python_m_ui_modern_info_cli_mode_overrides_environment_without_overriding_theme():
    result = run_ui_modern_info_with_env(
        {
            "MYHUB_UI_MODE": "shell",
            "MYHUB_UI_THEME": "clean",
        },
        "--mode",
        "dark",
    )

    assert result.returncode == 0, result.stderr
    assert "[ModernApp] Informações do launcher moderno" in result.stdout
    assert "mode: dark" in result.stdout
    assert "theme: clean" in result.stdout
    assert "module: UI.modern.dark_window" in result.stdout
