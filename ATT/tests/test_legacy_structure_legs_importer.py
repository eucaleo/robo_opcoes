import json
import sqlite3

import pytest

from repositories.structures_repository import StructuresRepository
from services.legacy_structure_legs_importer import LegacyStructureLegsImporter


def _create_schema(db_path):
    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE structures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            underlying_asset TEXT NOT NULL,
            alias_legacy_aba TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            notes TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE structure_legs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            structure_id INTEGER NOT NULL,
            position_side TEXT NOT NULL,
            option_type TEXT NOT NULL,
            symbol TEXT,
            strike REAL NOT NULL,
            expiration_date TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            premium REAL,
            multiplier REAL NOT NULL DEFAULT 1,
            leg_order INTEGER NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (structure_id) REFERENCES structures(id)
        )
    """)

    repo = StructuresRepository(db_path=str(db_path))
    repo.ensure_audit_schema(conn)

    conn.commit()
    conn.close()


def _insert_structure(db_path, structure_id=123):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO structures (
            id, name, underlying_asset, alias_legacy_aba,
            status, notes, created_at, updated_at
        )
        VALUES (
            ?, 'BOVA teste', 'BOVA11', 'BOVA_ALIAS',
            'active', NULL, '2026-05-19T10:00:00+00:00',
            '2026-05-19T10:00:00+00:00'
        )
    """, (structure_id,))
    conn.commit()
    conn.close()


def _insert_existing_leg(db_path, structure_id=123):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO structure_legs (
            structure_id, position_side, option_type, symbol,
            strike, expiration_date, quantity, premium,
            multiplier, leg_order, notes, created_at, updated_at
        )
        VALUES (
            ?, 'LONG', 'CALL', 'OLDLEG',
            100.0, '2026-06-20', 1, 0.10,
            1.0, 1, NULL,
            '2026-05-19T10:00:00+00:00',
            '2026-05-19T10:00:00+00:00'
        )
    """, (structure_id,))
    conn.commit()
    conn.close()


class FakeLegacyStructureLegsReader:
    def __init__(self, legs):
        self.legs = legs
        self.calls = []

    def read_by_structure_id(self, structure_id, timestamp):
        self.calls.append(
            {
                "structure_id": structure_id,
                "timestamp": timestamp,
            }
        )
        return self.legs


def test_import_by_structure_id_replaces_legs_and_writes_audit_log(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)
    _insert_structure(db_path)
    _insert_existing_leg(db_path)

    repo = StructuresRepository(db_path=str(db_path))

    reader = FakeLegacyStructureLegsReader([
        {
            "position_side": "LONG",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-06-20",
            "quantity": 5000,
            "premium": 1.23,
            "multiplier": 1.0,
            "leg_order": 1,
        },
        {
            "position_side": "SHORT",
            "option_type": "CALL",
            "symbol": "BOVAE200",
            "strike": 200.0,
            "expiration_date": "2026-06-20",
            "quantity": 5000,
            "premium": 0.78,
            "multiplier": 1.0,
            "leg_order": 2,
        },
    ])

    importer = LegacyStructureLegsImporter(
        reader=reader,
        structures_repository=repo,
    )

    result = importer.import_by_structure_id(
        structure_id=123,
        timestamp="2026-05-19 10:00:00",
    )

    assert result == {
        "structure_id": 123,
        "timestamp": "2026-05-19 10:00:00",
        "legs_count": 2,
        "imported": True,
    }

    assert reader.calls == [
        {
            "structure_id": 123,
            "timestamp": "2026-05-19 10:00:00",
        }
    ]

    structure = repo.get_structure(123)
    assert structure is not None

    legs = structure["legs"]
    assert [leg["symbol"] for leg in legs] == ["BOVAE195", "BOVAE200"]
    assert [leg["leg_order"] for leg in legs] == [1, 2]
    assert repo.count_legs(123) == 2

    audit = repo.get_audit_log(123)
    assert audit[0]["action"] == "REPLACE_LEGS"

    after = json.loads(audit[0]["after_json"])
    assert after["legs_count"] == 2
    assert "replaced_at" in after


def test_import_by_structure_id_raises_when_reader_returns_no_legs(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)
    _insert_structure(db_path)
    _insert_existing_leg(db_path)

    repo = StructuresRepository(db_path=str(db_path))
    reader = FakeLegacyStructureLegsReader([])

    importer = LegacyStructureLegsImporter(
        reader=reader,
        structures_repository=repo,
    )

    with pytest.raises(
        ValueError,
        match=r"structure_id=123 sem legs legadas para importar",
    ):
        importer.import_by_structure_id(
            structure_id=123,
            timestamp="2026-05-19 10:00:00",
        )

    assert repo.count_legs(123) == 1
    assert repo.get_structure(123)["legs"][0]["symbol"] == "OLDLEG"
    assert repo.get_audit_log(123) == []


def test_import_by_structure_id_raises_when_structure_does_not_exist(tmp_path):
    db_path = tmp_path / "app.db"
    _create_schema(db_path)

    repo = StructuresRepository(db_path=str(db_path))
    reader = FakeLegacyStructureLegsReader([
        {
            "position_side": "LONG",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-06-20",
            "quantity": 5000,
            "premium": 1.23,
            "multiplier": 1.0,
            "leg_order": 1,
        }
    ])

    importer = LegacyStructureLegsImporter(
        reader=reader,
        structures_repository=repo,
    )

    with pytest.raises(ValueError, match=r"structure not found: 999"):
        importer.import_by_structure_id(
            structure_id=999,
            timestamp="2026-05-19 10:00:00",
        )

    assert reader.calls == []
