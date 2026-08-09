# Profile Management Visualization Review

## Phase

7.1.13.2 Profile Management Visualization Review

## Statut

Review

## Date

2026-08-09

## Objectif

Analyser les fichiers réels du frontend et du backend afin de vérifier si la page Profiles peut être transformée en véritable écran métier sans modification backend.

Cette revue doit déterminer :

- les fichiers frontend existants ;
- les composants frontend réutilisables ;
- les endpoints backend disponibles ;
- les données accessibles ;
- les risques d'intégration ;
- les fichiers à modifier ;
- les fichiers à créer ;
- le plan d'implémentation recommandé.

Aucun code ne doit être produit pendant cette phase.

## Sources analysées

Fichiers frontend analysés :

- frontend/src/pages/ProfilesPage.tsx
- frontend/src/components/ProfileList.tsx
- frontend/src/services/api.ts

Recherches frontend analysées :

- recherche des occurrences de Profile dans frontend/src
- arborescence frontend/src/components
- arborescence frontend/src/pages

Recherches backend analysées :

- occurrences de profile dans backend/app
- occurrences de router dans backend/app
- occurrences de Profile dans backend/app
- occurrences de Skill dans backend/app
- occurrences de WorkExperience dans backend/app
- occurrences de Language dans backend/app
- occurrences de Certification dans backend/app
- arborescence backend/app

## Résumé exécutif

La page Profiles est actuellement un placeholder.

Le backend contient déjà les domaines nécessaires pour afficher une page métier Profile :

- Profile
- ProfileSkill
- Skill
- WorkExperience
- Language
- ProfileLanguage
- Certification
- ProfileCertification

Les routers backend exposent déjà des endpoints pour :

- lister les profils ;
- récupérer un profil ;
- récupérer les compétences d'un profil ;
- récupérer les expériences d'un profil ;
- récupérer les langues d'un profil ;
- récupérer les certifications d'un profil.

Conclusion :

Une première visualisation frontend Profiles peut être implémentée sans créer de nouveau domaine backend.

Cependant, les endpoints liés aux compétences, langues et certifications semblent principalement retourner des relations par identifiants.

Il faudra donc vérifier ou composer les données côté frontend avec les listes de référence :

- skills
- languages
- certifications

afin d'afficher des noms lisibles au lieu de simples IDs.

## État frontend actuel

### ProfilesPage.tsx

Le fichier est actuellement :

- très simple ;
- sans appel API ;
- sans state ;
- sans affichage de données ;
- sans composant métier.

Contenu fonctionnel actuel :

- PageHeader
- texte placeholder

Limite :

La page ne démontre pas la valeur du profil candidat.

### ProfileList.tsx

Le composant existe déjà.

Il affiche :

- id
- full_name

Le composant prend :

profiles

en prop.

Limites :

- pas de sélection de profil ;
- pas d'état actif ;
- pas de callback onSelect ;
- pas d'affichage du profile_name ;
- pas d'information complémentaire.

Décision :

ProfileList peut être réutilisé mais doit être enrichi.

### services/api.ts

Le fichier contient déjà :

- getProfiles
- getJobOffers
- getMatching
- getRankedJobOffers
- getApplications

Il manque encore des fonctions frontend pour consommer :

- profile skills
- work experiences
- profile languages
- profile certifications
- skills reference list
- languages reference list
- certifications reference list

Décision :

Ajouter des fonctions API frontend est nécessaire.

## Structure frontend actuelle

Dossier components :

- AIExplanationCard.tsx
- ApplicationTracker.tsx
- Dashboard.tsx
- JobOfferList.tsx
- MatchingResult.tsx
- OpportunityRanking.tsx
- ProfileList.tsx

Dossier components/ui :

- Card.tsx
- PageHeader.tsx
- Section.tsx
- StatCard.tsx

Dossier pages :

- AccountPage.tsx
- ApplicationsPage.tsx
- DashboardPage.tsx
- ForgotPasswordPage.tsx
- LoginPage.tsx
- OpportunitiesPage.tsx
- ProfilesPage.tsx
- SettingsPage.tsx

Aucun sous-dossier dédié aux profiles n'existe actuellement.

## État backend observé

### Profile

Backend observé :

- backend/app/profile/models.py
- backend/app/profile/router.py
- backend/app/profile/schemas.py

Endpoints observés :

- POST /profiles
- GET /profiles
- GET /profiles/{profile_id}

Données profil observées dans router :

- profile_name
- full_name
- current_title
- location
- years_of_experience
- target_role_short_term
- target_role_long_term
- remote_preference
- preferred_countries

Conclusion :

Les informations générales du profil sont disponibles.

### Profile Skills

Backend observé :

- backend/app/profile/profile_skill_models.py
- backend/app/profile/profile_skill_router.py
- backend/app/profile/profile_skill_schemas.py

Endpoints observés :

- POST /profile-skills
- GET /profile-skills
- GET /profiles/{profile_id}/skills

Données observées :

- profile_id
- skill_id
- years_of_experience
- self_assessment_level

