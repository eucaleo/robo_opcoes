# Alvos iniciais Fase 1 RTD Excel Vivo

Atualizado em: 20260630_220530

## Objetivo

Localizar pontos que ainda usam fluxo antigo RTD sob demanda, subprocesso, Excel direto ou reconciliação entre bancos.

## Arquivos alvo identificados

    UI/components/structure_editor_dialog.py
    scripts/rtd_reconciliar_app_para_derived.py
    scripts/import_rtd_option_quotes_wide_csv.py
    scripts/refresh_rtd_option_quotes_excel.ps1
    repositories/rtd_option_quotes_repository.py
    ATT/tests/test_rtd_live_db_guardrail.py
    ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py

## Trecho structure_editor_dialog.py

        self._legs_rows[idx], self._legs_rows[new_idx] = (
            self._legs_rows[new_idx],
            self._legs_rows[idx],
        )
        self._refresh_leg_tree()
        self._leg_tree.selection_set(str(new_idx))

    def _cmd_apply_leg(self):
        """Aplica os valores do formulario na leg selecionada."""
        idx = self._selected_leg_index()
        if idx is None:
            messagebox.showwarning(
                "Aplicar Leg", "Selecione uma leg na lista primeiro.", parent=self
            )
            return

        self._legs_rows[idx] = {
            "position_side":   normalize_position_side(self._lf_side.get()),
            "option_type":     self._lf_type.get(),
            "strike":          self._lf_strike.get(),
            "expiration_date": self._lf_expiry.get(),
            "quantity":        self._lf_qty.get(),
            "premium":         self._lf_premium.get() or None,
            "multiplier":      self._lf_mult.get() or 1,
            "leg_order":       idx + 1,
            "symbol":          self._lf_symbol.get() or None,
            "notes":           None,
        }
        self._refresh_leg_tree()


    def _refresh_rtd_symbol_on_demand(self, codigo_opcao: str) -> tuple[bool, str]:
        """Atualiza uma opcao via RTD/Excel e grava o cache em dados/app.db."""
        symbol = str(codigo_opcao or "").strip().upper()

        if not symbol:
            return False, "Codigo da opcao vazio."

        project_root = Path(__file__).resolve().parents[2]
        script_path = project_root / "scripts" / "refresh_rtd_symbol_to_option_quotes_fallback.py"
        db_path = project_root / "dados" / "app.db"

        if not script_path.exists():
            return False, f"Script RTD nao encontrado: {script_path}"

        cmd = [
            sys.executable,
            str(script_path),
            "--symbol",
            symbol,
            "--db",
            str(db_path),
            "--wait-seconds",
            "3",
            "--json",
        ]

        try:
            completed = subprocess.run(
                cmd,
                cwd=str(project_root),
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=20,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return False, f"Timeout ao atualizar RTD para {symbol}."

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        if completed.returncode != 0:
            detail = stderr or stdout or "sem detalhe"
            return False, f"Falha ao atualizar RTD para {symbol}: {detail}"

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return False, f"RTD atualizou, mas retornou JSON invalido: {stdout[:500]}"

        if data.get("status") != "ok":
            errors = data.get("errors") or []
            return False, f"RTD retornou erro para {symbol}: {errors}"

        quote = data.get("quote")

        if not quote:
            return False, f"RTD executou, mas nao retornou cotacao para {symbol}."

## Trecho scripts/rtd_reconciliar_app_para_derived.py

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

## Trecho scripts/import_rtd_option_quotes_wide_csv.py

import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from infra.bootstrap_rtd_option_quotes_schema import ensure_rtd_option_quotes_schema


NUMERIC_COLUMNS = {
    "strike",
    "ultimo_preco",
    "ultima_quantidade",
    "bid",
    "ask",
    "volume",
    "vwap",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
}


EXPECTED_COLUMNS = [
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
    "vwap",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
]


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_number(value):
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    invalids = {
        "#N/D",
        "#N/A",
        "#VALOR!",
        "#VALUE!",
        "#REF!",
        "#NAME?",
        "#NOME?",
        "#DIV/0!",
        "N/A",
        "NA",
        "NULL",
        "NONE",
        "-",
    }

    if text.upper() in invalids:
        return None

    text = text.replace("R$", "").replace("%", "").strip()

    # Formato BR: 20.119,50 -> 20119.50
    if "," in text:
        text = text.replace(".", "").replace(",", ".")

    try:
        return float(text)
    except ValueError:
        return None


def parse_excel_date(value):
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    # Já veio como data textual.
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    serial = parse_number(text)

    if serial is None:
        return None

    # Excel usa 1899-12-30 como base para compatibilidade histórica.
    days = int(serial)
    dt = datetime(1899, 12, 30) + timedelta(days=days)
    return dt.strftime("%Y-%m-%d")


def normalize_call_put(value):
    text = "" if value is None else str(value).strip().upper()

    if text in {"C", "CALL", "COMPRA"}:
        return "CALL"

    if text in {"P", "PUT", "VENDA"}:
        return "PUT"

    return text or None


def clean_text(value):
    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    return text


def detect_dialect(csv_path):
    sample = Path(csv_path).read_text(encoding="utf-8-sig", errors="replace")[:4096]

    try:
        return csv.Sniffer().sniff(sample, delimiters=";,")
    except csv.Error:
        class Dialect(csv.excel):
            delimiter = ";"

        return Dialect


def load_csv(csv_path):
    dialect = detect_dialect(csv_path)
    rows = []

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, dialect=dialect)

        if not reader.fieldnames:
            raise ValueError("CSV sem cabeçalho.")

        fieldnames = [c.strip() for c in reader.fieldnames]
        missing = [c for c in EXPECTED_COLUMNS if c not in fieldnames]

        if missing:
            raise ValueError("CSV sem colunas obrigatórias: " + ", ".join(missing))

        for raw in reader:
            raw = {str(k).strip(): v for k, v in raw.items() if k is not None}
            codigo = clean_text(raw.get("codigo_opcao"))

            if not codigo:
                continue

            record = {
                "codigo_opcao": codigo.upper(),
                "ativo_base": clean_text(raw.get("ativo_base")),
                "call_put": normalize_call_put(raw.get("call_put")),
                "strike": parse_number(raw.get("strike")),
                "vencimento": parse_excel_date(raw.get("vencimento")),
                "ultimo_preco": parse_number(raw.get("ultimo_preco")),
                "ultima_quantidade": parse_number(raw.get("ultima_quantidade")),
                "bid": parse_number(raw.get("bid")),
                "ask": parse_number(raw.get("ask")),
                "volume": parse_number(raw.get("volume")),
                "vwap": parse_number(raw.get("vwap")),
                "iv": parse_number(raw.get("iv")),
                "delta": parse_number(raw.get("delta")),
                "gamma": parse_number(raw.get("gamma")),
                "theta": parse_number(raw.get("theta")),
                "vega": parse_number(raw.get("vega")),
                "source": "BTG_RTD_EXCEL",
                "raw_json": json.dumps(raw, ensure_ascii=False),
            }

            rows.append(record)

    return rows


