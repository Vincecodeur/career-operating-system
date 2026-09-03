# Architecture

## Objectif

Construire une plateforme personnelle modulaire permettant :

- la gestion de plusieurs profils candidats ;
- la centralisation d'une source de vérité carrière ;
- la collecte automatisée d'offres d'emploi ;
- l'analyse des opportunités ;
- le matching entre profils et offres ;
- le classement des opportunités ;
- le suivi des candidatures ;
- l'analyse future du marché ;
- la planification de carrière.

Le système est conçu comme une plateforme personnelle d'intelligence carrière et d'aide à la décision.

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

### Source de vérité

Le profil structuré enregistré dans l'application constitue la source de vérité du système.

Les données peuvent provenir de plusieurs sources :

- CV ;
- LinkedIn ;
- analyses Copilot ;
- saisie manuelle ;
- autres sources futures.

Ces sources servent uniquement à enrichir le profil.

Toutes les analyses, comparaisons et décisions s'appuient sur le profil structuré enregistré dans la base de données.

---

## Domaines métier

### Profile

Gestion des profils candidats.

Sous-domaines :

- Profile
- Skill
- ProfileSkill
- WorkExperience
- Language
- ProfileLanguage
- Certification
- ProfileCertification

Le système supporte plusieurs profils candidats.

Note d'architecture :
Le système ne implémente actuellement aucune isolation multi-tenant. Tous les comptes utilisateurs (User) partagent l'intégralité des données Profile, Application, CV et autres entités métier. Cette limitation est documentée et assumée pour le MVP (voir ARCH-001 dans le backlog post-MVP).

Additional Profile Context

Purpose:

- Professional Summary
- Career Motivations
- Preferred Environment
- Non-Negotiables
- Additional Context

Implementation Status:
Completed

Stored directly on Profile.

Fields:

- professional_summary
- career_motivations
- preferred_environment
- non_negotiables
- additional_context

No impact on matching.
No impact on scoring.
Prepared for future AI Context phases.

Database status:

- five nullable TEXT columns added to the profiles table
- PostgreSQL persistence validated
- no separate domain table introduced

### Search Criteria

Gestion des critères de recherche d'opportunités.

Exemples :

- pays ;
- work mode ;
- salaire minimum ;
- langues ;
- types de contrat ;
- titres recherchés ;
- mots-clés inclus ;
- mots-clés exclus.

### Job Discovery

Collecte d'offres d'emploi depuis des sources externes.

Principes :

- API first ;
- scraping uniquement lorsqu'aucune API exploitable n'existe ;
- collecte quotidienne ;
- normalisation des données.

### Job Sources

Gestion des sources d'offres.

Types prévus :

- API ;
- SCRAPING ;
- MANUAL_IMPORT.

### Settings

Gestion des paramètres applicatifs.

Responsabilités :

- Job Discovery Settings
- Search Criteria Settings
- Matching Weights
- Source Configuration
- Application Workflow Settings
- Opportunity Discovery Preferences
- Saved Searches
- AI Features Settings
- AI Consent Settings

Search Criteria Settings currently support:

- Target Job Titles
- Preferred Countries
- Work Modes
- Included Keywords
- Excluded Keywords

Opportunity Discovery Preferences currently support:

- Opportunity Age Window
- Minimum Matching Score
- Default Opportunity Sort

No global default profile is stored.

Countries and Work Modes are controlled through the Reference Data Catalog.

Discovery Connectors are controlled through a dedicated connector catalog.

Current supported connectors:

- France Travail
- Greenhouse
- LinkedIn

Connector selection uses a controlled multi-select UI.

Implémenté :

- ApplicationSetting
- SettingsService
- GET /settings/job-discovery
- PUT /settings/job-discovery
- GET /settings/search-criteria
- PUT /settings/search-criteria
- GET /settings/ai
- PUT /settings/ai

AI Settings utilisent les clés suivantes dans ApplicationSetting :

- ai_features_enabled ;
- ai_consent_accepted.

Valeurs par défaut :

- ai_features_enabled = false ;
- ai_consent_accepted = false.

États cohérents autorisés :

