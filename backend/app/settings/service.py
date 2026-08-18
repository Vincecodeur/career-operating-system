from sqlalchemy.orm import Session

from app.settings.models import ApplicationSetting


class SettingsService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_value(
        self,
        key: str,
        default: str,
    ) -> str:
        setting = (
            self.db.query(ApplicationSetting)
            .filter(
                ApplicationSetting.setting_key == key
            )
            .first()
        )

        if setting is None:
            return default

        return setting.setting_value

    def set_value(
        self,
        key: str,
        value: str,
    ) -> None:
        setting = (
            self.db.query(ApplicationSetting)
            .filter(
                ApplicationSetting.setting_key == key
            )
            .first()
        )

        if setting is None:
            setting = ApplicationSetting(
                setting_key=key,
                setting_value=value,
            )

            self.db.add(setting)
        else:
            setting.setting_value = value

        self.db.commit()

    def get_job_discovery_settings(
        self,
    ) -> dict:
        return {
            "discovery_enabled": (
                self.get_value(
                    "job_discovery_enabled",
                    "false",
                ).lower()
                == "true"
            ),
            "discovery_interval_minutes": int(
                self.get_value(
                    "job_discovery_interval_minutes",
                    "1440",
                )
            ),
            "discovery_connectors": [
                item.strip()
                for item in self.get_value(
                    "job_discovery_connectors",
                    "france_travail",
                ).split(",")
                if item.strip()
            ],
        }

    def update_job_discovery_settings(
        self,
        payload: dict,
    ) -> None:
        self.set_value(
            "job_discovery_enabled",
            str(
                payload["discovery_enabled"]
            ).lower(),
        )

        self.set_value(
            "job_discovery_interval_minutes",
            str(
                payload[
                    "discovery_interval_minutes"
                ]
            ),
        )

        self.set_value(
            "job_discovery_connectors",
            ",".join(
                payload[
                    "discovery_connectors"
                ]
            ),
        )
        
        
        
    def get_search_criteria_settings(
        self,
    ) -> dict:
        return {
            "target_job_titles": [
                item.strip()
                for item in self.get_value(
                    "search_target_job_titles",
                    "",
                ).split(",")
                if item.strip()
            ],
            "preferred_countries": [
                item.strip()
                for item in self.get_value(
                    "search_preferred_countries",
                    "",
                ).split(",")
                if item.strip()
            ],
            "work_modes": [
                item.strip()
                for item in self.get_value(
                    "search_work_modes",
                    "",
                ).split(",")
                if item.strip()
            ],
            "included_keywords": [
                item.strip()
                for item in self.get_value(
                    "search_included_keywords",
                    "",
                ).split(",")
                if item.strip()
            ],
            "excluded_keywords": [
                item.strip()
                for item in self.get_value(
                    "search_excluded_keywords",
                    "",
                ).split(",")
                if item.strip()
            ],
        }

    def update_search_criteria_settings(
        self,
        payload: dict,
    ) -> None:
        self.set_value(
            "search_target_job_titles",
            ",".join(
                payload["target_job_titles"]
            ),
        )

        self.set_value(
            "search_preferred_countries",
            ",".join(
                payload["preferred_countries"]
            ),
        )

        self.set_value(
            "search_work_modes",
            ",".join(
                payload["work_modes"]
            ),
        )

        self.set_value(
            "search_included_keywords",
            ",".join(
                payload["included_keywords"]
            ),
        )

        self.set_value(
            "search_excluded_keywords",
            ",".join(
                payload["excluded_keywords"]
            ),
        )