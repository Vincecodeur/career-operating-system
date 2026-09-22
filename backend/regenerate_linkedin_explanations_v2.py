"""
DEC-090 validation script: deletes the 10 existing AI explanations
generated in v1 (score_explanation_v1, before DEC-090) for the same
10 LinkedIn offers already validated in 7.2.0.6, then regenerates
them using the now-default score_explanation_v2 (enriched context:
matching_skills, missing_skills, relevant_experience_summary,
professional_summary, career_motivations).

This allows a direct before/after comparison on the exact same
(profile, offer) pairs, rather than comparing across different
offers.

Real, persistent usage (not a throwaway test): the new v2
explanations are kept, not cleaned up afterwards. Uses Vincent's real
profile data, as already accepted for this project (DEC-085's
fictional-data requirement only applied to the very first technical
validation, already completed in 7.2.0.6).

Usage (from backend/):
    python regenerate_linkedin_explanations_v2.py
"""

import app.main  # noqa: F401 - forces safe import order, see TECH-004

from app.ai.context_service import AIContextService
from app.ai.models import JobOfferAIExplanation
from app.ai.scheduler import AIExplanationScheduler
from app.core.database import SessionLocal
from app.jobs.models import JobOffer
from app.matching.service import calculate_matching_result
from app.profile.models import Profile


TARGET_OFFER_IDS = [
    1612, 1615, 1620, 1640, 1644, 1645, 1659, 1660, 1661, 1662,
]


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

        active_profiles = (
            db.query(Profile)
            .filter(
                Profile.user_id == user_id,
                Profile.is_active == True,  # noqa: E712
            )
            .all()
        )

        print(
            f"Found {len(active_profiles)} active profile(s): "
            f"{[p.profile_name for p in active_profiles]}"
        )

        if not active_profiles:
            print("No active profile found, aborting.")
            return

        # --- Step 1: delete existing v1 explanations for these offers ---
        deleted_count = (
            db.query(JobOfferAIExplanation)
            .filter(
                JobOfferAIExplanation.job_offer_id.in_(
                    TARGET_OFFER_IDS
                ),
                JobOfferAIExplanation.profile_id.in_(
                    [p.id for p in active_profiles]
                ),
            )
            .delete(synchronize_session=False)
        )

        db.commit()

        print(
            f"\nDeleted {deleted_count} existing v1 explanation(s) "
            "for the 10 target offers."
        )

        # --- Step 2: regenerate using v2 (now the scheduler default) ---
        candidate_offers = (
            db.query(JobOffer)
            .filter(JobOffer.id.in_(TARGET_OFFER_IDS))
            .all()
        )

        print(
            f"Found {len(candidate_offers)} target offer(s) to "
            "regenerate:"
        )

        for offer in candidate_offers:
            print(f"  id={offer.id} | {offer.title}")

        ai_context_service = AIContextService(db, user_id)
        explanation_service = (
            AIExplanationScheduler._build_explanation_service()
        )
        scheduler = AIExplanationScheduler()

        generated = 0
        skipped_no_consent = 0
        skipped_not_calculable = 0
        failed = 0

        print("\n--- Regenerating with score_explanation_v2 ---\n")

        for profile in active_profiles:
            context_preview = (
                ai_context_service.get_ai_context_preview(profile.id)
            )

            if context_preview is None or not context_preview.ai_call_allowed:
                skipped_no_consent += 1

                print(
                    f"Profile '{profile.profile_name}' "
                    f"(id={profile.id}): skipped, ai_call_allowed="
                    f"{context_preview.ai_call_allowed if context_preview else None}"
                )

                continue

            for job_offer in candidate_offers:
                matching_result = calculate_matching_result(
                    profile_id=profile.id,
                    job_offer_id=job_offer.id,
                    db=db,
                )

                if not matching_result.is_calculable:
                    skipped_not_calculable += 1

                    print(
                        f"  Offer id={job_offer.id} "
                        f"('{job_offer.title}'): not calculable, "
                        "skipped."
                    )

                    continue

                try:
                    success = scheduler._generate_and_persist(
                        db=db,
                        profile_id=profile.id,
                        job_offer=job_offer,
                        matching_result=matching_result,
                        explanation_service=explanation_service,
                    )

                    if success:
                        generated += 1

                        print(
                            f"  Offer id={job_offer.id} "
                            f"('{job_offer.title}'): regenerated "
                            f"(score={matching_result.matching_score})"
                        )
                    else:
                        failed += 1

                        print(
                            f"  Offer id={job_offer.id} "
                            f"('{job_offer.title}'): AI explanation "
                            "unavailable."
                        )
                except Exception as error:
                    failed += 1

                    print(
                        f"  Offer id={job_offer.id} "
                        f"('{job_offer.title}'): error - {error}"
                    )

        print("\n--- Summary ---")
        print(f"deleted (v1): {deleted_count}")
        print(f"generated (v2): {generated}")
        print(f"skipped_no_consent: {skipped_no_consent}")
        print(f"skipped_not_calculable: {skipped_not_calculable}")
        print(f"failed: {failed}")

    finally:
        db.close()


if __name__ == "__main__":
    run()
