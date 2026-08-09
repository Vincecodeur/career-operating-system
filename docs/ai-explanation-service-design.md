# AI Explanation Service Design

## Phase

7.1.5 AI Explanation Service Design

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- AI Explanation Domain Design
- AI Explanation Backend Package Design
- AI Explanation Schema Design
- AI Provider Interface Design

Le projet dispose maintenant d'une vision claire des objets métier IA, des schémas attendus, de la structure backend cible et du contrat fournisseur IA.

Cette phase définit précisément le rôle de AIExplanationService avant toute implémentation.

Aucun code ne doit être produit pendant cette phase.

Aucun fournisseur IA réel ne doit être intégré.

Aucun appel LLM ne doit être développé.

## Objectif

Définir :

- les responsabilités de AIExplanationService ;
- ses entrées ;
- ses sorties ;
- son orchestration interne ;
- ses interactions avec les schémas ;
- ses interactions avec le provider ;
- sa stratégie de validation ;
- sa stratégie de gestion d'erreur ;
- sa stratégie de test.

## Principe fondamental

AIExplanationService ne calcule jamais :

- le score ;
- le ranking ;
- les strengths ;
- les weaknesses ;
- le verdict ;
- la recommendation.

Ces éléments sont produits par les moteurs déterministes existants.

AIExplanationService consomme uniquement ces résultats pour demander une explication textuelle.

## Position dans l'architecture

Pipeline cible :

Matching Engine
↓
Opportunity Analysis
↓
AIExplanationContext
↓
AIExplanationService
↓
Prompt Builder
↓
AIProvider
↓
AIProviderResponse
↓
AIExplanation
↓
API Response

## Rôle principal

AIExplanationService orchestre la génération d'explications IA.

Il ne contient pas de logique de matching.

Il ne contient pas de logique de scoring.

Il ne contient pas de logique de ranking.

Il transforme un résultat déterministe en explication utilisateur.

## Responsabilités autorisées

AIExplanationService peut :

- recevoir des données déterministes ;
- construire un AIExplanationContext ;
- vérifier que le contexte est exploitable ;
- construire une AIProviderRequest ;
- appeler un AIProvider ;
- recevoir une AIProviderResponse ;
- valider la réponse ;
- produire un AIExplanation ;
- retourner un AIExplanationResult.

## Responsabilités interdites

AIExplanationService ne doit jamais :

- recalculer un score ;
- modifier un score ;
- modifier une recommendation ;
- modifier un verdict ;
- inventer une strength ;
- inventer une weakness ;
- accéder directement à React ;
- accéder directement aux composants frontend ;
- appeler directement OpenAI ;
- appeler directement Azure OpenAI ;
- écrire directement en base de données ;
- lire directement les modèles SQLAlchemy.

## Entrées attendues

AIExplanationService doit recevoir des données déjà calculées.

Entrée conceptuelle :

- job_title
- score
- strengths
- weaknesses
- recommendation
- verdict
- deterministic_summary

Ces données peuvent provenir de :

- MatchingResult
- OpportunityAnalysis
- JobOffer
- Candidate Profile

La phase d'implémentation devra définir précisément les objets source utilisés.

## Sortie attendue

AIExplanationService retourne :

AIExplanationResult

Avec deux cas possibles.

### Cas succès

success = true

explanation = AIExplanation

error_message = null

### Cas échec

success = false

explanation = null

error_message = message contrôlé

## Objet principal produit

AIExplanation

Champs attendus :

- summary
- detailed_explanation
- action_plan
- generated_at
- provider_name
- model_name
- prompt_version

## Flux nominal

Étape 1

Recevoir les données déterministes.

Étape 2

Construire AIExplanationContext.

Étape 3

Valider AIExplanationContext.

Étape 4

Construire le prompt.

Étape 5

Construire AIProviderRequest.

Étape 6

Appeler AIProvider.generate_explanation().

Étape 7

Recevoir AIProviderResponse.

Étape 8

Valider AIProviderResponse.

Étape 9

Construire AIExplanation.

Étape 10

Retourner AIExplanationResult.

## Flux d'erreur

Si le contexte est invalide :

- pas d'appel provider ;
- retour AIExplanationResult(success=false).

Si le provider échoue :

- capturer l'exception ;
- retour AIExplanationResult(success=false).

Si la réponse provider est invalide :

- retour AIExplanationResult(success=false).

Le reste du système doit continuer à fonctionner.

## Validation du contexte

Avant appel provider, vérifier :

- score présent ;
- score compris entre 0 et 100 ;
- recommendation présente ;
- verdict présent ;
- job_title présent ;
- strengths est une liste ;
- weaknesses est une liste.

Si une validation échoue :

aucun appel IA.

## Validation de la réponse provider

Après retour provider, vérifier :

- summary présent ;
- detailed_explanation présent ;
- action_plan présent ;
- action_plan est une liste ;
- summary non vide ;
- detailed_explanation non vide.

Si une validation échoue :

AIExplanationResult(success=false)

## Gestion du provider

AIExplanationService ne doit pas connaître le provider concret.

Interdit :

- OpenAIProvider importé directement ;
- AzureOpenAIProvider importé directement.

Autorisé :

- dépendre de AIProvider ;
- recevoir un provider injecté ;
- utiliser une factory dans une phase ultérieure.

## Injection de dépendance

Décision recommandée :

AIExplanationService reçoit un AIProvider en paramètre.

Objectif :

- testabilité ;
- découplage ;
- remplacement facile du fournisseur ;
- utilisation d'un MockAIProvider en tests.

## Prompt Builder

AIExplanationService ne doit pas contenir directement les templates longs.

Il doit s'appuyer sur :

PromptBuilder

Responsabilités du PromptBuilder :

