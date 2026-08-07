# Offer Normalization

## Objectif

Définir le format interne normalisé des offres d'emploi collectées par le système Job Discovery.

Ce document fixe :

- le modèle métier principal ;
- les modèles normalisés ;
- les règles de normalisation ;
- les règles de qualité ;
- les règles de déduplication ;
- les règles d'archivage ;
- les règles de conservation des sources ;
- les règles d'extraction des compétences.

Ce document servira de référence pour :

- Job Discovery ;
- Matching ;
- Opportunity Ranking ;
- Opportunity Analysis ;
- Market Intelligence.

---

CONTEXTE

Les offres d'emploi proviendront de plusieurs sources :

- LinkedIn
- France Travail
- futures sources

Chaque source possède :

- ses propres champs ;
- son propre format ;
- sa propre qualité de données.

Le rôle de l'Offer Normalization est de convertir toutes les offres dans un format unique.

Le système ne doit jamais travailler directement avec les formats spécifiques des sources.

Toutes les phases futures utilisent uniquement le modèle normalisé.

---

PRINCIPE ARCHITECTURAL PRINCIPAL

Décision :

Offre → Sources

L'offre est l'entité métier principale.

Les sources sont uniquement des moyens de découverte.

Exemple :

Une même offre peut être trouvée sur :

- LinkedIn
- France Travail

Le système doit reconnaître qu'il s'agit d'une seule opportunité.

---

MODÈLE MÉTIER

Entités principales :

- JobOffer
- JobSource
- JobOfferSource

---

JOBSOURCE

Représente un fournisseur d'offres.

Exemples :

- LinkedIn
- France Travail

Champs recommandés :

id
uuid

name

source_type

api_first

is_active

created_at

updated_at

---

SOURCE TYPE

Valeurs prévues :

API
SCRAPING
MANUAL

---

JOB OFFER

Représente l'offre normalisée utilisée par l'application.

Chaque JobOffer représente une opportunité métier unique.

---

IDENTIFIANTS

Champs :

id

uuid

Décision :

- id SQL auto-incrémenté
- uuid public stable

Les deux identifiants sont conservés.

---

INFORMATIONS PRINCIPALES

title

company

description_raw

description_normalized

url_primary

language

---

RÈGLES

title

Obligatoire

company

Facultatif

description_raw

Obligatoire

Contient le texte original complet.

description_normalized

Facultatif

Prévu pour les futures phases.

url_primary

Obligatoire

Permet de revenir à la source originale.

language

Obligatoire après normalisation.

---

NORMALISATION DE LANGUE

Valeurs MVP :

FR
EN
UNKNOWN

Le système doit tenter de détecter la langue de l'annonce.

---

LOCALISATION

Champs :

city

region

country

---

EXEMPLE

Paris

Île-de-France

France

---

RÈGLES

city

Obligatoire lorsque disponible.

region

Souhaitée.

country

Obligatoire.

---

WORK MODE

Champs :

work_mode

---

VALEURS NORMALISÉES

REMOTE

HYBRID

ONSITE

UNKNOWN

---

EXEMPLES

Télétravail

→ REMOTE

Travail à distance

→ REMOTE

Hybride

→ HYBRID

Télétravail partiel

→ HYBRID

Présentiel

→ ONSITE

---

CONTRAT

Champ :

contract_type

---

VALEURS NORMALISÉES

CDI

CDD

FREELANCE

STAGE

ALTERNANCE

PART_TIME

UNKNOWN

---

SENIORITY

Champ :

seniority

---

VALEURS NORMALISÉES

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

Champs :

salary_min

salary_max

salary_currency

salary_original_text

---

EXEMPLES

"70k"

↓

salary_min = 70000

salary_max = null

salary_currency = EUR

---

"60000 - 80000 €"

↓

salary_min = 60000

salary_max = 80000

salary_currency = EUR

---

RÈGLES

Toujours conserver :

salary_original_text

même après normalisation.

---

DEVISES

Conserver :

devise d'origine

Prévoir :

devise normalisée future

Le MVP ne réalise aucune conversion monétaire.

---

COMPÉTENCES

Champs :

skills_extracted

skills_normalized

---

EXEMPLE

Texte source :

API
REST
PostgreSQL
Shopify

skills_extracted :

- API
- REST
- PostgreSQL
- Shopify

skills_normalized :

- API
- REST
- PostgreSQL
- Shopify

---

RÈGLE

Conserver :

- texte brut
- liste normalisée

Les futures versions du Matching Engine utiliseront principalement la liste normalisée.

---

QUALITÉ

Champ :

quality_level

---

VALEURS

EXCELLENT

GOOD

PARTIAL

POOR

---

RÈGLES RECOMMANDÉES

EXCELLENT

Tous les champs importants présents.

GOOD

Quelques champs secondaires manquants.

PARTIAL

Plusieurs champs manquants.

POOR

Informations minimales.

---

IMPORTANT

Au MVP :

Aucun score numérique.

Uniquement :

EXCELLENT
GOOD
PARTIAL
POOR

---

ARCHIVAGE

Champ :

status

---

VALEURS

ACTIVE

ARCHIVED

---

CHAMP COMPLÉMENTAIRE

archived_at

---

RÈGLE

Une offre expirée :

- est conservée ;
- n'est jamais supprimée automatiquement ;
- reçoit le statut ARCHIVED ;
- enregistre archived_at.

---

SOURCES MULTIPLES

Entité :

JobOfferSource

---

OBJECTIF

Permettre à une offre d'être associée à plusieurs sources.

Exemple :

JobOffer

↓

LinkedIn

↓

France Travail

---

CHAMPS RECOMMANDÉS

job_offer_id

job_source_id

source_job_id

source_url

first_seen_at

last_seen_at

---

DÉDUPLICATION

OBJECTIF

Éviter plusieurs JobOffer pour une même opportunité.

---

RÈGLE MVP

Une offre est potentiellement identique si :

title

- company
- city

sont identiques.

---

DÉCISION

Si doublon détecté :

Conserver l'offre la plus complète.

Conserver toutes les sources associées.

---
