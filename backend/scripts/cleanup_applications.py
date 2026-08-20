import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__)
        .resolve()
        .parent.parent
    )
)

from app.core.database import SessionLocal
from app.applications.models import Application
from app.applications.event_models import ApplicationEvent


def main():
    db = SessionLocal()

    try:
        print("Current applications:")
        print(
            db.query(Application).count()
        )

        print(
            "Current application events:"
        )
        print(
            db.query(
                ApplicationEvent
            ).count()
        )

        db.query(
            ApplicationEvent
        ).delete()

        db.query(
            Application
        ).delete()

        db.add(
            Application(
                profile_id=1,
                job_offer_id=1,
                status="Offer",
                source_type="OPPORTUNITY",
                notes=(
                    "Technical Partnerships demo"
                ),
            )
        )

        db.add(
            Application(
                profile_id=2,
                job_offer_id=159,
                status="Applied",
                source_type="OPPORTUNITY",
                notes=(
                    "Frontend demo"
                ),
            )
        )

        db.add(
            Application(
                profile_id=3,
                job_offer_id=544,
                status="Interview",
                source_type="OPPORTUNITY",
                notes=(
                    "Cloud demo"
                ),
            )
        )

        db.add(
            Application(
                profile_id=4,
                job_offer_id=447,
                status="Applied",
                source_type="OPPORTUNITY",
                notes=(
                    "Data demo"
                ),
            )
        )

        db.commit()

        print()
        print(
            "Cleanup completed."
        )

        print(
            "Applications after cleanup:"
        )

        applications = (
            db.query(Application)
            .order_by(
                Application.profile_id
            )
            .all()
        )

        for application in applications:
            print(
                (
                    application.id,
                    application.profile_id,
                    application.job_offer_id,
                    application.status,
                )
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
