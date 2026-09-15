# Career Operating System - Post MVP Backlog

Status: Draft
Last Updated: 2026-08-27

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

Examples observed:

- Linux Python
- MS Office PHP
- Visual Studio Code C
- PyCharm C++

---

## DATA-002 - CV Parsing Refinements

Status: Backlog

Remove parsing artifacts.

Examples:

- Tables
- Cross
- development

Multi-column PDF extraction is no longer tracked as a post-MVP item.

Moved to:

- 7.1.23.10 Complex Multi-Column PDF Extraction

Reason:
The issue must be addressed before AI Career Advisor integration because known corrupted extraction results must not enter the AI context.

---

## DATA-003 - Skill Alias Catalog

Status: Backlog

Maintain canonical aliases for common technologies.

## DATA-004 - Experience Extraction Refinement

Status: Backlog

Improvements:

- Date normalization
- Organization detection improvements
- Experience location extraction
- Experience type classification
  - Professional Experience
  - Academic Project
  - Personal Project

Reason deferred:
Current experience reconstruction is functionally validated for MVP.

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
PROFILE_CHANGED

with user-friendly labels:

Application Created
Status Changed
Application Profile Changed

without changing backend event types.

Current partial implementation:

PROFILE_CHANGED already displays the user-friendly title
"Application Profile Changed", but the technical event code
remains visible.

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

## SETTINGS-001 - Settings Categories

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

## SETTINGS-002 - Tag Autocomplete And Suggestions

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

## MATCHING-002 - Configurable Matching Weights

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

## SETTINGS-003 - Reusable Catalog Tag Selector Component

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

## APP-005 - Automatic Best Matching Profile Acceptance

Status: Backlog

When the user creates an application:

- automatically select the Best Matching Profile;
- bypass manual profile confirmation;
- create the application immediately.

Reason deferred:

The MVP keeps explicit user validation before application creation.

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

### TECH-002 - Recurring Console Error (reportAllChanges)

Status: Backlog
Context:
A recurring browser console error was observed across multiple manual
validation sessions (7.1.24.6, 7.1.27.2):
Uncaught TypeError: Cannot read properties of undefined (reading
'startTime') at et.reportAllChanges
The error count increases across page navigations within the same
session, suggesting a repeated trigger rather than a single occurrence.
Investigation performed:
A project-wide search for "reportAllChanges", "web-vitals" and
"reportWebVitals" across frontend/src returned no results, indicating
this does not originate from the project's own code or its declared
dependencies.
Current status:
Root cause not identified. No functional regression, no broken feature,
and no data integrity issue has ever been observed in association with
this error across all manual regression sessions.
Reason deferred:
No functional blocker for MVP closure. Suspected to originate from a
browser extension or an external dev tool rather than the application
itself, but this has not been formally confirmed (e.g. by reproducing
in a private/incognito window or a different browser).
Trigger for revisiting:
If this error is ever found to coincide with an actual functional
defect, or if it can be reproduced in a clean browser profile with no
extensions.

### UX-004 - Explainability For Secondary Profile Scores In Comparison Table

Status: Backlog
Context:
The multi-profile comparison table (OpportunitiesPage) displays 4
sub-scores (Skills, Experience, Work Mode, Location) for every
secondary profile, but provides no direct link to the corresponding
strengths/weaknesses/explanations. This was identified during the
DEC-039 (Explainable Opportunity Scoring) cross-cutting consistency
audit performed in 7.1.27.3.
Current behavior:

- the user must change the Primary Profile to that profile in order to
  see its full explainable matching result
- table rows have no onClick and no visual affordance indicating they
  are interactive
  Expected behavior:
- clicking a row in the comparison table could display that profile's
  full explanation without changing the Primary Profile context
  Nuance:
  This is not considered a fully opaque score under DEC-039, since the
  underlying explanation data exists and remains reachable through an
  indirect action (changing the Primary Profile). It is a UX limitation,
  not a missing backend capability.
  Reason deferred:
  No functional blocker for MVP closure. Backend already computes and
  exposes the full explainable result via calculate_matching_result();
  only the comparison table's UX lacks a shortcut to it.

## SETTINGS-004 - Prevent Duplicate Saved Search Names

Status: Backlog

Prevent creation of multiple Saved Searches using the same name.

Current behavior:

- Duplicate names are allowed.
- Users can create multiple Saved Searches with identical labels.

Expected behavior:

- Saved Search name must be unique.
- Validation occurs before persistence.
- User receives a clear validation message.

Example:
Technical Partnerships France
→ already exists
→ creation refused

Benefits:

- Reduce user confusion.
- Improve Saved Search discoverability.
- Simplify management of Saved Searches.

Out of Scope:

- Automatic rename generation.
- Folder organization.
- Saved Search tagging.

