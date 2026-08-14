from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.applications.router import (
    router as applications_router,
)
from app.auth.router import router as auth_router
from app.certifications.router import router as certifications_router
from app.core.database import create_tables
from app.core.database import engine
from app.core.database import SessionLocal
from app.reference_data.seed_loader import seed_reference_data
from app.cv.router import router as cv_router
from app.profile_enrichment.router import router as profile_enrichment_router
from app.experience.router import router as experience_router
from app.jobs.job_offer_skill_router import (
    router as job_offer_skill_router,
)
from app.jobs.router import router as jobs_router
from app.jobs.scheduler import DiscoveryScheduler
from app.languages.router import router as languages_router
from app.reference_data.router import (
    router as reference_data_router,
)
from app.matching.router import router as matching_router
from app.profile.profile_skill_router import router as profile_skill_router

from app.profile.router import router as profile_router
from app.skills.router import router as skills_router
from app.certifications.router import router as certifications_router



discovery_scheduler = DiscoveryScheduler()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    create_tables()

    db = SessionLocal()

    try:
        seed_reference_data(db)
    finally:
        db.close()

    discovery_scheduler.start()

    try:
        yield
    finally:
        await discovery_scheduler.stop()


app = FastAPI(
    title="Career Operating System API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(skills_router)
app.include_router(profile_skill_router)
app.include_router(experience_router)
app.include_router(languages_router)
app.include_router(certifications_router)
app.include_router(cv_router)
app.include_router(profile_enrichment_router)
app.include_router(jobs_router)
app.include_router(job_offer_skill_router)
app.include_router(matching_router)
app.include_router(applications_router)
app.include_router(auth_router)
app.include_router(reference_data_router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "career-operating-system",
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
            "query_result": value,
        }