def ensure_index(con):
    con.execute("""
        CREATE INDEX IF NOT EXISTS idx_rtd_option_quotes_codigo_opcao
        ON rtd_option_quotes(codigo_opcao)
    """)


def import_rows(db_path, rows, dry_run=False):
    updated_at = now_text()

    stats = {
        "input_rows": len(rows),

## Trecho repositories/rtd_option_quotes_repository.py

# repositories/rtd_option_quotes_repository.py

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class RtdOptionQuotesRepository:
    """
    Leitura da tabela rtd_option_quotes.

    Essa tabela e alimentada pelo CSV exportado da aba RTD_LINKS
    e funciona como cache centralizado das cotacoes RTD de opcoes.

    Arquitetura:
    - dados/app.db: dados persistentes da aplicacao/estruturas
    - dados/app.db: cache RTD operacional
    """

    def __init__(self, db_path: str | Path = "dados/app.db") -> None:
        self.db_path = Path(db_path)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def get_by_codigo(self, codigo_opcao: str) -> dict[str, Any] | None:
        sql = """
            SELECT
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
                vwap,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            WHERE UPPER(TRIM(codigo_opcao)) = UPPER(TRIM(?))
            ORDER BY updated_at DESC, id DESC
            LIMIT 1
        """

        with self._connect() as conn:
            row = conn.execute(sql, (codigo_opcao,)).fetchone()

        return dict(row) if row else None

    def list_by_ativo_base(self, ativo_base: str) -> list[dict[str, Any]]:
        sql = """
            SELECT
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
                vwap,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            WHERE UPPER(TRIM(ativo_base)) = UPPER(TRIM(?))
            ORDER BY vencimento, call_put, strike, codigo_opcao
        """

        with self._connect() as conn:
            rows = conn.execute(sql, (ativo_base,)).fetchall()

        return [dict(row) for row in rows]

    def list_all(self) -> list[dict[str, Any]]:
        sql = """
            SELECT
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
                vwap,
                iv,
                delta,
                gamma,
                theta,
                vega,
                source,
                raw_json,
                updated_at,
                created_at
            FROM rtd_option_quotes
            ORDER BY ativo_base, vencimento, call_put, strike, codigo_opcao
        """

        with self._connect() as conn:
            rows = conn.execute(sql).fetchall()

        return [dict(row) for row in rows]

## Trecho ATT/tests/test_rtd_live_db_guardrail.py

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


RTD_LIVE_OPERATIONAL_FILES = [
    "repositories/rtd_option_quotes_repository.py",
    "repositories/market_snapshot_repository.py",
    "services/structure_leg_rtd_enrichment_service.py",
    "UI/components/structure_editor_dialog.py",
    "UI/components/terminal_vwap_payoff_dark_panel.py",
    "infra/bootstrap_rtd_option_quotes_schema.py",
    "scripts/import_rtd_option_quotes_wide_csv.py",
    "scripts/refresh_rtd_symbol_to_option_quotes.py",
    "scripts/refresh_rtd_symbol_to_option_quotes_fallback.py",
]


FORBIDDEN_DERIVED_MARKERS = [
    "dados/derived.db",
    "data/derived.db",
    "derived.db",
    "DERIVED_DB_PATH",
    "connect_derived",
]


def _read_project_file(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    assert path.exists(), f"Arquivo esperado não encontrado: {relative_path}"
    return path.read_text(encoding="utf-8", errors="replace")


def test_rtd_live_operational_files_do_not_reference_derived_db():
    """
    RTD vivo operacional deve usar dados/app.db.

    A tabela rtd_option_quotes e a tabela rtd_underlying_quotes não podem voltar
    a ser lidas/escritas operacionalmente em dados/derived.db.

    derived.db permanece válido para payoff, snapshots derivados, simulações e
    artefatos regeneráveis, mas não para cache vivo RTD.
    """
    violations = []

    for relative_path in RTD_LIVE_OPERATIONAL_FILES:
        text = _read_project_file(relative_path)
        for marker in FORBIDDEN_DERIVED_MARKERS:
            if marker in text:
                violations.append(f"{relative_path}: contém marcador proibido `{marker}`")

    assert not violations, "\n".join(violations)


def test_rtd_option_quotes_repository_default_db_is_app_db():
    """
    O repositório operacional de rtd_option_quotes deve apontar por padrão para dados/app.db.
    """
    text = _read_project_file("repositories/rtd_option_quotes_repository.py")

    assert '"dados/app.db"' in text or "'dados/app.db'" in text
    assert '"dados/derived.db"' not in text
    assert "'dados/derived.db'" not in text


def test_structure_editor_rtd_refresh_and_enrichment_use_app_db():
    """
    A UI de edição de estrutura, ao atualizar/preencher leg via RTD, deve usar app.db.
    """
    text = _read_project_file("UI/components/structure_editor_dialog.py")

    assert 'project_root / "dados" / "app.db"' in text
    assert 'project_root / "dados" / "derived.db"' not in text

## Trecho ATT/tests/test_market_snapshot_repository_rtd_option_quotes.py

import sqlite3

import pytest

from repositories.market_snapshot_repository import MarketSnapshotRepository


def _create_rtd_legs_table(conn):
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


def _create_rtd_option_quotes_table(conn):
    conn.execute(
        """
        CREATE TABLE rtd_option_quotes (
            codigo_opcao TEXT,
            ativo_base TEXT,
            call_put TEXT,
            strike TEXT,
            vencimento TEXT,
            ultimo_preco TEXT,
            ultima_quantidade TEXT,
            bid TEXT,
            ask TEXT,
            volume TEXT,
            iv TEXT,
            delta TEXT,
            gamma TEXT,
            theta TEXT,
            vega TEXT,
            source TEXT,
            raw_json TEXT,
            updated_at TEXT,
            created_at TEXT
        )
        """
    )


def _insert_base_rtd_leg(conn):
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
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "2026-05-18 10:00:00",
            "BOVA11",
            "BOVAE195",
            "C",
            "C",
            "5000",
            "1,10",
            "1,00",
            "1,20",
            "0,20",
            "18,18",
            "0,22",
            "0,50",
            "0,01",
            "-0,02",
            "0,03",
            "195,00",
            "2026-05-15",
            "10",
            "100,00",
        ),
    )


