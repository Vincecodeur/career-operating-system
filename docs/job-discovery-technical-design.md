# Job Discovery Technical Design

## Objectif

Définir l'architecture technique du module Job Discovery avant toute implémentation backend.

Ce document sert de référence pour la création du module :

backend/app/job_discovery/

Il définit :

- l'arborescence cible ;
- les responsabilités des dossiers ;
- les interfaces des connecteurs ;
- le pipeline de découverte ;
- le pipeline de normalisation ;
- la persistance ;
- les tests attendus ;
- les points d'extension futurs.

Ce document s'appuie sur les décisions et documents existants :

- docs/job-sources.md
- docs/search-criteria.md
- docs/offer-normalization.md
- docs/first-external-source.md
- docs/decisions.md

---

CONTEXTE

Le module Job Discovery a pour objectif de collecter des offres d'emploi depuis une ou plusieurs sources externes, puis de les transformer en offres normalisées exploitables par le reste du système.

Le module ne doit pas seulement récupérer des offres.

Il doit valider le flux complet :

Source
↓
Connector
↓
Raw Offer
↓
Normalization
↓
JobOffer
↓
Database

Ce pipeline est obligatoire.

Aucune offre ne doit être persistée sans passer par l'étape de normalisation.

---

DÉCISIONS STRUCTURANTES

Les décisions suivantes sont déjà validées dans docs/decisions.md :

DEC-047 Connector Pattern

Chaque source d'offres possède son propre connecteur.

Exemples :

- FranceTravailConnector
- LinkedInConnector

Tous les connecteurs exposent une interface commune.

Objectif :

Permettre l'ajout de nouvelles sources sans modifier la logique métier.

---

DEC-048 Offer As Primary Discovery Entity

L'entité métier principale du Job Discovery est JobOffer.

Les sources sont des mécanismes de découverte.

Une même offre peut être associée à plusieurs sources.

---

DEC-049 Job Discovery Pipeline

Toutes les offres suivent obligatoirement le pipeline :

Source
↓
Connector
↓
Normalization
↓
Database

Aucune offre ne peut contourner l'étape de normalisation.

---

DEC-050 France Travail First External Source

La première source externe ciblée est France Travail.

Plan B :

- LinkedIn

La stratégie retenue est API First.

---

OBJECTIF DE LA PHASE 5.9.4

La phase 5.9.4 First External Source doit valider le premier flux réel ou simulé :

France Travail
↓
Connector
↓
Normalization
↓
Database

Si les accès France Travail ne sont pas disponibles au moment de l'implémentation, une source mock temporaire doit permettre de valider le pipeline interne sans bloquer le développement.

---

ARCHITECTURE CIBLE DU MODULE

Arborescence cible :

backend/app/job_discovery/

connectors/
base.py
france_travail.py
mock_source.py

normalization/
service.py
mappers.py

repositories/
job_offer_repository.py

schemas/
raw_offer.py
normalized_job_offer.py

services/
discovery_service.py

models.py
router.py

---

IMPORTANT

Les dossiers doivent être créés uniquement lorsqu'ils deviennent nécessaires.

Cette arborescence est une cible.

Elle ne doit pas être créée entièrement dès le premier commit si certains fichiers ne sont pas encore utilisés.

Le projet suit les décisions existantes :

- aucun dossier vide ;
- aucune création anticipée ;
- chaque dossier créé doit avoir une utilité immédiate.

---

RESPONSABILITÉ DES DOSSIERS

## connectors/

Le dossier connectors contient les connecteurs vers les sources externes.

Responsabilités :

- se connecter à une source ;
- récupérer les offres brutes ;
- encapsuler les spécificités de chaque source ;
- exposer une interface commune ;
- ne pas contenir de logique de persistance ;
- ne pas contenir de logique métier de normalisation avancée.

Exemples :

- FranceTravailConnector
- MockSourceConnector
- LinkedInConnector futur

---

## connectors/base.py

Responsabilité :

Définir le contrat commun à tous les connecteurs.

Interface cible :

- fetch_offers()
- fetch_offer_detail() si nécessaire
- source_name

Le connecteur de base doit permettre au DiscoveryService d'utiliser n'importe quelle source sans connaître ses détails internes.

---

## connectors/france_travail.py

Responsabilité :

Implémenter le connecteur France Travail.

Responsabilités spécifiques :

- gestion de l'authentification OAuth2 ;
- appel à l'API France Travail ;
- récupération des offres ;
- récupération du détail des offres si nécessaire ;
- transformation minimale vers RawOffer.

Ce connecteur ne doit pas sauvegarder les offres en base.

---

## connectors/mock_source.py

Responsabilité :

Fournir une source temporaire simulée.

Objectif :

Permettre de valider le pipeline interne lorsque les accès France Travail ne sont pas encore disponibles.

Le mock source doit produire des offres plausibles respectant les données attendues.

Le mock source est temporaire.

