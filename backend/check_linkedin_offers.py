from app.core.database import SessionLocal
from app.jobs.models import JobOffer

db = SessionLocal()

count = db.query(JobOffer).filter(JobOffer.source == "linkedin").count()

print("Nombre d offres LinkedIn en base :", count)

db.close()
