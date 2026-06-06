from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "dados" / "app.db"


FIELD_ALIASES = {
    "codigo": "codigo_opcao",
    "codigo_opcao": "codigo_opcao",
    "opcao": "codigo_opcao",
    "ativo": "codigo_opcao",
    "ativo_base": "ativo_base",
    "underlying": "ativo_base",

    "tipo": "call_put",
    "call_put": "call_put",
    "cp": "call_put",

    "strike": "strike",
    "preco_exercicio": "strike",

    "vencimento": "vencimento",
    "expiration": "vencimento",
    "expiration_date": "vencimento",

    "ultimo": "ultimo_preco",
    "último": "ultimo_preco",
    "last": "ultimo_preco",
    "ultimo_preco": "ultimo_preco",

    "ultima_quantidade": "ultima_quantidade",
    "last_qty": "ultima_quantidade",
    "quantidade_ultimo": "ultima_quantidade",

    "bid": "bid",
    "ask": "ask",
    "volume": "volume",

    "iv": "iv",
    "delta": "delta",
    "gamma": "gamma",
    "theta": "theta",
    "vega": "vega",
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


def norm_key(value: Any) -> str:
    return str(value or "").strip().lower()


def parse_float(value: Any) -> float | None:
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace("R$", "").replace("%", "").strip()

    if "," in text and "." in text:
        text = text.replace(".", "").replace(",", ".")
    elif "," in text:
        text = text.replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def normalize_call_put(value: Any) -> str | None:
    text = str(value or "").strip().upper()

    if text in {"C", "CALL"}:
        return "CALL"

    if text in {"P", "PUT"}:
        return "PUT"

    return text or None


def load_rows(csv_path: Path) -> list[dict[str, Any]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def pivot_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = defaultdict(dict)
    raw_grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        codigo = (
            row.get("codigo_opcao")
            or row.get("codigo")
            or row.get("opcao")
            or row.get("ativo")
        )

        if not codigo:
            continue

        codigo = str(codigo).strip().upper()
        raw_grouped[codigo].append(row)

        ativo_base = row.get("ativo_base") or row.get("underlying")
        if ativo_base:
            grouped[codigo]["ativo_base"] = str(ativo_base).strip().upper()

        campo = row.get("campo")
        valor = row.get("valor")

        if campo:
            campo_norm = FIELD_ALIASES.get(norm_key(campo), norm_key(campo))

            if campo_norm == "codigo_opcao":
                grouped[codigo]["codigo_opcao"] = codigo
            elif campo_norm == "ativo_base":
                grouped[codigo]["ativo_base"] = str(valor or "").strip().upper()
            elif campo_norm == "call_put":
                grouped[codigo]["call_put"] = normalize_call_put(valor)
            elif campo_norm in NUMERIC_FIELDS:
                grouped[codigo][campo_norm] = parse_float(valor)
            else:
                grouped[codigo][campo_norm] = valor

        else:
            # Também aceita CSV já largo, uma linha por opção.
            for key, value in row.items():
                key_norm = FIELD_ALIASES.get(norm_key(key), norm_key(key))

                if key_norm == "codigo_opcao":
                    grouped[codigo]["codigo_opcao"] = codigo
                elif key_norm == "ativo_base":
                    grouped[codigo]["ativo_base"] = str(value or "").strip().upper()
                elif key_norm == "call_put":
                    grouped[codigo]["call_put"] = normalize_call_put(value)
                elif key_norm in NUMERIC_FIELDS:
                    grouped[codigo][key_norm] = parse_float(value)
                elif key_norm:
                    grouped[codigo][key_norm] = value

    for codigo, data in grouped.items():
        data["codigo_opcao"] = codigo
        data["raw_json"] = json.dumps(raw_grouped[codigo], ensure_ascii=False)

    return grouped


def upsert_quotes(quotes: dict[str, dict[str, Any]]) -> int:
    sql = """
    INSERT INTO rtd_option_quotes (
        codigo_opcao,
        ativo_base,
        call_put,
        strike,
        vencimento,
        ultimo_preco,
        ultima_quantidade,
        bid,
        ask,
        volume,
        iv,
        delta,
        gamma,
        theta,
        vega,
        source,
        raw_json,
        updated_at
    )
    VALUES (
        :codigo_opcao,
        :ativo_base,
        :call_put,
        :strike,
        :vencimento,
        :ultimo_preco,
        :ultima_quantidade,
        :bid,
        :ask,
        :volume,
        :iv,
        :delta,
        :gamma,
        :theta,
        :vega,
        'rtd_links_csv',
        :raw_json,
        CURRENT_TIMESTAMP
    )
    ON CONFLICT(codigo_opcao) DO UPDATE SET
        ativo_base = excluded.ativo_base,
        call_put = excluded.call_put,
        strike = excluded.strike,
        vencimento = excluded.vencimento,
        ultimo_preco = excluded.ultimo_preco,
        ultima_quantidade = excluded.ultima_quantidade,
        bid = excluded.bid,
        ask = excluded.ask,
        volume = excluded.volume,
        iv = excluded.iv,
        delta = excluded.delta,
        gamma = excluded.gamma,
        theta = excluded.theta,
        vega = excluded.vega,
        source = excluded.source,
        raw_json = excluded.raw_json,
        updated_at = CURRENT_TIMESTAMP
    """

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        count = 0
        for quote in quotes.values():
            payload = {
                "codigo_opcao": quote.get("codigo_opcao"),
                "ativo_base": quote.get("ativo_base"),
                "call_put": quote.get("call_put"),
                "strike": quote.get("strike"),
                "vencimento": quote.get("vencimento"),
                "ultimo_preco": quote.get("ultimo_preco"),
                "ultima_quantidade": quote.get("ultima_quantidade"),
                "bid": quote.get("bid"),
                "ask": quote.get("ask"),
                "volume": quote.get("volume"),
                "iv": quote.get("iv"),
                "delta": quote.get("delta"),
                "gamma": quote.get("gamma"),
                "theta": quote.get("theta"),
                "vega": quote.get("vega"),
                "raw_json": quote.get("raw_json"),
            }

            conn.execute(sql, payload)
            count += 1

        conn.commit()

    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Caminho do CSV exportado da aba RTD_LINKS")
    args = parser.parse_args()

    csv_path = Path(args.csv_path)

    if not csv_path.exists():
        raise SystemExit(f"CSV não encontrado: {csv_path}")

    rows = load_rows(csv_path)
    quotes = pivot_rows(rows)
    count = upsert_quotes(quotes)

    print(f"[OK] {count} opções importadas/atualizadas em rtd_option_quotes")


if __name__ == "__main__":
    main()
