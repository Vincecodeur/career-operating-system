from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings


DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from app.profile.models import Profile
from app.skills.models import Skill
from app.profile.profile_skill_models import ProfileSkill
from app.experience.models import WorkExperience
from app.languages.models import Language
from app.languages.models import ProfileLanguage
from app.certifications.models import Certification
from app.certifications.models import ProfileCertification
from app.jobs.models import JobOffer
from app.jobs.job_offer_skill_models import JobOfferSkill
from app.jobs.job_source_models import JobSource
from app.jobs.job_offer_source_models import JobOfferSource
from app.auth.models import User
from app.auth.password_reset_models import (
    PasswordResetToken,
)
from app.cv.models import CV
from app.reference_data.models import Country
from app.reference_data.models import WorkMode
from app.reference_data.models import ContractType
from app.settings.models import ApplicationSetting
from app.profile.profile_soft_skill_models import ProfileSoftSkill


def create_tables():
    Base.metadata.create_all(bind=engine)