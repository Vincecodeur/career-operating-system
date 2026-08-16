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
