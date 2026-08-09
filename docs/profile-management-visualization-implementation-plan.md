# Profile Management Visualization Implementation Plan

## Phase

7.1.13.3 Profile Management Visualization Implementation Plan

## Statut

Implementation Planning

## Objectif

Définir précisément l'implémentation frontend nécessaire pour transformer la page Profiles en véritable écran métier.

Aucun développement n'est réalisé pendant cette étape.

L'objectif est de préparer une implémentation frontend propre, cohérente avec Opportunities et compatible avec les APIs backend déjà disponibles.

## Résultat attendu

À la fin de l'implémentation :

L'utilisateur pourra :

- consulter ses profils ;
- sélectionner un profil ;
- consulter les informations générales ;
- consulter les compétences ;
- consulter les expériences ;
- consulter les langues ;
- consulter les certifications.

Aucune modification de données n'est prévue.

## Décision d'architecture

Le modèle retenu est :

Master / Detail

déjà utilisé dans :

Opportunities

pour conserver une cohérence UX dans l'ensemble de l'application.

## Structure cible

Profiles Page

├── Profile List
└── Profile Detail

### Colonne gauche

Responsabilités :

- liste des profils ;
- changement du profil sélectionné ;
- indication visuelle du profil actif.

### Colonne droite

Responsabilités :

- informations générales ;
- KPIs ;
- compétences ;
- expériences ;
- langues ;
- certifications.

## Fichiers à modifier

### 1. frontend/src/services/api.ts

Ajouter :

getProfile(profileId)

getProfileSkills(profileId)

getSkills()

getProfileWorkExperiences(profileId)

getLanguages()

getProfileLanguages(profileId)

getCertifications()

getProfileCertifications(profileId)

Objectif :

Consommer les endpoints déjà disponibles côté backend.

Aucun endpoint backend supplémentaire.

## 2. frontend/src/components/ProfileList.tsx

Ajouter :

selectedProfileId

onSelectProfile

Objectif :

Transformer la liste actuelle en composant de navigation.

Ajouter :

- état actif ;
- mise en évidence visuelle ;
- comportement similaire à Opportunities.

## 3. frontend/src/pages/ProfilesPage.tsx

Transformer le placeholder actuel en page métier.

Responsabilités :

- charger les profils ;
- sélectionner automatiquement le premier profil ;
- charger les données du profil sélectionné ;
- afficher le layout master/detail ;
- gérer le loading ;
- gérer les erreurs ;
- gérer les états vides.

## Fichiers à créer

### 1. frontend/src/components/ProfileDetail.tsx

Responsabilité :

Assembler les différentes sections du profil.

Contenu :

- Header profil ;
- KPIs ;
- Skills ;
- Experience ;
- Languages ;
- Certifications.

## 2. frontend/src/components/ProfileSkillsSection.tsx

Responsabilité :

Afficher les compétences du profil.

Présentation :

Liste de badges.

## 3. frontend/src/components/ProfileExperienceSection.tsx

Responsabilité :

Afficher les expériences professionnelles.

Présentation :

Cards chronologiques.

Ordre :

Plus récente → plus ancienne.

## 4. frontend/src/components/ProfileLanguagesSection.tsx

Responsabilité :

Afficher les langues.

Présentation :

Card simple.

Format :

Language
Proficiency

## 5. frontend/src/components/ProfileCertificationsSection.tsx

Responsabilité :

Afficher les certifications.

Présentation :

Cards.

## Structure visuelle détaillée

Page Header

↓

Profile KPI Summary

↓

General Information Card

↓

Skills Card

↓

Experience Card

↓

Languages Card

↓

Certifications Card

## KPIs à calculer

Les KPIs sont calculés côté frontend.

Aucune logique métier.

Afficher :

Skills

Experiences

Languages

Certifications

Exemple :

Skills: 24

Experiences: 6

Languages: 3

Certifications: 2

## Mapping de données

### Skills

Source :

GET /profiles/{profile_id}/skills

-

GET /skills

Transformation :

skill_id

↓

skill.name

## Languages

Source :

GET /profiles/{profile_id}/languages

-

GET /languages

Transformation :

language_id

↓

language.name

## Certifications

Source :

GET /profiles/{profile_id}/certifications

-

GET /certifications

Transformation :

certification_id

↓

certification.name

## États UI

### Loading profils

Afficher :

Loading profiles...

### Loading détail

Afficher :

Loading profile details...

### Aucun profil

Afficher :

No profiles available.

### Aucun skill

Afficher :

No skills available.

### Aucune expérience

Afficher :

No experience available.

### Aucune langue

Afficher :

No languages available.

### Aucune certification

Afficher :

No certifications available.

### Erreur

Afficher :

Unable to load profiles.

## Réutilisation des composants UI

Réutiliser uniquement :

- Card
- PageHeader
- Section
- StatCard

Aucune nouvelle librairie.

Aucune modification du design system.

## Validation technique attendue

Build :

npm run build

Résultat attendu :

Build réussi.

## Validation fonctionnelle attendue

Ouvrir :

Profiles

Résultat attendu :

- liste visible ;
- sélection visible ;
- détail visible ;
- KPIs visibles ;
- compétences visibles ;
- expériences visibles ;
- langues visibles ;
- certifications visibles.

## Critères de succès

Phase terminée lorsque :

- toutes les données sont visibles ;
- aucun endpoint backend n'a été modifié ;
- build frontend valide ;
- validation visuelle réalisée ;
- cohérence visuelle avec Opportunities validée.

## Hors périmètre

Ne pas implémenter :

- création de profil ;
- modification de profil ;
- suppression de profil ;
- édition des compétences ;
- édition des langues ;
- édition des certifications ;
- import CV ;
- import LinkedIn ;
- fonctionnalités IA.

## Livrable

docs/profile-management-visualization-implementation-plan.md

## Étape suivante recommandée

Phase 7.1.13.4

Profile Management Visualization Repository Audit

Objectif :

Vérifier que chaque fichier prévu existe, que le découpage est cohérent et qu'aucune simplification n'est possible avant le développement.
