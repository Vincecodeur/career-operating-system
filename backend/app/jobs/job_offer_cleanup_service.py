from datetime import datetime
from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.applications.models import Application
from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.models import JobOffer


AGE_WINDOW_TO_DAYS: dict[str, int] = {
    "7_DAYS": 7,
    "14_DAYS": 14,
    "30_DAYS": 30,
    "90_DAYS": 90,
}

DEFAULT_AGE_WINDOW_DAYS = 30


def resolve_age_window_days(discovery_age_window: str) -> int:
    """
    Converts UserSettings.discovery_age_window (e.g. "30_DAYS") into a
    number of days. Falls back to DEFAULT_AGE_WINDOW_DAYS for unknown
    values, consistent with the fallback already used in
    frontend/src/pages/OpportunitiesPage.tsx.
    """
    return AGE_WINDOW_TO_DAYS.get(
        discovery_age_window,
        DEFAULT_AGE_WINDOW_DAYS,
    )


def _classify_job_offers(
    db: Session,
    age_window_days: int,
) -> tuple[list[int], list[int], int]:
    """
    Single-pass classification of every JobOffer row.

    Returns (stale_ids, protected_ids, total_evaluated):
    - stale_ids: offers eligible for permanent deletion. An offer is
      eligible when it has no JobOfferSource at all (never confirmed as
      seen through the real discovery pipeline - Option B, decision
      confirmed by Vincent on 2026-09-07), OR its most recent
      JobOfferSource.last_seen_at is older than age_window_days.
      Offers referenced by at least one Application are excluded from
      this list.
    - protected_ids: offers that would otherwise be stale under the same
      rule, but are kept alive because at least one Application
      references them.
    - total_evaluated: total number of JobOffer rows examined.
    """
    cutoff = datetime.utcnow() - timedelta(days=age_window_days)

    applied_job_offer_ids = {
        row[0]
        for row in db.query(Application.job_offer_id).distinct().all()
    }

    last_seen_by_offer = dict(
        db.query(
            JobOfferSource.job_offer_id,
            func.max(JobOfferSource.last_seen_at),
        )
        .group_by(JobOfferSource.job_offer_id)
        .all()
    )

    all_offer_ids = [row[0] for row in db.query(JobOffer.id).all()]

    stale_ids: list[int] = []
    protected_ids: list[int] = []

    for offer_id in all_offer_ids:
        most_recent_seen = last_seen_by_offer.get(offer_id)
        is_eligible_by_age = (
            most_recent_seen is None or most_recent_seen < cutoff
        )

        if not is_eligible_by_age:
            continue

        if offer_id in applied_job_offer_ids:
            protected_ids.append(offer_id)
        else:
            stale_ids.append(offer_id)

    return stale_ids, protected_ids, len(all_offer_ids)


def find_stale_job_offer_ids(
    db: Session,
    age_window_days: int,
) -> list[int]:
    """
    Returns the ids of JobOffer rows eligible for permanent deletion:
    - their most recent JobOfferSource.last_seen_at (across all attached
      sources) is older than age_window_days, OR
    - they have no JobOfferSource at all (Option B),
    excluding any offer referenced by at least one Application.
    """
    stale_ids, _protected_ids, _total = _classify_job_offers(
        db, age_window_days
    )
    return stale_ids


def delete_stale_job_offers(
    db: Session,
    age_window_days: int,
) -> dict:
    """
    Permanently deletes the JobOffer rows returned by
    find_stale_job_offer_ids(), along with their JobOfferSkill and
    JobOfferSource rows.

    JobOfferSkill and JobOfferSource both reference job_offers.id without
    an ondelete cascade at the database level (RESTRICT by default in
    PostgreSQL). Both must be deleted explicitly before JobOffer itself,
    in that order, otherwise the deletion raises an IntegrityError - this
    gap was not covered by the original phase design and was discovered
    during the 2026-09-07 repository audit.

    Returns a summary:
    {
        "evaluated": total number of JobOffer rows examined,
        "deleted": number of JobOffer rows actually deleted,
        "protected_by_application": number of otherwise-eligible offers
            skipped because at least one Application references them,
    }
    """
    stale_ids, protected_ids, total_evaluated = _classify_job_offers(
        db, age_window_days
    )

    if stale_ids:
        db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id.in_(stale_ids)
        ).delete(synchronize_session=False)

        db.query(JobOfferSource).filter(
            JobOfferSource.job_offer_id.in_(stale_ids)
        ).delete(synchronize_session=False)

        db.query(JobOffer).filter(
            JobOffer.id.in_(stale_ids)
        ).delete(synchronize_session=False)

        db.commit()

    return {
        "evaluated": total_evaluated,
        "deleted": len(stale_ids),
        "protected_by_application": len(protected_ids),
    }
