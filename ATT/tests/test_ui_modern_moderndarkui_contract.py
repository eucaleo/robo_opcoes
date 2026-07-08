import os
import subprocess
import sys
from pathlib import Path


def run_ui_modern(*args):
    env = os.environ.copy()
    env.pop("MYHUB_UI_THEME", None)
    env.pop("MYHUB_UI_MODE", None)
    return subprocess.run(
        [sys.executable, "-m", "UI.modern", *args],
        cwd=os.getcwd(),
        env=env,
        text=True,
        capture_output=True,
    )


def test_configure_runtime_sets_moderndarkui_contract(monkeypatch):
    import UI.modern.app as app

    monkeypatch.setenv("MYHUB_UI_THEME", "old_value")
    monkeypatch.setenv("MYHUB_UI_MODE", "old_value")

    runtime = app.configure_runtime()

    assert runtime["ui"] == "modern"
    assert runtime["style"] == "modernDarkUI"
    assert runtime["module"] == "UI.modern.dark_window"
    assert os.environ["MYHUB_UI"] == "modern"
    assert os.environ["MYHUB_UI_STYLE"] == "modernDarkUI"
    assert os.environ["MYHUB_UI_MODULE"] == "UI.modern.dark_window"
    assert "MYHUB_UI_THEME" not in os.environ
    assert "MYHUB_UI_MODE" not in os.environ


def test_main_without_info_routes_to_official_moderndarkui_module(monkeypatch):
    import UI.modern.app as app

    calls = []

    class FakeModule:
        @staticmethod
        def main():
            calls.append("main")
            return 0

    def fake_import_module(name):
        calls.append(name)
        return FakeModule()

    monkeypatch.setattr(app.importlib, "import_module", fake_import_module)

    result = app.main([])

    assert result == 0
    assert calls == ["UI.modern.dark_window", "main"]


def test_info_outputs_only_moderndarkui_contract():
    result = run_ui_modern("--info")

    assert result.returncode == 0
    assert "ui: modern" in result.stdout
    assert "style: modernDarkUI" in result.stdout
    assert "style: black" not in result.stdout
    assert "module: UI.modern.dark_window" in result.stdout
    assert "clean" not in result.stdout.lower()
    assert "shell" not in result.stdout.lower()
    assert "theme:" not in result.stdout.lower()
    assert "mode:" not in result.stdout.lower()


def test_help_does_not_publish_old_theme_or_shell_contract():
    result = run_ui_modern("--help")

    assert result.returncode == 0
    stdout = result.stdout.lower()
    assert "--info" in stdout
    assert "--theme" not in stdout
    assert "clean" not in stdout
    assert "shell" not in stdout
    assert "--mode" not in stdout


def test_old_theme_argument_is_rejected():
    result = run_ui_modern("--theme", "clean", "--info")

    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr.lower()


def test_old_shell_argument_is_rejected():
    result = run_ui_modern("--mode", "shell", "--info")

    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr.lower()


def test_legacy_theme_module_was_removed_from_moderndarkui_contract():
    root = Path(__file__).resolve().parents[2]
    theme_file = root / "UI" / "modern" / "theme.py"
    dark_window_file = root / "UI" / "modern" / "dark_window.py"

    assert not theme_file.exists()

    dark_window_source = dark_window_file.read_text(encoding="utf-8")
    assert "UI.modern.theme" not in dark_window_source
    assert "from UI.modern.theme" not in dark_window_source
    assert 'CUSTOMTKINTER_APPEARANCE_MODE = "Dark"' in dark_window_source
    assert 'CUSTOMTKINTER_COLOR_THEME = "blue"' in dark_window_source

