# AI Domain Implementation Plan

## Phase

7.1.7 AI Domain Implementation Plan

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- AI Explanation Domain Design
- AI Explanation Backend Package Design
- AI Explanation Schema Design
- AI Provider Interface Design
- AI Explanation Service Design
- AI Prompt Builder Design

La phase 7.1 vise à préparer l'implémentation du domaine IA sans intégrer immédiatement un fournisseur réel.

La Phase 7.0 est clôturée.

La Phase 7.1.1 AI Explanation Domain Design est la phase active du projet.

La prochaine étape logique est de définir précisément l'ordre de création des fichiers Python, les tests associés et les critères de validation.

Aucun code ne doit être produit pendant cette phase.

Aucun appel LLM réel ne doit être implémenté pendant cette phase.

Aucun fournisseur OpenAI ou Azure OpenAI ne doit être intégré pendant cette phase.

## Objectif

Définir :

- les fichiers backend à créer ;
- l'ordre exact de création ;
- les tests à créer ;
- les dépendances entre fichiers ;
- les critères de validation ;
- les limites du premier incrément IA ;
- la stratégie de commit.

## Principe fondamental

Le premier incrément IA doit rester entièrement local, déterministe et testable.

Le système ne doit pas encore appeler :

- OpenAI ;
- Azure OpenAI ;
- un fournisseur externe ;
- un service réseau.

Le premier objectif est de mettre en place le domaine IA interne.

## Objectif du premier incrément technique

Créer le socle backend minimal permettant de représenter et tester :

- les schémas IA ;
- les interfaces provider ;
- les erreurs IA ;
- les validateurs ;
- un provider mock ;
- le PromptBuilder ;
- AIExplanationService avec provider mock.

## Hors périmètre du premier incrément

Ne pas implémenter :

- OpenAIProvider ;
- AzureOpenAIProvider ;
- appels HTTP ;
- stockage en base ;
- cache ;
- endpoints FastAPI ;
- frontend ;
- RAG ;
- embeddings ;
- agents ;
- génération de CV ;
- génération de lettre de motivation.

## Structure cible

Créer progressivement :

backend/app/ai/

avec :

- **init**.py
- schemas.py
- exceptions.py
- interfaces.py
- settings.py
- validators/
- prompts/
- providers/
- services.py

Créer progressivement :

backend/tests/ai/

avec :

- test_ai_schemas.py
- test_ai_provider_interface.py
- test_ai_validators.py
- test_ai_prompt_builder.py
- test_mock_ai_provider.py
- test_ai_explanation_service.py

## Ordre d'implémentation recommandé

### Étape 1 - Créer le package IA

Fichiers à créer :

