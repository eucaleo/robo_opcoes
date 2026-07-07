import runpy
import sys

from UI.modern import app


def test_python_m_ui_modern_delegates_to_app_main(monkeypatch):
    calls = []

    def fake_main(argv=None):
        calls.append(argv)
        return 0

    monkeypatch.setattr(app, "main", fake_main)
    monkeypatch.setattr(sys, "argv", ["python -m UI.modern"])

    try:
        runpy.run_module("UI.modern.__main__", run_name="__main__")
    except SystemExit as exc:
        assert exc.code in (0, None)

    assert len(calls) == 1
    assert calls[0] in (None, [])


def test_python_m_ui_modern_propagates_app_main_exit_code(monkeypatch):
    calls = []

    def fake_main(argv=None):
        calls.append(argv)
        return 17

    monkeypatch.setattr(app, "main", fake_main)
    monkeypatch.setattr(sys, "argv", ["python -m UI.modern"])

    try:
        runpy.run_module("UI.modern.__main__", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 17
    else:
        raise AssertionError("UI.modern.__main__ should raise SystemExit with app.main return code")

    assert len(calls) == 1
