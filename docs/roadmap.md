# Roadmap

## Règle de progression

Une phase est terminée uniquement lorsque :

- le développement est terminé ;
- les tests sont passants ;
- la documentation est à jour ;
- project-status.md est à jour ;
- la prochaine étape est clairement définie.

Toute fonctionnalité métier majeure doit suivre le cycle :

Design
↓
Code
↓
Tests
↓
Validation fonctionnelle
↓
Validation frontend si applicable
↓
Audit de cohérence
↓
Commit technique
↓
Push
↓
Documentation
↓
Commit documentaire
↓
Push
↓
git status propre
↓
Étape suivante

Une phase technique n'est pas terminée si le code existe mais que les tests associés sont absents.
Le repository, les tests passants et l'historique Git priment sur la documentation en cas de contradiction.
Une phase backend n'est considérée comme réellement terminée que lorsque sa valeur est visible et validée dans le frontend.

---

## Phase 0

Documentation et cadrage

Statut :

In Progress

---

## Phase 1

Backend Foundation

Objectif :

Créer le socle technique FastAPI.

---

## Phase 2

Candidate Profile

Objectif :
Créer un profil candidat complet.

Sous-phases :

✅ 2.1 Skills Catalog
✅ 2.2 ProfileSkill Schema
✅ 2.3 Skills CRUD
✅ 2.4 ProfileSkill CRUD
✅ 2.5 Work Experience
✅ 2.6 Languages

✅ 2.7 Certifications

---

## Phase 3

Manual Job Import

✅ 3.1 JobOffer Model
✅ 3.2 JobOffer CRUD
✅ 3.2.5 Pytest Foundation
✅ 3.3 JobOfferSkill Model
✅ 3.4 JobOfferSkill CRUD

---

## Phase 4

Matching Engine V1

Objectif :
Comparer profil et offres.

✅ 4.1 Matching Engine V1

---

## Phase 5

✅ 5.1 Frontend Foundation
✅ 5.2 API Client
✅ 5.3 Dashboard MVP
✅ 5.4 Matching View

✅ 5.5 Opportunity Ranking

✅ 5.6.1 Definition & DEC-034
✅ 5.6.2 Application Model
✅ 5.6.3 Application CRUD
✅ 5.6.4 Application Tests
✅ 5.6.5.1 Application Tracker Component
✅ 5.6.5.2 Dashboard Integration
✅ 5.6.5.3 Frontend Validation & Documentation

---

### Phase 5.7

UX/UI Product Design & Frontend Structure Preparation

Objectif :
Définir la vision UX/UI complète du Career Operating System avant toute évolution majeure du frontend.

Cette phase a permis de définir :

- l'architecture informationnelle ;
- les parcours utilisateurs ;
- l'inventaire des pages ;
- les wireframes basse fidélité ;
- la direction visuelle ;
- la stratégie frontend cible ;
- les choix structurants d'authentification ;
- les choix frontend liés au state management, server state, formulaires, validation, design system et internationalisation.

Sous-phases :
✅ 5.7.1 Product Clarification
✅ 5.7.2 Information Architecture
✅ 5.7.3 User Flows
✅ 5.7.4 Page Inventory
✅ 5.7.5 Wireframes
✅ 5.7.6 Design Direction
✅ 5.7.7 Frontend Structure Plan

Livrables créés :

- docs/information-architecture.md
- docs/user-flows.md
- docs/page-inventory.md
- docs/wireframes.md
- docs/design-direction.md
- docs/frontend-structure-plan.md

Statut :
Completed

### Phase 5.8

Frontend Structure Implementation

Objectif :
Transformer le Dashboard MVP actuel en une application React multi-pages maintenable, sécurisée, accessible et prête pour les futures phases produit.

Cette phase doit implémenter progressivement :

- React Router ;
- Auth Layout ;
- App Layout ;
- Protected Routes ;
- Sidebar rétractable ;
- Header léger ;
- Theme Provider ;
- TanStack Query Provider ;
- Zustand stores ;
- structure i18n ;
- structure shadcn/ui + Tailwind ;
- pages MVP skeleton ;
- migration progressive du Dashboard existant.

Sous-phases :

- ✅ 5.8.1 Frontend Dependencies & Technical Setup
- ✅ 5.8.2 App Providers
- ✅ 5.8.3 Routing & Protected Routes
- ✅ 5.8.4 Authentication Flow
- ✅ 5.8.5 App Layout
- ✅ 5.8.6 Sidebar & Header
- ✅ 5.8.7 Dashboard Migration & Design System Foundation
  - ✅ 5.8.7.1 Dashboard Overview
  - ✅ 5.8.7.5.0 Design System Document
  - ✅ 5.8.7.5.1 Tailwind CSS Installation
  - ✅ 5.8.7.5.2 First UI Components
  - ✅ 5.8.7.5.3 Dashboard Cards
  - ✅ 5.8.7.5.4 Dashboard Component Modernization
- ✅ 5.8.8 MVP Page Skeletons
- ✅ 5.8.9 Frontend Structure Documentation

Statut :
Completed

### Phase 5.9

Job Discovery

Objectif :

Récupérer automatiquement des offres d'emploi depuis plusieurs sources externes.

Principes :

- API First
- Scraping uniquement lorsqu'aucune API exploitable n'existe
- Collecte quotidienne
- Sources configurables
- Stockage des offres collectées
- Conservation du lien source

Sous-phases :

- ✅ 5.9.1 Job Sources
- ✅ 5.9.2 Search Criteria
- ✅ 5.9.3 Offer Normalization
- ✅ 5.9.4 First External Source
  - ✅ 5.9.4.1 Job Discovery Data Models
  - ✅ 5.9.4.2 RawOffer Schema
  - ✅ 5.9.4.3 NormalizedJobOffer Schema
  - ✅ 5.9.4.4 MockSourceConnector
  - ✅ 5.9.4.5 NormalizationService
  - ✅ 5.9.4.6 JobOfferRepository
  - ✅ 5.9.4.7 DiscoveryService
  - ✅ 5.9.4.8 Pipeline Validation

- ✅ 5.9.5.1 Connector Interface
- ✅ 5.9.5.2 France Travail Connector
- ✅ 5.9.5.3 Connector Registry
- ✅ 5.9.5.4 Multi Source DiscoveryService
- ✅ 5.9.5.5 Multi Source Validation
- ✅ 5.9.6 Scheduled Synchronization
- ✅ 5.9.6.1 France Travail End-to-End Validation

- ✅ 5.9.7 Job Discovery Visualization

- ✅ 5.9.7.1 Opportunities List
- ✅ 5.9.7.2 Opportunity Details
- ✅ 5.9.7.3 Discovery Dashboard KPI
- ✅ 5.9.7.4 End-to-End Validation

