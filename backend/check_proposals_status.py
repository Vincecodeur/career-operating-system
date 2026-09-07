from app.core.database import SessionLocal
from app.profile_enrichment.models import ProfileEnrichmentProposal

db = SessionLocal()

proposal_ids = [4523, 4524, 4525, 4526, 4527, 4529, 4530, 4531, 4532, 4533, 4534, 4535, 4537, 4538]

proposals = db.query(ProfileEnrichmentProposal).filter(
    ProfileEnrichmentProposal.id.in_(proposal_ids)
).all()

print("Nombre de propositions trouvees :", len(proposals))

for p in proposals:
    print("id=", p.id, " status=", p.status, " proposal_type=", p.proposal_type)

db.close()
