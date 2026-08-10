# Profile Management CRUD Design

## Phase

7.1.15.2 Profile Management CRUD Design

## Statut

Design

## Contexte

La phase 7.1.15 Profile Management CRUD vise à rendre maintenable la source de vérité carrière du Career Operating System.

Aujourd'hui, le système permet déjà de visualiser :

- les profils ;
- les compétences associées au profil ;
- les expériences professionnelles ;
- les langues ;
- les certifications ;
- les opportunités ;
- les candidatures ;
- les analyses de matching ;
- les explications IA complémentaires.

Cependant, le profil candidat reste uniquement consultable depuis le frontend.

L'utilisateur ne peut pas encore :

- créer un profil depuis l'interface ;
- modifier un profil ;
- supprimer ou archiver un profil ;
- ajouter une compétence depuis l'interface ;
- modifier une compétence associée au profil ;
- supprimer une compétence associée au profil ;
- ajouter une expérience ;
- modifier une expérience ;
- supprimer une expérience ;
- ajouter une langue ;
- modifier une langue associée au profil ;
- supprimer une langue associée au profil ;
- ajouter une certification ;
- modifier une certification associée au profil ;
- supprimer une certification associée au profil ;
- gérer plusieurs profils depuis l'interface.

Cette limite bloque la capacité du produit à devenir un véritable Career Operating System utilisable quotidiennement.

## Source de vérité carrière

La source de vérité carrière du système est constituée de trois éléments :

- le profil structuré ;
- les CV associés ;
- l'historique des candidatures.

La phase 7.1.15 se concentre uniquement sur le premier élément :

- le profil structuré.

Les CV seront traités dans la phase 7.1.16 CV Management.

L'historique et le workflow des candidatures seront traités dans la phase 7.1.17 Application Workflow.

## Résultat du Repository Audit

Le Repository Audit 7.1.15.1 a confirmé que les domaines backend Profile Management sont actuellement limités aux opérations :

- Create ;
- Read.

Aucun endpoint Update, Patch ou Delete n'a été identifié pour les domaines audités.

Domaines audités :

- Profile ;
- Skill ;
- ProfileSkill ;
- WorkExperience ;
- Language ;
- ProfileLanguage ;
- Certification ;
- ProfileCertification.

Conclusion :

Le frontend CRUD ne peut pas être implémenté immédiatement.

Le backend doit d'abord être complété avec les opérations Update et Delete nécessaires.

## Objectif de cette phase

Définir l'architecture cible du CRUD Profile Management avant tout développement.

Cette phase ne produit pas de code.

Elle doit définir :

- le périmètre métier du CRUD ;
- la stratégie backend ;
- la stratégie frontend ;
- les endpoints nécessaires ;
- les règles de suppression ;
- les règles de validation ;
- l'ordre d'implémentation ;
- les limites du MVP ;
- les critères de validation.

## Principes directeurs

### Principe 1

Le profil structuré reste la source de vérité principale.

### Principe 2

Toute logique métier appartient au backend.

### Principe 3

Le frontend ne doit pas contourner l'absence d'API backend.

### Principe 4

La visualisation existe déjà.

Le CRUD doit enrichir l'existant, pas le remplacer.

### Principe 5

La suppression d'éléments sensibles doit être prudente.

### Principe 6

La première version doit rester simple et maintenable.

### Principe 7

Les opérations Update/Delete doivent être testées côté backend avant toute intégration frontend.

## Périmètre fonctionnel global

La phase 7.1.15 couvre :

- Profile CRUD ;
- Skills Management ;
- Experience Management ;
- Languages Management ;
- Certifications Management ;
- Multi Profile Management.

## Hors périmètre global

Ne pas inclure dans cette phase :

- CV Upload ;
- CV Parsing ;
- Profile Enrichment depuis un CV ;
- Application Workflow ;
- Opportunity Filters ;
- Settings Management ;
- AI Career Advisor ;
- génération de CV ;
- génération de lettre de motivation ;
- synchronisation LinkedIn ;
- import automatique depuis un réseau social.

## Découpage cible de la phase 7.1.15

