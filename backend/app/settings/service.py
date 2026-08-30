import json

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
                ApplicationSetting.setting_key
                == key
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
        commit: bool = True,
    ) -> None:
        setting = (
            self.db.query(ApplicationSetting)
            .filter(
                ApplicationSetting.setting_key
                == key
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

        if commit:
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

    def get_discovery_preferences_settings(
        self,
    ) -> dict:
        return {
            "discovery_age_window": self.get_value(
                "discovery_age_window",
                "30_DAYS",
            ),
            "discovery_minimum_matching_score": int(
                self.get_value(
                    "discovery_minimum_matching_score",
                    "25",
                )
            ),
            "discovery_show_archived": (
                self.get_value(
                    "discovery_show_archived",
                    "false",
                ).lower()
                == "true"
            ),
            "discovery_default_sort": self.get_value(
                "discovery_default_sort",
                "BEST_MATCH_FIRST",
            ),
        }

    def update_discovery_preferences_settings(
        self,
        payload: dict,
    ) -> None:
        self.set_value(
            "discovery_age_window",
            payload["discovery_age_window"],
        )

        self.set_value(
            "discovery_minimum_matching_score",
            str(
                payload[
                    "discovery_minimum_matching_score"
                ]
            ),
        )

        self.set_value(
            "discovery_show_archived",
            str(
                payload[
                    "discovery_show_archived"
                ]
            ).lower(),
        )

        self.set_value(
            "discovery_default_sort",
            payload["discovery_default_sort"],
        )

    def get_ai_settings(
        self,
    ) -> dict:
        ai_features_enabled = (
            self.get_value(
                "ai_features_enabled",
                "false",
            ).lower()
            == "true"
        )

        ai_consent_accepted = (
            self.get_value(
                "ai_consent_accepted",
                "false",
            ).lower()
            == "true"
        )

        if (
            ai_features_enabled
            and not ai_consent_accepted
        ):
            ai_features_enabled = False

        return {
            "ai_features_enabled": (
                ai_features_enabled
            ),
            "ai_consent_accepted": (
                ai_consent_accepted
            ),
        }

    def update_ai_settings(
        self,
        payload: dict,
    ) -> None:
        ai_features_enabled = payload[
            "ai_features_enabled"
        ]

        ai_consent_accepted = payload[
            "ai_consent_accepted"
        ]

        if (
            ai_features_enabled
            and not ai_consent_accepted
        ):
            raise ValueError(
                "AI consent must be accepted before AI features can be enabled."
            )

        if (
            not ai_features_enabled
            and ai_consent_accepted
        ):
            raise ValueError(
                "AI consent cannot remain accepted when AI features are disabled."
            )

        self.set_value(
            "ai_features_enabled",
            str(
                ai_features_enabled
            ).lower(),
            commit=False,
        )

        self.set_value(
            "ai_consent_accepted",
            str(
                ai_consent_accepted
            ).lower(),
            commit=False,
        )

        self.db.commit()

    def get_saved_searches(
        self,
    ) -> list[dict]:
        value = self.get_value(
            "saved_searches",
            "[]",
        )

        return json.loads(value)

    def create_saved_search(
        self,
        payload: dict,
    ) -> dict:
        searches = self.get_saved_searches()

        next_id = (
            max(
                [
                    search["id"]
                    for search in searches
                ],
                default=0,
            )
            + 1
        )

        saved_search = {
            "id": next_id,
            "name": payload["name"],
            "keyword": payload["keyword"],
            "application_status": payload[
                "application_status"
            ],
            "source": payload["source"],
            "location": payload["location"],
            "sort_by": payload["sort_by"],
        }

        searches.append(
            saved_search
        )

        self.set_value(
            "saved_searches",
            json.dumps(searches),
        )

        return saved_search

    def delete_saved_search(
        self,
        saved_search_id: int,
    ) -> dict:
        searches = self.get_saved_searches()

        search = next(
            (
                item
                for item in searches
                if item["id"]
                == saved_search_id
            ),
            None,
        )

        if search is None:
            raise ValueError(
                "Saved search not found."
            )

        searches = [
            item
            for item in searches
            if item["id"]
            != saved_search_id
        ]

        self.set_value(
            "saved_searches",
            json.dumps(searches),
        )

        return search