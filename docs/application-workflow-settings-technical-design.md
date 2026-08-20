# Application Workflow Settings Technical Design

## Phase

7.1.19.6.3 Technical Design

## Objective

Définir l'architecture technique nécessaire pour supporter les Application Workflow Settings.

Cette phase transforme les décisions produit définies dans :

- application-workflow-settings-design.md
- application-workflow-settings-repository-audit.md

en une conception technique implémentable.

Le design doit :

- réutiliser le domaine Settings existant ;
- éviter toute nouvelle table ;
- éviter toute duplication ;
- conserver le comportement MVP actuel ;
- préparer APP-005 ;
- préparer 7.1.22 Multi Profile Opportunity Context.

---

# Technical Principles

## Principle 1

Le comportement actuel doit rester identique.

Après implémentation :

- aucun utilisateur ne doit constater de changement fonctionnel.

---

## Principle 2

Les stratégies doivent être stockées dans ApplicationSetting.

Aucune nouvelle table n'est autorisée.

---

## Principle 3

Les stratégies doivent être validées par des enums backend.

Aucune valeur libre n'est acceptée.

---

## Principle 4

Les futures évolutions doivent pouvoir être activées sans migration de schéma.

---

## Principle 5

Le backend reste propriétaire de la stratégie.

Le frontend :

- affiche ;
- modifie ;
- sauvegarde ;

mais n'interprète jamais les règles métier.

---

# Solution Overview

Le domaine Settings sera enrichi avec quatre nouveaux paramètres :

- application_profile_selection
- opportunity_context_initialization
- opportunity_profile_comparison
- multiple_active_profiles

Ces paramètres seront stockés dans :

ApplicationSetting

comme les autres paramètres métier existants.

---

# Workflow Setting 1

## Application Profile Selection

### Technical Key

application_profile_selection

### Type

Enum

### Backend Enum

ApplicationProfileSelection

Values:

SELECTED_PROFILE_CONTEXT

ASK_EVERY_TIME

BEST_MATCHING_PROFILE

### MVP Default

SELECTED_PROFILE_CONTEXT

### MVP Enabled Values

SELECTED_PROFILE_CONTEXT

### Reserved Values

ASK_EVERY_TIME

BEST_MATCHING_PROFILE

### Current Runtime Behavior

Lors de la création d'une candidature :

Opportunity
↓
Selected Profile Context
↓
Application

Le comportement existant est conservé.

### Future Usage

APP-005

BEST_MATCHING_PROFILE

7.1.22

ASK_EVERY_TIME

---

# Workflow Setting 2

## Opportunity Context Initialization

### Technical Key

opportunity_context_initialization

### Type

Enum

### Backend Enum

OpportunityContextInitialization

Values:

FIRST_AVAILABLE_PROFILE

LAST_USED_PROFILE

### MVP Default

FIRST_AVAILABLE_PROFILE

### MVP Enabled Values

FIRST_AVAILABLE_PROFILE

### Reserved Values

LAST_USED_PROFILE

### Current Runtime Behavior

Open Opportunities Page
↓
No Context
↓
First Available Profile

### Future Usage

7.1.22

LAST_USED_PROFILE

---

# Workflow Setting 3

## Opportunity Profile Comparison

### Technical Key

opportunity_profile_comparison

### Type

Enum

### Backend Enum

OpportunityProfileComparison

Values:

ALL_PROFILES

ACTIVE_PROFILE_ONLY

### MVP Default

ALL_PROFILES

### MVP Enabled Values

ALL_PROFILES

### Reserved Values

ACTIVE_PROFILE_ONLY

### Current Runtime Behavior

Opportunity Details
↓
Display All Scores
↓
Best Matching Profile

### Future Usage

7.1.22

ACTIVE_PROFILE_ONLY

---

# Workflow Setting 4

## Multiple Active Profiles

### Technical Key

multiple_active_profiles

### Type

Enum

### Backend Enum

MultipleActiveProfilesMode

Values:

DISABLED

ENABLED

### MVP Default

DISABLED

### MVP Enabled Values

DISABLED

### Reserved Values

ENABLED

### Current Runtime Behavior

Single Active Profile

### Future Usage

7.1.22

Multi Active Profiles

---

# Backend Architecture

## Existing Domain

backend/app/settings/

No new package required.

---

## Files To Modify

backend/app/settings/models.py

backend/app/settings/schemas.py

backend/app/settings/service.py

backend/app/settings/router.py

---

# Settings Model Impact

## ApplicationSetting

No schema change required.

No migration required.

Existing storage mechanism reused.

---

# Schemas Design

## New Response Schema