Statut :
Completed

### Phase 6.0

Opportunity Analysis & Advanced Matching

Objectif :
Comparer automatiquement les offres collectées avec les profils candidats.

Le système doit :

- calculer un score ;
- expliquer le score ;
- identifier les points forts ;
- identifier les points faibles ;
- détecter les compétences manquantes ;
- recommander des opportunités pertinentes.

Sous-phases :

- ✅ 6.0.1 Matching V2 Design
- ✅ 6.0.2 Matching V2 Backend
- ✅ 6.0.3 Matching V2 Frontend Validation
- ✅ 6.0.4 Explainable Scoring Backend
- ✅ 6.0.5 Explainable Scoring Frontend Validation
- ✅ 6.0.6 Opportunity Analysis Backend
- ✅ 6.0.7 Opportunity Analysis Frontend Validation

Statut :
Completed

### Phase 6.1

External Sources Expansion

Objectif :
Étendre progressivement les sources d'opportunités professionnelles supportées par le système.

Principes :

- architecture multi-source ;
- réutilisation du pipeline existant ;
- visibilité frontend obligatoire ;
- validation bout en bout avant ajout d'une nouvelle source.

Sous-phases :

- ✅ 6.1.1 LinkedIn Connector Design
- ✅ 6.1.2 LinkedIn Connector Backend
- ✅ 6.1.3 Verification possibilité Welcome to the Jungle
- ✅ 6.1.4 Greenhouse Connector Design
- ✅ 6.1.5 Greenhouse Connector Backend
- ✅ 6.1.6 Greenhouse End-to-End Validation
- ✅ 6.1.7 Source Visualization Frontend
- ✅ 6.1.8 Multi-Source Validation

Statut :
Completed

### Phase 7.0

AI Explanation Layer

Objectif :
Utiliser l'IA pour expliquer les résultats générés par les moteurs déterministes du système.

Principes :

- l'IA n'effectue pas le calcul du score ;
- le score reste déterministe ;
- le score reste testable ;
- le score reste explicable ;
- l'IA fournit des explications complémentaires.

Sous-phases :

- ✅ 7.0.1 AI Score Explanation Design
- ✅ 7.0.2 AI Explanation Backend Design
- ✅ 7.0.3 AI Prompt Architecture Design
- ✅ 7.0.4 AI Explanation API Design
- ✅ 7.0.5 AI Provider Strategy Design
- ✅ 7.0.6 AI Security & Governance Design
- ✅ 7.0 Review

Statut :
Completed

### Phase 7.1

MVP Experience Completion

Objectif :

Finaliser les fonctionnalités cœur du MVP avant de poursuivre les fonctionnalités avancées d'assistance IA.

Cette phase vise à transformer Career Operating System en produit utilisable quotidiennement, en complétant :

- la visualisation et la gestion des profils ;
- la visualisation des candidatures ;
- la gestion du CV ;
- le workflow de candidature ;
- les filtres d'opportunités ;
- les paramètres de recherche et de matching ;
- la complétude du profil ;
- les recherches sauvegardées ;
- la revue globale de l'expérience MVP.

Principes :

- le profil structuré reste la source de vérité principale ;
- les CV associés enrichissent le profil mais ne le remplacent pas ;
- l'historique des candidatures fait partie de la source de vérité carrière ;
- les filtres et préférences doivent être configurables avant d'ajouter une couche IA avancée ;
- l'AI Career Advisor est volontairement repoussé après la finalisation des fonctionnalités cœur du MVP ;
- le Dashboard Evolution est considéré comme post-MVP.

Sous-phases :

✅ 7.1.1 AI Explanation Domain Design
✅ 7.1.2 AI Explanation Backend Package Design
✅ 7.1.3 AI Explanation Schema Design
✅ 7.1.4 AI Provider Interface Design
✅ 7.1.5 AI Explanation Service Design
✅ 7.1.6 AI Prompt Builder Design
✅ 7.1.7 AI Domain Implementation Plan
✅ 7.1 Review
✅ 7.1.8 AI Domain Implementation
✅ 7.1.9 AI Explanation Frontend Integration Design
✅ 7.1.10 AI Explanation Frontend Technical Design
✅ 7.1.11 AI Explanation Frontend Repository Review
✅ 7.1.12 AI Explanation Frontend Implementation
✅ 7.1.13.1 Profile Management Visualization Design
✅ 7.1.13.2 Profile Management Visualization Review
✅ 7.1.13.3 Profile Management Visualization Implementation Plan
✅ 7.1.13.4 Profile Management Visualization Repository Audit
✅ 7.1.13.5 Profile Management Visualization Implementation
✅ 7.1.14 Applications Visualization

✅ 7.1.15 Profile Management CRUD

✅ 7.1.15.1 Repository Audit

✅ 7.1.15.2 CRUD Design

✅ 7.1.15.3 Profile CRUD
✅ 7.1.15.3.1 Backend CRUD Completion
✅ 7.1.15.3.2 Backend CRUD Tests
✅ 7.1.15.3.3 Backend CRUD Validation
✅ 7.1.15.3.4 Frontend CRUD Design
✅ 7.1.15.3.5 Frontend CRUD Implementation
✅ 7.1.15.3.6 Frontend Validation
✅ 7.1.15.3.7 Documentation Synchronization
✅ 7.1.15.3.8 Frontend Profile Creation

✅ 7.1.15.4 Skills Management
✅ 7.1.15.4.1 Backend CRUD Completion
✅ 7.1.15.4.2 Backend CRUD Validation
✅ 7.1.15.4.3 Frontend CRUD Design
✅ 7.1.15.4.A ProfileSkill Backend CRUD Design
✅ 7.1.15.4.B ProfileSkill Backend CRUD Completion
✅ 7.1.15.4.C ProfileSkill Backend Validation
✅ 7.1.15.4.4 Frontend CRUD Implementation
✅ 7.1.15.4.5 Frontend Validation
✅ 7.1.15.4.6 Documentation Synchronization

✅ 7.1.15.5 Experience Management
✅ 7.1.15.5.1 Backend CRUD Completion
✅ 7.1.15.5.2 Backend CRUD Validation
✅ 7.1.15.5.3 Frontend CRUD Design
✅ 7.1.15.5.4 Frontend CRUD Implementation
✅ 7.1.15.5.5 Frontend Validation
✅ 7.1.15.5.6 Documentation Synchronization

✅ 7.1.15.6 Languages Management
✅ 7.1.15.6.1 Backend CRUD Completion
✅ 7.1.15.6.2 Backend CRUD Validation
✅ 7.1.15.6.3 Frontend CRUD Design
✅ 7.1.15.6.4 Frontend CRUD Implementation
✅ 7.1.15.6.5 Frontend Validation
✅ 7.1.15.6.6 Documentation Synchronization