def test_get_rtd_option_quote_legs_enriches_base_rtd_leg_with_quote_cache(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        _create_rtd_legs_table(conn)
        _create_rtd_option_quotes_table(conn)
        _insert_base_rtd_leg(conn)

        conn.execute(
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
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "BOVAE195",
                "BOVA11",
                "CALL",
                "195,00",
                "2026-05-15",
                "1,23",
                "100",
                "1,22",
                "1,24",
                "1000",
                "0,33",
                "0,44",
                "0,055",
                "-0,066",
                "0,077",
                "rtd_option_quotes",
                "{}",
                "2026-05-18 10:05:00",
                "2026-05-18 10:04:00",
            ),
        )
        conn.commit()

    repo = MarketSnapshotRepository(db_path=db_path)

    legs = repo.get_rtd_option_quote_legs("BOVA11")

    assert len(legs) == 1

    leg = legs[0]

    # Identidade/composição vêm da leg estrutural RTD.
    assert leg.aba == "BOVA11"
    assert leg.ativo == "BOVAE195"
    assert leg.cv == "C"
    assert leg.quant == 5000.0
    assert leg.dte == 10.0
    assert leg.pl_realista == 100.0

    # Cotação/greeks vêm do cache centralizado rtd_option_quotes.
    assert leg.source == "rtd_option_quotes"
    assert leg.call_put == "CALL"
    assert leg.bid == 1.22
    assert leg.ask == 1.24
    assert leg.mid == pytest.approx(1.23)
    assert leg.valor_executado == pytest.approx(1.23)
    assert leg.strike == 195.0
    assert leg.vencimento == "2026-05-15"
    assert leg.iv == 0.33
    assert leg.delta == 0.44
    assert leg.gamma == 0.055
    assert leg.theta == -0.066
    assert leg.vega == 0.077
    assert leg.timestamp == "2026-05-18 10:05:00"