### 7.1.15.1 Repository Audit

Statut :

Terminé.

Résultat :

- backend confirmé en mode Create + Read ;
- absence d'endpoints Update/Delete confirmée ;
- support multi-profile confirmé dans le modèle Profile.

### 7.1.15.2 CRUD Design

Statut :

En cours.

Objectif :

Définir ce document.

### 7.1.15.3 Profile CRUD

Objectif :

Permettre la création, modification et désactivation de profils candidats.

Sous-étapes :

- 7.1.15.3.1 Backend CRUD Completion
- 7.1.15.3.2 Backend CRUD Validation
- 7.1.15.3.3 Frontend CRUD Design
- 7.1.15.3.4 Frontend CRUD Implementation
- 7.1.15.3.5 Frontend Validation
- 7.1.15.3.6 Documentation Synchronization

### 7.1.15.4 Skills Management

Objectif :

Permettre la gestion des compétences du profil.

Sous-étapes :

- 7.1.15.4.1 Backend CRUD Completion
- 7.1.15.4.2 Backend CRUD Validation
- 7.1.15.4.3 Frontend CRUD Design
- 7.1.15.4.4 Frontend CRUD Implementation
- 7.1.15.4.5 Frontend Validation
- 7.1.15.4.6 Documentation Synchronization

### 7.1.15.5 Experience Management

Objectif :

Permettre la gestion des expériences professionnelles.

Sous-étapes :

- 7.1.15.5.1 Backend CRUD Completion
- 7.1.15.5.2 Backend CRUD Validation
- 7.1.15.5.3 Frontend CRUD Design
- 7.1.15.5.4 Frontend CRUD Implementation
- 7.1.15.5.5 Frontend Validation
- 7.1.15.5.6 Documentation Synchronization

### 7.1.15.6 Languages Management

Objectif :

Permettre la gestion des langues du profil.

Sous-étapes :

- 7.1.15.6.1 Backend CRUD Completion
- 7.1.15.6.2 Backend CRUD Validation
- 7.1.15.6.3 Frontend CRUD Design
- 7.1.15.6.4 Frontend CRUD Implementation
- 7.1.15.6.5 Frontend Validation
- 7.1.15.6.6 Documentation Synchronization

### 7.1.15.7 Certifications Management

Objectif :

Permettre la gestion des certifications du profil.

Sous-étapes :

- 7.1.15.7.1 Backend CRUD Completion
- 7.1.15.7.2 Backend CRUD Validation
- 7.1.15.7.3 Frontend CRUD Design
- 7.1.15.7.4 Frontend CRUD Implementation
- 7.1.15.7.5 Frontend Validation
- 7.1.15.7.6 Documentation Synchronization

### 7.1.15.8 Multi Profile Management

Objectif :

Permettre la gestion de plusieurs profils candidats.

Sous-étapes :

- 7.1.15.8.1 Backend Validation
- 7.1.15.8.2 Frontend UX Design
- 7.1.15.8.3 Profile Switcher Implementation
- 7.1.15.8.4 Active Profile Management
- 7.1.15.8.5 Validation
- 7.1.15.8.6 Documentation Synchronization

## Architecture backend cible

Le backend doit être complété avant le frontend.

Chaque domaine métier doit exposer des opérations cohérentes :

- Create ;
- Read ;
- Update ;
- Delete ou soft delete selon le cas.

## Stratégie de suppression

Toutes les suppressions ne doivent pas être traitées de la même façon.

### Profile

Recommandation :

Soft delete.

Raison :

Un profil peut être lié à :

- des candidatures ;
- des historiques de matching ;
- des CV futurs ;
- des données de suivi carrière.

Le modèle Profile contient déjà un champ :

- is_active.

Donc la suppression d'un profil doit désactiver le profil au lieu de le supprimer physiquement.

Endpoint recommandé :

DELETE /profiles/{profile_id}

Comportement :

- définir is_active à false ;
- conserver le profil en base ;
- ne plus l'afficher comme profil actif par défaut.

### ProfileSkill

Recommandation :

Hard delete possible.

Raison :