✅ 7.1.15.7 Certifications Management

✅ 7.1.15.7.1 Backend CRUD Completion
✅ 7.1.15.7.2 Backend CRUD Validation
✅ 7.1.15.7.3 Frontend CRUD Design
✅ 7.1.15.7.4 Frontend CRUD Implementation
✅ 7.1.15.7.5 Frontend Validation
✅ 7.1.15.7.6 Documentation Synchronization

✅ 7.1.15.8 Backend Validation

Objectif :
Auditer l'implémentation multi-profils existante.

Résultat :

- support multi-profils confirmé ;
- CRUD multi-profils confirmé ;
- sélection de profils existante côté frontend ;
- absence de notion de profils actifs pour les opportunités confirmée ;
- décision de déplacer la fonctionnalité vers une phase dédiée Multi Profile Opportunity Context.

✅ 7.1.16 CV Intelligence

✅ 7.1.16.1 Repository Audit
✅ 7.1.16.2 CV Management Design
✅ 7.1.16.3 Backend Data Model Design
✅ 7.1.16.4 Backend API Design
✅ 7.1.16.5 Backend Tests Design
✅ 7.1.16.6 Frontend UX Design
✅ 7.1.16.7 Backend Domain Implementation
✅ 7.1.16.8 Backend Tests Implementation
✅ 7.1.16.9 Backend Validation
✅ 7.1.16.10 Frontend Implementation
✅ 7.1.16.11 Frontend Validation
✅ 7.1.16.12 CV Parsing Design
✅ 7.1.16.13 CV Parsing Implementation
✅ 7.1.16.13.1 Parsing Schemas
✅ 7.1.16.13.2 Parsing Service
✅ 7.1.16.13.3 PDF Support
✅ 7.1.16.13.4 DOCX Support
✅ 7.1.16.13.5 Parsing Tests
✅ 7.1.16.13.6 Backend Validation

✅ 7.1.16.14 Profile Enrichment
✅ 7.1.16.14.1 Product Design
✅ 7.1.16.14.2 Reference Data Governance
✅ 7.1.16.14.3 Repository Resolution Strategy
✅ 7.1.16.14.4 Conflict Management Design
✅ 7.1.16.14.5 Enrichment Workflow Design
✅ 7.1.16.14.6 Backend Technical Design
✅ 7.1.16.14.7 Backend Implementation
✅ 7.1.16.14.8 Backend Tests
✅ 7.1.16.14.9 Backend Validation
✅ 7.1.16.14.10 Frontend UX Design
✅ 7.1.16.14.11 Frontend Implementation
✅ 7.1.16.14.12 Frontend Validation
✅ 7.1.16.15 Documentation Synchronization
✅ 7.1.16.16 Reference Data Catalog Design

Sous-phases :
✅ 7.1.16.16.1 Skill Catalog Mapping Design
✅ 7.1.16.16.2 Language Catalog Normalization Design
✅ 7.1.16.16.3 Country Catalog Normalization Design
✅ 7.1.16.16.4 Work Mode Catalog Design
✅ 7.1.16.16.5 Contract Type Catalog Design
✅ 7.1.16.16.6 Preference Options Design
✅ 7.1.16.17 Reference Data Catalog Implementation

✅ 7.1.16.17.1 Repository Audit
✅ 7.1.16.17.2 Backend Models
✅ 7.1.16.17.3 Database Schema Update
✅ 7.1.16.17.4 Seed Data
✅ 7.1.16.17.5 Backend APIs
✅ 7.1.16.17.6 Backend Tests
✅ 7.1.16.17.7 Backend Validation
✅ 7.1.16.17.8 Frontend Integration
✅ 7.1.16.17.9 Frontend Validation
✅ 7.1.16.17.10 Documentation Synchronization

✅ 7.1.16.18 Soft Skills MVP

✅ 7.1.16.18.1 Product Design
✅ 7.1.16.18.2 Backend Models
✅ 7.1.16.18.3 Database Schema
✅ 7.1.16.18.4 APIs
✅ 7.1.16.18.5 Frontend Integration
✅ 7.1.16.18.6 Validation
✅ 7.1.16.18.7 Documentation Synchronization

✅ 7.1.16.19 Soft Skills UX Completion

Objectif :
Propager la séparation Hard Skills / Soft Skills à l'ensemble du workflow CV afin d'assurer une expérience cohérente.

Sous-phases :

✅ 7.1.16.19.1 Repository Audit
✅ 7.1.16.19.2 CV Analysis Design
✅ 7.1.16.19.3 Wizard UX Design
✅ 7.1.16.19.4 Backend Adjustments
✅ 7.1.16.19.5 Frontend Implementation
✅ 7.1.16.19.6 Functional Validation
✅ 7.1.16.19.7 Documentation Synchronization

✅ 7.1.17 Application Workflow

Objectif :
Transformer le tracker de candidatures existant en véritable
workflow métier de pilotage des candidatures.

Le système doit permettre :

- créer une candidature ;
- lier une candidature à une opportunité ;
- associer une candidature à un profil ;
- suivre son cycle de vie ;
- conserver les notes ;
- conserver l'historique ;
- conserver les dates clés ;
- conserver la source ;
- mesurer les résultats ;
- préparer le support multi-profils.

Sous-phases :

✅ 7.1.17.1 Repository Audit
✅ 7.1.17.2 Product Design
✅ 7.1.17.2.1 Application Lifecycle
✅ 7.1.17.2.2 Status Definitions
✅ 7.1.17.2.3 Notes Strategy
✅ 7.1.17.2.4 Timeline Strategy
✅ 7.1.17.2.5 Source Tracking Strategy
✅ DEC-063 Application Workflow Lifecycle

✅ 7.1.17.3 Backend Design
✅ 7.1.17.3.1 Data Model
✅ 7.1.17.3.2 API Design
✅ 7.1.17.3.3 Status Transition Rules
✅ 7.1.17.3.4 Metrics Design

✅ 7.1.17.4 Backend Implementation

✅ 7.1.17.4.1 Application Model Evolution
✅ 7.1.17.4.2 ApplicationEvent Model
✅ 7.1.17.4.3 Complete Application Create API
✅ 7.1.17.4.4 Application Update API
✅ 7.1.17.4.5 Status Transition API
✅ 7.1.17.4.6 Timeline API

✅ 7.1.17.5 Backend Tests
✅ 7.1.17.6 Backend Validation

✅ 7.1.17.7 Frontend Design

Objectif :
Définir l'expérience utilisateur du workflow de candidature avant toute implémentation React.

