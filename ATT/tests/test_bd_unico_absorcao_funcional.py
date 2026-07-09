from __future__ import annotations

import inspect
import sqlite3
import tempfile
import uuid
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_DB = PROJECT_ROOT / "dados" / "app.db"


REQUIRED_TABLES = {
    "rtd_option_quotes",
    "rtd_underlying_quotes",
    "payoff_curve_points",
    "structure_decisions",
    "pricing_executions",
    "structures",
    "structure_legs",
    "structure_snapshots",
    "structure_leg_snapshots",
}


REQUIRED_COLUMNS = {
    "rtd_option_quotes": {
        "codigo_opcao",
        "ativo_base",
        "bid",
        "ask",
        "updated_at",
        "created_at",
        "vwap",
    },
    "rtd_underlying_quotes": {
        "ativo",
        "ultimo_preco",
        "bid",
        "ask",
        "close_price",
        "updated_at",
        "created_at",
        "vwap",
    },
    "payoff_curve_points": {
        "timestamp",
        "aba",
        "structure_id",
        "spot_ref",
        "point_spot",
        "point_pl",
        "meta_json",
        "created_at",
    },
    "structure_decisions": {
        "structure_id",
        "decision",
        "timestamp",
        "aba",
        "level",
        "pl_atual",
        "pl_max",
        "pl_pct_of_max",
        "dte_min",
        "why_json",
        "spot_ref",
        "meta_json",
        "why",
    },
    "pricing_executions": {
        "created_at",
        "structure_id",
        "underlying_asset",
        "reference_date",
        "execution_status",
        "execution_engine",
        "pricing_payload",
        "result",
    },
    "structure_snapshots": {
        "created_at",
        "structure_id",
        "pricing_execution_id",
        "underlying_asset",
        "reference_date",
        "structure_json",
        "market_json",
        "metrics_json",
        "payoff_json",
        "decision_json",
    },
    "structure_leg_snapshots": {
        "snapshot_id",
        "structure_id",
        "leg_id",
        "position_side",
        "option_type",
        "symbol",
        "strike",
        "expiration_date",
        "quantity",
        "premium",
        "metrics_json",
        "market_json",
        "raw_json",
    },
}


REQUIRED_INDEXES = {
    "idx_rtd_option_quotes_codigo_opcao",
    "idx_rtd_underlying_quotes_ativo",
    "ix_payoff_structure_id",
    "ux_payoff_snapshot",
    "ux_decision_snapshot",
    "idx_structure_decisions_sid_ts",
    "idx_pricing_executions_structure_id",
    "idx_structure_snapshots_structure_id",
    "idx_structure_leg_snapshots_structure_id",
}


def _table_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        """
    ).fetchall()
    return {str(row[0]) for row in rows}


def _index_names(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'index'
        """
    ).fetchall()
    return {str(row[0]) for row in rows}


def _columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {str(row[1]) for row in rows}


def test_app_db_contem_tabelas_funcionais_absorvidas() -> None:
    assert APP_DB.exists(), "dados/app.db deve existir como banco canonico unico"

    with sqlite3.connect(APP_DB) as conn:
        existing_tables = _table_names(conn)

    missing_tables = REQUIRED_TABLES - existing_tables
    assert not missing_tables, (
        "dados/app.db nao contem todas as tabelas funcionais absorvidas: "
        f"{sorted(missing_tables)}"
    )


def test_app_db_contem_colunas_e_indices_funcionais_absorvidos() -> None:
    assert APP_DB.exists(), "dados/app.db deve existir como banco canonico unico"

    with sqlite3.connect(APP_DB) as conn:
        for table_name, required_columns in REQUIRED_COLUMNS.items():
            existing_columns = _columns(conn, table_name)
            missing_columns = required_columns - existing_columns
            assert not missing_columns, (
                f"Tabela {table_name} sem colunas funcionais esperadas: "
                f"{sorted(missing_columns)}"
            )

        existing_indexes = _index_names(conn)

    missing_indexes = REQUIRED_INDEXES - existing_indexes
    assert not missing_indexes, (
        "dados/app.db nao contem todos os indices funcionais esperados: "
        f"{sorted(missing_indexes)}"
    )


def test_repositorio_consolidado_grava_payoff_e_decisao_na_conexao_fornecida() -> None:
    from db import derived_repo as repo

    run_id = uuid.uuid4().hex
    timestamp = f"fase5g_{run_id}"
    aba = "FASE5G"
    structure_id = 5001

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_root = Path(tmpdir)
        canonical_dir = tmp_root / "dados"
        canonical_dir.mkdir(parents=True, exist_ok=True)
        canonical_db = canonical_dir / "app.db"

        with sqlite3.connect(canonical_db) as conn:
            repo._apply_schema(conn)

            points = [
                (90.0, -10.0),
                (100.0, 0.0),
                (110.0, 10.0),
            ]
            points_meta = [
                {"source": "fase5g"},
                {"source": "fase5g"},
                {"source": "fase5g"},
            ]

            payoff_signature = inspect.signature(repo.write_payoff_snapshot_atomic)
            payoff_kwargs = {
                "conn": conn,
                "timestamp": timestamp,
                "aba": aba,
                "points": points,
            }

            if "points_meta" in payoff_signature.parameters:
                payoff_kwargs["points_meta"] = points_meta
            if "structure_id" in payoff_signature.parameters:
                payoff_kwargs["structure_id"] = structure_id

            repo.write_payoff_snapshot_atomic(**payoff_kwargs)

            decision_dict = {
                "structure_id": structure_id,
                "decision": "hold",
                "label": "fase5g",
                "level": 1,
                "pl_atual": 0.0,
                "pl_max": 10.0,
                "pl_pct_of_max": 0.0,
                "dte_min": 30,
                "why_json": "{}",
                "spot_ref": 100.0,
                "meta_json": "{}",
                "why": "contrato de absorcao funcional",
            }

            decision_signature = inspect.signature(repo.write_decision_snapshot_atomic)
            decision_kwargs = {
                "conn": conn,
                "timestamp": timestamp,
                "aba": aba,
            }

            if "decision_dict" in decision_signature.parameters:
                decision_kwargs["decision_dict"] = decision_dict
            elif "decision" in decision_signature.parameters:
                decision_kwargs["decision"] = decision_dict
            else:
                raise AssertionError(
                    "write_decision_snapshot_atomic nao expoe parametro de decisao esperado"
                )

            repo.write_decision_snapshot_atomic(**decision_kwargs)
            conn.commit()

            payoff_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM payoff_curve_points
                WHERE timestamp = ? AND aba = ?
                """,
                (timestamp, aba),
            ).fetchone()[0]

            decision_count = conn.execute(
                """
                SELECT COUNT(*)
                FROM structure_decisions
                WHERE timestamp = ? AND aba = ?
                """,
                (timestamp, aba),
            ).fetchone()[0]

        db_files = sorted(path.relative_to(tmp_root).as_posix() for path in tmp_root.rglob("*.db"))

    assert payoff_count == 3
    assert decision_count == 1
    assert db_files == ["dados/app.db"]