ApplicationWorkflowSettingsResponse

Fields:

application_profile_selection

opportunity_context_initialization

opportunity_profile_comparison

multiple_active_profiles

---

## New Update Schema

ApplicationWorkflowSettingsUpdate

Fields:

application_profile_selection

opportunity_context_initialization

opportunity_profile_comparison

multiple_active_profiles

---

# API Design

## Get Workflow Settings

GET

/settings/application-workflow

Response

{
"application_profile_selection": "SELECTED_PROFILE_CONTEXT",
"opportunity_context_initialization": "FIRST_AVAILABLE_PROFILE",
"opportunity_profile_comparison": "ALL_PROFILES",
"multiple_active_profiles": "DISABLED"
}

---

## Update Workflow Settings

PUT

/settings/application-workflow

Request

{
"application_profile_selection": "SELECTED_PROFILE_CONTEXT",
"opportunity_context_initialization": "FIRST_AVAILABLE_PROFILE",
"opportunity_profile_comparison": "ALL_PROFILES",
"multiple_active_profiles": "DISABLED"
}

Response

Updated settings.

---

# Validation Rules

## Rule 1

Unknown enum values rejected.

HTTP 422

---

## Rule 2

Reserved future values accepted.

Purpose:

avoid future migrations.

Example:

BEST_MATCHING_PROFILE

must already be accepted.

---

## Rule 3

Invalid combinations rejected.

Example:

multiple_active_profiles = ENABLED

before phase 7.1.22

must not be selectable through the UI.

---

# Service Layer Design

## New Methods

get_application_workflow_settings()

update_application_workflow_settings()

---

## Responsibility

Read settings.

Validate enums.

Persist settings.

Provide defaults.

---

# Default Configuration

System bootstrap defaults:

application_profile_selection

SELECTED_PROFILE_CONTEXT

opportunity_context_initialization

FIRST_AVAILABLE_PROFILE

opportunity_profile_comparison

ALL_PROFILES

multiple_active_profiles

DISABLED

---

# Frontend Architecture

## Existing Page

frontend/src/pages/SettingsPage.tsx

No new page required.

---

# New Settings Section

Application Workflow Settings

Display:

Application Profile Selection

Opportunity Context Initialization

Opportunity Profile Comparison

Multiple Active Profiles

---

# MVP UI Behavior

Display current configuration.

Allow saving configuration.

Future-only values visible but disabled.

Example:

Application Profile Selection

(●) Selected Profile Context

(○) Ask Every Time
Coming in 7.1.22

(○) Best Matching Profile
Coming in APP-005

---

# API Client Impact

## File

frontend/src/services/api.ts

Add:

getApplicationWorkflowSettings()

updateApplicationWorkflowSettings()

---

# Runtime Impact

MVP

No behavior change.

All current workflows continue to function identically.

---

# Testing Strategy

## Backend Tests

New file:

backend/tests/test_application_workflow_settings.py

Coverage:

- get settings
- update settings
- default values
- enum validation
- persistence validation

---

# Frontend Validation

Validation scenarios:

Scenario 1

Load workflow settings.

Expected:

defaults displayed.

---

Scenario 2

Save workflow settings.

Expected:

settings persisted.

---

Scenario 3

Refresh application.

Expected:

settings restored.

---

Scenario 4

Future values disabled.

Expected:

cannot activate APP-005 features.

---

# Database Impact

New Tables

None

New Columns

None

Migration Required

No

---

# Security Impact

No new permissions.

No secrets.

No authentication changes.

Uses existing settings security model.

---

# Future Compatibility Matrix

APP-005

Ready

No schema changes required.

---

7.1.22

Ready

No schema changes required.

---

Multi Active Profiles

Ready

No schema changes required.

---

Profile Selection Dialog

Ready

No schema changes required.

---

# Risks

Risk

Low

Reason

Existing Settings infrastructure reused.

No database migration.

No workflow modification.

No matching modification.

No application model modification.

---

# Success Criteria

The phase is complete when:

- all four settings exist;
- settings persist correctly;
- enums validate correctly;
- UI displays settings;
- UI saves settings;
- current workflow behavior remains unchanged;
- APP-005 remains compatible;
- 7.1.22 remains compatible;
- tests pass.

---

# Technical Design Conclusion

Application Workflow Settings are implemented as a lightweight extension of the existing Settings domain.

The implementation:

- introduces no new tables;
- introduces no new domains;
- introduces no workflow changes;
- prepares APP-005;
- prepares 7.1.22;
- preserves MVP behavior.

The repository architecture remains unchanged while gaining future extensibility for multi-profile workflow strategies.