Décision UX retenue :

- KPI Cards
- Application Cards
- Detail Panel
- Status Workflow
- Notes Section
- Timeline Section
- Source Tracking

Livrable :

- docs/application-workflow-frontend-design.md

  ✅ 7.1.17.8 Frontend Implementation
  ✅ 7.1.17.9 Frontend Validation

  Validation réalisée :

- Application Workflow UI
- KPI Cards
- Status Workflow
- Timeline Display
- Notes Management
- Source Tracking
- Profile → Application navigation
- Opportunity → Application navigation
- Application → Profile navigation
- Application → Opportunity navigation
- Create Application from Opportunity
- Open Application preselection
- Build frontend validé

✅ 7.1.17.10 Opportunity → Application Conversion Design
✅ 7.1.17.11 Opportunity → Application Conversion Implementation
✅ 7.1.17.12 Application Metrics
✅ 7.1.17.13 End-to-End Validation
✅ 7.1.17.14 Documentation Synchronization

✅ 7.1.18 Opportunities Search & Decision Cockpit  
Objectif :
Transformer la page Opportunities en cockpit de recherche, filtrage et priorisation des opportunités.

Le système doit permettre :

- rechercher rapidement une opportunité par mot-clé ;
- comprendre combien d'opportunités correspondent aux critères actifs ;
- filtrer les opportunités selon leur état de candidature ;
- filtrer les opportunités par source ;
- filtrer les opportunités par localisation ;
- distinguer visuellement les opportunités déjà traitées et non traitées ;
- afficher les signaux de décision directement dans les cartes ;
- trier les opportunités selon leur pertinence ou leur fraîcheur ;
- ouvrir ou créer une candidature depuis une opportunité selon le contexte.

Principes :

- rester frontend-only tant que toutes les opportunités sont déjà chargées côté frontend ;
- ne pas ajouter d'API backend prématurément ;
- ne pas introduire de pagination tant que le volume reste compatible avec le MVP ;
- garder la logique métier de scoring dans le backend ;
- utiliser le frontend uniquement pour la présentation, le filtrage local et l'expérience utilisateur ;
- privilégier les filtres utiles à la décision avant les filtres avancés ;
- transformer la page en outil d'aide à la décision, pas en simple job board.

✅ 7.1.18.1 Keyword Search
✅ 7.1.18.2 Search Summary
✅ 7.1.18.3 Reset Filters
✅ 7.1.18.4 Application Status Filter
✅ 7.1.18.5 Source Filter

✅ 7.1.18.6 Location Filter

✅ 7.1.18.7 Opportunity Decision Badges

✅ 7.1.18.8 Matching Score Badge
✅ 7.1.18.9 Opportunities Sorting

✅ 7.1.18.10 Smart Create / Open Application

✅ 7.1.18.11 Opportunities Search & Filters Validation
✅ 7.1.18.12 Documentation Synchronization

✅ 7.1.19 Settings Management
✅ 7.1.19.1 Job Discovery Settings

Livrables :

- backend/app/settings/models.py
- backend/app/settings/service.py
- backend/app/settings/router.py
- backend/app/settings/schemas.py
- application_settings table

✅ 7.1.19.1.1 Job Discovery Settings Design
✅ 7.1.19.1.2 Repository Impact Review
✅ 7.1.19.1.3 Backend Persistence
✅ 7.1.19.1.4 Settings API Validation

Validation réalisée :

- ApplicationSetting persistence validated
- SettingsService validated
- GET /settings/job-discovery validated
- PUT /settings/job-discovery validated
- PostgreSQL persistence validated
- Swagger validation completed

  ✅ 7.1.19.1.5 Frontend Repository Audit
  ✅ 7.1.19.1.6 Frontend Settings Implementation
  ✅ 7.1.19.1.7 Frontend Validation
  ✅ 7.1.19.1.8 Documentation Synchronization
  ✅ 7.1.19.2 Search Criteria Settings

Validation réalisée :

- Search Criteria persistence validated
- Target Job Titles UI completed
- Preferred Countries catalog integration completed
- Work Modes catalog integration completed
- Included Keywords UI completed
- Excluded Keywords UI completed
- Tags-based UX completed
- Counters implemented
- End-to-end validation completed

  ⏭️ 7.1.19.3 Matching Weights Configuration
  Moved to Post-MVP:
  MATCHING-002 Configurable Matching Weights

  ✅ 7.1.19.4 Source Configuration

Validation réalisée:

- Connector catalog introduced
- Connectors stored as controlled list
- Connectors tag-based UX implemented
- Connectors counter implemented
- End-to-end validation completed
  ✅ 7.1.19.5 Opportunity Context Selection

Objectif :

Définir quel profil pilote les opportunités
dans les écrans MVP avant l'arrivée du
Multi Profile Opportunity Context.

Principes :

- le premier profil est sélectionné à l'ouverture si aucun contexte n'existe ;
- l'utilisateur peut sélectionner un profil actif dans les écrans Opportunities ;
- le classement des opportunités utilise le profil sélectionné ;
- le détail affiche les scores de tous les profils ;
- Create Application recommande le Best Matching Profile ;
- l'utilisateur peut sélectionner un autre profil avant validation ;
- le profil confirmé est attaché à la candidature créée ;
- aucun profil global par défaut n'est stocké ;
- aucun contexte actif n'est persisté ;
- lors d'une nouvelle session, le système repart du premier profil disponible.

Règles d'affichage :

Opportunity Cards

- les cartes affichent uniquement le score du profil actuellement sélectionné ;
- le tri utilise uniquement le score du profil actuellement sélectionné.

Opportunity Details

- la fiche détail affiche les scores de tous les profils disponibles ;
- le meilleur score est identifié visuellement ;
- l'utilisateur peut comparer les résultats de tous les profils.

Sous-phases :

✅ 7.1.19.5.1 Product Design
✅ 7.1.19.5.2 Repository Audit
✅ 7.1.19.5.3 Technical Design
✅ 7.1.19.5.4 Validation
✅ 7.1.19.5.5 Documentation Synchronization

✅ 7.1.19.6 Application Workflow Settings
Objectif :

Visualiser les stratégies actuelles du workflow
et les évolutions déjà planifiées.

Aucune persistance.
Aucune API.
Aucune migration.

Validation réalisée :

- Application Workflow Strategy section added to Settings
- Current MVP strategy documented
- APP-005 roadmap visualization added
- 7.1.22 roadmap visualization added
- Frontend build validated
- No backend impact
- No database impact

