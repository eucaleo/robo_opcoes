from pathlib import Path
import sqlite3
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

APP_DB = ROOT / "dados" / "app.db"
DERIVED_DB = ROOT / "dados" / "derived.db"


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "").strip())
    except Exception:
        return None


def is_positive_number(value):
    try:
        return value is not None and float(value) > 0
    except Exception:
        return False


def main():
    if not APP_DB.exists():
        raise SystemExit(f"app.db não encontrado: {APP_DB}")

    if not DERIVED_DB.exists():
        raise SystemExit(f"derived.db não encontrado: {DERIVED_DB}")

    app = sqlite3.connect(str(APP_DB))
    app.row_factory = sqlite3.Row

    derived = sqlite3.connect(str(DERIVED_DB))
    derived.row_factory = sqlite3.Row

    app_rows = app.execute(
        """
        SELECT *
        FROM rtd_option_quotes
        """
    ).fetchall()

    print("=" * 100)
    print("Reconciliando app.db:rtd_option_quotes -> derived.db:rtd_option_quotes")
    print("=" * 100)
    print("linhas app:", len(app_rows))

    updated = 0
    inserted = 0
    skipped = 0

    for app_row in app_rows:
        a = dict(app_row)
        codigo = a.get("codigo_opcao")

        if not codigo:
            skipped += 1
            continue

        drow = derived.execute(
            """
            SELECT *
            FROM rtd_option_quotes
            WHERE codigo_opcao = ?
            LIMIT 1
            """,
            (codigo,),
        ).fetchone()

        if drow is None:
            derived.execute(
                """
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
                    updated_at,
                    created_at,
                    vwap
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    a.get("codigo_opcao"),
                    a.get("ativo_base"),
                    a.get("call_put"),
                    a.get("strike"),
                    a.get("vencimento"),
                    a.get("ultimo_preco"),
                    a.get("ultima_quantidade"),
                    a.get("bid"),
                    a.get("ask"),
                    a.get("volume"),
                    a.get("iv"),
                    a.get("delta"),
                    a.get("gamma"),
                    a.get("theta"),
                    a.get("vega"),
                    a.get("source") or "BTG_RTD_EXCEL_APP_SYNC",
                    a.get("raw_json"),
                    a.get("updated_at"),
                    a.get("created_at"),
                    a.get("vwap"),
                ),
            )
            inserted += 1
            print(f"INSERIDO {codigo}")
            continue

        d = dict(drow)

        app_dt = parse_dt(a.get("updated_at"))
        derived_dt = parse_dt(d.get("updated_at"))

        app_is_newer = bool(app_dt and derived_dt and app_dt > derived_dt)
        derived_vwap_missing = not is_positive_number(d.get("vwap"))
        app_vwap_valid = is_positive_number(a.get("vwap"))

        should_update = app_is_newer or (derived_vwap_missing and app_vwap_valid)

        if not should_update:
            skipped += 1
            continue

        # Regra conservadora:
        # - Se app for mais novo, atualiza principais campos de mercado.
        # - Se app só tiver VWAP melhor, pelo menos corrige VWAP sem destruir dado mais recente.
        if app_is_newer:
            derived.execute(
                """
                UPDATE rtd_option_quotes
                SET
                    ativo_base = COALESCE(?, ativo_base),
                    call_put = COALESCE(?, call_put),
                    strike = COALESCE(?, strike),
                    vencimento = COALESCE(?, vencimento),
                    ultimo_preco = COALESCE(?, ultimo_preco),
                    ultima_quantidade = COALESCE(?, ultima_quantidade),
                    bid = COALESCE(?, bid),
                    ask = COALESCE(?, ask),
                    volume = COALESCE(?, volume),
                    iv = COALESCE(?, iv),
                    delta = COALESCE(?, delta),
                    gamma = COALESCE(?, gamma),
                    theta = COALESCE(?, theta),
                    vega = COALESCE(?, vega),
                    source = COALESCE(?, source),
                    raw_json = COALESCE(?, raw_json),
                    updated_at = COALESCE(?, updated_at),
                    vwap = CASE
                        WHEN ? IS NOT NULL THEN ?
                        ELSE vwap
                    END
                WHERE codigo_opcao = ?
                """,
                (
                    a.get("ativo_base"),
                    a.get("call_put"),
                    a.get("strike"),
                    a.get("vencimento"),
                    a.get("ultimo_preco"),
                    a.get("ultima_quantidade"),
                    a.get("bid"),
                    a.get("ask"),
                    a.get("volume"),
                    a.get("iv"),
                    a.get("delta"),
                    a.get("gamma"),
                    a.get("theta"),
                    a.get("vega"),
                    a.get("source") or "BTG_RTD_EXCEL_APP_SYNC",
                    a.get("raw_json"),
                    a.get("updated_at"),
                    a.get("vwap"),
                    a.get("vwap"),
                    codigo,
                ),
            )
            updated += 1
            print(f"ATUALIZADO {codigo} app_mais_novo app_updated_at={a.get('updated_at')} derived_updated_at={d.get('updated_at')}")
        else:
            derived.execute(
                """
                UPDATE rtd_option_quotes
                SET
                    vwap = ?,
                    source = COALESCE(source, ?)
                WHERE codigo_opcao = ?
                """,
                (
                    a.get("vwap"),
                    a.get("source") or "BTG_RTD_EXCEL_APP_SYNC",
                    codigo,
                ),
            )
            updated += 1
            print(f"VWAP_CORRIGIDO {codigo} vwap={a.get('vwap')}")

    derived.commit()

    print()
    print("=" * 100)
    print("Resumo")
    print("=" * 100)
    print("inseridos:", inserted)
    print("atualizados:", updated)
    print("ignorados:", skipped)

    print()
    print("derived.db após reconciliação:")
    rows = derived.execute(
        """
        SELECT codigo_opcao, ativo_base, ultimo_preco, bid, ask, volume, vwap, updated_at
        FROM rtd_option_quotes
        ORDER BY updated_at DESC, id DESC
        """
    ).fetchall()

    for r in rows:
        print(dict(r))

    app.close()
    derived.close()


if __name__ == "__main__":
    main()
