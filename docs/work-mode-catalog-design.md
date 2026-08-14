# Work Mode Catalog Design

## Phase

7.1.16.16.4 Work Mode Catalog Design

---

## Objective

Introduce a normalized Work Mode Catalog used consistently across:

- candidate profiles;
- candidate preferences;
- job opportunities;
- matching;
- filtering;
- reporting.

The goal is to standardize how working arrangements are represented throughout the system.

---

## Problem Statement

Different data sources may use different terminology.

Examples:

Remote
Fully Remote
Work From Home
Telework

Hybrid
Flexible Hybrid
Partial Remote

On Site
Office
Presential

These variations create inconsistencies and complicate filtering and matching.

---

## Design Principles

### Principle 1

One work mode = one canonical value.

---

### Principle 2

Profiles and opportunities reference the same catalog.

---

### Principle 3

Matching must compare normalized values.

---

### Principle 4

Work mode values are controlled.

No free-text work mode values.

---

## Initial Catalog Scope

Three official values:

REMOTE

HYBRID

ONSITE

---

## Catalog Structure

WorkMode

Fields:

id
code
name

Example:

REMOTE
Remote

HYBRID
Hybrid

ONSITE
On-site

---

## Profile Usage

Profiles may define preferred work arrangements.

Examples:

Remote

Hybrid

Remote + Hybrid

The profile stores references to catalog entries.

---

## Opportunity Usage

Job opportunities should progressively reference the same catalog.

Examples:

Job A

Work Mode:
REMOTE

---

Job B

Work Mode:
HYBRID

---

Job C

Work Mode:
ONSITE

---

## Matching Impact

Matching becomes deterministic.

Example:

Candidate Preference:

REMOTE

Opportunity:

REMOTE

Result:

Full match

---

Candidate Preference:

REMOTE

Opportunity:

HYBRID

Result:

Partial match

---

Candidate Preference:

ONSITE

Opportunity:

REMOTE

Result:

No match

---

## Matching Scoring Strategy

Future scoring may use:

Exact Match

Preferred Match

Acceptable Match

Non-Match

Exact scoring rules are outside this phase.

---

## Search Filters

Future filters:

Remote

Hybrid

On-site

Remote + Hybrid

All modes

---

## Opportunity Analysis

The system can explain:

Candidate Preference:
Remote

Opportunity:
Hybrid

Result:

Preference partially satisfied

---

## CV Parsing Impact

Work mode information may appear in a CV.

Examples:

Remote worker

Hybrid environment

Office-based position

The parser should normalize these values to the catalog when possible.

---

## Alias Strategy

Examples:

Remote

Aliases:

Work From Home
WFH
Telework
Fully Remote

---

Hybrid

Aliases:

Flexible Hybrid
Partial Remote

---

On-site

Aliases:

Office
Presential
Office-based

---

## Future Alias Model

WorkModeAlias

Fields:

id
work_mode_id
alias

Not required during MVP.

---

## Analytics Impact

Future reports:

Most common work mode

Most demanded work mode

Work mode trends

Remote opportunity growth

Hybrid adoption trends

---

## Backend Impact

Potential entities:

WorkMode
WorkModeAlias

Reference Data package reuse.

---

## Frontend Impact

Current:

No standardized work mode selector.

Future:

Dropdown selector

Autocomplete selector

Filter component

Shared preference component

---

## Seed Strategy

work_modes.json

Content:

REMOTE
HYBRID
ONSITE

The catalog is maintained in Git.

No administration interface required for MVP.

---

## Example End-To-End Flow

Candidate Preference:

Remote

↓

Resolution

↓

REMOTE

↓

Stored In Database

↓

Matching

↓

Filtering

↓

Analytics

---

## Expected Outcome

The system gains:

- consistent work mode vocabulary;
- more reliable matching;
- cleaner filtering;
- standardized job preferences;
- future reporting capabilities.

The Work Mode Catalog becomes the official source of truth for working arrangement preferences and opportunity classification.
