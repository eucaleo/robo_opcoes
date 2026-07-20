from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from repositories.robo_legs_repository import (  # noqa: E402
    RoboLegsRepoConfig,
    RoboLegsRepository,
)
from repositories.structures_repository import StructuresRepository  # noqa: E402
from services.legacy_structure_legs_importer import (  # noqa: E402
    LegacyStructureLegsImporter,
)
from services.legacy_structure_legs_reader import LegacyStructureLegsReader  # noqa: E402


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Importa pernas legadas manual/rtd para structure_legs "
            "usando structures.alias_legacy_aba."
        )
    )

    parser.add_argument(
        "--structure-id",
        type=int,
        required=True,
        help="ID da estrutura em structures.id",
    )

    parser.add_argument(
        "--timestamp",
        required=True,
        help='Timestamp legado. Exemplo: "2026-05-19 10:00:00"',
    )

    parser.add_argument(
        "--db-path",
        default="./dados/app.db",
        help="Caminho do banco SQLite. Default: ./dados/app.db",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas lê e exibe as pernas canônicas, sem gravar em structure_legs.",
    )

    return parser


def _print_json(payload: dict) -> None:
    print(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    robo_legs_repository = RoboLegsRepository(
        RoboLegsRepoConfig(app_db_path=args.db_path)
    )

    reader = LegacyStructureLegsReader(
        robo_legs_repository=robo_legs_repository,
    )

    try:
        if args.dry_run:
            legs = reader.read_by_structure_id(
                structure_id=args.structure_id,
                timestamp=args.timestamp,
            )

            _print_json(
                {
                    "ok": True,
                    "dry_run": True,
                    "structure_id": args.structure_id,
                    "timestamp": args.timestamp,
                    "db_path": args.db_path,
                    "legs_count": len(legs),
                    "legs": legs,
                }
            )
            return 0

        structures_repository = StructuresRepository(
            db_path=args.db_path,
        )

        importer = LegacyStructureLegsImporter(
            reader=reader,
            structures_repository=structures_repository,
        )

        result = importer.import_by_structure_id(
            structure_id=args.structure_id,
            timestamp=args.timestamp,
        )

        _print_json(
            {
                "ok": True,
                "dry_run": False,
                "db_path": args.db_path,
                **result,
            }
        )
        return 0

    except Exception as exc:
        _print_json(
            {
                "ok": False,
                "dry_run": bool(args.dry_run),
                "structure_id": args.structure_id,
                "timestamp": args.timestamp,
                "db_path": args.db_path,
                "error": str(exc),
                "error_type": type(exc).__name__,
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
