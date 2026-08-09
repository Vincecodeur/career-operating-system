# AI Explanation Frontend Implementation Plan

## Phase

7.1.10 AI Explanation Frontend Technical Implementation Plan

## Statut

Design

## Contexte

Le backend contient désormais :

- AIExplanation schemas
- AIProvider interface
- PromptBuilder
- MockAIProvider
- AIExplanationService

Les tests backend sont validés.

Le frontend dispose déjà :

- OpportunitiesPage
- Opportunity Detail Panel
- Matching Analysis
- Opportunity Analysis
- AI Recommendations Placeholder

Les documents précédents ont défini :

- AI Explanation Frontend Integration Design
- règles d'intégration UI
- règles de fallback
- contrat cible

Cette phase définit précisément les fichiers à modifier et l'ordre d'implémentation avant tout développement frontend.

Aucun code ne doit être produit pendant cette phase.

## Objectif

Définir :

- les fichiers exacts à modifier ;
- les fichiers exacts à créer ;
- l'ordre des changements ;
- les validations attendues ;
- les tests attendus ;
- les critères de fin.

## Principe fondamental

Le frontend reste une couche d'affichage.

Toute logique métier reste côté backend.

Le frontend affiche :

- score ;
- verdict ;
- recommendation ;
- summary ;
- ai_explanation.

Le frontend ne génère jamais d'explication IA.

## Hypothèse MVP

Le backend exposera prochainement :

ai_explanation

dans la réponse utilisée par OpportunitiesPage.

L'implémentation frontend doit rester compatible avec :

ai_explanation = null

## Étape 1

Audit du contrat API réel

Objectif :

Confirmer le type réellement utilisé dans :

- OpportunitiesPage
- API client
- Matching Result

À vérifier :

- type TypeScript actuel
- propriété contenant opportunity_analysis
- structure exacte du payload

Critère de validation :

Structure documentée.

Aucun code.

## Étape 2

Adaptation des types TypeScript

Fichier probable :

frontend/src/types/api.ts

Objectif :

Ajouter :

AIExplanation

et

ai_explanation

dans les types appropriés.

Validation :

- build TypeScript passe
- aucune régression de type

## Étape 3

Création du composant

Fichier à créer :

frontend/src/components/AIExplanationCard.tsx

Responsabilité :

Affichage uniquement.

Props :

- explanation
- isLoading
- error

Validation :

Composant compilable.

Aucune logique métier.

## Étape 4

Création du Skeleton

Fichier à créer :

frontend/src/components/AIExplanationCardSkeleton.tsx

Responsabilité :

Afficher l'état loading.

Validation :

Affichage cohérent avec les autres composants.

## Étape 5

Intégration dans OpportunitiesPage

Fichier à modifier :

frontend/src/pages/OpportunitiesPage.tsx

Objectif :

Afficher AIExplanationCard après Opportunity Analysis.

Ordre attendu :

Opportunity Metadata

↓

Matching Analysis

↓

Opportunity Analysis

↓

AI Explanation

↓

Source Offer

Validation :

Position correcte.

## Étape 6

Gestion fallback

Implémenter :

- ai_explanation undefined
- ai_explanation null
- action_plan vide

Validation :

Aucune erreur React.

## Étape 7

Gestion erreurs

Afficher :

Unable to display AI explanation.

Ne jamais afficher :

- stack trace
- erreur provider
- erreur backend brute

Validation :

Message utilisateur contrôlé.

## Étape 8

Validation fonctionnelle

Scénario 1

ai_explanation disponible

Résultat attendu :

- Summary visible
- Detailed explanation visible
- Action plan visible

Scénario 2

ai_explanation null

Résultat attendu :

No AI explanation available.

Scénario 3

action_plan vide

Résultat attendu :

Section masquée.

Scénario 4

aucune régression OpportunitiesPage.

## Étape 9

Validation frontend

Vérifier :

- affichage score
- affichage verdict
- affichage recommendation
- affichage summary
- affichage ai explanation

Validation visuelle obligatoire.

## Étape 10

Audit de cohérence

Vérifier :

- backend
- frontend
- roadmap
- project-status
- handoff

Toujours alignés.

## Fichiers potentiellement créés

frontend/src/components/AIExplanationCard.tsx

frontend/src/components/AIExplanationCardSkeleton.tsx

## Fichiers potentiellement modifiés

frontend/src/types/api.ts

frontend/src/pages/OpportunitiesPage.tsx

## Tests attendus

Minimum :

- rendu avec explication
- rendu sans explication
- rendu avec erreur
- rendu loading

Si aucun framework frontend test n'est en place :

validation manuelle obligatoire.

## Critères de fin

La phase sera terminée lorsque :

- AIExplanationCard existe ;
- AIExplanationCardSkeleton existe ;
- contrat TypeScript mis à jour ;
- OpportunitiesPage intégrée ;
- fallback validé ;
- validation visuelle réalisée ;
- build frontend valide ;
- documentation synchronisée ;
- commit technique réalisé ;
- commit documentaire réalisé ;
- git status propre.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- appels LLM ;
- streaming ;
- chat IA ;
- feedback utilisateur ;
- historique ;
- régénération ;
- nouvelle page IA.

## Livrable

- docs/ai-explanation-frontend-implementation-plan.md

## Étape suivante recommandée

Phase 7.1.11

AI Explanation Frontend Repository Review

Objectif :

Analyser les fichiers réels du frontend et identifier exactement où intégrer AIExplanation avant de générer la moindre ligne de code.
