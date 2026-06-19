import csv
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

from repositories.pricing_executions_repository import PricingExecutionsRepository
from repositories.system_snapshots_repository import SystemSnapshotsRepository
from services.canonical_pricing_facade import CanonicalPricingFacade
from services.pricing_execution_persistence_service import (
    PricingExecutionPersistenceService,
)


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "scripts" / "import_rtd_links_to_option_quotes.py"

spec = importlib.util.spec_from_file_location(
    "import_rtd_links_to_option_quotes",
    SCRIPT_PATH,
)
importer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = importer
spec.loader.exec_module(importer)


class FakePricingExecutionService:
    def __init__(self):
        self.calls = []

    def execute_payload(self, pricing_payload):
        self.calls.append(pricing_payload)

        return {
            "pricing_payload": pricing_payload,
            "result": {
                "engine": "fake-integrated-engine",
                "status": "ok",
                "metrics": {
                    "number_of_legs": len(pricing_payload["legs"]),
                    "total_quantity": sum(
                        int(leg["quantity"]) for leg in pricing_payload["legs"]
                    ),
                    "spot_price": float(pricing_payload["spot_price"]),
                },
                "valuation": {
                    "theoretical_value": 0.0,
                },
            },
        }


def _create_pricing_executions_schema(db_path: Path) -> None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE pricing_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                structure_id INTEGER,
                underlying_asset TEXT,
                reference_date TEXT,
                execution_status TEXT,
                execution_engine TEXT,
                error_message TEXT,
                duration_ms INTEGER,
                number_of_legs INTEGER,
                total_quantity INTEGER,
                theoretical_value REAL,
                pricing_payload TEXT,
                result TEXT
            )
            """
        )


def _create_rtd_option_quotes_schema(db_path: Path) -> None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE rtd_option_quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                codigo_opcao TEXT NOT NULL,
                ativo_base TEXT,

                call_put TEXT,
                strike REAL,
                vencimento TEXT,

                ultimo_preco REAL,
                ultima_quantidade REAL,

                bid REAL,
                ask REAL,
                volume REAL,

                iv REAL,
                delta REAL,
                gamma REAL,
                theta REAL,
                vega REAL,

                source TEXT NOT NULL DEFAULT 'rtd_links',
                raw_json TEXT,

                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(codigo_opcao)
            )
            """
        )


