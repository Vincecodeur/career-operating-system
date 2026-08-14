# Handoff Prompt - Career Operating System

Tu reprends le projet Career Operating System.

## Règles absolues

- Toujours dire la vérité.
- Ne jamais inventer.
- Ne jamais extrapoler.
- Si une information n'est pas vérifiable, écrire : "je ne sais pas".
- Toujours partir des fichiers réels du repository.
- Toujours vérifier la cohérence entre le code, la documentation et les commits.
- Ne jamais sauter une phase.
- Ne jamais générer de code sans comprendre l'état réel du projet.
- Ne jamais introduire de complexité inutile.
- Toujours privilégier l'apprentissage, la clarté et la maintenabilité.
- Une fonctionnalité backend n'est pas considérée comme terminée tant qu'elle n'a pas été rendue visible et validée dans le frontend.
- Toujours privilégier une démonstration utilisateur rapide avant d'ajouter de nouvelles sources, de l'IA ou de nouvelles couches de complexité.

## Règle Git obligatoire

À partir de maintenant :

1 étape = 1 commit.

Pour chaque étape :

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

Une feature technique doit être commitée avec le code et les tests associés.
Un connecteur, service, endpoint ou module backend ne doit pas être commité sans ses tests lorsqu'ils sont applicables.

Ne pas mélanger dans le même commit :

- code backend ;
- code frontend ;
- tests ;
- documentation ;
- préparation de phase suivante.

## Documents à lire impérativement

Avant toute réponse, lire et croiser :

- docs/product-vision.md
- docs/architecture.md
- docs/roadmap.md
- docs/project-memory.md
- docs/project-status.md
- docs/decisions.md
- docs/ai-context.md
- docs/handoff-prompt.md
- tous les documents mentionnés comme terminés dans la phase courante

## Objectif du projet

Career Operating System est un projet personnel destiné à aider Vincent à piloter sa carrière de manière structurée, objective et basée sur des données.

Le système doit permettre :

- la gestion de plusieurs profils candidats ;
- la centralisation d'une source de vérité carrière ;
- la collecte automatisée d'opportunités professionnelles ;
- le filtrage des opportunités ;
- le matching entre profils et offres ;
- le calcul de scores explicables ;
- l'analyse des points forts et des points faibles ;
- le classement des opportunités ;
- le suivi manuel des candidatures ;
- l'analyse future du marché ;
- la planification de carrière.

Le produit est un système d'intelligence carrière et d'aide à la décision.

## Contraintes projet

- Projet personnel.
- Projet publiable sur GitHub.
- Pas de dépendance à un employeur.
- Pas de mention d'entreprise dans l'architecture, le code, la roadmap ou les exemples.
- Exception : les expériences professionnelles de Vincent peuvent être utilisées dans son profil candidat.
- Architecture simple.
- Monolithe modulaire.
- Pas de microservices.
- Pas de CQRS.
- Pas d'Event Sourcing.
- Simplicité avant optimisation.
- Maintenabilité avant sophistication.

## Stack actuelle

Backend :

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest
- Authentication
- User Model
- JWT Authentication

Frontend :

- React
- TypeScript
- Vite
- React Router
- Zustand
- TanStack Query
- React Hook Form
- Zod
- Hook Form Resolvers
- Lucide React

Architecture :

Frontend React
↓
FastAPI
↓
SQLAlchemy
↓
PostgreSQL

## Règle architecture principale

Toute logique métier appartient au backend.

Le frontend est une couche de présentation.

React ne doit pas :

- calculer le matching ;
- calculer les scores ;
- classer les opportunités ;
- appliquer des règles métier.

React consomme les APIs FastAPI et affiche les résultats.

## Règles métier importantes

- Le profil structuré constitue la source de vérité.
- Le système supporte plusieurs profils candidats.
- Opportunity Discovery est un composant central du MVP.
- La stratégie Job Discovery est API First.
- LinkedIn fait partie des sources visées par le MVP.
- Tous les scores doivent être explicables.
- Les offres sans salaire restent éligibles mais peuvent recevoir un malus.
- Les offres expirées sont archivées mais conservées.
- Toute logique métier appartient au backend.

## État fonctionnel actuel

### Backend

Implémenté :

