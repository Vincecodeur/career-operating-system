# AI Prompt Builder Design

## Phase

7.1.6 AI Prompt Builder Design

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- AI Explanation Domain Design
- AI Explanation Backend Package Design
- AI Explanation Schema Design
- AI Provider Interface Design
- AI Explanation Service Design

Le projet dispose maintenant :

- des objets métier IA ;
- des schémas attendus ;
- de l'interface fournisseur ;
- du service d'orchestration cible ;
- des règles de sécurité et de gouvernance IA.

Cette phase définit précisément le rôle du PromptBuilder avant toute implémentation.

Aucun code ne doit être produit pendant cette phase.

Aucun appel LLM ne doit être réalisé.

Aucun fournisseur IA ne doit être intégré.

## Objectif

Définir :

- les responsabilités du PromptBuilder ;
- la structure des prompts ;
- la structure des templates ;
- les variables autorisées ;
- les garde-fous anti-hallucination ;
- la stratégie de versionnement ;
- la stratégie de validation ;
- la stratégie de test.

## Principe fondamental

Le PromptBuilder ne décide rien.

Le PromptBuilder ne calcule rien.

Le PromptBuilder assemble uniquement un prompt à partir de données déjà validées.

Le PromptBuilder ne doit jamais :

- calculer le score ;
- modifier le score ;
- modifier le verdict ;
- modifier la recommendation ;
- inventer des compétences ;
- inventer des expériences ;
- enrichir une offre avec des informations non fournies.

## Position dans l'architecture

Pipeline cible :

Matching Engine
↓
Opportunity Analysis
↓
AIExplanationContext
↓
Context Validator
↓
PromptBuilder
↓
AIProviderRequest
↓
AIProvider
↓
AIProviderResponse
↓
Response Validator
↓
AIExplanation

## Rôle principal

PromptBuilder transforme un AIExplanationContext validé en prompt exploitable par un fournisseur IA.

Il prépare le texte d'instruction.

Il injecte les données structurées.

Il impose le format de sortie.

Il rappelle les interdictions au modèle.

## Responsabilités autorisées

PromptBuilder peut :

- recevoir un AIExplanationContext ;
- recevoir une version de prompt ;
- sélectionner un template ;
- injecter les valeurs du contexte ;
- produire un prompt final ;
- produire les métadonnées du prompt.

## Responsabilités interdites

PromptBuilder ne doit jamais :

- appeler un provider ;
- appeler OpenAI ;
- appeler Azure OpenAI ;
- valider la réponse IA ;
- interpréter la réponse IA ;
- accéder à PostgreSQL ;
- accéder aux modèles SQLAlchemy ;
- accéder aux routes FastAPI ;
- accéder au frontend ;
- lire directement les fichiers .env.

## Entrées attendues

PromptBuilder reçoit :

- AIExplanationContext
- prompt_version
- output_format

## Sortie attendue

PromptBuilder retourne :

- prompt
- prompt_version

Sortie conceptuelle :

AIProviderRequest

avec :

- prompt
- prompt_version
- context

## Structure générale du prompt

Le prompt est composé de trois blocs.

Bloc 1 :

System Instructions

Bloc 2 :

Structured Context

Bloc 3 :

Output Format Instructions

## Bloc 1 - System Instructions

Objectif :

Définir le comportement attendu du modèle.

Le bloc doit rappeler que :

- le modèle explique uniquement ;
- le modèle ne calcule pas ;
- le modèle ne modifie pas les résultats ;
- le modèle ne doit pas inventer d'information ;
- le modèle doit utiliser uniquement les données fournies.

Exemple conceptuel :

You are an explanation assistant for a deterministic career matching system.

Your role is to explain the provided matching result.

You must not change the score.

You must not change the recommendation.

You must not change the verdict.

You must not invent skills.

You must not invent experience.

Use only the provided structured context.

If information is missing, state that the information is unavailable.

## Bloc 2 - Structured Context

Objectif :

Fournir au modèle uniquement les données nécessaires.

Données autorisées :

- job_title
- score
- strengths
- weaknesses
- recommendation
- verdict
- deterministic_summary