Il doit rester clairement identifié comme outil de validation technique.

---

## normalization/

Le dossier normalization contient la logique de transformation des offres brutes en offres normalisées.

Responsabilités :

- transformer une RawOffer en NormalizedJobOffer ;
- mapper les contrats ;
- mapper le work mode ;
- mapper la séniorité ;
- mapper la langue ;
- normaliser le salaire ;
- extraire les compétences ;
- évaluer le quality_level.

La normalisation est obligatoire avant toute persistance.

---

## normalization/service.py

Responsabilité :

Orchestrer la normalisation.

Entrée :

RawOffer

Sortie :

NormalizedJobOffer

Ce service ne doit pas connaître les détails spécifiques des APIs externes.

Il reçoit une offre brute déjà encapsulée dans un format interne RawOffer.

---

## normalization/mappers.py

Responsabilité :

Contenir les fonctions de mapping.

Exemples :

- normalize_contract_type()
- normalize_work_mode()
- normalize_seniority()
- normalize_language()
- normalize_salary()
- extract_skills()
- compute_quality_level()

Ces fonctions doivent rester pures autant que possible.

Elles doivent être faciles à tester.

---

## repositories/

Le dossier repositories contient la logique d'accès à la base de données.

Responsabilités :

- chercher une offre existante ;
- créer une offre ;
- mettre à jour une offre ;
- associer une offre à une source ;
- appliquer les règles de déduplication ;
- archiver une offre si nécessaire.

---

## repositories/job_offer_repository.py

Responsabilité :

Persister les JobOffer normalisés.

Fonctions cibles :

- find_duplicate()
- create_job_offer()
- update_job_offer()
- attach_source()
- archive_job_offer()

Le repository ne doit pas appeler les sources externes.

Le repository ne doit pas faire de requêtes HTTP.

---

## schemas/

Le dossier schemas contient les structures de données internes utilisées par le pipeline.

Responsabilités :

- définir RawOffer ;
- définir NormalizedJobOffer ;
- sécuriser les échanges entre connecteurs, normalisation et services.

---

## schemas/raw_offer.py

Responsabilité :

Définir une offre brute interne.

RawOffer n'est pas le format natif d'une source.

RawOffer est un format intermédiaire commun avant normalisation.

Champs possibles :

- source_name
- source_job_id
- source_url
- title
- company
- raw_description
- city
- region
- country
- contract_type_raw
- work_mode_raw
- salary_raw
- published_at_raw
- language_raw
- raw_payload

---

## schemas/normalized_job_offer.py

Responsabilité :

Définir le format normalisé attendu avant persistance.

Champs possibles :

- title
- company
- description_raw
- description_normalized
- url_primary
- language
- city
- region
- country
- work_mode
- contract_type
- seniority
- salary_min
- salary_max
- salary_currency
- salary_original_text
- skills_extracted
- skills_normalized
- quality_level
- status

---

## services/

Le dossier services contient l'orchestration métier du Job Discovery.

Responsabilités :

- choisir le connecteur ;
- lancer la collecte ;
- envoyer chaque offre à la normalisation ;
- envoyer chaque offre normalisée au repository ;
- compter les résultats ;
- retourner un résumé d'import.

---

## services/discovery_service.py

Responsabilité :

Orchestrer le pipeline complet.

Flux cible :

1. sélectionner une source ;
2. récupérer les offres brutes ;
3. normaliser chaque offre ;
4. détecter les doublons ;
5. créer ou mettre à jour les offres ;
6. associer les sources ;
7. retourner un résumé.

Le DiscoveryService ne doit pas contenir de code spécifique France Travail.

Il doit manipuler des connecteurs via leur interface commune.

---

## models.py

Responsabilité :

Contenir les modèles SQLAlchemy du domaine Job Discovery.

Modèles cibles :

- JobSource
- JobOffer
- JobOfferSource

Ces modèles sont définis dans docs/offer-normalization.md.

---

## router.py

Responsabilité :

Exposer les endpoints API du domaine Job Discovery.

Endpoints potentiels :

- POST /job-discovery/import
- GET /job-discovery/offers
- GET /job-discovery/offers/{id}

Le router ne doit pas contenir de logique métier.

Il appelle les services.

---

PIPELINE TECHNIQUE

Flux complet cible :

Client API ou commande manuelle
↓
JobDiscovery Router
↓
DiscoveryService
↓
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

---

PREMIÈRE SOURCE

Source cible :

France Travail

Mode :

API officielle

Authentification :

OAuth2

Environnement :

Sandbox puis Production

Plan B :

Mock Source si les accès France Travail ne sont pas disponibles.

---

MOCK SOURCE

La Mock Source est autorisée uniquement pour valider le pipeline interne.

Elle doit permettre de vérifier :

- connecteur ;
- normalisation ;
- persistance ;
- déduplication ;
- tests automatisés.

Elle ne doit pas devenir la source principale du produit.