- Profile
- Skill
- ProfileSkill
- WorkExperience
- Language
- ProfileLanguage
- Certification
- ProfileCertification
- JobOffer
- JobOfferSkill
- Matching Engine V1
- Opportunity Ranking
- Application Model
- Application CRUD
- ConnectorInterface
- FranceTravailConnector
- MockSourceConnector
- Multi Source DiscoveryService
- ConnectorRegistry
- Job Discovery Data Models
- Search Criteria
- JobSource
- JobOfferSource
- Job Discovery PostgreSQL Migration
- Job Discovery Persistence Tests
- RawOffer Schema
- NormalizedJobOffer Schema
- NormalizationService
- JobOfferRepository
- DiscoveryService
- Pipeline Validation
- DiscoveryScheduler
- Scheduled Synchronization
- Real France Travail OAuth Validation
- Real France Travail API Validation
- Real France Travail PostgreSQL Persistence Validation
- Job Discovery Overview
- Total Opportunities KPI
- Imported Opportunities KPI
- Data Source KPI
- Discovery Status KPI
- Matching V2 Design documented
- Matching V2 Backend scoring
- Matching V2 sub-scores
- Matching V2 strengths
- Matching V2 weaknesses
- Matching V2 ranking
- Matching V2 deterministic explanations
- ScoreExplanation schema
- Skills explanations
- Experience explanations
- Work mode explanations
- Location explanations
- OpportunityAnalysis schema
- Opportunity Analysis
- Deterministic verdict
- Deterministic recommendation
- Deterministic summary
- LinkedInConnector
- GreenhouseConnector
- Greenhouse End-to-End Validation
- AI Explanation Domain
- AIExplanation schemas
- AIProvider interface
- PromptBuilder
- MockAIProvider
- AIExplanationService
- ProfileSkill Update
- ProfileSkill Delete
- ProfileSkill CRUD Completion
- WorkExperienceUpdate
- WorkExperience Update
- WorkExperience Delete
- WorkExperience CRUD Completion
- ProfileLanguageUpdate
- ProfileLanguage Update
- ProfileLanguage Delete
- ProfileLanguage CRUD Completion
- ProfileCertificationUpdate
- ProfileCertification Update
- ProfileCertification Delete
- ProfileCertification CRUD Completion
- CV Model
- CV Schemas
- CV Router
- CV Service
- CV Storage
- Profile ↔ CV Relationship
- CV Download Endpoint
- CV Parsing Schemas
- CV Parsing Service
- PDF Text Extraction
- DOCX Text Extraction
- Structured CV Parsing
- Profile Enrichment Domain
- Profile Enrichment Proposals
- Profile Enrichment Acceptance Workflow
- Profile Enrichment Rejection Workflow
- Skill Catalog Mapping
- Controlled Reference Data Governance
- Repository Resolution Strategy
- Conflict Resolution Workflow

Partiellement implémenté :

Non implémenté :

- Market Intelligence
- Career Planning

### Frontend

Implémenté :

