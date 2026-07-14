from datetime import datetime, timedelta

import pytest

from dto.robo_leg_dto import FonteType
from dto.robo_legs_status_dto import DataFreshness
from services.robo_legs_status_service import (
    RoboLegsFreshnessConfig,
    RoboLegsStatusService,
)


class DummyStatusRepo:
    def __init__(self, manual_latest=None, rtd_latest=None):
        self._manual_latest = manual_latest
        self._rtd_latest = rtd_latest
        self.last_aba = None

    def latest_timestamps(self, aba: str):
        self.last_aba = aba
        return self._manual_latest, self._rtd_latest


class DummyRepo:
    pass


def test_status_returns_missing_when_no_data():
    service = RoboLegsStatusService(
        repo=DummyRepo(),
        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=None),
        freshness=RoboLegsFreshnessConfig(default_ttl_seconds=120),
    )

    requested = datetime(2026, 5, 19, 10, 0, 0)
    result = service.status("TESTE", requested)

    assert result.aba == "TESTE"
    assert result.requested_ts == requested
    assert result.chosen_fonte is None
    assert result.chosen_ts is None
    assert result.manual_latest_ts is None
    assert result.rtd_latest_ts is None
    assert result.freshness == DataFreshness.MISSING
    assert result.reason == "no_data_for_aba"


def test_status_prefers_manual_when_manual_exists():
    manual_latest = datetime(2026, 5, 19, 10, 0, 0)
    rtd_latest = datetime(2026, 5, 19, 10, 1, 0)

    service = RoboLegsStatusService(
        repo=DummyRepo(),
        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=rtd_latest),
    )

    requested = datetime(2026, 5, 19, 10, 1, 30)
    result = service.status("ABAX", requested, ttl_seconds=120)

    assert result.chosen_fonte == FonteType.MANUAL
    assert result.chosen_ts == manual_latest
    assert result.manual_latest_ts == manual_latest
    assert result.rtd_latest_ts == rtd_latest
    assert result.freshness == DataFreshness.FRESH
    assert result.reason == "within_ttl"


def test_status_uses_rtd_when_manual_missing():
    rtd_latest = datetime(2026, 5, 19, 10, 0, 0)

    service = RoboLegsStatusService(
        repo=DummyRepo(),
        status_repo=DummyStatusRepo(manual_latest=None, rtd_latest=rtd_latest),
    )

    requested = datetime(2026, 5, 19, 10, 1, 0)
    result = service.status("ABAY", requested, ttl_seconds=120)

    assert result.chosen_fonte == FonteType.RTD
    assert result.chosen_ts == rtd_latest
    assert result.manual_latest_ts is None
    assert result.rtd_latest_ts == rtd_latest
    assert result.freshness == DataFreshness.FRESH
    assert result.reason == "within_ttl"


def test_status_returns_stale_when_delta_exceeds_ttl():
    manual_latest = datetime(2026, 5, 19, 10, 0, 0)

    service = RoboLegsStatusService(
        repo=DummyRepo(),
        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
    )

    requested = datetime(2026, 5, 19, 10, 5, 0)
    result = service.status("ABAZ", requested, ttl_seconds=60)

    assert result.chosen_fonte == FonteType.MANUAL
    assert result.freshness == DataFreshness.STALE
    assert result.reason == "older_than_ttl"


def test_status_future_timestamp_is_considered_fresh():
    manual_latest = datetime(2026, 5, 19, 10, 5, 0)

    service = RoboLegsStatusService(
        repo=DummyRepo(),
        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
    )

    requested = datetime(2026, 5, 19, 10, 0, 0)
    result = service.status("ABAF", requested, ttl_seconds=60)

    assert result.freshness == DataFreshness.FRESH
    assert result.reason == "within_ttl"


def test_status_uses_default_ttl_when_not_provided():
    manual_latest = datetime(2026, 5, 19, 10, 0, 0)

    service = RoboLegsStatusService(
        repo=DummyRepo(),
        status_repo=DummyStatusRepo(manual_latest=manual_latest, rtd_latest=None),
        freshness=RoboLegsFreshnessConfig(default_ttl_seconds=30),
    )

    requested = datetime(2026, 5, 19, 10, 0, 20)
    result = service.status("ABAD", requested)

    assert result.ttl == timedelta(seconds=30)
    assert result.freshness == DataFreshness.FRESH
