# Architecture

## Objectif

Construire une plateforme personnelle modulaire permettant :

- la gestion du profil candidat ;
- l'analyse du marché ;
- le matching des offres ;
- le suivi des candidatures ;
- l'analyse des compétences ;
- la planification de carrière.

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

---

## Domaines métier

#### Profile

Gestion du profil candidat.

Sous-domaines :

- Profile
- Skill
- ProfileSkill
- WorkExperience
- Language
- ProfileLanguage

### Jobs

Gestion des offres.

### Matching

Comparaison profil ↔ offres.

### Applications

Suivi des candidatures.

### Market

Analyse du marché.

### AI

Services IA.

### Career Planning

Planification de carrière.

---

## Entités principales

Profile
Représente le candidat.

Skill
Catalogue central des compétences.

ProfileSkill
Relation entre un profil et une compétence.

WorkExperience
Expérience professionnelle du candidat.

Language
Catalogue central des langues.

ProfileLanguage
Relation entre un profil et une langue.

JobOffer
Représente une offre d'emploi.

Application
Représente une candidature.

MarketInsight
Représente une analyse marché.

CareerGoal
Représente un objectif professionnel.

LearningRecommendation
Représente une recommandation d'apprentissage.

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

---

## Règles architecture

- Architecture modulaire.
- Responsabilités clairement séparées.
- Pas de dépendances circulaires.
- Logique métier dans le backend.
- Frontend focalisé sur la présentation.
- Module AI isolé.
- Simplicité avant optimisation.

---

## Architecture cible

Monolithe modulaire.

Pas de microservices.

Pas de CQRS.

Pas d'Event Sourcing.

Pas de complexité prématurée.