Il s'agit d'une relation entre un profil et une compétence.

Supprimer cette association ne supprime pas la compétence du catalogue global.

Endpoint recommandé :

DELETE /profile-skills/{profile_id}/{skill_id}

### Skill

Recommandation :

Ne pas supprimer dans le MVP, sauf besoin explicite.

Raison :

Skill est un catalogue partagé.

Supprimer une compétence globale pourrait casser des relations existantes.

Pour le MVP, la gestion prioritaire concerne l'association ProfileSkill, pas le catalogue Skill global.

### WorkExperience

Recommandation :

Hard delete possible.

Raison :

Une expérience appartient à un profil.

Endpoint recommandé :

DELETE /work-experiences/{work_experience_id}

### ProfileLanguage

Recommandation :

Hard delete possible.

Raison :

Il s'agit d'une relation entre un profil et une langue.

Endpoint recommandé :

DELETE /profile-languages/{profile_id}/{language_id}

### Language

Recommandation :

Ne pas supprimer dans le MVP, sauf besoin explicite.

Raison :

Language est un catalogue partagé.

La priorité MVP est de gérer la relation ProfileLanguage.

### ProfileCertification

Recommandation :

Hard delete possible.

Raison :

Il s'agit d'une relation entre un profil et une certification.

Endpoint recommandé :

DELETE /profile-certifications/{profile_id}/{certification_id}

### Certification

Recommandation :

Ne pas supprimer dans le MVP, sauf besoin explicite.

Raison :

Certification est un catalogue partagé.

La priorité MVP est de gérer la relation ProfileCertification.

## Stratégie Update

### Profile Update

Endpoint recommandé :

PUT /profiles/{profile_id}

Payload :

- profile_name ;
- full_name ;
- current_title ;
- location ;
- years_of_experience ;
- target_role_short_term ;
- target_role_long_term ;
- remote_preference ;
- preferred_countries.

Réponse :

ProfileResponse.

Règles :

- retourner 404 si le profil n'existe pas ;
- ne pas modifier created_at ;
- modifier updated_at ;
- conserver is_active.

### ProfileSkill Update

Endpoint recommandé :

PUT /profile-skills/{profile_id}/{skill_id}

Payload :

- years_of_experience ;
- self_assessment_level.

Réponse :

ProfileSkillResponse.

Règles :

- retourner 404 si l'association n'existe pas ;
- ne pas modifier profile_id ;
- ne pas modifier skill_id.

### WorkExperience Update

Endpoint recommandé :

PUT /work-experiences/{work_experience_id}

Payload :

- company_name ;
- job_title ;
- start_date ;
- end_date ;
- is_current_position ;
- description.

Réponse :

WorkExperienceResponse.

Règles :

- retourner 404 si l'expérience n'existe pas ;
- ne pas modifier profile_id ;
- ne pas modifier created_at.

### ProfileLanguage Update

Endpoint recommandé :

PUT /profile-languages/{profile_id}/{language_id}

Payload :

- proficiency_level.

Réponse :

ProfileLanguageResponse.

Règles :

- retourner 404 si l'association n'existe pas ;
- ne pas modifier profile_id ;
- ne pas modifier language_id.

### ProfileCertification Update

Endpoint recommandé :

PUT /profile-certifications/{profile_id}/{certification_id}

Payload :

- obtained_date ;
- expiration_date ;
- credential_id.

Réponse :

ProfileCertificationResponse.

Règles :

- retourner 404 si l'association n'existe pas ;
- ne pas modifier profile_id ;
- ne pas modifier certification_id.

## Endpoints backend à ajouter

### Profile

PUT /profiles/{profile_id}

DELETE /profiles/{profile_id}

### ProfileSkill

PUT /profile-skills/{profile_id}/{skill_id}

DELETE /profile-skills/{profile_id}/{skill_id}

### WorkExperience

PUT /work-experiences/{work_experience_id}

DELETE /work-experiences/{work_experience_id}

### ProfileLanguage

PUT /profile-languages/{profile_id}/{language_id}

DELETE /profile-languages/{profile_id}/{language_id}

### ProfileCertification

