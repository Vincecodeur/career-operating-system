# AI Explanation Frontend Technical Design

## Phase

7.1.10 AI Explanation Frontend Technical Design

## Statut

Design

## Contexte

La phase précédente a défini l'intégration fonctionnelle frontend de l'AI Explanation Layer.

Le backend dispose déjà d'un socle IA local et déterministe :

- AIExplanation schemas
- AIProvider interface
- PromptBuilder
- MockAIProvider
- AIExplanationService
- tests IA

La valeur backend n'est pas encore visible dans l'interface utilisateur.

L'objectif de cette phase est de définir précisément les adaptations frontend nécessaires avant toute implémentation React.

Aucun code frontend ne doit être produit pendant cette phase.

Aucun fournisseur IA réel ne doit être intégré.

Aucun appel OpenAI ou Azure OpenAI ne doit être implémenté.

Aucun appel LLM réel ne doit être réalisé.

## Objectif

Définir précisément :

- les types TypeScript ;
- les adaptations du client API ;
- les composants React à créer ;
- les composants existants à modifier ;
- les états UI ;
- les règles de fallback ;
- les tests frontend attendus ;
- les critères de validation visuelle.

## Principe fondamental

Le frontend affiche les explications IA.

Le frontend ne génère jamais les explications IA.

Le frontend ne calcule jamais :

- score ;
- verdict ;
- recommendation ;
- strengths ;
- weaknesses ;
- action plan.

Toute logique métier reste dans le backend.

## Scope frontend

Inclus :

- définition des types TypeScript ;
- définition du composant AIExplanationCard ;
- intégration dans OpportunitiesPage ;
- affichage summary ;
- affichage detailed_explanation ;
- affichage action_plan ;
- fallback si ai_explanation = null ;
- état loading ;
- état error ;
- validation visuelle.

Exclus :

- appel LLM ;
- OpenAI ;
- Azure OpenAI ;
- génération côté frontend ;
- stockage local des explications ;
- modification du moteur de matching ;
- nouvelle page dédiée ;
- chat IA ;
- régénération d'explication.

## Contrat API attendu

Le frontend doit accepter une structure enrichie contenant :

ai_explanation

Exemple conceptuel :

{
"score": 78,
"strengths": [],
"weaknesses": [],
"opportunity_analysis": {},
"ai_explanation": {
"summary": "...",
"detailed_explanation": "...",
"action_plan": [
"...",
"..."
],
"provider_name": "mock",
"model_name": "mock-ai-explanation-model",
"prompt_version": "score_explanation_v1"
}
}

## Cas ai_explanation null

Le frontend doit accepter :

{
"ai_explanation": null
}

comme un cas normal.

Ce cas ne doit pas être traité comme une erreur technique.

## Type TypeScript cible

Créer un type :

AIExplanation

Champs :

- summary
- detailed_explanation
- action_plan
- provider_name
- model_name
- prompt_version

## Définition conceptuelle

type AIExplanation = {
summary: string
detailed_explanation: string
action_plan: string[]
provider_name: string
model_name: string
prompt_version: string
}

## Intégration dans les types existants

Le type représentant l'analyse ou le matching doit être enrichi avec :

ai_explanation?: AIExplanation | null

La propriété doit être optionnelle ou nullable pour conserver la compatibilité avec les réponses existantes.

## Fichiers probablement concernés

frontend/src/types/api.ts

frontend/src/pages/OpportunitiesPage.tsx

frontend/src/components/AIExplanationCard.tsx

frontend/src/components/AIExplanationCardSkeleton.tsx

Le nom exact des dossiers devra être confirmé dans le repository avant implémentation.

## Nouveau composant principal

Nom :

AIExplanationCard

Responsabilité :

Afficher une explication IA.

Le composant ne doit pas appeler l'API.

Le composant ne doit pas calculer de logique métier.

Le composant reçoit uniquement des props.

## Props attendues

AIExplanationCardProps

Champs :

- explanation
- isLoading
- error

## Définition conceptuelle

type AIExplanationCardProps = {
explanation?: AIExplanation | null
isLoading?: boolean
error?: string | null
}

## Comportement du composant

### Cas loading

Si isLoading = true :

Afficher :

AIExplanationCardSkeleton

### Cas error

