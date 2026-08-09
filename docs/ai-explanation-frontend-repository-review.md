# AI Explanation Frontend Repository Review

## Phase

7.1.11 AI Explanation Frontend Repository Review

## Statut

Review

## Date

2026-08-09

## Objectif

Analyser les fichiers réels du frontend afin d'identifier précisément où intégrer l'AI Explanation Layer avant toute modification de code.

Cette revue doit vérifier :

- la structure actuelle du frontend ;
- les fichiers réellement existants ;
- les types actuellement utilisés ;
- le flux API actuel ;
- l'emplacement exact du placeholder AI ;
- les composants à créer ;
- les composants à modifier ;
- les risques avant implémentation.

Aucun code ne doit être produit pendant cette phase.

## Fichiers analysés

Fichiers fournis et analysés :

- frontend/src/pages/OpportunitiesPage.tsx
- frontend/src/services/api.ts
- frontend/src/components/MatchingResult.tsx

## Résumé exécutif

Le frontend contient déjà un emplacement clair pour intégrer l'AI Explanation Layer.

L'intégration devra se faire principalement dans :

- frontend/src/pages/OpportunitiesPage.tsx

Un nouveau composant devra être créé :

- frontend/src/components/AIExplanationCard.tsx

Un composant skeleton pourra être créé ultérieurement si nécessaire :

- frontend/src/components/AIExplanationCardSkeleton.tsx

Contrairement à l'hypothèse initiale du design :

- frontend/src/types/api.ts n'existe pas.

Les types sont actuellement définis localement dans OpportunitiesPage.tsx.

Le fichier API réel est :

- frontend/src/services/api.ts

La revue complète de MatchingResult.tsx montre qu'il ne doit pas être modifié dans le premier incrément.

## Structure frontend observée

### Pages

Dossier :

frontend/src/pages

Contenu observé :

- AccountPage.tsx
- ApplicationsPage.tsx
- DashboardPage.tsx
- ForgotPasswordPage.tsx
- LoginPage.tsx
- OpportunitiesPage.tsx
- ProfilesPage.tsx
- SettingsPage.tsx

Aucun sous-dossier observé.

### Components

Dossier :

frontend/src/components

Contenu observé :

- ApplicationTracker.tsx
- Dashboard.tsx
- JobOfferList.tsx
- MatchingResult.tsx
- OpportunityRanking.tsx
- ProfileList.tsx

Sous-dossier :

frontend/src/components/ui

Contenu observé :

- Card.tsx
- PageHeader.tsx
- Section.tsx
- StatCard.tsx

## Analyse de OpportunitiesPage.tsx

### Responsabilités actuelles

Le fichier gère déjà :

- chargement des offres ;
- sélection d'une offre ;
- chargement du matching ;
- affichage du panneau de détail ;
- affichage de MatchingResult ;
- affichage du placeholder AI Recommendations.

### Types locaux observés

Le fichier définit localement :

- JobOffer
- ScoreExplanation
- OpportunityAnalysis
- MatchingData

### Type MatchingData actuel

MatchingData contient :

- matching_score
- skills_score
- experience_score
- work_mode_score
- location_score
- matching_skills
- missing_skills
- strengths
- weaknesses
- opportunity_analysis
- explanations

Le type ne contient pas encore :

- ai_explanation

### Emplacement AI observé

Le bloc suivant existe déjà :

AI Recommendations

avec :

Available in Phase 7.

C'est le point d'intégration idéal de l'AI Explanation Layer.

## Analyse de MatchingResult.tsx

### Rôle actuel

MatchingResult.tsx affiche :

- Matching Score
- Score Details
- Strengths
- Weaknesses
- Score Explanations
- Opportunity Analysis
- Matching Skills
- Missing Skills

### Données reçues

Le composant reçoit actuellement :

