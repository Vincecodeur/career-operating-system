# AI Prompt Architecture Design

## Phase

7.0.3 AI Prompt Architecture Design

## Statut

Design

## Contexte

Le projet dispose désormais :

- d'un moteur de matching déterministe ;
- d'un moteur d'analyse déterministe ;
- d'un design de couche IA ;
- d'une architecture backend pour AIExplanationService.

La prochaine étape consiste à définir précisément comment les prompts seront construits afin de :

- limiter les hallucinations ;
- garantir la cohérence métier ;
- garantir la reproductibilité ;
- protéger les données utilisateur ;
- conserver le moteur déterministe comme source de vérité.

Aucun appel LLM réel ne sera implémenté pendant cette phase.

## Objectif

Définir :

- la structure des prompts ;
- les entrées autorisées ;
- les sorties attendues ;
- les garde-fous ;
- les validations backend ;
- les formats de réponse.

## Principe fondamental

Le LLM ne doit jamais :

- calculer le score ;
- recalculer le matching ;
- modifier un verdict ;
- modifier une recommandation ;
- inventer des compétences ;
- inventer une expérience.

Le LLM doit uniquement expliquer.

## Architecture du prompt

Le prompt est construit à partir de trois blocs.

Bloc 1 :

System Prompt

Bloc 2 :

Structured Business Context

Bloc 3 :

Expected Output Format

## Bloc 1 — System Prompt

Objectif :

Définir le comportement permanent du modèle.

Exemple :

You are an explainability assistant.

Your job is to explain deterministic career analysis results.

Never modify any score.

Never generate facts that are not provided.

Never invent skills.

Never invent experience.

Never modify recommendations.

Use only provided inputs.

If information is missing, state that information is unavailable.

## Bloc 2 — Structured Business Context

Contient uniquement :

Candidate Information

Opportunity Information

Matching Information

Opportunity Analysis

Exemple :

{
"job_title": "Backend Engineer",
"score": 78,
"strengths": [
"Python",
"FastAPI"
],
"weaknesses": [
"Docker",
"Kubernetes"
],
"recommendation": "APPLY"
}

Le backend est responsable de générer ce contexte.

## Bloc 3 — Expected Output Format

Le modèle doit produire une structure connue.

Exemple :

{
"summary": "...",
"detailed_explanation": "...",
"action_plan": [
"...",
"..."
]
}

Objectif :

Faciliter la validation backend.

## Catégories de prompts

### Prompt Type 1

Executive Summary

Objectif :

Résumé rapide.

Longueur cible :

50 à 120 mots.

### Prompt Type 2

Detailed Explanation

Objectif :

Explication détaillée.

Longueur cible :

150 à 400 mots.

### Prompt Type 3

Action Plan

Objectif :

Identifier des actions concrètes.

Format :

Liste courte.

## Construction du contexte

Ordre recommandé :

Job Information
↓
Matching Score
↓
Strengths
↓
Weaknesses
↓
Recommendation
↓
Verdict

Objectif :

Fournir les informations les plus importantes en premier.

## Anti-Hallucination Layer

Avant d'appeler le LLM :

Validation backend.

Contrôles obligatoires :

- score présent ;
- recommendation présente ;
- verdict présent ;
- strengths présentes ;
- weaknesses présentes.

Si un élément est absent :

pas d'appel IA.

## Validation de la réponse

Après retour du LLM :

Contrôler :

- JSON valide ;
- champs requis présents ;
- longueur raisonnable ;
- absence de contenu vide.

En cas d'échec :

ai_explanation = null

## Expressions interdites

Le prompt doit explicitement interdire :

- "I estimate"
- "Probably"
- "Likely"
- "You certainly"
- informations non présentes

Objectif :

limiter les spéculations.

## Données interdites

Ne jamais envoyer :

- secrets ;
- tokens ;
- mots de passe ;
- emails ;
- logs ;
- stack traces ;
- historique complet utilisateur.

## Langue

Règle MVP :

Anglais uniquement.

Le système générera :

- prompt anglais ;
- réponse anglaise.

Le support français sera traité dans une phase ultérieure.

## Versionnement

Chaque prompt doit être versionné.

Exemple :

AI_PROMPT_VERSION = 1

Objectif :

permettre de rattacher une explication à une version précise du prompt utilisé.

## Traçabilité

Conserver :

- model_name
- prompt_version
- generated_at

Ne jamais conserver :

- secret
- token
- clé API

## Limites de coût

L'IA ne doit être appelée que :

- lors de la consultation du détail d'une opportunité.

Jamais :

- sur les listes ;
- sur les dashboard ;
- sur les classements.

## Observabilité

Mesures recommandées :

- total_requests
- total_success
- total_failures
- average_response_time
- cache_hit_rate

## Validation attendue

La phase sera terminée lorsque :

- architecture des prompts documentée ;
- formats de réponse documentés ;
- stratégie anti-hallucination documentée ;
- données autorisées documentées ;
- données interdites documentées ;
- stratégie de validation documentée ;
- stratégie de traçabilité documentée.

Aucun code ne doit être produit pendant cette phase.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- stockage des explications ;
- cache réel ;
- frontend IA ;
- génération de CV ;
- génération de lettres ;
- career coaching ;
- agents ;
- embeddings ;
- RAG.

## Livrable

- docs/ai-prompt-architecture-design.md

## Étape suivante recommandée

Phase 7.0.4

AI Explanation API Design

Objectif :

Définir les contrats FastAPI, les schémas Pydantic et les réponses API nécessaires à l'intégration future de l'AI Explanation Layer.
