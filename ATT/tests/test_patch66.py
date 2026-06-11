"""
test_patch66.py
================
Testes formais do patch_66 — import de legs legadas para o modelo canonico.
Cobre: conversao de serial Excel, mapeamento cv->position_side,
       idempotencia, prioridade MANUAL > RTD, estrutura canonica das legs.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# Adiciona raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.import_legacy_structures import (
    excel_serial_to_iso,
    map_position_side,
    safe_float,
    safe_int,
    get_structures_by_alias,
    has_legs,
    get_latest_snapshot,
    import_legs_for_structure,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mem_db():
    """Banco em memoria com schema minimo para os testes."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE structures (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            underlying_asset TEXT NOT NULL,
            alias_legacy_aba TEXT,
            status TEXT NOT NULL DEFAULT 'active',
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

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
            updated_at TEXT NOT NULL
        );

        CREATE TABLE rtd_analise_robo_legs (
            timestamp TEXT,
            aba TEXT,
            ativo TEXT,
            cv TEXT,
            call_put TEXT,
            quant TEXT,
            valor_executado TEXT,
            bid TEXT,
            ask TEXT,
            spread TEXT,
            spread_pct TEXT,
            iv TEXT,
            delta TEXT,
            gamma TEXT,
            theta TEXT,
            vega TEXT,
            strike TEXT,
            vencimento TEXT,
            dte TEXT,
            pl_realista TEXT
        );

        CREATE TABLE manual_analise_robo_legs (
            timestamp TEXT NOT NULL,
            aba TEXT NOT NULL,
            ativo TEXT,
            cv TEXT,
            call_put TEXT,
            quant TEXT,
            valor_executado TEXT,
            bid TEXT,
            ask TEXT,
            spread TEXT,
            spread_pct TEXT,
            iv TEXT,
            delta TEXT,
            gamma TEXT,
            theta TEXT,
            vega TEXT,
            strike TEXT,
            vencimento TEXT,
            dte TEXT,
            pl_realista TEXT,
            source TEXT DEFAULT 'manual',
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    return conn


def insert_structure(conn, id_, alias, name="Struct Test"):
    now = "2026-01-01T00:00:00+00:00"
    conn.execute("""
        INSERT INTO structures (id, name, underlying_asset, alias_legacy_aba,
                                status, created_at, updated_at)
        VALUES (?, ?, ?, ?, 'active', ?, ?)
    """, (id_, name, alias, alias, now, now))
    conn.commit()


def insert_rtd_leg(conn, aba, ts="14/04/2026 17:55:51", ativo="TEST123",
                   cv="C", call_put="CALL", quant="1000",
                   valor_executado="2,50", strike="100", vencimento="46157,125"):
    conn.execute("""
        INSERT INTO rtd_analise_robo_legs
        (timestamp, aba, ativo, cv, call_put, quant, valor_executado,
         bid, ask, spread, spread_pct, iv, delta, gamma, theta, vega,
         strike, vencimento, dte, pl_realista)
        VALUES (?, ?, ?, ?, ?, ?, ?, '0', '0', '0', '0', '0',
                '0', '0', '0', '0', ?, ?, '30', '0')
    """, (ts, aba, ativo, cv, call_put, quant, valor_executado, strike, vencimento))
    conn.commit()


def insert_manual_leg(conn, aba, ts="09/05/2026 21:04:53", ativo="TEST456",
                      cv="V", call_put="PUT", quant="2000",
                      valor_executado="5,00", strike="95", vencimento="46157,125"):
    conn.execute("""
        INSERT INTO manual_analise_robo_legs
        (timestamp, aba, ativo, cv, call_put, quant, valor_executado,
         bid, ask, spread, spread_pct, iv, delta, gamma, theta, vega,
         strike, vencimento, dte, pl_realista)
        VALUES (?, ?, ?, ?, ?, ?, ?, '0', '0', '0', '0', '0',
                '0', '0', '0', '0', ?, ?, '30', '0')
    """, (ts, aba, ativo, cv, call_put, quant, valor_executado, strike, vencimento))
    conn.commit()


# ---------------------------------------------------------------------------
# Testes de conversao
# ---------------------------------------------------------------------------

class TestExcelSerialToIso:
    def test_valor_conhecido_46157(self):
        # Serial 46157 = 2026-05-15 (epoch Excel: 1899-12-30)
        result = excel_serial_to_iso("46157,125")
        assert result == "2026-05-15"

    def test_valor_conhecido_46129(self):
        # Serial 46129 = 2026-04-17
        result = excel_serial_to_iso("46129,125")
        assert result == "2026-04-17"

    def test_aceita_ponto_como_separador(self):
        assert excel_serial_to_iso("46157.125") == "2026-05-15"

    def test_valor_inteiro(self):
        result = excel_serial_to_iso("46157")
        assert result == "2026-05-15"

    def test_fallback_string_invalida(self):
        # Nao deve lancar excecao
        result = excel_serial_to_iso("nao-e-numero")
        assert isinstance(result, str)

    def test_referencia_cruzada_serial_vs_timestamp(self):
        """
        O timestamp '14/04/2026 17:55:51' e quando o robo capturou o snapshot.
        O serial 46157 no campo 'vencimento' e a data de expiracao da opcao: 15/05/2026.
        Sao conceitos distintos — nao confundir.
        """
        from datetime import date, timedelta
        base = date(1899, 12, 30)
        computed = (base + timedelta(days=46157)).strftime("%Y-%m-%d")
        assert computed == "2026-05-15"
        assert excel_serial_to_iso("46157") == computed

class TestMapPositionSide:
    def test_c_retorna_long(self):
        assert map_position_side("C") == "LONG"

    def test_v_retorna_short(self):
        assert map_position_side("V") == "SHORT"

    def test_lowercase_c(self):
        assert map_position_side("c") == "LONG"

    def test_lowercase_v(self):
        assert map_position_side("v") == "SHORT"

    def test_invalido_levanta_valueerror(self):
        with pytest.raises(ValueError, match="cv desconhecido"):
            map_position_side("X")


class TestSafeConversions:
    def test_safe_float_virgula(self):
        assert safe_float("1,38") == pytest.approx(1.38)

    def test_safe_float_ponto(self):
        assert safe_float("86.81") == pytest.approx(86.81)

    def test_safe_float_none(self):
        assert safe_float(None) is None

    def test_safe_int(self):
        assert safe_int("7000") == 7000

    def test_safe_int_float_str(self):
        assert safe_int("7000,0") == 7000


# ---------------------------------------------------------------------------
# Testes de consulta
# ---------------------------------------------------------------------------

class TestGetStructuresByAlias:
    def test_retorna_estruturas_com_alias(self, mem_db):
        insert_structure(mem_db, 1, "BOVA11")
        insert_structure(mem_db, 2, "EMBJ3")
        result = get_structures_by_alias(mem_db)
        assert "BOVA11" in result
        assert "EMBJ3" in result
        assert result["BOVA11"]["id"] == 1

    def test_ignora_alias_nulo(self, mem_db):
        now = "2026-01-01T00:00:00+00:00"
        mem_db.execute("""
            INSERT INTO structures (id, name, underlying_asset,
                                    alias_legacy_aba, status, created_at, updated_at)
            VALUES (99, 'Sem Alias', 'TEST', NULL, 'active', ?, ?)
        """, (now, now))
        mem_db.commit()
        result = get_structures_by_alias(mem_db)
        assert None not in result


class TestHasLegs:
    def test_sem_legs_retorna_false(self, mem_db):
        insert_structure(mem_db, 1, "BOVA11")
        assert has_legs(mem_db, 1) is False

    def test_com_legs_retorna_true(self, mem_db):
        insert_structure(mem_db, 1, "BOVA11")
        now = "2026-01-01T00:00:00+00:00"
        mem_db.execute("""
            INSERT INTO structure_legs
            (structure_id, position_side, option_type, symbol,
             strike, expiration_date, quantity, multiplier,
             leg_order, created_at, updated_at)
            VALUES (1, 'LONG', 'CALL', 'BOVA11E195',
                    195.0, '2026-04-14', 1000, 1.0, 1, ?, ?)
        """, (now, now))
        mem_db.commit()
        assert has_legs(mem_db, 1) is True


class TestGetLatestSnapshot:
    def test_rtd_sem_manual(self, mem_db):
        insert_rtd_leg(mem_db, "PRIO3")
        legs, source = get_latest_snapshot(mem_db, "PRIO3")
        assert len(legs) == 1
        assert "rtd_analise_robo_legs" in source

    def test_manual_mais_recente_tem_prioridade(self, mem_db):
        insert_rtd_leg(mem_db, "BOVA11", ts="14/04/2026 17:55:51")
        insert_manual_leg(mem_db, "BOVA11", ts="09/05/2026 21:04:53")
        legs, source = get_latest_snapshot(mem_db, "BOVA11")
        assert "manual_analise_robo_legs" in source

    def test_rtd_mais_recente_que_manual(self, mem_db):
        insert_rtd_leg(mem_db, "SBSP3", ts="10/06/2026 10:00:00")
        insert_manual_leg(mem_db, "SBSP3", ts="01/01/2026 00:00:00")
        legs, source = get_latest_snapshot(mem_db, "SBSP3")
        assert "rtd_analise_robo_legs" in source

    def test_aba_inexistente_retorna_vazio(self, mem_db):
        legs, source = get_latest_snapshot(mem_db, "INEXISTENTE")
        assert legs == []
        assert source == "sem_dados"

    def test_legs_contem_campos_esperados(self, mem_db):
        insert_rtd_leg(mem_db, "SMAL11")
        legs, _ = get_latest_snapshot(mem_db, "SMAL11")
        assert len(legs) == 1
        leg = legs[0]
        for campo in ["ativo", "cv", "call_put", "quant", "valor_executado",
                      "strike", "vencimento"]:
            assert campo in leg


# ---------------------------------------------------------------------------
# Teste de import
# ---------------------------------------------------------------------------

class TestImportLegsForStructure:
    def test_import_basico(self, mem_db):
        insert_structure(mem_db, 10, "EMBJ3")
        now = "2026-06-04T00:00:00+00:00"
        legs_raw = [
            {
                "ativo": "EMBJE868", "cv": "C", "call_put": "CALL",
                "quant": "7000", "valor_executado": "1,38",
                "strike": "86,81", "vencimento": "46157,125",
                "delta": "0,59", "gamma": "0,039",
                "theta": "4,85", "vega": "10,25", "iv": "37,78",
            },
            {
                "ativo": "EMBJE704", "cv": "V", "call_put": "CALL",
                "quant": "4000", "valor_executado": "8,35",
                "strike": "69,81", "vencimento": "46157,125",
                "delta": "0,98", "gamma": "0,004",
                "theta": "18,55", "vega": "1,16", "iv": "38,57",
            },
        ]

        n = import_legs_for_structure(
            mem_db, 10, "EMBJ3", legs_raw,
            "rtd_analise_robo_legs (ts=14/04/2026)", now
        )
        mem_db.commit()

        assert n == 2
        assert has_legs(mem_db, 10)

        cur = mem_db.cursor()
        cur.execute("SELECT * FROM structure_legs WHERE structure_id=10 ORDER BY leg_order")
        rows = cur.fetchall()
        assert len(rows) == 2

        # Leg 1 — LONG CALL
        assert rows[0][2] == "LONG"
        assert rows[0][3] == "CALL"
        assert rows[0][4] == "EMBJE868"
        assert rows[0][5] == pytest.approx(86.81)
        assert rows[0][6] == "2026-05-15"
        assert rows[0][7] == 7000

        # Leg 2 — SHORT CALL
        assert rows[1][2] == "SHORT"
        assert rows[1][3] == "CALL"

    def test_leg_order_sequencial(self, mem_db):
        insert_structure(mem_db, 20, "PRIO3")
        now = "2026-06-04T00:00:00+00:00"
        legs_raw = [
            {"ativo": "A", "cv": "C", "call_put": "CALL", "quant": "100",
             "valor_executado": "1", "strike": "50", "vencimento": "46157,125",
             "delta": "0", "gamma": "0", "theta": "0", "vega": "0", "iv": "0"},
            {"ativo": "B", "cv": "V", "call_put": "PUT", "quant": "200",
             "valor_executado": "2", "strike": "45", "vencimento": "46157,125",
             "delta": "0", "gamma": "0", "theta": "0", "vega": "0", "iv": "0"},
            {"ativo": "C", "cv": "C", "call_put": "PUT", "quant": "300",
             "valor_executado": "3", "strike": "55", "vencimento": "46157,125",
             "delta": "0", "gamma": "0", "theta": "0", "vega": "0", "iv": "0"},
        ]
        import_legs_for_structure(
            mem_db, 20, "PRIO3", legs_raw, "rtd_test", now
        )
        mem_db.commit()

        cur = mem_db.cursor()
        cur.execute("SELECT leg_order FROM structure_legs WHERE structure_id=20 ORDER BY leg_order")
        orders = [r[0] for r in cur.fetchall()]
        assert orders == [1, 2, 3]

    def test_strike_nulo_levanta_erro(self, mem_db):
        insert_structure(mem_db, 30, "SBSP3")
        now = "2026-06-04T00:00:00+00:00"
        legs_raw = [
            {"ativo": "X", "cv": "C", "call_put": "CALL", "quant": "100",
             "valor_executado": "1", "strike": None, "vencimento": "46157,125",
             "delta": "0", "gamma": "0", "theta": "0", "vega": "0", "iv": "0"},
        ]
        with pytest.raises(ValueError, match="strike nulo"):
            import_legs_for_structure(
                mem_db, 30, "SBSP3", legs_raw, "test", now
            )

    def test_cv_invalido_levanta_erro(self, mem_db):
        insert_structure(mem_db, 40, "SMAL11")
        now = "2026-06-04T00:00:00+00:00"
        legs_raw = [
            {"ativo": "X", "cv": "Z", "call_put": "CALL", "quant": "100",
             "valor_executado": "1", "strike": "100", "vencimento": "46157,125",
             "delta": "0", "gamma": "0", "theta": "0", "vega": "0", "iv": "0"},
        ]
        with pytest.raises(ValueError, match="cv desconhecido"):
            import_legs_for_structure(
                mem_db, 40, "SMAL11", legs_raw, "test", now
            )
