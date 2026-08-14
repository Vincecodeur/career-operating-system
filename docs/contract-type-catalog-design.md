# Contract Type Catalog Design

## Phase

7.1.16.16.5 Contract Type Catalog Design

---

## Objective

Introduce a normalized Contract Type Catalog used consistently across:

- candidate profiles;
- search preferences;
- job opportunities;
- matching;
- filtering;
- analytics.

The goal is to eliminate contract type inconsistencies and provide a standard employment model reference layer.

---

## Problem Statement

Different job sources use different terminology.

Examples:

Permanent
Full-Time Permanent
CDI

Fixed-Term
Temporary Contract
CDD

Freelance
Contractor
Independent Consultant

Without normalization:

- filters become unreliable;
- matching becomes inconsistent;
- reporting quality decreases;
- duplicate values appear.

---

## Design Principles

### Principle 1

One contract type = one canonical value.

---

### Principle 2

Profiles and opportunities must reference the same catalog.

---

### Principle 3

Users interact with readable labels.

The system stores normalized values.

---

### Principle 4

Contract types are governed reference data.

No free-text contract values.

---

## Initial Catalog Scope

The MVP catalog contains:

PERMANENT

FIXED_TERM

FREELANCE

CONTRACTOR

INTERNSHIP

APPRENTICESHIP

---

## Catalog Structure

ContractType

Fields:

id
code
name

Example:

PERMANENT
Permanent Employee

FIXED_TERM
Fixed-Term Contract

FREELANCE
Freelance

CONTRACTOR
Contractor

INTERNSHIP
Internship

APPRENTICESHIP
Apprenticeship

---

## Candidate Preferences

Profiles may express preferred contract types.

Examples:

Permanent only

Permanent + Freelance

Freelance only

Stored as references to ContractType entries.

---

## Opportunity Classification

Each opportunity should progressively reference a contract type.

Example:

Contract Type:

PERMANENT

instead of:

Permanent Position
CDI
Full-Time Permanent

---

## Matching Impact

Examples

Candidate Preferences:

PERMANENT

Opportunity:

PERMANENT

Result:

Exact match

---

Candidate Preferences:

PERMANENT

Opportunity:

FIXED_TERM

Result:

Non-preferred contract type

---

Candidate Preferences:

FREELANCE
CONTRACTOR

Opportunity:

CONTRACTOR

Result:

Preferred contract type

---

## Matching Scoring

Future matching may include:

Exact Preference Match

Preferred Contract Match

Acceptable Contract Match

Contract Mismatch

Detailed scoring rules are outside this phase.

---

## Search Filters

Future filters:

Permanent

Fixed-Term

Freelance

Contractor

Internship

Apprenticeship

Multiple selections must be supported.

---

## Opportunity Analysis

The system may explain:

Candidate Preference:

Permanent

Opportunity:

Fixed-Term

Result:

Contract type preference not satisfied

---

## CV Parsing Impact

Certain CVs may indicate preferred contract models.

Examples:

Freelance Consultant

Independent Contractor

Permanent Employee

These values may be normalized through the Contract Type Catalog.

---

## Alias Strategy

Examples:

PERMANENT

Aliases:

Permanent
CDI
Full-Time Permanent

---

FIXED_TERM

Aliases:

CDD
Temporary Contract
Fixed-Term Employment

---

FREELANCE

Aliases:

Independent Consultant
Self-Employed

---

CONTRACTOR

Aliases:

Contract Engagement
Contract Resource

---

## Future Alias Model

ContractTypeAlias

Fields:

id
contract_type_id
alias

Not required for MVP.

---

## Analytics Impact

Future analytics become possible.

Examples:

Most Common Contract Types

Contract Type Distribution

Contract Type Market Trends

Preferred Contract Type Trends

---

## Backend Impact

Future package:

backend/app/reference_data/

Potential entities:

ContractType
ContractTypeAlias

Shared normalization services should be reused.

---

## Frontend Impact

Current:

No standardized contract selector.

Future:

Dropdown selector

Autocomplete selector

Filter component

Shared preference component

---

## Seed Strategy

contract_types.json

Initial values:

PERMANENT
FIXED_TERM
FREELANCE
CONTRACTOR
INTERNSHIP
APPRENTICESHIP

Stored and versioned in Git.

No administration UI required for MVP.

---

## Example End-To-End Flow

Candidate Preference:

Permanent

↓

Resolution

↓

PERMANENT

↓

Stored In Database

↓

Matching

↓

Filters

↓

Analytics

---

## Expected Outcome

The system gains:

- consistent contract type vocabulary;
- better matching quality;
- stronger filtering capabilities;
- standardized candidate preferences;
- reusable analytics foundations.

The Contract Type Catalog becomes the official employment model reference layer across the Career Operating System.
