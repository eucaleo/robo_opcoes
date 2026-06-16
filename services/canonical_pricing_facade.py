# services/canonical_pricing_facade.py
"""
alteracao_17 -- Fachada canônica corrigida.
alteracao_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado
           no PricingExecutionPersistenceService.
alteracao_41 -- Corrige underlying_asset no pricing_payload.

Correções alteracao_41:
  C6: _get_alias_legacy_aba() substituído por _get_structure_info() --
      busca alias_legacy_aba E underlying_asset em uma única query.
  C7: _snapshot_result_to_payload() recebe underlying_asset explícito --
      elimina uso de selection_result.aba como underlying_asset
      (aba legada  ativo subjacente real).
  C8: execute_pricing() passa underlying_asset para o payload builder.

Correções anteriores mantidas:
  C1: sel.select(aba=...) -- parâmetro correto
  C2: alias_legacy_aba buscado via query antes de chamar o selector
  C3: orquestração direta repo  selector  execute_payload()
  C4: engine_result extraído do wrapper antes de passar ao persister
  C5: DerivedPayoffPersistence injetado como payoff_persistence_port
"""
from __future__ import annotations


import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from repositories.market_snapshot_repository import MarketSnapshotRepository
from repositories.rtd_option_quotes_repository import RtdOptionQuotesRepository
from repositories.system_snapshots_repository import SystemSnapshotsRepository
from services.derived_payoff_persistence import DerivedPayoffPersistence
from services.market_snapshot_selector import MarketSnapshotSelector
from services.pricing_execution_persistence_service import PricingExecutionPersistenceService
from services.pricing_execution_service import PricingExecutionService

_DEFAULT_DB = Path("dados/app.db")


#  C6: substitui _get_alias_legacy_aba -- busca aba + underlying em 1 query 

def _get_structure_info(structure_id: int, db_path: Path) -> tuple[str, str]:
    """
    Retorna (alias_legacy_aba, underlying_asset) para a estrutura.

    Raises ValueError se:
      - estrutura não existir
      - alias_legacy_aba for nulo (sem aba legada mapeada)
    """
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT alias_legacy_aba, underlying_asset FROM structures WHERE id = ?",
            (structure_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"structure not found: {structure_id}")

    aba = row["alias_legacy_aba"]
    if not aba:
        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")

    underlying_asset = row["underlying_asset"]  # NOT NULL -- sempre presente

    return aba, underlying_asset


#  C7: recebe underlying_asset explícito -- não usa selection_result.aba 



def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default

        if isinstance(value, str):
            text = value.strip()
            text = text.replace("R$", "").replace("$", "").strip()

            # Remove espaços internos comuns em valores monetários.
            text = text.replace(" ", "")

            # Caso BR simples: "124,66"
            if "," in text and "." not in text:
                text = text.replace(",", ".")

            return float(text)

        return float(value)
    except Exception:
        return default