- React + TypeScript + Vite
- API Client
- Dashboard MVP
- ProfileList
- JobOfferList
- MatchingResult
- OpportunityRanking
- ApplicationTracker
- React Router
- Protected Routes
- Authentication API
- Login Page
- Forgot Password Page
- Account Page
- Auth Store
- JWT Authentication
- AppLayout
- DashboardPage
- Sidebar MVP
- Header MVP
- Layout architecture
- Dashboard Overview
- Design System document
- Tailwind CSS
- PageHeader
- Section
- Card
- StatCard
- KPI Cards
- Dashboard Component Modernization
- Modernized OpportunityRanking
- Modernized MatchingResult
- Modernized ApplicationTracker
- Modernized ProfileList
- ProfilesPage
- OpportunitiesPage
- ApplicationsPage
- SettingsPage
- Extended Route Tree
- Extended Sidebar Navigation
- Frontend Architecture Documentation
- OpportunitiesPage
- Opportunities Master / Detail View
- Opportunity Selection
- Opportunity Detail Panel
- Source Offer Navigation
- Improved Opportunity Details Experience
- Selected Opportunity Visual Highlight
- Opportunities Counter
- Opportunity Metadata Grid
- Matching Analysis Placeholder
- AI Recommendations Placeholder
- Matching V2 visualization
- Matching V2 score details
- Matching V2 strengths display
- Matching V2 weaknesses display
- Matching V2 skills analysis display
- Matching V2 deterministic explanations
- ScoreExplanation schema
- Skills explanations
- Experience explanations
- Work mode explanations
- Location explanations
- Explainable scoring visualization
- Explanations display
- Skills explanation display
- Experience explanation display
- Work mode explanation display
- Location explanation display
- Opportunity Analysis visualization
- Opportunity Analysis display
- Verdict display
- Recommendation display
- Summary display
- AIExplanationCard
- AI Explanation visualization
- AI Explanation fallback handling
- Profile Management Visualization
- Profile master/detail layout
- ProfileDetail
- Profile KPI summary
- Profile general information display
- Profile skills visualization
- Profile work experience visualization
- Profile languages visualization
- Profile certifications visualization
- EditProfileModal
- DeleteProfileDialog
- Profile Update
- Profile Archive
- Profile Frontend CRUD
- CreateProfileModal
- Profile Create
- Frontend Profile Creation
- AddProfileSkillModal
- EditProfileSkillModal
- DeleteProfileSkillDialog
- createProfileSkill
- updateProfileSkill
- deleteProfileSkill
- Frontend ProfileSkill CRUD
- AddWorkExperienceModal
- EditWorkExperienceModal
- DeleteWorkExperienceDialog
- createWorkExperience
- updateWorkExperience
- deleteWorkExperience
- Frontend WorkExperience CRUD
- AddProfileLanguageModal
- EditProfileLanguageModal
- DeleteProfileLanguageDialog
- createProfileLanguage
- updateProfileLanguage
- deleteProfileLanguage
- Frontend ProfileLanguage CRUD
- AddProfileCertificationModal
- EditProfileCertificationModal
- DeleteProfileCertificationDialog
- createProfileCertification
- updateProfileCertification
- deleteProfileCertification
- Frontend ProfileCertification CRUD
- support multi-profils confirmé
- CRUD multi-profils confirmé
- sélection de profil frontend confirmée
- absence de profils actifs pour les opportunités confirmée
- CV Management Frontend
- CV Upload
- CV Delete
- CV Default Selection
- CV Download
- UploadCvModal
- DeleteCvDialog
- UploadCvWizard Step 1 Upload
- UploadCvWizard Step 2 Analysis
- UploadCvWizard Step 3 Review & Edit
- UploadCvWizard Step 4 Summary
- Profile Enrichment Frontend Workflow
- Skill Mapping Workflow
- Conflict Resolution Workflow
- Editable Enrichment Proposals
- Proposed Value Override
- Catalog Protection UX
- Unmapped Skill Review

Documenté mais pas encore implémenté :

- Auth Layout
- shadcn/ui
- Theme Provider
- i18n structure

### Tests

Pytest est en place.

Des tests existent pour :

- health
- profiles
- skills
- job offers
- matching
- opportunity ranking
- applications
- job discovery models
- raw offer schema
- normalized job offer schema
- mock source connector
- normalization service
- job offer repository
- discovery service
- pipeline validation
- connector interface
- france travail connector
- ConnectorRegistry
- connector registry
- multi source discovery service
- scheduler
- matching v2 backend scoring
- matching v2 frontend validation
- explainable scoring backend
- opportunity analysis backend
- opportunity analysis frontend validation
- linkedin connector
- greenhouse connector
- ai schemas
- ai exceptions
- ai provider interface
- ai validators
- ai prompt builder
- ai explanation service
- mock ai provider
- profile skills
- work experiences
- profile languages
- profile certifications
- cvs
- profile enrichment

## Phases terminées