Données interdites :

- secrets ;
- tokens ;
- mots de passe ;
- variables d'environnement ;
- logs ;
- stack traces ;
- historique complet utilisateur ;
- données système internes.

## Exemple de contexte

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
"recommendation": "APPLY",
"verdict": "GOOD_MATCH",
"deterministic_summary": "The role is aligned with backend API experience but requires stronger containerization skills."
}

## Bloc 3 - Output Format Instructions

Objectif :

Forcer une réponse structurée.

Format cible :

{
"summary": "...",
"detailed_explanation": "...",
"action_plan": [
"...",
"..."
]
}

Le modèle doit retourner uniquement ce format.

Aucune introduction.

Aucune conclusion libre.

Aucun texte hors structure attendue.

## Templates prévus

### Template 1

Nom :

score_explanation_v1

Objectif :

Expliquer le score déterministe.

Utilisation :

détail d'une opportunité.

### Template 2

Nom :

action_plan_v1

Objectif :

Transformer les weaknesses en pistes d'action.

Utilisation :

phase ultérieure.

Hors périmètre de la première implémentation.

### Template 3

Nom :

short_summary_v1

Objectif :

Résumé très court.

Utilisation :

potentielle optimisation frontend future.

Hors périmètre immédiat.

## Template MVP

Le template MVP est :

score_explanation_v1

Il doit produire :

- summary
- detailed_explanation
- action_plan

## Versionnement

Chaque template doit être versionné.

Exemple :

score_explanation_v1

Règle :

une modification significative du prompt crée une nouvelle version.

Exemples :

score_explanation_v2

score_explanation_v3

## Pourquoi versionner

Le versionnement permet :

- auditabilité ;
- comparaison ;
- rollback ;
- compréhension des explications générées ;
- traçabilité avec les réponses IA.

## Métadonnées prompt

PromptBuilder doit permettre de conserver :

- prompt_version
- template_name
- generated_at

La réponse finale AIExplanation doit conserver :

- prompt_version

## Variables autorisées

Variables autorisées dans le template MVP :

- job_title
- score
- strengths
- weaknesses
- recommendation
- verdict
- deterministic_summary

Aucune autre variable.

## Variables interdites

Ne jamais injecter :

- user email ;
- token ;
- password ;
- API key ;
- database URL ;
- full logs ;
- stack trace ;
- raw environment ;
- full application history.

## Validation avant génération

PromptBuilder doit refuser de générer un prompt si :

- context absent ;
- score absent ;
- recommendation absente ;
- verdict absent ;
- job_title absent ;
- prompt_version absente.

## Validation après génération

PromptBuilder doit vérifier :

- prompt non vide ;
- prompt contient les instructions anti-hallucination ;
- prompt contient le format attendu ;
- prompt contient la version ;
- prompt ne contient pas de secret connu.

## Règles anti-hallucination dans le prompt

Le prompt doit explicitement interdire :

- invention de compétences ;
- invention d'expérience ;
- invention de niveau de séniorité ;
- invention de salaire ;
- invention d'informations entreprise ;
- modification du score ;
- modification de la recommandation ;
- modification du verdict.

## Règle information manquante

Si une information n'est pas fournie, le modèle doit écrire :

The provided data does not specify this information.

Il ne doit jamais deviner.

## Langue MVP

Règle MVP :

anglais uniquement.

Conséquence :

- prompt en anglais ;
- réponse attendue en anglais.

Le support français est hors périmètre de cette phase.

## Longueur attendue

summary :

50 à 120 mots maximum.

detailed_explanation :

150 à 400 mots maximum.

action_plan :

3 à 5 éléments maximum.

Ces limites sont indicatives pour le prompt.

Les validations backend pourront être plus strictes dans une phase d'implémentation.

## Style attendu

Le style doit être :

- clair ;
- factuel ;
- neutre ;
- simple ;
- orienté décision.

Le style ne doit pas être :

- marketing ;
- exagéré ;
- émotionnel ;
- spéculatif.

## Exemple de prompt conceptuel

System Instructions:

You are an explanation assistant for a deterministic career matching system.

Use only the provided data.

Do not modify the score.

