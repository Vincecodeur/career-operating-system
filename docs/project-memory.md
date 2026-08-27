# Project Memory

## Contexte

Career Operating System est un projet personnel destiné à aider Vincent à piloter sa carrière de manière structurée, objective et basée sur des données.

Le système est conçu comme une plateforme personnelle d'intelligence carrière et d'aide à la décision.

---

## Utilisateur principal

Vincent.

Le projet est optimisé pour un utilisateur unique.

Aucun support multi-utilisateur n'est prévu.

---

### Multi-profils

Le système supporte plusieurs profils candidats.

Objectif :

- comparer plusieurs trajectoires professionnelles ;
- comparer plusieurs stratégies de carrière ;
- analyser une même opportunité selon plusieurs profils.

Exemples :

- Profil actuel
- Profil Solution Architect
- Profil Product Manager
- Profil Head of Partnerships

MVP Multi-Profile Strategy

The system does not use a global default profile.

Opportunity workflows use:

- one Primary Profile;
- one or more Active Profiles.

Primary Profile rules:

- the first available profile is selected when no context exists;
- the Primary Profile belongs to Active Profiles;
- opportunity ranking uses only the Primary Profile;
- score-based opportunity filtering uses only the Primary Profile;
- opportunity cards display the Primary Profile score;
- changing Active Profiles without changing the Primary Profile does not change ranking.

Active Profiles rules:

- several profiles can be active simultaneously;
- matching remains calculated independently for each profile;
- opportunity details display profile-specific comparison results;
- opportunity details identify the Best Matching Profile;
- active profiles are never merged into a combined profile;
- no average or combined multi-profile score is calculated.

Application profile attribution rules:

- an Application is attached to exactly one Profile;
- application creation recommends the Best Matching Profile;
- the Primary Profile resolves equal matching scores;
- the lowest profile_id resolves any remaining tie;
- the user may select another active profile before validation;
- the confirmed profile is attached to the created Application;
- the Application may later be explicitly reassigned to another active Profile;
- every effective reassignment creates a PROFILE_CHANGED timeline event;
- changing an Application profile does not change the Primary Profile or Active Profiles context.

Persistence rules:

- the Opportunity Context is not persisted during the MVP;
- no global default profile is stored;
- a new session starts from the first available profile.

Validation status:

- Opportunity → Application workflow validated
- Profile reassignment validated
- PROFILE_CHANGED audit trail validated
- Inactive profile protection validated
- End-to-end multi-profile workflow validated

---

## Règles projet

Aucune mention d'un employeur, client ou partenaire dans :

- le code ;
- l'architecture ;
- les règles métier ;
- la roadmap ;
- les exemples.

Exception :

Les expériences professionnelles de Vincent peuvent être utilisées dans son profil candidat.

---

## Contraintes personnelles

Le projet doit être :

- facilement maintenable ;
- compréhensible après plusieurs mois d'arrêt ;
- simple à reprendre dans un nouveau thread Copilot ;
- publiable sur GitHub ;
- utilisable avec ou sans IA ;
- capable de fonctionner avec plusieurs profils candidats ;
- basé sur des données explicables et vérifiables ;
- conçu selon une approche documentation-first ;
- conçu selon une approche UX-first pour les évolutions frontend ;
- construit par étapes incrémentales afin de limiter les refactorings majeurs.

La simplicité, la lisibilité et la capacité de reprise priment toujours sur la sophistication technique.

---

## Philosophie technique

Priorité :

1. Clarté
2. Apprentissage
3. Maintenabilité

Avant :

- Optimisation
- Performance
- Scalabilité

---

## Philosophie produit

Le Job Board n'est pas le produit.

Le suivi des candidatures n'est pas le produit.

Le produit est un système d'intelligence carrière.

Le coeur fonctionnel du MVP est :

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

Le système doit aider à identifier les meilleures opportunités et à prendre de meilleures décisions professionnelles.

