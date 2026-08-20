# Application Workflow Settings Design

## Phase

7.1.19.6.1 Product Design

## Objectif

Définir les paramètres de configuration du workflow de candidature qui seront utilisés par le MVP et qui prépareront les futures évolutions multi-profils.

Cette phase ne vise pas à rendre le workflow de candidature entièrement configurable.

Cette phase vise à :

- formaliser les stratégies métier actuellement utilisées ;
- préparer l'arrivée de APP-005 Best Matching Profile Preselection ;
- préparer l'arrivée de 7.1.22 Multi Profile Opportunity Context ;
- éviter les refactorings de modèle futurs ;
- conserver la simplicité du MVP.

## Problème métier

Le système supporte plusieurs profils candidats.

Aujourd'hui :

- un profil est sélectionné dans Opportunity Context ;
- le classement des opportunités utilise ce profil ;
- les cartes Opportunity affichent le score de ce profil ;
- Opportunity Details affiche les scores de tous les profils ;
- Create Application utilise le profil actuellement sélectionné.

Le comportement actuel fonctionne mais les stratégies associées ne sont pas encore formalisées dans les paramètres du système.

Cette phase introduit un cadre de configuration permettant de documenter et de préparer les évolutions futures.

---

# Design Principles

## Principle 1

Le MVP doit conserver son comportement actuel.

Aucun changement utilisateur ne doit apparaître après l'implémentation de cette phase.

## Principle 2

Les paramètres doivent refléter une stratégie métier.

Ils ne doivent pas être de simples flags techniques.

## Principle 3

Les futures évolutions doivent pouvoir être activées sans migration lourde.

Les futures phases doivent pouvoir réutiliser les mêmes paramètres.

## Principle 4

La logique métier reste dans le backend.

Le frontend ne décide jamais quel profil utiliser pour le matching ou la création de candidature.

---

# Workflow Strategy 1

## Application Profile Selection

### Purpose

Définir comment le profil utilisé pour créer une candidature est déterminé.

### Setting Name

Application Profile Selection

### Technical Key

application_profile_selection

### Supported Values

SELECTED_PROFILE_CONTEXT

ASK_EVERY_TIME

BEST_MATCHING_PROFILE

### MVP Value

SELECTED_PROFILE_CONTEXT

### Current Behavior

Workflow :

Opportunity
↓
User clicks Create Application
↓
Selected Profile Context
↓
Application Created

### Future Behavior

ASK_EVERY_TIME

Workflow :

Opportunity
↓
Create Application
↓
Profile Selection Dialog
↓
Selected Profile
↓
Application Created

### Future Behavior

BEST_MATCHING_PROFILE

Workflow :

Opportunity
↓
Calculate All Profile Scores
↓
Best Matching Profile
↓
User Can Override
↓
Application Created

### Related Future Work

APP-005 Best Matching Profile Preselection

7.1.22 Multi Profile Opportunity Context

---

# Workflow Strategy 2

## Opportunity Context Initialization

### Purpose

Définir comment le contexte profil est initialisé lorsque l'utilisateur ouvre la page Opportunities.

### Setting Name

Opportunity Context Initialization

### Technical Key

opportunity_context_initialization

### Supported Values

FIRST_AVAILABLE_PROFILE

LAST_USED_PROFILE

### MVP Value

FIRST_AVAILABLE_PROFILE

### Current Behavior

Opportunities Page
↓
No Active Context
↓
First Available Profile
↓
Page Loaded

### Future Behavior

LAST_USED_PROFILE

Opportunities Page
↓
Load Previous Context
↓
Restore Last Selected Profile
↓
Page Loaded

### Related Future Work

7.1.22 Multi Profile Opportunity Context

---

# Workflow Strategy 3

## Opportunity Profile Comparison

### Purpose

Définir la stratégie d'affichage des scores profil dans Opportunity Details.

### Setting Name

Opportunity Profile Comparison

### Technical Key

opportunity_profile_comparison

### Supported Values

ALL_PROFILES

ACTIVE_PROFILE_ONLY

### MVP Value

ALL_PROFILES

### Current Behavior

Opportunity Details
↓
Display Profile Scores
↓
Display All Profiles
↓
Identify Best Profile

### Future Behavior

ACTIVE_PROFILE_ONLY

Opportunity Details
↓
Display Active Profile Only

### Related Future Work

7.1.22 Multi Profile Opportunity Context

---

# Workflow Strategy 4

## Multiple Active Profiles

### Purpose

Préparer le support multi-profils actifs simultanés.

### Setting Name

Multiple Active Profiles

### Technical Key

multiple_active_profiles

### Supported Values

DISABLED

ENABLED

### MVP Value

DISABLED

### Current Behavior

Single Active Profile Context

### Future Behavior

Profile A
Profile B
Profile C
↓
Active Context Set
↓
Opportunity Evaluation

### Related Future Work

7.1.22 Multi Profile Opportunity Context

---

# Data Model Impact

Cette phase ne crée pas encore de nouveaux écrans spécialisés.

Les paramètres seront stockés dans le domaine Settings existant.

Chaque paramètre sera persisté dans ApplicationSetting.

Aucune nouvelle table n'est nécessaire.

---

# Frontend Impact

MVP

Settings Page

Nouvelle section :

Application Workflow Settings

Affichage uniquement des stratégies actuellement supportées.

Les valeurs futures peuvent être visibles mais non sélectionnables.

La logique métier reste pilotée par le backend.

---

# Backend Impact

Le backend devient propriétaire des stratégies métier.

Les endpoints de matching et de création de candidature utiliseront les paramètres configurés.

Le comportement MVP doit rester identique au comportement actuel.

---

# Out Of Scope

Cette phase ne couvre pas :

- statuts personnalisés ;
- transitions personnalisées ;
- workflow drag and drop ;
- notifications ;
- rappels ;
- SLA ;
- automatisations ;
- règles conditionnelles ;
- couleurs personnalisées ;
- KPI configurables ;
- gestion avancée des permissions.

Ces sujets seront traités dans des phases futures si leur valeur métier est démontrée.

---

# Success Criteria

La phase est considérée comme terminée lorsque :

- les stratégies métier sont documentées ;
- les paramètres sont persistés ;
- le comportement actuel est préservé ;
- aucune régression fonctionnelle n'est observée ;
- la préparation de APP-005 est validée ;
- la préparation de 7.1.22 est validée ;
- la documentation est synchronisée.

---

# Expected Outcome

Le système dispose désormais d'une stratégie explicite pour :

- sélectionner un profil lors de la création d'une candidature ;
- initialiser le contexte actif ;
- afficher les comparaisons de profils ;
- préparer les profils actifs multiples.

Le MVP garde exactement le même comportement utilisateur tout en préparant les futures évolutions multi-profils.