- assembler le prompt ;
- injecter le contexte ;
- appliquer la version du prompt.

AIExplanationService orchestre.

PromptBuilder construit.

AIProvider exécute.

## Versionnement

AIExplanationService doit conserver :

- prompt_version ;
- provider_name ;
- model_name.

Ces informations doivent être transmises vers AIExplanation.

Objectif :

- traçabilité ;
- auditabilité ;
- comparaison future.

## Gestion des erreurs provider

Exceptions attendues :

- AIProviderError
- AIProviderTimeout
- AIProviderConfigurationError
- AIProviderAuthenticationError
- AIProviderUnavailableError
- AIProviderInvalidResponseError

AIExplanationService doit capturer ces erreurs.

Aucune exception provider ne doit remonter jusqu'au frontend.

## Résultat en cas d'erreur

Exemple :

AIExplanationResult(
success=false,
explanation=null,
error_message="AI explanation unavailable"
)

Le message doit rester contrôlé.

Ne jamais transmettre :

- stack trace ;
- secret ;
- token ;
- prompt complet.

## Politique de fallback

Si l'IA échoue :

- le score reste visible ;
- l'opportunity analysis reste visible ;
- l'interface reste utilisable ;
- ai_explanation peut être null.

L'IA est un enrichissement.

L'IA n'est pas une dépendance critique.

## Logging

Logs autorisés :

- provider_name ;
- model_name ;
- prompt_version ;
- duration_ms ;
- success ;
- error_type.

Logs interdits :

- prompt complet ;
- contexte complet ;
- données privées inutiles ;
- tokens ;
- secrets ;
- variables d'environnement.

## Cache

Le cache est hors périmètre de cette phase.

Cependant, AIExplanationService doit être conçu pour permettre un cache futur.

Clé future possible :

profile_id

- job_offer_id
- matching_version
- prompt_version

Aucune implémentation cache pendant cette phase.

## Persistance

La persistance des explications IA est hors périmètre.

AIExplanationService doit retourner un objet en mémoire.

Le stockage éventuel sera étudié dans une phase ultérieure.

## Configuration

Paramètres futurs utilisés par le service :

- AI_ENABLED
- AI_PROVIDER
- AI_TIMEOUT_SECONDS
- AI_PROMPT_VERSION
- AI_MODEL_NAME

Ces paramètres ne sont pas obligatoirement implémentés pendant cette phase.

## Cas AI désactivée

Si AI_ENABLED = false :

AIExplanationService doit pouvoir retourner :

AIExplanationResult(
success=false,
explanation=null,
error_message="AI explanation disabled"
)

Ce comportement est utile pour :

- environnement local ;
- tests ;
- contrôle de coût ;
- rollback.

## Tests futurs attendus

Fichier probable :

backend/tests/ai/test_ai_explanation_service.py

Tests recommandés :

### Test 1

Service retourne une explanation en cas de provider valide.

### Test 2

Service retourne success=false si le contexte est invalide.

### Test 3

Service retourne success=false si le provider lève une erreur.

### Test 4

Service ne modifie jamais le score d'entrée.

### Test 5

Service n'appelle pas le provider si AI_ENABLED=false.

### Test 6

Service conserve provider_name, model_name et prompt_version.

### Test 7

Service supporte MockAIProvider.

## MockAIProvider attendu

Pour les tests, utiliser un provider déterministe.

Réponse type :

summary = "This opportunity is aligned with the provided matching result."

detailed_explanation = "The deterministic score indicates a strong match based on the provided strengths and weaknesses."

action_plan = [
"Review the listed weaknesses.",
"Adapt the application material accordingly."
]

Aucun appel réseau.

## Séquence de test cible

Préparer contexte
↓
Injecter MockAIProvider
↓
Appeler AIExplanationService
↓
Vérifier AIExplanationResult
↓
Vérifier AIExplanation
↓
Vérifier aucun score modifié

## Règles anti-hallucination côté service

AIExplanationService doit empêcher l'IA de recevoir des données non nécessaires.

Le contexte transmis doit être réduit à :

- job_title ;
- score ;
- strengths ;
- weaknesses ;
- recommendation ;
- verdict ;
- deterministic summary.

Aucune donnée sensible.

Aucun secret.

Aucun historique complet.

## Relation avec FastAPI

AIExplanationService ne doit pas dépendre de FastAPI.

Les routes FastAPI appelleront le service plus tard.

Le service doit rester testable indépendamment de l'API.

## Relation avec SQLAlchemy

AIExplanationService ne doit pas dépendre de SQLAlchemy.

Les objets doivent être déjà préparés avant d'appeler le service.

Objectif :

éviter couplage infrastructure / domaine.

## Relation avec Frontend

AIExplanationService ne connaît pas le frontend.

Il produit des objets backend.

Le frontend affichera les résultats via API.

## Critères de validation de cette phase

Cette phase sera considérée terminée lorsque :

- responsabilités du service définies ;
- entrées définies ;
- sorties définies ;
- flux nominal défini ;
- flux d'erreur défini ;
- dépendances autorisées définies ;
- dépendances interdites définies ;
- stratégie de test définie ;
- stratégie de fallback définie ;
- règles de sécurité définies.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- AIExplanationService ;
- MockAIProvider ;
- PromptBuilder ;
- OpenAIProvider ;
- AzureOpenAIProvider ;
- endpoints FastAPI ;
- frontend ;
- cache ;
- persistance ;
- appels LLM ;
- RAG ;
- embeddings ;
- agents.

## Livrable

- docs/ai-explanation-service-design.md

## Étape suivante recommandée

Phase 7.1.6

AI Prompt Builder Design

Objectif :

Définir précisément le rôle du PromptBuilder, la structure des templates, la validation des prompts, le versionnement et les règles anti-hallucination avant toute implémentation.
