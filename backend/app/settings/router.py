from fastapi import APIRouter

router = APIRouter(
    tags=["settings"],
)


@router.get(
    "/settings/job-discovery",
)
def get_job_discovery_settings():
    return {
        "discovery_enabled": False,
        "discovery_interval_minutes": 1440,
        "discovery_connectors": [
            "france_travail",
        ],
    }