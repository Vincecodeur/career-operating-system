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

## Règle Git obligatoire

À partir de maintenant :

1 étape = 1 commit.

Pour chaque étape :

1. Développement de l'étape
2. Validation fonctionnelle
3. Tests si applicable
4. Commit dédié
5. Mise à jour documentaire
6. Commit documentaire dédié
7. Push
8. `git status` propre
9. Étape suivante uniquement après validation

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

Non implémenté :

- Search Criteria
- Job Discovery
- Job Sources
- Opportunity Analysis
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

Documenté mais pas encore implémenté :

- Auth Layout
- App Layout
- Sidebar rétractable
- Header léger
- shadcn/ui
- Tailwind CSS
- Lucide Icons
- Zustand
- TanStack Query
- React Hook Form
- Zod
- Theme Provider
- i18n structure
- Login Page
- Forgot Password Page
- My Account Page

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

## Derniers commits importants

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
- DEC-045 : Design System Strategy

### Phase suivante recommandée

Phase 5.8.4 - Authentication Pages

Objectif :

Créer les premières pages d'authentification prévues dans l'architecture cible.

Livrables :

- Login Page
- Forgot Password Page
- My Account Page placeholder
- structure d'authentification frontend

Pas encore :

- JWT backend
- login fonctionnel
- refresh token
- API authentication

## Méthode de reprise

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
