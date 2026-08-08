# Roadmap

## Règle de progression

Une phase est terminée uniquement lorsque :

- le développement est terminé ;
- les tests sont passants ;
- la documentation est à jour ;
- project-status.md est à jour ;
- la prochaine étape est clairement définie.

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
- ⏳ 5.9.4 First External Source
  - ✅ 5.9.4.1 Job Discovery Data Models
  - ✅ 5.9.4.2 RawOffer Schema
  - ✅ 5.9.4.3 NormalizedJobOffer Schema
  - ⏳ 5.9.4.4 MockSourceConnector
  - ⏳ 5.9.4.5 NormalizationService
  - ⏳ 5.9.4.6 JobOfferRepository
  - ⏳ 5.9.4.7 DiscoveryService
  - ⏳ 5.9.4.8 Pipeline Validation

- 5.9.5 Multi Source Support
- 5.9.6 Scheduled Synchronization

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
- classer les opportunités.

Sous-phases :

- 6.0.1 Matching V2
- 6.0.2 Explainable Scoring
- 6.0.3 Strengths Analysis
- 6.0.4 Weaknesses Analysis
- 6.0.5 Opportunity Ranking V2
- 6.0.6 Opportunity Details

Statut :
Planned

### Phase 6.1

Application Assistant

Objectif :

Aider à préparer les candidatures à partir :

- du profil candidat ;
- des opportunités analysées ;
- des points forts ;
- des points faibles.

Limites :

- aucune candidature automatique ;
- aucun envoi automatique de CV ;
- aucun agent autonome.

Statut :
Planned

### Phase 7

Market Intelligence

Objectif :

Analyser le marché de l'emploi à partir des offres collectées.

Exemples :

- compétences les plus demandées ;
- postes les plus présents ;
- évolution du marché ;
- tendances de recrutement.

Statut :
Planned

### Phase 8

Career Roadmap

Objectif :

Construire une stratégie de progression de carrière basée sur :

- le profil candidat ;
- les opportunités ;
- le marché ;
- les écarts de compétences.

Statut :
Planned
