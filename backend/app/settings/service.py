from sqlalchemy.orm import Session

from app.settings.models import SavedSearch
from app.settings.models import UserSettings


class SettingsService:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def _get_or_create_user_settings(
        self,
        user_id: int,
    ) -> UserSettings:
        settings = (
            self.db.query(UserSettings)
            .filter(
                UserSettings.user_id == user_id
            )
            .first()
        )

        if settings is None:
            settings = UserSettings(
                user_id=user_id,
            )

            self.db.add(settings)
            self.db.commit()
            self.db.refresh(settings)

        return settings

    def get_job_discovery_settings(
        self,
        user_id: int,
    ) -> dict:
        settings = self._get_or_create_user_settings(
            user_id
        )

        return {
            "discovery_enabled": (
                settings.discovery_enabled
            ),
            "discovery_interval_minutes": (
                settings.discovery_interval_minutes
            ),
            "discovery_connectors": (
                settings.discovery_connectors
            ),
        }

    def update_job_discovery_settings(
        self,
        user_id: int,
        payload: dict,
    ) -> None:
        settings = self._get_or_create_user_settings(
            user_id
        )

        settings.discovery_enabled = payload[
            "discovery_enabled"
        ]
        settings.discovery_interval_minutes = payload[
            "discovery_interval_minutes"
        ]
        settings.discovery_connectors = payload[
            "discovery_connectors"
        ]

        self.db.commit()

    def get_search_criteria_settings(
        self,
        user_id: int,
    ) -> dict:
        settings = self._get_or_create_user_settings(
            user_id
        )

        return {
            "target_job_titles": (
                settings.search_target_job_titles
            ),
            "preferred_countries": (
                settings.search_preferred_countries
            ),
            "work_modes": (
                settings.search_work_modes
            ),
            "included_keywords": (
                settings.search_included_keywords
            ),
            "excluded_keywords": (
                settings.search_excluded_keywords
            ),
        }

    def update_search_criteria_settings(
        self,
        user_id: int,
        payload: dict,
    ) -> None:
        settings = self._get_or_create_user_settings(
            user_id
        )

        settings.search_target_job_titles = payload[
            "target_job_titles"
        ]
        settings.search_preferred_countries = payload[
            "preferred_countries"
        ]
        settings.search_work_modes = payload[
            "work_modes"
        ]
        settings.search_included_keywords = payload[
            "included_keywords"
        ]
        settings.search_excluded_keywords = payload[
            "excluded_keywords"
        ]

        self.db.commit()

    def get_discovery_preferences_settings(
        self,
        user_id: int,
    ) -> dict:
        settings = self._get_or_create_user_settings(
            user_id
        )

        return {
            "discovery_age_window": (
                settings.discovery_age_window
            ),
            "discovery_minimum_matching_score": (
                settings.discovery_minimum_matching_score
            ),
            "discovery_show_archived": (
                settings.discovery_show_archived
            ),
            "discovery_default_sort": (
                settings.discovery_default_sort
            ),
        }

    def update_discovery_preferences_settings(
        self,
        user_id: int,
        payload: dict,
    ) -> None:
        settings = self._get_or_create_user_settings(
            user_id
        )

        settings.discovery_age_window = payload[
            "discovery_age_window"
        ]
        settings.discovery_minimum_matching_score = payload[
            "discovery_minimum_matching_score"
        ]
        settings.discovery_show_archived = payload[
            "discovery_show_archived"
        ]
        settings.discovery_default_sort = payload[
            "discovery_default_sort"
        ]

        self.db.commit()

    def get_ai_settings(
        self,
        user_id: int,
    ) -> dict:
        settings = self._get_or_create_user_settings(
            user_id
        )

        ai_features_enabled = (
            settings.ai_features_enabled
        )
        ai_consent_accepted = (
            settings.ai_consent_accepted
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
        user_id: int,
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

        settings = self._get_or_create_user_settings(
            user_id
        )

        settings.ai_features_enabled = (
            ai_features_enabled
        )
        settings.ai_consent_accepted = (
            ai_consent_accepted
        )

        self.db.commit()

    def get_saved_searches(
        self,
        user_id: int,
    ) -> list[SavedSearch]:
        return (
            self.db.query(SavedSearch)
            .filter(
                SavedSearch.user_id == user_id
            )
            .order_by(
                SavedSearch.id.asc()
            )
            .all()
        )

    def create_saved_search(
        self,
        user_id: int,
        payload: dict,
    ) -> SavedSearch:
        saved_search = SavedSearch(
            user_id=user_id,
            name=payload["name"],
            keyword=payload["keyword"],
            application_status=payload[
                "application_status"
            ],
            source=payload["source"],
            location=payload["location"],
            sort_by=payload["sort_by"],
        )

        self.db.add(saved_search)
        self.db.commit()
        self.db.refresh(saved_search)

        return saved_search

    def delete_saved_search(
        self,
        user_id: int,
        saved_search_id: int,
    ) -> SavedSearch:
        saved_search = (
            self.db.query(SavedSearch)
            .filter(
                SavedSearch.id == saved_search_id,
                SavedSearch.user_id == user_id,
            )
            .first()
        )

        if saved_search is None:
            raise ValueError(
                "Saved search not found."
            )

        self.db.delete(saved_search)
        self.db.commit()

        return saved_search
