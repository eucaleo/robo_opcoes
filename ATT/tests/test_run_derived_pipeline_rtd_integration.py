import importlib.util
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "run_derived_pipeline.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "run_derived_pipeline_under_test",
        SCRIPT_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_parse_rtd_pipeline_metrics_from_stdout():
    module = load_module()

    output = """
Importação RTD wide CSV
-----------------------
input_rows: 4
inserted: 1
updated: 3
skipped: 0
updated_at: 2026-06-22 09:10:00
"""

    assert module._parse_rtd_pipeline_metrics(output) == {
        "input_rows": 4,
        "inserted": 1,
        "updated": 3,
        "skipped": 0,
    }


def test_rtd_quotes_updated_count_sums_inserted_and_updated():
    module = load_module()

    assert module._rtd_quotes_updated_count({"inserted": 2, "updated": 5}) == 7
    assert module._rtd_quotes_updated_count({"inserted": None, "updated": 5}) == 5
    assert module._rtd_quotes_updated_count(None) == 0


def test_run_rtd_option_quotes_import_uses_csv_pipeline_without_excel_or_powershell(
    tmp_path,
    monkeypatch,
):
    module = load_module()

    scripts_dir = tmp_path / "scripts"
    dados_dir = tmp_path / "dados"
    scripts_dir.mkdir()
    dados_dir.mkdir()

    (scripts_dir / "run_rtd_option_quotes_pipeline.py").write_text(
        "# fake rtd csv pipeline\n",
        encoding="utf-8",
    )
    (dados_dir / "RTD_LINKS.csv").write_text(
        "codigo_opcao;ativo_base\nPRIOG800;PRIO3\n",
        encoding="utf-8",
    )

    calls = []

    def fake_run(command, cwd, text, capture_output):
        calls.append(
            {
                "command": command,
                "cwd": cwd,
                "text": text,
                "capture_output": capture_output,
            }
        )
        return SimpleNamespace(
            returncode=0,
            stdout="input_rows: 1\ninserted: 0\nupdated: 1\nskipped: 0\n",
            stderr="",
        )

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    result = module._run_rtd_option_quotes_import(
        tmp_path,
        csv_path="dados/RTD_LINKS.csv",
        db_path="dados/derived.db",
    )

    assert result["returncode"] == 0
    assert result["input_rows"] == 1
    assert result["inserted"] == 0
    assert result["updated"] == 1
    assert result["skipped"] == 0

    assert len(calls) == 1
    command = calls[0]["command"]

    assert command[1].endswith("run_rtd_option_quotes_pipeline.py")
    assert "--csv" in command
    assert "dados/RTD_LINKS.csv" in command
    assert "--db" in command
    assert "dados/derived.db" in command

    command_text = " ".join(str(part) for part in command).lower()
    assert "powershell" not in command_text
    assert "refresh_rtd_option_quotes_excel" not in command_text
    assert "lista_rtd.xlsm" not in command_text
