from __future__ import annotations

import pytest

from UI.modern.smoke_mode import (
    DEFAULT_SMOKE_CLOSE_MS,
    SMOKE_CLOSE_MS_ENV_VAR,
    SMOKE_ENV_VAR,
    get_smoke_close_delay_ms,
    install_smoke_shutdown_if_requested,
    is_smoke_mode_enabled,
)


class FakeRoot:
    def __init__(self) -> None:
        self.after_calls = []
        self.quit_called = False
        self.destroy_called = False

    def after(self, delay_ms, callback):
        self.after_calls.append((delay_ms, callback))

    def quit(self):
        self.quit_called = True

    def destroy(self):
        self.destroy_called = True


class FakeApp:
    def __init__(self) -> None:
        self.root = FakeRoot()


class ObjectWithoutTkMethods:
    pass


def test_smoke_mode_is_disabled_by_default():
    assert is_smoke_mode_enabled({}) is False


def test_smoke_mode_is_enabled_by_environment_variable():
    assert is_smoke_mode_enabled({SMOKE_ENV_VAR: "1"}) is True


def test_smoke_mode_ignores_non_enabled_values():
    assert is_smoke_mode_enabled({SMOKE_ENV_VAR: "0"}) is False
    assert is_smoke_mode_enabled({SMOKE_ENV_VAR: "true"}) is False
    assert is_smoke_mode_enabled({SMOKE_ENV_VAR: ""}) is False


def test_get_smoke_close_delay_uses_default_when_missing():
    assert get_smoke_close_delay_ms({}) == DEFAULT_SMOKE_CLOSE_MS


def test_get_smoke_close_delay_reads_integer_from_environment():
    assert get_smoke_close_delay_ms({SMOKE_CLOSE_MS_ENV_VAR: "250"}) == 250


def test_get_smoke_close_delay_falls_back_for_invalid_values():
    assert get_smoke_close_delay_ms({SMOKE_CLOSE_MS_ENV_VAR: "abc"}) == DEFAULT_SMOKE_CLOSE_MS
    assert get_smoke_close_delay_ms({SMOKE_CLOSE_MS_ENV_VAR: "0"}) == DEFAULT_SMOKE_CLOSE_MS
    assert get_smoke_close_delay_ms({SMOKE_CLOSE_MS_ENV_VAR: "-1"}) == DEFAULT_SMOKE_CLOSE_MS


def test_install_smoke_shutdown_returns_false_when_disabled():
    root = FakeRoot()

    scheduled = install_smoke_shutdown_if_requested(root, environ={})

    assert scheduled is False
    assert root.after_calls == []


def test_install_smoke_shutdown_schedules_close_when_enabled():
    root = FakeRoot()

    scheduled = install_smoke_shutdown_if_requested(
        root,
        environ={SMOKE_ENV_VAR: "1", SMOKE_CLOSE_MS_ENV_VAR: "123"},
    )

    assert scheduled is True
    assert len(root.after_calls) == 1

    delay_ms, callback = root.after_calls[0]

    assert delay_ms == 123

    callback()

    assert root.quit_called is True
    assert root.destroy_called is True


def test_install_smoke_shutdown_accepts_app_object_with_root_attribute():
    app = FakeApp()

    scheduled = install_smoke_shutdown_if_requested(
        app,
        environ={SMOKE_ENV_VAR: "1"},
        close_delay_ms=10,
    )

    assert scheduled is True
    assert len(app.root.after_calls) == 1

    delay_ms, callback = app.root.after_calls[0]

    assert delay_ms == 10

    callback()

    assert app.root.quit_called is True
    assert app.root.destroy_called is True


def test_install_smoke_shutdown_requires_tk_like_object_when_enabled():
    with pytest.raises(TypeError, match="Tk-like object"):
        install_smoke_shutdown_if_requested(
            ObjectWithoutTkMethods(),
            environ={SMOKE_ENV_VAR: "1"},
        )
