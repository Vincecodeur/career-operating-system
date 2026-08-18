from pydantic import BaseModel


class JobDiscoverySettingsResponse(
    BaseModel,
):
    discovery_enabled: bool

    discovery_interval_minutes: int

    discovery_connectors: list[str]


class JobDiscoverySettingsUpdate(
    BaseModel,
):
    discovery_enabled: bool

    discovery_interval_minutes: int

    discovery_connectors: list[str]