from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql+psycopg://career_os_user:CHANGE_ME_LATER@localhost:5432/career_os"
)

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


def create_tables():
    Base.metadata.create_all(bind=engine)