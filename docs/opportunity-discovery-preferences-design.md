# Opportunity Discovery Preferences Design

## Phase

7.1.19.7.1 Product Design

## Objective

Permettre à l'utilisateur de personnaliser la manière dont les opportunités sont présentées dans l'application.

Cette phase ne modifie pas :

- les critères métier ;
- le moteur de matching ;
- le moteur de ranking ;
- les sources ;
- les profils.

Cette phase introduit uniquement des préférences de découverte et de visualisation.

---

# Business Context

Le système dispose déjà de :

- Job Discovery Settings ;
- Search Criteria Settings ;
- Source Configuration ;
- Opportunity Context Selection ;
- Multi Profile Opportunity Scoring.

Les critères métier permettent déjà de définir :

- ce qui est recherché ;
- dans quels pays ;
- selon quels mots-clés ;
- selon quels modes de travail.

Il manque cependant la possibilité de définir comment les résultats doivent être affichés.

---

# Design Principles

## Principle 1

Séparer :

Search Criteria

et

Discovery Preferences

Search Criteria définissent :

ce que l'utilisateur recherche.

Discovery Preferences définissent :

comment l'utilisateur souhaite voir les résultats.

---

## Principle 2

Les préférences doivent avoir une valeur immédiate.

Contrairement à Application Workflow Strategy Visualization, chaque option introduite dans cette phase doit être réellement utilisable.

---

## Principle 3

Le matching continue d'appartenir au backend.

Le frontend ne calcule aucun score.

---

## Principle 4

La simplicité prime.

Aucune IA.

Aucune automation avancée.

Aucune logique prédictive.

---

# Preference 1

## Opportunity Age Window

### Purpose

Limiter les opportunités affichées selon leur ancienneté.

Certaines opportunités deviennent peu pertinentes après plusieurs semaines.

Cette préférence permet de réduire le bruit.

### Setting Name

Opportunity Age Window

### Available Values

Last 7 Days

Last 14 Days

Last 30 Days

Last 90 Days

All Opportunities

### Default Value

Last 30 Days

### Example

Current Date
↓
20 August

Value

Last 30 Days

Displayed Opportunities

Only opportunities published during the last 30 days.

### User Value

- moins de bruit ;
- opportunités plus récentes ;
- meilleure prise de décision.

---

# Preference 2

## Minimum Matching Score

### Purpose

Masquer automatiquement les opportunités jugées peu pertinentes.

### Setting Name

Minimum Matching Score

### Available Values

0

25

50

75

### Default Value

25

### Example

Opportunity A

Score 82

Visible

Opportunity B

Score 64

Visible

Opportunity C

Score 18

Hidden

### User Value

- moins d'offres peu pertinentes ;
- meilleure concentration ;
- réduction du volume à traiter.

---

# Preference 3

## Archived Opportunities Visibility

### Purpose

Définir si les opportunités archivées doivent être visibles.

### Setting Name

Archived Opportunities Visibility

### Available Values

Hide Archived Opportunities

Show Archived Opportunities

### Default Value

Hide Archived Opportunities

### Example

Hide Archived Opportunities

↓

Only active opportunities displayed.

### User Value

- interface plus propre ;
- focalisation sur les actions utiles.

---

# Preference 4

## Default Opportunity Sort

### Purpose

Définir l'ordre de tri initial des opportunités.

### Setting Name

Default Opportunity Sort

### Available Values

Best Match First

Newest First

Oldest First

### Default Value

Best Match First

### Example

Best Match First

↓

82
75
63
41
18

### User Value

- personnalisation de l'expérience utilisateur ;
- accès plus rapide aux opportunités importantes.

---

# User Experience

## Settings Location

Settings

↓

Opportunity Discovery Preferences

Nouvelle section dédiée.

Cette section est indépendante :

- des Job Discovery Settings ;
- des Search Criteria Settings ;
- des Source Configuration Settings.

---

# High Level Wireframe

Settings

---

Job Discovery Settings

---

Search Criteria Settings

---

Source Configuration

---

Opportunity Discovery Preferences

Opportunity Age Window
[ Last 30 Days ▼ ]

Minimum Matching Score
[ 25 ▼ ]

Archived Opportunities Visibility
(●) Hide
( ) Show

Default Opportunity Sort
(●) Best Match First
( ) Newest First
( ) Oldest First

[ Save Preferences ]

---

---

# Backend Ownership

Toutes les préférences sont stockées côté backend.

Le backend :

- applique les préférences ;
- réalise les filtrages ;
- applique le tri initial.

Le frontend :

- affiche ;
- modifie ;
- sauvegarde.

---

# Interaction With Existing Features

## Search Criteria Settings

Aucune interaction directe.

Search Criteria :

détermine quelles opportunités sont récupérées.

Discovery Preferences :

détermine quelles opportunités sont affichées.

---

## Matching

Aucune modification.

Le calcul du score reste identique.

---

## Opportunity Context Selection

Aucune modification.

Le profil actif reste utilisé pour :

- scoring ;
- ranking ;
- affichage des cartes.

---

# Out Of Scope

Cette phase ne couvre pas :

- LinkedIn redesign ;
- alertes email ;
- notifications ;
- matching weights ;
- IA ;
- recommandations IA ;
- auto-application ;
- sauvegarde de recherches ;
- persistance du contexte actif ;
- gestion multi-profils actifs.

---

# Related Future Work

APP-005

Best Matching Profile Preselection

---

7.1.21

Saved Searches

---

7.1.22

Multi Profile Opportunity Context

---

TECH-001

Frontend Bundle Optimization

---

# Success Criteria

La phase est réussie lorsque :

- les préférences sont définies ;
- les comportements sont documentés ;
- les valeurs par défaut sont validées ;
- l'expérience utilisateur est validée ;
- le périmètre est figé ;
- les interactions avec les fonctionnalités existantes sont clarifiées.

---

# Design Conclusion

Opportunity Discovery Preferences permettent à l'utilisateur de contrôler la visibilité et la présentation des opportunités sans modifier les règles métier.

Le matching reste inchangé.

Le ranking reste inchangé.

Les préférences améliorent la lisibilité et la prise de décision tout en conservant une architecture simple et cohérente avec les principes MVP du projet.
