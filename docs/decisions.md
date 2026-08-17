# Decisions

## DEC-001

Le projet est personnel.

---

## DEC-002

Le Job Board est un module.

Le produit principal est un Career Operating System.

---

## DEC-003

Stack retenue :

Frontend :
React
TypeScript
Vite

Backend :
FastAPI

Database :
PostgreSQL

---

## DEC-004

Architecture retenue :

Monolithe modulaire.

---

## DEC-005

Commencer par l'import manuel des offres.

L'automatisation viendra plus tard.

---

## DEC-006

Le scoring doit toujours être justifié.

Aucun score opaque.

---

## DEC-007

La documentation est optimisée pour la reprise de contexte Copilot.

---

## DEC-008

Le projet doit rester publiable sur GitHub.

---

## DEC-009

Aucune candidature automatique.

Le système recommande.

L'utilisateur décide.

---

## DEC-010

Le repository suit une architecture Frontend / Backend séparée.

Le backend expose une API REST.

Le frontend consomme exclusivement cette API.

Toute logique métier appartient au backend.

Le frontend est responsable de la présentation et de l'expérience utilisateur.

---

DEC-011

Les dossiers ne sont créés que lorsqu'ils deviennent nécessaires.

Le repository doit rester minimaliste.

Toute création de dossier doit être justifiée par un besoin immédiat.

À chaque création de dossier, Copilot doit indiquer :

- son chemin complet ;
- son rôle ;
- pourquoi il devient nécessaire maintenant.

---

DEC-012

Les dossiers ne sont créés que lorsqu'ils deviennent nécessaires.

Copilot doit toujours indiquer :

- le chemin complet ;
- la raison de création ;
- le lien avec la phase actuelle.

Aucun dossier vide ne doit être créé de manière anticipée.

---

## DEC-013

Le profil candidat est construit selon une approche hybride.

Source initiale :

- CV
- Profil LinkedIn

Puis enrichissement manuel.

Le système doit permettre à l'utilisateur de corriger,
compléter ou modifier les informations extraites.

Le profil candidat devient la source de vérité du système.

Les documents importés servent uniquement à créer ou mettre à jour ce profil.

---

## DEC-014

Le backend est construit dès le départ avec :

- FastAPI
- PostgreSQL
- SQLAlchemy

Aucune phase intermédiaire utilisant du stockage mémoire,
des fichiers JSON ou SQLite n'est prévue.

Le projet doit être aligné dès le départ avec son architecture cible.

L'objectif est de limiter les refactorings futurs tout en conservant une architecture simple.

---

## DEC-015

Le projet utilise une base PostgreSQL dédiée.

Database :

career_os

User :

career_os_user

Le projet ne doit pas utiliser la base postgres par défaut.

Chaque projet possède sa propre base de données.

---

## DEC-016

Le domaine Profile est l'agrégat racine du système.

Tous les futurs domaines métier
(Jobs, Applications, Matching, Career Planning)
s'appuient sur le Profile.

Le développement fonctionnel commence toujours
par les besoins du Profile.

---

## DEC-017

Le système supporte plusieurs profils candidats.

Objectif :

Permettre différentes stratégies de carrière.

Exemples :

- Profil actuel
- Profil Product Manager
- Profil Solution Architect
- Profil Head of Partnerships

---

## DEC-018

Le modèle Profile V1 contient uniquement
les informations de pilotage de carrière.

Les compétences, langues, certifications
et expériences seront gérées dans des tables dédiées.

Le modèle Profile doit rester léger
et représenter la vue synthétique du candidat.

---

## DEC-019

SQLAlchemy create_all() est utilisé uniquement
pour les phases initiales du projet.

Toute évolution future du schéma devra être gérée
via un système de migrations.

Alembic sera introduit lorsque le modèle métier
commencera à évoluer régulièrement.

---

## DEC-020

Le projet utilise un catalogue central de compétences.

Les compétences sont stockées dans une entité dédiée : Skill.

Les profils candidats ne stockent pas directement les compétences sous forme de texte libre.

Les profils référencent les compétences via une relation dédiée.

Objectif :

Permettre un futur moteur de matching fiable entre :

- les compétences du profil candidat ;
- les compétences demandées par les offres d'emploi.

Cette approche évite les doublons et incohérences comme :

- Python
- python
- PYTHON
- Python Programming

Le catalogue central permettra plus tard d'ajouter :

- catégories de compétences ;
- niveaux de maîtrise ;
- synonymes ;
- relations avec les offres d'emploi.

## DEC-021

Les compétences d'un profil sont représentées par une table d'association dédiée : ProfileSkill.

ProfileSkill relie un Profile à une Skill.

Cette relation contient les informations spécifiques à la maîtrise de cette compétence par ce profil :

- years_of_experience ;
- self_assessment_level.

Le catalogue Skill reste générique.

Les informations de maîtrise appartiennent à la relation ProfileSkill, pas à Skill.

---

## DEC-022

Le projet expose une API dédiée pour associer les compétences aux profils.

L'association entre un profil et une compétence est gérée via ProfileSkill.

ProfileSkill permet de stocker les informations spécifiques à la maîtrise d'une compétence par un profil :

- years_of_experience ;
- self_assessment_level.

Le catalogue Skill reste générique.

Les données de maîtrise appartiennent à ProfileSkill.

---

## DEC-023

Les expériences professionnelles sont stockées dans une entité dédiée WorkExperience.

Une expérience appartient à un seul profil.

Les compétences restent stockées séparément dans le catalogue central Skills.

L'objectif est de séparer :

- ce que le candidat sait faire ;
- où et quand le candidat a acquis cette expérience.

WorkExperience permet de reconstruire le parcours professionnel du profil candidat sans mélanger les expériences avec les compétences.

---

## DEC-024

Le projet utilise un catalogue central de langues.

Les langues sont stockées dans une entité dédiée Language.

Les niveaux de maîtrise appartiennent à la relation ProfileLanguage.

L'objectif est de séparer :

- les langues disponibles ;
- le niveau réel du candidat pour chaque langue.

ProfileLanguage relie un Profile à une Language avec un proficiency_level.

Les niveaux recommandés sont :

- A1
- A2
- B1
- B2
- C1
- C2
- Native

---

## DEC-025

Le projet utilise un catalogue central de certifications.

Les certifications sont stockées dans une entité Certification.