Si error non null :

Afficher un message simple :

Unable to display AI explanation.

### Cas explanation null

Si explanation = null :

Afficher :

No AI explanation available.

### Cas explanation disponible

Afficher :

- summary
- detailed_explanation
- action_plan

## Structure UI cible

Card

Titre :

AI Explanation

Sous-sections :

1. Summary
2. Detailed explanation
3. Action plan

## Section Summary

Afficher :

explanation.summary

Rôle :

lecture rapide.

## Section Detailed Explanation

Afficher :

explanation.detailed_explanation

Rôle :

compréhension détaillée.

## Section Action Plan

Afficher :

explanation.action_plan

Format :

liste à puces.

Si action_plan est vide :

ne pas afficher la section Action Plan.

## Métadonnées techniques

Décision MVP :

ne pas afficher dans l'interface :

- provider_name
- model_name
- prompt_version

Raison :

ces informations sont utiles pour l'audit backend, mais ne sont pas utiles à l'utilisateur final dans le MVP.

## Placement dans OpportunitiesPage

Position cible dans le panneau de détail :

Opportunity Metadata

↓

Matching Analysis

↓

Opportunity Analysis

↓

AI Explanation

↓

Source Offer Link

## Raison du placement

L'utilisateur doit d'abord voir :

- les données principales de l'offre ;
- le score ;
- l'analyse déterministe ;
- puis l'explication IA.

L'IA reste complémentaire.

Elle ne doit pas être affichée avant le score déterministe.

## Data flow cible

User selects opportunity

↓

OpportunitiesPage loads selected offer details

↓

Matching / Opportunity Analysis data is available

↓

ai_explanation is read from response

↓

AIExplanationCard renders state

## API call strategy

Décision MVP :

aucun appel API dédié.

Le frontend consomme ai_explanation depuis la réponse existante.

Raison :

- simplicité ;
- pas de nouveau endpoint ;
- pas de complexité React Query supplémentaire ;
- cohérence avec la phase MVP.

## React Query

Aucun nouveau query hook dédié dans cette phase.

L'explication IA doit être intégrée dans le payload existant.

Si le payload existant n'inclut pas encore ai_explanation, l'implémentation backend/API devra être adaptée avant ou pendant la phase de code.

## Fallback strategy

Le frontend doit rester robuste si :

- ai_explanation absent ;
- ai_explanation null ;
- action_plan vide ;
- summary vide ;
- detailed_explanation vide.

Cependant les champs vides devraient normalement être filtrés côté backend.

## UI fallback cases

### Case 1

ai_explanation undefined

Afficher :

No AI explanation available.

### Case 2

ai_explanation null

Afficher :

No AI explanation available.

### Case 3

action_plan empty

Ne pas afficher la section Action Plan.

### Case 4

frontend rendering error

Afficher :

Unable to display AI explanation.

## Loading state

Le chargement doit être cohérent avec les autres blocs de OpportunitiesPage.

AIExplanationCardSkeleton doit afficher une structure visuelle simple.

Aucune animation complexe.

## Skeleton design

Afficher :

- ligne de titre
- bloc résumé
- 3 lignes de contenu
- 3 lignes action plan

## Error state

Message court :

Unable to display AI explanation.

Ne pas afficher :

- stack trace ;
- erreur provider ;
- erreur backend interne.

## Empty state

Message :

No AI explanation available.

Ce message ne doit pas être alarmant.

## Accessibility

Le composant doit respecter :

- titres structurés ;
- listes HTML pour action_plan ;
- contraste suffisant ;
- navigation clavier ;
- texte lisible.

## Design System

Réutiliser les composants existants :

- Card
- Section
- PageHeader si nécessaire

Ne pas introduire :

- nouvelle librairie UI ;
- nouveau système de design ;
- nouvelle dépendance.

## Styling

Le style doit rester cohérent avec :

- OpportunitiesPage ;
- Matching Analysis ;
- Opportunity Analysis ;
- Dashboard cards.

Le composant doit être sobre.

L'IA ne doit pas visuellement dominer les éléments déterministes.

## UX Copy

Titre :

AI Explanation

Summary label :

Summary

Detailed explanation label :

Detailed explanation

Action plan label :

Action plan

Fallback :

No AI explanation available.