PUT /profile-certifications/{profile_id}/{certification_id}

DELETE /profile-certifications/{profile_id}/{certification_id}

## Endpoints non prioritaires pour le MVP

Les endpoints suivants ne sont pas prioritaires pendant la première version CRUD :

- PUT /skills/{skill_id}
- DELETE /skills/{skill_id}
- PUT /languages/{language_id}
- DELETE /languages/{language_id}
- PUT /certifications/{certification_id}
- DELETE /certifications/{certification_id}

Raison :

Ces domaines sont des catalogues globaux.

Le besoin utilisateur immédiat est de gérer les éléments associés au profil, pas d'administrer les catalogues globaux.

## Schémas backend à ajouter

### ProfileUpdate

Champs :

- profile_name ;
- full_name ;
- current_title ;
- location ;
- years_of_experience ;
- target_role_short_term ;
- target_role_long_term ;
- remote_preference ;
- preferred_countries.

### ProfileSkillUpdate

Champs :

- years_of_experience ;
- self_assessment_level.

### WorkExperienceUpdate

Champs :

- company_name ;
- job_title ;
- start_date ;
- end_date ;
- is_current_position ;
- description.

### ProfileLanguageUpdate

Champs :

- proficiency_level.

### ProfileCertificationUpdate

Champs :

- obtained_date ;
- expiration_date ;
- credential_id.

## Validation backend attendue

Chaque endpoint Update doit être testé.

Chaque endpoint Delete doit être testé.

## Tests backend attendus

### Profile

Tests à ajouter :

- update profile returns updated profile ;
- update profile returns 404 if profile not found ;
- delete profile deactivates profile ;
- delete profile returns 404 if profile not found ;
- deleted profile is_active becomes false.

### ProfileSkill

Tests à ajouter :

- update profile skill returns updated relation ;
- update profile skill returns 404 if relation not found ;
- delete profile skill removes relation ;
- delete profile skill returns 404 if relation not found.

### WorkExperience

Tests à ajouter :

- update work experience returns updated experience ;
- update work experience returns 404 if not found ;
- delete work experience removes experience ;
- delete work experience returns 404 if not found.

### ProfileLanguage

Tests à ajouter :

- update profile language returns updated relation ;
- update profile language returns 404 if relation not found ;
- delete profile language removes relation ;
- delete profile language returns 404 if relation not found.

### ProfileCertification

Tests à ajouter :

- update profile certification returns updated relation ;
- update profile certification returns 404 if relation not found ;
- delete profile certification removes relation ;
- delete profile certification returns 404 if relation not found.

## Stratégie frontend cible

Le frontend viendra après validation backend.

Aucune interface CRUD ne doit être développée tant que les endpoints backend ne sont pas validés par tests.

## Frontend UX cible

### ProfilesPage

La page Profiles doit conserver son layout actuel :

- liste des profils à gauche ;
- détail du profil à droite.

Elle devra ajouter progressivement :

- Create Profile ;
- Edit Profile ;
- Delete Profile ;
- Add Skill ;
- Edit Skill ;
- Remove Skill ;
- Add Experience ;
- Edit Experience ;
- Remove Experience ;
- Add Language ;
- Edit Language ;
- Remove Language ;
- Add Certification ;
- Edit Certification ;
- Remove Certification.

## Formulaires frontend attendus

### Profile Form

Champs :

- Profile Name ;
- Full Name ;
- Current Title ;
- Location ;
- Years of Experience ;
- Short-Term Target Role ;
- Long-Term Target Role ;
- Remote Preference ;
- Preferred Countries.

### Skill Association Form

Champs :

- Skill ;
- Years of Experience ;
- Self Assessment Level.

### Experience Form

Champs :

- Company Name ;
- Job Title ;
- Start Date ;
- End Date ;
- Is Current Position ;
- Description.

### Language Form

Champs :

- Language ;
- Proficiency Level.

### Certification Form

Champs :

- Certification ;
- Obtained Date ;
- Expiration Date ;
- Credential ID.

## Règles UX

### Création

L'utilisateur doit pouvoir créer un élément depuis la page Profiles.

