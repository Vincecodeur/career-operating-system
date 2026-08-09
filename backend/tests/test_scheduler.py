from app.jobs.scheduler import DiscoveryScheduler


class FakeDatabaseSession:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class FakeDiscoveryService:
    calls = []

    def __init__(
        self,
        db,
    ):
        self.db = db

    def import_from_connector_names(
        self,
        connector_names: list[str],
        source_type: str = "MANUAL",
    ) -> dict:
        self.calls.append(
            {
                "db": self.db,
                "connector_names": connector_names,
                "source_type": source_type,
            }
        )

        return {
            "connectors_processed": len(connector_names),
            "offers_fetched": 2,
            "offers_imported": 2,
            "results": [
                {
                    "connector_name": connector_names[0],
                    "source_name": "Fake Source",
                    "offers_fetched": 2,
                    "offers_imported": 2,
                }
            ],
        }


def test_scheduler_is_disabled_by_configuration():
    scheduler = DiscoveryScheduler(
        enabled=False,
        interval_minutes=1440,
        connector_names=[
            "france_travail",
        ],
    )

    assert scheduler.enabled is False


def test_scheduler_uses_configured_interval_minutes():
    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=15,
        connector_names=[
            "france_travail",
        ],
    )

    assert scheduler.interval_minutes == 15
    assert scheduler.interval_seconds == 900


def test_scheduler_enforces_minimum_interval_of_one_minute():
    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=0,
        connector_names=[
            "france_travail",
        ],
    )

    assert scheduler.interval_seconds == 60


def test_run_once_triggers_discovery_service(
    monkeypatch,
):
    FakeDiscoveryService.calls = []

    fake_db = FakeDatabaseSession()

    def fake_session_factory():
        return fake_db

    monkeypatch.setattr(
        "app.jobs.scheduler.DiscoveryService",
        FakeDiscoveryService,
    )

    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=1440,
        connector_names=[
            "france_travail",
        ],
        session_factory=fake_session_factory,
    )

    result = scheduler.run_once()

    assert result == {
        "connectors_processed": 1,
        "offers_fetched": 2,
        "offers_imported": 2,
        "results": [
            {
                "connector_name": "france_travail",
                "source_name": "Fake Source",
                "offers_fetched": 2,
                "offers_imported": 2,
            }
        ],
    }

    assert len(FakeDiscoveryService.calls) == 1
    assert FakeDiscoveryService.calls[0]["connector_names"] == [
        "france_travail",
    ]
    assert FakeDiscoveryService.calls[0]["source_type"] == "API"
    assert fake_db.closed is True


def test_run_once_supports_multiple_connectors(
    monkeypatch,
):
    FakeDiscoveryService.calls = []

    fake_db = FakeDatabaseSession()

    def fake_session_factory():
        return fake_db

    monkeypatch.setattr(
        "app.jobs.scheduler.DiscoveryService",
        FakeDiscoveryService,
    )

    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=1440,
        connector_names=[
            "france_travail",
            "mock",
        ],
        session_factory=fake_session_factory,
    )

    result = scheduler.run_once()

    assert result["connectors_processed"] == 2
    assert FakeDiscoveryService.calls[0]["connector_names"] == [
        "france_travail",
        "mock",
    ]
    assert fake_db.closed is True