✅ 7.1.19.6.1 Product Design
✅ 7.1.19.6.2 Repository Audit
✅ 7.1.19.6.3 Technical Design
✅ 7.1.19.6.4 Frontend Strategy Visualization
✅ 7.1.19.6.5 Frontend Validation
✅ 7.1.19.6.6 Documentation Synchronization

✅ 7.1.19.7 Opportunity Discovery Preferences

Validation réalisée :

- Discovery Preferences Settings persistence implemented
- Opportunity Age Window implemented
- Minimum Matching Score implemented
- Default Opportunity Sort implemented
- Settings UI implemented
- Opportunities integration implemented
- Frontend build validated

Removed during design review:

- Archived Opportunities Visibility

Reason:
No demonstrated MVP value.

✅ 7.1.20 Profile Completeness

✅ 7.1.20.1 Completeness Scoring
✅ 7.1.20.2 Missing Information Detection
✅ 7.1.20.3 Profile Quality Recommendations
✅ 7.1.20.4 Profile Completeness Visualization

Validation réalisée :

- Foundation Profile scoring implemented
- Professional Evidence scoring implemented
- Overall Completeness scoring implemented
- Missing Information detection implemented
- Recommended Actions implemented
- Profile Completeness visualization implemented
- Frontend build validated
- Frontend functional validation completed
- No backend changes required
- No database changes required
- No API changes required

✅ 7.1.21 Saved Searches

✅ 7.1.21.1 Repository Audit
✅ 7.1.21.2 Product Design
✅ 7.1.21.3 Technical Design
✅ 7.1.21.4 Backend Implementation
✅ 7.1.21.5 Backend Validation
✅ 7.1.21.6 Frontend Design
✅ 7.1.21.7 Frontend Implementation
✅ 7.1.21.8 Functional Validation
✅ 7.1.21.9 Documentation Synchronization

✅ 7.1.22 Multi Profile Opportunity Context

Objectif :
Plusieurs profils peuvent être activés simultanément.
Les opportunités sont évaluées indépendamment pour chaque profil actif.
Une opportunité peut être pertinente pour plusieurs profils actifs.

Principes :

- plusieurs profils peuvent être activés simultanément ;
- un profil archivé reste distinct d'un profil activé ;
- le matching reste calculé profil par profil ;
- une opportunité peut être pertinente pour plusieurs profils ;
- l'utilisateur doit comprendre quel profil explique chaque score.

Opportunity details display
all profile scores simultaneously.

Ranking continues to use
the currently selected profile context.

Sous-phases :

✅ 7.1.22.1 Product Design
✅ 7.1.22.2 DEC Multi Active Profiles
✅ 7.1.22.3 Backend Context Model
✅ 7.1.22.4 Backend APIs
✅ 7.1.22.5 Backend Tests
✅ 7.1.22.6 Frontend UX Design
✅ 7.1.22.7 Profile Activation UI
✅ 7.1.22.8 Multi Profile Matching
✅ 7.1.22.9 Multi Profile Opportunities

✅ 7.1.22.10 Application Profile Attribution

Validation réalisée :

- Application profile attribution persisted
- Profile selection dialog implemented
- Best Matching Profile recommendation displayed
- Application profile override implemented
- Application reassignment implemented
- PROFILE_CHANGED timeline event implemented
- Timeline profile name rendering implemented
- Frontend validation completed
- Backend validation completed

✅ 7.1.22.11 Application Creation Strategy

Objectif :
Une opportunité peut être pertinente pour plusieurs profils.
Une candidature est créée pour un profil unique.

Exemple :

Opportunity
↓
Product Manager : 92 %
Solution Architect : 58 %
Technical Partnerships Manager : 41 %
↓
Create Application As Product Manager

Le système recommande le Best Matching Profile.
Règle de recommandation actuelle :

1. score de matching le plus élevé ;
2. Primary Profile en cas d'égalité ;
3. profile_id le plus faible si l'égalité persiste.

L'utilisateur peut :

- conserver la recommandation ;
- sélectionner un autre profil avant création ;
- créer la candidature avec le profil choisi.

Les règles définitives de création de candidature multi-profils restent à définir.

APP-005 reste hors MVP car il vise la création immédiate avec le Best Matching Profile sans confirmation manuelle.

✅ 7.1.22.12 Multi Profile Validation

✅ 7.1.22.13 End-to-End Validation

Validation réalisée :

- Opportunity → Application workflow validated
- Best Matching Profile recommendation validated
- Application profile override validated
- PostgreSQL profile attribution validated
- Application reassignment validated
- PROFILE_CHANGED timeline event validated
- Inactive profile protection validated
- Backend non-regression suite validated
- 249 backend tests passing

✅ 7.1.22.14 Documentation Synchronization

⏳ 7.1.23 MVP Experience Review

✅ 7.1.23.1 Test Database Isolation
✅ 7.1.23.2 CV Parsing Data Quality
✅ 7.1.23.3 CV Parsing Improvement Design
✅ 7.1.23.3.1 CV Parsing Benchmark Framework

Validation réalisée :

- 8 parser fixtures créées
- PDF simple validé
- PDF sidebar gauche validé
- PDF sidebar droite validé
- PDF colonnes partielles validé
- PDF multipages validé
- PDF scanné validé
- DOCX standard validé
- DOCX tableaux validé
- benchmark automatisé créé

✅ 7.1.23.3.2 Multiple Skills Sections Support

Validation réalisée :

- support de plusieurs sections skills dans un même CV
- COMPETENCIES + PROGRAMMING LANGUAGES supportés
- test de non-régression ajouté
- benchmark parser validé
- 256 tests backend passants

⚠️ Limitation documentée

PDF multicolonnes complexes :
support partiel

Exemple connu :
CV Lathan

Cause identifiée :
PyPDF2 peut produire un flux structurellement corrompu avant parsing.

### CV Parsing Improvements Completed

Status: DONE

Implemented:

- DOCX table extraction preserving reading order
- French heading support (`PROFIL`)
- Improved full-name detection
- Hard skills / soft skills separation
- Skill line merge support for split skills
- Robust handling of technical acronyms (SQL, VBA, UAT, CSS, HTML)
- Additional non-regression test coverage

Validation:

- 10 CV parsing tests passed
- 255 backend tests passed

✅ 7.1.23.3.3 Parser Benchmark And Sidebar Validation

Validation réalisée :

- benchmark parser créé
- 8 fixtures CV validées
- PDF mono-colonne validé
- PDF sidebar gauche validé
- PDF sidebar droite validé
- PDF colonnes partielles validé
- PDF multipages validé
- PDF scanné validé
- DOCX standard validé
- DOCX tableaux validé
- support de plusieurs sections skills validé
- 256 tests backend passants

Décision :

