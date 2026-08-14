# Preference Options Design

## Phase

7.1.16.16.6 Preference Options Design

---

## Objective

Define the future candidate preference model.

The objective is to provide structured preferences that can be used consistently by:

- job discovery;
- opportunity filtering;
- matching;
- ranking;
- analytics;
- future career planning.

Candidate preferences are not profile skills.

They represent the candidate's desired working conditions.

---

## Design Principles

### Principle 1

Preferences are structured.

Preferences must not rely on uncontrolled free-text values.

---

### Principle 2

Preferences support matching.

Every preference should be reusable by the matching engine.

---

### Principle 3

Preferences remain optional.

Missing preferences must not block profile creation.

---

### Principle 4

Preferences are candidate-centric.

Preferences describe what the candidate wants.

They do not describe the candidate's experience.

---

## Preference Domains

Initial MVP scope:

- Work Mode Preferences
- Country Preferences
- Contract Type Preferences
- Relocation Preferences
- Travel Preferences

---

## Work Mode Preferences

Purpose:

Define preferred working arrangements.

Reference Catalog:

WorkMode

Values:

REMOTE
HYBRID
ONSITE

Example:

Candidate accepts:

REMOTE
HYBRID

---

## Country Preferences

Purpose:

Define preferred work locations.

Reference Catalog:

Country

Examples:

FR
GB
PT

A candidate may select multiple countries.

---

## Contract Type Preferences

Purpose:

Define preferred employment models.

Reference Catalog:

ContractType

Examples:

PERMANENT
FREELANCE

Multiple selections supported.

---

## Relocation Preferences

Purpose:

Specify relocation willingness.

Recommended values:

NO_RELOCATION

RELOCATION_WITHIN_COUNTRY

RELOCATION_INTERNATIONAL

---

## Travel Preferences

Purpose:

Specify acceptable travel frequency.

Recommended values:

NONE

OCCASIONAL

FREQUENT

EXTENSIVE

---

## Future Candidate Preference Model

CandidatePreferences

Fields:

profile_id

preferred_work_modes

preferred_countries

preferred_contract_types

relocation_preference

travel_preference

---

## Matching Impact

Preferences influence opportunity relevance.

Example:

Candidate:

REMOTE

Opportunity:

REMOTE

Result:

Preference satisfied

---

Candidate:

REMOTE

Opportunity:

ONSITE

Result:

Preference not satisfied

---

Candidate:

France

United Kingdom

Opportunity:

United Kingdom

Result:

Country preference satisfied

---

## Ranking Impact

Opportunities aligned with preferences may receive a positive signal.

Opportunities conflicting with preferences may receive a negative signal.

Exact scoring rules are outside this phase.

---

## Search Filter Impact

Preferences may become default filters.

Example:

Candidate Preferences

↓

Opportunity Search

↓

Only compatible opportunities displayed

---

## User Experience

Future profile section:

Preferences

Contains:

Work Modes

Countries

Contract Types

Relocation

Travel

---

## UI Components

Recommended controls:

Autocomplete

Multi-select

Tag selectors

Radio groups

Controlled values only.

No free-text preference inputs.

---

## Job Discovery Integration

Search criteria may progressively reuse preferences.

Example:

Default Search

Countries:

FR
GB

Work Modes:

REMOTE
HYBRID

---

## Analytics Impact

Future reports:

Most common preferred countries

Most common work modes

Most common contract preferences

Relocation willingness distribution

Travel preference distribution

---

## Reference Data Dependencies

Preference management depends on:

Country Catalog

Work Mode Catalog

Contract Type Catalog

Preference values should never duplicate data already managed by reference catalogs.

---

## Future Extensions

Potential additional preferences:

Salary Expectations

Industry Preferences

Company Size Preferences

Management Preferences

Language Preferences

These are outside MVP scope.

---

## Example End-To-End Flow

Profile

↓

Preferences

Countries:
FR
GB

Work Modes:
REMOTE
HYBRID

Contract Types:
PERMANENT

↓

Matching

↓

Opportunity Ranking

↓

User Decision

---

## Expected Outcome

The system gains:

- structured candidate preferences;
- stronger filtering capabilities;
- better opportunity ranking;
- improved matching relevance;
- reusable preference data.

Preference Options become the foundation for future job discovery personalization.