- false / false ;
- true / true.

Les fonctionnalités IA ne peuvent pas être activées sans consentement accepté.

La désactivation des fonctionnalités IA révoque également le consentement dans le contrat MVP.

Les paramètres métier sont stockés en PostgreSQL.

Les secrets restent stockés dans les variables d'environnement.

Exemples :

- FRANCE_TRAVAIL_CLIENT_ID
- FRANCE_TRAVAIL_CLIENT_SECRET
- LINKEDIN_CLIENT_SECRET
- GREENHOUSE_BOARD_TOKEN

### Opportunity Analysis

Analyse détaillée des opportunités.

Le système doit être capable :

- d'évaluer une opportunité ;
- d'identifier les points forts ;
- d'identifier les points faibles ;
- d'expliquer les scores ;
- de détecter les compétences manquantes.

### Matching

Comparaison profil ↔ offre.

Version actuelle :

- matching basé sur les compétences.

Opportunity Profile Comparison

The Matching domain exposes a multi-profile opportunity comparison capability.

For a given opportunity:

- the score is calculated against every active profile;
- the best matching profile is identified;
- opportunity details can display all profile scores simultaneously;
- opportunity cards use the currently selected profile context.

The comparison logic remains entirely in the backend.

Version future :

- compétences ;
- langues ;
- séniorité ;
- localisation ;
- work mode ;
- salaire ;
- autres critères configurables.

### Opportunity Ranking

Classement des opportunités.

Le classement est calculé exclusivement par le backend.

Le frontend affiche les résultats.

### Applications

Suivi manuel des candidatures.

Le système ne réalise aucune candidature automatique.

Le domaine Applications implémente désormais un workflow de candidature.

Une Application est liée à :

- un profil ;
- une offre d’emploi.

Une Application contient :

- status ;
- notes ;
- source_type.

Le système conserve également un historique structuré via ApplicationEvent.

ApplicationEvent permet notamment de tracer :

- APPLICATION_CREATED ;
- STATUS_CHANGED ;
- PROFILE_CHANGED.

L’objectif est de fournir un suivi complet du cycle de vie d’une candidature.

Une Application peut être créée :

- directement depuis une Opportunity ;
- manuellement par l'utilisateur.

Lorsqu'une Application est créée depuis une Opportunity :

- le Best Matching Profile est recommandé à l'utilisateur ;
- l'utilisateur peut sélectionner un autre profil actif avant validation ;
- le profil confirmé est définitivement associé à l'Application.

Après la création :

- l'utilisateur peut explicitement réattribuer l'Application à un autre profil actif ;
- la réattribution ne modifie ni l'Opportunity, ni le statut, ni les notes, ni la source ;
- le résultat de matching est recalculé pour le nouveau profil ;
- toute réattribution effective crée un ApplicationEvent PROFILE_CHANGED ;
- aucun événement PROFILE_CHANGED n'est créé lorsque profile_id reste inchangé.

Règles de validation de l'attribution :

- le backend vérifie que le Profile sélectionné existe ;
- le backend vérifie que le Profile sélectionné est actif ;
- le backend vérifie que le JobOffer référencé existe lors de la création ;
- les clés étrangères de la base de données constituent le dernier niveau de protection de l'intégrité.

### Market Intelligence

Analyse future du marché.

### Career Planning

Planification de carrière.

### AI

Le domaine AI fournit des services d’assistance séparés des moteurs déterministes du système.

L’IA enrichit l’analyse mais ne constitue jamais la source de vérité.

Le système reste utilisable lorsque les fonctionnalités IA sont désactivées.

Sous-domaines actuellement présents :

- AI Explanation ;
- AI Context Preview ;
- AI Readiness ;
- AI Consent.

AI Explanation reste responsable de l’explication des résultats déterministes existants.

AI Context Preview est responsable de présenter les catégories de données validées qui pourront être utilisées par de futures fonctionnalités IA.

AI Readiness est calculé exclusivement par le backend.

Un profil est AI Ready uniquement lorsque les éléments suivants sont présents :

