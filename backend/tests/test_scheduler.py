from app.jobs.scheduler import DiscoveryScheduler


class FakeQuery:
    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return None


class FakeDatabaseSession:
    def __init__(self):
        self.closed = False

    def query(self, *args, **kwargs):
        return FakeQuery()

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
        user_id: int | None = None,
    ) -> dict:
        self.calls.append(
            {
                "db": self.db,
                "connector_names": connector_names,
                "source_type": source_type,
                "user_id": user_id,
            }
        )

        return {
            "connectors_processed": len(connector_names),
            "connectors_skipped": 0,
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
        "connectors_skipped": 0,
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
    assert FakeDiscoveryService.calls[0]["user_id"] is None
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
    

def test_resolve_primary_user_id_returns_none_without_configured_email(
    monkeypatch,
):
    from app.core.settings import settings

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        "",
    )

    fake_db = FakeDatabaseSession()

    user_id = DiscoveryScheduler._resolve_primary_user_id(fake_db)

    assert user_id is None


def test_resolve_primary_user_id_returns_none_when_email_matches_no_user(
    monkeypatch,
):
    from app.core.settings import settings

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        "no-such-user@career-os.local",
    )

    fake_db = FakeDatabaseSession()

    user_id = DiscoveryScheduler._resolve_primary_user_id(fake_db)

    assert user_id is None


def test_resolve_primary_user_id_returns_real_user_id(monkeypatch):
    from app.auth.models import User
    from app.core.database import SessionLocal
    from app.core.settings import settings

    monkeypatch.setattr(
        settings,
        "PRIMARY_USER_EMAIL",
        "test-primary-user@career-os.local",
    )

    db = SessionLocal()

    try:
        expected_user = db.query(User).filter(
            User.email == "test-primary-user@career-os.local"
        ).first()

        user_id = DiscoveryScheduler._resolve_primary_user_id(db)

        assert user_id == expected_user.id
    finally:
        db.rollback()
        db.close()
        

class FakeSettingsServiceWithConnectors:
    def __init__(self, db):
        self.db = db

    def get_job_discovery_settings(self, user_id):
        return {
            "discovery_enabled": True,
            "discovery_interval_minutes": 1440,
            "discovery_connectors": [
                "france_travail",
                "linkedin_email",
            ],
        }


class FakeSettingsServiceWithoutConnectors:
    def __init__(self, db):
        self.db = db

    def get_job_discovery_settings(self, user_id):
        return {
            "discovery_enabled": True,
            "discovery_interval_minutes": 1440,
            "discovery_connectors": [],
        }


def test_run_once_resolves_connectors_from_user_settings_when_no_override_given(
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
    monkeypatch.setattr(
        "app.jobs.scheduler.SettingsService",
        FakeSettingsServiceWithConnectors,
    )
    monkeypatch.setattr(
        DiscoveryScheduler,
        "_resolve_primary_user_id",
        staticmethod(lambda db: 1),
    )

    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=1440,
        connector_names=None,
        session_factory=fake_session_factory,
    )

    scheduler.run_once()

    assert FakeDiscoveryService.calls[0]["connector_names"] == [
        "france_travail",
        "linkedin_email",
    ]


def test_run_once_falls_back_to_env_when_user_has_no_connectors_configured(
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
    monkeypatch.setattr(
        "app.jobs.scheduler.SettingsService",
        FakeSettingsServiceWithoutConnectors,
    )
    monkeypatch.setattr(
        DiscoveryScheduler,
        "_resolve_primary_user_id",
        staticmethod(lambda db: 1),
    )
    monkeypatch.setattr(
        "app.jobs.scheduler.settings.DISCOVERY_CONNECTORS",
        ["france_travail"],
    )

    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=1440,
        connector_names=None,
        session_factory=fake_session_factory,
    )

    scheduler.run_once()

    assert FakeDiscoveryService.calls[0]["connector_names"] == [
        "france_travail",
    ]


def test_run_once_falls_back_to_env_when_no_user_id_resolved(
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
    monkeypatch.setattr(
        DiscoveryScheduler,
        "_resolve_primary_user_id",
        staticmethod(lambda db: None),
    )
    monkeypatch.setattr(
        "app.jobs.scheduler.settings.DISCOVERY_CONNECTORS",
        ["greenhouse"],
    )

    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=1440,
        connector_names=None,
        session_factory=fake_session_factory,
    )

    scheduler.run_once()

    assert FakeDiscoveryService.calls[0]["connector_names"] == [
        "greenhouse",
    ]


def test_explicit_connector_names_override_bypasses_user_settings(
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
    monkeypatch.setattr(
        DiscoveryScheduler,
        "_resolve_primary_user_id",
        staticmethod(lambda db: 1),
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError(
            "SettingsService must not be instantiated when an "
            "explicit connector_names override is given."
        )

    monkeypatch.setattr(
        "app.jobs.scheduler.SettingsService",
        fail_if_called,
    )

    scheduler = DiscoveryScheduler(
        enabled=True,
        interval_minutes=1440,
        connector_names=["mock"],
        session_factory=fake_session_factory,
    )

    scheduler.run_once()

    assert FakeDiscoveryService.calls[0]["connector_names"] == [
        "mock",
    ]