- backend/app/ai/**init**.py
- backend/app/ai/schemas.py
- backend/tests/ai/test_ai_schemas.py

Objectif :

Créer les schémas Pydantic du domaine IA.

Schémas attendus :

- AIExplanation
- AIExplanationContext
- AIProviderRequest
- AIProviderResponse
- AIExplanationResult
- AIProviderConfiguration

Critères de validation :

- les schémas peuvent être instanciés ;
- les champs requis sont validés ;
- les contraintes de score sont appliquées ;
- les structures sont sérialisables ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_ai_schemas.py -q

---

### Étape 2 - Créer les exceptions IA

Fichiers à créer :

- backend/app/ai/exceptions.py
- backend/tests/ai/test_ai_exceptions.py

Objectif :

Définir les erreurs spécifiques IA.

Exceptions attendues :

- AIProviderError
- AIProviderTimeout
- AIProviderConfigurationError
- AIProviderAuthenticationError
- AIProviderUnavailableError
- AIProviderInvalidResponseError
- AIValidationError
- AIPromptBuildError
- AIPromptTemplateError

Critères de validation :

- chaque exception peut être levée ;
- chaque exception hérite d'une exception IA commune ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_ai_exceptions.py -q

---

### Étape 3 - Créer l'interface provider

Fichiers à créer :

- backend/app/ai/interfaces.py
- backend/tests/ai/test_ai_provider_interface.py

Objectif :

Définir le contrat commun des fournisseurs IA.

Interface attendue :

AIProvider

Méthode attendue :

generate_explanation(request: AIProviderRequest) -> AIProviderResponse

Critères de validation :

- l'interface est importable ;
- un provider fictif peut l'implémenter ;
- la méthode attendue existe ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_ai_provider_interface.py -q

---

### Étape 4 - Créer les validateurs

Fichiers à créer :

- backend/app/ai/validators/**init**.py
- backend/app/ai/validators/context_validator.py
- backend/app/ai/validators/response_validator.py
- backend/tests/ai/test_ai_validators.py

Objectif :

Valider les données avant et après appel provider.

ContextValidator doit vérifier :

- score présent ;
- score entre 0 et 100 ;
- recommendation présente ;
- verdict présent ;
- job_title présent ;
- strengths est une liste ;
- weaknesses est une liste.

ResponseValidator doit vérifier :

- summary présent ;
- detailed_explanation présent ;
- action_plan présent ;
- action_plan est une liste ;
- summary non vide ;
- detailed_explanation non vide.

Critères de validation :

- contexte valide accepté ;
- contexte invalide rejeté ;
- réponse valide acceptée ;
- réponse invalide rejetée ;
- les erreurs restent contrôlées ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_ai_validators.py -q

---

### Étape 5 - Créer le PromptBuilder

Fichiers à créer :

- backend/app/ai/prompts/**init**.py
- backend/app/ai/prompts/prompt_templates.py
- backend/app/ai/prompts/prompt_builder.py
- backend/tests/ai/test_ai_prompt_builder.py

Objectif :

Construire un prompt déterministe à partir d'un AIExplanationContext validé.

Le PromptBuilder doit :

- recevoir un contexte ;
- recevoir une version de prompt ;
- utiliser un template ;
- injecter les données autorisées ;
- inclure les règles anti-hallucination ;
- inclure le format de sortie attendu ;
- retourner un prompt utilisable.

Critères de validation :

- prompt non vide ;
- prompt inclut le score ;
- prompt inclut la recommendation ;
- prompt inclut le verdict ;
- prompt inclut les règles anti-hallucination ;
- prompt inclut le format JSON attendu ;
- prompt conserve prompt_version ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_ai_prompt_builder.py -q

---

### Étape 6 - Créer le MockAIProvider

Fichiers à créer :

- backend/app/ai/providers/**init**.py
- backend/app/ai/providers/mock_provider.py
- backend/tests/ai/test_mock_ai_provider.py

Objectif :

Créer un provider déterministe sans appel réseau.

MockAIProvider doit :

- implémenter AIProvider ;
- retourner une réponse stable ;
- ne jamais appeler Internet ;
- ne jamais nécessiter de clé API ;
- permettre les tests de AIExplanationService.

Réponse mock attendue :

summary :

This opportunity is aligned with the provided matching result.

detailed_explanation :

The deterministic score indicates an alignment based on the provided strengths and weaknesses.

action_plan :

- Review the listed weaknesses.
- Adapt the application material accordingly.
- Use the deterministic summary as the main decision support.

Critères de validation :

- réponse déterministe ;
- structure AIProviderResponse valide ;
- aucun appel réseau ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_mock_ai_provider.py -q

---

### Étape 7 - Créer AIExplanationService

Fichiers à créer :

- backend/app/ai/services.py
- backend/tests/ai/test_ai_explanation_service.py

Objectif :

Orchestrer la génération d'une explication IA à partir d'un provider mock.

AIExplanationService doit :

- recevoir un contexte déterministe ;
- valider le contexte ;
- construire le prompt ;
- appeler le provider injecté ;
- valider la réponse ;
- produire AIExplanation ;
- retourner AIExplanationResult.

Le service ne doit jamais :

- calculer le score ;
- modifier le score ;
- modifier le verdict ;
- modifier la recommendation ;
- appeler directement un provider concret externe ;
- accéder à PostgreSQL ;
- dépendre de FastAPI ;
- dépendre du frontend.

Critères de validation :

- succès avec contexte valide et MockAIProvider ;
- échec propre avec contexte invalide ;
- échec propre si provider lève une erreur ;
- aucun score modifié ;
- prompt_version conservée ;
- provider_name conservé ;
- model_name conservé ;
- les tests passent.

Commande de validation :

pytest backend/tests/ai/test_ai_explanation_service.py -q

---

### Étape 8 - Suite de tests complète

Commande :

pytest backend/tests/ai -q

Puis :

pytest -q

Critères de réussite :

- tous les tests IA passent ;
- toute la suite backend passe ;
- aucune régression détectée.

## Ordre de commit recommandé

Selon la règle officielle du projet :

Une feature technique doit être commitée avec le code et les tests associés.

Pour cette première implémentation IA, je recommande un commit unique pour le socle IA local :

Commit technique :

feat: add ai explanation domain foundation

Contenu :

- backend/app/ai/
- backend/tests/ai/

Ne pas mélanger avec :

- documentation de clôture ;
- frontend ;
- endpoints FastAPI ;
- provider réel.

## Documentation de clôture attendue après code

Après validation technique, mettre à jour :

- docs/project-status.md
- docs/roadmap.md
- docs/handoff-prompt.md

Puis commit documentaire séparé :

docs: synchronize ai explanation domain foundation

## Critères de fin de phase 7.1.1

La phase 7.1.1 pourra être considérée comme terminée lorsque :

- le package backend/app/ai existe ;
- les schémas IA existent ;
- les interfaces IA existent ;
- les exceptions IA existent ;
- les validateurs existent ;
- le PromptBuilder existe ;
- le MockAIProvider existe ;
- AIExplanationService existe ;
- les tests IA existent ;
- les tests IA passent ;
- toute la suite backend passe ;
- la documentation est synchronisée ;
- les commits sont réalisés ;
- git status est propre.

## Risques identifiés

### Risque 1

Surcomplexifier le domaine IA trop tôt.

Mitigation :

premier incrément local et mock uniquement.

### Risque 2

Introduire un provider réel avant d'avoir un socle propre.

Mitigation :

interdiction d'OpenAI et Azure OpenAI pendant cette phase.

### Risque 3

Mélanger design et code.

Mitigation :

ce document clôture le design d'implémentation avant le code.

### Risque 4

Mélanger code et documentation dans le même commit.

Mitigation :

commit technique séparé du commit documentaire.

## Décisions de phase

DEC-AI-001

Le premier incrément IA utilise uniquement un provider mock.

DEC-AI-002

Aucun appel réseau n'est autorisé dans les tests IA.

DEC-AI-003

AIExplanationService reçoit un provider injecté.

DEC-AI-004

AIExplanationService ne dépend pas de FastAPI.

DEC-AI-005

AIExplanationService ne dépend pas de SQLAlchemy.

DEC-AI-006

PromptBuilder conserve le prompt_version.

DEC-AI-007

La réponse IA est représentée par AIExplanationResult.

## Prochaine étape

Phase 7.1.8

AI Domain Implementation

Objectif :

Créer le package backend/app/ai et les tests associés selon le plan défini dans ce document.

Aucun fournisseur réel ne doit être intégré pendant cette phase.
