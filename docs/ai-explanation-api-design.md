# AI Explanation API Design

## Phase

7.0.4 AI Explanation API Design

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- l'AI Explanation Layer ;
- l'architecture backend ;
- la stratégie de prompts ;
- les garde-fous anti-hallucination.

Aucun fournisseur IA n'est encore intégré.

L'objectif de cette phase est de définir les contrats API et les schémas nécessaires pour préparer l'intégration future de l'AI Explanation Layer.

Aucun code ne doit être produit pendant cette phase.

## Objectif

Définir :

- les schémas Pydantic ;
- les contrats FastAPI ;
- les réponses API ;
- les états d'erreur ;
- la compatibilité frontend.

## Principe fondamental

L'API doit continuer de fonctionner même lorsque l'IA est :

- désactivée ;
- indisponible ;
- en erreur ;
- en timeout.

La couche IA est facultative.

Le matching reste le cœur du système.

## Architecture cible

Client
↓
FastAPI
↓
Matching Engine
↓
Opportunity Analysis
↓
AI Explanation Layer
↓
Response DTO

## Nouveau schéma métier

AIExplanation

Objectif :

Représenter une explication générée par l'IA.

### Champs

summary

Type :

string

Description :

Résumé court destiné à une lecture rapide.

---

detailed_explanation

Type :

string

Description :

Explication détaillée du résultat.

---

action_plan

Type :

list[string]

Description :

Actions pratiques suggérées.

---

generated_at

Type :

datetime

Description :

Date de génération.

---

model_name

Type :

string

Description :

Modèle utilisé.

---

prompt_version

Type :

string

Description :

Version du prompt utilisée.

## Nouveau schéma API

AIExplanationResponse

Structure :

{
"summary": "...",
"detailed_explanation": "...",
"action_plan": [],
"generated_at": "...",
"model_name": "...",
"prompt_version": "..."
}

## Schéma principal enrichi

OpportunityAnalysisResponse

Aujourd'hui :

{
"matching_result": {},
"opportunity_analysis": {}
}

Demain :

{
"matching_result": {},
"opportunity_analysis": {},
"ai_explanation": {}
}

## Cas sans IA

Réponse :

{
"matching_result": {},
"opportunity_analysis": {},
"ai_explanation": null
}

Cette réponse est parfaitement valide.

## Endpoint MVP

Aucun nouvel endpoint.

Principe :

L'explication IA rejoint la réponse existante.

Objectif :

Éviter la multiplication de routes inutiles.

## Contrat API cible

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

## Version minimale

Premier MVP :

summary uniquement.

Structure :

{
"summary": "..."
}

Le reste peut être ajouté ultérieurement.

## Gestion d'erreur

### Cas 1

Provider indisponible

Réponse :

{
"ai_explanation": null
}

Aucune erreur HTTP.

### Cas 2

Timeout

Réponse :

{
"ai_explanation": null
}

Aucune erreur HTTP.

### Cas 3

Réponse invalide

Réponse :

{
"ai_explanation": null
}

Aucune erreur HTTP.

## Codes HTTP

Erreur IA :

HTTP 200

Pourquoi :

Le matching a fonctionné.

Seule l'explication non critique a échoué.

## Validation backend

Avant retour API :

Vérifier :

- summary non vide ;
- longueur acceptable ;
- structure valide.

Sinon :

ai_explanation = null

## Compatibilité Frontend

Le frontend doit accepter :

Cas 1

{
"ai_explanation": {}
}

Cas 2

{
"ai_explanation": null
}

Les deux cas sont normaux.

## Affichage Frontend prévu

Opportunities
↓
Matching Analysis
↓
Opportunity Analysis
↓
AI Explanation

Sections :

- Summary
- Detailed Explanation
- Action Plan

## Journalisation

Journaliser :

- request_id
- model_name
- prompt_version
- durée

Ne jamais journaliser :

- prompt complet
- données privées
- secrets

## Observabilité

Métriques visées :

- ai_requests_total
- ai_success_total
- ai_failure_total
- ai_timeout_total
- ai_cache_hit_total
- ai_cache_miss_total

## Cache API

Le cache ne modifie pas le contrat API.

Le frontend reçoit toujours :

{
"ai_explanation": {}
}

ou

{
"ai_explanation": null
}

## Validation attendue

La phase sera terminée lorsque :

- AIExplanation schema est défini ;
- contrat API est défini ;
- cas d'erreur documentés ;
- stratégie frontend documentée ;
- stratégie d'observabilité documentée ;
- compatibilité future
