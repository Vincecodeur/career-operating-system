from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine

app = FastAPI(
    title="Career Operating System API",
    version="0.1.0"
)


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