### Modification

L'utilisateur doit pouvoir modifier un élément depuis la section concernée.

### Suppression

L'utilisateur doit voir une action explicite.

Pour le MVP, une confirmation simple est suffisante.

### Erreur

Afficher un message clair :

Unable to save profile.

ou équivalent selon le domaine.

### Loading

Afficher un état simple :

Saving...

ou :

Deleting...

## Ordre d'implémentation recommandé

### Étape 1

Backend Profile CRUD.

Pourquoi :

Profile est la racine de la source de vérité carrière.

### Étape 2

Backend ProfileSkill CRUD.

Pourquoi :

Les compétences alimentent directement le matching.

### Étape 3

Backend WorkExperience CRUD.

Pourquoi :

L'expérience influence le matching et la qualité du profil.

### Étape 4

Backend ProfileLanguage CRUD.

Pourquoi :

Les langues sont utiles pour la recherche d'opportunités et l'analyse du profil.

### Étape 5

Backend ProfileCertification CRUD.

Pourquoi :

Les certifications enrichissent le profil et peuvent être utiles au matching futur.

### Étape 6

Frontend Profile CRUD.

### Étape 7

Frontend Skills Management.

### Étape 8

Frontend Experience Management.

### Étape 9

Frontend Languages Management.

### Étape 10

Frontend Certifications Management.

### Étape 11

Multi Profile Management.

## Décisions de design

### DEC-7.1.15-001

Le backend doit être complété avant toute implémentation frontend CRUD.

### DEC-7.1.15-002

Profile utilise une suppression logique via is_active.

### DEC-7.1.15-003

Les relations ProfileSkill, ProfileLanguage et ProfileCertification peuvent être supprimées physiquement.

### DEC-7.1.15-004

WorkExperience peut être supprimé physiquement.

### DEC-7.1.15-005

Les catalogues globaux Skill, Language et Certification ne sont pas prioritaires en CRUD complet pour le MVP.

### DEC-7.1.15-006

La page Profiles reste le point central de l'édition de la source de vérité carrière.

### DEC-7.1.15-007

Le frontend CRUD ne doit pas contourner l'absence de endpoints backend.

### DEC-7.1.15-008

Le multi-profile sera traité après la stabilisation du CRUD des éléments de profil.

## Risques identifiés

### Risque 1

Complexité trop élevée si tout le CRUD est développé en une seule étape.

Mitigation :

Découper par domaine.

### Risque 2

Suppression accidentelle de données historiques.

Mitigation :

Soft delete sur Profile.

### Risque 3

Confusion entre catalogue global et relation profil.

Mitigation :

Prioriser les relations de profil plutôt que les catalogues globaux.

### Risque 4

Frontend CRUD développé avant backend validé.

Mitigation :

Respecter l'ordre backend → tests → frontend.

### Risque 5

Multi-profile prématuré.

Mitigation :

Traiter Multi Profile Management après la stabilisation du CRUD de base.

## Critères de fin de phase 7.1.15.2

Cette phase est terminée lorsque :

- le périmètre CRUD est défini ;
- les endpoints backend cibles sont définis ;
- la stratégie de suppression est définie ;
- les schémas update nécessaires sont identifiés ;
- les tests backend attendus sont listés ;
- la stratégie frontend est définie ;
- les décisions de design sont documentées ;
- les risques sont documentés ;
- l'ordre d'implémentation est défini.

## Hors périmètre de ce document

Ce document ne produit pas :

- de code backend ;
- de code frontend ;
- de migration ;
- de tests ;
- de formulaire React ;
- de composant frontend ;
- de modification d'API.

## Livrable

docs/profile-crud-design.md

## Étape suivante recommandée

Phase 7.1.15.3.1 Backend CRUD Completion

Objectif :

Ajouter les endpoints backend Update/Delete nécessaires pour Profile CRUD, en commençant par le domaine Profile.

Première cible technique :

- PUT /profiles/{profile_id}
- DELETE /profiles/{profile_id}

Validation attendue :

- tests backend Profile CRUD passants ;
- aucun changement frontend pendant cette sous-phase.
