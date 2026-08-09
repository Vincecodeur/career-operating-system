# AI Explanation Backend Package Design

## Phase

7.1.2 AI Explanation Backend Package Design

## Statut

Design

## Contexte

La phase 7.1.1 a défini :

- les objets métier ;
- les schémas principaux ;
- les interfaces ;
- les services ;
- les responsabilités ;
- les dépendances.

L'objectif de cette phase est de définir précisément la structure du package backend avant l'écriture du premier code IA.

Aucun fournisseur IA ne sera implémenté pendant cette phase.

Aucun appel réseau ne sera développé.

Aucun endpoint FastAPI ne sera créé.

## Objectif

Définir :

- l'arborescence backend ;
- les responsabilités par fichier ;
- les dépendances internes ;
- les conventions d'import ;
- le plan d'implémentation.

## Principe directeur

Chaque module doit avoir une responsabilité unique.

Le package IA doit être totalement isolé du frontend.

Le package IA doit être faiblement couplé au fournisseur.

## Structure cible

backend/app/ai/

Contenu :

- **init**.py
- schemas.py
- interfaces.py
- services.py
- exceptions.py
- settings.py
- providers/
- prompts/
- validators/

## **init**.py

Responsabilité :

Point d'entrée du package.

Ne doit contenir :

- exports publics.

Ne doit pas contenir :

- logique métier ;
- configuration.

## schemas.py

Responsabilité :

Tous les schémas Pydantic de la couche IA.

Contiendra :

- AIExplanation
- AIExplanationContext
- AIProviderRequest
- AIProviderResponse
- AIExplanationResult

Aucune logique métier.

## interfaces.py

Responsabilité :

Contrats d'abstraction.

Contiendra :

AIProvider

Méthodes :

generate_explanation()

Objectif :

Permettre plusieurs fournisseurs.

## services.py

Responsabilité :

AIExplanationService

Responsabilités :

- construire le contexte ;
- construire la requête fournisseur ;
- appeler le fournisseur ;
- valider la réponse ;
- produire AIExplanation.

Responsabilités interdites :

- calcul des scores ;
- accès direct FastAPI ;
- accès frontend.

## exceptions.py

Responsabilité :

Exceptions spécifiques IA.

Exemples :

AIProviderError

AIProviderTimeout

AIValidationError

AIConfigurationError

Objectif :

Isoler les erreurs IA du reste du système.

## settings.py

Responsabilité :

Paramètres IA.

Exemples :

AI_ENABLED

AI_PROVIDER

AI_TIMEOUT_SECONDS

AI_PROMPT_VERSION

Les secrets ne doivent pas être stockés ici.

Les secrets restent dans :

.env

## providers/

Responsabilité :

Implémentations fournisseur.

## providers/base.py

Contiendra :

classe de base commune.

Objectif :

outillage commun.

## providers/openai_provider.py

Prévu plus tard.

Non implémenté.

## providers/azure_openai_provider.py

Prévu plus tard.

Non implémenté.

## prompts/

Responsabilité :

Gestion des prompts.

## prompts/prompt_builder.py

Responsabilité :

Assembler les prompts.

## prompts/prompt_templates.py

Responsabilité :

Stocker les templates.

## validators/

Responsabilité :

Valider les données.

## validators/context_validator.py

Valider :

- score ;
- verdict ;
- recommendation.

Avant appel IA.

## validators/response_validator.py

Valider :

- structure retour ;
- champs requis ;
- longueurs minimales.

Après appel IA.

## Dépendances autorisées

Le package AI peut dépendre de :

- app.matching
- app.opportunity_analysis
- app.core.settings
- pydantic

## Dépendances interdites

Le package AI ne doit pas dépendre de :

- React
- frontend
- routes FastAPI
- SQLAlchemy models
- PostgreSQL

## Flux d'exécution prévu

Matching Engine
↓
Opportunity Analysis
↓
AIExplanationService
↓
Context Validator
↓
Prompt Builder
↓
Provider
↓
Response Validator
↓
AIExplanation

## Conventions d'import

Autorisé :

from app.ai.schemas import ...

from app.ai.interfaces import ...

from app.ai.services import ...

Interdit :

imports circulaires.

## Plan d'implémentation futur

Étape 1

Créer :

- schemas.py

Étape 2

Créer :

- interfaces.py

Étape 3

Créer :

- exceptions.py

Étape 4

Créer :

- validators/

Étape 5

Créer :

- services.py

Étape 6

Créer :

- providers/base.py

Aucun fournisseur réel à ce stade.

## Tests futurs

Prévoir :

tests/ai/

Contenu :

- test_schemas.py
- test_interfaces.py
- test_context_validator.py
- test_response_validator.py
- test_ai_explanation_service.py

Aucun test n'est implémenté pendant cette phase.

## Critères de validation

La phase sera considérée terminée lorsque :

- la structure package est définie ;
- chaque fichier possède une responsabilité unique ;
- les dépendances sont définies ;
- le flux est défini ;
- le plan d'implémentation est défini.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- FastAPI ;
- endpoints ;
- cache ;
- persistance ;
- frontend ;
- RAG ;
- embeddings ;
- agents.

## Livrable

- docs/ai-explanation-backend-package-design.md

## Étape suivante recommandée

Phase 7.1.3

AI Explanation Schema Design

Objectif :

Définir précisément les schémas Pydantic, leurs champs, validations, contraintes et contrats avant la création du premier fichier Python du domaine IA.
