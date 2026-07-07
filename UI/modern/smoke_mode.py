"""Smoke mode utilities for the modern UI entrypoint.

This module allows the modern UI to be launched through the real route:

    python -m UI.modern

When ATT_MODERN_UI_SMOKE=1 is present, the UI schedules an automatic
shutdown after a short delay.

The goal is to make the modern UI route testable without changing the
normal interactive behavior.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any


SMOKE_ENV_VAR = "ATT_MODERN_UI_SMOKE"
SMOKE_CLOSE_MS_ENV_VAR = "ATT_MODERN_UI_SMOKE_CLOSE_MS"
DEFAULT_SMOKE_CLOSE_MS = 500


def is_smoke_mode_enabled(
    environ: Mapping[str, str] | None = None,
) -> bool:
    """Return True when modern UI smoke mode is enabled."""

    env = os.environ if environ is None else environ
    return env.get(SMOKE_ENV_VAR) == "1"


def get_smoke_close_delay_ms(
    environ: Mapping[str, str] | None = None,
    default: int = DEFAULT_SMOKE_CLOSE_MS,
) -> int:
    """Return the auto-close delay for smoke mode.

    Invalid values fall back to the default. Values below 1 are ignored.
    """

    env = os.environ if environ is None else environ
    raw_value = env.get(SMOKE_CLOSE_MS_ENV_VAR)

    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError:
        return default

    if value < 1:
        return default

    return value


def _resolve_root(widget_or_app: Any) -> Any:
    """Resolve the root-like object used by the modern UI."""

    for attr_name in ("root", "master", "window"):
        candidate = getattr(widget_or_app, attr_name, None)

        if candidate is not None and hasattr(candidate, "after"):
            return candidate

    return widget_or_app


def install_smoke_shutdown_if_requested(
    widget_or_app: Any,
    *,
    environ: Mapping[str, str] | None = None,
    close_delay_ms: int | None = None,
) -> bool:
    """Schedule shutdown when smoke mode is enabled.

    Returns True when shutdown was scheduled.
    Returns False when smoke mode is disabled.
    """

    if not is_smoke_mode_enabled(environ):
        return False

    root = _resolve_root(widget_or_app)

    if not hasattr(root, "after"):
        raise TypeError("Modern UI smoke mode requires a Tk-like object with after().")

    delay_ms = (
        close_delay_ms
        if close_delay_ms is not None
        else get_smoke_close_delay_ms(environ)
    )

    def shutdown() -> None:
        quit_method = getattr(root, "quit", None)
        destroy_method = getattr(root, "destroy", None)

        if callable(quit_method):
            quit_method()

        if callable(destroy_method):
            destroy_method()

    root.after(delay_ms, shutdown)
    return True
