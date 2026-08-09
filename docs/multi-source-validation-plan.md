# Multi-Source Validation Plan

## Phase

6.1.8 Multi-Source Validation

## Statut

Planned

## Contexte

Le projet supporte désormais plusieurs sources d'opportunités professionnelles :

- France Travail
- LinkedIn
- Greenhouse

Chaque source utilise le pipeline standardisé :

Connector
↓
RawOffer
↓
NormalizationService
↓
NormalizedJobOffer
↓
JobOfferRepository
↓
PostgreSQL
↓
FastAPI
↓
Frontend

Les connecteurs ont déjà été validés individuellement.

L'objectif de cette phase est désormais de valider leur fonctionnement simultané dans un environnement unique.

Aucune nouvelle source ne sera ajoutée durant cette phase.

Aucune fonctionnalité IA ne sera ajoutée durant cette phase.

Cette phase est exclusivement dédiée à la validation du fonctionnement multi-source de la plateforme.

## Objectifs

Valider que :

- plusieurs connecteurs peuvent être activés simultanément ;
- DiscoveryScheduler fonctionne correctement avec plusieurs connecteurs ;
- les offres sont correctement stockées dans PostgreSQL ;
- les APIs FastAPI retournent les résultats attendus ;
- le frontend affiche correctement les données multi-sources ;
- la déduplication continue de fonctionner ;
- les indicateurs de suivi restent cohérents.

## Périmètre

### Inclus

- France Travail
- LinkedIn
- Greenhouse

- DiscoveryScheduler
- DiscoveryService
- NormalizationService
- JobOfferRepository

- PostgreSQL
- FastAPI
- Frontend Opportunities

### Exclus

- nouveaux connecteurs
- IA
- analyse de marché
- scoring IA
- nouvelles fonctionnalités frontend
- optimisation des performances
- monitoring avancé

## Architecture à valider

France Travail
↓
RawOffer

LinkedIn
↓
RawOffer

Greenhouse
↓
RawOffer

RawOffer
↓
NormalizationService
↓
NormalizedJobOffer
↓
JobOfferRepository
↓
PostgreSQL
↓
FastAPI
↓
OpportunitiesPage

## Cas de validation

### Validation 1 - Registry

Objectif

Vérifier que tous les connecteurs attendus sont enregistrés.

Résultat attendu

Connecteurs disponibles :

- mock
- france_travail
- linkedin
- greenhouse

Critère de succès

Registry retourne 4 connecteurs.

---

### Validation 2 - Scheduler

Objectif

Vérifier que DiscoveryScheduler exécute plusieurs connecteurs.

Résultat attendu

Le scheduler démarre sans erreur.

Chaque connecteur configuré est exécuté.

Critère de succès

Aucune exception.

Tous les connecteurs configurés sont appelés.

---

### Validation 3 - Import Multi-Source

Objectif

Valider l'import simultané des offres.

Résultat attendu

Les offres provenant de plusieurs sources sont importées.

Critère de succès

Présence de données provenant :

- de France Travail
- de LinkedIn
- de Greenhouse

dans PostgreSQL.

---

### Validation 4 - Déduplication

Objectif

Vérifier qu'une même offre ne crée pas de doublons.

Résultat attendu

Une offre déjà connue est mise à jour et non recréée.

Critère de succès

Pas de croissance artificielle du volume des offres.

---

### Validation 5 - PostgreSQL

Objectif

Valider la persistance des données.

Résultat attendu

Les offres multi-sources sont présentes dans les tables métier.

Critère de succès

Présence correcte des JobOffer et JobOfferSource.

---

### Validation 6 - API Job Offers

Objectif

Vérifier les endpoints FastAPI.

Résultat attendu

L'API expose des offres provenant de plusieurs sources.

Critère de succès

Le champ source est correctement renseigné.

---

### Validation 7 - Frontend Opportunities

Objectif

Valider l'affichage multi-source.

Résultat attendu

L'utilisateur visualise :

- l'origine de l'offre ;
- le détail de l'offre ;
- le lien vers l'offre source.

Critère de succès

Les sources sont visibles dans Opportunities.

---

### Validation 8 - Dashboard KPI

Objectif

Valider les KPI Discovery.

Résultat attendu

Les KPI reflètent correctement les données importées.

Critère de succès

Cohérence entre :

- PostgreSQL
- API
- Dashboard

---

### Validation 9 - End-to-End

Objectif

Valider le flux complet.

Résultat attendu

Source externe
↓
Connector
↓
Database
↓
API
↓
Frontend

Critère de succès

L'utilisateur visualise les offres importées depuis plusieurs sources.

## Critères de réussite de la phase

La phase est considérée comme terminée lorsque :

- tous les tests backend sont passants ;
- les validations manuelles sont réalisées ;
- plusieurs sources sont visibles dans Opportunities ;
- les KPI Dashboard restent cohérents ;
- aucune régression n'est observée ;
- la documentation est mise à jour ;
- le commit technique est réalisé ;
- le commit documentaire est réalisé ;
- git status est propre.

## Livrables attendus

- Validation Registry
- Validation Scheduler
- Validation PostgreSQL
- Validation API
- Validation Frontend
- Validation KPI
- Validation Déduplication
- Validation End-to-End
- Documentation de résultats

## Hors périmètre

Cette phase ne doit pas :

- ajouter un nouveau connecteur ;
- ajouter une fonctionnalité IA ;
- modifier le moteur de matching ;
- modifier le scoring ;
- modifier l'architecture ;
- introduire du scraping supplémentaire ;
- introduire de nouvelles dépendances techniques.

## Étape suivante prévue

Phase 7.0

AI Explanation Layer

Cette étape ne pourra être démarrée qu'après validation complète de la phase 6.1.8.
