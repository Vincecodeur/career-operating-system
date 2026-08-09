# Profile Management Visualization Design

## Phase

7.1.13.1 Profile Management Visualization Design

## Statut

Design

## Contexte

Le backend contient déjà les domaines suivants :

- Profile
- Skill
- ProfileSkill
- WorkExperience
- Language
- ProfileLanguage
- Certification
- ProfileCertification

Les APIs existent.

Les données existent.

La logique métier existe.

Cependant la page frontend Profiles est actuellement un placeholder.

Dans l'état actuel du produit :

- Dashboard est utilisable
- Opportunities est avancée
- Account est minimale
- Profiles est vide
- Applications est vide
- Settings est vide

Le moteur de matching repose sur le profil candidat mais ce profil n'est actuellement pas visible dans l'interface utilisateur.

Cela crée une rupture dans la compréhension du système.

## Problème

Aujourd'hui l'utilisateur voit :

Opportunité
↓
Matching
↓
Analyse
↓
AI Explanation

Mais il ne voit pas clairement :

Profil
↓
Compétences
↓
Expériences
↓
Certifications
↓
Langues

qui alimentent le moteur de matching.

Le système paraît donc partiellement opaque.

## Objectif

Transformer Profiles en véritable page métier.

Permettre à l'utilisateur de consulter la source de vérité utilisée par le système.

Créer une expérience cohérente avec Opportunities.

## Principe directeur

Le profil candidat est la source de vérité du système.

Toutes les analyses, scores, recommandations et explications doivent pouvoir être reliées visuellement aux données du profil.

## Objectifs utilisateurs

Permettre de :

- consulter un profil ;
- comprendre les compétences connues ;
- comprendre les expériences connues ;
- comprendre les langues connues ;
- comprendre les certifications connues ;
- visualiser rapidement la richesse du profil.

Aucune édition n'est prévue dans cette phase.

## Hors périmètre

Ne pas implémenter :

- modification de profil ;
- upload de CV ;
- import LinkedIn ;
- génération IA ;
- édition des compétences ;
- édition des expériences ;
- création d'un profil ;
- suppression d'un profil ;
- gestion documentaire ;
- versioning du profil.

## Vision UX

Le pattern principal doit être identique à Opportunities.

L'utilisateur connaît déjà :

Liste
↓
Détail

Cette logique doit être réutilisée.

## Architecture cible

Profiles Page

├── Profile List
└── Profile Detail

## Layout principal

Desktop

+-----------------------+----------------------------------+
| | |
| Profile List | Profile Detail |
| | |
| Vincent | General Information |
| Profile 2 | Skills |
| Profile 3 | Experience |
| | Languages |
| | Certifications |
| | |
+-----------------------+----------------------------------+

## Responsabilités de la colonne gauche

Afficher :

- profils disponibles ;
- profil sélectionné ;
- changement de profil.

Ne jamais afficher de logique métier.

## Responsabilités du panneau droit

Afficher :

- informations générales ;
- compétences ;
- expériences ;
- langues ;
- certifications.

## Page Header

Titre :

Profiles

Description :

Manage candidate profiles.

## KPIs de profil

Afficher en haut du panneau détail :

Skills

Experiences

Languages

Certifications

Exemple :

Skills: 24

Experiences: 8

Languages: 3

Certifications: 4

Objectif :

Vision rapide du profil.

## Section General Information

Afficher :

- Full Name
- Email
- Location
- Headline
- LinkedIn URL si disponible

Présentation :

Card dédiée.

## Section Skills

Afficher :

Liste des compétences.

Format :

Badges.

Exemple :

Python
FastAPI
Azure
PostgreSQL
React

## Organisation Skills

Compétences triées alphabétiquement.

Aucune pondération affichée.

Aucune notion de score.

## Section Work Experience

Afficher :

- Job Title
- Company
- Start Date
- End Date
- Description

Ordre :

Plus récente → plus ancienne.

## Section Languages

Afficher :

- Language
- Proficiency

Exemple :

French - Native

English - Professional

Portuguese - Intermediate

## Section Certifications

Afficher :

- Certification Name
- Issuer
- Date

## Cartes UI réutilisées

Réutiliser :

- Card
- PageHeader
- Section
- StatCard

Aucune nouvelle librairie.

Aucun nouveau design system.

## API Strategy

Réutiliser l'API existante.

Ne créer aucun endpoint spécifique.

Le frontend consomme les endpoints déjà disponibles.

## Loading State

Afficher :

Loading profiles...

et

Loading profile...

Aucune animation complexe.

## Empty State

Cas :

Aucun profil.

Afficher :

No profiles available.

## Error State

Cas :

Erreur API.

Afficher :

Unable to load profiles.

## Responsive

Desktop :

Master / Detail.

Tablet :

Master / Detail.

Mobile futur :

Hors périmètre.

## Navigation

Le changement de profil doit :

- conserver la page ;
- mettre à jour le panneau détail ;
- rester instantané.

## Accessibilité

Respecter :

- navigation clavier ;
- contraste AA ;
- ordre logique de lecture ;
- titres hiérarchiques.

## Cohérence produit

Après implémentation :

Le parcours utilisateur devient :

Profile
↓
Opportunities
↓
Matching
↓
Opportunity Analysis
↓
AI Explanation

Le système devient plus compréhensible.

## Composants frontend prévus

Probablement :

ProfileList

ProfileDetailCard

ProfileSkillsSection

ProfileExperienceSection

ProfileLanguagesSection

ProfileCertificationsSection

Les noms exacts seront validés pendant la revue repository.

## Structure visuelle cible

Page Header

↓

Profile KPI Summary

↓

General Information

↓

Skills

↓

Experience

↓

Languages

↓

Certifications

## Validation fonctionnelle attendue

L'utilisateur ouvre Profiles.

↓

La liste des profils apparaît.

↓

Un profil est sélectionné.

↓

Les informations générales apparaissent.

↓

Les compétences apparaissent.

↓

Les expériences apparaissent.

↓

Les langues apparaissent.

↓

Les certifications apparaissent.

↓

Aucune erreur visuelle.

## Critères de validation

Cette phase est terminée lorsque :

- architecture définie ;
- layout défini ;
- composants définis ;
- stratégie API définie ;
- états loading définis ;
- états erreur définis ;
- responsive défini ;
- critères de validation définis.

Aucun code produit.

## Livrable

docs/profile-management-visualization-design.md

## Étape suivante recommandée

Phase 7.1.13.2

Profile Management Visualization Review

Objectif :

Relire la conception et vérifier son alignement avec les APIs backend existantes avant toute implémentation frontend.
