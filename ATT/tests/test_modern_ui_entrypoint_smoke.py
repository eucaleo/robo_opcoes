from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_modern_ui_entrypoint_module_exists():
    entrypoint = PROJECT_ROOT / "UI" / "modern" / "__main__.py"

    assert entrypoint.exists(), (
        "Expected UI.modern to expose python -m UI.modern entrypoint."
    )


@pytest.mark.ui
def test_python_m_ui_modern_smoke_route_exits_successfully():
    """Execute the real modern UI route in smoke mode.

    This test is opt-in because graphical UI execution may require a display
    server in CI environments.

    Local execution example:

        RUN_UI_SMOKE=1 pytest ATT/tests/test_modern_ui_entrypoint_smoke.py -q
    """

    if os.environ.get("RUN_UI_SMOKE") != "1":
        pytest.skip("Set RUN_UI_SMOKE=1 to execute the real modern UI smoke route.")

    env = os.environ.copy()
    env["ATT_MODERN_UI_SMOKE"] = "1"
    env["ATT_MODERN_UI_SMOKE_CLOSE_MS"] = "500"

    completed = subprocess.run(
        [sys.executable, "-m", "UI.modern"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )

    output = "\n".join(
        [
            "STDOUT:",
            completed.stdout,
            "STDERR:",
            completed.stderr,
        ]
    )

    assert completed.returncode == 0, output