def test_get_rtd_option_quote_legs_returns_empty_list_when_cache_table_is_missing(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        _create_rtd_legs_table(conn)
        _insert_base_rtd_leg(conn)
        conn.commit()

    repo = MarketSnapshotRepository(db_path=db_path)

    assert repo.get_rtd_option_quote_legs("BOVA11") == []


def _insert_rtd_option_quote(
    conn,
    *,
    codigo_opcao="BOVAE195",
    ativo_base="BOVA11",
    call_put="CALL",
    strike="195,00",
    vencimento="2026-05-15",
    ultimo_preco="1,23",
    bid="1,22",
    ask="1,24",
    iv="0,33",
    delta="0,44",
    gamma="0,055",
    theta="-0,066",
    vega="0,077",
    updated_at="2026-05-18 10:05:00",
):
    conn.execute(
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
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            codigo_opcao,
            ativo_base,
            call_put,
            strike,
            vencimento,
            ultimo_preco,
            "100",
            bid,
            ask,
            "1000",
            iv,
            delta,
            gamma,
            theta,
            vega,
            "rtd_option_quotes",
            "{}",
            updated_at,
            updated_at,
        ),
    )


def test_get_rtd_option_quote_legs_ignores_orphan_quote_without_structural_leg(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        _create_rtd_legs_table(conn)
        _create_rtd_option_quotes_table(conn)

        _insert_rtd_option_quote(
            conn,
            codigo_opcao="BOVAE195",
            ativo_base="BOVA11",
            ultimo_preco="1,23",
            bid="1,22",
            ask="1,24",
            updated_at="2026-05-18 10:05:00",
        )

        conn.commit()

    repo = MarketSnapshotRepository(db_path=db_path)

    assert repo.get_rtd_option_quote_legs("BOVA11") == []


def test_get_rtd_option_quote_legs_uses_latest_quote_when_cache_has_duplicates(tmp_path):
    db_path = tmp_path / "app.db"

    with sqlite3.connect(str(db_path)) as conn:
        _create_rtd_legs_table(conn)
        _create_rtd_option_quotes_table(conn)
        _insert_base_rtd_leg(conn)

        _insert_rtd_option_quote(
            conn,
            codigo_opcao="BOVAE195",
            ativo_base="BOVA11",
            ultimo_preco="1,11",
            bid="1,10",
            ask="1,12",
            iv="0,21",
            delta="0,31",
            gamma="0,041",
            theta="-0,051",
            vega="0,061",
            updated_at="2026-05-18 10:01:00",
        )

        _insert_rtd_option_quote(
            conn,
            codigo_opcao="BOVAE195",
            ativo_base="BOVA11",
            ultimo_preco="1,45",
            bid="1,44",
            ask="1,46",
            iv="0,39",
            delta="0,49",
            gamma="0,059",
            theta="-0,069",
            vega="0,079",
            updated_at="2026-05-18 10:09:00",
        )

        conn.commit()

    repo = MarketSnapshotRepository(db_path=db_path)

    legs = repo.get_rtd_option_quote_legs("BOVA11")

    assert len(legs) == 1

    leg = legs[0]

    assert leg.source == "rtd_option_quotes"
    assert leg.ativo == "BOVAE195"
