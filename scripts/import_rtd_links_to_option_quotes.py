#!/usr/bin/env python3
"""
Importa dados verticais de dados/RTD_LINKS.csv para rtd_option_quotes.

Formato esperado do CSV:

codigo_opcao,ativo_base,campo,valor,atualizado_em
PETRA123,PETR4,call_put,CALL,2026-06-06 17:50:00
PETRA123,PETR4,strike,32.50,2026-06-06 17:50:00
PETRA123,PETR4,bid,1.20,2026-06-06 17:50:00

Uso:

python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db
python scripts/import_rtd_links_to_option_quotes.py --csv dados/RTD_LINKS.csv --db dados/app.db --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = {
    "codigo_opcao",
    "ativo_base",
    "campo",
    "valor",
    "atualizado_em",
}

NUMERIC_FIELDS = {
    "strike",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
}

TEXT_FIELDS = {
    "call_put",
    "vencimento",
}

SUPPORTED_FIELDS = NUMERIC_FIELDS | TEXT_FIELDS

UPSERT_COLUMNS = [
    "codigo_opcao",
    "ativo_base",
    "call_put",
    "strike",
    "vencimento",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "source",
    "raw_json",
    "updated_at",
]


@dataclass
class ImportStats:
    rows_read: int = 0
    rows_ignored: int = 0
    options_normalized: int = 0
    inserted: int = 0
    updated: int = 0
    dry_run: bool = False


def parse_br_number(value: Any) -> float | None:
    """
    Converte números em formatos comuns BR/US para float.

    Exemplos:
    - "1.234,56" -> 1234.56
    - "1,23" -> 1.23
    - "32.50" -> 32.5
    - "10000" -> 10000.0
    - "" -> None
    """
    if value is None:
        return None

    text = str(value).strip()

    if not text or text in {"-", "--", "NA", "N/A", "null", "None"}:
        return None

    text = (
        text.replace("R$", "")
        .replace("%", "")
        .replace(" ", "")
        .strip()
    )

    if not text:
        return None

    # Mantém apenas dígitos, sinal, ponto e vírgula.
    text = re.sub(r"[^0-9,\.\-+]", "", text)

    if not text:
        return None

    has_comma = "," in text
    has_dot = "." in text

    if has_comma and has_dot:
        # Decide pelo último separador como decimal.
        if text.rfind(",") > text.rfind("."):
            # BR: 1.234,56
            text = text.replace(".", "").replace(",", ".")
        else:
            # US: 1,234.56
            text = text.replace(",", "")
    elif has_comma:
        # Decimal brasileiro simples: 1,23
        text = text.replace(".", "").replace(",", ".")
    elif has_dot:
        # Se tiver múltiplos pontos, trata como separador de milhar exceto o último.
        if text.count(".") > 1:
            parts = text.split(".")
            text = "".join(parts[:-1]) + "." + parts[-1]

    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"número inválido: {value!r}") from exc


def normalize_call_put(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip().upper()

    if not text:
        return None

    aliases = {
        "C": "CALL",
        "CALL": "CALL",
        "COMPRA": "CALL",
        "P": "PUT",
        "PUT": "PUT",
        "VENDA": "PUT",
    }

    return aliases.get(text, text)


def detect_dialect(csv_path: Path) -> csv.Dialect:
    sample = csv_path.read_text(encoding="utf-8-sig", errors="replace")[:4096]

    try:
        return csv.Sniffer().sniff(sample, delimiters=",;")
    except csv.Error:
        return csv.excel


def validate_columns(fieldnames: list[str] | None) -> None:
    if not fieldnames:
        raise ValueError("CSV sem cabeçalho")

    normalized = {name.strip() for name in fieldnames}
    missing = REQUIRED_COLUMNS - normalized

    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"CSV sem colunas obrigatórias: {missing_text}")


def empty_record(codigo_opcao: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "codigo_opcao": codigo_opcao,
        "ativo_base": None,
        "call_put": None,
        "strike": None,
        "vencimento": None,
        "ultimo_preco": None,
        "ultima_quantidade": None,
        "bid": None,
        "ask": None,
        "volume": None,
        "iv": None,
        "delta": None,
        "gamma": None,
        "theta": None,
        "vega": None,
        "source": "rtd_links",
        "raw_json": None,
        "updated_at": None,
        "_raw_rows": [],
    }
    return record


def load_and_normalize(csv_path: str | Path) -> tuple[list[dict[str, Any]], ImportStats]:
    path = Path(csv_path)
    stats = ImportStats()

    if not path.exists():
        raise FileNotFoundError(f"CSV não encontrado: {path}")

    dialect = detect_dialect(path)
    grouped: dict[str, dict[str, Any]] = {}

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, dialect=dialect)
        validate_columns(reader.fieldnames)

        for row in reader:
            stats.rows_read += 1

            cleaned = {
                str(k).strip(): (v.strip() if isinstance(v, str) else v)
                for k, v in row.items()
                if k is not None
            }

            codigo = str(cleaned.get("codigo_opcao") or "").strip().upper()
            ativo_base = str(cleaned.get("ativo_base") or "").strip().upper()
            campo = str(cleaned.get("campo") or "").strip()
            valor = cleaned.get("valor")
            atualizado_em = str(cleaned.get("atualizado_em") or "").strip()

            if not codigo or not campo:
                stats.rows_ignored += 1
                continue

            campo = campo.lower()

            if campo not in SUPPORTED_FIELDS:
                stats.rows_ignored += 1
                continue

            record = grouped.setdefault(codigo, empty_record(codigo))

            if ativo_base:
                record["ativo_base"] = ativo_base

            record["_raw_rows"].append(cleaned)

            try:
                if campo in NUMERIC_FIELDS:
                    record[campo] = parse_br_number(valor)
                elif campo == "call_put":
                    record[campo] = normalize_call_put(valor)
                elif campo == "vencimento":
                    record[campo] = str(valor).strip() if valor is not None and str(valor).strip() else None
            except ValueError:
                stats.rows_ignored += 1
                continue

            if atualizado_em:
                current = record.get("updated_at")
                if not current or atualizado_em > current:
                    record["updated_at"] = atualizado_em

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    records = []

    for record in grouped.values():
        if not record.get("updated_at"):
            record["updated_at"] = now

        raw_rows = record.pop("_raw_rows", [])
        record["raw_json"] = json.dumps(raw_rows, ensure_ascii=False, sort_keys=True)

        records.append(record)

    stats.options_normalized = len(records)

    return records, stats


def existing_codes(conn: sqlite3.Connection, codes: list[str]) -> set[str]:
    if not codes:
        return set()

    placeholders = ",".join(["?"] * len(codes))
    sql = f"""
        SELECT codigo_opcao
        FROM rtd_option_quotes
        WHERE codigo_opcao IN ({placeholders})
    """

    return {row[0] for row in conn.execute(sql, codes).fetchall()}


def upsert_records(
    conn: sqlite3.Connection,
    records: list[dict[str, Any]],
) -> None:
    placeholders = ", ".join(["?"] * len(UPSERT_COLUMNS))
    columns_sql = ", ".join(UPSERT_COLUMNS)

    # COALESCE evita apagar dado existente quando campo não veio no CSV.
    update_assignments = [
        "ativo_base = COALESCE(excluded.ativo_base, rtd_option_quotes.ativo_base)",
        "call_put = COALESCE(excluded.call_put, rtd_option_quotes.call_put)",
        "strike = COALESCE(excluded.strike, rtd_option_quotes.strike)",
        "vencimento = COALESCE(excluded.vencimento, rtd_option_quotes.vencimento)",
        "ultimo_preco = COALESCE(excluded.ultimo_preco, rtd_option_quotes.ultimo_preco)",
        "ultima_quantidade = COALESCE(excluded.ultima_quantidade, rtd_option_quotes.ultima_quantidade)",
        "bid = COALESCE(excluded.bid, rtd_option_quotes.bid)",
        "ask = COALESCE(excluded.ask, rtd_option_quotes.ask)",
        "volume = COALESCE(excluded.volume, rtd_option_quotes.volume)",
        "iv = COALESCE(excluded.iv, rtd_option_quotes.iv)",
        "delta = COALESCE(excluded.delta, rtd_option_quotes.delta)",
        "gamma = COALESCE(excluded.gamma, rtd_option_quotes.gamma)",
        "theta = COALESCE(excluded.theta, rtd_option_quotes.theta)",
        "vega = COALESCE(excluded.vega, rtd_option_quotes.vega)",
        "source = excluded.source",
        "raw_json = excluded.raw_json",
        "updated_at = excluded.updated_at",
    ]

    sql = f"""
        INSERT INTO rtd_option_quotes ({columns_sql})
        VALUES ({placeholders})
        ON CONFLICT(codigo_opcao) DO UPDATE SET
            {", ".join(update_assignments)}
    """

    values = [
        tuple(record.get(column) for column in UPSERT_COLUMNS)
        for record in records
    ]

    conn.executemany(sql, values)


def import_csv_to_db(
    csv_path: str | Path,
    db_path: str | Path,
    dry_run: bool = False,
) -> ImportStats:
    records, stats = load_and_normalize(csv_path)
    stats.dry_run = dry_run

    conn = sqlite3.connect(str(db_path))

    try:
        codes = [record["codigo_opcao"] for record in records]
        already_existing = existing_codes(conn, codes)

        stats.updated = sum(1 for code in codes if code in already_existing)
        stats.inserted = len(codes) - stats.updated

        if not dry_run and records:
            upsert_records(conn, records)
            conn.commit()

    finally:
        conn.close()

    return stats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Importa dados/RTD_LINKS.csv para rtd_option_quotes"
    )

    parser.add_argument(
        "--csv",
        default="dados/RTD_LINKS.csv",
        help="Caminho do CSV RTD_LINKS.csv",
    )

    parser.add_argument(
        "--db",
        default="dados/app.db",
        help="Caminho do banco SQLite",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida e normaliza sem gravar no banco",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()

    stats = import_csv_to_db(
        csv_path=args.csv,
        db_path=args.db,
        dry_run=args.dry_run,
    )

    print("Importação RTD_LINKS.csv -> rtd_option_quotes")
    print(f"CSV: {args.csv}")
    print(f"DB: {args.db}")
    print(f"Dry-run: {'sim' if stats.dry_run else 'não'}")
    print(f"Registros lidos: {stats.rows_read}")
    print(f"Opções normalizadas: {stats.options_normalized}")
    print(f"Inseridos estimados: {stats.inserted}")
    print(f"Atualizados estimados: {stats.updated}")
    print(f"Registros ignorados: {stats.rows_ignored}")

    if stats.dry_run:
        print("Nenhuma alteração foi gravada no banco.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
