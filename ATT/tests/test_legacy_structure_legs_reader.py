from datetime import datetime
from types import SimpleNamespace

import pytest

from services.legacy_structure_legs_reader import LegacyStructureLegsReader


class FakeRoboLegsRepository:
    def __init__(self, legs):
        self.legs = legs
        self.calls = []

    def get_legs_by_structure_id(self, structure_id, timestamp):
        self.calls.append(
            {
                "structure_id": structure_id,
                "timestamp": timestamp,
            }
        )
        return self.legs


def test_read_by_structure_id_maps_legacy_legs_to_structure_legs_payload():
    legacy_legs = [
        SimpleNamespace(
            cv="C",
            call_put="CALL",
            ativo=" bovae195 ",
            strike=195.0,
            vencimento=datetime(2026, 5, 15),
            quant=5000,
            preco=1.23,
        ),
        SimpleNamespace(
            cv="V",
            call_put="PUT",
            ativo=" bovao185 ",
            strike=185.0,
            vencimento=datetime(2026, 5, 15),
            quant=1000,
            preco=0.98,
        ),
    ]

    repo = FakeRoboLegsRepository(legacy_legs)
    reader = LegacyStructureLegsReader(robo_legs_repository=repo)

    result = reader.read_by_structure_id(
        structure_id=123,
        timestamp="2026-05-19 10:00:00",
    )

    assert repo.calls == [
        {
            "structure_id": 123,
            "timestamp": "2026-05-19 10:00:00",
        }
    ]

    assert result == [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-05-15",
            "quantity": 5000,
            "premium": 1.23,
            "multiplier": 1.0,
            "leg_order": 1,
        },
        {
            "position_side": "VENDIDO",
            "option_type": "PUT",
            "symbol": "BOVAO185",
            "strike": 185.0,
            "expiration_date": "2026-05-15",
            "quantity": 1000,
            "premium": 0.98,
            "multiplier": 1.0,
            "leg_order": 2,
        },
    ]


def test_read_by_structure_id_propagates_mapper_errors():
    legacy_legs = [
        SimpleNamespace(
            cv="X",
            call_put="CALL",
            ativo="BOVAE195",
            strike=195.0,
            vencimento=datetime(2026, 5, 15),
            quant=1,
            preco=1.0,
        ),
    ]

    reader = LegacyStructureLegsReader(
        robo_legs_repository=FakeRoboLegsRepository(legacy_legs)
    )

    with pytest.raises(ValueError, match=r"invalid cv: X"):
        reader.read_by_structure_id(
            structure_id=123,
            timestamp="2026-05-19 10:00:00",
        )


def _prepare_integration_db(db_path):
    import sqlite3

    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE structures (
            id INTEGER PRIMARY KEY,
            name TEXT,
            underlying_asset TEXT,
            alias_legacy_aba TEXT,
            status TEXT
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

    conn.commit()
    conn.close()


def test_read_by_structure_id_integrates_structure_alias_with_rtd_legs(tmp_path):
    from repositories.robo_legs_repository import (
        RoboLegsRepoConfig,
        RoboLegsRepository,
    )

    db_path = tmp_path / "app.db"
    _prepare_integration_db(db_path)

    import sqlite3

    conn = sqlite3.connect(db_path)

    conn.execute("""
        INSERT INTO structures
        (id, name, underlying_asset, alias_legacy_aba, status)
        VALUES (123, 'BOVA teste', 'BOVA11', 'BOVA_ALIAS', 'active')
    """)

    conn.execute("""
        INSERT INTO rtd_analise_robo_legs
        (id, aba, timestamp, cv, call_put, strike, quant, ativo, vencimento, preco)
        VALUES (
            10,
            'BOVA_ALIAS',
            '2026-05-19 10:00:00',
            'C',
            'CALL',
            195.0,
            5000,
            'bovae195',
            '2026-06-20',
            1.23
        )
    """)

    conn.commit()
    conn.close()

    repo = RoboLegsRepository(
        RoboLegsRepoConfig(app_db_path=str(db_path))
    )
    reader = LegacyStructureLegsReader(robo_legs_repository=repo)

    result = reader.read_by_structure_id(
        structure_id=123,
        timestamp="2026-05-19 10:00:00",
    )

    assert result == [
        {
            "position_side": "COMPRADO",
            "option_type": "CALL",
            "symbol": "BOVAE195",
            "strike": 195.0,
            "expiration_date": "2026-06-20",
            "quantity": 5000,
            "premium": 1.23,
            "multiplier": 1.0,
            "leg_order": 1,
        }
    ]


def test_read_by_structure_id_raises_when_structure_has_no_alias(tmp_path):
    from repositories.robo_legs_repository import (
        RoboLegsRepoConfig,
        RoboLegsRepository,
    )

    db_path = tmp_path / "app.db"
    _prepare_integration_db(db_path)

    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.execute("""
        INSERT INTO structures
        (id, name, underlying_asset, alias_legacy_aba, status)
        VALUES (123, 'BOVA teste', 'BOVA11', NULL, 'active')
    """)
    conn.commit()
    conn.close()

    repo = RoboLegsRepository(
        RoboLegsRepoConfig(app_db_path=str(db_path))
    )
    reader = LegacyStructureLegsReader(robo_legs_repository=repo)

    with pytest.raises(
        ValueError,
        match=r"structure_id=123 sem alias_legacy_aba em structures",
    ):
        reader.read_by_structure_id(
            structure_id=123,
            timestamp="2026-05-19 10:00:00",
        )
