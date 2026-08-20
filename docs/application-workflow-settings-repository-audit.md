# Application Workflow Settings Repository Audit

## Phase

7.1.19.6.2 Repository Audit

## Objective

Identifier l'ensemble des composants backend, frontend, modèles, APIs et paramètres qui seront impactés par l'introduction des Application Workflow Settings.

L'objectif de cet audit est :

- éviter toute duplication ;
- réutiliser l'infrastructure Settings existante ;
- identifier les composants déjà compatibles ;
- identifier les impacts réels ;
- limiter le périmètre de modification ;
- préparer correctement la conception technique.

---

# Current Functional Context

Le projet implémente déjà :

- Application Workflow ;
- Opportunity Context ;
- Multi Profile Support ;
- Settings Domain ;
- Application Settings Persistence ;
- Opportunity Ranking ;
- Opportunity Profile Comparison.

Le comportement actuel fonctionne et doit être préservé.

Aucun défaut fonctionnel n'a été identifié.

Cette phase introduit uniquement une couche de configuration des stratégies métier.

---

# Audit Scope

Les stratégies concernées sont :

- Application Profile Selection
- Opportunity Context Initialization
- Opportunity Profile Comparison
- Multiple Active Profiles

---

# Backend Audit

## Domain

Settings

### Existing Components

backend/app/settings/

Composants identifiés :

- models.py
- schemas.py
- service.py
- router.py

### Finding

Le domaine Settings existe déjà.

Il permet déjà :

- lecture des paramètres ;
- mise à jour des paramètres ;
- persistance PostgreSQL ;
- validation backend.

### Conclusion

Aucun nouveau domaine backend n'est nécessaire.

Les nouvelles stratégies doivent être intégrées dans ce domaine.

Risk Level

LOW

---

# Existing Persistence Layer

## ApplicationSetting

### Current Status

Le modèle ApplicationSetting existe déjà.

Il est utilisé pour :

- Job Discovery Settings
- Search Criteria Settings
- Source Configuration

### Finding

Le modèle supporte déjà le stockage de paramètres métier.

### Conclusion

Aucune nouvelle table n'est nécessaire.

Les nouvelles stratégies doivent être stockées dans ApplicationSetting.

Risk Level

LOW

---

# Matching Domain Audit

## Domain

backend/app/matching/

### Existing Components

- router.py
- service.py
- schemas.py

### Current Behavior

Le domaine Matching :

- calcule les scores ;
- réalise les comparaisons multi-profils ;
- identifie le meilleur profil ;
- fournit les données utilisées dans Opportunities.

### Finding

Les stratégies futures :

- BEST_MATCHING_PROFILE
- MULTIPLE_ACTIVE_PROFILES

auront un impact direct sur ce domaine.

### Conclusion

Aucune modification immédiate du moteur n'est requise.

Les paramètres introduits doivent simplement être pris en compte lors des futures phases.

Risk Level

LOW

---

# Opportunities Domain Audit

## Frontend

frontend/src/pages/OpportunitiesPage.tsx

### Current Behavior

OpportunitiesPage :

- gère Opportunity Context ;
- affiche les scores ;
- affiche Best Matching Profile ;
- affiche Profile Scores ;
- applique le ranking du profil actif.

### Finding

OpportunitiesPage consomme déjà les données nécessaires.

### Future Impact

Les futures stratégies :

- LAST_USED_PROFILE
- ACTIVE_PROFILE_ONLY
- MULTIPLE_ACTIVE_PROFILES

modifieront les comportements de cette page.

### Conclusion

Aucune modification immédiate requise.

Risk Level

LOW

---

# Applications Domain Audit

## Backend

backend/app/applications/

### Current Behavior

Une candidature possède :

- profile_id
- job_offer_id
- status
- notes
- source_type

### Current Rule

Lors de la création :

- le profil actif est utilisé.

### Finding

Cette règle correspond à :

Application Profile Selection

=
SELECTED_PROFILE_CONTEXT

### Future Impact

Les futures valeurs :

- ASK_EVERY_TIME
- BEST_MATCHING_PROFILE

modifieront cette logique.

### Conclusion

La règle actuelle doit être formalisée dans un paramètre.

Risk Level

MEDIUM

---

# Application Creation Flow Audit

## Current State

Workflow :

Opportunity
↓
Create Application
↓
Selected Profile Context
↓
Application Created

### Finding

