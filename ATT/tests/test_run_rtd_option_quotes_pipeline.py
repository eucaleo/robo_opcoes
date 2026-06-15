from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "run_rtd_option_quotes_pipeline.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "run_rtd_option_quotes_pipeline_under_test",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_import_command_uses_csv_db_and_script_path():
    module = load_module()

    command = module.build_import_command(
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/app.db",
    )

    assert command[0] == sys.executable
    assert command[1].endswith("import_rtd_links_to_option_quotes.py")
    assert "--csv" in command
    assert "dados/RTD_LINKS.csv" in command
    assert "--db" in command
    assert "dados/app.db" in command
    assert "--dry-run" not in command


def test_build_import_command_includes_dry_run_when_requested():
    module = load_module()

    command = module.build_import_command(
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/app.db",
        dry_run=True,
    )

    assert "--dry-run" in command


def test_build_audit_command_uses_db_and_max_age():
    module = load_module()

    command = module.build_audit_command(
        db_path="dados/app.db",
        max_age_minutes=15,
    )

    assert command[0] == sys.executable
    assert command[1].endswith("audit_rtd_option_quotes.py")
    assert "--db" in command
    assert "dados/app.db" in command
    assert "--max-age-minutes" in command
    assert "15" in command
    assert "--json" not in command
    assert "--fail-on-warn" not in command


def test_build_audit_command_includes_json_and_fail_on_warn():
    module = load_module()

    command = module.build_audit_command(
        db_path="dados/app.db",
        max_age_minutes=30,
        json_output=True,
        fail_on_warn=True,
    )

    assert "--json" in command
    assert "--fail-on-warn" in command


def test_run_pipeline_stops_when_import_fails(monkeypatch):
    module = load_module()
    calls = []

    def fake_run_command(command):
        calls.append(command)
        return 9

    monkeypatch.setattr(module, "run_command", fake_run_command)

    code = module.run_pipeline(
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/app.db",
    )

    assert code == 9
    assert len(calls) == 1
    assert calls[0][1].endswith("import_rtd_links_to_option_quotes.py")


def test_run_pipeline_runs_import_and_audit_when_import_succeeds(monkeypatch):
    module = load_module()
    calls = []

    def fake_run_command(command):
        calls.append(command)
        return 0

    monkeypatch.setattr(module, "run_command", fake_run_command)

    code = module.run_pipeline(
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/app.db",
    )

    assert code == 0
    assert len(calls) == 2
    assert calls[0][1].endswith("import_rtd_links_to_option_quotes.py")
    assert calls[1][1].endswith("audit_rtd_option_quotes.py")


def test_run_pipeline_dry_run_skips_audit(monkeypatch):
    module = load_module()
    calls = []

    def fake_run_command(command):
        calls.append(command)
        return 0

    monkeypatch.setattr(module, "run_command", fake_run_command)

    code = module.run_pipeline(
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/app.db",
        dry_run=True,
    )

    assert code == 0
    assert len(calls) == 1
    assert calls[0][1].endswith("import_rtd_links_to_option_quotes.py")
    assert "--dry-run" in calls[0]


def test_run_pipeline_returns_audit_code_when_audit_fails(monkeypatch):
    module = load_module()
    calls = []

    def fake_run_command(command):
        calls.append(command)
        if command[1].endswith("import_rtd_links_to_option_quotes.py"):
            return 0
        return 2

    monkeypatch.setattr(module, "run_command", fake_run_command)

    code = module.run_pipeline(
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/app.db",
    )

    assert code == 2
    assert len(calls) == 2


def test_main_parses_arguments_and_runs_pipeline(monkeypatch):
    module = load_module()
    received = {}

    def fake_run_pipeline(**kwargs):
        received.update(kwargs)
        return 0

    monkeypatch.setattr(module, "run_pipeline", fake_run_pipeline)

    code = module.main(
        [
            "--csv",
            "x.csv",
            "--db",
            "x.db",
            "--dry-run",
            "--max-age-minutes",
            "5",
            "--json-audit",
            "--fail-on-warn",
        ]
    )

    assert code == 0
    assert received == {
        "csv_path": "x.csv",
        "db_path": "x.db",
        "dry_run": True,
        "max_age_minutes": 5,
        "json_audit": True,
        "fail_on_warn": True,
    }
