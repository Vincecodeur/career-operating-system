# Page Inventory

## Phase

5.7.4 Page Inventory

## Objectif

Définir précisément toutes les pages du Career Operating System avant la création des wireframes et avant toute évolution majeure du frontend.

Chaque page doit définir :

- son rôle ;
- ses données ;
- ses composants ;
- ses actions ;
- ses dépendances backend ;
- son statut MVP ou futur.

Le frontend reste une couche de navigation et de visualisation.

Le backend reste responsable :

- du matching ;
- du scoring ;
- du ranking ;
- de l'analyse des opportunités ;
- des règles métier.

---

# Vue d'ensemble des pages

## Pages MVP

PI-00 Login
PI-00.1 Forgot Password
PI-00.2 My Account
PI-01 Dashboard
PI-02 Profile List
PI-03 Profile Details
PI-04 Search Criteria List
PI-05 Search Criteria Details
PI-06 Opportunities List
PI-07 Opportunity Details
PI-08 Applications List
PI-09 Application Details
PI-10 Settings

## Pages futures

PI-11 Job Sources
PI-12 Market Intelligence
PI-13 Career Roadmap
PI-14 Interview Preparation
PI-15 Application Assistant

---

## PI-00 Login

### Statut

MVP

### Route

/login

### Objectif

Permettre à l'utilisateur de s'authentifier afin d'accéder aux fonctionnalités protégées du Career Operating System.

### Données affichées

- Email
- Password
- Message d'erreur éventuel

### Composants

- LoginForm
- EmailInput
- PasswordInput
- LoginButton

### Actions utilisateur

- Saisir son email
- Saisir son mot de passe
- Se connecter
- Ouvrir Forgot Password

### APIs nécessaires

- POST /auth/login

### Dépendances

- Authentication

## PI-00.1 Forgot Password

### Statut

MVP Minimal

### Route

/forgot-password

### Objectif

Permettre à l'utilisateur de demander une réinitialisation de mot de passe.

### Données affichées

- Email

### Composants

- ForgotPasswordForm
- EmailInput
- SubmitButton

### Actions utilisateur

- Saisir son email
- Envoyer la demande
- Revenir vers Login

### APIs futures nécessaires

- POST /auth/forgot-password

### Dépendances

- Authentication

## PI-00.2 My Account

#### Statut

MVP

#### Route

/account

#### Objectif

Permettre à l'utilisateur de consulter et modifier les informations de son compte.

#### Données affichées

- Email
- Langue
- Préférences utilisateur
- Thème sélectionné

#### Composants

- AccountForm
- PreferencesSection
- ThemeSelector
- LanguageSelector

#### Actions utilisateur

- Modifier ses préférences
- Modifier sa langue
- Changer de thème
- Changer son mot de passe
- Se déconnecter

#### APIs nécessaires

- GET /me
- PUT /me

#### Dépendances

- Authentication
- User Preferences

# PI-01 Dashboard

## Statut

MVP

## Route

/

## Objectif

Donner une vue synthétique de la situation carrière.

## Données affichées

- Nombre total d'opportunités
- Nombre d'opportunités pertinentes
- Nombre d'opportunités à analyser
- Nombre de candidatures
- Top opportunités
- Dernières opportunités collectées
- Actions recommandées
- Alertes éventuelles

## Composants

- CareerSummaryCard
- OpportunitySummaryCard
- ApplicationSummaryCard
- RecentOpportunitiesWidget
- TopOpportunitiesWidget
- RecommendedActionsWidget

## Actions utilisateur

- Ouvrir un profil
- Ouvrir Opportunities
- Ouvrir Applications
- Ouvrir Search Criteria
- Ouvrir Settings

## APIs nécessaires

- GET /profiles
- GET /job-offers
- GET /applications
- GET /ranked-job-offers

## Dépendances

- Profiles
- Opportunities
- Applications

---

# PI-02 Profile List

## Statut

MVP

## Route

/profile

## Objectif

Afficher la liste des profils candidats.

## Données affichées

- Nom du profil
- Titre professionnel
- Pays cible
- Date de mise à jour

## Composants

- ProfileTable
- ProfileCard
- CreateProfileButton

## Actions utilisateur

- Créer un profil
- Sélectionner un profil
- Modifier un profil
- Supprimer un profil

## APIs nécessaires

- GET /profiles
- POST /profiles
- DELETE /profiles/{id}

## Dépendances

- Profile

---

# PI-03 Profile Details

## Statut

MVP

## Route

/profile/:id

## Objectif

Afficher et modifier un profil candidat.

## Données affichées

- Informations générales
- Compétences
- Expériences
- Langues
- Certifications
- Notes d'analyse
- Documents

## Composants

- ProfileHeader
- SkillsSection
- ExperienceSection
- LanguagesSection
- CertificationsSection
- NotesSection
- DocumentsSection

## Actions utilisateur

- Modifier le profil
- Ajouter une compétence
- Ajouter une expérience
- Ajouter une certification
- Ajouter une langue
- Ajouter un document
- Ajouter une analyse externe

## APIs nécessaires

- GET /profiles/{id}
- PUT /profiles/{id}
- CRUD Skills
- CRUD Languages
- CRUD Certifications
- CRUD Experience

## Dépendances

- Profile
- Skill
- WorkExperience
- Language
- Certification

---

# PI-04 Search Criteria List

## Statut

MVP

## Route

/search-criteria

## Objectif

Afficher les critères de recherche configurés.

## Données affichées

- Nom du critère
- Profil associé
- Statut actif

## Composants

- SearchCriteriaTable
- SearchCriteriaCard
- CreateSearchCriteriaButton

## Actions utilisateur

- Créer un critère
- Modifier un critère
- Activer ou désactiver un critère
- Supprimer un critère

