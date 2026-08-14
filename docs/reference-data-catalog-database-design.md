# Reference Data Catalog Database Design

## Phase

7.1.16.17.3 Database Schema Update Design

---

## Objective

Define how the new Reference Data Catalog models are integrated into the existing database schema.

The project currently does not use Alembic.

Database evolution follows the existing SQLAlchemy strategy already used throughout the repository.

This phase only defines the database update strategy.

No API implementation is performed.

No seed implementation is performed.

---

## Existing Situation

Current reference models:

Skill

Language

Certification

New models already implemented:

Country

WorkMode

ContractType

---

## Existing Database Strategy

The project currently relies on SQLAlchemy models.

No Alembic migration framework is installed.

No migration history was identified during repository audit.

Database evolution currently follows:

Model creation

↓

Metadata registration

↓

Table creation

↓

Validation

---

## Design Principles

### Principle 1

Reuse existing project patterns.

Do not introduce Alembic during MVP implementation.

---

### Principle 2

Keep changes isolated.

Do not modify Profile tables during this phase.

---

### Principle 3

Create only the required tables.

Avoid premature normalization.

---

### Principle 4

Protect existing functionality.

Current profile behavior must remain unchanged.

---

## New Tables

The following tables must be created.

### countries

Fields:

id

code

name

created_at

---

### work_modes

Fields:

id

code

name

created_at

---

### contract_types

Fields:

id

code

name

created_at

---

## Profile Impact

No Profile changes during this phase.

Current fields remain unchanged:

location

remote_preference

preferred_countries

Current storage remains:

String

String

String

---

## Relationship Strategy

No foreign keys added during this phase.

Reason:

The catalogs must exist and be validated first.

---

## Future Relationship Strategy

Future profile evolution may introduce:

country_id

preferred_country_ids

work_mode_id

contract_type_id

This is out of scope for the current phase.

---

## Metadata Registration

The new models must be imported and registered so they are included in the SQLAlchemy metadata.

Validation criteria:

Country visible in metadata

WorkMode visible in metadata

ContractType visible in metadata

---

## Table Creation Strategy

Target state:

countries table exists

work_modes table exists

contract_types table exists

Existing tables remain unchanged.

---

## Validation Strategy

Validation must confirm:

Country table creation

WorkMode table creation

ContractType table creation

No regression on existing tables

Backend startup remains operational

---

## Out Of Scope

Seed data

Reference APIs

Profile migration

Matching integration

Frontend integration

Administration UI

---

## Risks

### Risk 1

Accidental Profile modifications.

Mitigation:

No Profile changes allowed during this phase.

---

### Risk 2

Breaking database startup.

Mitigation:

Validate metadata registration before startup validation.

---

### Risk 3

Premature foreign keys.

Mitigation:

Keep catalogs standalone.

---

## Expected Deliverables

Database recognizes:

Country

WorkMode

ContractType

Tables exist:

countries

work_modes

contract_types

No functional behavior changes.

---

## Exit Criteria

Database schema update phase is complete when:

Country table exists

WorkMode table exists

ContractType table exists

Backend startup succeeds

No existing tests regress

No Profile schema changes introduced

Working tree remains clean after validation

---

## Next Phase

7.1.16.17.4 Seed Data

Objective:

Populate Country

Populate WorkMode

Populate ContractType

using controlled data stored in Git.