- le parser est considéré stable sur les layouts couverts par le benchmark
- les PDF multicolonnes complexes ne sont pas couverts par cette étape
- leur traitement est déplacé vers la phase 7.1.23.10 Complex Multi-Column PDF Extraction
- cette phase doit être réalisée avant l’intégration de l’AI Career Advisor

✅ 7.1.23.4 CV Parsing Implementation V1
Validation réalisée :

- DOCX table extraction
- Reading order preservation
- PROFIL heading support
- Hard skills / soft skills separation
- Acronym handling (SQL, VBA, UAT, HTML, CSS)
- Split skill lines merge
- 10 targeted tests passed
- 255 backend tests passed
- Commit c574ea9

✅ 7.1.23.5 CV Parsing Regression Validation

Validation réalisée :

- validation du parsing PDF standard ;
- validation du parsing DOCX standard ;
- validation du parsing DOCX avec tableaux ;
- validation du heading français PROFIL ;
- validation de la séparation Hard Skills / Soft Skills ;
- validation de la gestion des acronymes techniques ;
- 10 tests ciblés passants ;
- 255 tests backend passants.

✅ 7.1.23.6 Existing Data Cleanup

Validation réalisée :

- sauvegarde PostgreSQL créée avant nettoyage ;
- audit non destructif de la base career_os réalisé ;
- profils temporaires 2101, 2102, 2103 et 2104 identifiés ;
- absence de candidature associée confirmée ;
- profils temporaires supprimés ;
- CV et données dépendantes supprimés ;
- dataset ramené aux quatre profils du démonstrateur ;
- contrôles post-nettoyage validés.

✅ 7.1.23.7 Enrichment Summary Consistency

Validation réalisée :

- pollution historique du profil Cloud identifiée ;
- 10 associations de langues invalides supprimées ;
- 12 propositions invalides du CV 822 supprimées ;
- 10 entrées de langues orphelines supprimées du catalogue ;
- compétence invalide "17/01/2022" supprimée du catalogue ;
- aucune référence résiduelle détectée ;
- aucun fichier CV orphelin détecté ;
- CV 822 conservé ;
- 255 tests backend passants.

✅ 7.1.23.8 Profile Creation With Optional CV

Validation réalisée :

- workflow Create Profile validé
- option Continue With CV validée
- Upload CV Wizard lancé automatiquement
- profile créé même si le workflow CV est interrompu
- frontend validation réalisée

✅ 7.1.23.9 Additional Profile Context

Validation réalisée :

- Professional Summary implémenté
- Career Motivations implémenté
- Preferred Environment implémenté
- Non-Negotiables implémenté
- Additional Context implémenté
- persistance PostgreSQL validée
- création de profil validée
- édition de profil validée
- affichage dans Profile Detail validé
- frontend build validé
- 257 tests backend passants
- commits techniques 7e787ff et 63d956e

✅ 7.1.23.10 Complex Multi-Column PDF Extraction

Validation réalisée :

- stratégie multi-moteur implémentée
  - PyPDF2
  - pdfplumber
- benchmark parser conservé
- régressions benchmark validées
- support amélioré des PDF multicolonnes
- support amélioré des CV avec sidebar
- headings français améliorés
- détection du nom améliorée
- détection du titre améliorée
- détection des langues améliorée
- reconstruction des expériences améliorée
- validation fonctionnelle sur le CV réel Lathan
- validation fonctionnelle sur un nouvel upload (CV 1070)
- 274 tests backend passants

Limitation connue :

- certaines compétences restent fusionnées
  (ex : Linux Python, MS Office PHP)

Actions futures :

- DATA-001 Advanced Skill Normalization
- Experience Extraction Refinement

Objectif :
Résoudre ou encadrer techniquement la corruption de l’ordre de lecture des PDF multicolonnes complexes avant l’intégration de l’AI Career Advisor.

Cas de référence :

- CV Lathan

Cause racine connue :

- PyPDF2 peut produire un texte structurellement corrompu avant le parsing
- le parser métier ne peut pas reconstruire de manière fiable un texte dont l’ordre de lecture est déjà dégradé

Critères de fin :

- stratégie d’extraction documentée
- cas Lathan couvert par un test reproductible
- résultat du cas Lathan validé fonctionnellement
- benchmark CV existant sans régression
- suite backend complète passante
- décision explicite si certaines structures PDF restent non supportées

Principe :
Aucune donnée issue d’un PDF connu comme incorrectement extrait ne doit être transmise à la future couche AI Career Advisor.

✅ 7.1.23.11 AI Context Contract

Validation réalisée :

- source de vérité structurée définie ;
- données autorisées définies ;
- données interdites définies ;
- AI Readiness STRICT définie ;
- rôle autorisé de l’IA défini ;
- gouvernance du contexte IA définie ;
- docs/ai-context-contract-design.md créé.

✅ 7.1.23.12 AI Context Preview And Consent

Backend terminé :

- AI Settings persistés via ApplicationSetting
- GET /settings/ai implémenté
- PUT /settings/ai implémenté
- consentement explicite requis
- fonctionnalités IA désactivées par défaut
- AIContextPreviewResponse implémenté
- AIContextService implémenté
- AI Readiness STRICT calculée par le backend
- ai_call_allowed calculé par le backend
- GET /profiles/{profile_id}/ai-context-preview implémenté

Frontend terminé :

- AI Consent Dialog implémenté
- AI Features Settings section implémentée
- AI Context Readiness Card implémentée
- intégration Settings réalisée
- intégration Profile Detail réalisée
- activation AI validée
- désactivation AI validée
- affichage AI Readiness validé

Validation :

- 59 tests AI passants
- 304 tests backend passants
- build frontend validé

Commits :

- 2cc84d3 backend
- 651d262 frontend

✅ 7.1.23.13 AI Readiness Validation

✅ 7.1.23.14 Login UX Polish

Validation réalisée :

- Login page redesigned
- Forgot Password page redesigned
- Account page redesigned
- Design system alignment completed
- Authentication roadmap visibility added
- Frontend build validated

Commit :
179f8e6 - feat(auth): improve login, account and recovery UX

⏳ 7.1.23.15 Authentication Learning Features  
Objectif :

- Sign Up
- Remember Me
- Password Recovery
- Email Recovery
- JWT lifecycle understanding
- Authentication security patterns

  Sous-phases :
  ✅ 7.1.23.15.1 Repository Audit
  ✅ 7.1.23.15.2 Product Design
  ✅ 7.1.23.15.3 Backend Design
  ✅ 7.1.23.15.4 Frontend Design
  ✅ 7.1.23.15.5.1 Password Recovery
  ✅ 7.1.23.15.5.2 Email Recovery
  ✅ 7.1.23.15.5.3 Sign Up
  ✅ 7.1.23.15.5.4 Remember Me
  ✅ 7.1.23.15.6 Validation
  ✅ 7.1.23.15.7 Documentation Synchronization

  Validation Password Recovery :

