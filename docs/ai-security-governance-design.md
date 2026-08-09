# AI Security & Governance Design

## Phase

7.0.6 AI Security & Governance Design

## Statut

Design

## Contexte

Les phases précédentes ont défini :

- AI Score Explanation Design
- AI Explanation Backend Design
- AI Prompt Architecture Design
- AI Explanation API Design
- AI Provider Strategy Design

L'architecture fonctionnelle et technique de la couche IA est désormais définie.

Avant toute implémentation réelle d'un fournisseur LLM, il est nécessaire de définir les règles de sécurité, de confidentialité, de gouvernance et de traçabilité.

Cette phase ne doit produire aucun code.

Aucun fournisseur IA ne doit être intégré durant cette phase.

## Objectif

Définir :

- les règles de sécurité ;
- les règles de confidentialité ;
- les règles de gouvernance ;
- les règles de traçabilité ;
- les règles d'audit ;
- les responsabilités des composants IA.

## Principe fondamental

Le système de matching reste la source officielle de vérité.

Le LLM est considéré comme :

- un composant auxiliaire ;
- un système potentiellement faillible ;
- un système non autoritaire ;
- un système non décisionnel.

Le LLM n'a pas l'autorité de modifier une décision métier.

## Classification des données

### Niveau 1

Données publiques

Exemples :

- titre du poste ;
- description publique de l'offre ;
- nom de l'entreprise publié par l'offre.

Peu de restrictions.

### Niveau 2

Données utilisateur

Exemples :

- compétences ;
- expériences ;
- certifications ;
- préférences de recherche.

Transmission strictement limitée au besoin métier.

### Niveau 3

Données sensibles

Exemples :

- mots de passe ;
- refresh tokens ;
- clés API ;
- secrets ;
- informations techniques internes.

Transmission interdite.

## Données autorisées vers le LLM

Le LLM peut recevoir :

- score calculé ;
- strengths ;
- weaknesses ;
- recommendation ;
- verdict ;
- titre du poste ;
- résumé de l'offre ;
- informations strictement nécessaires à l'explication.

## Données interdites vers le LLM

Interdiction absolue de transmettre :

- JWT ;
- mots de passe ;
- tokens OAuth ;
- clés API ;
- variables d'environnement ;
- logs techniques ;
- stack traces ;
- chaînes de connexion base de données ;
- historique complet des candidatures ;
- informations système internes.

## Gestion des secrets

Tous les secrets doivent être stockés uniquement dans :

.env

Interdictions :

- hardcode dans le code ;
- commit Git ;
- documentation ;
- prompts ;
- logs.

## Rotation des secrets

Les secrets doivent pouvoir être remplacés sans modification du code.

Architecture cible :

Settings
↓
Environment Variables
↓
Provider Adapter

## Gouvernance IA

Le système détermine :

- score ;
- classement ;
- matching ;
- recommandation.

L'IA explique uniquement les résultats.

L'IA ne décide pas.

## Validation des entrées

Avant appel IA :

Vérifier :

- score présent ;
- recommendation présente ;
- verdict présent ;
- objet valide.

Si validation échoue :

pas d'appel IA.

## Validation des sorties

Après réponse IA :

Vérifier :

- structure attendue ;
- champs obligatoires ;
- longueur raisonnable ;
- absence de contenu vide.

Si validation échoue :

ai_explanation = null

## Politique anti-hallucination

Règle 1

Le LLM n'utilise que les données fournies.

Règle 2

Le LLM ne doit pas extrapoler.

Règle 3

Le LLM ne doit pas inventer de compétences.

Règle 4

Le LLM ne doit pas inventer d'expérience.

Règle 5

Le LLM ne doit pas modifier le score.

Règle 6

Le LLM ne doit pas modifier le verdict.

## Auditabilité

Chaque réponse IA doit pouvoir être reliée à :

- model_name ;
- provider_name ;
- prompt_version ;
- generated_at.

Objectif :

reproductibilité des analyses.

## Journalisation autorisée

Autorisé :

- timestamp ;
- provider ;
- durée ;
- statut ;
- version du prompt ;
- version du modèle.

## Journalisation interdite

Interdit :

- prompt complet ;
- données privées ;
- tokens ;
- secrets ;
- réponses sensibles.

## Traçabilité

Conserver :

- provider_name
- model_name
- prompt_version
- generated_at

Permet :

- audit ;
- comparaison ;
- amélioration future.

## Gestion des erreurs

Cas :

- timeout ;
- erreur réseau ;
- indisponibilité fournisseur ;
- réponse invalide.

Comportement :

ai_explanation = null

Le reste du système fonctionne normalement.

## Politique de disponibilité

Le matching doit fonctionner même si :

- le fournisseur IA est arrêté ;
- le fournisseur IA est indisponible ;
- le fournisseur IA est supprimé.

Le système ne doit jamais dépendre d'un LLM pour fonctionner.

## Contrôle des coûts

Les appels IA doivent être limités à :

consultation du détail d'une opportunité.

Interdictions :

- appels de masse ;
- génération systématique ;
- génération sur dashboard ;
- génération sur liste.

## Conformité du projet

Le projet doit respecter :

- principe de minimisation des données ;
- principe du moindre privilège ;
- séparation des responsabilités ;
- traçabilité ;
- auditabilité.

## Responsabilités

### Matching Engine

Responsable :

- score ;
- ranking ;
- analyse.

### AIExplanationService

Responsable :

- orchestration IA ;
- validation ;
- contrôle qualité.

### Provider Adapter

Responsable :

- communication fournisseur.

### Frontend

Responsable :

- affichage uniquement.

## Validation attendue

La phase est terminée lorsque :

- règles de sécurité documentées ;
- règles de confidentialité documentées ;
- gouvernance documentée ;
- traçabilité documentée ;
- auditabilité documentée ;
- gestion des erreurs documentée.

Aucun code ne doit être produit pendant cette phase.

## Hors périmètre

Ne pas implémenter :

- fournisseur IA ;
- stockage d'explications ;
- cache réel ;
- chiffrement applicatif ;
- RBAC avancé ;
- gestion multi-tenant ;
- RAG ;
- embeddings ;
- agents.

## Livrable

- docs/ai-security-governance-design.md

## Étape suivante recommandée

Phase 7.0 Review

Objectif :

Réaliser une revue complète de tous les documents de la phase 7.0 afin de vérifier :

- cohérence fonctionnelle ;
- cohérence technique ;
- cohérence sécurité ;
- cohérence API ;
- cohérence roadmap ;

avant toute ligne de code liée à l'IA.
