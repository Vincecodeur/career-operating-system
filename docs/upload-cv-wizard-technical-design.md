# Upload CV Wizard Technical Design

## Status

Proposed

---

## Objective

Transform the current Upload CV modal into a multi-step wizard capable of:

- uploading a CV
- launching backend parsing
- reviewing detected information
- resolving profile conflicts
- importing validated information

The wizard reuses the existing backend enrichment engine.

No additional page is introduced.

The workflow remains modal-based.

---

# Component Architecture

Current:

UploadCvModal

Target:

UploadCvModal
├── WizardHeader
├── WizardProgress
├── Step1Upload
├── Step2Analysis
├── Step3Review
├── Step4Summary
└── WizardFooter

---

# Wizard State

type WizardStep =
| "upload"
| "analysis"
| "review"
| "summary";

const [step, setStep] =
useState<WizardStep>("upload");

---

# Step 1 Upload

## Responsibility

Collect upload information.

## Existing fields

CV File

Language

Version Label

Set As Default

## Validation

A file is mandatory.

## Action

Continue

---

# Step 2 Analysis

## Responsibility

Execute enrichment workflow.

## Backend Calls

Upload CV

Generate Proposals

Load Proposals

## Progress States

Uploading CV

Parsing CV

Generating Suggestions

Loading Suggestions

Completed

## Result

AnalysisResult

skillsFound

experiencesFound

languagesFound

certificationsFound

conflictCount

---

# Step 3 Review

## Responsibility

Review imported information.

---

# Layout

Two-column layout.

Left:

Navigation

Right:

Selected section content

---

# Navigation Sections

Skills

Experiences

Languages

Certifications

Conflicts

---

# Internal State

type EnrichmentReviewState = {

    selectedSkills: number[];

    selectedLanguages: number[];

    selectedCertifications: number[];

    selectedExperiences: number[];

    experienceEdits: Record<
        number,
        ExperienceDraft
    >;

    conflictResolutions: Record<
        number,
        ConflictResolution
    >;

};

---

# Skills Section

## Display

Checkbox list.

## Controls

Select All

Unselect All

## Editing

Disabled.

## Import Logic

Selected items only.

---

# Languages Section

## Display

Checkbox list.

## Controls

Select All

Unselect All

## Editing

Disabled.

---

# Certifications Section

## Display

Checkbox list.

## Controls

Select All

Unselect All

## Editing

Disabled.

---

# Experiences Section

## Display

Collapsed cards.

Default view:

Job Title

Company

Date Range

Review Button

---

# Expanded Experience View

Import Checkbox

Job Title

Company

Start Date

End Date

Description

Source Extract

---

# Editable Fields

Job Title

Company

Start Date

End Date

Description

---

# Experience Draft

type ExperienceDraft = {

    jobTitle: string;

    companyName: string;

    startDate: string;

    endDate: string | null;

    description: string;

};

---

# Conflicts Section

## Responsibility

Resolve profile conflicts.

---

# Conflict Definition

A conflict exists when:

Profile Value != CV Value

for the same mapped profile field.

---

# Conflict Display

Current Profile Value

Detected CV Value

Resolution

---

# Resolution Options

KEEP_PROFILE_VALUE

USE_CV_VALUE

USE_CUSTOM_VALUE

---

# Custom Value

Enabled only when:

USE_CUSTOM_VALUE selected.

---

# Conflict State

type ConflictResolution = {

    resolution:
        | "profile"
        | "cv"
        | "custom";

    customValue: string | null;

};

---

# Conflict Rule

All conflicts must be resolved.

---

# Step Completion Rule

Review step cannot continue if:

unresolvedConflicts > 0

---

# Step 4 Summary

## Responsibility

Show final import result.

---

# Display

Skills Selected

Experiences Selected

Languages Selected

Certifications Selected

Resolved Conflicts

---

# Validation

# resolvedConflicts

totalConflicts

---

# Apply Changes Button

Enabled only if:

All conflicts resolved

---

# Import Strategy

## Skills

Accept selected proposals.

Reject unselected proposals.

---

## Languages

Accept selected proposals.

Reject unselected proposals.

---

## Certifications

Accept selected proposals.

Reject unselected proposals.

---

## Experiences

Accept selected proposals.

Apply edited values when present.

Reject unselected proposals.

---

## Conflicts

Apply chosen resolution.

---

# Duplicate Prevention

Backend normalization remains source of truth.

Items already present in profile should not appear in review lists.

Applies to:

Skills

Languages

Certifications

Experiences

---

# Success Flow

Apply Changes

↓

Refresh Profile

↓

Close Wizard

↓

Display Success Message

---

# Error Handling

Upload Error

Parsing Error

Suggestion Loading Error

Import Error

Conflict Validation Error

---

# Exit Rules

User may cancel wizard before Apply Changes.

No profile modification occurs before Apply Changes.

Imported changes become permanent only after successful Apply Changes.
