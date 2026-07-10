from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_operational_dark_window_help_menu_and_live_excel_rtd_status() -> None:
    """
    Teste operacional real.

    Valida em um subprocess Python limpo, fora dos fakes de tkinter do conftest:

    - import real de UI.modern.dark_window;
    - tkinter/customtkinter/matplotlib reais;
    - construção real do menu Ajuda;
    - presença do item "Status RTD Excel";
    - payload real do RTD/Excel ativo;
    - formatação real da mensagem exibida pela UI.

    Este teste deve falhar se Excel/RTD/workbook/aba/cabeçalhos não estiverem
    prontos no ambiente operacional.
    """
    code = r'''
import json
import tkinter as tk

import UI.modern.dark_window as module


root = tk.Tk()
root.withdraw()

try:
    window = module.ModernDarkWindow.__new__(module.ModernDarkWindow)
    window.root = root
    window._build_menu()

    menu_name = root.cget("menu")
    menu_bar = root.nametowidget(menu_name)

    help_labels = []
    top_level_labels = []

    end_index = menu_bar.index("end")
    if end_index is not None:
        for index in range(end_index + 1):
            item_type = menu_bar.type(index)

            if item_type not in {"cascade", "command"}:
                continue

            label = menu_bar.entrycget(index, "label")
            top_level_labels.append(label)

            if label == "Ajuda":
                help_menu_name = menu_bar.entrycget(index, "menu")
                help_menu = root.nametowidget(help_menu_name)
                help_end_index = help_menu.index("end")

                if help_end_index is not None:
                    for help_index in range(help_end_index + 1):
                        help_item_type = help_menu.type(help_index)

                        if help_item_type != "command":
                            continue

                        help_labels.append(help_menu.entrycget(help_index, "label"))

    payload = module.get_excel_rtd_status_payload()
    message = module._format_excel_rtd_status_message(payload)

    result = {
        "top_level_labels": top_level_labels,
        "help_labels": help_labels,
        "payload": payload,
        "message": message,
    }

    print("RESULT_JSON=" + json.dumps(result, ensure_ascii=False))
finally:
    root.destroy()
'''

    completed = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert completed.returncode == 0, (
        "Subprocess operacional falhou.\n\n"
        f"STDOUT:\n{completed.stdout}\n\n"
        f"STDERR:\n{completed.stderr}"
    )

    result_lines = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith("RESULT_JSON=")
    ]

    assert result_lines, (
        "Subprocess operacional não retornou RESULT_JSON.\n\n"
        f"STDOUT:\n{completed.stdout}\n\n"
        f"STDERR:\n{completed.stderr}"
    )

    data = json.loads(result_lines[-1].removeprefix("RESULT_JSON="))

    assert "Ajuda" in data["top_level_labels"]
    assert "Status RTD Excel" in data["help_labels"]

    payload = data["payload"]

    assert payload["ready"] is True, json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
    )
    assert payload["severity"] == "ok", json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
    )
    assert payload["title"] == "RTD Excel online"
    assert payload["missing_headers"] == []

    checks_by_key = {
        check["key"]: check
        for check in payload["checks"]
    }

    assert checks_by_key["pywin32_available"]["ok"] is True
    assert checks_by_key["excel_running"]["ok"] is True
    assert checks_by_key["workbook_open"]["ok"] is True
    assert checks_by_key["worksheet_available"]["ok"] is True
    assert checks_by_key["required_headers_ok"]["ok"] is True

    message = data["message"]

    assert "Pronto para leitura: Sim" in message
    assert "Severidade: ok" in message
    assert f"Workbook: {payload['workbook_name']}" in message
    assert f"Aba: {payload['worksheet_name']}" in message
