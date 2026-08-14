# Reference Data Seed Design

## Phase

7.1.16.17.4 Seed Data Design

---

## Objective

Populate the Reference Data Catalog tables with controlled values.

Tables:

countries

work_modes

contract_types

---

## Design Principles

Reference data is stored in Git.

Reference data is deterministic.

Reference data is loaded automatically.

Reference data is not managed through the UI.

---

## Storage Location

backend/app/reference_data/seeds

Files:

countries.json

work_modes.json

contract_types.json

---

## Countries

Initial MVP scope:

FR
France

GB
United Kingdom

PT
Portugal

ES
Spain

DE
Germany

IT
Italy

BE
Belgium

NL
Netherlands

US
United States

CA
Canada

---

## Work Modes

REMOTE
Remote

HYBRID
Hybrid

ONSITE
On-site

---

## Contract Types

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

## Loading Strategy

At application startup:

Read JSON files

↓

Check whether records exist

↓

Insert missing values

↓

Keep existing values unchanged

---

## Idempotency Requirement

The seed process must be rerunnable.

Running multiple times must not create duplicates.

---

## Validation Rules

Country code unique

Country name unique

WorkMode code unique

ContractType code unique

---

## Expected Result

countries table populated

work_modes table populated

contract_types table populated

Reference catalogs ready for API exposure.

---

## Next Phase

7.1.16.17.4 Seed Data Implementation
