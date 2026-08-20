# Career Operating System - Post MVP Backlog

Status: Draft
Last Updated: 2026-08-16

## Purpose

This document contains all improvements explicitly identified during MVP implementation and validation.

Items listed here are intentionally excluded from the MVP scope and will be considered after MVP stabilization.

---

# P1 - Profile Evolution

## PROF-001 - Education Management

Status: Backlog

Add education management:

- Degree
- School
- Field of Study
- Start Date
- End Date
- Grade

---

## PROF-002 - Certification Details

Status: Backlog

Add:

- Issuing Organization
- Obtained Date
- Expiration Date
- Credential ID
- Credential URL

---

## PROF-003 - Language Framework

Status: Backlog

Support CEFR levels:

- A1
- A2
- B1
- B2
- C1
- C2
- Native

---

## PROF-004 - Skill Proficiency Display

Status: Backlog

Display:

- Beginner
- Intermediate
- Advanced
- Expert

---

## PROF-005 - Skill Experience Display

Status: Backlog

Display years of experience for each skill.

---

## PROF-006 - Skill Source Tracking

Status: Backlog

Display skill source:

- CV
- Manual
- Imported
- AI Suggested

---

# P1 - Data Quality

## DATA-001 - Advanced Skill Normalization

Status: Backlog

Examples:

PowerQuery
→ Power Query

NodeJS
→ Node.js

PowerBI
→ Power BI

---

## DATA-002 - CV Parsing Refinements

Status: Backlog

Remove parsing artifacts.

Examples:

- Tables
- Cross
- development

---

## DATA-003 - Skill Alias Catalog

Status: Backlog

Maintain canonical aliases for common technologies.

---

# P2 - Career Operating System

---

## CAREER-002 - Career Readiness Score

Status: Backlog

Compare profile against target role.

---

## CAREER-003 - Skill Gap Analysis

Status: Backlog

Identify missing skills for target role.

---

## CAREER-004 - Missing Certifications

Status: Backlog

Identify certification gaps.

---

## CAREER-005 - Career Timeline

Status: Backlog

Visual career progression timeline.

---

## CAREER-006 - Multi Career Targets

Status: Backlog

Support multiple target roles.

---

# P2 - CV Enrichment

## ENRICH-001 - Selective Bulk Processing

Status: Backlog

Support:

- Accept All Hard Skills
- Accept All Soft Skills
- Accept All Languages
- Accept All Experiences

---

## ENRICH-002 - Confidence Scores

Status: Backlog

Display enrichment confidence score.

---

## ENRICH-003 - Auto-Accept Rules

Status: Backlog

Allow user-defined acceptance rules.

---

# P3 - UX

## UX-001 - Skill Search And Filtering

Status: Backlog

Search and filter by:

- Category
- Level
- Source

---

## UX-002 - Experience Collapsing

Status: Backlog

Collapse long experiences.

---

## UX-003 - Profile Dashboard Cards

Status: Backlog

Quick navigation dashboard.

---

# P3 - Matching

## MATCH-001 - Skill Match Score

Status: Backlog

Use skills in matching score.

---

## MATCH-002 - Certification Match

Status: Backlog

Use certifications in matching.

---

## MATCH-003 - Language Match

Status: Backlog

Use CEFR levels in matching.

---

## MATCH-004 - Experience Match

Status: Backlog

Use years of experience in matching.

---

## APP-001 - Human Friendly Timeline Labels

Status: Backlog

Replace technical event labels:

APPLICATION_CREATED
STATUS_CHANGED

with user-friendly labels:

Application Created
Status Changed

without changing backend event types.

---

## APP-002 - Application Filters Persistence

Status: Backlog

Remember:

- Search
- Status Filter
- Profile Filter
- Source Filter

when navigating between pages.

---

## APP-003 - Application Export ( à revoir le besoin)

Status: Backlog

Export applications to CSV.

Fields:

- Profile
- Opportunity
- Status
- Source
- Created At
- Updated At

## APP-004 - Application Funnel Dashboard

Status: Backlog

Provide funnel visualization:

Applied
→ Phone Screen
→ Interview
→ Offer
→ Accepted

### SETTINGS-001 - Settings Categories

Status: Backlog

Group Settings into functional categories:

- Discovery
- Matching
- Search
- Profiles
- Applications

Possible future navigation:

Settings
├── Discovery
├── Matching
├── Search
├── Profiles
└── Applications

Rationale:
Improve Settings Management scalability and maintainability as new configuration areas are added after MVP completion.

Out of Scope for MVP:

- Multi-page settings navigation
- Permission management
- User-specific settings isolation
- Advanced settings search

### SETTINGS-002 - Tag Autocomplete And Suggestions

Status: Backlog

Provide autocomplete suggestions for:

- Target Job Titles
- Included Keywords
- Excluded Keywords

Examples:

- Technical Partnerships Manager
- Solution Architect
- Product Manager

Benefits:

- Faster data entry
- Reduced duplicates
- Improved consistency of search criteria

Out of Scope for MVP:

- AI suggestions
- Market-driven recommendations
- Dynamic ranking based on opportunity history

### MATCHING-002 - Configurable Matching Weights

Status: Backlog

Allow users to configure matching score weights:

- Skills
- Experience
- Work Mode
- Location

Current default values:

- Skills: 70%
- Experience: 15%
- Work Mode: 10%
- Location: 5%

Requirements:

- Total must equal 100%
- Persist through Settings
- Applied by Matching Engine

Reason deferred:
Current default weights are sufficient for MVP.
Additional configurability increases complexity without delivering core user value.

### SETTINGS-003 - Reusable Catalog Tag Selector Component

Status: Backlog

Create a reusable CatalogTagSelector component.

Current duplicated patterns:

- Preferred Countries
- Connectors

Future candidates:

- Contract Types
- Job Sources
- Future Reference Data Catalogs

Expected capabilities:

- Selected tags display
- Add from dropdown
- Remove through tag action
- Counter display
- Empty state handling

Benefits:

- Reduce duplicated React code
- Improve maintainability
- Ensure consistent user experience
- Simplify future catalog integrations

Reason deferred:

Current implementation is functional and stable.
This is a code maintainability improvement rather than a user-facing MVP requirement.

### APP-005 - Best Matching Profile Preselection

Status: Backlog

When creating an application from an opportunity:

- automatically preselect the profile with the highest matching score;
- allow user override before validation;
- preserve current workflow compatibility.

Reason deferred:
Current MVP uses the active profile context.
Opportunity profile comparison is already implemented.

### TECH-001 - Frontend Bundle Optimization

Status: Backlog

Current Vite build produces chunks larger than 500 KB.

Potential improvements:

- route splitting
- dynamic imports
- lazy loading
- bundle optimization

Reason deferred:
No functional impact on MVP.
Build validation is successful.
