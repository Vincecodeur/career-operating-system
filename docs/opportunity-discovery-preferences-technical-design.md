# Opportunity Discovery Preferences Technical Design

## Phase

7.1.19.7.3 Technical Design

---

# Objective

Implement user-configurable opportunity discovery preferences.

The feature allows users to customize how opportunities are presented without modifying:

- matching algorithms
- ranking algorithms
- profile scoring
- job offer ingestion
- application workflows

---

# Architecture Decision

## Selected Architecture

Settings-based implementation.

Discovery preferences are stored in the existing Application Settings subsystem.

No new database table is required.

No new domain is required.

No new service layer is required.

---

# Existing Components Reused

## Backend

ApplicationSetting

Current storage mechanism:

application_settings

Already used for:

- Job Discovery Settings
- Search Criteria Settings

Discovery Preferences will reuse the same pattern.

---

SettingsService

Current responsibilities:

- load settings
- persist settings

Discovery Preferences will be added to this service.

---

## Frontend

SettingsPage

Current responsibilities:

- Job Discovery Settings
- Search Criteria Settings
- Application Workflow Strategy

Discovery Preferences will become a new Settings section.

---

OpportunitiesPage

Current responsibilities:

- search
- filtering
- sorting
- opportunity display

Discovery Preferences will be applied here.

---

# Discovery Preferences Model

## Opportunity Age Window

Purpose

Limit displayed opportunities by age.

Storage Key

discovery_age_window

Allowed Values

7_DAYS
14_DAYS
30_DAYS
90_DAYS
ALL

Default

30_DAYS

---

## Minimum Matching Score

Purpose

Hide low relevance opportunities.

Storage Key

discovery_minimum_matching_score

Allowed Values

0
25
50
75

Default

25

---

## Archived Opportunities Visibility

Purpose

Control archived opportunity visibility.

Storage Key

discovery_show_archived

Allowed Values

true
false

Default

false

---

## Default Opportunity Sort

Purpose

Control initial sorting.

Storage Key

discovery_default_sort

Allowed Values

BEST_MATCH_FIRST
NEWEST_FIRST
OLDEST_FIRST

Default

BEST_MATCH_FIRST

---

# Backend Changes

## File

backend/app/settings/schemas.py

Add:

DiscoveryPreferencesSettingsResponse

DiscoveryPreferencesSettingsUpdate

---

Expected Structure

discovery_age_window

discovery_minimum_matching_score

discovery_show_archived

discovery_default_sort

---

## File

backend/app/settings/service.py

Add

get_discovery_preferences_settings()

update_discovery_preferences_settings()

Pattern identical to:

get_job_discovery_settings()

update_job_discovery_settings()

---

Settings keys used

discovery_age_window

discovery_minimum_matching_score

discovery_show_archived

discovery_default_sort

---

## File

backend settings router

Add new endpoints:

GET

/settings/discovery-preferences

PUT

/settings/discovery-preferences

Pattern identical to existing Settings APIs.

---

# Frontend Changes

## File

frontend/src/services/api.ts

Add

DiscoveryPreferencesSettings type

Add

getDiscoveryPreferencesSettings()

Add

updateDiscoveryPreferencesSettings()

No other API changes required.

---

## File

frontend/src/pages/SettingsPage.tsx

Add new card:

Opportunity Discovery Preferences

Fields:

Opportunity Age Window

Minimum Matching Score

Show Archived Opportunities

Default Opportunity Sort

Add:

Save Discovery Preferences

---

# Opportunities Page Integration

## File

frontend/src/pages/OpportunitiesPage.tsx

Load discovery preferences on page initialization.

---

# Age Filter

Apply before sorting.

Rules

7_DAYS

created_at >= current_date - 7 days

14_DAYS

created_at >= current_date - 14 days

30_DAYS

created_at >= current_date - 30 days

90_DAYS

created_at >= current_date - 90 days

ALL

no filter

---

# Archived Visibility

If

discovery_show_archived=false

Hide opportunities where:

status != ACTIVE

or

archived_at != null

---

# Minimum Matching Score

Filter opportunities where:

matching_score >= configured threshold

Threshold

0
25
50
75

Profile Context

Always use:

Selected Profile Context

No global scoring exists.

---

# Default Sort

Only controls initial page state.

Supported values:

BEST_MATCH_FIRST

NEWEST_FIRST

OLDEST_FIRST

Users can still manually change sorting afterward.

---

# Data Flow

Settings Page

↓

Discovery Preferences API

↓

Application Settings

↓

Opportunities Page

↓

Filtering

↓

Sorting

↓

Opportunity List

---

# Components Not Impacted

JobOffer model

Matching Engine

Profile Engine

Application Engine

Timeline Engine

CV Engine

Enrichment Engine

Reference Data

---

# Migration Impact

Database Migration

None

---

# API Breaking Changes

None

---

# Security Impact

None

---

# Performance Impact

Low

Filtering occurs on already loaded opportunities.

No expensive computation added.

---

# Risks

Risk 1

Large opportunity datasets may increase frontend filtering cost.

Risk Level

Low

Reason

Current MVP dataset remains limited.

---

Risk 2

Minimum Matching Score depends on selected profile.

Risk Level

Low

Reason

Current architecture already supports profile-specific ranking.

---

# Testing Requirements

Validate:

Opportunity Age Window

Minimum Matching Score

Archived Visibility

Default Sort

Persistence

Settings Reload

Backward Compatibility

No Regression

---

# Technical Design Conclusion

The feature is implemented entirely through the existing Settings architecture.

No schema changes are required.

No opportunity model changes are required.

No matching engine changes are required.

The implementation remains aligned with MVP principles while providing meaningful control over opportunity discovery behavior.
