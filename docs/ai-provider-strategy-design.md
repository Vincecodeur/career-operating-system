# AI Provider Strategy Design

## Phase

7.0.5 AI Provider Strategy Design

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- AI Score Explanation Design
- AI Explanation Backend Design
- AI Prompt Architecture Design
- AI Explanation API Design

L'architecture IA est désormais suffisamment définie pour réfléchir à la stratégie fournisseur.

Aucun fournisseur ne doit être intégré pendant cette phase.

Aucun appel LLM réel ne doit être développé.

L'objectif est uniquement de formaliser les critères de sélection et les exigences techniques du projet.

## Objectif

Définir :

- les exigences fonctionnelles ;
- les exigences techniques ;
- les exigences de sécurité ;
- les critères de coût ;
- les critères d'évolutivité ;
- les stratégies de fournisseur.

## Principe fondamental

Le projet doit rester indépendant d'un fournisseur spécifique.

L'architecture doit permettre :

Provider A
↓
Provider Adapter
↓
AIExplanationService

ou

Provider B
↓
Provider Adapter
↓
AIExplanationService

sans modifier la logique métier.

## Exigences fonctionnelles

Le fournisseur doit permettre :

- génération de texte ;
- réponses structurées ;
- faible latence ;
- sortie fiable ;
- contrôle du prompt ;
- fonctionnement en anglais.

Le fournisseur n'a pas besoin de :

- génération d'image ;
- génération audio ;
- agents ;
- recherche web ;
- outils externes.

## Exigences techniques

Le fournisseur doit supporter :

- API HTTP ;
- authentification sécurisée ;
- timeout configurable ;
- JSON en entrée ;
- JSON en sortie.

Le système doit rester compatible avec :

- FastAPI ;
- PostgreSQL ;
- architecture monolithique.

## Exigences de sécurité

Le fournisseur doit permettre :

- stockage sécurisé des secrets ;
- rotation des clés ;
- communication TLS ;
- séparation des environnements.

Les clés doivent être conservées uniquement dans :

.env

Les clés ne doivent jamais :

- apparaître dans Git ;
- apparaître dans les logs ;
- apparaître dans la documentation.

## Exigences de confidentialité

Le système doit transmettre uniquement :

- informations d'opportunité ;
- résultats de matching ;
- analyses déterministes.

Ne jamais transmettre :

- mots de passe ;
- secrets ;
- tokens ;
- informations techniques internes.

## Critères de coût

Le MVP doit minimiser :

- coût par requête ;
- coût mensuel ;
- coût de développement.

Les appels IA doivent être limités à :

consultation du détail d'une opportunité.

Aucun appel IA :

- dans le dashboard ;
- dans les listes ;
- dans les classements.

## Critères de qualité

Le fournisseur doit être capable de :

- respecter les instructions ;
- produire des réponses cohérentes ;
- limiter les hallucinations ;
- accepter des prompts structurés.

## Critères de disponibilité

Le fournisseur doit permettre :

- reprise après erreur ;
- timeout contrôlé ;
- gestion des indisponibilités.

Le système doit fonctionner même si le fournisseur échoue.

## Architecture fournisseur cible

Frontend
↓
FastAPI
↓
AIExplanationService
↓
AIProviderAdapter
↓
AI Provider

Le backend ne doit jamais dépendre directement d'un SDK fournisseur.

## Interface cible

AIProvider

Méthodes attendues :

generate_explanation()

Entrée :

- prompt
- configuration

Sortie :

- summary
- detailed_explanation
- action_plan

## Fournisseurs envisageables

### Option 1

OpenAI API

Avantages :

- intégration simple ;
- documentation mature ;
- adoption importante.

Inconvénients :

- dépendance à un fournisseur externe.

### Option 2

Azure OpenAI

Avantages :

- intégration entreprise ;
- gouvernance renforcée ;
- conformité facilitée.

Inconvénients :

- configuration plus complexe.

### Décision MVP

Aucune décision durant cette phase.

Le choix fournisseur sera effectué dans une phase ultérieure.

## Stratégie de changement de fournisseur

Objectif :

permettre :

OpenAI
→ Azure OpenAI

ou

Azure OpenAI
→ autre fournisseur

sans impact sur :

- API ;
- frontend ;
- logique métier.

## Versionnement

Les éléments suivants doivent être versionnés :

- prompts ;
- modèles ;
- fournisseurs.

Exemple :

provider_name
model_name
prompt_version

## Observabilité

Mesures recommandées :

- requests_total
- success_total
- failure_total
- timeout_total
- average_response_time
- average_cost_estimate

## Gestion des erreurs

Cas :

fournisseur indisponible

Résultat :

ai_explanation = null

Le système reste fonctionnel.

## Stratégie MVP recommandée

Priorités :

1. simplicité ;
2. faible coût ;
3. traçabilité ;
4. robustesse ;
5. évolutivité.

Avant tout développement :

- architecture validée ;
- prompts validés ;
- API validée ;
- sécurité validée.

## Validation attendue

La phase est terminée lorsque :

- critères fournisseur documentés ;
- exigences sécurité documentées ;
- exigences coût documentées ;
- stratégie de changement documentée ;
- interface cible documentée ;
- architecture documentée.

Aucun code ne doit être produit pendant cette phase.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- appels API ;
- stockage des réponses ;
- cache réel ;
- génération de CV ;
- génération de lettres ;
- agents ;
- embeddings ;
- RAG.

## Livrable

- docs/ai-provider-strategy-design.md

## Étape suivante recommandée

Phase 7.0.6

AI Security & Governance Design

Objectif :

Définir les règles de sécurité, confidentialité, auditabilité, traçabilité et gouvernance nécessaires avant toute implémentation réelle d'un fournisseur IA.
