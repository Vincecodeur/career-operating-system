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

### Profile

Gestion du profil candidat.

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

JobOffer

Représente une offre d'emploi.

Application

Représente une candidature.

Skill

Représente une compétence.

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