Les paramètres métier sont configurables par l'utilisateur.

Les secrets techniques restent séparés des paramètres métier.

Les paramètres métier sont persistés dans PostgreSQL via le domaine Settings.

---

## Règle de simplicité

Toute fonctionnalité doit être développée dans sa version la plus simple avant d'être complexifiée.

---

### Philosophie UX

Le projet suit une approche UX First.

Avant toute évolution majeure du frontend :

- les parcours utilisateurs doivent être définis ;
- les pages doivent être identifiées ;
- les wireframes doivent être produits ;
- la navigation doit être validée.

Le développement frontend suit la vision produit et non l'inverse.

---

### Philosophie Frontend

Le frontend doit être conçu comme une application SaaS personnelle, professionnelle et maintenable.

Décisions structurantes validées :

- approche desktop first ;
- sidebar gauche rétractable ;
- header léger ;
- theme light et dark ;
- accessibilité cible WCAG AA ;
- design system basé sur shadcn/ui ;
- styling basé sur Tailwind CSS ;
- icônes Lucide ;
- couleur primaire bleue via variables de thème ;
- composants réutilisables ;
- aucune couleur hardcodée dans les composants.

Le frontend doit privilégier :

- la lisibilité ;
- l'analyse ;
- la comparaison ;
- la prise de décision.

Le frontend ne doit pas ressembler à :

- un job board marketing ;
- un réseau social ;
- un ATS complet ;
- une marketplace de recrutement.

---

#### Design System Foundation

Décisions validées :

- style Modern SaaS + Data Analytics ;
- sidebar de référence à 280px ;
- densité visuelle aérée ;
- dark mode par défaut ;
- light mode supporté ;
- KPI Cards utilisées pour les métriques principales ;
- premières briques UI internes créées avant l'introduction de shadcn/ui.

Composants UI initiaux :

- PageHeader
- Section
- Card
- StatCard

Le Dashboard doit progressivement évoluer vers une interface structurée autour de sections et cartes réutilisables.

---

### Authentification

L'authentification fait partie du MVP.

Décisions validées :

- email + mot de passe au MVP ;
- SSO possible plus tard ;
- un seul compte utilisateur créé manuellement au MVP ;
- pas d'inscription publique dans le MVP ;
- JWT access token ;
- refresh token ;
- routes protégées ;
- redirection vers Login si utilisateur non authentifié.

Le choix du compte unique manuel est un compromis MVP.

L'architecture doit rester compatible avec une évolution future vers plusieurs utilisateurs.

---

### Internationalisation

Le frontend doit être pensé multilingue dès le départ.

Décisions validées :

- anglais comme première langue MVP ;
- français prévu rapidement après le MVP ;
- aucune chaîne UI hardcodée dans les composants ;
- toutes les chaînes d'interface doivent être externalisées.

L'objectif est d'éviter un refactoring i18n majeur après le MVP.

---

### Stack Frontend Cible

Choix validés pour la structure frontend :

- React Router pour le routing ;
- Zustand pour le state management global ;
- TanStack Query pour le server state ;
- React Hook Form pour les formulaires ;
- Zod pour la validation ;
- shadcn/ui pour les composants UI ;
- Tailwind CSS pour le styling ;
- Lucide Icons pour les icônes.

Zustand ne doit pas être utilisé pour stocker les données API.

TanStack Query est responsable du cache, des états loading, des retries et de l'invalidation.

La combinaison retenue privilégie :

- la simplicité ;
- la maintenabilité ;
- le typage fort ;
- les standards modernes React ;
- la limitation des refactorings futurs.

---

## Vision long terme

Répondre aux questions :