Les informations relatives à la possession d'une certification par un candidat sont stockées dans ProfileCertification.

L'objectif est de séparer :

- les certifications disponibles ;
- les certifications réellement obtenues par le candidat.

ProfileCertification permet de gérer :

- la date d'obtention ;
- la date d'expiration ;
- l'identifiant de justificatif éventuel.

---

## DEC-026

Les offres d'emploi sont stockées dans une entité JobOffer.

La Phase 3 est limitée à l'import manuel des offres.

Aucune récupération automatique depuis un site tiers n'est prévue à ce stade.

L'objectif est de construire le premier consommateur des données du profil candidat avant l'introduction du moteur de matching.

Le modèle JobOffer V1 doit rester minimal et contenir uniquement les informations nécessaires à l'analyse d'une offre.

---

## DEC-027

Le projet utilise Pytest comme framework de tests automatisés.

Les tests automatisés sont introduits avant le Matching Engine afin de limiter les régressions.

Chaque nouveau domaine métier important devra progressivement être couvert par des tests automatisés.

---

## DEC-028

Les compétences requises par une offre sont stockées dans une relation dédiée JobOfferSkill.

JobOfferSkill relie une offre d'emploi à une compétence du catalogue central Skill.

Cette relation est utilisée comme fondation du futur moteur de matching.

Les compétences d'une offre ne sont pas stockées sous forme de texte libre afin de permettre une comparaison fiable avec les compétences du candidat.

---

## DEC-029

Le Matching Engine V1 compare uniquement les compétences du profil candidat et les compétences requises par une offre d'emploi.

Le score est calculé à partir du pourcentage de compétences de l'offre présentes dans le profil.

Les langues, certifications, expériences professionnelles et futures capacités IA sont exclues de la V1.

L'objectif est de valider le flux métier complet avant l'introduction de règles plus avancées.

---

## DEC-030

Le Frontend MVP adopte une approche Dashboard First.

L'utilisateur arrive sur un tableau de bord permettant de visualiser :

- les profils candidats ;
- les offres d'emploi ;
- les résultats de matching.

Le Frontend consomme exclusivement les APIs FastAPI existantes.

Aucune logique métier ne doit être implémentée dans React.

Le backend reste la source unique de vérité.

---

## DEC-031

Le Dashboard MVP affiche en priorité :

- les profils ;
- les offres d'emploi.

Le Dashboard ne calcule aucune logique métier.

Toutes les données affichées proviennent exclusivement des APIs backend.

Le Dashboard constitue une couche de visualisation.

---

## DEC-032

La Matching View affiche exclusivement les résultats
calculés par le backend.

Le frontend ne réalise aucun calcul de matching.

Le score, les compétences correspondantes
et les compétences manquantes
sont entièrement produits par l'API backend.

---

## DEC-033

Opportunity Ranking

Le système doit être capable de classer plusieurs offres
pour un profil donné.

L'objectif est de permettre à l'utilisateur d'identifier
rapidement les opportunités les plus pertinentes.

Le classement est calculé exclusivement par le backend.

Le frontend affiche le classement sans logique métier.

Le classement s'appuie sur les résultats du Matching Engine.

Les offres sont triées par score décroissant.

---

## DEC-034

Application Tracker

Le système doit permettre de suivre le cycle de vie
d'une candidature.

Une candidature est liée à :

- un profil candidat
- une offre d'emploi

Une candidature possède un statut unique.

Les statuts initiaux retenus sont :

- Not Applied
- Applied
- Interview
- Offer
- Rejected
- Accepted

Le suivi des candidatures est manuel dans la V1.

Aucune synchronisation avec LinkedIn, Indeed ou d'autres plateformes n'est prévue.

Le système conserve l'historique courant de la candidature afin d'aider à piloter la recherche d'emploi.

## DEC-035

Profile Structured Source Of Truth

Le profil structuré enregistré dans l'application constitue la source de vérité du système.

Les informations peuvent provenir de différentes sources :

- CV ;
- LinkedIn ;
- analyses Copilot ;
- saisie manuelle ;
- autres sources futures.

Ces sources servent uniquement à enrichir le profil.

Toutes les analyses, comparaisons et recommandations utilisent exclusivement le profil structuré enregistré dans le système.

## DEC-036

Opportunity Discovery As Core MVP Capability

Opportunity Discovery devient un composant central du MVP.

Le système doit permettre :

- la collecte automatisée des offres ;
- le stockage des offres ;
- le filtrage des offres ;
- l'analyse des opportunités ;
- le classement des opportunités.

Le suivi des candidatures reste un composant du produit mais ne constitue pas le coeur du MVP.

Le coeur du MVP devient :

Profile
↓
Opportunity Discovery
↓
Opportunity Analysis
↓
Opportunity Ranking
↓
Decision Support
↓
Application Tracker

## DEC-037

API First Job Discovery Strategy

La collecte des offres suit une stratégie API First.

Ordre de priorité :

1. API officielle
2. Flux publics exploitables
3. Scraping lorsqu'aucune API exploitable n'existe

Le scraping doit rester compatible avec les conditions d'utilisation des plateformes concernées.

Les offres collectées conservent toujours :

- leur source ;
- leur URL d'origine ;
- leur date de collecte.

## DEC-038

LinkedIn MVP Target Source

LinkedIn fait partie des sources d'opportunités visées par le MVP.

La méthode d'intégration sera déterminée pendant la Phase Job Discovery.

Aucune hypothèse technique spécifique n'est retenue à ce stade.

Le MVP ne dépend pas exclusivement de LinkedIn.

Le système doit être capable de fonctionner avec plusieurs sources d'opportunités.

## DEC-039

Explainable Opportunity Scoring

Tous les scores d'opportunité doivent être explicables.

Le système doit pouvoir expliquer :

- les critères utilisés ;
- les points forts ;
- les points faibles ;
- les compétences correspondantes ;
- les compétences manquantes ;
- les éventuels malus appliqués.

Aucun score opaque n'est autorisé.

## DEC-040

UX First Frontend Strategy

Le développement frontend suit une stratégie UX First.

Avant toute évolution majeure du frontend :

- les parcours utilisateurs doivent être définis ;
- l'architecture informationnelle doit être définie ;
- les pages doivent être identifiées ;
- les wireframes doivent être validés ;
- la navigation doit être validée.

Le refactoring frontend intervient uniquement après validation de ces éléments.

## DEC-041

