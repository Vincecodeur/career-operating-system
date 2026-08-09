# AI Provider Interface Design

## Phase

7.1.4 AI Provider Interface Design

## Statut

Design

## Contexte

Le projet Career Operating System a validé :

- AI Score Explanation Design
- AI Explanation Backend Design
- AI Prompt Architecture Design
- AI Explanation API Design
- AI Provider Strategy Design
- AI Security & Governance Design
- AI Explanation Domain Design
- AI Explanation Backend Package Design
- AI Explanation Schema Design

Le prochain objectif est de définir précisément le contrat des fournisseurs IA avant toute implémentation technique.

Aucun code ne doit être produit pendant cette phase.

Aucun fournisseur réel ne doit être intégré.

## Objectif

Définir :

- les interfaces ;
- les responsabilités ;
- les contrats ;
- les points d'extension ;
- les règles d'erreur ;
- les exigences de testabilité ;
- les contraintes de sécurité ;
- les futures implémentations.

## Principes architecturaux

Principe 1

Les fournisseurs sont remplaçables.

Principe 2

Le service métier ne dépend jamais d'un SDK spécifique.

Principe 3

Le backend ne connaît que l'interface AIProvider.

Principe 4

La logique métier reste indépendante de la technologie IA utilisée.

Principe 5

Un changement de fournisseur ne doit provoquer aucun changement :

- dans le frontend ;
- dans l'API ;
- dans le matching ;
- dans l'Opportunity Analysis.

## Architecture cible

AIExplanationService
↓
AIProvider Interface
↓
Provider Factory
↓
Concrete Provider
↓
External LLM

## Interface principale

Nom :

AIProvider

Responsabilité :

Définir le contrat commun de tous les fournisseurs.

## Méthode obligatoire

generate_explanation()

Entrée :

AIProviderRequest

Sortie :

AIProviderResponse

Signature conceptuelle :

generate_explanation(request) -> response

## Préconditions

Le provider reçoit :

- un prompt déjà construit ;
- un contexte déjà validé ;
- une configuration déjà validée.

Le provider n'effectue pas ces validations métier.

## AIProviderRequest

Contenu attendu :

- prompt
- prompt_version
- context

Le provider ne modifie jamais ces données.

## AIProviderResponse

Contient :

- summary
- detailed_explanation
- action_plan

Aucun champ métier.

Aucune recommandation.

Aucun score.

## Responsabilités du provider

Le provider est autorisé à :

- envoyer une requête ;
- recevoir une réponse ;
- gérer les timeouts ;
- convertir les formats ;
- remonter les erreurs.

## Responsabilités interdites

Le provider ne doit jamais :

- calculer un score ;
- calculer un ranking ;
- modifier un verdict ;
- modifier une recommendation ;
- modifier une weakness ;
- modifier une strength ;
- lire PostgreSQL ;
- écrire PostgreSQL ;
- communiquer avec React ;
- connaître les routes API.

## Interface secondaire

Nom :

AIProviderCapabilities

Objectif :

décrire les capacités du provider.

Informations futures :

- supports_json_output
- supports_streaming
- supports_function_calling
- max_context_size

MVP :

documentation uniquement.

Aucune implémentation.

## Interface secondaire

Nom :

AIProviderHealth

Objectif :

représenter l'état du provider.

Informations possibles :

- provider_name
- reachable
- tested_at

Hors périmètre MVP.

## Gestion du timeout

Chaque provider doit respecter :

AI_TIMEOUT_SECONDS

Le timeout ne doit jamais être codé en dur.

Le timeout provient de :

settings

## Gestion des erreurs

Famille d'erreurs IA :

AIProviderError

Classe racine.

## AIProviderTimeout

Déclenchée lorsque :

- l'appel dépasse le timeout.

## AIProviderConfigurationError

Déclenchée lorsque :

- provider absent ;
- modèle absent ;
- configuration invalide.

