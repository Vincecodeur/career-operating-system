# Skill Catalog Mapping Design

## Phase

7.1.16.16 Skill Catalog Mapping Design

---

# 1. Contexte

Le système permet désormais :

- l'upload de CV ;
- le parsing structuré des CV ;
- la génération de propositions d'enrichissement ;
- la validation manuelle des propositions ;
- la résolution des conflits ;
- l'application contrôlée des modifications vers le profil candidat.

Le profil structuré reste la source de vérité du système.

Le workflow actuel applique automatiquement les propositions uniquement lorsqu'elles peuvent être résolues vers une donnée existante du système.

Pour les compétences, le système utilise un catalogue centralisé.

Une proposition de compétence ne peut être acceptée que si elle est associée à une compétence existante du catalogue.

Les compétences inconnues sont actuellement :

- affichées dans le workflow ;
- marquées comme "Not present in skill catalog" ;
- décochées par défaut ;
- exclues de l'enrichissement.

Cette approche protège la qualité du référentiel mais ne permet pas à l'utilisateur de réutiliser facilement une compétence existante lorsqu'une correspondance métier existe.

Exemple :

CV :

Power Automate

Catalogue :

Microsoft Power Automate

Aujourd'hui :

le système considère qu'il s'agit d'une compétence inconnue.

---

# 2. Problème

Le système protège correctement le référentiel mais perd une partie de la valeur du parsing.

Certaines compétences détectées :

- existent conceptuellement ;
- sont déjà représentées dans le catalogue ;
- ne peuvent pas être reliées automatiquement à cause d'une différence de formulation.

Résultat :

Compétence trouvée
↓
Compétence non résolue
↓
Compétence ignorée

L'utilisateur doit ensuite recréer manuellement la compétence dans son profil.

---

# 3. Objectifs

Le système doit permettre :

- d'identifier les compétences non résolues ;
- de proposer un mécanisme de mapping manuel ;
- d'associer une compétence détectée à une compétence existante du catalogue ;
- de conserver la gouvernance du référentiel ;
- d'éviter la création automatique de nouvelles compétences ;
- de conserver le workflow de validation humaine.

---

# 4. Non objectifs

Cette phase ne doit pas :

- créer automatiquement des compétences ;
- créer de nouvelles catégories ;
- modifier le catalogue de compétences ;
- introduire du fuzzy matching ;
- introduire de l'IA ;
- introduire la gestion des synonymes ;
- introduire un workflow d'approbation du catalogue ;
- modifier les règles de gouvernance existantes.

---

# 5. Décisions métier

## DEC-051

Reference Data Governance

Les référentiels sont les sources officielles de vocabulaire.

---

## DEC-052

Repository Resolution Strategy

Ordre de résolution :

- Exact Match
- Normalized Match
- Alias Match

Pas de fuzzy matching.

---

## DEC-053

Les compétences inconnues ne sont pas créées automatiquement.

Le catalogue reste gouverné.

---

# 6. Approche retenue

Option A

Mapping uniquement vers des compétences existantes.

Aucune création automatique.

Aucune création manuelle depuis le workflow CV.

Le catalogue reste administré indépendamment.

---

# 7. User Experience

## Situation actuelle

Power Automate

Not present in skill catalog

☐ Exclue

---

## Nouveau comportement

Power Automate

Not present in skill catalog

Select existing skill

[ Microsoft Power Automate ▼ ]

☑ Include in import

---

## Workflow utilisateur

CV
↓
Analyse
↓
Review

Skill inconnue détectée

↓

Utilisateur sélectionne une skill existante

↓

Le système mémorise le mapping

↓

L'utilisateur applique les modifications

↓

Le profil est enrichi avec la skill existante

---

# 8. Règles métier

## Règle 1

Une compétence inconnue reste décochée par défaut.

---

## Règle 2

Une compétence inconnue ne peut être sélectionnée qu'après mapping.

---

## Règle 3

Le mapping doit pointer vers une skill existante.

---

## Règle 4

