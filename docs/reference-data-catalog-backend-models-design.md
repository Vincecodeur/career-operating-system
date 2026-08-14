# Reference Data Catalog Backend Models Design

## Phase

7.1.16.17.2 Backend Models Design

---

## Objective

Define the backend model structure required to implement controlled reference data catalogs.

This phase only defines the models.

No database update is performed.

No API implementation is performed.

No frontend work is performed.

---

## Design Goals

The Reference Data Catalog must provide reusable controlled values.

These values will eventually support:

- profile preferences;
- profile normalization;
- CV enrichment;
- matching;
- opportunity filtering;
- analytics.

---

## Scope

The MVP scope contains only:

Country

WorkMode

ContractType

---

## Out Of Scope

Language

Skill

Certification

Profile migration

Matching changes

Frontend integration

Administration interfaces

---

## Existing Repository Alignment

The project already contains the following controlled entities:

Skill

Language

Certification

The new models must follow the same SQLAlchemy patterns.

---

## Package Location

New package:

backend/app/reference_data

Expected structure:

backend/app/reference_data/
│
├── models.py
├── schemas.py
├── router.py
├── service.py
└── **init**.py

---

## Shared Design Principles

### Principle 1

Every catalog entry has a stable identifier.

---

### Principle 2

Display names may evolve.

Codes remain stable.

---

### Principle 3

Matching and business logic should rely on codes.

Not labels.

---

### Principle 4

Catalog entries are reusable.

They are not profile-specific.

---

## Country Model

Purpose:

Store controlled country values.

Table:

countries

---

### Fields

id

Integer

Primary Key

---

code

String(10)

Unique

Not Null

---

name

String(255)

Unique

Not Null

---

created_at

DateTime

Default datetime.utcnow

---

### Examples

FR

France

---

GB

United Kingdom

---

PT

Portugal

---

US

United States

---

## WorkMode Model

Purpose:

Store controlled working arrangements.

Table:

work_modes

---

### Fields

id

Integer

Primary Key

---

code

String(50)

Unique

Not Null

---

name

String(255)

Not Null

---

created_at

DateTime

Default datetime.utcnow

---

### Examples

REMOTE

Remote

---

HYBRID

Hybrid

---

ONSITE

On-site

---

## ContractType Model

Purpose:

Store controlled employment models.

Table:

contract_types

---

### Fields

id

Integer

Primary Key

---

code

String(50)

Unique

Not Null

---

name

String(255)

Not Null

---

created_at

DateTime

Default datetime.utcnow

---

### Examples

PERMANENT

Permanent

---

FIXED_TERM

Fixed-Term

---

FREELANCE

Freelance

---

CONTRACTOR

Contractor

---

INTERNSHIP

Internship

---

APPRENTICESHIP

Apprenticeship

---

## SQLAlchemy Convention

Models should follow existing repository patterns.

Example:

class Country(Base):

    __tablename__ = "countries"

Follow:

Mapped

mapped_column

DateTime

datetime.utcnow

---

## Relationship Strategy

No relationships are added during MVP implementation.

Country

WorkMode

ContractType

remain standalone catalogs.

---

## Profile Integration Strategy

Not implemented during this phase.

Current profile fields remain unchanged.

Current fields:

location

remote_preference

preferred_countries

remain String fields.

---

## Future Profile Migration

Future profile model may evolve toward:

country_id

work_mode_id

preferred_country_ids

This is outside the current phase.

---

## API Impact

Future APIs:

GET /reference-data/countries

GET /reference-data/work-modes

GET /reference-data/contract-types

No write endpoints planned.

---

## Validation Rules

Country

Unique code

Unique name

---

WorkMode

Unique code

---

ContractType

Unique code

---

## Seed Compatibility

Models are designed to support Git-managed seed files.

Expected future files:

countries.json

work_modes.json

contract_types.json

---

## Matching Compatibility

Matching services should use catalog codes later.

No matching changes are introduced in this phase.

---

## CV Enrichment Compatibility

Future enrichment workflows may resolve values against:

Country

WorkMode

ContractType

No enrichment changes are introduced in this phase.

---

## Testing Impact

Future tests:

Model creation

Uniqueness validation

Schema validation

API validation

Seed validation

---

## Expected Deliverables

backend/app/reference_data/models.py

Country

WorkMode

ContractType

---

backend/app/reference_data/schemas.py

CountryCreate

CountryResponse

WorkModeCreate

WorkModeResponse

ContractTypeCreate

ContractTypeResponse

---

## Implementation Recommendation

Implement the models first.

Do not modify:

Profile

Matching

Profile Enrichment

Frontend

until reference catalogs are stable.

---

## Design Conclusion

The MVP Reference Data Catalog is implemented as three standalone controlled catalogs:

Country

WorkMode

ContractType

The catalogs are intentionally isolated from existing profile data.

This minimizes implementation risk and creates a reusable foundation for future normalization and matching improvements.