## SETTINGS-005 - Saved Search UX Refinements

Status: Backlog

Improve usability and discoverability of Saved Searches.

Candidate improvements:

- Move Save Search action closer to filter management actions.
- Simplify Saved Search summary display.
- Improve empty state messaging.
- Add success notification after creation.
- Improve Apply/Delete visual hierarchy.
- Improve mobile responsiveness.

Current behavior:

- Full filter summary is displayed.
- Save Search action is separated from filter actions.
- No user feedback after successful creation.

Expected behavior:

- Faster understanding of saved searches.
- Cleaner visual presentation.
- Reduced cognitive load.

Benefits:

- Better user experience.
- Faster opportunity review workflow.
- Higher Saved Search adoption.

Out of Scope:

- Edit Saved Search.
- Favorite Saved Search.
- Search folders.
- Shared searches.
- Scheduled searches.
- Notification alerts.

## AUTH-001 – Multi Factor Authentication (MFA)

Status: Backlog

Support:

- TOTP
- Microsoft Authenticator
- Google Authenticator

Capabilities:

- QR Code setup
- MFA challenge
- Recovery codes
- Device trust

Learning goals:

- RFC 6238
- TOTP
- Authentication security
- Step-up authentication

## AUTH-002 – OAuth Providers

Status: Backlog

Support:

- Microsoft
- Google
- GitHub

Capabilities:

- OAuth2
- OpenID Connect
- Authorization Code Flow
- PKCE

Learning goals:

- Identity federation
- OAuth2
- OIDC
- External providers

## AUTH-003 – Enterprise SSO

Status: Backlog

Support:

- Microsoft Entra ID
- Keycloak
- Generic OpenID Connect

Capabilities:

- Enterprise login
- Claims mapping
- Group mapping
- Role mapping

Learning goals:

- Enterprise identity
- SSO
- Federation
- IAM architecture

## P1 - Architecture

### ARCH-001 - Multi-Tenant Data Isolation

Status: Superseded by DEC-081 (Implemented 2026-09-04)

This item has been reopened and is no longer deferred to post-MVP. See
DEC-081 (User Data Ownership And Isolation) and roadmap.md phase 7.1.24
for the current implementation plan. This entry is preserved for historical
traceability of the original reasoning that led to the initial deferral.

Context:
Sign Up allows creating multiple User accounts, but Profile, Application, CV, WorkExperience, ProfileSkill, ProfileSoftSkill, ProfileLanguage, ProfileCertification, ProfileEnrichmentProposal, SavedSearch and ApplicationSetting (including AI settings) currently have no user_id or owner_id foreign key. All accounts share the same business data.

Required changes if implemented:

- add user_id (ForeignKey to users.id) on all business entities listed above
- filter every existing query by the authenticated user across all domain routers
- data migration strategy for existing records (attribution to a default/primary user)
- test suite updates across most domains (currently 324 backend tests)
- frontend impact assessment (any UI relying on implicit single-user context)

Reason deferred:
This is a major architectural change touching nearly every domain of the application. Sign Up was introduced for authentication learning purposes (DEC-079), not to enable a real multi-user product. Implementing this now would introduce significant regression risk for limited MVP value, since the project remains a personal single-user tool (see project-memory.md, "Utilisateur principal").

Trigger for revisiting:
If Career Operating System is ever intended to support multiple real users (e.g., shared with other people, deployed as a service), this must be addressed before that transition.

### JOBS-001 - Manual Completion Of LinkedIn Email Offers

Status: Completed (2026-09-15, Phase 7.1.31)
LinkedIn Email Connector offers (DEC-086) never include a real
description, contract type or extracted skills - only title,
company, city, work mode and source URL are available from the
notification email. This structurally capped their matching score
and AI explanation quality (quality_level = PARTIAL) compared to
offers from France Travail or Greenhouse.
Sequencing decision (2026-09-15): this item was moved ahead of Phase
7.2 (AI Career Advisor / Gemini integration). Rationale: LinkedIn
Email offers are considered the most relevant and coherent
opportunities for Vincent's actual career targets, making them the
most effective real-world dataset to validate matching quality
before connecting a real AI provider.
Implemented capability:

- PATCH /job-offers/{id}/complete-description lets the user paste
  the real "About the job" section copied from LinkedIn onto a
  PARTIAL offer, setting quality_level to COMPLETE
- MatchingResult, RankedJobOffer and ProfileOpportunityScore enriched
  with is_calculable: bool - matching is never computed for PARTIAL
  offers (neutral result returned instead), consistent with DEC-039
  (no opaque score); frontend shows "Not scored"/"—" rather than a
  misleading 0%
- Partial Only / Complete Only filter and a Partial badge added to
  Opportunities
