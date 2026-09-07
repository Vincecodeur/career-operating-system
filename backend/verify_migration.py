from app.core.database import SessionLocal
from app.settings.models import UserSettings

db = SessionLocal()

all_settings = db.query(UserSettings).all()

print("Nombre de lignes UserSettings :", len(all_settings))

for s in all_settings:
    print("user_id=", s.user_id)
    print("  discovery_enabled=", s.discovery_enabled)
    print("  discovery_connectors=", s.discovery_connectors)
    print("  search_preferred_countries=", s.search_preferred_countries)
    print("  ai_features_enabled=", s.ai_features_enabled)
    print("  ai_consent_accepted=", s.ai_consent_accepted)

db.close()
