from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import create_tables
from app.core.database import engine
from app.profile.router import router as profile_router
from app.skills.router import router as skills_router
from app.profile.profile_skill_router import router as profile_skill_router
from app.experience.router import router as experience_router
from app.languages.router import router as languages_router
from app.certifications.router import router as certifications_router
from app.jobs.router import router as jobs_router
from app.jobs.job_offer_skill_router import (
    router as job_offer_skill_router
)
from app.matching.router import router as matching_router


app = FastAPI(
    title="Career Operating System API",
    version="0.1.0"
)

create_tables()
app.include_router(profile_router)
app.include_router(skills_router)
app.include_router(profile_skill_router)
app.include_router(experience_router)
app.include_router(languages_router)
app.include_router(certifications_router)
app.include_router(jobs_router)
app.include_router(job_offer_skill_router)
app.include_router(matching_router)




@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "career-operating-system"
    }

@app.get("/db-health")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        value = result.scalar()

        return {
            "status": "database_connected",
            "database": "career_os",
            "query_result": value
        }