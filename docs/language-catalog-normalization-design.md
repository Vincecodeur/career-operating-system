# Language Catalog Normalization Design

## Phase

7.1.16.16.2 Language Catalog Normalization Design

---

## Objective

Define a normalized language catalog that becomes the unique source of truth for language references used across:

- candidate profiles;
- CV parsing;
- CV enrichment;
- search preferences;
- matching;
- future analytics.

The goal is to eliminate language duplication and inconsistent naming.

---

## Current Situation

The system already contains:

Language
ProfileLanguage

However, the catalog currently focuses primarily on profile management.

The language catalog must become a reusable reference layer for the entire application.

---

## Problems To Solve

Examples of equivalent values:

English
english
ENGLISH
Anglais

Portuguese
Português
Portugais

Spanish
Español
Espagnol

These variations create:

- duplicate entries;
- inconsistent filtering;
- unreliable matching;
- lower quality analytics.

---

## Design Principles

### Principle 1

One language = one canonical entry.

---

### Principle 2

Profiles reference languages.

They never store language names directly.

---

### Principle 3

Imported CV data must resolve to existing catalog entries whenever possible.

---

### Principle 4

Language catalog values are governed.

No automatic language creation.

---

## Recommended Language Model

Language

Fields:

id
code
name

Example:

EN
English

FR
French

PT
Portuguese

ES
Spanish

DE
German

IT
Italian

NL
Dutch

---

## ISO Strategy

Recommendation:

Use ISO 639-1 language codes.

Examples:

EN
FR
PT
ES
DE
IT
NL

Benefits:

- international standard;
- interoperability;
- future integrations;
- cleaner filtering.

---

## ProfileLanguage Model

Current model remains.

ProfileLanguage

Fields:

profile_id
language_id
proficiency_level

The profile references the catalog.

---

## Language Proficiency Levels

Recommended controlled values:

A1
A2
B1
B2
C1
C2
NATIVE

---

## Proficiency Reference

A1
Beginner

A2
Elementary

B1
Intermediate

B2
Upper Intermediate

C1
Advanced

C2
Proficient

NATIVE
Native Speaker

---

## CV Parsing Resolution

Example:

CV Input:

Anglais

Resolution:

EN
English

---

Example:

CV Input:

Português

Resolution:

PT
Portuguese

---

## Resolution Strategy

Order of execution:

1. Exact Match
2. Normalized Match
3. Alias Match

No fuzzy matching.

---

## Language Alias Support

Future candidate:

LanguageAlias

Fields:

id
language_id
alias

Example:

English

Aliases:

English
anglais

---

Portuguese

Aliases:

Portuguese
Portugais
Português

---

## Matching Impact

Current matching benefits:

- exact language comparison;
- consistent filters;
- cleaner scoring rules.

Future matching benefits:

- proficiency-aware scoring;
- mandatory language checks;
- language gap detection.

---

## Search Criteria Impact

Future filters:

Country
Work Mode
Contract Type

Language requirements

Example:

Required Language:

English

Minimum Level:

B2

---

## Opportunity Analysis Impact

The system can explain:

Required:

English B2

Candidate:

English C1

Result:

Requirement satisfied

---

## Analytics Impact

Future analytics become possible.

Examples:

Most common languages

Most demanded languages

Language trends

Language gaps

---

## Backend Impact

No immediate implementation.

Future package:

backend/app/reference_data/

Possible additions:

LanguageAlias

Shared resolution service

---

## Frontend Impact

Current:

Language selector

Future:

Autocomplete selector

Controlled values only

No free-text language entry.

---

## Seed Strategy

Languages are versioned in Git.

Example:

languages.json

Containing:

EN
FR
PT
ES
DE
IT
NL

Additional languages can be added through future governance processes.

---

## Example End-To-End Flow

CV:

French
English
Português

↓

Parsing

↓

Resolution

↓

FR
EN
PT

↓

ProfileLanguage proposals

↓

User validation

↓

Profile update

---

## Expected Outcome

The system gains:

- consistent language vocabulary;
- stronger matching;
- cleaner filtering;
- better CV enrichment;
- better reporting;
- future multilingual support.

The Language Catalog becomes a shared reference layer across the entire Career Operating System.
