## AI Context Contract Design

### Phase

7.1.23.11 AI Context Contract

### Statut

Completed

### Objectif

Définir quelles données peuvent être transmises à l'AI Career Advisor.

Le contrat AI constitue le périmètre officiel des données accessibles à l'IA.

### Principe fondamental

Le profil structuré est la source de vérité.

Le CV n'est jamais une source de vérité.

Les données non validées ne doivent jamais être transmises à l'IA.

L'IA ne doit jamais inventer d'information.

L'IA ne doit jamais modifier les données métier.

### Source de vérité

Source autorisée :

- Profile
- Hard Skills
- Soft Skills
- Languages
- Certifications
- Work Experiences
- Additional Profile Context

Source interdite :

- CV brut
- Texte extrait du CV
- Données d'enrichissement non validées
- Propositions d'enrichissement en attente

### Données autorisées

### Profile Identity

Données autorisées :

- current_title
- location
- years_of_experience

Le full_name reste disponible dans le profil structuré mais n’est pas transmis par défaut au fournisseur IA dans le contrat MVP.

Toute future transmission du full_name nécessitera un besoin fonctionnel explicite et documenté.

#### Career Objectives

- target_role_short_term
- target_role_long_term

#### Hard Skills

Toutes les compétences validées du profil.

#### Soft Skills

Toutes les soft skills validées.

#### Languages

Toutes les langues validées.

#### Certifications

Toutes les certifications validées.

#### Work Experiences

Toutes les expériences validées.

Données autorisées :

- company_name
- job_title
- start_date
- end_date
- description

#### Additional Profile Context

- professional_summary
- career_motivations
- preferred_environment
- non_negotiables
- additional_context

### Données explicitement interdites

Ne jamais transmettre :

- JWT
- tokens OAuth
- API keys
- mots de passe
- variables .env
- secrets applicatifs
- logs techniques
- stack traces
- données internes du système
- historique complet des candidatures
- données non validées

### Rôle autorisé de l'IA

L'IA peut :

- expliquer
- conseiller
- reformuler
- suggérer des actions
- suggérer des pistes de progression

L'IA ne peut jamais :

- modifier un profil
- modifier un score
- recalculer un matching
- recalculer un verdict
- créer une compétence
- créer une expérience
- créer une certification
- créer une langue

### AI Readiness

Mode retenu :

STRICT

Un profil est AI Ready uniquement si les éléments suivants existent :

- current_title
- au moins une compétence
- au moins une expérience
- au moins une langue
- professional_summary renseigné
- career_motivations renseigné
- preferred_environment renseigné
- non_negotiables renseigné
- additional_context renseigné

### Contrat cible

Objet conceptuel :

AIProfileContext

Sections :

- Identity
- Career Goals
- Hard Skills
- Soft Skills
- Languages
- Certifications
- Experiences
- Additional Context

### Compatibilité avec le domaine AI actuel

AIExplanationContext reste utilisé pour AI Explanation.

AIProfileContext sera utilisé par AI Career Advisor.

Les deux contrats restent séparés.

### Gouvernance

Toutes les données envoyées à l'IA doivent être :

- validées
- explicables
- auditables
- traçables

Le profil structuré reste la source officielle de vérité.

### Critères de validation

Cette phase est terminée lorsque :

- les données autorisées sont définies ;
- les données interdites sont définies ;
- la source de vérité est définie ;
- les critères AI Ready sont définis ;
- le rôle autorisé de l'IA est défini ;
- le contrat cible est défini ;
- la gouvernance est définie.

#### Implementation Status

Completed

Implemented through:

- backend/app/ai/context_schemas.py
- backend/app/ai/context_service.py
- backend/app/ai/router.py
- backend/app/settings/schemas.py
- backend/app/settings/service.py
- backend/app/settings/router.py
- backend/app/main.py

Validation:

- explicit AI Context Preview contract implemented
- STRICT AI Readiness implemented
- AI settings disabled by default
- explicit consent persistence implemented
- raw CV exclusion implemented
- unvalidated enrichment exclusion implemented
- application history exclusion implemented
- technical secrets exclusion implemented
- 59 AI tests passed
- 304 backend tests passed

Technical commit:

2cc84d3 - feat(ai): add AI context preview, readiness and consent backend