- fix discovered along the way: NormalizationService previously
  stamped ALL sources as PARTIAL regardless of description
  completeness; France Travail and Greenhouse now correctly default
  to COMPLETE (opt-in list); 199 pre-existing offers reclassified via
  a one-time migration
- fix: JobOfferRepository.update_job_offer() no longer regresses an
  already-COMPLETE offer back to PARTIAL on re-import, preventing a
  manual completion from being silently overwritten on the next
  discovery cycle
- 10 new backend tests, 424 backend tests passing, 0 regressions
- manually validated end-to-end on a real LinkedIn offer (DECADE -
  Architecte Solutions E-commerce)
  Commit: 091eafe - feat(jobs): manual completion of PARTIAL offers,
  source-aware quality_level (JOBS-001)
  Remaining follow-up: discovery_connectors not yet updated to activate
  linkedin_email for the real account (separate from JOBS-001 itself).

### JOBS-002 - LinkedIn API Connector Kept As Dead Code

Status: Backlog
LinkedInConnector (backend/app/jobs/connectors/linkedin_connector.py,
Phase 6.1.2) remains in the codebase, registered in ConnectorRegistry
under "linkedin", but is no longer used in discovery_connectors or
the frontend connector selector (DEC-086). It never fetched a single
real offer since its creation, since no viable LinkedIn API for
individual job search has ever existed.
Trigger for revisiting: if a legitimate LinkedIn partner API access
ever becomes available (e.g. through an official partnership), this
connector could be reactivated instead of being rewritten.

#### JOBS-003 - Manual Archiving Of Old Job Offers

Status: Backlog
Context:
DEC-084 (Job Offer Retention Amendment, 7.1.29) introduced automatic
hard deletion of stale offers via find_stale_job_offer_ids() /
delete_stale_job_offers(), based on discovery_age_window and absence
of JobOfferSource/Application protection. This automatic mechanism
runs only via POST /job-offers/cleanup, triggered manually or by a
future scheduled job - there is currently no way for the user to
manually flag a specific offer as "no longer relevant" before it
reaches the automatic age threshold.
Proposed capability: allow the user to manually archive an
individual offer directly from Opportunity Details (or from the
Opportunities list), independent of discovery_age_window, for offers
they've reviewed and decided are not worth pursuing but do not want
to wait for automatic cleanup to remove.
Open questions (not yet designed):

- does "archive" mean a new status value (e.g. status = "ARCHIVED"
  alongside the existing "ACTIVE"), or immediate hard deletion via
  the existing delete_stale_job_offers() path?
- if a new status is introduced, should archived offers be hidden by
  default from Opportunities (consistent with the already-removed
  "Archived Opportunities Visibility" feature, cut during 7.1.19.7
  design review for lack of demonstrated MVP value), or shown behind
  a dedicated filter (following the same pattern as the "Partial
  Only" / "Complete Only" filter introduced in JOBS-001)?
- interaction with existing Application protection: an offer
  referenced by an Application must presumably remain protected from
  manual archiving too, consistent with DEC-084's existing rule for
  automatic cleanup.
  Reason deferred: requires product design (status vs deletion,
  filter UX, confirmation dialog) before implementation; not blocking
  any MVP capability delivered so far.
  Related Decisions:
- DEC-041 - Standardized Job Evaluation Rules (offer archival
  concept originally introduced here, before being superseded in
  part by DEC-084)
- DEC-084 - Job Offer Retention Amendment (existing automatic
  cleanup mechanism this feature would complement, not replace)

#### TECH-004 - Circular Import Between app.core.database And app.auth.models

Status: Backlog
Context:
Discovered on 2026-09-15 while manually validating DiscoveryScheduler
outside of the FastAPI application context (python -c "from
app.jobs.scheduler import DiscoveryScheduler ..."):
ImportError: cannot import name 'User' from partially initialized
module 'app.auth.models' (most likely due to a circular import)
Root cause: app/core/database.py imports User from app.auth.models
(likely for a relationship or type reference), while
app/auth/models.py imports Base from app.core.database. Under normal
operation (pytest via conftest.py, or the real FastAPI server via
app.main), app.main is imported first, which happens to load modules
in an order that avoids triggering the cycle. Importing
app.jobs.scheduler (or any module transitively importing
app.auth.models) directly, without app.main already loaded first,
triggers the cycle.
Workaround confirmed: importing app.main before the affected module
sidesteps the issue completely, with no need to change any production
code path (pytest and the real server are both unaffected).
Reason deferred: no functional impact on the running application or
the test suite; only affects ad-hoc scripts/REPL usage that import
backend modules directly without going through app.main first.
Trigger for revisiting: if this cycle starts causing real failures in
the test suite or the running server, or if a maintenance pass on
app/core/database.py and app/auth/models.py is scheduled for another
reason.
