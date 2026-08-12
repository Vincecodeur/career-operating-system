# Profile Enrichment Backend Technical Design

## Phase

7.1.16.14.6 Backend Technical Design

## Status

Design

## Objective

Define the backend architecture for the controlled profile enrichment mechanism based on data already extracted by the CV Parsing Service.

This phase does not produce production code.

The goal is to design how parsed CV data can generate enrichment proposals without automatically modifying the structured profile.

## Context

The Career Operating System already supports:

- profile management;
- profile skills;
- work experiences;
- profile languages;
- profile certifications;
- CV upload;
- CV listing;
- CV download;
- CV default selection;
- CV parsing for PDF and DOCX files.

The CV parsing service currently returns structured data from an uploaded CV.

The parsed CV data can contain:

- full_name;
- professional_title;
- summary;
- skills;
- languages;
- certifications;
- experiences.

The existing parsing endpoint returns a parsed response but does not persist parsed data into profile-related tables.

The Profile remains the source of truth.

The CV is an observation source.

No profile update must happen without explicit user validation.

## Current Repository Audit Summary

### Profile model

The current Profile model contains:

- id;
- profile_name;
- full_name;
- current_title;
- location;
- years_of_experience;
- target_role_short_term;
- target_role_long_term;
- remote_preference;
- preferred_countries;
- is_active;
- created_at;
- updated_at;
- cvs relationship.

The Profile does not currently contain a summary field.

The Profile does not directly contain embedded skill, language, certification or experience fields. These are handled through dedicated related domains.

### CV model

The current CV model contains:

- id;
- profile_id;
- file_name;
- original_file_name;
- storage_path;
- file_size_bytes;
- mime_type;
- language;
- version_label;
- is_default;
- parsing_status;
- uploaded_at;
- updated_at.

The CV belongs to a Profile.

The CV model already supports a parsing_status lifecycle.

Current values used by the router are:

- PENDING;
- PROCESSING;
- COMPLETED;
- FAILED.

### CV parsing

The CV parsing service supports:

- PDF text extraction;
- DOCX text extraction;
- structured parsing from raw text;
- full name detection;
- professional title detection;
- summary extraction;
- skills extraction;
- languages extraction;
- certifications extraction;
- experiences extraction.

The parser returns ParsedCVData.

The parser does not update the Profile.

The parser does not update Skill, Language, Certification or WorkExperience repositories.

### Existing parsing endpoint

The existing endpoint is:

POST /cvs/{cv_id}/parse

Current behavior:

1. Load the CV.
2. Set parsing_status to PROCESSING.
3. Run parse_cv_file.
4. If parsing fails, set parsing_status to FAILED.
5. If parsing succeeds, set parsing_status to COMPLETED.
6. Return ParsedCVResponse.

The endpoint returns the parsed data but does not persist enrichment proposals.

## Design Principles

### Principle 1: Profile is the source of truth

The structured Profile remains the official career source of truth.

Matching, ranking, opportunity analysis and future recommendations must continue to rely on the structured profile, not directly on a CV.

### Principle 2: CV is an observation source

A CV can contain useful information, but this information must be treated as observed data.

Observed data is not trusted as final profile data.

### Principle 3: No automatic profile update

The enrichment backend must never update the Profile automatically after parsing a CV.

All profile updates require explicit user validation.

### Principle 4: Proposal-based workflow

Parsed CV data must produce enrichment proposals.

A proposal starts as PENDING.

The user can then accept or reject the proposal.

Only accepted proposals may update the profile or related profile data.

### Principle 5: Backend owns business logic

All enrichment comparison, conflict detection, repository resolution and proposal application logic belongs to the backend.

The frontend only displays proposals and sends accept or reject actions.

### Principle 6: Repository reuse first

Skills, Languages and Certifications are central reference data.

The enrichment mechanism must try to reuse existing reference entries before proposing anything new.

Automatic repository creation is out of scope.

### Principle 7: Traceability

The system must preserve enough information to understand:

- the source CV;
- the target profile;
- the proposal type;
- the proposed value;
- the current profile value when relevant;
- the user decision;
- the proposal status.

## Target Backend Package

Create a new backend package:

backend/app/profile_enrichment/

Target files:

- models.py
- schemas.py
- service.py
- router.py
- enums.py

### Responsibilities

models.py

Stores enrichment proposals.

schemas.py

Defines API request and response contracts.

service.py

Contains the enrichment business logic.

router.py

