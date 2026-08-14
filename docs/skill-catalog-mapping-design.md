# Skill Catalog Mapping Design

## Phase

7.1.16.16.1 Skill Catalog Mapping Design

---

## Objective

Improve CV enrichment quality by allowing unknown skills extracted from a CV to be mapped to an existing Skill catalog entry before profile update.

The goal is to protect the Skill catalog while reducing manual profile corrections.

---

## Problem Statement

Current situation:

CV
↓
Parsing
↓
Skill Extraction
↓
Enrichment Proposal

Known skills:
accepted normally

Unknown skills:
not automatically added

This protects the catalog but creates additional manual work.

Example:

CV skill:
MS Excel

Catalog skill:
Microsoft Excel

Current behavior:
No match found

Desired behavior:
User maps CV skill to existing catalog entry.

---

## Design Principles

### Principle 1

The Skill catalog remains governed.

No automatic skill creation.

---

### Principle 2

The profile remains the source of truth.

The CV is an observation source.

---

### Principle 3

User validation is mandatory.

The system proposes.

The user decides.

---

### Principle 4

Mapping must be reusable.

Once a mapping is validated it should be reusable by future enrichments.

---

## Mapping Workflow

### Step 1

CV parsing extracts skills.

Example:

Python
Excel
Power BI
MS Excel

---

### Step 2

Resolution engine attempts matching.

Order:

1. Exact Match
2. Normalized Match
3. Alias Match

---

### Step 3

Known skills are automatically linked.

Example:

Python
↓
Skill #12

Power BI
↓
Skill #45

---

### Step 4

Unknown skills generate mapping proposals.

Example:

MS Excel

Status:

UNMAPPED

---

### Step 5

User reviews proposal.

Available actions:

Accept Existing Match
Select Different Skill
Ignore Skill

---

### Step 6

Profile enrichment applies selected mapping.

Example:

MS Excel
↓
Microsoft Excel
↓
ProfileSkill Created

---

## Mapping Statuses

### RESOLVED

Catalog match confirmed.

### UNMAPPED

No match found.

### IGNORED

User intentionally ignored the skill.

### PENDING

Waiting for user decision.

---

## Alias Strategy

Purpose:

Support alternative names.

Examples:

MS Excel
Microsoft Excel

Excel
Microsoft Excel

PowerBI
Power BI

JS
JavaScript

TS
TypeScript

---

## Alias Entity

Future candidate model:

SkillAlias

Fields:

id
skill_id
alias

Example:

skill_id = 45

aliases:

PowerBI
Power BI Desktop

---

## User Experience

Unknown skills appear in a dedicated section:

Unmapped Skills

Example:

⚠ MS Excel
⚠ JS
⚠ PowerBI

For each item:

[Map]
[Ignore]

---

## Mapping Selector

User chooses among existing catalog skills.

Selector type:

Autocomplete

Reason:

Catalog size will grow over time.

---

## Catalog Protection Rules

Allowed:

Map to existing skill

Ignore skill

Not allowed:

Automatic skill creation

Automatic category creation

Automatic catalog modification

---

## Matching Impact

Benefits:

Higher skill normalization

Less catalog duplication

More accurate matching scores

Better analytics

Better future recommendations

---

## Future Enhancement

Potential phase:

Skill Alias Repository

Capabilities:

Store validated aliases

Reuse mappings automatically

Reduce future manual intervention

Not included in MVP.

---

## Example

Parsed Skill:

MS Excel

Catalog:

Microsoft Excel

User Action:

Map to existing skill

Result:

ProfileSkill
↓
Microsoft Excel

No new Skill created

Catalog remains consistent.

---

## Expected Outcome

The system gains:

- better CV enrichment quality;
- lower catalog duplication;
- reusable mappings;
- improved matching quality;
- controlled skill governance.

The Skill catalog remains a trusted source of reference data.
