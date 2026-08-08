# Job Discovery Model Migration

## Objectif

Définir la stratégie de migration entre le modèle JobOffer actuellement implémenté et le modèle cible du domaine Job Discovery.

Ce document évite :

- la création de modèles dupliqués ;
- les refactorings inutiles ;
- les incohérences entre le code et la documentation.

La stratégie retenue est une évolution progressive du modèle existant.

Aucun remplacement brutal du modèle JobOffer n'est autorisé.

---

CONTEXTE

Le projet possède déjà une implémentation fonctionnelle du domaine Jobs.

Les fichiers existants sont :

backend/app/jobs/models.py

backend/app/jobs/schemas.py

backend/app/jobs/router.py

Le modèle JobOffer existe déjà et est utilisé par les routes API.

Le modèle cible défini dans :

- job-sources.md
- search-criteria.md
- offer-normalization.md
- job-discovery-data-model.md

est plus riche que l'implémentation actuelle.

L'objectif est donc :

faire évoluer le modèle existant

et non

créer un nouveau modèle concurrent.

---

ÉTAT ACTUEL

Le modèle JobOffer contient actuellement :

- id
- title
- company_name
- location
- source
- source_url
- description
- created_at

Cette structure est suffisante pour l'import manuel.

Elle est insuffisante pour :

- le Job Discovery multi-sources ;
- la déduplication ;
- la normalisation ;
- l'analyse d'opportunités ;
- le futur ranking.

---

PRINCIPE DE MIGRATION

Décision :

Conserver JobOffer.

Le modèle JobOffer reste l'entité principale.

La migration consiste à :

- enrichir JobOffer ;
- créer JobSource ;
- créer JobOfferSource.

Aucune table JobOfferV2 ne doit être créée.

Aucune duplication du concept JobOffer n'est autorisée.

---

ARCHITECTURE CIBLE

Avant

JobOffer

Après

JobSource
↓
JobOfferSource
↓
JobOffer

JobOffer reste l'agrégat principal.

---

PHASE 1

CONSERVATION DU MODÈLE EXISTANT

Les champs suivants sont conservés :

id

title

company_name

source_url

created_at

---

CHAMPS À FAIRE ÉVOLUER

location

doit être progressivement remplacé par :

- city
- region
- country

La compatibilité doit être maintenue pendant la transition.

---

description

devient :

description_raw

Le contenu actuel est conservé.

---

source

doit disparaître à terme.

Cette information sera portée par :

JobSource

- JobOfferSource

La suppression n'est pas immédiate.

---

PHASE 2

NOUVEAUX CHAMPS JOBOFFER

Les champs suivants doivent être ajoutés progressivement.

---

IDENTIFIANT PUBLIC

uuid

Type :

UUID

Unique

Not Null

---

LANGUE

language

Valeurs :

FR
EN
UNKNOWN

---

LOCALISATION NORMALISÉE

city

region

country

---

WORK MODE

work_mode

Valeurs :

REMOTE
HYBRID
ONSITE
UNKNOWN

---

CONTRAT

contract_type

Valeurs :

CDI
CDD
FREELANCE
STAGE
ALTERNANCE
PART_TIME
UNKNOWN

---

SENIORITY

seniority

Valeurs :

JUNIOR
MID
SENIOR
LEAD
MANAGER
DIRECTOR
VP
UNKNOWN

---

SALAIRE

salary_min

salary_max

salary_currency

salary_original_text

---

SKILLS

skills_extracted

skills_normalized

---

QUALITÉ

quality_level

Valeurs :

EXCELLENT
GOOD
PARTIAL
POOR

---

STATUT

status

Valeurs :

ACTIVE
ARCHIVED

---

ARCHIVAGE

archived_at

---

AUDIT

updated_at

---

PHASE 3

CRÉATION DE JOBSOURCE

OBJECTIF

Représenter les fournisseurs d'offres.

Exemples :

France Travail

LinkedIn

Mock Source

---

TABLE

job_sources

---

RESPONSABILITÉS

- identifier la source ;
- stocker le type ;
- permettre le multi-source.

---

PHASE 4

CRÉATION DE JOBOFFERSOURCE

OBJECTIF

Associer plusieurs sources à une même offre.

---

TABLE

job_offer_sources

---

RESPONSABILITÉS

- conserver les identifiants source ;
- conserver les URLs source ;
- tracer l'origine des offres ;
- supporter le multi-source.

---

STRATÉGIE DE DÉDUPLICATION

RÈGLE MVP

Une offre est considérée comme doublon potentiel lorsque :

title

- company_name
- city

correspondent.

---

ACTION

Si doublon :

mettre à jour l'offre existante.

Ne pas créer une nouvelle JobOffer.

Créer ou mettre à jour JobOfferSource.

---

COMPATIBILITÉ API

PHASE 1

Les APIs existantes continuent de fonctionner.

Aucune rupture de contrat.

---

PHASE 2

Les nouveaux champs deviennent disponibles.

Les anciens champs restent présents lorsque nécessaire.

---

PHASE 3

Migration progressive vers les schémas enrichis.

---

MIGRATION DES SCHÉMAS PYDANTIC

Le schéma :

JobOfferCreate

sera enrichi progressivement.

---

Le schéma :

JobOfferResponse

sera enrichi progressivement.

---

Aucune suppression brutale de champ ne doit être effectuée.

---

MIGRATION DU ROUTER

Le router existant reste conservé.

Les évolutions doivent être incrémentales.

Objectif :

éviter de casser le frontend existant.

---

ORDRE DE DÉVELOPPEMENT

1. Ajouter les colonnes JobOffer
2. Ajouter JobSource
3. Ajouter JobOfferSource
4. Mettre à jour les schémas
5. Mettre à jour les routes
6. Introduire les repositories
7. Introduire les services Discovery
8. Introduire les connecteurs
9. Activer l'import automatisé

---

RISQUES IDENTIFIÉS

Création d'un deuxième JobOffer

Impact :

Duplication métier.

Décision :

Interdite.

---

Suppression du champ source trop tôt

Impact :

Rupture API.

Décision :

Migration progressive.

---

Modification du champ location sans transition

Impact :

Données incompatibles.

Décision :

Conserver location temporairement.

---

ÉTAT CIBLE FINAL

JobOffer

contient :

- données normalisées ;
- informations métier ;
- statut ;
- qualité ;
- compétences.

---

JobSource

contient :

- informations source.

---

JobOfferSource

contient :

- origine ;
- identifiants externes ;
- URLs ;
- historique de découverte.

---

CRITÈRES DE SUCCÈS

La migration est considérée comme validée lorsque :

- JobOffer est conservé ;
- JobOffer est enrichi ;
- JobSource est créé ;
- JobOfferSource est créé ;
- les APIs continuent de fonctionner ;
- la déduplication est supportée ;
- le multi-source est supporté ;
- aucune duplication de modèle métier n'existe.

---

PROCHAINE ÉTAPE

Implémentation SQLAlchemy :

- évolution de JobOffer ;
- création de JobSource ;
- création de JobOfferSource ;
- tests de persistance.