- Current Title ;
- au moins une Hard Skill ;
- au moins une Work Experience ;
- au moins une Language ;
- Professional Summary ;
- Career Motivations ;
- Preferred Environment ;
- Non-Negotiables ;
- Additional Context.

Les Soft Skills, Certifications et CV sont optionnels pour AI Readiness.

L’autorisation finale est calculée par le backend :

ai_call_allowed =
is_ai_ready
AND
ai_features_enabled
AND
ai_consent_accepted

Le backend expose :

- GET /profiles/{profile_id}/ai-context-preview ;
- GET /settings/ai ;
- PUT /settings/ai.

L’endpoint AI Context Preview :

- ne contacte aucun fournisseur IA ;
- ne construit aucun prompt ;
- ne retourne pas le contenu brut du profil ;
- ne lit pas le contenu brut d’un CV ;
- ne lit pas les propositions d’enrichissement non validées ;
- ne lit pas les candidatures.

Catégories explicitement exclues :

- RAW_CV ;
- UNVALIDATED_ENRICHMENT ;
- APPLICATION_HISTORY ;
- TECHNICAL_SECRETS.

Architecture backend :

app/ai/
├── schemas.py
├── services.py
├── context_schemas.py
├── context_service.py
└── router.py

Séparation des responsabilités :

- AIExplanationService gère les explications IA ;
- AIContextService gère la readiness, le preview et l’autorisation ;
- SettingsService gère la persistance de l’activation et du consentement.

Le frontend AI Context Preview and Consent est implémenté.

Frontend elements:

- AIConsentDialog
- AIContextReadinessCard
- Settings integration
- Profile Detail integration

Validation:

- AI enable workflow validated
- AI disable workflow validated
- AI context preview display validated

---

### Entités principales

Profile
Représente un profil candidat.

Skill
Catalogue central de compétences.

ProfileSkill
Relation entre un profil et une compétence.

WorkExperience
Expérience professionnelle.

Language
Catalogue central de langues.

ProfileLanguage
Relation entre un profil et une langue.

Certification
Catalogue central de certifications.

ProfileCertification
Relation entre un profil et une certification.

SearchCriteria
Critères de recherche associés à un profil.

JobSource
Source externe d'opportunités.

JobOffer
Offre d'emploi normalisée.

OpportunityAnalysis
Résultat d'analyse d'une opportunité.

Application
Candidature suivie dans le système.

MarketInsight
Analyse marché.

CareerGoal
Objectif carrière futur.

---

## Architecture Backend

app/
├── core/
├── auth/
├── profile/
├── skills/
├── experience/
├── languages/
├── certifications/
├── cv/
├── profile_enrichment/
├── reference_data/
├── jobs/
├── matching/
├── applications/
├── settings/
└── ai/

### Futurs domaines prévus

search_criteria/
job_discovery/
job_sources/
opportunity_analysis/
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
layouts/

Architecture cible :

Dashboard
Profile
Search Criteria
Opportunities
Opportunity Details
Applications
Settings

### Architecture Frontend Cible

Stack frontend validée :

- React Router
- Zustand
- TanStack Query
- React Hook Form
- Zod
- shadcn/ui
- Tailwind CSS
- Lucide Icons

Principes :

- Authentification dès le MVP
- Routes protégées
- Sidebar rétractable
- Desktop First
- Light Theme
- Dark Theme
- WCAG AA
- Internationalisation dès l'architecture

Langue MVP :

- English

Langue post MVP :

- Français

---

## Règles architecture

- Architecture modulaire.
- Responsabilités clairement séparées.
- Pas de dépendances circulaires.
- Logique métier dans le backend.
- Frontend focalisé sur la présentation.
- Module AI isolé.
- Simplicité avant optimisation.
- Le profil structuré constitue la source de vérité.
- Les scores doivent toujours être explicables.
- Toute logique de scoring appartient au backend.
- Toute logique de matching appartient au backend.
- L'IA enrichit les résultats mais ne remplace jamais les règles métier.
- Les offres collectées conservent leur lien source d'origine.
- Le frontend est une couche de navigation et de visualisation.

Exception MVP:
Profile Completeness is a frontend-only visualization score.
It is computed from already loaded profile data.
No backend persistence exists.
No business decision depends on this score.

