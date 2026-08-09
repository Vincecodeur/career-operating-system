# AI Score Explanation Design

## Phase

7.0.1 AI Score Explanation Design

## Statut

Design

## Contexte

Le système dispose déjà d'un moteur de matching déterministe entièrement fonctionnel.

Les éléments suivants existent déjà :

- Matching V2
- Score global
- Sous-scores
- Skills Match
- Experience Match
- Work Mode Match
- Location Match
- Strengths
- Weaknesses
- Opportunity Analysis
- Verdict
- Recommendation
- Summary

Ces résultats sont produits par des règles métier déterministes et testables.

Le score ne doit jamais être calculé par l'IA.

L'IA intervient uniquement comme couche d'explication complémentaire.

L'objectif de cette phase est de définir comment utiliser un LLM pour rendre les résultats plus compréhensibles pour l'utilisateur sans modifier les calculs réalisés par le backend. 【1-e72b19】【2-136f79】【3-4c5167】

## Problème à résoudre

Les résultats actuels sont factuellement corrects mais parfois peu naturels.

Exemple actuel :

Score : 78

Strengths :

- Python
- FastAPI
- API Design

Weaknesses :

- Kubernetes
- Docker

Recommendation :
Apply

Un utilisateur comprend le résultat mais ne comprend pas forcément :

- pourquoi l'opportunité est vraiment intéressante ;
- quels sont les risques ;
- ce qu'il devrait faire ensuite ;
- comment interpréter les sous-scores.

L'IA doit améliorer cette compréhension.

## Objectif métier

Permettre au candidat de comprendre facilement :

- pourquoi une opportunité est recommandée ;
- quels sont ses avantages ;
- quels sont ses points de vigilance ;
- quels sont les écarts principaux ;
- quelles actions seraient pertinentes.

Sans modifier le score calculé.

## Principe fondamental

Le moteur déterministe reste la source de vérité.

Architecture :

Job Offer

- Candidate Profile
  ↓
  Matching Engine
  ↓
  Score Deterministe
  ↓
  Opportunity Analysis
  ↓
  AI Explanation Layer
  ↓
  Explication utilisateur

Le LLM reçoit le résultat.

Le LLM ne produit jamais le résultat.

## Séparation stricte des responsabilités

### Backend déterministe

Responsable de :

- score
- ranking
- analyse
- strengths
- weaknesses
- verdict
- recommendation

### IA

Responsable uniquement de :

- reformulation
- pédagogie
- résumé
- contextualisation
- aide à l'interprétation

Le LLM n'a pas l'autorité de modifier :

- score
- classement
- verdict

## Données fournies à l'IA

Entrée :

Candidate Profile

Matching Result

Opportunity Analysis

Exemple :

{
"job_title": "Senior Backend Engineer",
"score": 78,
"strengths": [
"Python",
"FastAPI",
"REST APIs"
],
"weaknesses": [
"Kubernetes",
"Docker"
],
"recommendation": "APPLY"
}

## Données interdites

L'IA ne reçoit pas :

- historique complet des candidatures
- secrets
- identifiants
- données techniques sensibles
- logs système
- informations inutiles au raisonnement

## Sortie IA attendue

Exemple :

Cette opportunité présente un bon niveau d'adéquation avec votre profil.

Les compétences Python et FastAPI sont fortement alignées avec les exigences du poste.

Les principaux écarts concernent Kubernetes et Docker.

Ces compétences sont souvent acquises rapidement dans un environnement backend moderne.

Cette opportunité semble donc constituer une candidature pertinente.

## Types d'explications

### Type 1

Executive Summary

Format :

3 à 6 phrases

Objectif :

lecture rapide

### Type 2

Detailed Explanation

Format :

plusieurs paragraphes

Objectif :

lecture approfondie

### Type 3

Action Plan

Format :

liste d'actions

Exemple :

- renforcer Kubernetes
- renforcer Docker
- adapter le CV

## Architecture backend

Nouveau composant :

AIExplanationService

Responsabilités :

- construire le prompt
- appeler le fournisseur IA
- sécuriser les entrées
- sécuriser les sorties

Architecture visée :

Matching Engine
↓
Opportunity Analysis
↓
AIExplanationService
↓
LLM Provider
↓
AIExplanation

## Nouveau schéma

AIExplanation

Proposition :

class AIExplanation

Fields :

- summary
- detailed_explanation
- action_plan
- generated_at
- model_name

Aucune information métier complémentaire.

## Prompt Strategy

Principe :

prompt extrêmement encadré.

Exemple :

You are a career advisor.

You must explain the provided score.

Never modify any score.

Never invent missing skills.

Never invent experience.

Use only provided inputs.

Return factual explanations.

## Anti-Hallucination Strategy

Règle 1

L'IA ne voit que des données structurées.

Règle 2

L'IA ne calcule aucun score.

Règle 3

L'IA ne crée aucune nouvelle compétence.

Règle 4

L'IA ne crée aucune expérience professionnelle.

Règle 5

L'IA ne modifie jamais la recommandation.

Règle 6

Le backend doit conserver :

- score officiel
- recommendation officielle
- verdict officiel

## Contrat API

Proposition :

GET /matching/{job_offer_id}

Retour :

{
"score": 78,
"strengths": [],
"weaknesses": [],
"opportunity_analysis": {},
"ai_explanation": {
"summary": "...",
"detailed_explanation": "...",
"action_plan": []
}
}

## Gestion d'erreur

Si l'IA échoue :

Retour :

{
"score": 78,
"opportunity_analysis": {},
"ai_explanation": null
}

Le système doit rester pleinement utilisable.

L'IA est une amélioration.

L'IA n'est jamais une dépendance bloquante.

## Coût et performance

Objectif MVP :

1 appel IA uniquement :

- lorsqu'un utilisateur consulte le détail d'une opportunité.

Pas d'appel IA :

- sur les listes ;
- sur les classements ;
- sur le dashboard.

Objectif :

contenir le coût.

## Cache

Phase MVP :

cache simple recommandé.

Clé :

profile_id

- job_offer_id
- matching_version

Permet d'éviter plusieurs appels identiques.

## Frontend

Nouvelle zone :

AI Explanation

Position :

Opportunities
↓
Matching Analysis
↓
AI Explanation

Contenu :

- Executive Summary
- Detailed Explanation
- Action Plan

## Validation attendue

La phase sera considérée comme terminée lorsque :

- AIExplanation schema est défini ;
- contrat API est défini ;
- stratégie anti-hallucination est documentée ;
- stratégie de prompt est documentée ;
- architecture backend est documentée ;
- impact frontend est documenté.

Aucun code ne doit être produit pendant cette phase.

## Hors périmètre

Ne pas implémenter :

- appel OpenAI ;
- appel Azure OpenAI ;
- génération de CV ;
- génération de lettre de motivation ;
- coaching carrière ;
- analyse de marché ;
- embeddings ;
- RAG ;
- agents.

Ces sujets seront étudiés dans des phases ultérieures.

## Livrables de la phase

- docs/ai-score-explanation-design.md

## Étape suivante recommandée

Phase 7.0.2

AI Explanation Backend Design

Objectif :

Concevoir l'implémentation backend de AIExplanationService avant toute intégration réelle d'un fournisseur LLM.
