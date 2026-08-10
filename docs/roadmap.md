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
⬜ 7.1.14 Applications Visualization

⬜ 7.1.15 Profile Management CRUD
⬜ 7.1.15.1 Profile CRUD
⬜ 7.1.15.2 Skills Management
⬜ 7.1.15.3 Experience Management
⬜ 7.1.15.4 Languages Management
⬜ 7.1.15.5 Certifications Management
⬜ 7.1.15.6 Multi Profile Management

⬜ 7.1.16 CV Management
⬜ 7.1.16.1 CV Upload
⬜ 7.1.16.2 CV Library
⬜ 7.1.16.3 CV Parsing
⬜ 7.1.16.4 Profile Enrichment

⬜ 7.1.17 Application Workflow
⬜ 7.1.17.1 Application Status Model
⬜ 7.1.17.2 Application Status Visualization
⬜ 7.1.17.3 Application Status Update
⬜ 7.1.17.4 Application Notes
⬜ 7.1.17.5 Application Timeline

⬜ 7.1.18 Opportunities Search & Filters
⬜ 7.1.18.1 Keyword Search
⬜ 7.1.18.2 Location Filters
⬜ 7.1.18.3 Remote Filters
⬜ 7.1.18.4 Salary Filters
⬜ 7.1.18.5 Source Filters
⬜ 7.1.18.6 Matching Score Filters
⬜ 7.1.18.7 Required Skills Filters
⬜ 7.1.18.8 Publication Date Filters
⬜ 7.1.18.9 User Status Filters

⬜ 7.1.19 Settings Management
⬜ 7.1.19.1 Job Discovery Settings
⬜ 7.1.19.2 Search Criteria Settings
⬜ 7.1.19.3 Matching Weights Configuration
⬜ 7.1.19.4 Source Configuration
⬜ 7.1.19.5 Default Profile Selection
⬜ 7.1.19.6 Default CV Selection
⬜ 7.1.19.7 Application Workflow Settings

⬜ 7.1.20 Profile Completeness
⬜ 7.1.20.1 Completeness Scoring
⬜ 7.1.20.2 Missing Information Detection
⬜ 7.1.20.3 Profile Quality Recommendations
⬜ 7.1.20.4 Profile Completeness Visualization

⬜ 7.1.21 Saved Searches
⬜ 7.1.21.1 Search Presets
⬜ 7.1.21.2 Saved Filters
⬜ 7.1.21.3 Default Search Strategy
⬜ 7.1.21.4 Saved Search Execution

⬜ 7.1.22 MVP Experience Review

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
