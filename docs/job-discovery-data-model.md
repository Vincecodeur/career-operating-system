# Job Discovery Data Model

## Objectif

Définir le modèle de données du domaine Job Discovery avant l'implémentation SQLAlchemy.

Ce document fixe :

- les entités métier ;
- les colonnes ;
- les contraintes ;
- les relations ;
- les index ;
- la stratégie de déduplication ;
- les règles d'intégrité.

Ce document constitue la source de vérité du modèle de données Job Discovery.

Il sera utilisé pour :

- SQLAlchemy Models ;
- migrations futures ;
- repositories ;
- APIs ;
- tests.

---

CONTEXTE

Le domaine Job Discovery doit permettre :

- la collecte d'offres ;
- le stockage des offres ;
- la déduplication ;
- le suivi des sources ;
- l'analyse future des opportunités.

Les décisions déjà validées imposent :

- JobOffer comme entité principale ;
- plusieurs sources possibles pour une offre ;
- normalisation obligatoire ;
- persistance des données normalisées uniquement ;
- conservation des offres archivées.

---

MODÈLE MÉTIER

Entités principales :

- JobSource
- JobOffer
- JobOfferSource

Relations :

JobOffer
1
↕

N
JobOfferSource

N
↕

1
JobSource

Une offre peut provenir de plusieurs sources.

Une source peut fournir plusieurs offres.

---

ENTITY : JOBSOURCE

Objectif :

Représenter un fournisseur d'offres.

Exemples :

- France Travail
- LinkedIn
- Mock Source

---

TABLE

job_sources

---

COLONNES

id

Type :
Integer

Contraintes :
Primary Key

---

uuid

Type :
UUID

Contraintes :
Unique
Not Null

---

name

Type :
String(100)

Contraintes :
Unique
Not Null

Exemples :

France Travail
LinkedIn

---

source_type

Type :
String(50)

Contraintes :
Not Null

Valeurs prévues :

API
SCRAPING
MANUAL

---

is_active

Type :
Boolean

Default :
True

---

created_at

Type :
DateTime

Not Null

---

updated_at

Type :
DateTime

Not Null

---

INDEXES

idx_job_source_name

Sur :

name

---

ENTITY : JOBOFFER

Objectif :

Représenter une opportunité métier unique.

JobOffer est l'entité principale du domaine.

---

TABLE

job_offers

---

IDENTIFIANTS

id

Type :
Integer

Primary Key

---

uuid

Type :
UUID

Unique

Not Null

---

INFORMATIONS PRINCIPALES

title

Type :
String(500)

Not Null

---

company

Type :
String(500)

Nullable

Décision validée :

Entreprise facultative

---

description_raw

Type :
Text

Not Null

Conserve le texte original.

---

description_normalized

Type :
Text

Nullable

Prévu pour les futures évolutions.

---

url_primary

Type :
Text

Not Null

---

LANGUE

language

Type :
String(20)

Not Null

Valeurs :

FR
EN
UNKNOWN

---

LOCALISATION

city

Type :
String(255)

Nullable

---

region

Type :
String(255)

Nullable

---

country

Type :
String(255)

Not Null

---

WORK MODE

work_mode

Type :
String(50)

Not Null

Valeurs :

REMOTE
HYBRID
ONSITE
UNKNOWN

---

CONTRAT

contract_type

Type :
String(50)

Not Null

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

Type :
String(50)

Not Null

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

Type :
Integer

Nullable

---

salary_max

Type :
Integer

Nullable

---

salary_currency

Type :
String(10)

Nullable

Exemples :

EUR
GBP
USD

---

salary_original_text

Type :
Text

Nullable

Toujours conserver le texte original.

---

COMPÉTENCES

skills_extracted

Type :
JSON

Nullable

---

skills_normalized

Type :
JSON

Nullable

---

QUALITÉ

quality_level

Type :
String(20)

Not Null

Valeurs :

