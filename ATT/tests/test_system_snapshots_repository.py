from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from infra.bootstrap_structures_schema import ensure_structures_schema
from repositories.system_snapshots_repository import SystemSnapshotsRepository


def _insert_structure(conn: sqlite3.Connection) -> int:
    cur = conn.execute(
        """
        INSERT INTO structures (
            name,
            underlying_asset,
            alias_legacy_aba,
            status,
            notes,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "Teste Snapshot",
            "PETR4",
            "PETR4_TESTE",
            "active",
            "estrutura para teste",
            "2026-06-12T12:00:00Z",
            "2026-06-12T12:00:00Z",
        ),
    )
    return int(cur.lastrowid)


def _insert_leg(
    conn: sqlite3.Connection,
    *,
    structure_id: int,
    leg_order: int,
    symbol: str,
    strike: float,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO structure_legs (
            structure_id,
            position_side,
            option_type,
            symbol,
            strike,
            expiration_date,
            quantity,
            premium,
            multiplier,
            leg_order,
            notes,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            structure_id,
            "long",
            "call",
            symbol,
            strike,
            "2026-12-18",
            100,
            1.25,
            1,
            leg_order,
            None,
            "2026-06-12T12:00:00Z",
            "2026-06-12T12:00:00Z",
        ),
    )
    return int(cur.lastrowid)


def test_create_snapshot_persists_snapshot_and_legs(tmp_path: Path):
    db_path = tmp_path / "app.db"
    ensure_structures_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        structure_id = _insert_structure(conn)
        leg_1_id = _insert_leg(
            conn,
            structure_id=structure_id,
            leg_order=1,
            symbol="PETRA10",
            strike=10.0,
        )
        leg_2_id = _insert_leg(
            conn,
            structure_id=structure_id,
            leg_order=2,
            symbol="PETRA12",
            strike=12.0,
        )

    repo = SystemSnapshotsRepository(db_path)

    snapshot_id = repo.create_snapshot(
        structure_id=structure_id,
        underlying_asset="PETR4",
        reference_date="2026-06-12",
        created_at="2026-06-12T15:00:00Z",
        structure_json={
            "id": structure_id,
            "name": "Teste Snapshot",
            "underlying_asset": "PETR4",
        },
        market_json={"spot": 31.25},
        metrics_json={"theoretical_value": 2.5},
        payoff_json={"max_gain": 1000},
        decision_json={"action": "hold"},
        alerts_json=[{"level": "info", "message": "ok"}],
        operation_state_json={"state": "active"},
        legs=[
            {
                "leg_id": leg_1_id,
                "leg_order": 1,
                "position_side": "long",
                "option_type": "call",
                "symbol": "PETRA10",
                "strike": 10.0,
                "expiration_date": "2026-12-18",
                "quantity": 100,
                "premium": 1.25,
                "multiplier": 1,
                "metrics_json": {"delta": 0.55},
                "market_json": {"bid": 1.2, "ask": 1.3},
            },
            {
                "leg_id": leg_2_id,
                "leg_order": 2,
                "position_side": "long",
                "option_type": "call",
                "symbol": "PETRA12",
                "strike": 12.0,
                "expiration_date": "2026-12-18",
                "quantity": 100,
                "premium": 0.95,
                "multiplier": 1,
                "metrics_json": {"delta": 0.42},
                "market_json": {"bid": 0.9, "ask": 1.0},
            },
        ],
    )

    snapshot = repo.get_snapshot(snapshot_id)

    assert snapshot is not None
    assert snapshot["id"] == snapshot_id
    assert snapshot["structure_id"] == structure_id
    assert snapshot["underlying_asset"] == "PETR4"
    assert snapshot["reference_date"] == "2026-06-12"
    assert snapshot["snapshot_source"] == "system"
    assert snapshot["structure_json"]["name"] == "Teste Snapshot"
    assert snapshot["market_json"] == {"spot": 31.25}
    assert snapshot["metrics_json"] == {"theoretical_value": 2.5}
    assert snapshot["payoff_json"] == {"max_gain": 1000}
    assert snapshot["decision_json"] == {"action": "hold"}
    assert snapshot["alerts_json"] == [{"level": "info", "message": "ok"}]
    assert snapshot["operation_state_json"] == {"state": "active"}

    assert len(snapshot["legs"]) == 2
    assert snapshot["legs"][0]["leg_id"] == leg_1_id
    assert snapshot["legs"][0]["symbol"] == "PETRA10"
    assert snapshot["legs"][0]["metrics_json"] == {"delta": 0.55}
    assert snapshot["legs"][1]["leg_id"] == leg_2_id
    assert snapshot["legs"][1]["symbol"] == "PETRA12"
    assert snapshot["legs"][1]["market_json"] == {"bid": 0.9, "ask": 1.0}


def test_list_snapshots_for_structure_orders_by_created_at_desc(tmp_path: Path):
    db_path = tmp_path / "app.db"
    ensure_structures_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        structure_id = _insert_structure(conn)

    repo = SystemSnapshotsRepository(db_path)

    first_id = repo.create_snapshot(
        structure_id=structure_id,
        created_at="2026-06-12T10:00:00Z",
        structure_json={"version": 1},
    )
    second_id = repo.create_snapshot(
        structure_id=structure_id,
        created_at="2026-06-12T11:00:00Z",
        structure_json={"version": 2},
    )

    snapshots = repo.list_snapshots_for_structure(structure_id)

    assert [snapshot["id"] for snapshot in snapshots] == [second_id, first_id]
    assert snapshots[0]["structure_json"] == {"version": 2}
    assert snapshots[1]["structure_json"] == {"version": 1}


def test_get_latest_snapshot_for_structure_returns_snapshot_with_legs(tmp_path: Path):
    db_path = tmp_path / "app.db"
    ensure_structures_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        structure_id = _insert_structure(conn)

    repo = SystemSnapshotsRepository(db_path)

    repo.create_snapshot(
        structure_id=structure_id,
        created_at="2026-06-12T10:00:00Z",
        structure_json={"version": 1},
    )

    latest_id = repo.create_snapshot(
        structure_id=structure_id,
        created_at="2026-06-12T11:00:00Z",
        structure_json={"version": 2},
        legs=[
            {
                "leg_order": 1,
                "position_side": "short",
                "option_type": "put",
                "symbol": "PETRM30",
                "strike": 30.0,
                "expiration_date": "2026-12-18",
                "quantity": -100,
                "premium": 2.1,
                "multiplier": 1,
            }
        ],
    )

    latest = repo.get_latest_snapshot_for_structure(structure_id)

    assert latest is not None
    assert latest["id"] == latest_id
    assert latest["structure_json"] == {"version": 2}
    assert len(latest["legs"]) == 1
    assert latest["legs"][0]["symbol"] == "PETRM30"


def test_get_snapshot_returns_none_when_not_found(tmp_path: Path):
    db_path = tmp_path / "app.db"

    repo = SystemSnapshotsRepository(db_path)

    assert repo.get_snapshot(999999) is None


def test_create_snapshot_requires_structure_id_and_structure_json(tmp_path: Path):
    db_path = tmp_path / "app.db"

    repo = SystemSnapshotsRepository(db_path)

    with pytest.raises(ValueError, match="structure_id"):
        repo.create_snapshot(
            structure_id=0,
            structure_json={"ok": True},
        )

    with pytest.raises(ValueError, match="structure_json"):
        repo.create_snapshot(
            structure_id=1,
            structure_json={},
        )