def _normalize_expiration_date(value: Any) -> str | None:
    if not value:
        return None

    text = str(value).strip()

    formats = [
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass

    return text


def _pick(data: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = data.get(name)
        if value is not None:
            return value
    return None


def _quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _sqlite_table_exists(db_path: Path, table_name: str) -> bool:
    """Retorna True se a tabela existir no SQLite informado."""
    if not db_path.exists():
        return False

    try:
        with sqlite3.connect(str(db_path)) as conn:
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
    except Exception:
        return False


def _resolve_rtd_option_quotes_db_path(primary_db_path: Path) -> Path:
    """
    Resolve o banco correto para rtd_option_quotes.

    Em alguns fluxos a facade é instanciada com dados/derived.db, mas
    rtd_option_quotes vive em dados/app.db.
    """
    candidates: list[Path] = []

    for candidate in (
        primary_db_path,
        primary_db_path.parent / "app.db",
        Path("dados/app.db"),
    ):
        candidate = Path(candidate)
        if candidate not in candidates:
            candidates.append(candidate)

    for candidate in candidates:
        if _sqlite_table_exists(candidate, "rtd_option_quotes"):
            return candidate

    # Fallback conservador: mantém comportamento anterior.
    return primary_db_path


def _is_manual_source(value: Any) -> bool:
    """Retorna True quando a fonte da leg é manual."""
    if value is None:
        return False

    raw = getattr(value, "value", value)
    return "manual" in str(raw).strip().lower()


def _quote_value(quote: Any, field: str) -> Any:
    """Lê campo de dict/sqlite.Row/objeto de forma tolerante."""
    if quote is None:
        return None

    if hasattr(quote, "get"):
        try:
            return quote.get(field)
        except Exception:
            pass

    try:
        return quote[field]
    except Exception:
        pass

    try:
        return getattr(quote, field)
    except Exception:
        return None


def _pick_rtd_option_price_with_trace(
    quote: Any | None,
) -> tuple[float | None, str | None]:
    """
    Escolhe o melhor preço disponível em rtd_option_quotes e informa
    qual campo/critério foi usado.

    Precedência:
      1. ultimo_preco
      2. price / last_price, se existirem por compatibilidade
      3. mid bid/ask
      4. bid
      5. ask
    """
    if not quote:
        return None, None

    for field in ("ultimo_preco", "price", "last_price"):
        price = _to_float(_quote_value(quote, field), 0.0)
        if price > 0:
            return price, field

    bid = _to_float(_quote_value(quote, "bid"), 0.0)
    ask = _to_float(_quote_value(quote, "ask"), 0.0)

    if bid > 0 and ask > 0:
        return round((bid + ask) / 2.0, 6), "bid_ask_mid"

    if bid > 0:
        return bid, "bid"

    if ask > 0:
        return ask, "ask"

    return None, None


def _pick_rtd_option_price(quote: Any | None) -> float | None:
    """
    Escolhe o melhor preço disponível em rtd_option_quotes.

    Mantém a API anterior retornando apenas o preço. Para rastreabilidade
    completa, usar _pick_rtd_option_price_with_trace.
    """
    price, _field = _pick_rtd_option_price_with_trace(quote)
    return price


def _normalize_asset_code(value: Any) -> str:
    """Normaliza código de ativo para comparação operacional."""
    if value is None:
        return ""

    return str(value).strip().upper()


def _rtd_quote_traceability(
    quote: Any | None,
    *,
    rtd_quote_found: bool,
    price_resolution_status: str,
    rtd_validation_status: str,
    rtd_validation_message: str | None,
    rtd_price_field: str | None = None,
) -> dict[str, Any]:
    """Monta metadados de guardrail/diagnóstico RTD."""
    traceability: dict[str, Any] = {
        "price_resolution_status": price_resolution_status,
        "rtd_quote_found": rtd_quote_found,
        "rtd_validation_status": rtd_validation_status,
        "rtd_validation_message": rtd_validation_message,
    }

    if rtd_price_field:
        traceability["rtd_price_field"] = rtd_price_field

    if quote is not None:
        traceability.update(
            {
                "rtd_quote_codigo_opcao": _quote_value(quote, "codigo_opcao"),
                "rtd_quote_ativo_base": _quote_value(quote, "ativo_base"),
                "rtd_price_source": _quote_value(quote, "source"),
                "rtd_price_updated_at": _quote_value(quote, "updated_at"),
                "rtd_price_created_at": _quote_value(quote, "created_at"),
            }
        )

    return traceability


def _lookup_rtd_option_quote(
    repository: RtdOptionQuotesRepository,
    raw_asset: Any,
) -> Any | None:
    """
    Busca cotação RTD da opção por código.

    Tenta métodos comuns do repository sem quebrar o fluxo caso a API varie.
    """
    if not raw_asset:
        return None

    codigo_original = str(raw_asset).strip()
    if not codigo_original:
        return None

    codigos = []
    for codigo in (codigo_original, codigo_original.upper()):
        if codigo and codigo not in codigos:
            codigos.append(codigo)

    method_names = (
        "get_by_codigo",
        "get_by_codigo_opcao",
        "get_latest_by_codigo",
        "find_by_codigo",
        "find_by_codigo_opcao",
    )

    for codigo in codigos:
        for method_name in method_names:
            method = getattr(repository, method_name, None)
            if method is None:
                continue

            try:
                quote = method(codigo)
            except Exception:
                quote = None

            if quote:
                return quote

    return None


def _resolve_effective_leg_price(
    *,
    raw_price: Any,
    raw_asset: Any,
    leg_source: Any,
    rtd_option_quotes_repository: RtdOptionQuotesRepository | None,
    underlying_asset: Any | None = None,
) -> tuple[float, str, dict[str, Any]]:
    """
    Resolve preço efetivo da leg para o pricing_payload.

    Regra conservadora:
      manual explícito > rtd_option_quotes > preço original do snapshot.

    Retorna:
      (preço efetivo, origem do preço, metadados de rastreabilidade)
    """
    original_price = _to_float(raw_price, 0.0)

    if _is_manual_source(leg_source) and original_price > 0:
        return (
            original_price,
            "manual",
            {
                "price_resolution_status": "ok",
                "rtd_quote_found": None,
                "rtd_validation_status": "not_applicable",
                "rtd_validation_message": "Preço manual explícito preservado; RTD não consultado.",
            },
        )

    if rtd_option_quotes_repository is not None:
        quote = _lookup_rtd_option_quote(
            repository=rtd_option_quotes_repository,
            raw_asset=raw_asset,
        )

        if not quote:
            fallback_source = "snapshot" if original_price > 0 else "missing"
            return (
                original_price,
                fallback_source,
                _rtd_quote_traceability(
                    None,
                    rtd_quote_found=False,
                    price_resolution_status="missing_rtd_quote",
                    rtd_validation_status="error",
                    rtd_validation_message=(
                        f"Quote RTD não encontrada para a opção {raw_asset}."
                    ),
                ),
            )

        quote_ativo_base = _normalize_asset_code(_quote_value(quote, "ativo_base"))
        expected_ativo_base = _normalize_asset_code(underlying_asset)

        if quote_ativo_base and expected_ativo_base and quote_ativo_base != expected_ativo_base:
            fallback_source = "snapshot" if original_price > 0 else "missing"
            return (
                original_price,
                fallback_source,
                _rtd_quote_traceability(
                    quote,
                    rtd_quote_found=True,
                    price_resolution_status="rtd_asset_mismatch",
                    rtd_validation_status="error",
                    rtd_validation_message=(
                        "Ativo base da quote RTD diverge do ativo base da estrutura: "
                        f"quote={quote_ativo_base}, estrutura={expected_ativo_base}."
                    ),
                ),
            )

        rtd_price, rtd_price_field = _pick_rtd_option_price_with_trace(quote)

        if rtd_price is not None and rtd_price > 0:
            return (
                rtd_price,
                "rtd_option_quotes",
                _rtd_quote_traceability(
                    quote,
                    rtd_quote_found=True,
                    price_resolution_status="ok",
                    rtd_validation_status="ok",
                    rtd_validation_message=None,
                    rtd_price_field=rtd_price_field,
                ),
            )

        fallback_source = "snapshot" if original_price > 0 else "missing"
        return (
            original_price,
            fallback_source,
            _rtd_quote_traceability(
                quote,
                rtd_quote_found=True,
                price_resolution_status="invalid_rtd_price",
                rtd_validation_status="error",
                rtd_validation_message=(
                    f"Quote RTD encontrada para {raw_asset}, mas sem preço utilizável."
                ),
            ),
        )

    fallback_source = "snapshot" if original_price > 0 else "missing"
    fallback_status = "ok" if original_price > 0 else "missing_price"

    return (
        original_price,
        fallback_source,
        {
            "price_resolution_status": fallback_status,
            "rtd_quote_found": None,
            "rtd_validation_status": "not_applicable",
            "rtd_validation_message": "Repository RTD não disponível para consulta.",
        },
    )


def _lookup_spot_price(db_path: Path, underlying_asset: str) -> float:
    """
    Procura spot positivo no app.db.

    Caso confirmado:
      estrutura SMAL11 possui spot positivo disponível na base canônica/staging.
      spot observado = 124.66
    """
    if not underlying_asset:
        return 0.0

    symbol_candidates = {
        "aba",
        "ativo",
        "asset",
        "symbol",
        "ticker",
        "underlying_asset",
        "codigo",
        "papel",
    }

    price_candidates = {
        "spot",
        "spot_price",
        "underlying_price",
        "last_price",
        "price",
        "preco",
        "preco_atual",
        "valor",
        "cotacao",
        "ultimo",
        "fechamento",
        "close",
    }

    try:
        with sqlite3.connect(str(db_path)) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()

            for (table_name,) in tables:
                columns_info = conn.execute(
                    f"PRAGMA table_info({_quote_ident(table_name)})"
                ).fetchall()

                columns = [row[1] for row in columns_info]
                lower_to_real = {col.lower(): col for col in columns}

                symbol_cols = [
                    lower_to_real[name]
                    for name in symbol_candidates
                    if name in lower_to_real
                ]

                price_cols = [
                    lower_to_real[name]
                    for name in price_candidates
                    if name in lower_to_real
                ]

                if not symbol_cols or not price_cols:
                    continue

                for symbol_col in symbol_cols:
                    for price_col in price_cols:
                        query = (
                            f"SELECT {_quote_ident(price_col)} "
                            f"FROM {_quote_ident(table_name)} "
                            f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = UPPER(?) "
                            f"AND {_quote_ident(price_col)} IS NOT NULL "
                            f"LIMIT 20"
                        )

                        try:
                            rows = conn.execute(query, (underlying_asset,)).fetchall()
                        except Exception:
                            continue

                        for row in rows:
                            price = _to_float(row[0], 0.0)
                            if price > 0:
                                return price
    except Exception:
        return 0.0

    return 0.0


def _snapshot_result_to_payload(
    selection_result: Any,
    structure_id: int,
    underlying_asset: str,
    reference_date: str | None,
    db_path: Path,
    rtd_option_quotes_repository: RtdOptionQuotesRepository | None = None,
) -> dict[str, Any]:
    legs_data = []

    for leg in selection_result.legs:
        d = leg if isinstance(leg, dict) else vars(leg)

        quantity = _to_float(_pick(d, "quantity", "quant"), 0.0)

        raw_price = _pick(d, "premium", "price", "valor_executado")
        raw_asset = _pick(d, "symbol", "asset", "ativo")
        raw_expiry = _pick(d, "expiration_date", "expiry", "vencimento")
        leg_source = _pick(d, "source")

        effective_price, price_source, price_traceability = _resolve_effective_leg_price(
            raw_price=raw_price,
            raw_asset=raw_asset,
            leg_source=leg_source,
            rtd_option_quotes_repository=rtd_option_quotes_repository,
            underlying_asset=underlying_asset,
        )

        side = _pick(d, "side", "position_side")
        if not side:
            side = "SHORT" if quantity < 0 else "LONG"

        canonical_leg = {
            # campos originais/compatíveis
            "quantity":    quantity,
            "price":       effective_price,
            "asset":       raw_asset,
            "option_type": _pick(d, "option_type", "call_put"),
            "strike":      _to_float(_pick(d, "strike"), 0.0),
            "expiry":      raw_expiry,
            "iv":          _pick(d, "iv"),
            "delta":       _pick(d, "delta"),
            "gamma":       _pick(d, "gamma"),
            "theta":       _pick(d, "theta"),
            "vega":        _pick(d, "vega"),
            "source":      str(_pick(d, "source")),
            "price_source": price_source,

            # campos canônicos esperados pelo fluxo pricing/payoff
            "symbol":          raw_asset,
            "premium":         effective_price,
            "expiration_date": _normalize_expiration_date(raw_expiry),
            "multiplier":      1.0,
            "side":            str(side).upper(),
            "position_side":   str(side).upper(),
        }

        canonical_leg.update(
            {
                key: value
                for key, value in price_traceability.items()
                if value != ""
            }
        )

        legs_data.append(canonical_leg)

    spot = (
        getattr(selection_result, "spot_price", None)
        or getattr(selection_result, "spot", None)
        or getattr(selection_result, "underlying_price", None)
        or getattr(selection_result, "last_price", None)
    )

    spot_price = _to_float(spot, 0.0)

    if spot_price <= 0:
        spot_price = _lookup_spot_price(
            db_path=db_path,
            underlying_asset=underlying_asset,
        )

    if spot_price <= 0:
        raise ValueError(
            f"spot_price inválido ou ausente para underlying_asset={underlying_asset}. "
            "Não persistir execução OK com spot_price <= 0."
        )

    return {
        "structure_id":     structure_id,
        "underlying_asset": underlying_asset,
        "reference_date":   reference_date,
        "spot_price":       spot_price,
        "interest_rate":    0.0,
        "volatility":       0.0,
        "legs":             legs_data,
        "meta": {
            "snapshot_source":  str(selection_result.source),
            "snapshot_aba":     selection_result.aba,
            "manual_overrides": getattr(selection_result, "manual_overrides", None) or [],
            "legs_count":       len(legs_data),
        },
    }


class CanonicalPricingFacade:
    """
    Orquestra o pipeline canônico ponta a ponta:

        structure_id
             alias_legacy_aba + underlying_asset  (query em structures)
                     MarketSnapshotSelector.select(aba=...)
                             pricing_payload  (underlying_asset = ativo real)
                                     PricingExecutionService.execute_payload()
                                             PricingExecutionPersistenceService.persist()
                                                     DerivedPayoffPersistence.persist()
                                                             derived.db
    """

    def __init__(
        self,
        db_path: Path | str = _DEFAULT_DB,
        pricing_execution_service: PricingExecutionService | None = None,
        persistence_service: PricingExecutionPersistenceService | None = None,
    ) -> None:
        self._db_path  = Path(db_path)
        self._repo     = MarketSnapshotRepository(db_path=self._db_path)
        self._selector = MarketSnapshotSelector(repository=self._repo)
        self._rtd_option_quotes_db_path = _resolve_rtd_option_quotes_db_path(self._db_path)
        self._rtd_option_quotes_repository = RtdOptionQuotesRepository(
            db_path=self._rtd_option_quotes_db_path,
        )
        self._engine   = pricing_execution_service or PricingExecutionService()

        self._persister = persistence_service or PricingExecutionPersistenceService(
            payoff_persistence_port=DerivedPayoffPersistence(),
            system_snapshots_repository=SystemSnapshotsRepository(db_path=self._db_path),
        )

    def execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        started_at = time.perf_counter()

        try:
            #  1. Resolve aba + underlying_asset 
            aba, underlying_asset = _get_structure_info(   #  C6/C8
                structure_id, self._db_path
            )

            #  2. Seleciona snapshot (manual > rtd) 
            selection = self._selector.select(aba=aba)

            #  3. Monta pricing_payload 
            pricing_payload = _snapshot_result_to_payload(
                selection_result=selection,
                structure_id=structure_id,
                underlying_asset=underlying_asset,          #  C7/C8
                reference_date=reference_date,
                db_path=self._db_path,
                rtd_option_quotes_repository=self._rtd_option_quotes_repository,
            )

            #  4. Executa engine 
            execution_result = self._engine.execute_payload(
                pricing_payload=pricing_payload,
            )

            #  C4: extrai dict interno do wrapper 
            engine_result = execution_result.get("result", execution_result)

            duration_ms = int((time.perf_counter() - started_at) * 1000)

            #  5. Persiste (app.db + derived.db via port) 
            persisted = self._persister.persist_execution(
                pricing_payload=pricing_payload,
                result=engine_result,
                duration_ms=duration_ms,
                error_message=None,
            )

            return {
                "status":          "ok",
                "canonical_input": pricing_payload,
                "pricing_payload": pricing_payload,
                "result":          execution_result,
                "persisted":       persisted,
                "meta":            pricing_payload["meta"],
                "duration_ms":     duration_ms,
            }

        except Exception as exc:
            duration_ms   = int((time.perf_counter() - started_at) * 1000)
            error_message = str(exc)

            try:
                self._persister.persist_execution(
                    pricing_payload=None,
                    result={"engine": "stub", "status": "error", "error_message": error_message},
                    duration_ms=duration_ms,
                    error_message=error_message,
                )
            except Exception:
                pass

            return {
                "status":          "error",
                "canonical_input": None,
                "pricing_payload": None,
                "result":          None,
                "persisted":       None,
                "meta":            {},
                "duration_ms":     duration_ms,
                "error_message":   error_message,
            }
