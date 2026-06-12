import json
import sqlite3

from repositories.robo_legs_repository import (
    RoboLegsRepoConfig,
    RoboLegsRepository,
)
from repositories.structures_repository import StructuresRepository
from services.legacy_structure_legs_importer import LegacyStructureLegsImporter
from services.legacy_structure_legs_reader import LegacyStructureLegsReader


def _create_integration_schema(db_path):
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

    conn.execute("""
        CREATE TABLE manual_analise_robo_legs (
            id INTEGER,
            aba TEXT,
            timestamp TEXT,
            cv TEXT,
            call_put TEXT,
            strike REAL,
            quant INTEGER,
            ativo TEXT,
            vencimento TEXT,
            preco REAL
        )
    """)

    conn.execute("""
        CREATE TABLE rtd_analise_robo_legs (
            id INTEGER,
            aba TEXT,
            timestamp TEXT,
            cv TEXT,
            call_put TEXT,
            strike REAL,
            quant INTEGER,
            ativo TEXT,
            vencimento TEXT,
            preco REAL
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
            'active', NULL,
            '2026-05-19T10:00:00+00:00',
            '2026-05-19T10:00:00+00:00'
        )
    """, (structure_id,))

    conn.commit()
    conn.close()


def _insert_existing_canonical_leg(db_path, structure_id=123):
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


def _insert_legacy_rtd_leg(db_path):
    conn = sqlite3.connect(db_path)

    conn.execute("""
        INSERT INTO rtd_analise_robo_legs (
            id, aba, timestamp, cv, call_put,
            strike, quant, ativo, vencimento, preco
        )
        VALUES (
            10, 'BOVA_ALIAS', '2026-05-19 10:00:00',
            'C', 'CALL',
            190.0, 1000, 'rtdleg190', '2026-06-20', 0.55
        )
    """)

    conn.commit()
    conn.close()


def _insert_legacy_manual_leg(db_path):
    conn = sqlite3.connect(db_path)

    conn.execute("""
        INSERT INTO manual_analise_robo_legs (
            id, aba, timestamp, cv, call_put,
            strike, quant, ativo, vencimento, preco
        )
        VALUES (
            20, 'BOVA_ALIAS', '2026-05-19 10:00:00',
            'V', 'PUT',
            185.0, 5000, 'manualput185', '2026-06-20', 1.23
        )
    """)

    conn.commit()
    conn.close()


def test_importer_integrates_real_reader_robo_repository_and_structures_repository(
    tmp_path,
):
    db_path = tmp_path / "app.db"

    _create_integration_schema(db_path)
    _insert_structure(db_path)
    _insert_existing_canonical_leg(db_path)

    # Insere RTD e MANUAL no mesmo timestamp.
    # RoboLegsRepository deve preferir MANUAL.
    _insert_legacy_rtd_leg(db_path)
    _insert_legacy_manual_leg(db_path)

    structures_repo = StructuresRepository(db_path=str(db_path))

    robo_legs_repo = RoboLegsRepository(
        RoboLegsRepoConfig(app_db_path=str(db_path))
    )

    reader = LegacyStructureLegsReader(
        robo_legs_repository=robo_legs_repo,
    )

    importer = LegacyStructureLegsImporter(
        reader=reader,
        structures_repository=structures_repo,
    )

    result = importer.import_by_structure_id(
        structure_id=123,
        timestamp="2026-05-19 10:00:00",
    )

    assert result == {
        "structure_id": 123,
        "timestamp": "2026-05-19 10:00:00",
        "legs_count": 1,
        "imported": True,
    }

    structure = structures_repo.get_structure(123)
    assert structure is not None

    legs = structure["legs"]

    assert len(legs) == 1

    imported_leg = legs[0]

    assert imported_leg["position_side"] == "SHORT"
    assert imported_leg["option_type"] == "PUT"
    assert imported_leg["symbol"] == "MANUALPUT185"
    assert imported_leg["strike"] == 185.0
    assert imported_leg["expiration_date"] == "2026-06-20"
    assert imported_leg["quantity"] == 5000
    assert imported_leg["premium"] == 1.23
    assert imported_leg["multiplier"] == 1.0
    assert imported_leg["leg_order"] == 1

    # Garante que a leg antiga foi substituida e que RTD nao foi usado
    # quando havia MANUAL disponivel.
    assert imported_leg["symbol"] != "OLDLEG"
    assert imported_leg["symbol"] != "RTDLEG190"

    assert structures_repo.count_legs(123) == 1

    audit = structures_repo.get_audit_log(123)

    assert len(audit) == 1
    assert audit[0]["action"] == "REPLACE_LEGS"

    after = json.loads(audit[0]["after_json"])

    assert after["legs_count"] == 1
    assert "replaced_at" in after
