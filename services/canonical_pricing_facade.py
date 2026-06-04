# services/canonical_pricing_facade.py
"""
patch_17 -- Fachada canônica corrigida.
patch_21 -- Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado
           no PricingExecutionPersistenceService.
patch_41 -- Corrige underlying_asset no pricing_payload.

Correções patch_41:
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
from pathlib import Path
from typing import Any

from repositories.market_snapshot_repository import MarketSnapshotRepository
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

def _snapshot_result_to_payload(
    selection_result: Any,
    structure_id: int,
    underlying_asset: str,          #  parâmetro novo (era implícito via .aba)
    reference_date: str | None,
) -> dict[str, Any]:
    legs_data = []
    for leg in selection_result.legs:
        d = leg if isinstance(leg, dict) else vars(leg)
        legs_data.append({
            "quantity":    d.get("quant"),
            "price":       d.get("valor_executado"),
            "asset":       d.get("ativo"),
            "option_type": d.get("call_put"),
            "strike":      d.get("strike"),
            "expiry":      d.get("vencimento"),
            "iv":          d.get("iv"),
            "delta":       d.get("delta"),
            "gamma":       d.get("gamma"),
            "theta":       d.get("theta"),
            "vega":        d.get("vega"),
            "source":      str(d.get("source")),
        })

    spot = getattr(selection_result, "spot_price", None) \
        or getattr(selection_result, "spot", None)

    return {
        "structure_id":     structure_id,
        "underlying_asset": underlying_asset,   #  C7: ativo real, não aba legada
        "reference_date":   reference_date,
        "spot_price":       float(spot) if spot else 0.0,
        "interest_rate":    0.0,
        "volatility":       0.0,
        "legs":             legs_data,
        "meta": {
            "snapshot_source":  str(selection_result.source),
            "snapshot_aba":     selection_result.aba,   #  preserva aba para rastreabilidade
            "manual_overrides": getattr(selection_result, "manual_overrides", None),
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