Exposes enrichment endpoints.

enums.py

Defines proposal types and statuses.

## Enrichment Proposal

An enrichment proposal represents one potential update detected from a parsed CV.

Examples:

- add a skill detected in a CV;
- add a language detected in a CV;
- add a certification detected in a CV;
- add a work experience detected in a CV;
- update current title from professional title;
- flag a full name conflict;
- ignore summary until a Profile summary field exists.

## Proposal Types

The proposal types should be:

- PROFILE_FIELD;
- SKILL;
- LANGUAGE;
- CERTIFICATION;
- EXPERIENCE.

### PROFILE_FIELD

Used for parsed values that map to fields on the Profile model.

Current possible mappings:

- ParsedCVData.full_name maps to Profile.full_name;
- ParsedCVData.professional_title maps to Profile.current_title.

Important limitation:

ParsedCVData.summary currently has no target Profile field.

Therefore summary must not be applied to Profile during this phase.

The backend may either ignore summary for now or create a non-applicable proposal type for future use.

For MVP simplicity, the recommended choice is:

Do not generate profile update proposals for summary until the Profile model has a dedicated field.

### SKILL

Used for parsed CV skills.

Target domain:

- Skill reference catalog;
- ProfileSkill relationship.

### LANGUAGE

Used for parsed CV languages.

Target domain:

- Language reference catalog;
- ProfileLanguage relationship.

### CERTIFICATION

Used for parsed CV certifications.

Target domain:

- Certification reference catalog;
- ProfileCertification relationship.

### EXPERIENCE

Used for parsed CV experiences.

Target domain:

- WorkExperience.

Experiences are profile-owned data and are not resolved through a central repository.

## Proposal Statuses

The proposal statuses should be:

- PENDING;
- ACCEPTED;
- REJECTED.

### PENDING

The proposal was generated and is waiting for user validation.

### ACCEPTED

The user accepted the proposal.

The backend applied the corresponding update.

### REJECTED

The user rejected the proposal.

No profile update was made.

## Proposed Data Model

### ProfileEnrichmentProposal

Recommended fields:

id

Primary key.

profile_id

Foreign key to profiles.id.

cv_id

Foreign key to cvs.id.

proposal_type

Type of proposal.

Allowed values:

- PROFILE_FIELD;
- SKILL;
- LANGUAGE;
- CERTIFICATION;
- EXPERIENCE.

status

Current proposal status.

Allowed values:

- PENDING;
- ACCEPTED;
- REJECTED.

source_field

Name of the parsed CV field that generated the proposal.

Examples:

- full_name;
- professional_title;
- skills;
- languages;
- certifications;
- experiences.

target_field

Target field or target domain.

Examples:

- full_name;
- current_title;
- profile_skill;
- profile_language;
- profile_certification;
- work_experience.

observed_value

Raw value detected from the parsed CV.

normalized_value

Normalized value used for comparison.

current_profile_value

Current value in the profile when relevant.

proposed_value

Value proposed for update or creation.

reference_id

Optional ID of a matched reference entity.

Examples:

- skill_id;
- language_id;
- certification_id.

conflict_detected

Boolean flag indicating whether the proposal represents a conflict with existing profile data.

rejection_reason

Optional text field for future use.

created_at

Creation timestamp.

validated_at

Timestamp set when accepted or rejected.

## Repository Resolution

### Skills

For every parsed skill:

1. Normalize the parsed skill value.
2. Search existing Skill records using normalized comparison.
3. If a matching Skill exists, generate a ProfileSkill proposal using the existing Skill.
4. If no Skill exists, generate a proposal without creating a new Skill.
5. Do not create a Skill automatically.

### Languages

For every parsed language:

1. Normalize the parsed language value.
2. Search existing Language records using normalized comparison.
3. If a matching Language exists, generate a ProfileLanguage proposal using the existing Language.
4. If no Language exists, generate a proposal without creating a new Language.
5. Do not create a Language automatically.

### Certifications

For every parsed certification:

1. Normalize the parsed certification value.
2. Search existing Certification records using normalized comparison.
3. If a matching Certification exists, generate a ProfileCertification proposal using the existing Certification.
4. If no Certification exists, generate a proposal without creating a new Certification.
5. Do not create a Certification automatically.

### Experiences

Experiences are not reference data.

For each parsed experience:

1. Normalize title and description when available.
2. Compare with existing WorkExperience records for the profile.
3. If no similar experience exists, generate an EXPERIENCE proposal.
4. If a similar experience exists with different details, generate a conflict proposal.
5. Do not create WorkExperience automatically.

