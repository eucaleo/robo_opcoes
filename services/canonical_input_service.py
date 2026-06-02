# services/canonical_input_service.py
"""
patch_25 — Separa responsabilidades de resolução de snapshot:
  - _resolve_spot_and_rates  → MarketSnapshotProvider (spot, taxa, vol)
  - _resolve_legs            → MarketSnapshotSelector (manual > rtd por ativo)
  - _resolve_snapshot        → merge das duas fontes em contrato completo para o assembler

Contrato exigido pelo assemble_structure_market_input:
  {
    "reference_date":     str | None,
    "underlying_asset":   str,
    "spot_price":         float | None,
    "interest_rate":      float | None,
    "volatility":         float | None,
    "legs":               list[dict],   # campo extra, assembler ignora mas outros consomem
    "aba":                str | None,
  }
"""

from __future__ import annotations

from typing import Any

from repositories.structures_repository import StructuresRepository
from services.legacy_robo_legs_fallback import LegacyRoboLegsFallback
from services.market_snapshot_provider import MarketSnapshotProvider
from services.market_snapshot_selector import MarketSnapshotSelector
from services.structure_market_input_assembler import assemble_structure_market_input


class CanonicalInputService:
    def __init__(
        self,
        repository: StructuresRepository | None = None,
        market_snapshot_provider: MarketSnapshotProvider | None = None,
        market_snapshot_selector: MarketSnapshotSelector | None = None,
        robo_legs_service: Any | None = None,
        prefer_canonical_legs: bool = True,
        enable_legacy_legs_fallback: bool = True,
        allow_legacy_name_fallback: bool = False,
    ):
        self.repository                 = repository or StructuresRepository()
        self.market_snapshot_provider   = market_snapshot_provider or MarketSnapshotProvider()
        self.market_snapshot_selector   = market_snapshot_selector  # None = desabilitado
        self.prefer_canonical_legs      = prefer_canonical_legs
        self.enable_legacy_legs_fallback = enable_legacy_legs_fallback
        self.allow_legacy_name_fallback  = allow_legacy_name_fallback

        if robo_legs_service is not None:
            self.robo_legs_service = robo_legs_service
        else:
            try:
                from services.robo_legs_service import RoboLegsService
                self.robo_legs_service = RoboLegsService()
            except Exception:
                self.robo_legs_service = None

        self.legacy_robo_legs_fallback = LegacyRoboLegsFallback(
            robo_legs_service=self.robo_legs_service,
            allow_name_fallback=self.allow_legacy_name_fallback,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # API pública
    # ──────────────────────────────────────────────────────────────────────────

    def build_structure_market_input(
        self,
        structure_id: int,
        reference_date: str | None = None,
    ) -> dict[str, Any]:
        structure = self.repository.get_structure(structure_id)
        if structure is None:
            raise ValueError(f"structure not found: {structure_id}")

        structure = {
            **structure,
            "name":              self._clean_text(structure.get("name")),
            "underlying_asset":  self._clean_text(structure.get("underlying_asset")),
            "alias_legacy_aba":  self._clean_text(structure.get("alias_legacy_aba")),
        }

        snapshot, snapshot_meta = self._resolve_snapshot(
            structure=structure,
            reference_date=reference_date,
        )

        effective_reference_date = reference_date or snapshot.get("reference_date")

        enriched_structure, enrichment_meta = self._enrich_structure_with_legs(
            structure=structure,
            reference_date=effective_reference_date,
        )

        assembled       = assemble_structure_market_input(enriched_structure, snapshot)
        assembled_meta  = assembled.get("meta") or {}

        return {
            **assembled,
            "meta": {
                **assembled_meta,
                "reference_date": effective_reference_date,
                **enrichment_meta,
                **snapshot_meta,
            },
        }

    # ──────────────────────────────────────────────────────────────────────────
    # Resolução de snapshot — PATCH_25: duas responsabilidades separadas
    # ──────────────────────────────────────────────────────────────────────────

    def _resolve_snapshot(
        self,
        structure: dict[str, Any],
        reference_date: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Monta o snapshot dict completo exigido pelo assembler.

        Sempre busca spot/taxa/vol no MarketSnapshotProvider (fonte autoritativa).
        Se o selector estiver injetado E alias_legacy_aba existir, substitui as
        legs pelo resultado do selector (manual > rtd).
        """
        underlying_asset = structure["underlying_asset"]
        aba              = structure.get("alias_legacy_aba")

        # 1. Spot, taxa, vol — sempre via provider
        base_snapshot = self.market_snapshot_provider.get_snapshot(
            underlying_asset,
            reference_date=reference_date,
        )

        # 2. Legs — via selector se disponível, senão mantém o que o provider trouxe
        if self.market_snapshot_selector is not None and aba:
            legs_list, legs_meta = self._resolve_legs_via_selector(aba)
            snapshot_source = legs_meta["snapshot_source"]
        else:
            legs_list  = base_snapshot.get("legs", [])
            legs_meta  = {}
            snapshot_source = "provider_legacy"

        # 3. Monta contrato completo para o assembler
        snapshot = {
            **base_snapshot,            # reference_date, underlying_asset, spot_price,
                                        # interest_rate, volatility (e qualquer extra)
            "aba":  aba,
            "legs": legs_list,
        }

        meta = {
            "snapshot_source":  snapshot_source,
            **legs_meta,
        }

        return snapshot, meta

    # ──────────────────────────────────────────────────────────────────────────
    # Legs via selector (manual > rtd)
    # ──────────────────────────────────────────────────────────────────────────

    def _resolve_legs_via_selector(
        self,
        aba: str,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """
        Delega ao MarketSnapshotSelector e serializa legs completas.

        Serialização cobre todos os campos de LegMarketSnapshot para que
        consumidores downstream (pricing, greeks, payoff) tenham os dados.
        """
        result = self.market_snapshot_selector.select(aba)

        legs_as_dict = [
            {
                # ── identificação ──────────────────────────────────────────
                "aba":              leg.aba,
                "ativo":            leg.ativo,
                "source":           leg.source.value if hasattr(leg.source, "value") else str(leg.source),
                # ── posição ────────────────────────────────────────────────
                "cv":               leg.cv,
                "call_put":         leg.call_put,
                "quant":            leg.quant,
                "valor_executado":  leg.valor_executado,
                # ── preços ─────────────────────────────────────────────────
                "bid":              leg.bid,
                "ask":              leg.ask,
                "mid":              leg.mid,
                "spread":           leg.spread,
                "spread_pct":       leg.spread_pct,
                # ── greeks ─────────────────────────────────────────────────
                "iv":               leg.iv,
                "delta":            leg.delta,
                "gamma":            leg.gamma,
                "theta":            leg.theta,
                "vega":             leg.vega,
                # ── contrato ───────────────────────────────────────────────
                "strike":           leg.strike,
                "vencimento":       leg.vencimento,
                "dte":              leg.dte,
                "pl_realista":      leg.pl_realista,
                # ── auditoria ──────────────────────────────────────────────
                "timestamp":        leg.timestamp,
            }
            for leg in result.legs
        ]

        # reference_date derivada do timestamp da leg mais recente
        reference_date = self._reference_date_from_legs(result.legs)

        meta = {
            "snapshot_source":  result.source.value if hasattr(result.source, "value") else str(result.source),
            "snapshot_aba":     aba,
            "manual_overrides": result.manual_overrides,
            "is_manual_first":  result.is_manual_first,
            "legs_reference_date": reference_date,
        }

        return legs_as_dict, meta

    @staticmethod
    def _reference_date_from_legs(legs) -> str | None:
        """Extrai a data (YYYY-MM-DD) do timestamp mais recente entre as legs."""
        timestamps = [leg.timestamp for leg in legs if leg.timestamp]
        if not timestamps:
            return None
        latest = max(timestamps)          # ISO string → max() funciona diretamente
        return latest[:10]               # "YYYY-MM-DD HH:MM:SS" → "YYYY-MM-DD"

    # ──────────────────────────────────────────────────────────────────────────
    # Enriquecimento de legs canônicas / fallback (inalterado do patch_13)
    # ──────────────────────────────────────────────────────────────────────────

    def _build_meta(
        self,
        legs_source: str,
        legacy_timestamp: str | None = None,
        legacy_aba: str | None = None,
        legacy_key_source: str | None = None,
        fallback_reason: str | None = None,
    ) -> dict[str, Any]:
        meta: dict[str, Any] = {"legs_source": legs_source}
        if legacy_timestamp  is not None: meta["legacy_timestamp"]  = legacy_timestamp
        if legacy_aba        is not None: meta["legacy_aba"]        = legacy_aba
        if legacy_key_source is not None: meta["legacy_key_source"] = legacy_key_source
        if fallback_reason   is not None: meta["fallback_reason"]   = fallback_reason
        return meta

    def _base_legs_response(
        self,
        structure: dict[str, Any],
        existing_legs: list[dict[str, Any]],
        legs_source: str,
        fallback_reason: str | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        return (
            {**structure, "legs": existing_legs},
            self._build_meta(legs_source=legs_source, fallback_reason=fallback_reason),
        )

    def _enrich_structure_with_legs(
        self,
        structure: dict[str, Any],
        reference_date: str | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        existing_legs = structure.get("legs", []) or []

        if self.prefer_canonical_legs and existing_legs:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                legs_source="canonical",
            )

        if not self.enable_legacy_legs_fallback:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                legs_source="empty",
                fallback_reason="legacy_fallback_disabled",
            )

        fallback_legs, fallback_meta = self.legacy_robo_legs_fallback.load(
            structure=structure,
            reference_date=reference_date,
        )

        if fallback_legs:
            return (
                {**structure, "legs": fallback_legs},
                {
                    "legs_source":       fallback_meta.get("legs_source", "legacy_fallback"),
                    "legacy_timestamp":  fallback_meta.get("legacy_timestamp"),
                    "legacy_aba":        fallback_meta.get("legacy_aba"),
                    "legacy_key_source": fallback_meta.get("legacy_key_source"),
                    "fallback_reason":   fallback_meta.get("fallback_reason"),
                },
            )

        if existing_legs:
            return self._base_legs_response(
                structure=structure,
                existing_legs=existing_legs,
                legs_source="canonical",
                fallback_reason="canonical_legs_retained_after_empty_fallback",
            )

        return self._base_legs_response(
            structure=structure,
            existing_legs=existing_legs,
            legs_source="empty",
            fallback_reason=(
                fallback_meta.get("fallback_reason") if fallback_meta else "no_legs_available"
            ),
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Utilitários
    # ──────────────────────────────────────────────────────────────────────────

    def _clean_text(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value
