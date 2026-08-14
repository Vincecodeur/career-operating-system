# Reference Data Catalog Design

## Phase

7.1.16.16 Reference Data Catalog Design

---

## Objective

Introduce controlled reference data catalogs to improve:

- profile consistency;
- CV enrichment quality;
- search preference management;
- opportunity filtering;
- matching accuracy;
- future market intelligence.

The system must progressively replace free-text fields with normalized reference entities when the domain is stable and predictable.

---

## Design Principles

### Principle 1

The structured profile remains the source of truth.

Reference data catalogs define valid vocabulary.
Profiles reference catalog entries.

---

### Principle 2

Reference data must be reusable.

The same catalog entry must be usable across:

- profile management;
- CV enrichment;
- opportunity analysis;
- search criteria;
- matching engine.

---

### Principle 3

Reference data is governed.

Reference values are controlled.

No automatic creation is allowed when a missing value could impact:

- matching;
- filtering;
- reporting;
- recommendations.

User validation is required.

---

### Principle 4

Reference data must support normalization.

Different user inputs should resolve to the same canonical value.

Example:

English
english
ENGLISH
Anglais

↓

English

---

## Initial Catalog Scope

### Catalog 1

Skill Catalog

Status:
Existing

Purpose:
Normalize skills used by profiles and jobs.

Current entities:

- Skill
- ProfileSkill
- JobOfferSkill

---

### Catalog 2

Language Catalog

Status:
Existing

Purpose:
Normalize spoken languages.

Current entities:

- Language
- ProfileLanguage

Examples:

- English
- French
- Portuguese
- Spanish

---

### Catalog 3

Country Catalog

Status:
New

Purpose:
Normalize countries used by:

- search preferences;
- job locations;
- remote preferences;
- future market intelligence.

Recommended structure:

## Country

id
iso_code
name

Examples:

FR
GB
PT
ES
CA

---

### Catalog 4

Work Mode Catalog

Status:
New

Purpose:
Normalize work location preferences.

Values:

REMOTE
HYBRID
ONSITE

Examples:

Remote
Hybrid
On-site

---

### Catalog 5

Contract Type Catalog

Status:
New

Purpose:
Normalize employment types.

Recommended values:

PERMANENT
FIXED_TERM
FREELANCE
CONTRACTOR
INTERNSHIP
APPRENTICESHIP

---

### Catalog 6

Preference Options Catalog

Status:
New

Purpose:
Normalize candidate job preferences.

Initial scope:

Work Preference
Location Preference
Travel Preference

---

## Reference Data Ownership

Reference catalogs belong to the system.

Profiles reference catalogs.

Jobs reference catalogs.

CV enrichment proposes mappings to catalogs.

---

## CV Parsing Integration

Current behavior:

CV
↓
Parsing
↓
Structured Extraction

Future behavior:

CV
↓
Parsing
↓
Reference Resolution
↓
Structured Proposal
↓
User Validation
↓
Profile Update

---

## Reference Resolution Strategy

Apply existing strategy:

1. Exact Match
2. Normalized Match
3. Alias Match

No fuzzy matching in MVP.

---

## Backend Architecture

Target package:

backend/app/reference_data/

Proposed structure:

reference_data/
├── models.py
├── schemas.py
├── repository.py
├── service.py
└── router.py

---

## Frontend Impact

Current:

Free text inputs

Future:

Select controls
Autocomplete controls
Reference pickers

Examples:

Languages
Countries
Contract Types
Work Modes

---

## Seed Strategy

MVP approach:

Static seeds stored in Git.

Examples:

backend/seeds/

languages.json
countries.json
work_modes.json
contract_types.json

No administration interface is required for MVP.

---

## Future Extensions

Potential catalogs:

- Education Levels
- Seniority Levels
- Certification Providers
- Industries
- Job Families
- Currency Codes

These items are outside the current phase.

---

## Expected Outcome

The system gains:

- consistent vocabulary;
- improved matching quality;
- improved CV enrichment quality;
- stronger search criteria;
- reusable filtering capabilities;
- easier future analytics implementation.

Reference data becomes a foundational layer shared across the Career Operating System.
