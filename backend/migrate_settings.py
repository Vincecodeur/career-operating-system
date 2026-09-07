from app.core.database import SessionLocal
from app.auth.models import User
from app.settings.models import UserSettings

db = SessionLocal()

TARGET_EMAIL = "maw282003@gmail.com"

user = db.query(User).filter(User.email == TARGET_EMAIL).first()

if user is None:
    print("ERREUR : utilisateur introuvable, migration annulee.")
else:
    existing = db.query(UserSettings).filter(UserSettings.user_id == user.id).first()

    if existing is not None:
        print("ATTENTION : une ligne UserSettings existe deja pour cet utilisateur, migration annulee pour eviter un doublon.")
    else:
        migrated_settings = UserSettings(
            user_id=user.id,
            discovery_enabled=True,
            discovery_interval_minutes=1440,
            discovery_connectors=["france_travail", "greenhouse"],
            search_target_job_titles=["Technical Partnerships Manager", "Solution Architect"],
            search_preferred_countries=["FR", "BE", "NL"],
            search_work_modes=["Remote", "Hybrid"],
            search_included_keywords=["API", "Integration", "oms"],
            search_excluded_keywords=["Internship"],
            discovery_age_window="30_DAYS",
            discovery_minimum_matching_score=0,
            discovery_show_archived=False,
            discovery_default_sort="BEST_MATCH_FIRST",
            ai_features_enabled=True,
            ai_consent_accepted=True,
        )

        db.add(migrated_settings)
        db.commit()

        print("Migration reussie pour user_id=", user.id)

db.close()
