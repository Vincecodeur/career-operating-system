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
⏳ 5.6.5.3 Frontend Validation & Documentation

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
- ⏳ 5.8.7 Dashboard Migration & Design System Foundation
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

- ⏳ 5.9.7 Job Discovery Visualization

- ✅ 5.9.7.1 Opportunities List
- ✅ 5.9.7.2 Opportunity Details
- ✅ 5.9.7.3 Discovery Dashboard KPI
- ✅ 5.9.7.4 End-to-End Validation

Statut :
In Progress

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
In Progress

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

⬜ 7.1.19 Settings Management
⏳ 7.1.19.1 Job Discovery Settings

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
- Create Application utilise le profil actuellement sélectionné ;
- l'utilisateur peut modifier ce profil avant validation ;
- la pré-sélection automatique du meilleur profil est reportée à APP-005 ;
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

⬜ 7.1.22 Multi Profile Opportunity Context

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

⬜ 7.1.22.1 Product Design
⬜ 7.1.22.2 DEC Multi Active Profiles
⬜ 7.1.22.3 Backend Context Model
⬜ 7.1.22.4 Backend APIs
⬜ 7.1.22.5 Backend Tests
⬜ 7.1.22.6 Frontend UX Design
⬜ 7.1.22.7 Profile Activation UI
⬜ 7.1.22.8 Multi Profile Matching

⬜ 7.1.22.9 Multi Profile Opportunities

⬜ 7.1.22.10 Application Profile Attribution

Objectif :
Une candidature conserve le profil utilisé
lors de sa création.

⬜ 7.1.22.11 Application Creation Strategy

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

pré-sélection du meilleur score

- override manuel utilisateur

⬜ 7.1.22.12 Multi Profile Validation

⬜ 7.1.22.13 End-to-End Validation

⬜ 7.1.22.14 Documentation Synchronization

⬜ 7.1.23 MVP Experience Review

Statut :

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