- PasswordResetToken model implémenté
- token hashé SHA-256 en base
- expiration configurable (PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
- SMTP Mailtrap réel intégré
- POST /auth/forgot-password implémenté
- POST /auth/reset-password implémenté
- ForgotPasswordPage connectée à l'API réelle
- ResetPasswordPage créée
- réponse publique générique anti-énumération
- email réel reçu et lien fonctionnel validés dans Mailtrap
- ancien mot de passe refusé après reset
- nouveau mot de passe accepté après reset
- 9 tests backend ajoutés  
  Validation Email Recovery :
- EmailChangeRequest model implémenté
- réutilisation du token service et de l'infrastructure SMTP
- POST /auth/change-email implémenté (authentifié)
- POST /auth/change-email/confirm implémenté
- email de confirmation envoyé à l'adresse ACTUELLE (pas la nouvelle)
- ConfirmEmailChangePage créée avec confirmation par clic explicite
- formulaire Change Email ajouté dans AccountPage
- ancienne adresse refusée après confirmation
- nouvelle adresse acceptée après confirmation
- 6 tests backend ajoutés  
  Commits :
- da54568 - feat(auth): implement password recovery with Mailtrap SMTP
- abeb09b - feat(auth): add password recovery frontend flow
- 4a6b239 - feat(auth): implement email recovery backend and frontend  
  Validation Sign Up :
- POST /auth/register réactivé via PUBLIC_REGISTRATION_ENABLED (variable d'environnement, false par défaut)
- RegisterRequest schema créé (email, password, confirm_password)
- password_policy.py créé (8 caractères min, majuscule, minuscule, chiffre, caractère spécial)
- règle de mot de passe appliquée à Sign Up ET à Reset Password
- checklist de mot de passe en temps réel implémentée côté frontend
- SignUpPage créée, route /signup ajoutée
- 5 tests backend ajoutés

Validation Remember Me :

- ACCESS_TOKEN_EXPIRE_MINUTES conservé à 60 minutes (comportement par défaut inchangé)
- REMEMBER_ME_TOKEN_EXPIRE_MINUTES ajouté (30 jours)
- create_access_token() accepte un paramètre remember_me (rétrocompatible)
- LoginRequest enrichi avec remember_me: bool = False
- checkbox "Remember me for 30 days" ajoutée sur LoginPage
- décodage JWT manuel validé : ~60 minutes sans Remember Me, ~30 jours avec Remember Me
- 2 tests backend ajoutés

Validation End-to-End combinée (7.1.23.15.6) :

- scénario complet exécuté : Sign Up → Login avec Remember Me → Change Email (confirmation Mailtrap réelle) → Forgot Password sur la nouvelle adresse → Reset Password (confirmation Mailtrap réelle) → Login final avec Remember Me
- ancienne adresse email refusée après changement
- ancien mot de passe refusé après reset
- nouveau compte fonctionnel de bout en bout avec toutes les fonctionnalités combinées
- aucune régression détectée sur l'enchaînement complet

Commits :

- da54568 - feat(auth): implement password recovery with Mailtrap SMTP
- abeb09b - feat(auth): add password recovery frontend flow
- 4a6b239 - feat(auth): implement email recovery backend and frontend
- ae5869c - feat(auth): implement sign up with password policy validation
- 9cbc366 - feat(auth): implement remember me with variable token expiration

Tests :

- 326 tests backend passants (0 régression)

  Décision architecture :

- l'isolation multi-tenant des données (Profile, Application, CV, etc.) n'est pas implémentée ;
- tous les comptes créés via Sign Up partagent actuellement les mêmes données ;
- décision actée : rester en mode single-tenant assumé pour le MVP ;
- référence : ARCH-001 Multi-Tenant Data Isolation ajouté au backlog post-MVP.

Statut :

Completed

✅ 7.1.23.16 Minimal Account UX Polish

Objectif :

- nettoyer AccountPage.tsx des éléments devenus obsolètes après la clôture de 7.1.23.15
- ajouter une information factuelle utile à l'utilisateur (date de création du compte)

Modifications :

- UserResponse (backend) enrichi avec created_at
- AuthUser (frontend) enrichi avec created_at
- AccountPage.tsx : ajout de l'affichage "Member since"
- AccountPage.tsx : suppression de "Account Mode: Single User MVP" (devenu factuellement inexact après Sign Up, qui autorise la création de plusieurs comptes User sans isolation de données réelle — voir ARCH-001)
- AccountPage.tsx : suppression complète de la Card "Authentication Roadmap" (artefact de suivi de développement, plus pertinent pour un utilisateur final une fois toutes les fonctionnalités listées terminées)

Validation :

- 326 tests backend passants, 0 régression
- validation manuelle réalisée : affichage de la date réelle de création de compte, disparition confirmée des deux éléments obsolètes

Commit :

- aaac824 - feat(account): add member since date and remove obsolete roadmap display

⏳ 7.1.24 Settings Strategy Synchronization

Objectif :
S'assurer que tous les paramètres utilisateur sont cohérents entre :

- Frontend
- Backend
- Base PostgreSQL
- Roadmap
- Documentation

Contexte historique :
Cette phase avait été identifiée à la fin de la phase MVP Experience Review, mais n'a jamais été exécutée car le projet a dérivé vers Optional CV puis vers l'investigation et le durcissement du parser CV.

Question centrale :
Quels paramètres doivent être :

- globaux au compte (User) ?
- spécifiques à un profil (Profile) ?
- spécifiques à une recherche (SavedSearch) ?

Note importante :
Cette question a pris une dimension nouvelle depuis la rédaction initiale, car Sign Up (7.1.23.15.5.3) autorise désormais la création de plusieurs comptes User, et ARCH-001 Multi-Tenant Data Isolation documente qu'aucune isolation multi-tenant n'existe. Tout paramètre "global au compte" est aujourd'hui en réalité partagé entre tous les comptes.

Sous-phases :
⬜ 7.1.24.1 Repository Audit
⬜ 7.1.24.2 Product Design
⬜ 7.1.24.3 Gap Analysis
⬜ 7.1.24.4 Decision
⬜ 7.1.24.5 Documentation Synchronization

Livrable attendu :
docs/settings-strategy.md

Hors périmètre de cette phase :

- SETTINGS-001 Settings Categories (reste en post-MVP backlog)
- MATCHING-002 Configurable Matching Weights (reste hors MVP)
- toute migration de données sans validation explicite préalable

⚠️ MISE À JOUR - Séquencement révisé suite à DEC-081

Le séquencement ci-dessous, initialement défini pour 7.1.24, a été révisé
suite à DEC-081 (User Data Ownership And Isolation). Une nouvelle phase
préalable a été identifiée : l'isolation des données par utilisateur doit
précéder la synchronisation des Settings, car cette dernière dépend de
l'existence d'un user_id sur Profile et ApplicationSetting.

⏳ 7.1.24 User Data Ownership And Isolation

Objectif :
Implémenter le modèle d'ownership confirmé :

- 1 User (personne) possède 1..N Profiles (stratégies de carrière / métiers)
- chaque Profile possède ses propres CVs (français, anglais, ...)
- chaque Profile possède ses propres Applications

Cette phase reprend et supersede ARCH-001 (Multi-Tenant Data Isolation),
initialement reporté en post-MVP backlog. Voir DEC-081 pour le contexte
complet et la justification.

Décisions actées (DEC-081) :

- user_id ajouté sur Profile (ForeignKey vers users.id)
- ownership en cascade via les relations existantes (CV, WorkExperience,
  ProfileSkill, ProfileSoftSkill, ProfileLanguage, ProfileCertification,
  ProfileEnrichmentProposal, Application, ApplicationEvent)
- JobOffer, JobSource, JobOfferSource restent globaux (catalogue mutualisé)
- le scoring de matching reste calculé par (Profile, JobOffer), déterministe,
  sans changement du moteur de matching
- l'IA ne calcule pas elle-même le score ; elle peut l'expliquer/l'enrichir
  (cohérent avec DEC-039, DEC-075)
- ApplicationSetting devient per-user : contrainte unique(user_id, setting_key)
- Skill, Language, Certification, Country, WorkMode, ContractType restent
  des catalogues globaux (DEC-051, DEC-055)

Stratégie de migration des données démo :

- audit non destructif des 4 profils démo existants avant toute suppression
- décision de conservation basée sur cet audit (probablement 1 profil
  conservé pour tests, les autres supprimés)
- rattachement des données conservées au compte principal

Sous-phases :
⬜ 7.1.24.1 Repository Audit (complément CV, Application)
⬜ 7.1.24.2 Product Design (DEC-081 - terminé)
⬜ 7.1.24.3 Backend Migration
⬜ 7.1.24.4 Backend Tests (adaptation suite existante + tests d'isolation)
⬜ 7.1.24.5 Frontend Impact Review
⬜ 7.1.24.6 Validation End-To-End (2 comptes réels, étanchéité vérifiée)
⬜ 7.1.24.7 Documentation Synchronization

Hors périmètre :

- SETTINGS-001 Settings Categories (reste post-MVP)
- MATCHING-002 Configurable Matching Weights (reste hors MVP)
- AUTH-001/002/003 MFA, OAuth, SSO (restent post-MVP)

⬜ 7.1.25 Settings Strategy Synchronization

Objectif :
S'assurer que tous les paramètres utilisateur sont cohérents entre Frontend,
Backend, PostgreSQL et documentation, désormais avec un vrai user_id
disponible sur Profile et ApplicationSetting.

Décisions actées (à mettre en oeuvre une fois 7.1.24 terminé) :

- fusionner Profile.preferred_countries et
  ApplicationSetting["search_preferred_countries"] (actuellement dupliqués
  sans synchronisation)
- créer une vraie table saved_searches (actuellement stockée en JSON blob
  dans ApplicationSetting.setting_value, limité à 2000 caractères)
- discovery_minimum_matching_score devient une préférence par utilisateur

Livrable attendu :
docs/settings-strategy.md

⬜ 7.1.26 Best Profile Recommendation Architecture Review
⬜ 7.1.27 Final Regression And Documentation
⬜ 7.1.28 MVP Closure Decision

Statut global (7.1.24 à 7.1.28) :
In Progress

### Phase 7.2

AI Career Advisor

Objectif :
Fournir un accompagnement personnalisé dans les décisions de carrière.

Le système doit :

- analyser les opportunités ;
- analyser les compétences ;
- analyser les écarts ;
- proposer des trajectoires cohérentes.

Sous-phases :

- 7.2.1 Career Path Suggestions
- 7.2.2 Opportunity Strategy
- 7.2.3 Long-Term Career Planning

Statut :
Planned

### Phase 7.3

Dashboard Evolution

Objectif :

Transformer le Dashboard actuel en véritable cockpit de pilotage carrière après la finalisation du MVP.

Le Dashboard actuel reste un dashboard MVP de validation technique et fonctionnelle.

Le Dashboard Evolution devra permettre :

- de suivre le pipeline de candidatures ;
- de visualiser la qualité du profil ;
- de suivre les performances du matching ;
- de suivre l'activité des opportunités ;
- de fournir une aide à la décision quotidienne.

Sous-phases :

⬜ 7.3.1 Career KPI Dashboard
⬜ 7.3.2 Application Funnel
⬜ 7.3.3 Profile Quality Dashboard
⬜ 7.3.4 Job Discovery Analytics
⬜ 7.3.5 Decision Support Dashboard

Statut :

Planned

### Phase 8

Market Intelligence

Objectif :
Analyser le marché de l'emploi à partir des offres collectées.

Le système doit permettre :

- d'identifier les compétences les plus demandées ;
- d'identifier les postes les plus présents ;
- d'analyser les évolutions du marché ;
- d'observer les tendances de recrutement ;
- d'analyser l'évolution des salaires.

Sous-phases :

- 8.1 Market Intelligence Design
- 8.2 Market Data Aggregation Backend
- 8.3 Market Analytics Backend
- 8.4 Market Intelligence Frontend Validation
- 8.5 Skills Trends Dashboard
- 8.6 Jobs Trends Dashboard
- 8.7 Salary Trends Dashboard
- 8.8 Market Insights Visualization
- 8.9 End-to-End Validation

Statut :
Planned

### Phase 9

Career Roadmap

Objectif :
Construire une stratégie de progression de carrière basée sur :

- le profil candidat ;
- les opportunités ;
- le marché ;
- les écarts de compétences.

Le système doit permettre :

- la définition d'objectifs ;
- la projection de carrière ;
- le suivi des progrès ;
- la planification long terme.

Sous-phases :

- 9.1 Career Roadmap Design
- 9.2 Career Roadmap Backend
- 9.3 Career Roadmap Frontend Validation
- 9.4 Roadmap Visualization
- 9.5 Progress Tracking
- 9.6 Scenario Planning
- 9.7 End-to-End Validation

Statut :
Planned

## Post MVP Backlog

The list of validated improvements intentionally excluded from MVP scope is maintained in:

- docs/post-mvp-backlog.md

This backlog is frozen until MVP completion.