Do not modify the verdict.

Do not modify the recommendation.

Do not invent missing skills.

Do not invent missing experience.

Structured Context:

job_title: Backend Engineer

score: 78

strengths:

- Python
- FastAPI

weaknesses:

- Docker
- Kubernetes

recommendation: APPLY

verdict: GOOD_MATCH

deterministic_summary:
The role is aligned with backend API experience but requires stronger containerization skills.

Expected Output:

Return a JSON object with:

summary

detailed_explanation

action_plan

## Interaction avec AIExplanationService

AIExplanationService orchestre.

PromptBuilder construit.

AIProvider exécute.

ResponseValidator valide la réponse.

AIExplanationService ne doit pas contenir les templates complets.

## Interaction avec AIProvider

AIProvider reçoit :

AIProviderRequest

Le champ prompt est déjà complet.

AIProvider ne modifie pas le prompt.

## Interaction avec Validators

ContextValidator intervient avant PromptBuilder.

ResponseValidator intervient après AIProvider.

PromptBuilder ne remplace pas ces validateurs.

## Gestion d'erreur

Si PromptBuilder ne peut pas construire le prompt :

lever une erreur contrôlée future :

AIPromptBuildError

AIExplanationService devra capturer cette erreur.

## Erreurs prévues

AIPromptBuildError

Cas :

- contexte invalide ;
- template introuvable ;
- version introuvable ;
- variable manquante.

AIPromptTemplateError

Cas :

- template mal formé ;
- output format absent ;
- instructions anti-hallucination absentes.

## Logging

Logs autorisés :

- template_name ;
- prompt_version ;
- success ;
- error_type.

Logs interdits :

- prompt complet ;
- contexte complet ;
- données personnelles ;
- secrets.

## Tests futurs attendus

Fichier probable :

backend/tests/ai/test_prompt_builder.py

Tests recommandés :

### Test 1

PromptBuilder construit un prompt avec un contexte valide.

### Test 2

PromptBuilder refuse un contexte sans score.

### Test 3

PromptBuilder refuse un contexte sans recommendation.

### Test 4

PromptBuilder inclut les règles anti-hallucination.

### Test 5

PromptBuilder inclut le format de sortie attendu.

### Test 6

PromptBuilder conserve prompt_version.

### Test 7

PromptBuilder ne modifie pas le contexte.

### Test 8

PromptBuilder n'inclut pas de données interdites.

## Stratégie de test

Tous les tests doivent être déterministes.

Aucun appel réseau.

Aucun fournisseur IA réel.

Aucune clé API.

Aucun fichier .env requis.

## Structure future des fichiers

backend/app/ai/prompts/

Fichiers prévus :

- prompt_builder.py
- prompt_templates.py

## prompt_builder.py

Responsabilité :

- construire le prompt ;
- valider les variables ;
- appliquer la version.

## prompt_templates.py

Responsabilité :

- contenir les templates ;
- exposer les versions disponibles.

## Template storage

Décision MVP :

templates en Python.

Pas de fichiers externes.

Raison :

- simplicité ;
- testabilité ;
- pas de parsing fichier ;
- cohérence backend.

Évolution future possible :

templates en fichiers .md ou .yaml.

Hors périmètre.

## Critères de validation de cette phase

Cette phase sera considérée comme terminée lorsque :

- rôle du PromptBuilder défini ;
- structure des prompts définie ;
- templates définis ;
- versionnement défini ;
- règles anti-hallucination définies ;
- validations définies ;
- erreurs définies ;
- tests futurs définis.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- PromptBuilder ;
- prompt_templates.py ;
- provider IA ;
- OpenAI ;
- Azure OpenAI ;
- appels LLM ;
- FastAPI ;
- frontend ;
- cache ;
- RAG ;
- embeddings ;
- agents.

## Livrable

- docs/ai-prompt-builder-design.md

## Étape suivante recommandée

Phase 7.1.7

AI Domain Implementation Plan

Objectif :

Définir le plan exact d'implémentation des premiers fichiers Python du domaine IA, l'ordre de création des fichiers, les tests à écrire et les critères de validation avant de commencer le code.
