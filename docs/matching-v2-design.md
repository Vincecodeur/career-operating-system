# Matching V2 Design

## Phase

6.0.1 Matching V2 Design

## Status

Design

## Purpose

The purpose of Matching V2 is to improve the opportunity matching engine by moving from a skills-only score to a multi-criteria, explainable scoring model.

Matching V2 must remain:

- deterministic
- testable
- explainable
- fully calculated by the backend
- transparent for the user
- compatible with future AI explanation layers

The frontend must not calculate the score.

The frontend only displays the results returned by the backend API.

## References

- DEC-006 Explainable Scoring
- DEC-029 Matching Engine V1
- DEC-035 Structured Profile Source Of Truth
- DEC-039 Explainable Opportunity Scoring
- DEC-041 Standardized Job Evaluation Rules

## Current Matching V1

Matching V1 compares only the skills attached to a profile and the skills attached to a job offer.

Current formula:

matching_score =
matching_skills /
required_skills × 100

Example:

Job offer required skills:

- Python
- FastAPI
- Docker
- Azure

Profile skills:

- Python
- FastAPI

Matching skills:

- Python
- FastAPI

Missing skills:

- Docker
- Azure

Score:
2 / 4 × 100 = 50 %

## Current Matching V1 Limitations

Matching V1 does not use:

- experience
- work mode
- location
- contract type
- salary
- languages
- certifications
- seniority
- candidate preferences

This limitation was acceptable for V1 because the objective was to validate the complete matching workflow.

Matching V2 must provide a more realistic evaluation of opportunities while remaining simple and explainable.

## Matching V2 Design Principles

Matching V2 must follow the following principles:

- The score must remain explainable
- The score must be calculated by the backend only
- The frontend must not contain scoring rules
- Every sub-score must be visible or explainable
- Missing data must not automatically exclude an opportunity
- Missing data may apply a penalty when appropriate
- AI must not calculate the score
- AI may explain the score in later phases
- Matching V2 must remain simple enough to test with Pytest
- Matching V2 must prepare future Opportunity Analysis phases

## Matching V2 Score Structure

The Matching V2 score is calculated on 100 points.

Recommended weighting:

Skills Match 60%
Experience Match 15%
Work Mode Match 10%
Location Match 10%
Contract Match 5%

---

Total 100%

## 1. Skills Match

Weight:

60%

Objective:

Measure how many required skills are already present in the candidate profile.

Formula:

skills_score =
matching_skills /
required_skills × 100

Example:

Required skills:

- Python
- FastAPI
- PostgreSQL
- Docker

Profile skills:

- Python
- FastAPI
- PostgreSQL

Matching skills:

- Python
- FastAPI
- PostgreSQL

Missing skills:

- Docker

Skills score:
3 / 4 × 100 = 75 %

Rules:

- If the offer contains no required skills, score = 0
- Matching skills must be returned by the backend
- Missing skills must be returned by the backend
- Skill comparison continues to use the Skill catalog
- Free-text semantic analysis is out of scope

## 2. Experience Match

Weight:

15%

Objective:

Evaluate whether the candidate has sufficient experience for the opportunity.

Potential data sources:

Profile:

- WorkExperience
- years_of_experience from ProfileSkill

Job Offer:

- seniority
- future required_experience field

Initial scoring proposal:

Candidate experience >= required experience
= 100 %

Candidate experience >= 75 % of required experience
= 75 %

Candidate experience >= 50 % of required experience
= 50 %

Candidate experience < 50 % of required experience
= 25 %

No experience data
= neutral score

Examples:

Required:
5 years

Profile:
7 years

Experience score:
100 %

Required:
5 years

Profile:
2 years

Experience score:
50 %

Rules:

- Missing experience data must not exclude the offer
- Any penalty must be explicit
- No AI-based interpretation

## 3. Work Mode Match

Weight:

10%

Objective:

Compare the candidate preferred work mode with the opportunity.

Supported values:

- Remote
- Hybrid
- Onsite

Initial scoring proposal:

Exact match
= 100 %

Partially compatible
= 50 %

Incompatible
= 0 %

Unknown
= neutral score

Examples:

Profile:
Remote

Offer:
Remote

Work mode score:
100 %

Profile:
Remote

Offer:
Hybrid

Work mode score:
50 %

Profile:
Remote

Offer:
Onsite

Work mode score:
0 %

Rules:

- Work mode scoring must be explicit
- Unknown mode must not exclude the offer
- Uses standardized values from DEC-041

## 4. Location Match

Weight:

10%

Objective:

Evaluate location compatibility.

Initial scoring proposal:

Same city
= 100 %

Same region
= 75 %

Same country
= 50 %

Remote compatible
= 100 %

Different country
= 0 %

Unknown
= neutral score

Examples:

