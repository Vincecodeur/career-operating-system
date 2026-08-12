# CV Profile Enrichment Wizard Design

## Status

Proposed

---

## Objective

Transform CV upload into a guided profile enrichment workflow.

The user goal is not to manage enrichment proposals.

The user goal is to update and enrich the profile from a CV as quickly and safely as possible.

The workflow must:

- reduce manual profile completion effort
- reuse CV parsing capabilities
- prevent accidental profile overwrites
- prevent duplicate profile data
- keep the user in control of imported information

---

## UX Principles

### Principle 1

The profile is the source of truth.

The CV is a source of information.

Profile values must never be silently overwritten.

### Principle 2

The user thinks in profile categories.

The workflow must be organized by:

- Skills
- Work Experience
- Languages
- Certifications

The workflow must not expose technical concepts such as:

- proposals
- pending
- accepted
- rejected

### Principle 3

Bulk actions should be preferred over repetitive actions.

The user should be able to import multiple detected items at once.

### Principle 4

Conflicts require explicit resolution.

A conflicting value must never be automatically applied.

---

# Wizard Structure

The existing Upload CV modal becomes a 4-step wizard.

---

## Step 1 - Upload CV

### Goal

Upload a CV and collect metadata.

### Fields

CV File

Language

Version Label

Set As Default CV

### Actions

Cancel

Continue

### Validation

A file must be selected before continuing.

---

## Step 2 - CV Analysis

### Goal

Show progress while the backend processes the CV.

### Analysis Stages

Reading CV

Extracting Skills

Extracting Experiences

Extracting Languages

Extracting Certifications

Comparing With Existing Profile

Generating Suggestions

### Result Summary

Example:

12 Skills Found

4 Experiences Found

2 Languages Found

1 Certification Found

### Actions

Review Suggestions

---

## Step 3 - Review & Edit

### Goal

Review and select the information to be imported.

### Layout

Two-column layout.

Left side:

Skills

Experiences

Languages

Certifications

Right side:

Import Summary

### Import Summary

Skills Selected

Experiences Selected

Languages Selected

Certifications Selected

Conflicts Remaining

The summary updates in real time.

---

## Skills Section

### Controls

Select All

Unselect All

### Display

Checkbox list.

Example:

☑ Agile

☑ Jira

☑ Scrum

☑ Stakeholder Management

### Editing

Not editable.

### Conflict Handling

No conflicts.

### Duplicate Handling

Skills already present in the profile are automatically hidden.

---

## Languages Section

### Controls

Select All

Unselect All

### Display

Language + proficiency level.

### Editing

Not editable.

### Duplicate Handling

Languages already present in the profile are automatically hidden.

---

## Certifications Section

### Controls

Select All

Unselect All

### Display

Certification name

Issuer

Optional obtained date

### Editing

Not editable.

### Duplicate Handling

Certifications already present in the profile are automatically hidden.

---

## Work Experience Section

### Controls

Select All

Unselect All

### Display

Each experience starts collapsed.

Displayed:

Job Title

Company

Date Range

Review Button

### Expanded View

Import Experience Checkbox

Job Title

Company

Start Date

End Date

Description

Source Extract

### Editing

Editable.

Users may modify:

Job Title

Company

Dates

Description

before importing.

### Duplicate Handling

Existing identical experiences are automatically hidden.

---

## Conflict Resolution

### Definition

A conflict occurs when:

Profile Value != CV Value

for a mapped profile field.

Example:

Current Title

Technical Partnerships Manager

Detected Value

Senior Technical Partnerships Manager

### Resolution Options

Keep Current Value

Use CV Value

Use Custom Value

### Rule

Every conflict must be resolved before proceeding.

### Blocking Behavior

Apply Changes remains disabled while unresolved conflicts exist.

---

## Step 4 - Summary & Apply

### Goal

Present final import summary.

### Display

Skills to Import

Experiences to Import

Languages to Import

Certifications to Import

Resolved Conflicts

### Validation

Resolved Conflicts must equal Total Conflicts.

### Actions

Back

Apply Changes

### Rule

Apply Changes disabled if:

Resolved Conflicts < Total Conflicts

---

## Data Rules

### Skills

Imported only when selected.

### Languages

Imported only when selected.

### Certifications

Imported only when selected.

### Experiences

Imported only when selected.

Modified values entered by the user are used.

---

## Duplicate Prevention

The wizard relies on profile normalization rules.

Items already present in the profile must not be proposed again.

This rule applies to:

Skills

Languages

Certifications

Work Experiences

---

## Success State

After Apply Changes:

Profile updated successfully.

Summary example:

12 Skills Added

4 Experiences Added

2 Languages Added

1 Certification Added

The wizard closes automatically.

The profile page refreshes.

---

## Future Enhancements

Import from LinkedIn

Import from JSON

Import from Resume Builder

AI-generated experience summaries

AI-generated profile headline suggestions
