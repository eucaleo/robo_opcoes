#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path


UI_PATH = Path("UI/components/terminal_vwap_payoff_dark_panel.py")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_method_source(text: str, method_name: str) -> str:
    pattern = re.compile(
        rf"(?ms)^([ \t]+)def {re.escape(method_name)}\s*\([^)]*\).*?(?=^\1def |\Z)"
    )
    match = pattern.search(text)
    return match.group(0) if match else ""


def _ok(message: str) -> None:
    print(f"OK: {message}")


def _fail(message: str) -> int:
    print(f"ERRO: {message}")
    return 1


def _db_has_payoff_points(db_path: Path) -> bool:
    if not db_path.exists():
        return False

    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name IN (
                  'payoff_curve_points',
                  'rtd_payoff_points',
                  'rtd_payoff_curva',
                  'payoff_points'
              )
            """
        ).fetchall()

        return bool(rows)
    finally:
        conn.close()


def _load_payoff_points_without_local_fallback(ui_text: str) -> bool:
    source = _extract_method_source(ui_text, "_load_payoff_points")
    if not source:
        return False

    forbidden_tokens = [
        "_calculate_payoff",
        "calculate_payoff",
        "black_scholes",
        "bs_price",
        "fallback",
        "cálculo local",
        "calculo local",
    ]

    lowered = source.lower()
    return not any(token.lower() in lowered for token in forbidden_tokens)


def _persisted_payoff_uses_latest_timestamp(ui_text: str) -> bool:
    source = _extract_method_source(ui_text, "_load_persisted_payoff_points")
    if not source:
        return False

    compact = re.sub(r"\s+", " ", source).lower()

    has_timestamp_detection = any(
        token in compact
        for token in [
            '"timestamp"',
            "'timestamp'",
            "updated_at",
            "created_at",
            "dt_ref",
            "ts_col",
        ]
    )

    uses_max_snapshot = (
        "max(timestamp)" in compact
        or "max({_q(ts_col)})" in compact
        or "max(" in compact and "ultimo_timestamp" in compact
    )

    uses_desc_limit_snapshot = (
        "order by" in compact
        and "timestamp" in compact
        and "desc" in compact
        and "limit 1" in compact
    )

    resolves_latest_row = "latest_row" in compact
    resolves_latest_ts = "latest_ts" in compact or "ultimo_timestamp" in compact

    filters_final_snapshot = (
        "and" in compact
        and "ts_col" in compact
        and "= ?" in compact
    ) or (
        "timestamp" in compact
        and "= ?" in compact
    )

    orders_points = "order by" in compact and (
        "spot_col" in compact
        or "point_spot" in compact
        or "spot" in compact
    )

    return all(
        [
            has_timestamp_detection,
            uses_max_snapshot or uses_desc_limit_snapshot,
            resolves_latest_row,
            resolves_latest_ts,
            filters_final_snapshot,
            orders_points,
        ]
    )


def _ui_starts_auto_refresh(ui_text: str) -> bool:
    tokens = [
        "run_rtd_and_payoff_auto_refresh_loop.py",
        "run_rtd_and_payoff_auto_refresh_loop",
        "auto-refresh",
        "auto_refresh",
    ]
    return any(token in ui_text for token in tokens)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="dados/app.db")
    args = parser.parse_args()

    db_path = Path(args.db)

    if not UI_PATH.exists():
        return _fail(f"arquivo UI não encontrado: {UI_PATH}")

    _ok(f"arquivo UI encontrado: {UI_PATH}")

    ui_text = _read(UI_PATH)

    if "import os" not in ui_text:
        return _fail("import os não encontrado")
    _ok("import os encontrado")

    if not _ui_starts_auto_refresh(ui_text):
        return _fail("auto-refresh não parece ser iniciado pela UI")
    _ok("auto-refresh é iniciado pela UI")

    if not _load_payoff_points_without_local_fallback(ui_text):
        return _fail("_load_payoff_points parece fazer fallback de cálculo local")
    _ok("_load_payoff_points não faz fallback de cálculo local")

    if not _persisted_payoff_uses_latest_timestamp(ui_text):
        return _fail("_load_persisted_payoff_points não parece buscar o último snapshot por timestamp")
    _ok("_load_persisted_payoff_points busca o último snapshot por timestamp")

    if db_path.exists():
        if _db_has_payoff_points(db_path):
            _ok(f"banco encontrado e possui tabela de payoff: {db_path}")
        else:
            print(f"AVISO: banco encontrado, mas nenhuma tabela de payoff conhecida foi localizada: {db_path}")
    else:
        print(f"AVISO: banco não encontrado para inspeção opcional: {db_path}")

    print("OK: arquitetura de refresh/payoff validada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