Point d'attention :

La relation ProfileSkill semble exposer skill_id.

Pour afficher le nom de la compétence, le frontend devra probablement aussi charger :

GET /skills

et faire une correspondance skill_id → skill.name.

### Skills

Backend observé :

- backend/app/skills/models.py
- backend/app/skills/router.py
- backend/app/skills/schemas.py

Endpoints observés :

- POST /skills
- GET /skills
- GET /skills/{skill_id}

Données observées :

- name
- category

Conclusion :

Le frontend peut récupérer le catalogue de compétences.

### Work Experience

Backend observé :

- backend/app/experience/models.py
- backend/app/experience/router.py
- backend/app/experience/schemas.py

Endpoints observés :

- POST work experience
- GET work experiences
- GET work experience by id
- GET /profiles/{profile_id}/work-experiences

Conclusion :

Les expériences professionnelles peuvent être affichées pour un profil.

### Languages

Backend observé :

- backend/app/languages/models.py
- backend/app/languages/router.py
- backend/app/languages/schemas.py

Endpoints observés :

- GET /languages
- GET /languages/{language_id}
- GET /profile-languages
- GET /profiles/{profile_id}/languages

Données relation observées :

- profile_id
- language_id
- proficiency_level

Point d'attention :

Le frontend devra probablement charger :

GET /languages

pour convertir language_id en nom lisible.

### Certifications

Backend observé :

- backend/app/certifications/models.py
- backend/app/certifications/router.py
- backend/app/certifications/schemas.py

Endpoints observés :

- GET /certifications
- GET /certifications/{certification_id}
- GET /profile-certifications
- GET /profiles/{profile_id}/certifications

Données relation observées :

- profile_id
- certification_id
- obtained_date
- expiration_date
- credential_id

Point d'attention :

Le frontend devra probablement charger :

GET /certifications

pour convertir certification_id en nom lisible.

## Décision d'architecture frontend

La page Profiles peut être implémentée comme une page master/detail.

### Colonne gauche

Responsabilité :

- afficher les profils ;
- permettre la sélection du profil actif ;
- mettre en évidence le profil sélectionné.

### Panneau droit

Responsabilité :

- afficher les informations générales ;
- afficher les KPIs profil ;
- afficher les compétences ;
- afficher les expériences ;
- afficher les langues ;
- afficher les certifications.

## Endpoints frontend à ajouter dans services/api.ts

Ajouter les fonctions suivantes :

- getProfile(profileId)
- getProfileSkills(profileId)
- getSkills()
- getProfileWorkExperiences(profileId)
- getLanguages()
- getProfileLanguages(profileId)
- getCertifications()
- getProfileCertifications(profileId)

## Stratégie de chargement recommandée

Étape 1 :

Charger les profils avec getProfiles.

Étape 2 :

Sélectionner automatiquement le premier profil si la liste n'est pas vide.

Étape 3 :

Lorsqu'un profil est sélectionné, charger en parallèle :

- profile skills
- skills
- work experiences
- profile languages
- languages
- profile certifications
- certifications

Étape 4 :

Composer les données côté frontend pour afficher des noms lisibles.

## Données composées côté frontend

### Skills

profileSkill.skill_id

doit être rapproché de :

skill.id

pour afficher :

skill.name

et éventuellement :

skill.category

### Languages

profileLanguage.language_id

doit être rapproché de :

language.id

pour afficher :

language.name

et :

profileLanguage.proficiency_level

### Certifications

profileCertification.certification_id

doit être rapproché de :

certification.id

pour afficher :

certification.name

et :

certification.issuing_organization

## Fichiers à modifier

### Fichier 1

frontend/src/pages/ProfilesPage.tsx

Modifications prévues :

- ajouter state profiles ;
- ajouter state selectedProfile ;
- ajouter state profileSkills ;
- ajouter state workExperiences ;
- ajouter state profileLanguages ;
- ajouter state profileCertifications ;
- ajouter loading ;
- ajouter error ;
- remplacer placeholder par master/detail layout.

### Fichier 2

frontend/src/components/ProfileList.tsx

Modifications prévues :

- ajouter selectedProfileId ;
- ajouter onSelectProfile ;
- ajouter style actif ;
- conserver affichage simple.

### Fichier 3

frontend/src/services/api.ts

Modifications prévues :

- ajouter fonctions API profile-related.

## Fichiers à créer

### Fichier 1

frontend/src/components/ProfileDetail.tsx

Responsabilité :

Afficher le détail d'un profil.

### Fichier 2

frontend/src/components/ProfileSkillsSection.tsx

Responsabilité :

Afficher les compétences du profil.

### Fichier 3

frontend/src/components/ProfileExperienceSection.tsx

Responsabilité :

Afficher les expériences du profil.

### Fichier 4

frontend/src/components/ProfileLanguagesSection.tsx

Responsabilité :

Afficher les langues du profil.

### Fichier 5

frontend/src/components/ProfileCertificationsSection.tsx

Responsabilité :

Afficher les certifications du profil.

