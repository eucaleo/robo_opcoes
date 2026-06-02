# services/canonical_pricing_facade.py
"""
patch_17 — Fachada canônica corrigida.
patch_21 — Wiring do PayoffPersistencePort (DerivedPayoffPersistence) injetado
           no PricingExecutionPersistenceService.

Correções aplicadas:
  C1: sel.select(aba=...) — parâmetro correto
  C2: alias_legacy_aba buscado via MarketSnapshotRepository antes de chamar o selector
  C3: orquestração direta repo → selector → execute_payload(), sem depender de
      CanonicalInputService.build_structure_market_input() (assinatura não confirmada)
  C4: engine_result extraído do wrapper do engine antes de passar ao persister
      execution_result = { "pricing_payload": ..., "result": { engine, status, metrics... } }
      engine_result    = execution_result.get("result", execution_result)
  C5 (patch_21): DerivedPayoffPersistence injetado como payoff_persistence_port —
      após persist_execution, payoff + decisão são gravados no derived.db
      de forma fire-and-forget (falha não derruba a execução principal).
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


def _get_alias_legacy_aba(structure_id: int, db_path: Path) -> str:
    """
    Busca alias_legacy_aba direto no banco.
    Lança ValueError se a estrutura não existir ou aba for nula.
    """
    with sqlite3.connect(str(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT alias_legacy_aba FROM structures WHERE id = ?",
            (structure_id,),
        ).fetchone()

    if row is None:
        raise ValueError(f"structure not found: {structure_id}")

    aba = row["alias_legacy_aba"]
    if not aba:
        raise ValueError(f"alias_legacy_aba is null for structure_id={structure_id}")

    return aba


def _snapshot_result_to_payload(
    selection_result: Any,
    structure_id: int,
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

    # spot_price: tenta no selection_result, senão pega do primeiro leg como fallback
    spot = getattr(selection_result, "spot_price", None) \
        or getattr(selection_result, "spot", None)

    return {
        "structure_id":     structure_id,
        "underlying_asset": selection_result.aba,
        "reference_date":   reference_date,
        "spot_price":       float(spot) if spot else 0.0,
        "interest_rate":    0.0,
        "volatility":       0.0,
        "legs":             legs_data,
        "meta": {
            "snapshot_source":  str(selection_result.source),
            "manual_overrides": getattr(selection_result, "manual_overrides", None),
            "legs_count":       len(legs_data),
        },
    }


class CanonicalPricingFacade:
    """
    Orquestra o pipeline canônico ponta a ponta:

        structure_id
            └─► alias_legacy_aba  (query em structures)
                    └─► MarketSnapshotSelector.select(aba=...)
                            └─► pricing_payload
                                    └─► PricingExecutionService.execute_payload()
                                            └─► PricingExecutionPersistenceService.persist()
                                                    └─► DerivedPayoffPersistence.persist()  ← patch_21
                                                            └─► derived.db (payoff + decisão)
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

        # patch_21: injeta DerivedPayoffPersistence se nenhum persister for fornecido
        self._persister = persistence_service or PricingExecutionPersistenceService(
            payoff_persistence_port=DerivedPayoffPersistence(),
        )

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def execute_pricing(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        """
        Executa o pipeline canônico completo.

        Returns dict:
            status          "ok" | "error"
            canonical_input payload montado
            pricing_payload idem (alias semântico)
            result          saída do engine (wrapper completo)
            persisted       registro persistido
            meta            snapshot_source, overrides, legs_count
            duration_ms     tempo total
            error_message   presente apenas se status="error"
        """
        started_at = time.perf_counter()

        try:
            # ── 1. Resolve aba ─────────────────────────────────────────────
            aba = _get_alias_legacy_aba(structure_id, self._db_path)

            # ── 2. Seleciona snapshot (manual > rtd) ───────────────────────
            selection = self._selector.select(aba=aba)

            # ── 3. Monta pricing_payload ───────────────────────────────────
            pricing_payload = _snapshot_result_to_payload(
                selection_result=selection,
                structure_id=structure_id,
                reference_date=reference_date,
            )

            # ── 4. Executa engine ──────────────────────────────────────────
            execution_result = self._engine.execute_payload(
                pricing_payload=pricing_payload,
            )

            # ── C4: extrai dict interno do wrapper antes de passar ao persister
            # execution_result: { "pricing_payload": ..., "result": { engine, status, metrics, valuation } }
            engine_result = execution_result.get("result", execution_result)

            duration_ms = int((time.perf_counter() - started_at) * 1000)

            # ── 5. Persiste (app.db) + derived.db via port (patch_21) ──────
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
                "result":          execution_result,   # wrapper completo na resposta pública
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
