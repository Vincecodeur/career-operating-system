# Profile Enrichment Design

# Phase 7.1.16.14

# Career Operating System

Status:
Design

Related Decisions:

- DEC-013 Profile Source Of Truth
- DEC-020 Central Skill Catalog
- DEC-024 Central Language Catalog
- DEC-025 Central Certification Catalog
- DEC-035 Structured Profile Source Of Truth
- DEC-051 Reference Data Governance

---

1. OBJECTIVE

---

The objective of this phase is to define how CV data can enrich an existing candidate profile while preserving data quality, traceability and user control.

The profile remains the official source of truth.

A CV is considered an external source of information.

The parser never directly updates the profile.

The parser only produces observations and enrichment proposals.

---

2. GUIDING PRINCIPLES

---

Principle 1
Profile is the source of truth.

All matching, scoring, analysis and recommendations are based on the structured profile stored in the application.

CVs are supporting data sources.

---

Principle 2
Human validation is mandatory.

No information extracted from a CV may automatically update a profile.

All updates require explicit user validation.

---

Principle 3
Reference data governance.

Skills, Languages and Certifications use centralized repositories.

The CV parser must reuse existing repository entries whenever possible.

Creation of new repository entries must remain exceptional.

---

Principle 4
Traceability.

The system must preserve:

- the detected value from the CV
- the normalized value
- the resolved repository value
- the final user decision

---

3. TARGET WORKFLOW

---

CV Upload
↓
Text Extraction
↓
Parsing
↓
Observed Values
↓
Normalization
↓
Repository Resolution
↓
Enrichment Proposals
↓
User Validation
↓
Profile Update

---

4. OBSERVED VALUES

---

An observed value is a raw value detected inside a CV.

Examples:

Observed Skill:
Docker Engine

Observed Certification:
AWS Practitioner

Observed Language:
english

Observed Experience:
Technical Partnerships Manager

Observed values are not profile values.

Observed values are not repository values.

---

5. NORMALIZATION

---

Before any comparison, values must be normalized.

Normalization rules:

- trim spaces
- lowercase comparison
- remove duplicate spaces
- normalize punctuation
- normalize accents when appropriate

Examples:

" Docker "
→ "docker"

"DOCKER"
→ "docker"

"English"
→ "english"

---

6. REPOSITORY RESOLUTION

---

After normalization the system searches existing repositories.

Repositories:

- Skill
- Language
- Certification

---

Example

Observed value:

docker

Repository contains:

Docker

Result:

Matched Skill:
Docker

Skill ID:
3

---

Example

Observed value:

english

Repository contains:

English

Result:

Matched Language:
English

Language ID:
2

---

7. PROFILE ENRICHMENT PROPOSALS

---

The system never updates the profile directly.

Instead it creates proposals.

Proposal Lifecycle:

PENDING
↓
ACCEPTED
or
REJECTED

Only ACCEPTED proposals may modify profile data.

---

8. PROPOSAL TYPES

---

SKILL

LANGUAGE

CERTIFICATION

EXPERIENCE

PROFILE_FIELD

---

9. SKILL ENRICHMENT RULES

---

Scenario:

CV contains:

Docker

Profile currently contains:

Python
FastAPI

Repository contains:

Docker

Result:

Proposal:

Add Skill:
Docker

Status:
PENDING

---

If accepted:

Create ProfileSkill

No Skill creation.

---

10. LANGUAGE ENRICHMENT RULES

---

Scenario:

CV contains:

English

Profile contains:

French

Repository contains:

English

Result:

Proposal:

Add Language:
English

---

If accepted:

Create ProfileLanguage

No Language creation.

---

11. CERTIFICATION ENRICHMENT RULES

---

Scenario:

CV contains:

AWS Certified Cloud Practitioner

Profile contains:

No certification

Repository contains:

AWS Certified Cloud Practitioner

Result:

Proposal:

Add Certification:
AWS Certified Cloud Practitioner

---

If accepted:

Create ProfileCertification

No Certification creation.

---

12. EXPERIENCE ENRICHMENT RULES

---

Experiences are not repository-driven.

An experience belongs to a specific profile.

Example:

Technical Partnerships Manager
Anchanto
2024-2026

Result:

Proposal:

Add Work Experience

---

If accepted:

Create WorkExperience

---

13. CONFLICT MANAGEMENT

---

Example

Profile:

English
Level B2

CV:

English
Level C1

---

The system must not choose automatically.

Create Conflict Proposal:

Field:
English Level

Profile Value:
B2

CV Value:
C1

Skill Conflict Example

Profile:
Docker
Years Of Experience: 3

CV:
Docker
Years Of Experience: 8

Result:
Conflict Proposal

Field:
Years Of Experience

Profile Value:
3

CV Value:
8

User Actions:
Keep Existing Value
Update With CV Value
Reject CV Value

---

14. REFERENCE DATA GOVERNANCE

---

The repositories are the official vocabulary of the system.

Repositories:

- Skills
- Languages
- Certifications

The parser must never create duplicates.

---

Example

Repository:

Docker

CV:

docker

Result:

Reuse existing repository value.

---

Example

Repository:

Docker

CV:

Docker Engine

Potential match:

Docker

User validation required.

---

15. CREATION OF NEW REFERENCE ENTRIES

---

The parser must not automatically create:

- Skills
- Languages
- Certifications

Creation workflow:

Observed Value
↓
No Match Found
↓
User Validation
↓
Repository Creation

---

Example

Observed Skill:

Temporal.io

Repository:

No match found

Proposal:

Create New Skill:
Temporal.io

User Decision Required

---

16. DATA QUALITY RULES

---

Mandatory rules:

- no automatic repository creation
- repository reuse whenever possible
- normalized search before creation
- human validation before profile update
- human validation before repository expansion
- full traceability of detected values

---

17. TARGET USER EXPERIENCE

---

New section in Profile Details:

CV Suggestions

---

Skills

New Skills Detected

[ ] Docker
[ ] Kubernetes

Actions:

Accept
Reject

---

Languages

New Languages Detected

[ ] English

Actions:

Accept
Reject

---

Certifications

New Certifications Detected

[ ] AWS Certified Cloud Practitioner

Actions:

Accept
Reject

---

Experiences

New Experiences Detected

[ ] Technical Partnerships Manager

Actions:

Accept
Reject

---

18. OUT OF SCOPE

---

Not included in this phase:

- AI enrichment
- LLM analysis
- Embeddings
- Automatic skills inference
- Automatic profile modification
- Automatic repository creation
- Career recommendations
- Matching improvements

---

19. SUCCESS CRITERIA

---

The phase is complete when:

- enrichment workflow is defined
- repository governance is defined
- conflict management is defined
- proposal lifecycle is defined
- user validation process is defined
- data quality principles are defined

No production code is expected during this phase.