La skill du catalogue reste la seule donnée enregistrée dans le profil.

---

## Règle 5

Aucune nouvelle skill n'est créée.

---

## Règle 6

Le mapping concerne uniquement la proposition actuelle.

Il ne modifie pas le catalogue.

---

# 9. Modèle de données

## Objectif

Limiter les changements de schéma.

---

## Option retenue

Aucune migration PostgreSQL.

Aucune nouvelle table.

Aucune nouvelle relation.

---

## Utilisation de l'existant

Le système utilise déjà :

ProfileEnrichmentProposal

et

reference_id

Le mapping utilisateur permet simplement de renseigner :

reference_id

avec l'identifiant de la skill sélectionnée.

---

# 10. Backend Design

## Endpoint réutilisé

POST

/enrichment/{proposal_id}/accept

---

## Données transmises

Exemple :

{
"reference_id": 123
}

---

## Validation

Le backend doit vérifier :

- la proposition existe ;
- la proposition est de type SKILL ;
- la skill existe ;
- la skill est active ;
- le mapping est valide.

---

## Résultat

Le système crée :

ProfileSkill

en utilisant la skill sélectionnée.

---

# 11. Frontend Design

## Emplacement

UploadCvWizardStep3

Review & Edit

---

## Affichage

Compétence résolue

Python

☑

---

Compétence non résolue

Power Automate

Not present in skill catalog

Skill Mapping

[ Select skill ▼ ]

☐

---

## Comportement

Tant que :

Select skill

n'est pas renseigné

la proposition reste :

- décochée ;
- non sélectionnable.

Une fois une skill choisie :

la proposition devient sélectionnable.

---

# 12. Chargement du catalogue

Le catalogue est chargé une seule fois pendant la phase Review.

Source :

GET /skills

---

## MVP

Chargement complet du catalogue.

Pas d'autocomplete.

Pas de recherche serveur.

Pas de pagination.

---

# 13. Validation Frontend

Avant Apply :

Le frontend doit vérifier :

- qu'une skill inconnue possède un mapping ;
- que la skill sélectionnée existe ;
- que la proposition est sélectionnée.

---

## Cas invalide

Power Automate

Mapping vide

↓

Apply

↓

Blocage frontend

Message :

Please select an existing skill before accepting this proposal.

---

# 14. Cas limites

## Cas 1

Aucune skill dans le catalogue

Résultat :

aucun mapping possible.

La proposition reste ignorée.

---

## Cas 2

La skill est supprimée pendant la session

Validation backend.

Retour erreur métier contrôlée.

---

## Cas 3

L'utilisateur change plusieurs fois le mapping

Le dernier choix devient la source de vérité.

---

## Cas 4

Plusieurs propositions utilisent la même skill cible

Autorisé.

Le backend gère déjà les doublons ProfileSkill.

---

# 15. Sécurité

La logique métier reste côté backend.

Le frontend ne décide jamais :

- si une skill existe ;
- si une association est valide ;
- si un doublon doit être créé.

Le backend reste source de vérité.

---

# 16. Impacts techniques

Backend :

- Adaptation endpoint accept
- Validation reference_id

Frontend :

- UploadCvWizardStep3
- UploadCvModal
- API layer

Base de données :

- Aucun changement

Migration :

- Aucune

---

# 17. Critères de fin

La phase sera considérée terminée lorsque :

✅ Les compétences non résolues sont identifiées

✅ L'utilisateur peut choisir une skill existante

✅ Le mapping est transmis au backend

✅ Le profil est enrichi avec la skill sélectionnée

✅ Aucun enrichissement automatique du catalogue

✅ Aucun POST 400 lié aux skills non résolues

✅ Validation fonctionnelle réalisée

✅ Documentation synchronisée

✅ Working tree propre

---

# Résultat attendu

CV

Power Automate

↓

Mapping

Microsoft Power Automate

↓

Apply

↓

ProfileSkill

Microsoft Power Automate

↓

Profil enrichi

sans création automatique de nouvelle compétence.