def _create_controlled_app_db_without_imported_quote(db_path: Path) -> None:
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE structures (
                id INTEGER PRIMARY KEY,
                alias_legacy_aba TEXT,
                underlying_asset TEXT
            )
            """
        )

        conn.execute(
            """
            INSERT INTO structures (
                id,
                alias_legacy_aba,
                underlying_asset
            ) VALUES (?, ?, ?)
            """,
            (123, "ABCD", "ABCD"),
        )

        conn.execute(
            """
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
            )
            """
        )

        conn.execute(
            """
            INSERT INTO rtd_analise_robo_legs (
                timestamp,
                aba,
                ativo,
                cv,
                call_put,
                quant,
                valor_executado,
                bid,
                ask,
                spread,
                spread_pct,
                iv,
                delta,
                gamma,
                theta,
                vega,
                strike,
                vencimento,
                dte,
                pl_realista
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "2026-06-15T10:00:00",
                "ABCD",
                "ABCD11",
                "C",
                "CALL",
                "100",
                "5,55",
                "5,40",
                "5,70",
                "0,30",
                "5,00",
                "0,20",
                "0,50",
                "0,01",
                "-0,02",
                "0,03",
                "10,00",
                "2026-06-15",
                "30",
                "0",
            ),
        )

        conn.execute(
            """
            CREATE TABLE manual_analise_robo_legs (
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
                pl_realista TEXT,
                source TEXT,
                created_at TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE rtd_analise_robo (
                aba TEXT,
                spot TEXT,
                num_pernas TEXT,
                dte_min TEXT,
                pl_realista_total TEXT,
                delta_liq TEXT,
                gamma_liq TEXT,
                theta_liq TEXT,
                vega_liq TEXT,
                spread_medio TEXT,
                spread_pct_medio TEXT,
                alertas_v2 TEXT
            )
            """
        )

        conn.execute(
            """
            INSERT INTO rtd_analise_robo (
                aba,
                spot,
                num_pernas,
                dte_min,
                pl_realista_total,
                delta_liq,
                gamma_liq,
                theta_liq,
                vega_liq,
                spread_medio,
                spread_pct_medio,
                alertas_v2
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ABCD",
                "100,00",
                "1",
                "30",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "[]",
            ),
        )


def _write_rtd_links_csv(csv_path: Path) -> None:
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "codigo_opcao",
                "ativo_base",
                "campo",
                "valor",
                "atualizado_em",
            ]
        )
        writer.writerows(
            [
                ["ABCD11", "ABCD", "call_put", "CALL", "2026-06-15T10:01:00"],
                ["ABCD11", "ABCD", "strike", "10.0", "2026-06-15T10:01:00"],
                ["ABCD11", "ABCD", "vencimento", "2026-06-15", "2026-06-15T10:01:00"],
                ["ABCD11", "ABCD", "ultimo_preco", "9.99", "2026-06-15T10:01:00"],
                ["ABCD11", "ABCD", "bid", "9.80", "2026-06-15T10:01:00"],
                ["ABCD11", "ABCD", "ask", "10.20", "2026-06-15T10:01:00"],
                ["ABCD11", "ABCD", "volume", "1000", "2026-06-15T10:01:00"],
            ]
        )


def _fetch_imported_quote(db_path: Path, codigo_opcao: str) -> sqlite3.Row | None:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    try:
        return conn.execute(
            """
            SELECT
                codigo_opcao,
                ativo_base,
                ultimo_preco,
                bid,
                ask,
                volume,
                source,
                updated_at
            FROM rtd_option_quotes
            WHERE codigo_opcao = ?
            """,
            (codigo_opcao,),
        ).fetchone()
    finally:
        conn.close()


def test_fase_11_rtd_links_import_to_pricing_persistence_and_snapshot_query(tmp_path):
    app_db = tmp_path / "app.db"
    csv_path = tmp_path / "RTD_LINKS.csv"

    _create_controlled_app_db_without_imported_quote(app_db)
    _create_rtd_option_quotes_schema(app_db)
    _create_pricing_executions_schema(app_db)
    _write_rtd_links_csv(csv_path)

    import_stats = importer.import_csv_to_db(
        csv_path=csv_path,
        db_path=app_db,
        dry_run=False,
    )

    assert import_stats.rows_read == 7
    assert import_stats.rows_ignored == 0
    assert import_stats.options_normalized == 1
    assert import_stats.inserted == 1
    assert import_stats.updated == 0

    imported_quote = _fetch_imported_quote(app_db, "ABCD11")

    assert imported_quote is not None
    assert imported_quote["codigo_opcao"] == "ABCD11"
    assert imported_quote["ativo_base"] == "ABCD"
    assert imported_quote["ultimo_preco"] == pytest.approx(9.99)
    assert imported_quote["bid"] == pytest.approx(9.80)
    assert imported_quote["ask"] == pytest.approx(10.20)
    assert imported_quote["volume"] == pytest.approx(1000.0)
    assert imported_quote["source"] == "rtd_links"
    assert imported_quote["updated_at"] == "2026-06-15T10:01:00"

    pricing_repository = PricingExecutionsRepository(db_path=app_db)
    snapshots_repository = SystemSnapshotsRepository(db_path=app_db)

    persistence_service = PricingExecutionPersistenceService(
        pricing_executions_repository=pricing_repository,
        system_snapshots_repository=snapshots_repository,
    )

    fake_engine_service = FakePricingExecutionService()

    facade = CanonicalPricingFacade(
        db_path=app_db,
        pricing_execution_service=fake_engine_service,
        persistence_service=persistence_service,
    )

    response = facade.execute_pricing(
        structure_id=123,
        reference_date="2026-06-15",
    )

    assert response["status"] == "ok"

    assert len(fake_engine_service.calls) == 1
    pricing_payload = fake_engine_service.calls[0]

    leg = pricing_payload["legs"][0]

    # O preço original do snapshot operacional era 5.55.
    # O preço efetivo integrado deve vir do CSV importado para
    # rtd_option_quotes.ultimo_preco = 9.99.
    assert pricing_payload["structure_id"] == 123
    assert pricing_payload["underlying_asset"] == "ABCD"
    assert pricing_payload["reference_date"] == "2026-06-15"
    assert pricing_payload["spot_price"] == 100.0

    assert leg["symbol"] == "ABCD11"
    assert leg["asset"] == "ABCD11"
    assert leg["price"] == pytest.approx(9.99)
    assert leg["premium"] == pytest.approx(9.99)
    assert leg["price_source"] == "rtd_option_quotes"
    assert leg["rtd_price_field"] == "ultimo_preco"
    assert leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert leg["rtd_quote_ativo_base"] == "ABCD"
    assert leg["rtd_price_source"] == "rtd_links"
    assert leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"

    persisted = response["persisted"]
    record = persisted["record"]

    loaded_execution = pricing_repository.get_execution(record["id"])

    assert loaded_execution is not None
    assert loaded_execution["execution_status"] == "ok"
    assert loaded_execution["execution_engine"] == "fake-integrated-engine"

    persisted_leg = loaded_execution["pricing_payload"]["legs"][0]

    assert persisted_leg["price"] == pytest.approx(9.99)
    assert persisted_leg["premium"] == pytest.approx(9.99)
    assert persisted_leg["price_source"] == "rtd_option_quotes"
    assert persisted_leg["rtd_price_field"] == "ultimo_preco"
    assert persisted_leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert persisted_leg["rtd_quote_ativo_base"] == "ABCD"
    assert persisted_leg["rtd_price_source"] == "rtd_links"
    assert persisted_leg["rtd_price_updated_at"] == "2026-06-15T10:01:00"

    snapshot_id = persisted["snapshot_id"]
    loaded_snapshot = snapshots_repository.get_snapshot(snapshot_id)

    assert loaded_snapshot is not None
    assert loaded_snapshot["structure_id"] == 123
    assert loaded_snapshot["pricing_execution_id"] == record["id"]
    assert loaded_snapshot["underlying_asset"] == "ABCD"
    assert loaded_snapshot["reference_date"] == "2026-06-15"
    assert loaded_snapshot["snapshot_source"] == "system_pricing_execution"

    snapshot_state_leg = loaded_snapshot["operation_state_json"]["pricing_payload"]["legs"][0]

    assert snapshot_state_leg["price"] == pytest.approx(9.99)
    assert snapshot_state_leg["premium"] == pytest.approx(9.99)
    assert snapshot_state_leg["price_source"] == "rtd_option_quotes"
    assert snapshot_state_leg["rtd_price_field"] == "ultimo_preco"
    assert snapshot_state_leg["rtd_quote_codigo_opcao"] == "ABCD11"
    assert snapshot_state_leg["rtd_quote_ativo_base"] == "ABCD"
    assert snapshot_state_leg["rtd_price_source"] == "rtd_links"

    snapshot_leg = loaded_snapshot["legs"][0]

    assert snapshot_leg["symbol"] == "ABCD11"
    assert snapshot_leg["premium"] == pytest.approx(9.99)
    assert snapshot_leg["raw_json"]["price"] == pytest.approx(9.99)
    assert snapshot_leg["raw_json"]["price_source"] == "rtd_option_quotes"
    assert snapshot_leg["raw_json"]["rtd_price_field"] == "ultimo_preco"
    assert snapshot_leg["raw_json"]["rtd_quote_codigo_opcao"] == "ABCD11"
    assert snapshot_leg["raw_json"]["rtd_quote_ativo_base"] == "ABCD"
    assert snapshot_leg["raw_json"]["rtd_price_source"] == "rtd_links"