EXCELLENT
GOOD
PARTIAL
POOR

---

STATUT

status

Type :
String(20)

Not Null

Valeurs :

ACTIVE
ARCHIVED

---

ARCHIVAGE

archived_at

Type :
DateTime

Nullable

---

AUDIT

created_at

Type :
DateTime

Not Null

---

updated_at

Type :
DateTime

Not Null

---

INDEXES

idx_job_offer_title

Sur :

title

---

idx_job_offer_company

Sur :

company

---

idx_job_offer_city

Sur :

city

---

idx_job_offer_country

Sur :

country

---

idx_job_offer_status

Sur :

status

---

INDEX DE DÉDUPLICATION

Index métier :

title
company
city

Objectif :

accélérer la recherche de doublons.

---

ENTITY : JOBOFFERSOURCE

Objectif :

Conserver le lien entre une offre et ses différentes sources.

---

TABLE

job_offer_sources

---

IDENTIFIANTS

id

Type :
Integer

Primary Key

---

uuid

Type :
UUID

Unique

Not Null

---

RELATIONS

job_offer_id

Type :
Integer

Foreign Key

job_offers.id

Not Null

---

job_source_id

Type :
Integer

Foreign Key

job_sources.id

Not Null

---

IDENTITÉ SOURCE

source_job_id

Type :
String(255)

Nullable

Identifiant fourni par la source.

---

source_url

Type :
Text

Not Null

---

SUIVI

first_seen_at

Type :
DateTime

Not Null

---

last_seen_at

Type :
DateTime

Not Null

---

created_at

Type :
DateTime

Not Null

---

updated_at

Type :
DateTime

Not Null

---

CONTRAINTE D'UNICITÉ

Unicité :

job_offer_id

- job_source_id
- source_job_id

Objectif :

éviter plusieurs associations identiques.

---

RELATIONS SQLALCHEMY

JobSource

relationships :

job_offer_sources

---

JobOffer

relationships :

job_offer_sources

---

JobOfferSource

relationships :

job_offer

job_source

---

STRATÉGIE DE DÉDUPLICATION

Règle MVP :

Une offre est considérée comme doublon potentiel lorsque :

title

- company
- city

correspondent.

---

SI DOUBLON

Ne pas créer une nouvelle JobOffer.

Mettre à jour :

- les données plus complètes ;
- les associations JobOfferSource.

---

EXEMPLE

France Travail

Integration Architect

Paris

Entreprise X

-

LinkedIn

Integration Architect

Paris

Entreprise X

↓

1 JobOffer

2 JobOfferSource

---

ARCHIVAGE

Les offres expirées ne sont jamais supprimées automatiquement.

Le système applique :

status = ARCHIVED

et renseigne :

archived_at

Les données restent disponibles pour :

- analyses ;
- statistiques ;
- comparaisons ;
- historique.

---

CONTRAINTES IMPORTANTES

JobOffer

Toujours :

- title obligatoire
- description_raw obligatoire
- url_primary obligatoire
- country obligatoire
- language obligatoire

---

JobSource

Toujours :

- name unique
- uuid unique

---

JobOfferSource

Toujours :

- relation source obligatoire
- relation offre obligatoire
- source_url obligatoire

---

PREMIER JALON D'IMPLÉMENTATION

Les premiers modèles SQLAlchemy à créer seront :

- JobSource
- JobOffer
- JobOfferSource

Aucune autre table Job Discovery n'est nécessaire au premier jalon.

---

CRITÈRES DE SUCCÈS

Le modèle de données est validé lorsque :

- les entités sont définies ;
- les colonnes sont définies ;
- les contraintes sont définies ;
- les relations sont définies ;
- les index sont définis ;
- la déduplication est définie ;
- l'archivage est défini.

---

PROCHAINE ÉTAPE

Créer les modèles SQLAlchemy :

- JobSource
- JobOffer
- JobOfferSource

puis écrire les tests de persistance associés.
