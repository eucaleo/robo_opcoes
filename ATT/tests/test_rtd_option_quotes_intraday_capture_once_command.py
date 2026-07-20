from __future__ import annotations

import importlib.util
import inspect
import json
import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
CMD_PATH = ROOT_DIR / "scripts" / "rtd_option_quotes_intraday_capture_once.py"


def _load_command_module():
    spec = importlib.util.spec_from_file_location(
        "rtd_option_quotes_intraday_capture_once",
        CMD_PATH,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def test_capture_once_command_accepts_db_and_dry_run_args():
    module = _load_command_module()

    parser = module.build_parser()
    args = parser.parse_args(["--db", "arquivo.sqlite", "--dry-run"])

    assert args.db == "arquivo.sqlite"
    assert args.dry_run is True


def test_capture_once_command_dry_run_counts_snapshot_rows(tmp_path):
    module = _load_command_module()

    db_path = tmp_path / "rtd.sqlite"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                codigo_opcao TEXT NOT NULL,
                preco REAL
            )
            """
        )
        conn.execute(
            "INSERT INTO rtd_option_quotes (codigo_opcao, preco) VALUES (?, ?)",
            ("PETRA100", 1.23),
        )
        conn.execute(
            "INSERT INTO rtd_option_quotes (codigo_opcao, preco) VALUES (?, ?)",
            ("PETRA101", 1.45),
        )

    result = module.run_capture_once(db_path, dry_run=True)

    assert result["mode"] == "dry-run"
    assert result["snapshot_rows"] == 2
    assert result["captured_rows"] == 0


def test_capture_once_command_main_outputs_json_in_dry_run(tmp_path, capsys):
    module = _load_command_module()

    db_path = tmp_path / "rtd.sqlite"

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                codigo_opcao TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT INTO rtd_option_quotes (codigo_opcao) VALUES (?)",
            ("PETRA100",),
        )

    exit_code = module.main(["--db", str(db_path), "--dry-run"])
    captured = capsys.readouterr()

    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["ok"] is True
    assert payload["mode"] == "dry-run"
    assert payload["snapshot_rows"] == 1


def test_capture_once_command_has_no_loop_or_external_dependency_literals():
    module = _load_command_module()
    source = inspect.getsource(module).lower()

    forbidden_terms = [
        "win32" + "com",
        "xl" + "wings",
        "." + "work" + "books",
        "." + "sheets",
        "po" + "pen",
        "sub" + "process",
    ]

    assert ("while " + "true") not in source

    for term in forbidden_terms:
        assert term not in source


def test_capture_once_generated_files_have_no_backtick_character():
    files = [
        CMD_PATH,
        ROOT_DIR / "ATT" / "tests" / "test_rtd_option_quotes_intraday_capture_once_command.py",
        # Documento histórico removido junto com artefatos obsoletos da frente RTD.
    ]

    for path in files:
        assert path.exists()
        assert chr(96) not in path.read_text(encoding="utf-8")
