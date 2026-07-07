import os
import sys

from UI.modern import app


def test_configure_runtime_sets_expected_environment(monkeypatch):
    monkeypatch.delenv("MYHUB_UI_MODE", raising=False)
    monkeypatch.delenv("MYHUB_UI_THEME", raising=False)
    monkeypatch.delenv("MYHUB_UI_APPEARANCE_MODE", raising=False)

    theme = app.configure_runtime(mode="dark", theme_name="dark")

    assert os.environ["MYHUB_UI_MODE"] == "dark"
    assert os.environ["MYHUB_UI_THEME"] == "dark"
    assert os.environ["MYHUB_UI_APPEARANCE_MODE"] == theme["appearance_mode"]


def test_main_info_prints_launcher_diagnostics_without_launching(monkeypatch, capsys):
    def fail_if_launch_called(*args, **kwargs):
        raise AssertionError("launch_module should not be called when --info is used")

    monkeypatch.setattr(app, "launch_module", fail_if_launch_called)

    result = app.main(["--mode", "dark", "--theme", "dark", "--info"])

    captured = capsys.readouterr()

    assert result == 0
    assert "[ModernApp] Informações do launcher moderno" in captured.out
    assert "mode: dark" in captured.out
    assert "theme: dark" in captured.out
    assert "module: UI.modern.dark_window" in captured.out


def test_main_defaults_to_dark_mode_and_forwards_passthrough_args(monkeypatch):
    calls = []

    def fake_launch_module(mode, passthrough_args):
        calls.append((mode, passthrough_args))

    monkeypatch.setattr(app, "launch_module", fake_launch_module)

    result = app.main(["--theme", "dark", "--extra-arg", "123"])

    assert result == 0
    assert calls == [("dark", ["--extra-arg", "123"])]
    assert os.environ["MYHUB_UI_MODE"] == "dark"
    assert os.environ["MYHUB_UI_THEME"] == "dark"


def test_main_can_route_to_shell_mode_without_opening_ui(monkeypatch):
    calls = []

    def fake_launch_module(mode, passthrough_args):
        calls.append((mode, passthrough_args))

    monkeypatch.setattr(app, "launch_module", fake_launch_module)

    result = app.main(["--mode", "shell", "--theme", "clean"])

    assert result == 0
    assert calls == [("shell", [])]
    assert os.environ["MYHUB_UI_MODE"] == "shell"
    assert os.environ["MYHUB_UI_THEME"] == "clean"


def test_launch_module_runs_selected_module_and_restores_sys_argv(monkeypatch):
    original_argv = sys.argv[:]
    calls = []

    def fake_run_module(module_name, run_name):
        calls.append(
            {
                "module_name": module_name,
                "run_name": run_name,
                "sys_argv": sys.argv[:],
            }
        )

    monkeypatch.setattr(app.runpy, "run_module", fake_run_module)

    app.launch_module("dark", ["--sample", "abc"])

    assert calls == [
        {
            "module_name": "UI.modern.dark_window",
            "run_name": "__main__",
            "sys_argv": [
                "python -m UI.modern.dark_window",
                "--sample",
                "abc",
            ],
        }
    ]
    assert sys.argv == original_argv