Standardized Job Evaluation Rules

Le système applique des règles standardisées afin de permettre une comparaison cohérente des opportunités.

Work Mode supportés :

- Remote
- Hybrid
- Onsite

Ce critère peut être utilisé dans :

- les critères de recherche ;
- le filtrage ;
- le scoring ;
- l'analyse des opportunités.

Gestion des offres sans salaire :

- une offre sans information salariale reste éligible ;
- l'offre n'est pas exclue ;
- un malus peut être appliqué dans le scoring ;
- le malus doit être explicité dans l'analyse.

Gestion des offres expirées :

- les offres expirées sont conservées ;
- elles sont archivées ;
- elles restent disponibles pour :
  - l'historique ;
  - les analyses marché ;
  - les statistiques ;
  - les comparaisons futures.

L'utilisateur peut filtrer l'affichage des offres archivées.

## DEC-042

Frontend Technical Stack

Le frontend cible utilise :

- React Router pour le routing ;
- Zustand pour le state management global ;
- TanStack Query pour le server state ;
- React Hook Form pour les formulaires ;
- Zod pour la validation ;
- shadcn/ui pour les composants UI ;
- Tailwind CSS pour le styling ;
- Lucide Icons pour les icônes.

Zustand est réservé aux états globaux comme l'utilisateur connecté, le thème, les préférences UI ou l'état de la sidebar.

TanStack Query est responsable des données serveur, du cache, des états loading, des retries et de l'invalidation.

Cette combinaison est retenue pour conserver une architecture simple, moderne et maintenable.

## DEC-043

Authentication From MVP

L'authentification est intégrée dès le MVP.

Le système démarre avec :

- un seul compte utilisateur ;
- un compte créé manuellement ;
- email + mot de passe ;
- JWT access token ;
- refresh token ;
- routes protégées ;
- redirection vers Login si l'utilisateur n'est pas authentifié.

Aucune inscription publique n'est prévue dans le MVP.

Cette approche permet de rester simple tout en évitant un refactoring majeur si le produit évolue vers plusieurs utilisateurs.

L'architecture doit rester compatible avec :

- plusieurs utilisateurs ;
- SSO Microsoft ;
- SSO Google ;
- autres fournisseurs d'identité futurs.

## DEC-044

Multilingual Ready Frontend

Le frontend doit être pensé multilingue dès le départ.

Langue MVP :

- English

Langue prévue rapidement après MVP :

- Français

Aucune chaîne d'interface ne doit être hardcodée dans les composants React.

Toutes les chaînes UI doivent être externalisées afin de préparer l'internationalisation sans refactoring majeur.

## DEC-045

Design System Strategy

Le frontend utilise une stratégie design system légère.

Choix validés :

- shadcn/ui ;
- Tailwind CSS ;
- Lucide Icons ;
- thème clair ;
- thème sombre ;
- couleur primaire bleue ;
- variables de thème ;
- accessibilité cible WCAG AA.

Les couleurs ne doivent pas être utilisées directement dans les composants.

Les composants doivent utiliser des variables comme :

- --primary
- --secondary
- --accent
- --background
- --foreground
- --success
- --warning
- --danger

Objectif :

Permettre un rebranding futur sans refactoring majeur du frontend.

## DEC-046

Frontend UX Scope Before Implementation

La Phase 5.7 a été créée pour finaliser la vision UX/UI avant toute évolution majeure du frontend.

Les livrables validés sont :

- information architecture ;
- user flows ;
- page inventory ;
- wireframes ;
- design direction ;
- frontend structure plan.

Le développement frontend de Phase 5.8 doit s'appuyer sur ces documents et ne pas introduire de nouvelle décision structurante non documentée.

---

## DEC-047

Connector Pattern

Chaque source d'offres possède son propre connecteur.

Exemples :

- FranceTravailConnector
- LinkedInConnector

Tous les connecteurs exposent une interface commune.

Objectif :
Permettre l'ajout de nouvelles sources sans modifier la logique métier.

---

## DEC-048

Offer As Primary Discovery Entity

L'entité métier principale du Job Discovery est JobOffer.

Les sources sont des mécanismes de découverte.

Une même offre peut être associée à plusieurs sources.

---

## DEC-049

Job Discovery Pipeline

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

## DEC-050

France Travail First External Source

La première source externe ciblée est France Travail.

Plan B :
LinkedIn.

La stratégie retenue est API First.

## DEC-051

Reference Data Governance

Les référentiels Skills, Languages et Certifications
sont les sources officielles de vocabulaire du système.

Toute donnée issue d'un CV doit être résolue
vers une entrée existante du référentiel lorsque cela est possible.

La création d'une nouvelle entrée de référentiel
est exceptionnelle et nécessite l'absence de correspondance
ainsi qu'une validation explicite de l'utilisateur.

## DEC-052

Repository Resolution Strategy

Les référentiels Skills, Languages et Certifications
utilisent une stratégie de résolution standardisée.

Ordre de recherche :

1. Exact Match
2. Normalized Match
3. Alias Match

Aucune stratégie de fuzzy matching n'est utilisée dans le MVP.

Une donnée issue d'un CV est d'abord comparée
au référentiel existant.

Si une correspondance est trouvée,
le système réutilise l'entrée existante.

Si aucune correspondance n'est trouvée,
une proposition de création peut être présentée
à l'utilisateur.

Toute création d'une nouvelle entrée
de référentiel nécessite une validation explicite.

Objectifs :

- préserver la qualité des référentiels ;
- éviter les doublons ;
- garantir un vocabulaire cohérent ;
- améliorer la qualité du matching ;
- simplifier la gouvernance des données.

## DEC-053

Les skills inconnues ne sont pas créées automatiquement.

skills.category est obligatoire côté modèle de données.
Le système ne peut pas inventer une catégorie fiable.
Le profil structuré reste la source de vérité.
Le catalogue de skills doit rester gouverné.

## DEC-054

Skill Mapping UX

Le composant de sélection utilisera un champ de recherche
avec filtrage côté frontend.

Le MVP peut charger l'ensemble du catalogue puis filtrer en mémoire.

Aucune recherche serveur n'est introduite dans cette phase.

## DEC-055

Reference Data Catalog

Le projet utilise un catalogue de données de référence pour les valeurs stables et réutilisables du système.

Les référentiels cibles incluent :

