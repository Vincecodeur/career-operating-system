# AI Explanation Domain Design

## Phase

7.1.1 AI Explanation Domain Design

## Statut

Design

## Contexte

Les phases 7.0 ont défini :

- la vision fonctionnelle ;
- l'architecture IA ;
- l'architecture backend ;
- l'architecture API ;
- la stratégie fournisseur ;
- la sécurité ;
- la gouvernance.

La phase 7.0 est validée et clôturée.

L'objectif de cette phase est de définir les objets métier et les structures backend nécessaires avant la première ligne de code.

Aucun fournisseur IA ne sera intégré pendant cette phase.

Aucun appel LLM ne sera implémenté.

## Objectif

Définir :

- les objets métier IA ;
- les schémas Pydantic ;
- les contrats internes ;
- les interfaces ;
- l'organisation des dossiers ;
- les dépendances.

## Principe fondamental

Le domaine IA ne calcule jamais :

- le score ;
- le ranking ;
- les strengths ;
- les weaknesses ;
- le verdict ;
- la recommendation.

Ces éléments proviennent exclusivement du moteur déterministe.

Le domaine IA consomme ces résultats.

## Architecture cible

Profile

- Job Offer
  ↓
  Matching Engine
  ↓
  Opportunity Analysis
  ↓
  AI Explanation Domain
  ↓
  AI Provider
  ↓
  AI Explanation

## Domaine principal

AIExplanation

Objectif :

représenter une explication produite par la couche IA.

## AIExplanation

Attributs :

- summary
- detailed_explanation
- action_plan
- generated_at
- provider_name
- model_name
- prompt_version

## Description des champs

### summary

Type :

string

Objectif :

résumé court destiné à une lecture rapide.

### detailed_explanation

Type :

string

Objectif :

explication détaillée.

### action_plan

Type :

list[string]

Objectif :

actions suggérées.

### generated_at

Type :

datetime

Objectif :

date de génération.

### provider_name

Type :

string

Objectif :

fournisseur utilisé.

### model_name

Type :

string

Objectif :

modèle utilisé.

### prompt_version

Type :

string

Objectif :

version du prompt.

## Objet contexte IA

AIExplanationContext

Objectif :

regrouper les données transmises à l'IA.

## AIExplanationContext

Attributs :

- job_title
- score
- strengths
- weaknesses
- recommendation
- verdict
- summary

## Description

Le backend construit cet objet.

Le fournisseur IA reçoit uniquement cet objet.

## Objet réponse fournisseur

AIProviderResponse

Objectif :

normaliser la réponse d'un fournisseur.

## AIProviderResponse

Attributs :

- summary
- detailed_explanation
- action_plan

Aucune donnée métier.

Aucun score.

Aucune recommandation.

## Objet requête fournisseur

AIProviderRequest

Objectif :

normaliser les appels fournisseur.

## AIProviderRequest

Attributs :

- prompt
- prompt_version
- context

## Interface principale

AIProvider

Objectif :

abstraction fournisseur.

## Responsabilités

- génération explication ;
- appel fournisseur ;
- retour normalisé.

## Méthode prévue

generate_explanation()

Entrée :

AIProviderRequest

Sortie :

AIProviderResponse

## Service principal

AIExplanationService

Objectif :

orchestration du domaine IA.

## Responsabilités

- construire le contexte ;
- construire le prompt ;
- appeler le provider ;
- valider la réponse ;
- produire AIExplanation.

## Responsabilités interdites

- calcul score ;
- ranking ;
- matching ;
- opportunity analysis.

## Factory future

AIProviderFactory

Objectif :

sélection du fournisseur actif.

Exemple futur :

settings
↓
provider_name
↓
factory
↓
provider

## Structure backend proposée

backend/app/ai/

Contenu :

- schemas.py
- interfaces.py
- services.py
- providers/
- prompts/

## providers/

Contiendra plus tard :

- base.py
- openai_provider.py
- azure_openai_provider.py

Aucun de ces fichiers n'est implémenté pendant cette phase.

## prompts/

Contiendra plus tard :

- prompt_builder.py
- prompt_templates.py

Aucun code pendant cette phase.

## Schemas Pydantic prévus

AIExplanation

AIExplanationContext

AIProviderRequest

AIProviderResponse

## Dépendances autorisées

Le domaine IA peut dépendre de :

- matching schemas ;
- opportunity analysis schemas ;
- configuration.

## Dépendances interdites

Le domaine IA ne doit pas dépendre :

- React ;
- frontend ;
- SQLAlchemy models ;
- endpoints FastAPI.

## Gestion d'erreur

Objet :

AIExplanationResult

Attributs :

- success
- explanation
- error_message

Objectif :

encapsuler proprement les erreurs IA.

## Validation

Les validations minimales :

### Contexte

- score présent ;
- recommendation présente ;
- verdict présent.

### Réponse

- summary présent ;
- structure valide ;
- longueur acceptable.

## Extension future

Le domaine doit permettre plus tard :

- multilingue ;
- plusieurs fournisseurs ;
- cache ;
- persistance éventuelle.

Sans modifier les contrats principaux.

## Critères de validation

Cette phase sera terminée lorsque :

- les objets métier sont définis ;
- les schémas sont définis ;
- les interfaces sont définies ;
- les services sont définis ;
- l'organisation des dossiers est définie ;
- les dépendances sont définies.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- OpenAI ;
- Azure OpenAI ;
- appels HTTP ;
- prompts réels ;
- cache ;
- persistance ;
- frontend ;
- RAG ;
- embeddings ;
- agents.

## Livrable

- docs/ai-explanation-domain-design.md

## Étape suivante recommandée

Phase 7.1.2

AI Explanation Backend Package Design

Objectif :

Définir précisément les fichiers Python, responsabilités par module, imports, dépendances internes et plan d'implémentation avant l'écriture du premier code IA.