---

RÈGLES DE NORMALISATION

Les règles sont définies dans docs/offer-normalization.md.

Le module doit respecter :

- work_mode normalisé ;
- contract_type normalisé ;
- seniority normalisée ;
- language détectée ;
- salary_min ;
- salary_max ;
- salary_currency ;
- quality_level ;
- status ;
- archived_at.

---

WORK MODE

Valeurs normalisées :

- REMOTE
- HYBRID
- ONSITE
- UNKNOWN

---

CONTRACT TYPE

Valeurs normalisées :

- CDI
- CDD
- FREELANCE
- STAGE
- ALTERNANCE
- PART_TIME
- UNKNOWN

---

SENIORITY

Valeurs normalisées :

- JUNIOR
- MID
- SENIOR
- LEAD
- MANAGER
- DIRECTOR
- VP
- UNKNOWN

---

QUALITY LEVEL

Valeurs normalisées :

- EXCELLENT
- GOOD
- PARTIAL
- POOR

---

STATUS

Valeurs prévues :

- ACTIVE
- ARCHIVED

---

DÉDUPLICATION

Règle MVP :

Une offre est considérée comme doublon potentiel si les champs suivants correspondent :

title

- company
- city

Si doublon :

- ne pas créer de nouvelle JobOffer ;
- mettre à jour la JobOffer existante si les données sont plus complètes ;
- créer ou mettre à jour l'association JobOfferSource.

---

MODÈLE OFFER → SOURCES

JobOffer est l'entité principale.

JobSource est une source possible.

JobOfferSource relie une offre à une source.

Une offre peut donc être associée à plusieurs sources.

Exemple :

JobOffer 1
↓
LinkedIn
↓
France Travail

---

GESTION DES ERREURS

Stratégie MVP :

Logger et continuer.

Une offre invalide ne doit pas bloquer tout l'import.

Les erreurs doivent inclure :

- source concernée ;
- identifiant source si disponible ;
- URL source si disponible ;
- cause de l'erreur ;
- étape du pipeline.

---

OBSERVABILITÉ

Le pipeline doit produire un résumé d'import.

Champs recommandés :

- source_name
- started_at
- completed_at
- offers_fetched
- offers_normalized
- offers_created
- offers_updated
- offers_skipped
- errors_count

---

TESTS ATTENDUS

Tests connecteurs :

- le connecteur retourne des RawOffer ;
- le connecteur gère les erreurs ;
- le connecteur respecte l'interface commune.

Tests normalization :

- contract_type normalisé ;
- work_mode normalisé ;
- seniority normalisée ;
- salary normalisé ;
- quality_level calculé.

Tests repository :

- création JobOffer ;
- mise à jour JobOffer ;
- déduplication ;
- association JobOfferSource.

Tests pipeline :

- Source → Normalization → Database ;
- offre valide persistée ;
- doublon mis à jour ;
- erreur isolée sans blocage global.

---

LIVRABLES TECHNIQUES DE LA PREMIÈRE IMPLÉMENTATION

Pour le premier jalon code, créer uniquement ce qui est nécessaire :

- modèles SQLAlchemy nécessaires ;
- schémas internes nécessaires ;
- MockSourceConnector ou FranceTravailConnector selon accès ;
- NormalizationService minimal ;
- JobOfferRepository minimal ;
- DiscoveryService minimal ;
- tests associés.

Ne pas créer toute l'arborescence cible si elle n'est pas utilisée immédiatement.

---

ORDRE DE DÉVELOPPEMENT RECOMMANDÉ

1. Créer les modèles Job Discovery
2. Créer les schémas internes RawOffer et NormalizedJobOffer
3. Créer le connecteur Mock Source
4. Créer le NormalizationService
5. Créer le JobOfferRepository
6. Créer le DiscoveryService
7. Créer les tests unitaires
8. Créer un endpoint manuel d'import si nécessaire
9. Valider le pipeline complet
10. Commit

---

HORS PÉRIMÈTRE

Cette phase ne traite pas :

- multi-source complet ;
- synchronisation planifiée ;
- interface frontend avancée ;
- dashboard marché ;
- analyse salaire ;
- matching avancé ;
- ranking avancé ;
- recommandations IA.

Ces sujets appartiennent aux phases suivantes.

---

CRITÈRES DE SUCCÈS

La conception technique est validée lorsque :

- l'arborescence cible est définie ;
- les responsabilités sont définies ;
- le pipeline est défini ;
- les modèles attendus sont définis ;
- les connecteurs sont cadrés ;
- la normalisation est cadrée ;
- la déduplication est cadrée ;
- les tests attendus sont définis ;
- l'ordre de développement est défini.

---

PROCHAINE ÉTAPE

Après validation et commit de ce document :

Phase 5.9.4 Implementation Start

Première étape recommandée :

Créer les modèles SQLAlchemy nécessaires au domaine Job Discovery.
