from __future__ import annotations

import argparse
import inspect
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from services import rtd_option_quotes_intraday_history_service as history_service


CAPTURE_METHOD_CANDIDATES = (
    "capture_once",
    "capture_current_snapshot",
    "capture_snapshot",
    "capture_from_snapshot",
    "capture_intraday_history",
    "capture_intraday_history_once",
    "capture_from_rtd_option_quotes",
    "run_once",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executa uma captura manual unica do historico intraday RTD."
    )
    parser.add_argument(
        "--db",
        required=True,
        help="Caminho do banco SQLite canonico ou de validacao.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida leitura do snapshot sem gravar historico.",
    )
    return parser


def _connect_readonly(db_path: Path) -> sqlite3.Connection:
    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
          FROM sqlite_master
         WHERE type = 'table'
           AND name = ?
         LIMIT 1
        """,
        (table_name,),
    ).fetchone()
    return row is not None


def _count_snapshot_rows(db_path: Path) -> int:
    with _connect_readonly(db_path) as conn:
        if not _table_exists(conn, "rtd_option_quotes"):
            raise RuntimeError("Tabela rtd_option_quotes nao encontrada.")

        row = conn.execute(
            "SELECT COUNT(*) AS total FROM rtd_option_quotes"
        ).fetchone()

        return int(row["total"])


def _find_service_class() -> type[Any]:
    explicit = getattr(
        history_service,
        "RtdOptionQuotesIntradayHistoryService",
        None,
    )

    if isinstance(explicit, type):
        return explicit

    candidates: list[type[Any]] = []

    for name in dir(history_service):
        obj = getattr(history_service, name)

        if not isinstance(obj, type):
            continue

        lower_name = name.lower()

        if "intraday" in lower_name and "service" in lower_name:
            candidates.append(obj)

    if len(candidates) == 1:
        return candidates[0]

    available = ", ".join(sorted(cls.__name__ for cls in candidates)) or "nenhum"

    raise RuntimeError(
        "Classe de service da Fase 3 nao localizada de forma inequivoca. "
        f"Candidatos: {available}"
    )


def _instantiate_service(service_class: type[Any], db_path: Path) -> Any:
    attempts = (
        lambda: service_class(db_path=db_path),
        lambda: service_class(db_path=str(db_path)),
        lambda: service_class(database_path=db_path),
        lambda: service_class(database_path=str(db_path)),
        lambda: service_class(path=db_path),
        lambda: service_class(path=str(db_path)),
        lambda: service_class(db_path),
        lambda: service_class(str(db_path)),
        lambda: service_class(sqlite3.connect(str(db_path))),
    )

    errors: list[str] = []

    for attempt in attempts:
        try:
            return attempt()
        except TypeError as exc:
            errors.append(str(exc))

    joined = " | ".join(errors[-3:])

    raise RuntimeError(
        f"Nao foi possivel instanciar o service da Fase 3: {joined}"
    )


def _find_capture_method(service: Any) -> Any:
    for method_name in CAPTURE_METHOD_CANDIDATES:
        method = getattr(service, method_name, None)

        if callable(method):
            return method

    available = [
        name
        for name in dir(service)
        if not name.startswith("_") and callable(getattr(service, name))
    ]

    raise RuntimeError(
        "Metodo de captura unica nao encontrado no service da Fase 3. "
        f"Metodos publicos disponiveis: {', '.join(sorted(available))}"
    )


def _call_capture_method(method: Any, db_path: Path) -> Any:
    signature = inspect.signature(method)
    parameters = signature.parameters

    if not parameters:
        return method()

    kwargs: dict[str, Any] = {}

    if "dry_run" in parameters:
        kwargs["dry_run"] = False

    if "db_path" in parameters:
        kwargs["db_path"] = db_path

    if "database_path" in parameters:
        kwargs["database_path"] = db_path

    if "path" in parameters:
        kwargs["path"] = db_path

    if kwargs:
        return method(**kwargs)

    return method()


def _normalize_capture_result(result: Any) -> dict[str, Any]:
    if result is None:
        return {
            "mode": "capture",
            "captured_rows": None,
            "result_type": "none",
        }

    if isinstance(result, int):
        return {
            "mode": "capture",
            "captured_rows": result,
            "result_type": "int",
        }

    if isinstance(result, dict):
        normalized = dict(result)
        normalized.setdefault("mode", "capture")
        return normalized

    if isinstance(result, (list, tuple, set)):
        return {
            "mode": "capture",
            "captured_rows": len(result),
            "result_type": type(result).__name__,
        }

    for attr_name in (
        "captured_rows",
        "captured_count",
        "inserted_rows",
        "inserted_count",
        "total",
    ):
        if hasattr(result, attr_name):
            value = getattr(result, attr_name)

            return {
                "mode": "capture",
                "captured_rows": value,
                "result_type": type(result).__name__,
            }

    return {
        "mode": "capture",
        "captured_rows": None,
        "result_type": type(result).__name__,
        "result_repr": repr(result),
    }


def run_capture_once(db_path: str | Path, dry_run: bool = False) -> dict[str, Any]:
    resolved_db_path = Path(db_path).expanduser().resolve()

    if not resolved_db_path.exists():
        raise FileNotFoundError(f"Banco nao encontrado: {resolved_db_path}")

    if dry_run:
        snapshot_rows = _count_snapshot_rows(resolved_db_path)

        return {
            "mode": "dry-run",
            "db_path": str(resolved_db_path),
            "snapshot_rows": snapshot_rows,
            "captured_rows": 0,
        }

    service_class = _find_service_class()
    service = _instantiate_service(service_class, resolved_db_path)
    method = _find_capture_method(service)
    result = _call_capture_method(method, resolved_db_path)

    normalized = _normalize_capture_result(result)
    normalized.setdefault("db_path", str(resolved_db_path))

    return normalized


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = run_capture_once(args.db, dry_run=args.dry_run)
    except Exception as exc:
        payload = {
            "ok": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
        }

        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return 2

    payload = {
        "ok": True,
        **result,
    }

    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