- Quels postes me correspondent aujourd'hui ?
- Quels postes correspondent à chacun de mes profils candidats ?
- Pourquoi une opportunité est-elle recommandée ?
- Quels sont mes points forts face à cette opportunité ?
- Quels sont mes points faibles face à cette opportunité ?
- Quelles compétences dois-je développer ?
- Quelle opportunité dois-je privilégier ?
- Comment accélérer ma progression professionnelle ?
- Comment évolue ma position sur le marché ?

## Documentation Governance Incident - Greenhouse Integration

During the Greenhouse connector integration, documentation became partially inconsistent after a thread change.

Root cause:

- technical implementation, tests, validation and documentation were not handled as a single coherent feature milestone;
- handoff and status documents temporarily carried outdated next-step information;
- roadmap numbering was affected by mid-thread source strategy changes.

Decision:

- the repository, tests and Git history are the primary source of truth;
- documentation must be synchronized only after technical validation;
- feature work must include code, tests and validation before being considered complete;
- after each thread change, project state must be reconstructed from git status, git log, tests and key documents before generating new code or roadmap changes.

## Règle de structuration des phases

Niveau X
= Capacité produit majeure

Niveau X.Y
= Fonctionnalité métier

Niveau X.Y.Z
= Sous-fonctionnalité métier

Niveau X.Y.Z.W
= Exécution technique

Exemple :

7.1.15 Profile Management CRUD
7.1.15.3 Profile CRUD
7.1.15.3.1 Backend CRUD Completion
7.1.15.3.2 Backend CRUD Validation
7.1.15.3.3 Frontend CRUD Design
7.1.15.3.4 Frontend CRUD Implementation
7.1.15.3.5 Frontend Validation
7.1.15.3.6 Documentation Synchronization

### Règle de livraison Code + Tests

À partir de la phase 7.1.15 :

- Une implémentation backend doit inclure les tests associés dans la même étape.
- Le code et les tests sont développés ensemble avant le commit technique.
- Une étape backend n'est pas terminée tant que :
  - le code est implémenté ;
  - les tests associés existent ;
  - les tests passent.
- La documentation reste traitée dans une étape distincte après le commit technique.

Cycle :

Code
↓
Tests associés
↓
Pytest
↓
Validation
↓
Commit technique
↓
Documentation
↓
Commit documentaire

MVP Review Findings

Critical before AI:

- Existing Data Cleanup
- Enrichment Summary Consistency
- Profile Creation With Optional CV
- Additional Profile Context
- AI Context Contract
- AI Context Preview
- AI Readiness Validation

Completed:

- Test Database Isolation
- CV Parsing Data Quality
- CV Parsing Improvement Design
- CV Parsing Implementation V1
- CV Parsing Regression Validation
- Existing Data Cleanup
- Enrichment Summary Consistency
- Profile Creation With Optional CV
- Additional Profile Context

Data cleanup results:

- Temporary profiles 2101, 2102, 2103 and 2104 removed
- Demo dataset restored to four business profiles
- Invalid enrichment data removed from the Cloud profile
- Invalid CV 822 enrichment proposals removed
- Orphan invalid language catalog entries removed
- Invalid "17/01/2022" skill entry removed
- CV 822 preserved
- No orphan CV storage files detected
- Backend non-regression suite validated with 255 passing tests

Additional Profile Context results:

- Professional Summary stored on Profile
- Career Motivations stored on Profile
- Preferred Environment stored on Profile
- Non-Negotiables stored on Profile
- Additional Context stored on Profile
- PostgreSQL persistence validated
- Create Profile workflow validated
- Edit Profile workflow validated
- Profile Detail display validated
- Frontend build validated
- Backend non-regression suite validated with 257 passing tests

Current Phase:

- Complex Multi-Column PDF Extraction

Remaining:

- Complex Multi-Column PDF Extraction
- AI Context Contract
- AI Context Preview And Consent
- AI Readiness Validation
- Login UX Polish
- Minimal Account UX Polish
- Settings Strategy Synchronization
- Best Profile Recommendation Architecture Review
- Final Regression And Documentation
- MVP Closure Decision
