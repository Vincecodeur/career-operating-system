# Architecture

## Objectif

Construire une plateforme personnelle modulaire permettant :

- la gestion de plusieurs profils candidats ;
- la centralisation d'une source de vérité carrière ;
- la collecte automatisée d'offres d'emploi ;
- l'analyse des opportunités ;
- le matching entre profils et offres ;
- le classement des opportunités ;
- le suivi des candidatures ;
- l'analyse future du marché ;
- la planification de carrière.

Le système est conçu comme une plateforme personnelle d'intelligence carrière et d'aide à la décision.

---

## Architecture générale

Frontend

React
TypeScript
Vite

↓

Backend API

FastAPI
Python

↓

Database

PostgreSQL

↓

AI Layer

OpenAI API

---

## Principe fondamental

Le système doit rester utilisable sans IA.

L'IA vient enrichir l'expérience utilisateur.

Le fonctionnement principal du produit ne doit jamais dépendre totalement d'un fournisseur IA.

### Source de vérité

Le profil structuré enregistré dans l'application constitue la source de vérité du système.

Les données peuvent provenir de plusieurs sources :

- CV ;
- LinkedIn ;
- analyses Copilot ;
- saisie manuelle ;
- autres sources futures.

Ces sources servent uniquement à enrichir le profil.

Toutes les analyses, comparaisons et décisions s'appuient sur le profil structuré enregistré dans la base de données.

---

## Domaines métier

### Profile

Gestion des profils candidats.

Sous-domaines :

- Profile
- Skill
- ProfileSkill
- WorkExperience
- Language
- ProfileLanguage
- Certification
- ProfileCertification

Le système supporte plusieurs profils candidats.

### Search Criteria

Gestion des critères de recherche d'opportunités.

Exemples :

- pays ;
- work mode ;
- salaire minimum ;
- langues ;
- types de contrat ;
- titres recherchés ;
- mots-clés inclus ;
- mots-clés exclus.

### Job Discovery

Collecte d'offres d'emploi depuis des sources externes.

Principes :

- API first ;
- scraping uniquement lorsqu'aucune API exploitable n'existe ;
- collecte quotidienne ;
- normalisation des données.

### Job Sources

Gestion des sources d'offres.

Types prévus :

- API ;
- SCRAPING ;
- MANUAL_IMPORT.

### Opportunity Analysis

Analyse détaillée des opportunités.

Le système doit être capable :

- d'évaluer une opportunité ;
- d'identifier les points forts ;
- d'identifier les points faibles ;
- d'expliquer les scores ;
- de détecter les compétences manquantes.

### Matching

Comparaison profil ↔ offre.

Version actuelle :

- matching basé sur les compétences.

Version future :

- compétences ;
- langues ;
- séniorité ;
- localisation ;
- work mode ;
- salaire ;
- autres critères configurables.

### Opportunity Ranking

Classement des opportunités.

Le classement est calculé exclusivement par le backend.

Le frontend affiche les résultats.

### Applications

Suivi manuel des candidatures.

Le système ne réalise aucune candidature automatique.

Le domaine Applications implémente désormais un workflow de candidature.

Une Application est liée à :

- un profil ;
- une offre d’emploi.

Une Application contient :

- status ;
- notes ;
- source_type.

Le système conserve également un historique structuré via ApplicationEvent.

ApplicationEvent permet notamment de tracer :

- APPLICATION_CREATED ;
- STATUS_CHANGED.

L’objectif est de fournir un suivi complet du cycle de vie d’une candidature.

An Application may be created:

- directly from an Opportunity
- manually by the user

### Market Intelligence

Analyse future du marché.

### Career Planning

Planification de carrière.

### AI

Services IA d'assistance.

L'IA enrichit l'analyse mais ne constitue jamais la seule source de vérité.

---

### Entités principales

Profile
Représente un profil candidat.

Skill
Catalogue central de compétences.

ProfileSkill
Relation entre un profil et une compétence.

WorkExperience
Expérience professionnelle.

Language
Catalogue central de langues.

ProfileLanguage
Relation entre un profil et une langue.

Certification
Catalogue central de certifications.

ProfileCertification
Relation entre un profil et une certification.

SearchCriteria
Critères de recherche associés à un profil.

JobSource
Source externe d'opportunités.

JobOffer
Offre d'emploi normalisée.

OpportunityAnalysis
Résultat d'analyse d'une opportunité.

Application
Candidature suivie dans le système.

MarketInsight
Analyse marché.

CareerGoal
Objectif carrière futur.

---

## Architecture Backend

app/
core/
profile/
skills/
experience/
languages/
jobs/
matching/
applications/

### Futurs domaines prévus

search_criteria/
job_discovery/
job_sources/
opportunity_analysis/
market/
career/
ai/

---

## Architecture Frontend

src/

pages/
components/
features/
services/
hooks/
layouts/

Architecture cible :

Dashboard
Profile
Search Criteria
Opportunities
Opportunity Details
Applications
Settings

### Architecture Frontend Cible

Stack frontend validée :

- React Router
- Zustand
- TanStack Query
- React Hook Form
- Zod
- shadcn/ui
- Tailwind CSS
- Lucide Icons

Principes :

- Authentification dès le MVP
- Routes protégées
- Sidebar rétractable
- Desktop First
- Light Theme
- Dark Theme
- WCAG AA
- Internationalisation dès l'architecture

Langue MVP :

- English

Langue post MVP :

- Français

---

## Règles architecture

- Architecture modulaire.
- Responsabilités clairement séparées.
- Pas de dépendances circulaires.
- Logique métier dans le backend.
- Frontend focalisé sur la présentation.
- Module AI isolé.
- Simplicité avant optimisation.
- Le profil structuré constitue la source de vérité.
- Les scores doivent toujours être explicables.
- Toute logique de scoring appartient au backend.
- Toute logique de matching appartient au backend.
- L'IA enrichit les résultats mais ne remplace jamais les règles métier.
- Les offres collectées conservent leur lien source d'origine.
- Le frontend est une couche de navigation et de visualisation.

---

### Work Mode

Le système prend en charge les modes de travail suivants :

- Remote
- Hybrid
- Onsite

Ce critère pourra être utilisé dans :

- les critères de recherche ;
- le filtrage ;
- le scoring ;
- l'analyse des opportunités.

---

## Architecture cible

Monolithe modulaire.

Pas de microservices.

Pas de CQRS.

Pas d'Event Sourcing.

Pas de complexité prématurée.

---

Frontend navigation supports:

Profile
↔ Applications

Opportunity
↔ Applications

Applications
↔ Profile

Applications
↔ Opportunity

Applications may be created directly from Opportunities.