- Skills ;
- Languages ;
- Certifications ;
- Countries ;
- Work Modes ;
- Contract Types ;
- Preference Options.

Objectif :

- garantir la cohérence des données ;
- éviter les doublons ;
- éviter les variations d'écriture ;
- fiabiliser le matching ;
- simplifier les filtres ;
- améliorer la qualité de l'enrichissement CV.

Les champs fermés ou fortement normalisables doivent utiliser des listes contrôlées plutôt que du texte libre.

Aucune nouvelle valeur de référence ne doit être créée automatiquement sans validation explicite de l'utilisateur lorsque cette valeur impacte le matching, les filtres ou les préférences.

## DEC-056

Reference Data Implementation Before Application Workflow

La phase Reference Data Catalog Design a été validée.

L'implémentation des référentiels est réalisée avant la phase Application Workflow.

Les premiers référentiels implémentés sont :

- Country
- WorkMode
- ContractType

Motivations :

- éviter le refactoring des préférences ;
- éviter le refactoring des filtres ;
- améliorer la qualité du matching ;
- améliorer l'enrichissement CV ;
- préparer les futurs modules d'analyse.

## DEC-057

Preferred Countries Frontend Multi-Select Option A

Le champ Preferred Countries utilise temporairement une stratégie Option A.

Le frontend expose un multi-select dropdown basé sur le Country Catalog.

Le backend conserve le champ existant preferred_countries sous forme de string.

Format temporaire retenu :

FR,BE,NL

Cette approche permet :

- une meilleure expérience utilisateur ;
- la sélection de plusieurs pays ;
- l'utilisation immédiate du Country Catalog ;
- aucune migration base de données ;
- aucune nouvelle API backend ;
- aucune modification du modèle Profile.

Une future Option B pourra remplacer ce stockage par une relation normalisée dédiée :

profile_preferred_countries

Cette évolution est explicitement reportée à une phase ultérieure de normalisation du modèle.

## DEC-058 - Soft Skills MVP

### Contexte

Le Career Operating System distingue désormais deux catégories de compétences :

- Hard Skills
- Soft Skills

Les Hard Skills sont utilisées pour :

- le matching
- le scoring
- l'analyse des écarts (gap analysis)
- l'enrichissement de profil
- le CV Enrichment

Les Soft Skills ont une finalité différente :

- représentation du profil professionnel
- mise en valeur du candidat
- futur enrichissement IA

Elles ne sont pas utilisées dans les mécanismes métier du MVP.

---

### Décision

Les Hard Skills et les Soft Skills sont séparées dans le modèle fonctionnel.

#### Hard Skills

Les Hard Skills restent intégrées au système existant :

- catalogue gouverné
- référentiel centralisé
- gestion des compétences normalisées
- matching
- scoring
- CV Enrichment

Architecture conservée :

Profile
→ ProfileSkill
→ Skill

#### Soft Skills

Les Soft Skills sont gérées séparément.

Elles ne reposent sur aucun catalogue central dans le MVP.

Chaque utilisateur peut ajouter manuellement ses propres Soft Skills.

Exemples :

- Leadership
- Communication
- Negotiation
- Problem Solving
- Stakeholder Management

Les Soft Skills :

- ne sont pas utilisées dans le matching
- ne sont pas utilisées dans le scoring
- ne sont pas extraites automatiquement des CV
- ne sont pas pilotées par l'IA
- ne sont pas gouvernées par un référentiel

---

### Modèle de données MVP

Table :

profile_soft_skills

Structure :

- id
- profile_id
- name
- created_at

Règles :

- une Soft Skill appartient à un profil
- le même libellé peut exister sur plusieurs profils
- une même Soft Skill ne peut exister qu'une seule fois pour un profil donné

Contrainte :

UNIQUE(profile_id, name)

---

### Expérience utilisateur

La section "Skills" du profil devient un conteneur.

Elle est séparée en deux sections distinctes :

Hard Skills

- compétences techniques
- catalogue gouverné
- matching

Soft Skills

- compétences comportementales
- ajout manuel
- texte libre

Exemple :

Skills

## Hard Skills

Python
FastAPI
PostgreSQL
React

## Soft Skills

Leadership
Communication
Negotiation

---

### Hors périmètre MVP

Les éléments suivants sont explicitement reportés :

- extraction IA des Soft Skills
- normalisation des Soft Skills
- catalogue de Soft Skills
- gouvernance des Soft Skills
- scoring basé sur les Soft Skills
- matching basé sur les Soft Skills
- suggestions automatiques de Soft Skills
- analyse comportementale

---

### Conséquences

Le système conserve :

- un catalogue gouverné pour les Hard Skills
- une gestion libre et simple des Soft Skills

Cette approche permet :

- de limiter la complexité du MVP
- d'éviter la maintenance d'un référentiel de Soft Skills
- de préparer de futures fonctionnalités IA sans refactoring majeur
- de séparer clairement compétences techniques et compétences comportementales

# DEC-059 - Automatic Hard Skill / Soft Skill Detection During CV Enrichment

Date: 2026-08-16

Status: Accepted

## Context

The Upload CV workflow extracts skills from uploaded CVs and generates enrichment proposals before importing data into a profile.

The Career Operating System domain model already distinguishes:

- ProfileSkill
- ProfileSoftSkill

Before this decision, all detected skills were treated identically and imported through the ProfileSkill workflow.

This prevented the platform from distinguishing technical competencies from behavioural competencies.

A classification layer is therefore required between CV parsing and profile enrichment.

---

## Decision

The CV parser remains unchanged.

ParsedCVData continues to expose:

skills[]

The parser is responsible for extraction only.

The enrichment layer is responsible for classification.

Two new proposal types are introduced:

- HARD_SKILL
- SOFT_SKILL

Classification occurs during enrichment proposal generation.

---

## Architecture

CV
↓
Parsing
↓
skills[]
↓
Enrichment Classification
↓
HARD_SKILL or SOFT_SKILL
↓
Review & Validation
↓
Profile Import

Parsing remains independent from enrichment business rules.

---

## Classification Strategy

The enrichment engine evaluates every detected skill.

### Rule 1

If the detected skill matches an existing skill in the Skill Catalog:

→ HARD_SKILL

Examples:

- React
- Python
- GraphQL
- Docker

---

### Rule 2

If the detected skill matches a known Soft Skill Dictionary entry:

→ SOFT_SKILL

Examples:

- Leadership
- Communication
- Teamwork
- Adaptability
- Negotiation
- Mentoring
- Problem Solving

---

### Rule 3

If no match is found:

→ HARD_SKILL

The system intentionally defaults to HARD_SKILL.

This avoids incorrectly filling the Soft Skills section with technical competencies that are simply absent from the catalog.

---

## Rationale For Defaulting To HARD_SKILL

Real-world CVs frequently contain:

- Tools
- Frameworks
- Technical Concepts
- Platforms
- Methodologies

that may not yet exist in the Skill Catalog.

Examples:

- Power Platform
- API REST
- GraphQL
- Power BI
- JIRA
- Confluence
- Git
- Excel
- CI/CD
- Kubernetes

These items are much more likely to represent technical competencies than behavioural competencies.

For this reason:

Unknown Skill
→ HARD_SKILL

is preferred over:

Unknown Skill
→ SOFT_SKILL

---

## Skill Catalog Dependency

The Skill Catalog improves classification quality.

However, classification accuracy must not rely exclusively on catalog completeness.

The system must continue operating correctly when:

- skills are missing from the catalog
- new technologies emerge
- customer-specific skills appear in CVs

---

## Import Behaviour

HARD_SKILL proposals are imported into:

ProfileSkill

SOFT_SKILL proposals are imported into:

ProfileSoftSkill

---

## Frontend Behaviour

Step 2 - Analysis

Display:

- Hard Skills Found
- Soft Skills Found

Step 3 - Review & Edit

Display separate sections:

- Hard Skills
- Soft Skills

The classification shown at this stage is the result of the enrichment engine.

---

## Backward Compatibility

Legacy proposal type:

SKILL

remains supported during migration.

For display purposes:

# SKILL

HARD_SKILL

until all historical data has been migrated.

---

## Known Limitations

The enrichment engine may receive compound values from CV parsing.

Examples:

API REST & GraphQL

instead of:

- API REST
- GraphQL

Such compound values may reduce matching accuracy.

Skill normalization and splitting are considered a separate concern from classification.

---

## Future Improvements

Potential future enhancements:

- Skill normalization engine
- Compound skill splitting
- Soft Skill Dictionary enrichment
- AI-based classification
- Confidence scoring
- User classification override

User classification override is defined in DEC-060.

---

## Related Decisions

DEC-058
Hard Skills and Soft Skills are stored separately in the domain model.

DEC-059
Automatic classification of detected skills.

DEC-060
User can override the detected classification during CV enrichment review.

# DEC-060 - Editable Skill Classification During CV Enrichment

Date: 2026-08-16

Status: Accepted

## Context

DEC-059 introduced automatic classification of skills detected during CV enrichment:

- HARD_SKILL = skill recognized as a technical skill
- SOFT_SKILL = skill recognized as a behavioural skill

During functional validation, the Upload CV Wizard successfully separated Hard Skills and Soft Skills.

However, testing on real CVs showed that the automatic classification is not always accurate.

Examples observed:

- API REST & GraphQL classified as Soft Skill
- Power Platform classified as Soft Skill
- Other technical competencies not present in the Skill Catalog incorrectly classified as Soft Skill

The classification engine must therefore be considered as a suggestion, not as a source of truth.

The user must remain able to correct the classification before importing data into the profile.

---

## Decision

The CV enrichment engine remains responsible for proposing an initial classification.

Each detected skill shall have:

- Detected Classification
- Selected Classification

Initially:

Selected Classification = Detected Classification

The user may modify the classification inside Upload CV Wizard Step 3 before applying changes.

The selected classification becomes the source of truth during the import process.

---

## User Experience

For every detected skill:

Example:

API REST & GraphQL

Classification detected:
[ Hard Skill ▼ ]

or

Leadership

Classification detected:
[ Soft Skill ▼ ]

The dropdown allows:

- Hard Skill
- Soft Skill

No additional categories are introduced in MVP.

---

## Import Behaviour

When Apply Changes is executed:

If Selected Classification = Hard Skill

→ Import into ProfileSkill

If Selected Classification = Soft Skill

→ Import into ProfileSoftSkill

The original engine classification is ignored once the user has made a selection.

The user choice always takes precedence.

---

## UI Rules

The dropdown is visible for all detected skills.

For Hard Skills:

- Skill catalog mapping remains available when required.

For Soft Skills:

- Skill catalog mapping is hidden.

If a user changes:

Hard Skill → Soft Skill

Any pending skill mapping becomes unnecessary and is ignored.

If a user changes:

Soft Skill → Hard Skill

The UI must require a valid skill catalog mapping before allowing import.

---

## Rationale

Benefits:

- Preserves automatic classification.
- Keeps the workflow fast.
- Allows correction of classification errors.
- Prevents incorrect profile enrichment.
- Avoids dependence on a perfect classification engine.
- Gives full control to the user.

The enrichment engine provides recommendations.

The user remains the final authority.

---

## Consequences

Frontend:

- UploadCvWizardStep3 must support editable classification.
- Classification dropdown must be introduced.
- Dynamic display of skill mapping section based on current selection.

Backend:

- Accept enrichment flow must support user-selected classification.
- Final import destination is determined by Selected Classification.

Data Governance:

- User validation overrides automatic detection.
- Classification errors can be corrected during enrichment without modifying the source CV.

---

## Future Considerations

Future versions may improve automatic classification using:

- Soft Skill Dictionary
- Skill Taxonomy
- AI Classification
- Confidence Scores

These improvements do not replace user validation.

User validation remains authoritative.

# DEC-061 - Skill Normalization And Compound Skill Splitting

Date: 2026-08-16

Status: Accepted

## Context

Real-world validation of the CV Enrichment workflow revealed that many detected skills are extracted as compound expressions rather than individual competencies.

Examples observed:

- API REST & GraphQL
- Power Platform (PowerApps, Power Automate)
- Excel (Pivot Tables, VBA, PowerQuery)
- JIRA & Confluence
- Software testing (UAT, Sanity, Regression)
- Cross-functional collaboration

The enrichment engine currently treats these expressions as single skills.

This has several negative consequences:

- Lower Skill Catalog matching rate
- Reduced Hard Skill detection accuracy
- Reduced matching quality
- Duplicate or fragmented profile data
- Increased manual corrections during CV review

The platform requires a normalization layer capable of splitting compound skills into atomic skills before enrichment classification.

---

## Decision