- Phase 1 - Backend Foundation
- Phase 2 - Candidate Profile
- Phase 3 - Manual Job Import
- Phase 4.1 - Matching Engine V1
- Phase 5.1 - Frontend Foundation
- Phase 5.2 - API Client
- Phase 5.3 - Dashboard MVP
- Phase 5.4 - Matching View
- Phase 5.5 - Opportunity Ranking
- Phase 5.6.1 - Application Definition
- Phase 5.6.2 - Application Model
- Phase 5.6.3 - Application CRUD
- Phase 5.6.4 - Application Tests
- Phase 5.6.5.1 - Application Tracker Component
- Phase 5.6.5.2 - Dashboard Integration
- Phase 5.7.1 - Product Clarification
- Phase 5.7.2 - Information Architecture
- Phase 5.7.3 - User Flows
- Phase 5.7.4 - Page Inventory
- Phase 5.7.5 - Wireframes
- Phase 5.7.6 - Design Direction
- Phase 5.7.7 - Frontend Structure Plan
- Phase 5.8.1 Frontend Dependencies & Technical Setup
- Phase 5.8.2 App Providers
- Phase 5.8.3 Routing & Protected Routes
- Phase 5.8.4 Authentication Flow
- Phase 5.8.5 App Layout
- Phase 5.8.6 Sidebar & Header
- Phase 5.8.7.1 Dashboard Overview
- Phase 5.8.7.5.0 Design System Document
- Phase 5.8.7.5.1 Tailwind CSS Installation
- Phase 5.8.7.5.2 First UI Components
- Phase 5.8.7.5.3 Dashboard Cards
- Phase 5.8.7.5.4 Dashboard Component Modernization
- Phase 5.8.8 MVP Page Skeletons
- Phase 5.8.9 Frontend Structure Documentation
- Phase 5.9.1 Job Sources
- Phase 5.9.2 Search Criteria
- Phase 5.9.3 Offer Normalization
- Phase 5.9.4 First External Source
- Phase 5.9.5.1 Connector Interface
- Phase 5.9.5.2 France Travail Connector
- Phase 5.9.5.3 Connector Registry
- Phase 5.9.5.4 Multi Source DiscoveryService
- Phase 5.9.5.5 Multi Source Validation
- Phase 5.9.6 Scheduled Synchronization
- Phase 5.9.7.1 Opportunities List
- Phase 5.9.7.2 Opportunity Details
- Phase 5.9.7.3 Discovery Dashboard KPI
- Phase 5.9.7.4 End-to-End Validation
- Phase 6.0.1 Matching V2 Design
- Phase 6.0.2 Matching V2 Backend
- Phase 6.0.3 Matching V2 Frontend Validation
- Phase 6.0.4 Explainable Scoring Backend
- Phase 6.0.5 Explainable Scoring Frontend Validation
- Phase 6.0.6 Opportunity Analysis Backend
- Phase 6.0.7 Opportunity Analysis Frontend Validation
- Phase 6.1.1 LinkedIn Connector Design
- Phase 6.1.2 LinkedIn Connector Backend
- Phase 6.1.3 Verification possibilité Welcome to the Jungle
- Phase 6.1.4 Greenhouse Connector Design
- Phase 6.1.5 Greenhouse Connector Backend
- Phase 6.1.6 Greenhouse End-to-End Validation
- Phase 6.1.7 Source Visualization Frontend
- Phase 6.1.8 Multi-Source Validation
- Phase 7.0.1 AI Score Explanation Design
- Phase 7.0.2 AI Explanation Backend Design
- Phase 7.0.3 AI Prompt Architecture Design
- Phase 7.0.4 AI Explanation API Design
- Phase 7.0.5 AI Provider Strategy Design
- Phase 7.0.6 AI Security & Governance Design
- Phase 7.0 Review
- Phase 7.1.13.1 Profile Management Visualization Design
- Phase 7.1.13.2 Profile Management Visualization Review
- Phase 7.1.13.3 Profile Management Visualization Implementation Plan
- Phase 7.1.13.4 Profile Management Visualization Repository Audit
- Phase 7.1.13.5 Profile Management Visualization Implementation
- Phase 7.1.14 Applications Visualization
- Phase 7.1.15.3 Profile CRUD
- Phase 7.1.15.3.1 Backend CRUD Completion
- Phase 7.1.15.3.2 Backend CRUD Tests
- Phase 7.1.15.3.3 Backend CRUD Validation
- Phase 7.1.15.3.4 Frontend CRUD Design
- Phase 7.1.15.3.5 Frontend CRUD Implementation
- Phase 7.1.15.3.6 Frontend Validation
- Phase 7.1.15.3.7 Documentation Synchronization
- Phase 7.1.15.3.8 Frontend Profile Creation
- Phase 7.1.15.4.A ProfileSkill Backend CRUD Design
- Phase 7.1.15.4.B ProfileSkill Backend CRUD Completion
- Phase 7.1.15.4.C ProfileSkill Backend Validation
- Phase 7.1.15.4.4 Frontend CRUD Implementation
- Phase 7.1.15.5 Experience Management
- Phase 7.1.15.5.1 Backend CRUD Completion
- Phase 7.1.15.5.2 Backend CRUD Validation
- Phase 7.1.15.5.3 Frontend CRUD Design
- Phase 7.1.15.5.4 Frontend CRUD Implementation
- Phase 7.1.15.5.5 Frontend Validation
- Phase 7.1.15.5.6 Documentation Synchronization
- Phase 7.1.15.6 Languages Management
- Phase 7.1.15.6.1 Backend CRUD Completion
- Phase 7.1.15.6.2 Backend CRUD Validation
- Phase 7.1.15.6.3 Frontend CRUD Design
- Phase 7.1.15.6.4 Frontend CRUD Implementation
- Phase 7.1.15.6.5 Frontend Validation
- Phase 7.1.15.6.6 Documentation Synchronization
- Phase 7.1.15.7.1 Backend CRUD Completion
- Phase 7.1.15.7.2 Backend CRUD Validation
- Phase 7.1.15.7.3 Frontend CRUD Design
- Phase 7.1.15.7.4 Frontend CRUD Implementation
- Phase 7.1.15.7.5 Frontend Validation
- Phase 7.1.15.7.6 Documentation Synchronization
- Phase 7.1.15.8 Backend Validation terminée
- Phase 7.1.16.1 Repository Audit
- Phase 7.1.16.2 CV Management Design
- Phase 7.1.16.3 Backend Data Model Design
- Phase 7.1.16.4 Backend API Design
- Phase 7.1.16.5 Backend Tests Design
- Phase 7.1.16.6 Frontend UX Design
- Phase 7.1.16.7 Backend Domain Implementation
- Phase 7.1.16.8 Backend Tests Implementation
- Phase 7.1.16.9 Backend Validation
- Phase 7.1.16.10 Frontend Implementation
- Phase 7.1.16.11 Frontend Validation
- Phase 7.1.16.12 CV Parsing Design
- Phase 7.1.16.13 CV Parsing Implementation
- Phase 7.1.16.13.1 Parsing Schemas
- Phase 7.1.16.13.2 Parsing Service
- Phase 7.1.16.13.3 PDF Support
- Phase 7.1.16.13.4 DOCX Support
- Phase 7.1.16.13.5 Parsing Tests
- Phase 7.1.16.13.6 Backend Validation
- Phase 7.1.16.14.1 Product Design terminée
- Phase 7.1.16.14.2 Reference Data Governance terminée
- Phase 7.1.16.14.3 Repository Resolution Strategy terminée
- Phase 7.1.16.14.4 Conflict Management Design terminée
- Phase 7.1.16.14.5 Enrichment Workflow Design terminée
- Phase 7.1.16.14.6 Backend Technical Design
- Phase 7.1.16.14.7 Backend Implementation
- Phase 7.1.16.14.8 Backend Tests
- Phase 7.1.16.14.9 Backend Validation
- Phase 7.1.16.14.10 Frontend UX Design
- Phase 7.1.16.14.11 Frontend Implementation
- Phase 7.1.16.14.12 Frontend Validation
- Phase 7.1.16.15 Documentation Synchronization
- Phase 7.1.16.16 Reference Data Catalog Design
- Phase 7.1.16.16.1 Skill Catalog Mapping Design
- Phase 7.1.16.16.2 Language Catalog Normalization Design
- Phase 7.1.16.16.3 Country Catalog Normalization Design
- Phase 7.1.16.16.4 Work Mode Catalog Design
- Phase 7.1.16.16.5 Contract Type Catalog Design
- Phase 7.1.16.16.6 Preference Options Design

