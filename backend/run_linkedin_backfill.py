"""
One-off backfill script for phase 7.1.30 (LinkedIn Email Connector).

Processes ALL matching LinkedIn emails currently in the mailbox
(read or unread), not just unread ones, since the mailbox already
contains manually forwarded historical emails from before the
automatic redirection was set up. Uses DiscoveryService so offers
are actually persisted (JobOffer, JobOfferSource), not just printed.

Usage (from backend/):
    python run_linkedin_backfill.py

Safe to run multiple times: already-known offers are deduplicated
and refreshed (last_seen_at updated) rather than duplicated, thanks
to JobOfferRepository.upsert_job_offer().
"""

from app.core.database import SessionLocal
from app.auth.models import User
from app.jobs.connectors.credentials_resolver import (
    resolve_linkedin_email_credentials,
)
from app.jobs.connectors.linkedin_email_connector import (
    LinkedInEmailConnector,
)
from app.jobs.discovery_service import DiscoveryService


def run_backfill():
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == "maw282003@gmail.com"
        ).first()

        if user is None:
            print("Utilisateur principal introuvable.")
            return

        credentials = resolve_linkedin_email_credentials(
            db, user.id
        )

        if credentials is None:
            print(
                "Aucun identifiant LinkedIn Email resolu - "
                "verifier la configuration Settings."
            )
            return

        connector = LinkedInEmailConnector(
            imap_host=credentials["imap_host"],
            imap_port=credentials["imap_port"],
            email_address=credentials["email_address"],
            app_password=credentials["app_password"],
            folder=credentials["folder"],
            only_unread=False,
        )

        discovery_service = DiscoveryService(db)

        result = discovery_service.import_from_connector(
            connector=connector,
            source_type="API",
        )

        print("Resultat du backfill:")
        print("  source_name:", result["source_name"])
        print("  offers_fetched:", result["offers_fetched"])
        print("  offers_imported:", result["offers_imported"])

    finally:
        db.close()


if __name__ == "__main__":
    run_backfill()