## Décision MVP

Pour éviter une explosion de fichiers trop tôt, deux approches sont possibles.

### Option A

Créer tous les composants séparés.

Avantage :

- propre ;
- maintenable ;
- clair.

Inconvénient :

- plus de fichiers.

### Option B

Créer uniquement ProfileDetail.tsx et garder les sous-sections internes.

Avantage :

- plus rapide ;
- moins de fichiers.

Inconvénient :

- fichier potentiellement long.

## Recommandation

Choisir Option A.

Raison :

Le projet a déjà commencé à structurer le frontend en composants.

La page Profile va devenir une source de vérité importante.

La séparation des sections réduira la dette technique.

## Première version MVP recommandée

Créer :

- ProfileDetail.tsx
- ProfileSkillsSection.tsx
- ProfileExperienceSection.tsx
- ProfileLanguagesSection.tsx
- ProfileCertificationsSection.tsx

Modifier :

- ProfilesPage.tsx
- ProfileList.tsx
- services/api.ts

Ne pas ajouter d'édition.

Ne pas ajouter de création.

Ne pas ajouter de suppression.

## KPIs profil à afficher

Afficher en haut du panneau détail :

- Skills
- Experiences
- Languages
- Certifications

Calculés côté frontend à partir des tableaux chargés.

## États UI à gérer

### Loading profiles

Afficher :

Loading profiles...

### Loading profile details

Afficher :

Loading profile details...

### No profiles

Afficher :

No profiles available.

### Error

Afficher :

Unable to load profiles.

## Risques identifiés

### Risque 1

Les endpoints retournent des relations avec identifiants mais pas les noms.

Mitigation :

charger les catalogues skills, languages, certifications.

### Risque 2

Trop d'appels API en parallèle.

Mitigation :

acceptable pour MVP local.

Optimisation future possible.

### Risque 3

Complexité frontend excessive.

Mitigation :

composants séparés.

### Risque 4

Données vides.

Mitigation :

états vides par section.

### Risque 5

Créer du CRUD prématurément.

Mitigation :

visualisation uniquement.

## Décisions validées

DEC-7.1.13-001

Profiles doit devenir une page métier avant AI Career Advisor.

DEC-7.1.13-002

La première version est lecture seule.

DEC-7.1.13-003

Aucun nouveau backend n'est requis pour la première visualisation.

DEC-7.1.13-004

Le frontend composera les relations profile skills, languages et certifications avec les catalogues de référence.

DEC-7.1.13-005

Le layout sera master/detail, cohérent avec Opportunities.

DEC-7.1.13-006

Les composants seront séparés par section.

## Plan d'implémentation recommandé

### Étape 1

Ajouter les fonctions API dans :

frontend/src/services/api.ts

### Étape 2

Modifier :

frontend/src/components/ProfileList.tsx

### Étape 3

Créer :

frontend/src/components/ProfileSkillsSection.tsx

### Étape 4

Créer :

frontend/src/components/ProfileExperienceSection.tsx

### Étape 5

Créer :

frontend/src/components/ProfileLanguagesSection.tsx

### Étape 6

Créer :

frontend/src/components/ProfileCertificationsSection.tsx

### Étape 7

Créer :

frontend/src/components/ProfileDetail.tsx

### Étape 8

Modifier :

frontend/src/pages/ProfilesPage.tsx

### Étape 9

Lancer :

npm run build

### Étape 10

Lancer :

pytest

### Étape 11

Validation visuelle de ProfilesPage

## Validation fonctionnelle attendue

L'utilisateur ouvre Profiles.

Résultat attendu :

- liste des profils visible ;
- premier profil sélectionné automatiquement ;
- panneau détail visible ;
- informations générales visibles ;
- KPIs visibles ;
- skills visibles ou état vide ;
- experiences visibles ou état vide ;
- languages visibles ou état vide ;
- certifications visibles ou état vide.

## Validation visuelle attendue

La page doit être cohérente avec Opportunities :

- même largeur globale ;
- même logique master/detail ;
- même style de cartes ;
- même dark theme ;
- même hiérarchie textuelle.

## Critères de fin

La phase de revue est terminée lorsque :

- les fichiers réels ont été analysés ;
- les endpoints disponibles ont été identifiés ;
- les limites API ont été identifiées ;
- les fichiers à modifier sont listés ;
- les fichiers à créer sont listés ;
- les risques sont documentés ;
- le plan d'implémentation est défini.

## Hors périmètre

Ne pas implémenter :

- édition de profil ;
- création de profil ;
- suppression de profil ;
- import CV ;
- import LinkedIn ;
- génération IA ;
- recommandations carrière ;
- refonte complète du design ;
- pagination ;
- recherche ;
- filtres avancés.

## Livrable

docs/profile-management-visualization-review.md

## Étape suivante recommandée

Phase 7.1.13.3

Profile Management Visualization Implementation Plan

Objectif :

Définir précisément le code à créer, les types TypeScript, les fonctions API, les composants React et les validations à exécuter avant le développement.