Ce flux existe déjà.

### Conclusion

Aucune implémentation métier supplémentaire n'est nécessaire pour le MVP.

Le paramètre ajouté doit simplement refléter le comportement actuel.

Risk Level

LOW

---

# Opportunity Context Audit

## Current State

Workflow :

Open Opportunities
↓
No Context
↓
First Available Profile
↓
Ranking

### Finding

La stratégie existe déjà.

### Conclusion

Elle doit être formalisée comme paramètre configurable.

Risk Level

LOW

---

# Opportunity Comparison Audit

## Current State

Opportunity Details :

- affiche tous les profils ;
- affiche Best Matching Profile ;
- compare les scores.

### Finding

Le comportement actuel correspond à :

ALL_PROFILES

### Conclusion

Le paramètre doit documenter cette stratégie.

Aucune modification immédiate n'est nécessaire.

Risk Level

LOW

---

# Multi Profile Audit

## Current State

Le système supporte :

- plusieurs profils ;
- comparaison multi-profils ;
- profile scores.

Le système ne supporte pas :

- plusieurs profils actifs simultanément.

### Finding

Cette capacité est prévue dans :

7.1.22 Multi Profile Opportunity Context

### Conclusion

Le paramètre Multiple Active Profiles doit uniquement préparer cette évolution.

Aucune activation réelle dans cette phase.

Risk Level

LOW

---

# Frontend Settings Audit

## Existing Page

frontend/src/pages/SettingsPage.tsx

### Current Sections

- Job Discovery Settings
- Search Criteria Settings
- Source Configuration

### Finding

La page Settings dispose déjà de l'infrastructure nécessaire.

### Conclusion

Ajouter une nouvelle section :

Application Workflow Settings

Aucune nouvelle page n'est requise.

Risk Level

LOW

---

# API Audit

## Existing Settings APIs

GET /settings/job-discovery

PUT /settings/job-discovery

GET /settings/search-criteria

PUT /settings/search-criteria

### Finding

Le pattern API est déjà établi.

### Conclusion

Les nouveaux paramètres doivent réutiliser ce modèle.

Risk Level

LOW

---

# Database Audit

## Existing Storage

ApplicationSetting

### Finding

Le stockage est déjà présent.

### Conclusion

Aucune migration de schéma n'est attendue.

Aucune nouvelle table n'est nécessaire.

Risk Level

LOW

---

# Test Impact Audit

## Existing Coverage

Le projet dispose déjà :

- d'une couverture Settings ;
- d'une couverture Matching ;
- d'une couverture Application Workflow.

### New Tests Expected

- workflow settings persistence
- workflow settings retrieval
- default strategy validation
- enum validation

### Conclusion

L'impact test reste limité.

Risk Level

LOW

---

# Repository Impact Summary

## Backend

Files expected to change

backend/app/settings/models.py

backend/app/settings/schemas.py

backend/app/settings/service.py

backend/app/settings/router.py

backend/tests/

---

## Frontend

Files expected to change

frontend/src/pages/SettingsPage.tsx

frontend/src/services/api.ts

---

## Documentation

Files expected to change

docs/architecture.md

docs/project-memory.md

docs/project-status.md

docs/roadmap.md

docs/handoff-prompt.md

---

# Out Of Scope Confirmation

Cette phase ne couvre pas :

- nouveaux statuts ;
- transitions configurables ;
- workflow custom ;
- drag and drop ;
- SLA ;
- notifications ;
- rappels ;
- automation ;
- multi-profils actifs réels.

Ces sujets restent hors périmètre MVP.

---

# Audit Result

Current Architecture Compatibility

EXCELLENT

Required Database Changes

NONE

Required New Tables

NONE

Required New Domains

NONE

Required Frontend Pages

NONE

Required Backend Services

NONE

Repository Risk

LOW

Implementation Complexity

LOW

MVP Compatibility

FULL

Future Compatibility

APP-005 Ready

7.1.22 Ready

---

# Audit Conclusion

Le repository est déjà suffisamment structuré pour supporter Application Workflow Settings.

La totalité de l'implémentation peut être réalisée :

- dans le domaine Settings existant ;
- sans nouvelle table ;
- sans nouveau service ;
- sans modification majeure de l'architecture.

La phase est principalement une formalisation et une préparation des futures stratégies multi-profils.

Le périmètre est maîtrisé.

Le risque technique est faible.