Error :

Unable to display AI explanation.

## Langue MVP

Anglais uniquement.

Le support français est hors périmètre de cette phase.

## Tests frontend attendus

Si l'environnement de test frontend est déjà disponible :

- AIExplanationCard renders summary
- AIExplanationCard renders detailed explanation
- AIExplanationCard renders action plan
- AIExplanationCard hides empty action plan
- AIExplanationCard renders fallback when null
- AIExplanationCard renders error state
- AIExplanationCard renders loading skeleton

Si les tests frontend ne sont pas encore structurés :

validation manuelle obligatoire.

## Validation manuelle attendue

Scénario 1 :

Sélectionner une opportunité avec ai_explanation disponible.

Résultat attendu :

AI Explanation visible.

Scénario 2 :

Sélectionner une opportunité avec ai_explanation null.

Résultat attendu :

Fallback visible.

Scénario 3 :

Vérifier que le score déterministe reste visible avant l'explication IA.

Résultat attendu :

Score visible.

AI Explanation affichée après Opportunity Analysis.

Scénario 4 :

Vérifier qu'aucune erreur console n'apparaît.

Résultat attendu :

Aucune erreur bloquante.

## Dépendances backend

Le frontend dépend d'un payload API contenant :

ai_explanation

Si ce champ n'existe pas encore dans l'API réelle, l'étape d'implémentation devra inclure une adaptation backend/API avant ou en parallèle de l'affichage frontend.

## Décision de découpage

La phase 7.1.9 est un design frontend.

La phase d'implémentation devra probablement être découpée en :

1. backend API contract update
2. TypeScript type update
3. AIExplanationCard
4. OpportunitiesPage integration
5. validation frontend

## Impact backend possible

À vérifier avant code :

- endpoint qui retourne MatchingResult
- endpoint qui retourne Opportunity Analysis
- structure utilisée dans OpportunitiesPage

Aucune modification backend ne doit être faite sans vérifier le contrat réel.

## Impact frontend possible

À vérifier avant code :

- structure exacte de OpportunitiesPage
- type actuellement utilisé pour matching
- client API existant
- composant Opportunity Analysis existant
- emplacement du placeholder AI Recommendations

## Risques identifiés

### Risque 1

Le contrat API actuel ne contient pas ai_explanation.

Mitigation :

valider le contrat réel avant code.

### Risque 2

Le frontend affiche l'IA avant les éléments déterministes.

Mitigation :

respecter la hiérarchie d'affichage.

### Risque 3

Le composant devient trop complexe.

Mitigation :

composant pure display uniquement.

### Risque 4

L'utilisateur interprète l'IA comme décision officielle.

Mitigation :

positionner l'explication IA comme complément.

## Décisions validées

DEC-7.1.9-001

L'AI Explanation est affichée dans OpportunitiesPage.

DEC-7.1.9-002

L'AI Explanation apparaît après Opportunity Analysis.

DEC-7.1.9-003

Aucun endpoint dédié n'est créé pour le MVP.

DEC-7.1.9-004

Le composant AIExplanationCard est purement présentationnel.

DEC-7.1.9-005

ai_explanation = null est un cas normal.

DEC-7.1.9-006

Les métadonnées provider ne sont pas affichées dans le MVP.

## Critères de validation de cette phase

Cette phase sera terminée lorsque :

- le contrat TypeScript est défini ;
- le composant AIExplanationCard est défini ;
- les états UI sont définis ;
- le placement dans OpportunitiesPage est défini ;
- les cas de fallback sont définis ;
- les validations manuelles sont définies ;
- les impacts backend sont identifiés ;
- les impacts frontend sont identifiés.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- fournisseur réel ;
- appels LLM ;
- streaming ;
- chat ;
- feedback utilisateur ;
- régénération ;
- historique ;
- stockage permanent ;
- nouveau dashboard IA ;
- génération CV ;
- génération lettre.

## Livrable

- docs/ai-explanation-frontend-integration-design.md

## Étape suivante recommandée

Phase 7.1.10

AI Explanation Frontend Technical Implementation Plan

Objectif :

Définir les fichiers exacts à modifier, les fichiers à créer, l'ordre d'implémentation, les tests attendus et les validations manuelles avant toute modification du frontend.
