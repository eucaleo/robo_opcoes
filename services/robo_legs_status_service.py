from __future__ import annotations
"""
patch_57c -- RoboLegsStatusService.
  - from __future__ garantido como linha 1
"""

from src.domain.refs.structure_ref import StructureRef

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from dto.robo_leg_dto import FonteType
from dto.robo_legs_status_dto import DataFreshness, RoboLegsStatusDTO
from repositories.robo_legs_repository import RoboLegsRepository
from repositories.robo_legs_status_repository import RoboLegsStatusRepository, RoboLegsStatusRepoConfig
from utils.leg_normalizers import parse_timestamp
from validators.timestamp_validator import validate_ttl


@dataclass(frozen=True)
class RoboLegsFreshnessConfig:
    default_ttl_seconds: int = 120


class RoboLegsStatusService:
    def __init__(
        self,
        repo: Optional[RoboLegsRepository] = None,
        status_repo: Optional[RoboLegsStatusRepository] = None,
        freshness: Optional[RoboLegsFreshnessConfig] = None,
    ):
        self.repo = repo or RoboLegsRepository()
        self.status_repo = status_repo or RoboLegsStatusRepository(RoboLegsStatusRepoConfig())
        self.freshness = freshness or RoboLegsFreshnessConfig()

# services/robo_legs_status_service.py
# SUBSTITUA o método status() inteiro por este:

    def status(self, ref: StructureRef, requested_timestamp: object, ttl_seconds: Optional[int] = None) -> RoboLegsStatusDTO:
        requested_ts = parse_timestamp(requested_timestamp)
        ttl = timedelta(seconds=ttl_seconds if ttl_seconds is not None else self.freshness.default_ttl_seconds)
        validate_ttl(ttl)

        # patch_57c: extrair aba de ref (StructureRef ou str direto)
        if isinstance(ref, str):
            aba = ref
        else:
            aba = getattr(ref, "aba", None) or str(ref)

        manual_latest, rtd_latest = self.status_repo.latest_timestamps(ref=ref)

        if manual_latest is not None:
            chosen_fonte = FonteType.MANUAL
            chosen_ts = manual_latest
        elif rtd_latest is not None:
            chosen_fonte = FonteType.RTD
            chosen_ts = rtd_latest
        else:
            return RoboLegsStatusDTO(
                aba=aba,
                requested_ts=requested_ts,
                ttl=ttl,
                chosen_fonte=None,
                chosen_ts=None,
                manual_latest_ts=None,
                rtd_latest_ts=None,
                freshness=DataFreshness.MISSING,
                reason="no_data_for_aba",
            )

        delta = requested_ts - chosen_ts

        if delta <= ttl:
            freshness = DataFreshness.FRESH
            reason = "within_ttl"
        else:
            freshness = DataFreshness.STALE
            reason = "older_than_ttl"

        return RoboLegsStatusDTO(
            aba=aba,
            requested_ts=requested_ts,
            ttl=ttl,
            chosen_fonte=chosen_fonte,
            chosen_ts=chosen_ts,
            manual_latest_ts=manual_latest,
            rtd_latest_ts=rtd_latest,
            freshness=freshness,
            reason=reason,
        )