## Normalization Rules

The enrichment service should apply simple deterministic normalization.

Recommended normalization rules:

- trim leading and trailing spaces;
- lowercase comparison value;
- collapse duplicate spaces;
- remove simple punctuation differences where safe;
- preserve the original observed value for display and traceability.

The system must store both:

- observed_value;
- normalized_value.

## Proposal Generation Workflow

Endpoint:

POST /cvs/{cv_id}/enrichment/generate

Workflow:

1. Load CV by cv_id.
2. If CV does not exist, return 404.
3. Load related Profile.
4. If Profile does not exist, return 404.
5. Run or reuse CV parsing output.
6. Produce ParsedCVData.
7. Compare ParsedCVData against the Profile.
8. Resolve Skills, Languages and Certifications against repositories.
9. Generate proposals.
10. Store proposals as PENDING.
11. Return the generated proposals.

Important design decision:

For the first backend implementation, the service can call parse_cv_file again when generating proposals.

Persisting parsed CV data is out of scope unless a dedicated ParsedCV storage model is added later.

## Duplicate Proposal Handling

The service must avoid generating duplicate PENDING proposals for the same:

- profile_id;
- cv_id;
- proposal_type;
- normalized_value;
- target_field.

Recommended MVP behavior:

Before creating a new proposal, check whether an equivalent PENDING proposal already exists.

If yes, do not create a duplicate.

## Proposal Listing Workflow

Endpoint:

GET /profiles/{profile_id}/enrichment

Workflow:

1. Load Profile.
2. If Profile does not exist, return 404.
3. Return all enrichment proposals for the profile.
4. Recommended default ordering:
   - newest first;
   - PENDING proposals first.

Optional future filters:

- status;
- cv_id;
- proposal_type.

Filters are not required for the first MVP implementation.

## Proposal Acceptance Workflow

Endpoint:

POST /enrichment/{proposal_id}/accept

Workflow:

1. Load proposal.
2. If proposal does not exist, return 404.
3. If proposal status is not PENDING, reject the action.
4. Apply the proposal according to proposal_type.
5. Set proposal status to ACCEPTED.
6. Set validated_at.
7. Commit transaction.
8. Return updated proposal.

### Acceptance Rules By Type

#### PROFILE_FIELD

Allowed target fields for MVP:

- full_name;
- current_title.

Behavior:

- update Profile.full_name or Profile.current_title;
- do not update fields that do not exist on the Profile model;
- do not apply summary because Profile.summary does not exist.

#### SKILL

If reference_id points to an existing Skill:

- create ProfileSkill if it does not already exist.

If reference_id is null:

- do not create Skill automatically;
- the proposal cannot be applied directly in MVP;
- keep the proposal pending or mark it as rejected through user action.

Recommended MVP choice:

Only accept SKILL proposals with a resolved Skill reference.

#### LANGUAGE

If reference_id points to an existing Language:

- create ProfileLanguage if it does not already exist.

If reference_id is null:

- do not create Language automatically.

Recommended MVP choice:

Only accept LANGUAGE proposals with a resolved Language reference.

#### CERTIFICATION

If reference_id points to an existing Certification:

- create ProfileCertification if it does not already exist.

If reference_id is null:

- do not create Certification automatically.

Recommended MVP choice:

Only accept CERTIFICATION proposals with a resolved Certification reference.

#### EXPERIENCE

Create WorkExperience for the profile using the proposed experience data.

Because the current parser only partially structures experiences, the first implementation should keep this conservative.

If only a title and description are available:

- create WorkExperience only if required fields can be safely populated;
- otherwise do not apply automatically.

Recommended MVP choice:

Generate EXPERIENCE proposals, but defer acceptance implementation if WorkExperience requires fields that the parser does not reliably provide.

## Proposal Rejection Workflow

Endpoint:

POST /enrichment/{proposal_id}/reject

Workflow:

1. Load proposal.
2. If proposal does not exist, return 404.
3. If proposal status is not PENDING, reject the action.
4. Set status to REJECTED.
5. Set validated_at.
6. Commit transaction.
7. Return updated proposal.

Rejecting a proposal must not modify Profile or any related profile table.

## API Design

### Generate proposals

POST /cvs/{cv_id}/enrichment/generate

Response:

list[ProfileEnrichmentProposalResponse]

Purpose:

Generate PENDING proposals from a parsed CV.

### List proposals for profile

GET /profiles/{profile_id}/enrichment

Response:

list[ProfileEnrichmentProposalResponse]

Purpose:

Display enrichment proposals in the Profile page.

### Accept proposal

POST /enrichment/{proposal_id}/accept

Response:

ProfileEnrichmentProposalResponse

Purpose:

Apply one proposal after user validation.

### Reject proposal

POST /enrichment/{proposal_id}/reject

Response:

ProfileEnrichmentProposalResponse

Purpose:

Reject one proposal after user validation.

## Pydantic Schemas

### ProfileEnrichmentProposalResponse

Fields:

- id;
- profile_id;
- cv_id;
- proposal_type;
- status;
- source_field;
- target_field;
- observed_value;
- normalized_value;
- current_profile_value;
- proposed_value;
- reference_id;
- conflict_detected;
- rejection_reason;
- created_at;
- validated_at.

### ProfileEnrichmentGenerateResponse

Recommended first version:

list[ProfileEnrichmentProposalResponse]

A wrapper schema is optional and can be added later if metadata is needed.

## Service Design

### ProfileEnrichmentService

Recommended service methods:

generate_proposals_for_cv(
cv_id,
db,
)

Responsibilities:

- load CV;
- load Profile;
- parse CV;
- compare parsed data with profile data;
- generate proposals;
- avoid duplicates;
- persist proposals.

accept_proposal(
proposal_id,
db,
)

Responsibilities:

- load proposal;
- validate status;
- apply change;
- set status to ACCEPTED;
- commit.

reject_proposal(
proposal_id,
db,
)

Responsibilities:

- load proposal;
- validate status;
- set status to REJECTED;
- commit.

normalize_value(
value,
)

Responsibilities:

- produce deterministic comparison value.

resolve_skill(
value,
db,
)

Responsibilities:

- find matching Skill.

resolve_language(
value,
db,
)

Responsibilities:

- find matching Language.

resolve_certification(
value,
db,
)

Responsibilities:

- find matching Certification.

## Conflict Detection

### Profile field conflict

A conflict exists when:

- parsed value is not empty;
- current profile value is not empty;
- normalized parsed value differs from normalized profile value.

Examples:

Profile.full_name:
Vincent Gueret

CV.full_name:
Vincent Guéret

Result:

PROFILE_FIELD proposal with conflict_detected = true.

### Current title conflict

Mapping:

ParsedCVData.professional_title
↓
Profile.current_title

If values differ, generate a PROFILE_FIELD proposal with conflict_detected = true.

### Skill conflict

For MVP, skill conflict detection should stay simple.

If the Skill is already linked to the Profile, do not generate a duplicate proposal.

Future versions may compare years of experience or level if the parser supports those fields.

### Language conflict

For MVP, language conflict detection should stay simple.

If the Language is already linked to the Profile, do not generate a duplicate proposal.

Future versions may compare proficiency level if the parser supports it.

### Certification conflict

If the Certification is already linked to the Profile, do not generate a duplicate proposal.

### Experience conflict

Experience conflict detection is limited because the parser currently does not reliably extract company, start date or end date.

Recommended MVP behavior:

- generate proposal only when parsed experience text does not already appear in existing WorkExperience title or description;
- avoid complex matching.

## Important Limitations From Current Parser

The parser currently extracts experiences in a limited way.

The ParsedCVExperience schema supports:

- title;
- company;
- start_date;
- end_date;
- description.

However, the current parser mostly fills:

- title;
- description.

Therefore, backend design must not assume that company, start_date or end_date are available.

The parser also extracts summary, but Profile does not currently have a summary field.

Therefore, summary must not be applied to the Profile in this phase.

## Database Migration

The backend implementation phase will require one new database table:

profile_enrichment_proposals

Expected columns:

- id;
- profile_id;
- cv_id;
- proposal_type;
- status;
- source_field;
- target_field;
- observed_value;
- normalized_value;
- current_profile_value;
- proposed_value;
- reference_id;
- conflict_detected;
- rejection_reason;
- created_at;
- validated_at.

Foreign keys:

- profile_id references profiles.id;
- cv_id references cvs.id.

Indexes recommended:

- profile_id;
- cv_id;
- status;
- proposal_type.

## Transaction Rules

Proposal acceptance must be transactional.

If applying a proposal fails:

- the proposal must remain PENDING;
- no partial profile update should be committed.

Rejecting a proposal only updates the proposal itself.