## APIs futures nécessaires

- GET /search-criteria
- POST /search-criteria
- PUT /search-criteria

## Dépendances

- SearchCriteria

---

# PI-05 Search Criteria Details

## Statut

MVP

## Route

/search-criteria/:id

## Objectif

Configurer les critères utilisés pour la collecte et le scoring.

## Données affichées

- Titres recherchés
- Pays
- Régions
- Work Mode
- Salaire minimum
- Types de contrat
- Langues
- Sources activées
- Mots-clés inclus
- Mots-clés exclus

## Composants

- TargetTitlesForm
- LocationForm
- WorkModeForm
- SalaryForm
- ContractTypeForm
- LanguageForm
- SourceSelector
- KeywordsForm

## Actions utilisateur

- Modifier les critères
- Sauvegarder
- Réinitialiser

## APIs futures nécessaires

- GET /search-criteria/{id}
- PUT /search-criteria/{id}

## Dépendances

- SearchCriteria
- JobSource

---

# PI-06 Opportunities List

## Statut

MVP

## Route

/opportunities

## Objectif

Afficher les opportunités collectées et classées.

## Données affichées

- Titre
- Entreprise
- Localisation
- Source
- Score
- Niveau de pertinence
- Salaire
- Work Mode
- Statut

## Composants

- OpportunitiesTable
- OpportunitiesCards
- OpportunitiesFilters
- RankingWidget

## Actions utilisateur

- Filtrer
- Trier
- Ouvrir Opportunity Details
- Archiver
- Marquer comme intéressante
- Marquer comme non intéressante

## APIs nécessaires

- GET /job-offers
- GET /ranked-job-offers

## Dépendances

- JobOffer
- OpportunityRanking

---

# PI-07 Opportunity Details

## Statut

MVP

## Route

/opportunities/:id

## Objectif

Analyser une opportunité.

## Données affichées

- Offre complète
- Score
- Pertinence
- Points forts
- Points faibles
- Compétences correspondantes
- Compétences manquantes
- Salaire
- Localisation
- Source
- Date de publication

## Composants

- OpportunityHeader
- OpportunityDescription
- ScoreCard
- StrengthsPanel
- WeaknessesPanel
- SkillsMatchPanel
- MissingSkillsPanel
- SourcePanel

## Actions utilisateur

- Open Job Offer
- Convert To Application
- Archive
- Mark Interesting
- Mark Not Interesting

## APIs nécessaires

- GET /job-offers/{id}
- GET /matching/{profile_id}/{job_offer_id}

## Dépendances

- Matching
- OpportunityAnalysis

---

# PI-08 Applications List

## Statut

MVP

## Route

/applications

## Objectif

Afficher les candidatures suivies.

## Données affichées

- Offre
- Entreprise
- Profil associé
- Statut
- Date de création

## Composants

- ApplicationsTable
- ApplicationStatusBadge

## Actions utilisateur

- Ouvrir une candidature
- Modifier le statut

## APIs nécessaires

- GET /applications

## Dépendances

- Application

---

# PI-09 Application Details

## Statut

MVP

## Route

/applications/:id

## Objectif

Afficher une candidature détaillée.

## Données affichées

- Offre associée
- Profil associé
- Statut
- Historique
- Score initial
- Source originale

## Composants

- ApplicationHeader
- StatusPanel
- OpportunitySnapshot

## Actions utilisateur

- Modifier le statut
- Ouvrir l'opportunité
- Ouvrir le lien source

## APIs nécessaires

- GET /applications/{id}
- PUT /applications/{id}

## Dépendances

- Application
- JobOffer

---

# PI-10 Settings

## Statut

MVP Minimal

## Route

/settings

## Objectif

Centraliser les préférences utilisateur.

## Données affichées

- Préférences générales
- Préférences IA
- Préférences de synchronisation
- Informations système

## Composants

- GeneralSettingsForm
- AISettingsForm
- SyncSettingsForm

## Actions utilisateur

- Modifier les paramètres
- Sauvegarder

## APIs futures nécessaires

- GET /settings
- PUT /settings

---

# PI-11 Job Sources

## Statut

Futur

## Route

/job-sources

## Objectif

Gérer les sources d'opportunités.

## Données affichées

- Source
- Type
- Statut
- Dernière synchronisation

## Actions utilisateur

- Activer
- Désactiver
- Configurer

---

# PI-12 Market Intelligence

## Statut

Futur

## Route

/market

## Objectif

Afficher les tendances marché issues des opportunités collectées.

## Données affichées

- Compétences demandées
- Salaires
- Pays
- Secteurs
- Tendances

---

# PI-13 Career Roadmap

## Statut

Futur

## Route

/career-roadmap

## Objectif

Construire une stratégie de carrière.

## Données affichées

- Objectifs
- Écarts de compétences
- Recommandations

---

# PI-14 Interview Preparation

## Statut

Futur

## Route

/interview-preparation

## Objectif

Préparer les entretiens à partir d'une opportunité ciblée.

---

# PI-15 Application Assistant

## Statut

Futur

## Route

/application-assistant

## Objectif

Aider à préparer les candidatures.

---

# Critères de validation

La phase 5.7.4 est terminée lorsque :

- toutes les pages MVP sont documentées ;
- toutes les pages futures sont identifiées ;
- les routes sont identifiées ;
- les composants sont identifiés ;
- les actions utilisateur sont définies ;
- les dépendances backend sont identifiées ;
- le document est suffisamment détaillé pour produire les wireframes.

---

# Prochaine étape

Phase 5.7.5 - Wireframes

Objectif :

Définir les wireframes basse fidélité de l'ensemble des pages MVP avant la phase Design Direction.