A new Skill Normalization layer is introduced between CV Parsing and Enrichment Classification.

The responsibility of this layer is to transform compound skill expressions into normalized atomic skills.

This normalization occurs before:

- Skill Catalog Matching
- Hard Skill / Soft Skill Classification
- Profile Enrichment Proposal Creation

---

## Architecture

Previous flow:

CV
↓
Parsing
↓
skills[]
↓
Classification
↓
Enrichment Proposals

New flow:

CV
↓
Parsing
↓
skills[]
↓
Skill Normalization
↓
normalized_skills[]
↓
Classification
↓
Enrichment Proposals

---

## Goals

The normalization layer must:

- Split compound skills
- Remove formatting artifacts
- Remove wrapping characters
- Remove invalid separators
- Standardize whitespace
- Improve catalog matching
- Improve classification quality

The normalization layer must not:

- Change skill meaning
- Translate skills
- Remove valid skills
- Reclassify skills

Classification remains the responsibility of DEC-059.

---

## Normalization Rules

### Rule 1 - Separator Splitting

The system must split skills using common separators.

Supported separators:

- &
- /
- ,
- ;
- |
- and

Example:

Input:

API REST & GraphQL

Output:

- API REST
- GraphQL

Example:

JIRA & Confluence

Output:

- JIRA
- Confluence

---

### Rule 2 - Parenthesis Expansion

Skills contained in parenthesis must be extracted independently.

Example:

Power Platform (PowerApps, Power Automate)

Output:

- Power Platform
- PowerApps
- Power Automate

Example:

Excel (Pivot Tables, VBA, PowerQuery)

Output:

- Excel
- Pivot Tables
- VBA
- PowerQuery

---

### Rule 3 - Trim Invalid Characters

The system must remove leading and trailing artefacts.

Examples:

Input:

Power Automate)

Output:

Power Automate

Input:

& Confluence

Output:

Confluence

Input:

(React

Output:

React

---

### Rule 4 - Whitespace Normalization

Multiple spaces become a single space.

Examples:

Input:

API REST

Output:

API REST

Input:

Power BI

Output:

Power BI

---

### Rule 5 - Duplicate Removal

Duplicates must be removed after normalization.

Example:

Input:

- React
- React
- React

Output:

- React

---

### Rule 6 - Empty Entry Removal

Empty fragments are discarded.

Example:

Input:

JIRA &

Output:

- JIRA

---

## Normalization Examples

Example 1

Input:

API REST & GraphQL

Output:

- API REST
- GraphQL

---

Example 2

Input:

Power Platform (PowerApps, Power Automate)

Output:

- Power Platform
- PowerApps
- Power Automate

---

Example 3

Input:

Excel (Pivot Tables, VBA, PowerQuery)

Output:

- Excel
- Pivot Tables
- VBA
- PowerQuery

---

Example 4

Input:

JIRA & Confluence

Output:

- JIRA
- Confluence

---

Example 5

Input:

Software Testing (UAT, Sanity, Regression)

Output:

- Software Testing
- UAT
- Sanity
- Regression

---

## Classification Interaction

DEC-061 executes before DEC-059.

Example:

Input:

API REST & GraphQL

Normalization:

- API REST
- GraphQL

Classification:

API REST
→ HARD_SKILL

GraphQL
→ HARD_SKILL

instead of:

API REST & GraphQL
→ single proposal

---

Example:

Input:

JIRA & Confluence

Normalization:

- JIRA
- Confluence

Classification:

JIRA
→ HARD_SKILL

Confluence
→ HARD_SKILL

---

## Catalog Matching Benefits

Without normalization:

API REST & GraphQL

Catalog Match:

❌ Not Found

Result:

Single proposal

---

With normalization:

API REST
GraphQL

Catalog Match:

✅ API REST
✅ GraphQL

Result:

Two independent proposals

---

## User Experience Impact

Step 2 - Analysis

Users see a more accurate count of skills.

---

Step 3 - Review & Edit

Users review:

API REST
GraphQL

instead of:

API REST & GraphQL

This reduces manual corrections and increases catalog mapping success.

---

## Data Quality Benefits

Benefits:

- Better catalog coverage
- Better hard skill recognition
- More precise matching
- Cleaner profiles
- Better analytics
- Better AI recommendations
- Reduced user corrections

---

## Out Of Scope

DEC-061 does not introduce:

- AI-based normalization
- Synonym detection
- Skill taxonomy mapping
- Skill hierarchy management
- Skill translation

Examples:

JavaScript → JS

ReactJS → React

NodeJS → Node.js

are not handled by DEC-061.

Those concerns belong to future normalization improvements.

---

## Related Decisions

DEC-058
Hard Skills and Soft Skills are stored separately.

DEC-059
Automatic Hard Skill / Soft Skill classification.

DEC-060
User can override detected classification.

DEC-061
Normalize and split compound skills before classification.

Execution order:

DEC-061
↓
DEC-059
↓
DEC-060

# DEC-062 - Bulk Proposal Processing

Date: 2026-08-16

Status: Accepted

## Context

The CV Enrichment workflow currently requires users to process enrichment proposals individually.

Since the implementation of:

- DEC-059 - Automatic Hard Skill / Soft Skill Classification

- DEC-060 - User Classification Override

- DEC-061 - Skill Normalization And Compound Skill Splitting

the quality and quantity of generated enrichment proposals have significantly improved.

Real validation performed on production-like CVs generated:

- 34 Hard Skills

- 8 Soft Skills

- 5 Experiences

- 2 Languages

Total:

49 proposals

The current workflow forces users to manually click Accept or Reject for every proposal.

This process becomes inefficient and time-consuming when importing complete CVs.

The platform requires bulk actions to reduce friction and accelerate profile enrichment.

---

## Problem Statement

Current workflow:

```text

Upload CV

    ↓

Analysis

    ↓

Review Suggestions

    ↓

Accept proposal

Accept proposal

Accept proposal

Accept proposal

Accept proposal

...

```

Issues:

- Too many manual clicks

- Poor scalability

- Slower profile creation

- Reduced user productivity

- Increased validation fatigue

---

## Decision

The platform shall support bulk processing of enrichment proposals.

Users can:

- Accept all pending proposals

- Reject all pending proposals

Existing individual validation actions remain available.

Bulk processing is optional.

---

## Goals

The feature must:

- Reduce repetitive manual actions

- Accelerate CV enrichment

- Improve user experience

- Support large CV imports

- Preserve audit history

- Reuse existing business rules

- Minimize implementation complexity

The feature must not:

- Automatically approve proposals

- Skip conflict visibility

- Bypass validation logic

- Remove manual control

- Duplicate acceptance code

---

## Functional Scope

Supported proposal types:

- PROFILE_FIELD

- HARD_SKILL

- SOFT_SKILL

- LANGUAGE

- CERTIFICATION

- EXPERIENCE

Supported proposal status:

- PENDING

Already processed proposals are ignored.

---

## Backend Design

### Endpoint: Accept All

Method:

```http

POST

```

Route:

```text

/enrichment/accept-all

```

Request:

```json
{
  "profile_id": 151,

  "cv_id": 502
}
```

Response:

```json
{
  "accepted": 49
}
```

### Endpoint: Reject All

Method:

```http

POST

```

Route:

```text

/enrichment/reject-all

```

Request:

```json
{
  "profile_id": 151,

  "cv_id": 502
}
```

Response:

```json
{
  "rejected": 49
}
```

---

## Acceptance Processing Flow

```text

Load pending proposals

    ↓

For each proposal

    ↓

Reuse existing accept_proposal()

    ↓

Apply profile update

    ↓

Commit transaction

```

Examples:

```text

HARD_SKILL

→ create ProfileSkill



SOFT_SKILL

→ create ProfileSoftSkill



LANGUAGE

→ create ProfileLanguage



CERTIFICATION

→ create ProfileCertification



EXPERIENCE

→ create WorkExperience



PROFILE_FIELD

→ update Profile field

```

---

## Rejection Processing Flow

```text

Load pending proposals

    ↓

For each proposal

    ↓

Reuse existing reject_proposal()

    ↓

Update status

    ↓

Commit transaction

```

No profile update is applied.

---

## Transaction Rules

Bulk processing must be transactional.

Expected behaviour:

```text

All proposals processed

or

None processed

```

No partial acceptance.

No partial rejection.

---

## Error Handling

If any proposal fails:

```text

Rollback transaction

Return error

No modification applied

```

Response:

```json
{
  "success": false,

  "message": "Bulk processing failed",

  "processed": 0
}
```

---

## Frontend Design

### Step 3 - Review Suggestions

Current UI:

```text

Proposal



[Accept]

[Reject]

```

New UI:

```text

[Accept All]

[Reject All]



---------------------------------



Proposal 1



[Accept]

[Reject]



Proposal 2



[Accept]

[Reject]



Proposal 3



[Accept]

[Reject]



...

```

Individual actions remain available.

---

## Confirmation Dialog

### Accept All

Title:

```text

Accept All Suggestions

```

Message:

```text

You are about to accept all pending enrichment suggestions.



49 suggestions will be applied to the profile.



Do you want to continue?

```

Buttons:

```text

[Cancel]

[Accept All]

```

### Reject All

Title:

```text

Reject All Suggestions

```

Message:

```text

You are about to reject all pending enrichment suggestions.



49 suggestions will be rejected.



Do you want to continue?

```

Buttons:

```text

[Cancel]

[Reject All]

```

---

## Summary Screen

Successful acceptance:

```text

49 Suggestions Accepted



34 Hard Skills

8 Soft Skills

5 Experiences

2 Languages



Profile successfully enriched.

```

Successful rejection:

```text

49 Suggestions Rejected



No profile data has been updated.

```

---

## Conflict Handling

Existing conflict detection remains unchanged.

Example:

```text

Current Value:

Technical Partnerships Manager



Proposed Value:

Technical Partnership & Integration Manager

```

Conflict remains visible.

Bulk acceptance does not bypass conflict detection.

Users still see conflict information before launching bulk processing.

---

## Auditability

Accepted proposals:

```text

Status = ACCEPTED



ValidatedAt populated



History preserved

```

Rejected proposals:

```text

Status = REJECTED



ValidatedAt populated



History preserved

```

No proposal is deleted.

---

## Security

Bulk processing can only affect:

- The selected profile

- The selected CV

Cross-profile processing is forbidden.

Cross-CV processing is forbidden.

---

## Performance

Expected volume:

```text

10 to 100 proposals

```

Observed real-world volume:

```text

49 proposals

```

Current expected workload is small enough to be processed in a single transaction.

No batching optimization is required for MVP.

---

## UX Benefits

Before:

```text

49 clicks required

```

After:

```text

1 click required

```

Benefits:

- Faster onboarding

- Faster CV imports

- Better user satisfaction

- Reduced review fatigue

- Increased adoption

---

## Success Criteria

Scenario:

```text

Upload CV

    ↓

Analysis

    ↓

Review Suggestions

    ↓

Accept All

    ↓

Profile Updated

    ↓

Summary

```

Expected Results:

- All pending proposals accepted

- No duplicate records

- No validation error

- No missing profile records

- Existing individual actions still work

- Proposal history preserved

---

## Out Of Scope

The following features are not included:

- Auto acceptance during upload

- AI confidence scoring

- Automatic validation thresholds

- Scheduled acceptance

- User-specific acceptance rules

---

### Future Evolution

#### Future Decision - Selective Bulk Processing

Potential actions:

- Accept All Hard Skills
- Accept All Soft Skills
- Accept All Languages
- Accept All Certifications
- Accept All Experiences
- Reject All Hard Skills
- Reject All Soft Skills

## Not included in DEC-062.

## Related Decisions

### DEC-058

Hard Skills and Soft Skills stored separately.

### DEC-059

Automatic Hard Skill / Soft Skill Classification.

### DEC-060

User Classification Override.

### DEC-061

Skill Normalization And Compound Skill Splitting.

### DEC-062

Bulk Proposal Processing.

---

## Workflow

```text

CV Upload

    ↓

DEC-061 Skill Normalization

    ↓

DEC-059 Classification

    ↓

DEC-060 User Review & Override

    ↓

DEC-062 Bulk Processing

    ↓

Profile Enriched

```

## DEC-063 - Application Workflow Lifecycle

Date: 2026-08-16

Status: Accepted

### Context

The current Application domain is a simple application registry.

The existing Application model stores:

- profile_id

- job_offer_id

- status

- created_at

- updated_at

The current API supports:

- application creation

- application listing

- application detail retrieval

The system does not yet support:

- controlled lifecycle transitions

- application notes

- application timeline

- source tracking

- application metrics

- structured workflow history

The MVP now requires the Application domain to represent a real application workflow, not just a stored relationship between a profile and a job offer.

---

### Decision

An Application represents a real job application.

An Application must not represent:

- an opportunity under consideration

- a job offer saved for later

- an offer not yet applied to

Those cases belong to the Opportunity domain.

Therefore, the Application lifecycle does not include:

- Draft

- Not Applied

The legacy status `Not Applied` is removed from the target workflow.

---

### Application Lifecycle

Supported statuses:

- Applied

- Phone Screen

- Interview

- Offer

- Accepted

- Rejected

- Withdrawn

---

### Status Definitions

#### Applied

The user has applied to the job.

This is the first valid status of an Application.

#### Phone Screen

The user has entered an initial recruiter screening step.

This may represent:

- recruiter call

- HR screening

- first qualification call

#### Interview

The user is engaged in the interview process.

For the MVP, all interview types are grouped under this status.

The MVP does not distinguish between:

- HR interview

- technical interview

- manager interview

- final interview

#### Offer

The user has received an offer.

The process is not yet completed.

#### Accepted

The user has accepted the offer.

This is a terminal status.

#### Rejected

The company has rejected the application.

This is a terminal status.

#### Withdrawn

The user has voluntarily withdrawn the application.

Examples:

- another offer accepted

- salary mismatch

- location mismatch

- role no longer relevant

- personal decision

This is a terminal status.

---

### Status Transition Rules

Allowed transitions:

```text

Applied

├── Phone Screen

├── Rejected

└── Withdrawn



Phone Screen

├── Interview

├── Rejected

└── Withdrawn



Interview

├── Offer

├── Rejected

└── Withdrawn



Offer

├── Accepted

├── Rejected

└── Withdrawn

```

Terminal statuses:

- Accepted

- Rejected

- Withdrawn

No transition is allowed after a terminal status.

Examples of forbidden transitions:

```text

Accepted -> Interview

Accepted -> Offer

Rejected -> Interview

Withdrawn -> Applied

```

---

### Notes Strategy

An Application contains a single free-form notes field.

Field:

```text

notes

```

Type:

```text

TEXT

```

Purpose:

- recruiter feedback

- interview preparation

- salary details

- follow-up actions

- personal observations

- application context

The MVP does not include note history.

The MVP does not include a separate ApplicationNote table.

---

### Timeline Strategy

The system introduces an ApplicationEvent entity.

ApplicationEvent records structured workflow events.

Supported event types:

- APPLICATION_CREATED

- STATUS_CHANGED

The MVP does not include:

- NOTE_ADDED

- INTERVIEW_SCHEDULED

- EMAIL_SENT

- REMINDER_CREATED

- CALENDAR_EVENT

Notes remain free-form user content.

Timeline remains structured workflow history.

---

### ApplicationEvent Model

ApplicationEvent contains:

- id

- application_id

- event_type

- old_value

- new_value

- event_date

- created_at

`old_value` and `new_value` are used to make status changes explicit.

Example:

```text

STATUS_CHANGED

old_value = Applied

new_value = Interview

```

This allows the timeline to display:

```text

Applied -> Interview

```

instead of a generic status change event.

---

### Source Tracking Strategy

An Application contains a source type.

Field:

```text

source_type

```

Allowed values:

- OPPORTUNITY

- MANUAL

- REFERRAL

- EXTERNAL

If an Application is created from a JobOffer, the JobOffer remains the source of detailed opportunity information.

The Application only stores the high-level source type.

---

### Metrics Compatibility

The lifecycle supports future MVP metrics:

- Total Applications

- Active Applications

- Applied

- Phone Screens

- Interviews

- Offers

- Accepted

- Rejected

- Withdrawn

- Interview Rate

- Offer Rate

- Success Rate

Metrics must be calculated from Application records.

Metrics are not stored as persisted counters.

---

### Multi Profile Compatibility

Applications remain linked to:

```text

profile_id

```

This supports future phase:

```text

7.1.22 Application Profile Attribution

```

The Application keeps the profile used when the application is created.

No major refactoring should be required for the future multi-profile opportunity context.

---

### Out Of Scope

DEC-063 does not include:

- automatic profile recommendation

- CV adaptation per profile

- email synchronization

- calendar synchronization

- interview reminders

- recruiter CRM

- automatic follow-up reminders

- AI application coaching

- advanced source performance analytics

These topics belong to future phases or the post-MVP backlog.

---

### Consequences

The Application domain evolves from a simple registry to a workflow-oriented domain.

The system keeps a clear boundary:

```text

Opportunity

= job offer under consideration



Application

= real application submitted or actively tracked

```

This avoids mixing opportunity exploration with real application tracking.

---

### Related Decisions

DEC-034 introduced the initial Application Tracker concept.

DEC-036 positioned Opportunity Discovery as a core MVP capability.

DEC-063 replaces the legacy Application statuses from DEC-034 with a clearer workflow lifecycle.

DEC-063 prepares the future phase 7.1.22 Multi Profile Opportunity Context.

## DEC-064 - Application Workflow Frontend UX

Date: 2026-08-17

Status: Accepted

### Decision

The Application Workflow MVP frontend uses:

- KPI Cards
- Application Cards
- Application Detail Panel
- Status Workflow
- Notes Section
- Timeline Section
- Source Tracking

### Rejected For MVP

- Kanban
- Drag and Drop
- CRM Table

### Rationale

Career Operating System is a career management platform, not an ATS.

The selected design provides a better balance between usability, simplicity and future Dashboard Evolution.

## DEC-065 - Opportunity To Application Conversion

Date: 2026-08-17
Status: Accepted

### Context

Users can evaluate Job Offers from OpportunitiesPage.

A workflow was required to create a tracked Application directly from an Opportunity.

### Decision

An Opportunity can create an Application.

The user selects:

- Profile
- Opportunity

The system creates:

Application
→ profile_id
→ job_offer_id
→ status = Applied
→ source_type = OPPORTUNITY

### Navigation Rules

The following navigation paths are supported:

Profile
↔ Application

Opportunity
↔ Application

### Rationale

This reflects the natural user workflow:

Opportunity
↓
Apply
↓
Application Tracking

instead of creating applications separately.

### Consequences

The Application domain becomes the operational tracking layer.

The Opportunity domain remains the discovery layer.