Generating proposals should commit only after all proposals for a CV have been prepared.

## Error Handling

### CV not found

Return 404.

### Profile not found

Return 404.

### Proposal not found

Return 404.

### Proposal already processed

Return 400.

### Parsing failed

Return 400 and keep or set CV parsing_status to FAILED.

### Unsupported proposal acceptance

Return 400.

Example:

Trying to accept a Skill proposal with no resolved Skill reference.

## Testing Strategy

Tests should be created in:

backend/tests/test_profile_enrichment.py

### Generation tests

- test_generate_profile_field_proposal_from_professional_title
- test_generate_skill_proposal_from_parsed_cv
- test_generate_language_proposal_from_parsed_cv
- test_generate_certification_proposal_from_parsed_cv
- test_generate_experience_proposal_from_parsed_cv
- test_generate_does_not_update_profile
- test_generate_does_not_create_reference_data
- test_generate_avoids_duplicate_pending_proposals

### Conflict tests

- test_detect_full_name_conflict
- test_detect_current_title_conflict
- test_no_conflict_when_values_match

### Acceptance tests

- test_accept_profile_field_proposal_updates_profile
- test_accept_skill_proposal_creates_profile_skill
- test_accept_language_proposal_creates_profile_language
- test_accept_certification_proposal_creates_profile_certification
- test_accept_rejects_unresolved_reference_proposal
- test_accept_rejects_non_pending_proposal

### Rejection tests

- test_reject_proposal_sets_status_rejected
- test_reject_does_not_update_profile
- test_reject_rejects_non_pending_proposal

### API tests

- test_generate_enrichment_endpoint
- test_list_profile_enrichment_endpoint
- test_accept_enrichment_endpoint
- test_reject_enrichment_endpoint

## Frontend Impact

No frontend implementation is included in this phase.

However, the future frontend will need:

- list of proposals;
- proposal type;
- proposed value;
- current profile value;
- conflict indicator;
- accept action;
- reject action.

The frontend must not decide how to apply a proposal.

The frontend only calls backend endpoints.

## Out Of Scope

The following items are out of scope for this phase:

- AI enrichment;
- LLM analysis;
- embeddings;
- semantic matching;
- automatic profile update;
- automatic repository creation;
- advanced duplicate detection;
- profile summary field creation;
- frontend implementation;
- UX design;
- bulk accept;
- bulk reject;
- enrichment scoring;
- confidence calculation based on AI.

## Decisions

### DEC-7.1.16.14.6-001

A new profile_enrichment backend package will own enrichment proposal logic.

### DEC-7.1.16.14.6-002

ProfileEnrichmentProposal is the central model for controlled enrichment.

### DEC-7.1.16.14.6-003

The backend generates proposals but does not update Profile automatically.

### DEC-7.1.16.14.6-004

Only accepted proposals may update Profile or related profile data.

### DEC-7.1.16.14.6-005

Skills, Languages and Certifications must reuse existing repositories whenever possible.

### DEC-7.1.16.14.6-006

Automatic repository creation is excluded from the MVP.

### DEC-7.1.16.14.6-007

ParsedCVData.summary will not be applied until Profile has a dedicated summary field.

### DEC-7.1.16.14.6-008

Experience enrichment will remain conservative because the current parser does not reliably extract all WorkExperience fields.

## Criteria Of Completion

This design phase is complete when:

- backend architecture is defined;
- proposal model is defined;
- proposal lifecycle is defined;
- repository resolution strategy is defined;
- conflict handling strategy is defined;
- endpoints are defined;
- test strategy is defined;
- out-of-scope items are documented;
- no production code has been created during this phase.

## Next Phase

7.1.16.14.7 Backend Implementation

Objective:

Implement the backend foundation for Profile Enrichment.

Expected start-of-phase audit:

Before generating code, request and review the current versions of:

- backend/app/main.py;
- backend/app/core/database.py;
- backend/app/profile/profile_skill_models.py;
- backend/app/profile/profile_skill_schemas.py;
- backend/app/profile/profile_skill_router.py;
- backend/app/languages/models.py;
- backend/app/languages/schemas.py;
- backend/app/languages/router.py;
- backend/app/certifications/models.py;
- backend/app/certifications/schemas.py;
- backend/app/certifications/router.py;
- backend/app/experience/models.py;
- backend/app/experience/schemas.py;
- backend/app/experience/router.py.

No implementation should start without reviewing the real current files.
