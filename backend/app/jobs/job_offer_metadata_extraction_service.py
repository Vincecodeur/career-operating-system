import logging

from sqlalchemy.orm import Session

from app.core.settings import settings
from app.ai.providers.gemini_provider import GeminiProvider
from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.models import JobOffer
from app.skills.models import Skill

logger = logging.getLogger(__name__)


EXTRACTION_PROMPT_TEMPLATE = """
Tu es un assistant d'extraction de métadonnées pour des offres
d'emploi.

Ta tâche : lire la description d'une offre d'emploi et en extraire
des métadonnées structurées.

Règles strictes :
- Pour les compétences, tu ne dois choisir que parmi la liste de
  compétences autorisées fournie ci-dessous (le catalogue).
- matched_skills : compétences du catalogue explicitement mentionnées
  ou clairement requises par l'offre. Recopie exactement le nom tel
  qu'il apparaît dans le catalogue.
- unmatched_skill_mentions : compétences ou technologies mentionnées
  dans l'offre mais absentes du catalogue fourni. Recopie-les telles
  qu'elles apparaissent dans le texte de l'offre.
- N'invente jamais de compétence absente du texte de l'offre.
- seniority : choisis exactement une valeur parmi Junior, Mid,
  Senior, Lead, Executive, UNKNOWN (si le niveau requis n'est pas
  clairement précisé).
- work_mode : choisis exactement une valeur parmi Remote, Hybrid,
  Onsite, UNKNOWN (si le mode de travail n'est pas précisé).

Catalogue de compétences autorisées :
{skill_catalog}

Description de l'offre :
{job_offer_description}

Retourne un objet JSON avec exactement ces champs : matched_skills,
unmatched_skill_mentions, seniority, work_mode.
"""


class JobOfferMetadataExtractionService:
    """
    DEC-093 - extraction de compétences/séniorité/mode de travail
    depuis le texte d'une offre complétée manuellement (JOBS-001),
    via Gemini. Appelée de façon synchrone, mais son échec ne doit
    jamais empêcher la sauvegarde de la description elle-même.
    """

    @staticmethod
    def extract_and_persist(
        db: Session,
        job_offer_id: int,
    ) -> bool:
        job_offer = db.query(JobOffer).filter(
            JobOffer.id == job_offer_id
        ).first()

        if job_offer is None:
            return False

        skills = db.query(Skill).all()
        skill_catalog = "\n".join(
            f"- {skill.name}" for skill in skills
        )

        prompt = EXTRACTION_PROMPT_TEMPLATE.format(
            skill_catalog=skill_catalog,
            job_offer_description=job_offer.description,
        )

        provider = GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.GEMINI_MODEL_NAME,
            timeout_seconds=settings.GEMINI_TIMEOUT_SECONDS,
        )

        extracted = provider.extract_job_offer_metadata(prompt)

        skill_by_name_lower = {
            skill.name.lower(): skill for skill in skills
        }

        matched_skill_ids = []
        matched_skill_names = []

        for name in extracted.matched_skills:
            skill = skill_by_name_lower.get(name.strip().lower())

            if skill is not None:
                matched_skill_ids.append(skill.id)
                matched_skill_names.append(skill.name)

        db.query(JobOfferSkill).filter(
            JobOfferSkill.job_offer_id == job_offer_id
        ).delete()

        for skill_id in matched_skill_ids:
            db.add(
                JobOfferSkill(
                    job_offer_id=job_offer_id,
                    skill_id=skill_id,
                    is_required=True,
                )
            )

        job_offer.skills_normalized = matched_skill_names
        job_offer.skills_extracted = (
            extracted.unmatched_skill_mentions
        )
        job_offer.seniority = extracted.seniority
        job_offer.work_mode = extracted.work_mode

        db.commit()

        return True