---

### Work Mode

Le système prend en charge les modes de travail suivants :

- Remote
- Hybrid
- Onsite

Ce critère pourra être utilisé dans :

- les critères de recherche ;
- le filtrage ;
- le scoring ;
- l'analyse des opportunités.

---

## Architecture cible

Monolithe modulaire.

Pas de microservices.

Pas de CQRS.

Pas d'Event Sourcing.

Pas de complexité prématurée.

---

Frontend navigation supports:

Profile
↔ Applications

Opportunity
↔ Applications

Applications
↔ Profile

Applications
↔ Opportunity

Applications may be created directly from Opportunities.

### CV Parsing Architecture

Version actuelle :

- Extraction PDF via PyPDF2
- Extraction DOCX via python-docx
- Parsing heuristique par sections

Amélioration V1 :

- Support des contenus présents dans les tableaux DOCX
- Validation renforcée des noms détectés
- Gestion explicite des sections PROFIL
- Séparation des soft skills et hard skills

Validation status:

- Parser benchmark framework implemented
- 8 parser fixtures validated
- Standard sidebar CV layouts supported
- Multiple skills sections supported
- 256 backend tests passing

Known limitation:
Complex multi-column PDFs may produce corrupted reading order when extracted through PyPDF2.

Representative example:
CV Lathan

Current decision:
Support for complex multi-column PDFs significantly improved.

Validated:

- benchmark fixtures
- real Lathan CV
- re-upload validation through CV 1070

Known remaining limitation:
some tool/language combinations may still appear merged in extracted skills.

A dedicated extraction phase must be completed before AI Career Advisor integration.

Reference failing scenario:

- CV Lathan

AI safety boundary:
Profile data produced by a known failed extraction must not be treated as reliable AI context.

Current implementation:

- PyPDF2 extraction engine
- pdfplumber extraction engine
- extraction quality evaluation
- automatic engine selection

Validation:

- benchmark fixtures validated
- Lathan real CV validated
- experience reconstruction validated

Known limitation:
Some tool/language combinations may still appear merged
inside skill extraction results.

### Authentication

Current authentication UX includes:

- Login page
- Forgot Password page (connected to real API)
- Reset Password page (new, token read from URL)
- Confirm Email Change page (new, explicit click confirmation)
- Account page (with Change Email form)

The authentication roadmap is visible inside Account Page.

Password Recovery:

- PasswordResetToken model persists a SHA-256 hash of the token, never the raw value
- token expiration is configurable via PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
- a new request invalidates any previous unused token for the same user
- the public forgot-password response is identical whether the account exists or not
- real SMTP delivery validated through Mailtrap

Email Recovery:

- EmailChangeRequest model reuses the same token hashing strategy
- the confirmation email is sent to the CURRENT email address, never to the requested new address
- confirmation requires an explicit user action (button click), not an automatic action on page load
- uniqueness of the new email is verified both at request time and at confirmation time

SMTP configuration:

- SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM_EMAIL, SMTP_FROM_NAME, SMTP_USE_TLS
- stored as environment variables, never in PostgreSQL
- validated against a real Mailtrap sandbox

Sign Up:

- registration endpoint gated by PUBLIC_REGISTRATION_ENABLED environment variable (disabled by default)
- password policy enforced: minimum 8 characters, one uppercase, one lowercase, one digit, one special character
- the same password policy is enforced on both Sign Up and Reset Password
- real-time password checklist displayed in the frontend during password entry

Remember Me:

- access tokens default to a 60-minute expiration (ACCESS_TOKEN_EXPIRE_MINUTES)
- an optional remember_me flag on login extends the token expiration to 30 days (REMEMBER_ME_TOKEN_EXPIRE_MINUTES)
- token storage strategy in the frontend (localStorage) is unchanged; only the JWT expiration duration varies
- backward compatible: remember_me defaults to false, preserving existing behavior for any caller that omits it

Combined validation:

- Sign Up, Password Recovery, Email Recovery and Remember Me were validated together in a single end-to-end scenario, not only in isolation

Future learning features:

- MFA
- SSO
