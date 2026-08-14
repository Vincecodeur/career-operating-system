# Reference Data Catalog Repository Audit

## Phase

7.1.16.17.1 Repository Audit

---

## Objective

Audit the real repository structure before implementing the Reference Data Catalog.

The purpose of this audit is to:

- identify existing reference-style domains;
- identify reusable patterns;
- verify SQLAlchemy conventions;
- verify schema conventions;
- identify profile fields impacted by normalization;
- identify implementation risks;
- define the safest implementation strategy.

No code is implemented during this phase.

---

## Audit Scope

Repository areas reviewed:

backend/app/skills

backend/app/languages

backend/app/certifications

backend/app/profile

backend/app/profile_enrichment

backend/app/core

---

## Existing Backend Structure

Current backend structure is organized by business domains.

Observed packages:

applications

auth

certifications

core

cv

experience

jobs

languages

matching

profile

profile_enrichment

skills

---

## Existing Reference-Like Domains

Several existing domains already behave like controlled reference data.

Current catalogs:

Skill

Language

Certification

These domains already provide:

- dedicated SQLAlchemy models;
- dedicated schemas;
- CRUD endpoints;
- frontend consumption.

---

## Missing Reference Domains

The following catalogs do not currently exist.

Country

WorkMode

ContractType

They must be implemented during this phase.

---

## Existing SQLAlchemy Convention

Observed convention:

- SQLAlchemy 2 style;
- Mapped typing;
- mapped_column usage.

Example pattern:

id

name

created_at

All future models must follow the same pattern.

---

## Existing Pydantic Convention

Observed convention:

BaseModel

Response schemas expose:

model_config = {
"from_attributes": True
}

Future schemas must follow the same convention.

---

## Existing Skill Catalog Analysis

Current model:

Skill

Current fields:

id

name

category

created_at

The Skill catalog is currently the closest implementation to a managed reference catalog.

Strengths:

- simple;
- reusable;
- easy to expose through APIs.

Limitations:

- no immutable code field;
- cannot safely support aliases;
- unsuitable as a template for country identifiers.

---

## Existing Language Catalog Analysis

Current model:

Language

Current purpose:

Controlled language catalog used by profile language relationships.

This confirms that the application already supports the concept of reusable reference entities.

---

## Existing Certification Catalog Analysis

Current model:

Certification

Current purpose:

Controlled certification catalog reused by profile certifications.

This further validates the reference-data pattern already present in the project.

---

## Existing Profile Model Analysis

Current file:

backend/app/profile/models.py

Observed fields potentially impacted by Reference Data Catalog:

location

remote_preference

preferred_countries

Current implementation:

location = String

remote_preference = String

preferred_countries = String

---

## Current Profile Limitation

Current profile preferences are stored as free text.

Examples:

Remote

Hybrid

France

Portugal

United Kingdom

No controlled reference validation currently exists.

Potential consequences:

- inconsistent spelling;
- difficult filtering;
- difficult matching;
- duplicate values.

---

## Profile Normalization Strategy

The profile should not be modified immediately.

Recommended order:

Step 1

Implement reference catalogs.

Step 2

Expose APIs.

Step 3

Seed data.

Step 4

Validate backend.

Step 5

Migrate profile preference fields.

This reduces project risk.

---

## Existing Profile Enrichment Analysis

Current enrichment workflow already contains:

Reference Data Governance

Repository Resolution Strategy

Conflict Resolution Workflow

Skill Catalog Mapping

This is important because:

Reference Data Catalog implementation can reuse the exact same governance concepts.

---

## Existing Matching Analysis

Matching V2 already contains:

Work Mode Explanation

Location Explanation

Contract Match Concepts

Future catalog implementation can improve consistency.

No matching refactor should be performed during the first implementation phase.

---

## Existing Frontend Impact

Current frontend consumes:

Skills

Languages

Certifications

Future frontend consumers will include:

Countries

Work Modes

Contract Types

The frontend already contains reusable CRUD and selector patterns.

---

## Recommended Package Strategy

Create a dedicated package.

Recommended location:

backend/app/reference_data

Structure:

models.py

schemas.py

router.py

service.py

**init**.py

Reason:

Country

WorkMode

ContractType

share the same business responsibility.

---

## Alternative Strategy Considered

Alternative:

backend/app/countries

backend/app/work_modes

backend/app/contract_types

Rejected because:

- more boilerplate;
- duplicated APIs;
- duplicated services;
- duplicated tests.

A shared package is simpler.

---

## Recommended Country Model

Fields:

id

code

name

created_at

Examples:

FR
France

GB
United Kingdom

PT
Portugal

US
United States

---

## Recommended WorkMode Model

Fields:

id

code

name

created_at

Examples:

REMOTE
Remote

HYBRID
Hybrid

ONSITE
On-site

---

## Recommended ContractType Model

Fields:

id

code

name

created_at

Examples:

PERMANENT
Permanent

FIXED_TERM
Fixed-Term

FREELANCE
Freelance

CONTRACTOR
Contractor

INTERNSHIP
Internship

APPRENTICESHIP
Apprenticeship

---

## Recommended API Scope

MVP APIs should be read-only.

Countries:

GET /reference-data/countries

Work Modes:

GET /reference-data/work-modes

Contract Types:

GET /reference-data/contract-types

No administration endpoints should be implemented.

---

## Seed Data Strategy

Expected seed files:

countries.json

work_modes.json

contract_types.json

Recommended location:

backend/app/reference_data/seeds

Catalog data should be versioned in Git.

No administration UI required.

---

## Migration Assessment

Migration structure was not audited during this phase.

Unknown:

- Alembic location;
- migration naming convention;
- migration workflow.

This must be verified before creating database tables.

---

## Countries Scope

Initial scope should remain limited.

Recommended:

France

United Kingdom

Portugal

Spain

Germany

Italy

Belgium

Netherlands

United States

Canada

Future countries can be added later.

---

## Work Mode Scope

Initial scope:

REMOTE

HYBRID

ONSITE

No additional values required.

---

## Contract Type Scope

Initial scope:

PERMANENT

FIXED_TERM

FREELANCE

CONTRACTOR

INTERNSHIP

APPRENTICESHIP

No additional values required.

---

## Matching Impact

Out of scope for this phase:

Matching algorithm changes.

Only the catalogs should be introduced.

Matching integration should happen after catalog validation.

---

## Profile Impact

Out of scope for this phase:

Profile schema migration.

Current profile behavior must remain operational.

---

## Frontend Impact

Out of scope for this phase:

Settings forms

Profile preferences forms

Opportunity filters

These changes should occur after backend validation.

---

## Risks

Risk 1

Premature profile migration.

Mitigation:

Keep profile fields unchanged initially.

---

Risk 2

Reference data duplication.

Mitigation:

Single source of truth inside Reference Data package.

---

Risk 3

Frontend coupling.

Mitigation:

Complete backend validation before frontend integration.

---

## Recommended Implementation Order

7.1.16.17.2 Backend Models

Create:

Country

WorkMode

ContractType

---

7.1.16.17.3 Database Migration

Create:

countries

work_modes

contract_types

tables.

---

7.1.16.17.4 Seed Data

Create:

countries.json

work_modes.json

contract_types.json

---

7.1.16.17.5 Backend APIs

Expose read-only endpoints.

---

7.1.16.17.6 Backend Tests

Model tests

API tests

Seed validation tests

---

7.1.16.17.7 Backend Validation

Pytest

Swagger

Database validation

---

## Audit Conclusion

The repository is ready for Reference Data Catalog implementation.

Current architecture already contains successful examples of controlled entities:

Skill

Language

Certification

The safest implementation strategy is:

- create a dedicated Reference Data package;
- introduce Country;
- introduce WorkMode;
- introduce ContractType;
- expose read-only APIs;
- seed catalog values;
- validate backend;
- postpone profile migration until the catalog foundation is stable.

This approach minimizes risk while preparing future work on:

- profile preferences;
- opportunity filters;
- matching;
- CV enrichment;
- analytics.
