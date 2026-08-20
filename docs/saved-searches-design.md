# Saved Searches Design

## Phase

7.1.21 Saved Searches

## Status

Product Design

---

# Objectif

Permettre à l'utilisateur de sauvegarder des configurations de recherche d'opportunités afin de retrouver rapidement des critères fréquemment utilisés.

Saved Searches est une fonctionnalité métier distincte :

- des Search Criteria Settings ;
- des Discovery Preferences ;
- du contexte de profil actif.

Une Saved Search représente un instantané des filtres actuellement appliqués dans Opportunities.

---

# Problème utilisateur

Aujourd'hui :

- l'utilisateur configure plusieurs filtres ;
- l'utilisateur quitte la page ;
- les filtres sont perdus ;
- l'utilisateur doit les reconstruire manuellement.

Exemples :

- Technical Partnerships France
- Solution Architect Remote
- UAE Marketplace Opportunities
- Not Applied Opportunities
- High Match Opportunities

Le système doit permettre de réutiliser ces recherches rapidement.

---

# Périmètre MVP

Le MVP permet :

- créer une recherche sauvegardée ;
- afficher les recherches sauvegardées ;
- appliquer une recherche sauvegardée ;
- supprimer une recherche sauvegardée ;
- conserver les recherches en PostgreSQL.

Le MVP ne permet pas :

- partage ;
- alertes ;
- exécution automatique ;
- favoris ;
- tags ;
- dossiers ;
- historique ;
- statistiques ;
- exécution planifiée.

---

# Concepts Métier

## Discovery Preferences

Les Discovery Preferences définissent le comportement global du système :

- Opportunity Age Window
- Minimum Matching Score
- Default Opportunity Sort

Elles sont persistées dans Settings.

Elles ne font pas partie d'une Saved Search.

---

## Search Criteria Settings

Les Search Criteria définissent les préférences globales de découverte :

- Target Job Titles
- Preferred Countries
- Work Modes
- Included Keywords
- Excluded Keywords

Elles sont persistées dans Settings.

Elles ne font pas partie d'une Saved Search.

---

## Saved Search

Une Saved Search représente :

- un nom ;
- un ensemble de filtres Opportunities ;
- un ordre de tri.

Une Saved Search est persistée indépendamment.

---

# Données sauvegardées

## Name

Type :

string

Obligatoire :

Oui

Exemples :

- Technical Partnerships France
- UAE Remote Jobs
- High Match Opportunities

---

## Keyword

Type :

string

Obligatoire :

Non

Exemples :

- partnerships
- architect
- marketplace

---

## Application Status

Type :

enum

Valeurs :

- ALL
- APPLIED
- NOT_APPLIED

Obligatoire :

Oui

---

## Source

Type :

string

Valeurs possibles :

- ALL
- France Travail
- LinkedIn
- Greenhouse
- autres sources futures

Obligatoire :

Oui

---

## Location

Type :

string

Valeurs possibles :

- ALL
- Paris
- London
- Remote
- autres localisations

Obligatoire :

Oui

---

## Sort By

Type :

enum

Valeurs :

- BEST_MATCH_FIRST
- NEWEST_FIRST
- OLDEST_FIRST
- APPLIED_FIRST
- NOT_APPLIED_FIRST

Obligatoire :

Oui

---

# Données non sauvegardées

Les éléments suivants ne sont volontairement pas stockés :

- contexte de profil actif ;
- profil sélectionné ;
- Discovery Preferences ;
- Search Criteria Settings ;
- résultat de recherche ;
- matching score ;
- nombre d'opportunités trouvées.

Ces informations peuvent évoluer indépendamment.

---

# Règles métier

## Création

L'utilisateur peut créer une Saved Search à partir des filtres actuellement visibles.

Les valeurs courantes de recherche sont copiées dans la Saved Search.

---

## Application

L'application d'une Saved Search :

- remplace tous les filtres actuels ;
- applique le tri sauvegardé ;
- recharge l'affichage Opportunities.

Aucune opportunité n'est modifiée.

---

## Suppression

La suppression :

- retire la Saved Search ;
- ne retire aucune opportunité ;
- ne modifie aucune candidature ;
- ne modifie aucun paramètre global.

---

## Nom

Le nom est obligatoire.

Le système refuse :

- chaîne vide ;
- uniquement des espaces.

Les doublons sont autorisés dans le MVP.

---

# UX MVP

## Opportunities

Ajout d'une section :

Saved Searches

---

Exemple :

[Save Search]

Saved Searches

Technical Partnerships France
[Apply] [Delete]

UAE Marketplace Opportunities
[Apply] [Delete]

High Match Opportunities
[Apply] [Delete]

---

# Save Search Dialog

Titre :

Save Current Search

Champs :

Name

Résumé affiché :

Keyword:
partnerships

Application Status:
NOT_APPLIED

Source:
France Travail

Location:
Paris

Sort:
BEST_MATCH_FIRST

Actions :

[Cancel]

[Save Search]

---

# Apply Search

Comportement :

L'utilisateur clique :

Apply

Le système :

- recharge les filtres ;
- applique le tri ;
- met à jour immédiatement la liste.

Aucune confirmation n'est nécessaire.

---

# Delete Search

Comportement :

L'utilisateur clique :

Delete

Confirmation :

Delete Saved Search ?

This action cannot be undone.

[Cancel]

[Delete]

---

# Architecture

La persistance est réalisée côté backend.

Les Saved Searches sont stockées en PostgreSQL.

Le frontend ne stocke aucune recherche dans localStorage.

---

# Principes d'architecture

Saved Searches est :

- une donnée métier ;
- persistée ;
- indépendante du navigateur.

Saved Searches n'est pas :

- un cache ;
- une préférence frontend ;
- une donnée temporaire.

---

# Hors MVP

## Alertes

Exemple :

Notify me when new opportunities match this search.

Reporté.

---

## Exécution automatique

Exemple :

Run every day.

Reporté.

---

## Favoris

Exemple :

Pinned Saved Searches.

Reporté.

---

## Tags

Exemple :

Marketplace
Architecture
Management

Reporté.

---

## Dossiers

Exemple :

EMEA
France
Remote

Reporté.

---

## Statistiques

Exemple :

25 matching opportunities.

Reporté.

---

# Critères de validation

Le MVP est considéré terminé lorsque :

- une Saved Search peut être créée ;
- une Saved Search peut être affichée ;
- une Saved Search peut être appliquée ;
- une Saved Search peut être supprimée ;
- les données sont persistées en PostgreSQL ;
- le build frontend est validé ;
- la validation fonctionnelle est réalisée ;
- la documentation est synchronisée.

---

# Décisions Produit

Décision :

Saved Searches est un domaine métier persistant.

Motivation :

Alignement avec :

- Settings ;
- Search Criteria ;
- Applications ;
- Profils.

Le stockage localStorage est rejeté afin de préserver la cohérence architecturale.

---

# Résultat attendu

L'utilisateur doit pouvoir :

1. Construire une recherche.
2. La sauvegarder.
3. La retrouver ultérieurement.
4. La réappliquer en un clic.
5. Reprendre son analyse sans reconfigurer les filtres.