## Derniers commits importants

- a91a7df - test: add reference data api coverage
- 30c2c0f - docs: synchronize reference data catalog api status
- 8b9d79a - feat: add reference data seed loader
- fd59521 - feat: add reference data api
- f06b889 - fix: fix cv parsing docx et pdf
- f1acd03 - docs: add reference data catalog roadmap
- aa44437 - feat(cv): map unknown skills to existing catalog entries
- 7c3abf3 - docs : skill-catalog-mapping design and decision
- 1cf897d - feat(cv): support skill mapping during enrichment accept
- 73fa003 - feat(cv): finalize profile enrichment workflow
- 23da381 - feat(cv): finalize profile enrichment workflow
- 382cda7 - feat(cv): finalize profile enrichment workflow
- 0d79f1b - fix: support long enrichment proposal values
- 5022005 - fix: support long enrichment proposal values
- cccd778 - test: add profile enrichment backend coverage
- ee679cc - feat : profile-enrichment-design implementation
- 0528f74 - feat: CV parsing service implementation
- a923afc - feat: complete cv management frontend
- 42f1bb2 - docs: synchronize cv backend implementation status
- 4cf5193 - chore: ignore generated cv storage directory
- a91e42b - chore: ignore generated cv storage files
- 0dcdc9f - feat: add cv management backend domain
- 4bc24c5 - docs: align roadmap after multi profile review
- 03c7e86 - docs: close certifications management phase
- 4615c02 - docs: close certifications management phase
- 005465e - feat: add frontend profile certification crud
- 35824ec - feat: complete profile certification crud backend
- f955978 - feat: add profile language frontend crud
- 0c33a61 - docs: synchronize profile language
- c06e745 - feat: complete profile language crud backend
- 93afcae - feat: add frontend work experience crud
- da0635b - test: add work experience crud coverage
- ca1ce1b - feat: complete work experience crud backend
- a2c1ef0 - feat: add frontend profile skill crud
- b1db1ca - feat: complete profile skill crud backend
- f54172e - feat: add frontend profile creation
- aba55bd - feat: complete skills update crud
- 367f3f1 - docs: synchronize profile frontend crud
- 0da9765 - feat: implement profile frontend crud
- be143c6 - docs: close profile crud validation
- 5f55b9e - feat: implement applications visualization
- 94727f8 - feat: implement profile management visualization
- a612b0b - docs: define profile management visualization
- 14e6830 - docs: synchronize ai explanation frontend implementation
- 9eddaa9 - feat: add ai explanation frontend integration
- 1cf1560 - docs: document ai explanation frontend integration
- a95a2af - feat: add ai explanation domain foundation
- 4993cec - docs: close phase 7 review
- a1646fc - docs: synchronize phase 7 review status
- 5303d32 - docs : add greenhouse connector design
- c26f13a - docs: synchronize Linkedin Connecteur Backend
- de999b3 - docs: linkedin-connector-backend-design.md
- 7a2eb90 - feat: add opportunity analysis frontend
- 906f405 - feat: add opportunity analysis backend
- e33bc1f - feat: add explainable scoring frontend
- 53f059b - feat: add deterministic matching explanations
- 35df497 - feat: add matching v2 frontend validation
- 1452dcc - feat: implement matching v2 backend scoring
- 47725a5 - docs: define matching v2 design
- 467c150 - fix: make dashboard source KPI accurate
- 2dabed2 - feat: add job discovery dashboard kpis
- 30caf05 - feat: improve opportunity details experience
- 7ccac70 - feat: implement opportunities master detail view
- a141ae3 - docs: validate france travail end-to-end pipeline
- ad29764 - feat: add scheduled job discovery
- 09b52bc - docs: synchronize France Travail connector
- 87aa796 - feat: add multi source discovery service
- 587f1ec - feat: add connector registry
- e7f92d4 - docs: synchronize connector registry
- bddc081 - feat: add France Travail connector
- 2599fb8 - docs: synchronize connector package refactor
- 5d45a13 - refactor: move connectors to dedicated package
- b42f9f9 - docs: synchronize connector interface
- c495bf3 - feat: connector_interface.py
- 4d4956f - feat: pipeline validation
- 45bbf42 - docs: synchronize pipeline validation
- 16f5041 - docs: synchronize job offer repository
- 0c4f09b - feat: add discovery service
- cbcb8f9 - commit documentaire DiscoveryService
- 67e26e6 - docs: synchronize normalization service
- 4f5adde - docs: synchronize mock source connector
- 44f2274 - feat: add mock source connector
- fafa8f9 - feat: add normalized job offer schema
- 49aed32 - docs: synchronize raw and normalized offer schemas
- 93f8b63 - feat: add raw offer schema
- 733179d - feat: add job discovery data-model.md, model-migration.md technical-design.md
- 55bc29f - feat: add job discovery data models
- 29816fb - docs: define offer normalization
- ce842f5 - docs: define search criteria
- 8a0a56a - docs: define job discovery sources
- c56bd3b - docs: add frontend architecture documentation
- 117c972 - feat: add mvp page skeletons
- 31ed22f - docs: synchronize dashboard component modernization
- a908f36 - feat: modernize dashboard components
- 6e42175 - docs: add design system foundation
- 7f285fe - feat: implement frontend authentication flow
- 8e0560f - feat: implement backend authentication flow
- 8af58bd - feat: add authentication user model
- 21836af - chore: add authentication dependencies
- b4f3a7b - feat: add frontend routing foundation
- c015510 - docs: synchronize phase 5.8.1 dependency installation
- ab9d149 - chore: install frontend architecture dependencies
- 408b576 - docs: finalize phase 5.7 ux architecture and frontend planning
- 0717453 - docs: update application tracker frontend documentation
- f9060c8 - feat: connect application tracker to dashboard
- 7828d0b - feat: add application tracker component
- 9893c4d - docs: synchronize application tracker phase
- 834c331 - feat: implement application crud