- matchingScore
- skillsScore
- experienceScore
- workModeScore
- locationScore
- matchingSkills
- missingSkills
- strengths
- weaknesses
- explanations
- opportunityAnalysis

### Conclusion

MatchingResult.tsx est un composant d'affichage dédié aux résultats déterministes.

Il est cohérent.

Il est lisible.

Il ne nécessite aucune modification dans le premier incrément AI.

Décision :

Conserver MatchingResult.tsx inchangé.

Raison :

- séparation claire des responsabilités ;
- limitation du risque de régression ;
- conservation du découplage entre analyse déterministe et explication IA.

## Analyse de services/api.ts

### Fonctions observées

Le fichier expose :

- getProfiles
- getJobOffers
- getMatching
- getRankedJobOffers
- getApplications

### Constat

getMatching retourne directement :

response.json()

Le service est donc déjà compatible avec un enrichissement futur du payload backend.

Aucune modification n'est nécessaire dans le premier incrément.

## Constat important

Le fichier suivant n'existe pas :

frontend/src/types/api.ts

Conséquence :

Le design doit être mis à jour.

Pour rester cohérent avec le code réel :

- AIExplanation doit être ajouté localement dans OpportunitiesPage.tsx ;
- MatchingData doit être enrichi localement.

Aucune refactorisation globale des types n'est justifiée dans le MVP.

## Emplacement d'intégration cible

Position actuelle :

- Matching Analysis
- AI Recommendations
- Open Source Offer

Position cible :

- Matching Analysis
- AI Explanation
- Open Source Offer

Cette position respecte la hiérarchie métier :

1. score déterministe
2. analyse déterministe
3. explication IA

## Nouveau type à ajouter

Dans OpportunitiesPage.tsx :

type AIExplanation = {
summary: string;
detailed_explanation: string;
action_plan: string[];
provider_name: string;
model_name: string;
prompt_version: string;
};

## Modification du type MatchingData

Ajouter :

ai_explanation?: AIExplanation | null;

Le champ doit rester optionnel.

Objectif :

Permettre l'intégration progressive du backend.

## Nouveau composant à créer

### Fichier

frontend/src/components/AIExplanationCard.tsx

### Responsabilité

Afficher une explication IA.

Le composant ne doit pas :

- appeler l'API ;
- modifier le score ;
- modifier la recommandation ;
- exécuter une logique métier.

Il doit uniquement afficher :

- summary
- detailed_explanation
- action_plan

## Props attendues

type AIExplanationCardProps = {
explanation?: AIExplanation | null;
isLoading?: boolean;
error?: string | null;
};

## Comportements attendus

### Cas explanation disponible

Afficher :

- Summary
- Detailed Explanation
- Action Plan

### Cas explanation null

Afficher :

No AI explanation available.

### Cas explanation undefined

Afficher :

No AI explanation available.

### Cas action_plan vide

Masquer la section Action Plan.

### Cas erreur

Afficher :

Unable to display AI explanation.

## Composant Skeleton

Décision MVP :

Ne pas créer immédiatement AIExplanationCardSkeleton.tsx.

Raison :

Le frontend actuel n'utilise pas encore ce pattern.

Le premier incrément doit rester minimal.

Le skeleton pourra être ajouté ultérieurement.

## API Contract

Le frontend devra accepter :

ai_explanation

dans le payload récupéré via :

getMatching()

Structure attendue :

ai_explanation

{
"summary": "...",
"detailed_explanation": "...",
"action_plan": ["..."],
"provider_name": "mock",
"model_name": "mock-ai-explanation-model",
"prompt_version": "score_explanation_v1"
}

## Risque principal identifié

Le backend ne retourne peut-être pas encore :

ai_explanation

dans :

GET /matching/{profileId}/{jobOfferId}

Conséquence :

Le frontend doit être conçu avec fallback.

## Fichiers à créer

### Fichier 1

frontend/src/components/AIExplanationCard.tsx

Obligatoire.

