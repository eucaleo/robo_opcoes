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
from repositories.system_snapshots_repository import SystemSnapshotsRepository
from services.derived_payoff_persistence import DerivedPayoffPersistence
from services.market_snapshot_selector import MarketSnapshotSelector
from services.pricing_execution_persistence_service import PricingExecutionPersistenceService
from services.pricing_execution_service import PricingExecutionService
from services.pricing_input_service import PricingInputService

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
            if not text:
                return default

            text = text.replace("R$", "").replace("$", "").strip()

            # Remove espaços internos comuns em valores monetários.
            text = text.replace(" ", "")

            # Formatos comuns vindos de RTD/planilha:
            #   BR: "1.234,56" -> "1234.56"
            #   US: "1,234.56" -> "1234.56"
            #   BR simples: "124,66" -> "124.66"
            if "," in text and "." in text:
                if text.rfind(",") > text.rfind("."):
                    text = text.replace(".", "").replace(",", ".")
                else:
                    text = text.replace(",", "")
            elif "," in text:
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


def _lookup_spot_price(db_path: Path, underlying_asset: str) -> float:
    """
    Procura spot positivo no app.db.

    Fonte prioritaria:
      rtd_underlying_quotes.ultimo_preco

    Motivo:
      A busca generica pode encontrar valores antigos em tabelas auxiliares.
      Para ativos base, a fonte autoritativa atual e rtd_underlying_quotes.
    """
    if not underlying_asset:
        return 0.0

    normalized_asset = str(underlying_asset).strip().upper()
    if not normalized_asset:
        return 0.0

    price_priority = [
        "ultimo_preco",
        "last_price",
        "spot_price",
        "spot",
        "underlying_price",
        "close_price",
        "prev_close",
        "bid",
        "ask",
        "price",
        "preco",
        "preco_atual",
        "cotacao",
        "ultimo",
        "fechamento",
        "close",
    ]

    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row

            # 1. Fonte autoritativa RTD para ativo base
            try:
                rtd_columns_info = conn.execute(
                    'PRAGMA table_info("rtd_underlying_quotes")'
                ).fetchall()

                rtd_lower_to_real = {
                    row[1].lower(): row[1]
                    for row in rtd_columns_info
                }

                if "ativo" in rtd_lower_to_real:
                    available_price_cols = [
                        name
                        for name in price_priority
                        if name in rtd_lower_to_real
                    ]

                    if available_price_cols:
                        select_expr = ", ".join(
                            _quote_ident(rtd_lower_to_real[name])
                            for name in available_price_cols
                        )

                        order_parts = []
                        if "updated_at" in rtd_lower_to_real:
                            order_parts.append(
                                f'{_quote_ident(rtd_lower_to_real["updated_at"])} DESC'
                            )
                        if "id" in rtd_lower_to_real:
                            order_parts.append(
                                f'{_quote_ident(rtd_lower_to_real["id"])} DESC'
                            )

                        order_clause = (
                            " ORDER BY " + ", ".join(order_parts)
                            if order_parts
                            else ""
                        )

                        query = (
                            f"SELECT {select_expr} "
                            f"FROM {_quote_ident('rtd_underlying_quotes')} "
                            f"WHERE UPPER(CAST({_quote_ident(rtd_lower_to_real['ativo'])} AS TEXT)) = ?"
                            f"{order_clause} "
                            f"LIMIT 1"
                        )

                        row = conn.execute(query, (normalized_asset,)).fetchone()

                        if row is not None:
                            for logical_name in available_price_cols:
                                real_name = rtd_lower_to_real[logical_name]
                                price = _to_float(row[real_name], 0.0)
                                if price > 0:
                                    return price
            except Exception:
                pass

            # 2. Fallback generico legado
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

            price_candidates = set(price_priority)

            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()

            for table_row in tables:
                table_name = table_row[0]

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
                            f"WHERE UPPER(CAST({_quote_ident(symbol_col)} AS TEXT)) = ? "
                            f"AND {_quote_ident(price_col)} IS NOT NULL "
                            f"LIMIT 20"
                        )

                        try:
                            rows = conn.execute(query, (normalized_asset,)).fetchall()
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
) -> dict[str, Any]:
    legs_data = []

    for leg in selection_result.legs:
        d = leg if isinstance(leg, dict) else vars(leg)

        quantity = _to_float(_pick(d, "quantity", "quant"), 0.0)

        raw_price = _pick(d, "premium", "price", "valor_executado")
        raw_asset = _pick(d, "symbol", "asset", "ativo")
        raw_expiry = _pick(d, "expiration_date", "expiry", "vencimento")

        side = _pick(d, "side", "position_side")
        if not side:
            side = "SHORT" if quantity < 0 else "LONG"

        canonical_leg = {
            # campos originais/compatíveis
            "quantity":    quantity,
            "price":       _to_float(raw_price, 0.0),
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

            # campos canônicos esperados pelo fluxo pricing/payoff
            "symbol":          raw_asset,
            "premium":         _to_float(raw_price, 0.0),
            "expiration_date": _normalize_expiration_date(raw_expiry),
            "multiplier":      1.0,
            "side":            str(side).upper(),
            "position_side":   str(side).upper(),
        }

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
            # 1. Monta pricing_payload.
            #
            # Caminho A - legado/captura:
            #   structures.alias_legacy_aba preenchido -> MarketSnapshotSelector.
            #
            # Caminho B - manual canônico:
            #   structures.alias_legacy_aba NULL -> PricingInputService.build_pricing_payload().
            #
            # O caminho B corrige estruturas cadastradas manualmente pela UI.
            try:
                aba, underlying_asset = _get_structure_info(
                    structure_id,
                    self._db_path,
                )

                selection = self._selector.select(aba=aba)

                pricing_payload = _snapshot_result_to_payload(
                    selection_result=selection,
                    structure_id=structure_id,
                    underlying_asset=underlying_asset,
                    reference_date=reference_date,
                    db_path=self._db_path,
                )

            except ValueError as exc:
                message = str(exc)

                if "alias_legacy_aba is null" not in message:
                    raise

                try:
                    pricing_input_service = PricingInputService(db_path=self._db_path)
                except TypeError:
                    pricing_input_service = PricingInputService()

                try:
                    pricing_payload = pricing_input_service.build_pricing_payload(
                        structure_id=structure_id,
                        reference_date=reference_date,
                    )
                except TypeError:
                    pricing_payload = pricing_input_service.build_pricing_payload(
                        structure_id=structure_id,
                    )

                if not isinstance(pricing_payload, dict):
                    raise ValueError(
                        "PricingInputService.build_pricing_payload() retornou payload inválido"
                    )

                pricing_payload.setdefault("structure_id", structure_id)

                if reference_date is not None:
                    pricing_payload.setdefault("reference_date", reference_date)

                meta = pricing_payload.get("meta")
                if not isinstance(meta, dict):
                    meta = {}
                    pricing_payload["meta"] = meta

                meta.setdefault("snapshot_source", "canonical_manual_without_alias")
                meta.setdefault("alias_legacy_aba", None)
                meta.setdefault("fallback_reason", message.strip())

            # 2. Executa engine
            execution_result = self._engine.execute_payload(
                pricing_payload=pricing_payload,
            )

            # C4: extrai dict interno do wrapper
            engine_result = execution_result.get("result", execution_result)

            duration_ms = int((time.perf_counter() - started_at) * 1000)

            # 3. Persiste app.db + derived.db via port
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
                "meta":            pricing_payload.get("meta", {}),
                "duration_ms":     duration_ms,
            }

        except Exception as exc:
            duration_ms   = int((time.perf_counter() - started_at) * 1000)
            error_message = str(exc)

            try:
                self._persister.persist_execution(
                    pricing_payload=None,
                    result={"engine": "payoff_pricing_engine", "status": "error", "error_message": error_message},
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
