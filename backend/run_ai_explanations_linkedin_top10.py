"""
One-off manual run: generates AI explanations for the first 10
COMPLETE LinkedIn job offers, for all of Vincent's currently active
profiles (2026-09-16).

Rationale (Vincent's own reasoning): LinkedIn offers are expected to
be the most relevant and coherent opportunities for his actual career
targets (same reasoning already documented for JOBS-001 sequencing),
making them a more useful first real dataset to validate AI
explanation quality than the France Travail/Greenhouse offers already
tested (which scored very low - around 12/100 - since they are
unrelated blue-collar/retail postings, e.g. "Boucher", "Peintre
Batiment").

Design choices, made explicit:
- Selects job_offers where source == "LinkedIn" AND
  quality_level == "COMPLETE", ordered by id ascending ("first"
  interpreted as insertion order), limited to 10. Only offers
  manually completed via JOBS-001
  (PATCH /job-offers/{id}/complete-description) qualify - as of this
  session, only 1 such offer is known to exist (DECADE - Architecte
  Solutions E-commerce F/H, completed during 7.1.31.7 validation).
  This script reports the real count found rather than assuming 10.
- Does NOT apply the discovery_minimum_matching_score threshold from
  DEC-089 (used by the daily automated AIExplanationScheduler run).
  This is a deliberate, explicit choice for this manual targeted
  script: Vincent is choosing these offers directly because they are
  expected to be relevant, not relying on the generic score filter.
- Still enforces: ai_call_allowed gating per profile (DEC-078) and
  no duplicate explanation generation (an existing
  JobOfferAIExplanation row is never regenerated).
- This is REAL, PERSISTENT usage of the feature (not a throwaway
  test): generated explanations are kept, not cleaned up afterwards.
  Vincent's real profile data is sent to Gemini's free tier for this
  run, which is expected and intended (DEC-085's fictional-data
  requirement only applied to the very first technical validation,
  already completed).
- Reuses AIExplanationScheduler's already-validated internal helpers
  (_resolve_primary_user_id, _build_explanation_service,
  _generate_and_persist) rather than duplicating that logic. The
  scheduler instance created here is never started (.start() is
  never called), so no background asyncio task is spawned - it is
  used purely as a synchronous helper container.

Usage (from backend/):
    python run_ai_explanations_linkedin_top10.py
"""

import app.main  # noqa: F401 - forces safe import order, see TECH-004

from app.ai.context_service import AIContextService
from app.ai.models import JobOfferAIExplanation
from app.ai.scheduler import AIExplanationScheduler
from app.core.database import SessionLocal
from app.jobs.models import JobOffer
from app.matching.service import calculate_matching_result
from app.profile.models import Profile


MAX_OFFERS = 10


def run():
    db = SessionLocal()

    try:
        user_id = AIExplanationScheduler._resolve_primary_user_id(db)

        if user_id is None:
            print(
                "PRIMARY_USER_EMAIL does not match any user, "
                "aborting."
            )
            return

        print(f"Using primary account user_id={user_id}")

        candidate_offers = (
            db.query(JobOffer)
            .filter(
                JobOffer.source == "LinkedIn",
                JobOffer.quality_level == "COMPLETE",
            )
            .order_by(JobOffer.id.asc())
            .limit(MAX_OFFERS)
            .all()
        )

        print(
            f"\nFound {len(candidate_offers)} COMPLETE LinkedIn "
            f"offer(s) (requested up to {MAX_OFFERS}):"
        )

        for offer in candidate_offers:
            print(
                f"  id={offer.id} | {offer.title} | "
                f"{offer.company_name}"
            )

        if not candidate_offers:
            print(
                "\nNo COMPLETE LinkedIn offers found. Complete one "
                "via the Opportunity Details 'Complete Description' "
                "form (JOBS-001) before running this script."
            )
            return

        active_profiles = (
            db.query(Profile)
            .filter(
                Profile.user_id == user_id,
                Profile.is_active == True,  # noqa: E712
            )
            .all()
        )

        print(
            f"\nFound {len(active_profiles)} active profile(s): "
            f"{[p.profile_name for p in active_profiles]}"
        )

        ai_context_service = AIContextService(db, user_id)
        explanation_service = (
            AIExplanationScheduler._build_explanation_service()
        )

        scheduler = AIExplanationScheduler()

        generated = 0
        skipped_existing = 0
        skipped_no_consent = 0
        skipped_not_calculable = 0
        failed = 0

        print("\n--- Processing ---\n")

        for profile in active_profiles:
            preview = ai_context_service.get_ai_context_preview(
                profile.id
            )

            if preview is None or not preview.ai_call_allowed:
                skipped_no_consent += 1

                print(
                    f"Profile '{profile.profile_name}' "
                    f"(id={profile.id}): skipped, ai_call_allowed="
                    f"{preview.ai_call_allowed if preview else None}"
                )

                continue

            for offer in candidate_offers:
                existing = (
                    db.query(JobOfferAIExplanation)
                    .filter(
                        JobOfferAIExplanation.profile_id
                        == profile.id,
                        JobOfferAIExplanation.job_offer_id
                        == offer.id,
                    )
                    .first()
                )

                if existing is not None:
                    skipped_existing += 1

                    print(
                        f"  Offer id={offer.id} ('{offer.title}'): "
                        "already has an explanation, skipped."
                    )

                    continue

                matching_result = calculate_matching_result(
                    profile_id=profile.id,
                    job_offer_id=offer.id,
                    db=db,
                )

                if not matching_result.is_calculable:
                    skipped_not_calculable += 1

                    print(
                        f"  Offer id={offer.id} ('{offer.title}'): "
                        "not calculable, skipped."
                    )

                    continue

                try:
                    success = scheduler._generate_and_persist(
                        db=db,
                        profile_id=profile.id,
                        job_offer=offer,
                        matching_result=matching_result,
                        explanation_service=explanation_service,
                    )

                    if success:
                        generated += 1

                        print(
                            f"  Offer id={offer.id} "
                            f"('{offer.title}'): generated "
                            f"(score={matching_result.matching_score})"
                        )
                    else:
                        failed += 1

                        print(
                            f"  Offer id={offer.id} "
                            f"('{offer.title}'): AI explanation "
                            "unavailable."
                        )
                except Exception as error:
                    failed += 1

                    print(
                        f"  Offer id={offer.id} ('{offer.title}'): "
                        f"error - {error}"
                    )

        print("\n--- Summary ---")
        print(f"generated: {generated}")
        print(f"skipped_existing: {skipped_existing}")
        print(f"skipped_no_consent: {skipped_no_consent}")
        print(f"skipped_not_calculable: {skipped_not_calculable}")
        print(f"failed: {failed}")

    finally:
        db.close()


if __name__ == "__main__":
    run()