## Résultat métier validé

Le système a démontré un flux complet :

Profile
↓
ProfileSkill
↓
JobOffer
↓
JobOfferSkill
↓
Matching Engine
↓
Opportunity Ranking
↓
FastAPI
↓
React
↓
Dashboard

Exemple de résultat validé :

- Score : 75 %
- Matching Skills :
  - Python
  - FastAPI
  - Azure
- Missing Skills :
  - Kubernetes

## Décisions clés

Respecter notamment :

- DEC-013 : Profile Source Of Truth
- DEC-017 : Multi Profiles
- DEC-030 : Dashboard First MVP
- DEC-033 : Opportunity Ranking
- DEC-034 : Application Tracker
- DEC-035 : Structured Profile Source Of Truth
- DEC-036 : Opportunity Discovery Core MVP
- DEC-037 : API First Job Discovery
- DEC-038 : LinkedIn MVP Target Source
- DEC-039 : Explainable Opportunity Scoring
- DEC-040 : UX First Frontend Strategy
- DEC-041 : Standardized Job Evaluation Rules
- DEC-042 : Frontend Technical Stack
- DEC-043 : Authentication From MVP
- DEC-044 : Multilingual Ready Frontend
- DEC-045 :
- DEC-046 :
- DEC-047 :
- DEC-048 :
- DEC-049 :
- DEC-050 :
- DEC-051 :
- DEC-052 :
- DEC-053 :
- DEC-054 :

