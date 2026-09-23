import app.main
from app.core.database import SessionLocal
from app.ai.models import JobOfferAIExplanation
from app.ai.scheduler import AIExplanationScheduler
from app.jobs.models import JobOffer
from app.matching.service import calculate_matching_result

db = SessionLocal()

profile_id = 2114
job_offer_id = 1620

job_offer = db.query(JobOffer).filter(JobOffer.id == job_offer_id).first()
matching_result = calculate_matching_result(profile_id=profile_id, job_offer_id=job_offer_id, db=db)

scheduler = AIExplanationScheduler()
explanation_service = AIExplanationScheduler._build_explanation_service()

success = scheduler._generate_and_persist(
    db=db,
    profile_id=profile_id,
    job_offer=job_offer,
    matching_result=matching_result,
    explanation_service=explanation_service,
)

print("Succes :", success)

if success:
    explanation = db.query(JobOfferAIExplanation).filter(
        JobOfferAIExplanation.profile_id == profile_id,
        JobOfferAIExplanation.job_offer_id == job_offer_id,
    ).first()
    print("Enregistre en base, id =", explanation.id)
    print("prompt_version =", explanation.prompt_version)

db.close()