Profile:
Paris

Offer:
Paris

Location score:
100 %

Profile:
Paris

Offer:
Lyon

Location score:
50 %

Profile:
France

Offer:
Germany

Location score:
0 %

Rules:

- Remote jobs may override some location penalties
- Location scoring must remain deterministic
- Geocoding is out of scope
- Distance calculation is out of scope

## 5. Contract Match

Weight:

5%

Objective:

Evaluate whether the contract type matches the candidate preference.

Supported examples:

- Permanent
- Fixed-term
- Freelance
- Internship
- Apprenticeship

Initial scoring proposal:

Exact match
= 100 %

Acceptable alternative
= 50 %

Incompatible
= 0 %

Unknown
= neutral score

Examples:

Profile:
Permanent

Offer:
Permanent

Contract score:
100 %

Profile:
Permanent

Offer:
Internship

Contract score:
0 %

Rules:

- Unknown contract type must not exclude the offer
- Contract mismatch must be visible in explanations

## Final Score Formula

final_score =
(skills_score × 0.60)

- (experience_score × 0.15)
- (work_mode_score × 0.10)
- (location_score × 0.10)
- (contract_score × 0.05)

The final score is rounded to two decimals.

## Example Calculation

Skills score:
75 %

Experience score:
100 %

Work mode score:
50 %

Location score:
100 %

Contract score:
100 %

Calculation:

75 × 0.60 = 45
100 × 0.15 = 15
50 × 0.10 = 5
100 × 0.10 = 10
100 × 0.05 = 5

Final score:
45 + 15 + 5 + 10 + 5 = 80 %

## Expected API Output

{
"profile_id": 1,
"job_offer_id": 123,
"matching_score": 80.0,
"scores": {
"skills_score": 75.0,
"experience_score": 100.0,
"work_mode_score": 50.0,
"location_score": 100.0,
"contract_score": 100.0
},
"weights": {
"skills_weight": 60,
"experience_weight": 15,
"work_mode_weight": 10,
"location_weight": 10,
"contract_weight": 5
},
"matching_skills": [
"Python",
"FastAPI",
"PostgreSQL"
],
"missing_skills": [
"Docker"
],
"strengths": [
"Strong skills alignment",
"Experience exceeds expected level",
"Location is compatible",
"Contract type is compatible"
],
"weaknesses": [
"Work mode is partially compatible",
"Docker is missing from the profile"
]
}

## Backend Responsibilities

The backend must:

- calculate all sub-scores
- calculate the final score
- identify matching skills
- identify missing skills
- identify strengths
- identify weaknesses
- generate deterministic explanations
- return all required data for the frontend
- keep scoring rules testable
- prevent opaque scoring

## Frontend Responsibilities

The frontend must:

- display the final score
- display sub-scores
- display matching skills
- display missing skills
- display strengths
- display weaknesses
- display explanations
- avoid calculating any score
- avoid applying business rules
- consume only backend API results

## Ranking Behaviour

The opportunity ranking continues to sort offers by descending score.

Matching V2 ranking must use the final Matching V2 score instead of the current skills-only score.

Tie-breaker rules are not required during this phase.

## Missing Data Strategy

Missing information must not automatically exclude an offer.

Examples:

Missing salary
=> offer remains eligible

Missing work mode
=> offer remains eligible

Missing location
=> offer remains eligible

Missing contract
=> offer remains eligible

Missing experience
=> offer remains eligible

All penalties must remain explicit and explainable.

## Out Of Scope

The following topics are not part of Matching V2:

- AI scoring
- Embeddings
- LLM ranking
- Semantic similarity
- Machine Learning
- Market Intelligence
- Career Roadmap
- Automatic Applications
- LinkedIn Connector implementation
- New Discovery Sources
- Frontend redesign
- Dashboard redesign

## Future Compatibility

Matching V2 must prepare:

- 6.0.2 Matching V2 Backend
- 6.0.3 Matching V2 Frontend Validation
- 6.0.4 Explainable Scoring Backend
- 6.0.5 Explainable Scoring Frontend Validation
- 6.0.6 Opportunity Analysis Backend
- 6.0.7 Opportunity Analysis Frontend Validation
- 7.x AI Explanation Layer
- 8.x Market Intelligence
- 9.x Career Roadmap

## Validation Criteria For Phase 6.0.1

The phase is complete when:

- the design document exists
- scoring dimensions are defined
- weighting rules are defined
- expected API output is defined
- backend responsibilities are defined
- frontend responsibilities are defined
- out-of-scope elements are defined
- no backend implementation has started
- no frontend implementation has started

## Next Phase

6.0.2 Matching V2 Backend

Objective:

Implement the Matching V2 deterministic scoring engine according to this design document.

The backend implementation must begin only after validation and documentation review of this design.