## AIProviderAuthenticationError

Déclenchée lorsque :

- clé API invalide ;
- authentification refusée.

## AIProviderUnavailableError

Déclenchée lorsque :

- fournisseur indisponible ;
- erreur réseau critique.

## AIProviderInvalidResponseError

Déclenchée lorsque :

- structure invalide ;
- données obligatoires absentes.

## Stratégie de propagation

Provider
↓
Exception IA
↓
AIExplanationService
↓
AIExplanationResult

Le système ne doit jamais tomber complètement.

## Factory

Nom :

AIProviderFactory

Responsabilité :

Instancier le fournisseur actif.

Entrée :

provider_name

Sortie :

AIProvider

## Comportement

Si :

provider_name = mock

Retour :

MockAIProvider

Si :

provider_name = openai

Retour :

OpenAIProvider

Si :

provider_name = azure_openai

Retour :

AzureOpenAIProvider

Sinon :

AIProviderConfigurationError

## Fournisseur mock

Nom :

MockAIProvider

Objectif :

Tests.

Le provider mock :

- ne fait aucun appel réseau ;
- retourne toujours la même structure.

Utilité :

- développement ;
- CI ;
- démonstration ;
- validation backend.

## Fournisseur OpenAI

Nom :

OpenAIProvider

Phase future.

Responsabilités :

- conversion requête
- appel API
- parsing réponse

## Fournisseur Azure OpenAI

Nom :

AzureOpenAIProvider

Phase future.

Même contrat que OpenAIProvider.

## Décision de compatibilité

Tous les providers doivent implémenter exactement :

generate_explanation()

Aucune méthode obligatoire supplémentaire.

## Journalisation

Autorisé :

- provider_name
- model_name
- duration_ms
- success
- error_type

Interdit :

- prompts
- secrets
- token
- contexte complet

## Sécurité

Le provider ne connaît jamais :

- JWT
- mots de passe
- variables d'environnement complètes

Il reçoit uniquement :

- configuration utile
- requête IA

## Contrat de testabilité

La totalité des tests doit pouvoir fonctionner :

sans accès Internet

sans clé API

sans fournisseur réel

## Tests attendus

test_provider_interface.py

Validation :

- respect du contrat

test_mock_provider.py

Validation :

- réponse déterministe

test_provider_factory.py

Validation :

- sélection fournisseur

test_provider_errors.py

Validation :

- propagation erreurs

## Contrat de performance

MVP :

objectif principal :

fiabilité

avant :

performance

Le cache sera traité ultérieurement.

## Contrat de versionnement

Chaque réponse doit pouvoir être reliée à :

- provider_name
- model_name
- prompt_version

Objectif :

auditabilité.

## Contrat de compatibilité future

Le design doit permettre :

- changement fournisseur
- fournisseur local
- fournisseur cloud
- plusieurs modèles

sans changement des services métier.

## Séquence d'exécution cible

Opportunity Analysis
↓
AIExplanationContext
↓
Prompt Builder
↓
AIProviderRequest
↓
Provider Factory
↓
Concrete Provider
↓
AIProviderResponse
↓
Response Validator
↓
AIExplanation

## Critères de validation

Cette phase est terminée lorsque :

- interface principale définie ;
- factory définie ;
- erreurs définies ;
- responsabilités définies ;
- interdictions définies ;
- stratégie de test définie ;
- stratégie de sécurité définie ;
- stratégie d'audit définie.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- OpenAI SDK
- Azure SDK
- HTTP Client
- cache
- persistance
- endpoints FastAPI
- frontend
- RAG
- embeddings
- agents

## Livrable

- docs/ai-provider-interface-design.md

## Étape suivante recommandée

Phase 7.1.5

AI Explanation Service Design

Objectif :

Définir complètement AIExplanationService, son orchestration, ses interactions avec les validateurs, les providers, les schémas et les stratégies de gestion d'erreur avant la création du premier code IA.