## Fichiers à modifier

### Fichier 1

frontend/src/pages/OpportunitiesPage.tsx

Modifications prévues :

- ajout du type AIExplanation ;
- enrichissement de MatchingData ;
- import AIExplanationCard ;
- remplacement du placeholder AI Recommendations ;
- passage de matching?.ai_explanation.

### Fichier 2

frontend/src/services/api.ts

Aucune modification recommandée.

### Fichier 3

frontend/src/components/MatchingResult.tsx

Statut :

Analysé.

Modification :

Aucune modification recommandée.

## Modifications exactes prévues

### Ajout import

Ajouter :

import { AIExplanationCard } from "../components/AIExplanationCard";

### Ajout type

Ajouter :

type AIExplanation = {
summary: string;
detailed_explanation: string;
action_plan: string[];
provider_name: string;
model_name: string;
prompt_version: string;
};

### Enrichissement MatchingData

Ajouter :

ai_explanation?: AIExplanation | null;

### Remplacement du placeholder

Remplacer :

AI Recommendations

Available in Phase 7.

par :

AIExplanationCard

avec :

explanation={matching?.ai_explanation ?? null}

## Validation attendue

### Build frontend

Commande :

npm run build

### Tests backend

Commande :

pytest

### Validation visuelle

Vérifier :

- Matching Analysis visible ;
- AI Explanation visible ;
- fallback visible ;
- aucune erreur console.

## Décisions validées

DEC-7.1.11-001

Ne pas créer frontend/src/types/api.ts dans ce premier incrément.

DEC-7.1.11-002

Conserver les types locaux dans OpportunitiesPage.tsx.

DEC-7.1.11-003

Créer AIExplanationCard.tsx.

DEC-7.1.11-004

Ne pas modifier MatchingResult.tsx.

DEC-7.1.11-005

Remplacer le placeholder AI Recommendations.

DEC-7.1.11-006

Accepter ai_explanation undefined ou null.

DEC-7.1.11-007

MatchingResult.tsx a été analysé et restera inchangé dans le premier incrément.

DEC-7.1.11-008

AIExplanationCard sera intégré après MatchingResult pour préserver la séparation entre analyse déterministe et explication IA.

## Plan d'implémentation recommandé

### Étape 1

Créer :

frontend/src/components/AIExplanationCard.tsx

Objectif :

Créer un composant d'affichage indépendant.

### Étape 2

Modifier :

frontend/src/pages/OpportunitiesPage.tsx

Objectif :

- importer AIExplanationCard ;
- ajouter type AIExplanation ;
- enrichir MatchingData ;
- remplacer AI Recommendations ;
- transmettre matching?.ai_explanation.

### Étape 3

Ne pas modifier :

frontend/src/components/MatchingResult.tsx

### Étape 4

Lancer :

npm run build

### Étape 5

Lancer :

pytest

### Étape 6

Valider visuellement OpportunitiesPage.

### Étape 7

Commit technique frontend.

## Critères de fin

La revue repository est terminée lorsque :

- les fichiers réels ont été analysés ;
- MatchingResult.tsx a été analysé ;
- l'absence de frontend/src/types/api.ts est documentée ;
- les composants à créer sont identifiés ;
- les fichiers à modifier sont identifiés ;
- les risques sont documentés ;
- le plan d'implémentation est validé.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- appels LLM ;
- nouveau endpoint ;
- React Query dédié ;
- historique ;
- régénération ;
- chat IA ;
- feedback utilisateur ;
- refonte globale du typage frontend.

## Livrable

- docs/ai-explanation-frontend-repository-review.md

## Étape suivante recommandée

Phase 7.1.12

AI Explanation Frontend Implementation

Objectif :

Créer AIExplanationCard.tsx et intégrer le composant dans OpportunitiesPage.tsx avec une stratégie de fallback robuste, sans fournisseur IA réel et sans appel LLM.