### Phase suivante recommandée

7.1.16.17.8 Frontend Integration

Objectif :

Consommer les catalogues de référence dans le frontend.

Périmètre :

- Countries catalog
- WorkModes catalog
- ContractTypes catalog

Utilisation cible :

- Profile Preferences
- CV Enrichment
- Search Filters
- Matching Inputs

Les valeurs libres doivent être progressivement remplacées par les référentiels contrôlés.

## Méthode de reprise

Avant toute implémentation :

- vérifier que la phase précédente est terminée ;
- vérifier que la phase courante dispose d'un document de design ;
- réaliser un audit du code réel concerné par la phase ;
- ne jamais produire de code à partir de la documentation seule.

Au démarrage d'un nouveau thread :

1. Lire tous les documents listés.
2. Résumer l'état réel du projet.
3. Vérifier la cohérence documentaire.
4. Identifier la phase courante.
5. Identifier le dernier commit.
6. Vérifier s'il existe des modifications non commitées.
7. Proposer uniquement la prochaine étape.
8. Attendre validation ou mot-clé `forward`.

## Mot-clé forward

Si Vincent écrit :

forward

alors :

- reprendre exactement la prochaine étape annoncée précédemment ;
- ne pas sauter d'étape ;
- rappeler :
  "Forward détecté → lancement de l'étape X annoncée précédemment."

## Interdictions

Ne pas :

- inventer l'état du repository ;
- supposer l'existence d'un fichier ;
- générer un fichier sans connaître son contexte ;
- mélanger plusieurs étapes dans un seul commit ;
- passer au frontend avant validation backend ;
- passer à la documentation de clôture avant validation fonctionnelle ;
- introduire IA, embeddings, scraping ou automatisation avancée sans décision documentée.
