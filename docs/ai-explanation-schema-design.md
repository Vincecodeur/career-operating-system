# AI Explanation Schema Design

## Phase

7.1.3 AI Explanation Schema Design

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- l'architecture IA globale ;
- le domaine IA ;
- l'organisation du package backend ;
- les responsabilités des composants.

Avant la création du premier fichier Python, les schémas doivent être définis précisément.

Cette phase décrit les contrats qui serviront de référence pour l'implémentation backend.

Aucun code ne doit être produit pendant cette phase.

Aucun fournisseur IA ne doit être intégré.

## Objectif

Définir :

- les schémas Pydantic ;
- leurs champs ;
- leurs contraintes ;
- leurs validations ;
- leurs relations ;
- les contrats internes.

## Principes

Les schémas IA ne remplacent jamais :

- MatchingResult ;
- RankedJobOffer ;
- OpportunityAnalysis.

Ils les complètent uniquement.

Le moteur déterministe reste la source de vérité.

## Schéma AIExplanation

Objectif :

Représenter une explication IA validée et prête à être exposée à l'API.

### Champs

summary

Type :

str

Obligatoire :

oui

Description :

Résumé court destiné à une lecture rapide.

---

detailed_explanation

Type :

str

Obligatoire :

oui

Description :

Explication complète.

---

action_plan

Type :

list[str]

Obligatoire :

oui

Description :

Actions recommandées.

---

generated_at

Type :

datetime

Obligatoire :

oui

Description :

Date de génération.

---

provider_name

Type :

str

Obligatoire :

oui

Description :

Nom du fournisseur IA.

---

model_name

Type :

str

Obligatoire :

oui

Description :

Nom du modèle.

---

prompt_version

Type :

str

Obligatoire :

oui

Description :

Version du prompt.

## Contraintes AIExplanation

summary :

- minimum 20 caractères
- maximum 1000 caractères

detailed_explanation :

- minimum 50 caractères
- maximum 10000 caractères

action_plan :

- minimum 0 élément
- maximum 20 éléments

## Schéma AIExplanationContext

Objectif :

Contexte envoyé au fournisseur IA.

### Champs

job_title

Type :

str

---

score

Type :

int

---

strengths

Type :

list[str]

---

weaknesses

Type :

list[str]

---

recommendation

Type :

str

---

verdict

Type :

str

---

summary

Type :

str

## Contraintes AIExplanationContext

score :

minimum :

0

maximum :

100

strengths :

maximum :

50

weaknesses :

maximum :

50

## Schéma AIProviderRequest

Objectif :

Normaliser tous les appels fournisseur.

### Champs

prompt

Type :

str

---

prompt_version

Type :

str

---

context

Type :

AIExplanationContext

## Contraintes

prompt :

minimum :

1 caractère

prompt_version :

obligatoire

context :

obligatoire

## Schéma AIProviderResponse

Objectif :

Normaliser les réponses fournisseur.

### Champs

summary

Type :

str

---

detailed_explanation

Type :

str

---

action_plan

Type :

list[str]

## Contraintes

summary :

obligatoire

detailed_explanation :

obligatoire

action_plan :

obligatoire

## Schéma AIExplanationResult

Objectif :

Encapsuler les résultats du service IA.

### Champs

success

Type :

bool

---

explanation

Type :

AIExplanation | None

---

error_message

Type :

str | None

## Règles

si :

success = true

alors :

error_message = null

si :

success = false

alors :

explanation = null

## Schéma AIProviderConfiguration

Objectif :

Représenter la configuration active.

### Champs

provider_name

Type :

str

---

model_name

Type :

str

---

timeout_seconds

Type :

int

---

prompt_version

Type :

str

## Contraintes

timeout_seconds :

minimum :

1

maximum :

300

## Compatibilité API

Les schémas doivent être sérialisables en JSON.

Ils doivent être compatibles avec :

- FastAPI ;
- OpenAPI ;
- Swagger.

## Compatibilité future

Les schémas doivent permettre plus tard :

- multilingue ;
- cache ;
- plusieurs fournisseurs ;
- persistance éventuelle.

Sans modification majeure.

## Validations métier

Validation obligatoire :

### AIExplanationContext

- score présent ;
- recommendation présente ;
- verdict présent.

### AIProviderResponse

- summary présent ;
- detailed_explanation présent.

### AIExplanation

- provider_name présent ;
- model_name présent ;
- prompt_version présente.

## Relations

MatchingResult
↓
OpportunityAnalysis
↓
AIExplanationContext
↓
AIProviderResponse
↓
AIExplanation

## Critères de validation

La phase sera terminée lorsque :

- tous les schémas sont définis ;
- tous les champs sont définis ;
- toutes les contraintes sont définies ;
- les relations sont définies ;
- les validations sont définies.

Aucun code produit.

## Hors périmètre

Ne pas implémenter :

- fournisseurs IA ;
- appels HTTP ;
- cache ;
- persistance ;
- FastAPI ;
- frontend ;
- OpenAI ;
- Azure OpenAI.

## Livrable

- docs/ai-explanation-schema-design.md

## Étape suivante recommandée

Phase 7.1.4

AI Provider Interface Design

Objectif :

Définir précisément les interfaces Python, signatures de méthodes, contrats d'entrée et de sortie, ainsi que les règles d'extension fournisseur avant l'écriture du premier code IA.
