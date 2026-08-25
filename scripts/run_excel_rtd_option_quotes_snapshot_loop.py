#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from services.rtd_option_quotes_excel_sync import sync_rtd_option_quotes_from_excel


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(name, default)

    return getattr(obj, name, default)


def _format_result(result: Any) -> str:
    if isinstance(result, dict):
        codes = result.get("codes") or []
        quotes = result.get("quotes") or []
        db_result = result.get("db_result") or {}

        parts = []

        if isinstance(codes, list):
            parts.append(f"codes={len(codes)}")

        if isinstance(quotes, list):
            parts.append(f"quotes={len(quotes)}")

        if isinstance(db_result, dict):
            updated = db_result.get("updated")
            inserted = db_result.get("inserted")
            total = db_result.get("total")

            if updated is not None:
                parts.append(f"updated={updated}")

            if inserted is not None:
                parts.append(f"inserted={inserted}")

            if total is not None:
                parts.append(f"total={total}")

        if parts:
            return ", ".join(parts)

    inserted = _get_attr(result, "inserted", None)
    updated = _get_attr(result, "updated", None)
    skipped = _get_attr(result, "skipped", None)
    total = _get_attr(result, "total", None)
    rows = _get_attr(result, "rows", None)

    parts = []

    if total is not None:
        parts.append(f"total={total}")

    if rows is not None:
        parts.append(f"rows={rows}")

    if inserted is not None:
        parts.append(f"inserted={inserted}")

    if updated is not None:
        parts.append(f"updated={updated}")

    if skipped is not None:
        parts.append(f"skipped={skipped}")

    if not parts:
        return repr(result)

    return ", ".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Executa snapshots recorrentes de cotações RTD de opções usando o "
            "fluxo Excel online canônico."
        )
    )

    parser.add_argument(
        "--db",
        "--db-path",
        dest="db_path",
        default=None,
        help="Caminho do banco SQLite. Se omitido, usa o padrão da aplicação.",
    )

    parser.add_argument(
        "--workbook",
        "--workbook-path",
        dest="workbook_path",
        default=None,
        help="Caminho da planilha RTD. Se omitido, usa o padrão do serviço.",
    )

    parser.add_argument(
        "--sheet",
        "--sheet-name",
        dest="sheet_name",
        default=None,
        help="Nome da aba da planilha. Se omitido, usa o padrão do serviço.",
    )

    parser.add_argument(
        "--wait",
        "--wait-seconds",
        dest="wait_seconds",
        type=float,
        default=10,
        help="Segundos de espera para atualização do RTD após popular a planilha.",
    )

    parser.add_argument(
        "--interval",
        "--sleep",
        "--sleep-seconds",
        dest="interval_seconds",
        type=float,
        default=60,
        help="Intervalo em segundos entre snapshots.",
    )

    parser.add_argument(
        "--iterations",
        "--count",
        "--max-iterations",
        dest="iterations",
        type=int,
        default=0,
        help="Quantidade de snapshots. Use 0 para loop infinito.",
    )

    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Inclui estruturas/ativos arquivados, se suportado pelo serviço.",
    )

    parser.add_argument(
        "--visible",
        action="store_true",
        help="Abre o Excel visível.",
    )

    parser.add_argument(
        "--shared-excel",
        dest="isolated",
        action="store_false",
        default=True,
        help="Não usa instância isolada do Excel.",
    )

    parser.add_argument(
        "--keep-open",
        dest="close_on_finish",
        action="store_false",
        default=True,
        help="Mantém o Excel aberto ao final de cada snapshot.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa sem gravar no banco, se suportado pelo serviço.",
    )

    parser.add_argument(
        "--quiet",
        dest="print_rows",
        action="store_false",
        default=True,
        help="Não imprime linhas individuais processadas.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    current_iteration = 0

    while True:
        current_iteration += 1

        print(
            f"[rtd-loop] snapshot {current_iteration} iniciado "
            f"(wait={args.wait_seconds}s, interval={args.interval_seconds}s)"
        )

        try:
            result = sync_rtd_option_quotes_from_excel(
                db_path=args.db_path,
                workbook_path=args.workbook_path,
                sheet_name=args.sheet_name,
                include_archived=args.include_archived,
                wait_seconds=args.wait_seconds,
                visible=args.visible,
                isolated=args.isolated,
                close_on_finish=args.close_on_finish,
                dry_run=args.dry_run,
                print_rows=args.print_rows,
            )

            print(f"[rtd-loop] snapshot {current_iteration} concluído: {_format_result(result)}")

        except KeyboardInterrupt:
            print()
            print("[rtd-loop] interrompido pelo usuário.")
            return 130

        except Exception as exc:
            print(f"[rtd-loop] erro no snapshot {current_iteration}: {exc}", file=sys.stderr)

        if args.iterations and current_iteration >= args.iterations:
            break

        try:
            time.sleep(args.interval_seconds)
        except KeyboardInterrupt:
            print()
            print("[rtd-loop] interrompido pelo usuário.")
            return 130

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
