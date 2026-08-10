## Skills Management Frontend Design

### Phase

7.1.15.4.3 Frontend CRUD Design

### Statut

Design

### Contexte

La phase 7.1.15.4.2 a validé le CRUD backend Skills.

Le backend permet désormais :

- créer une compétence ;
- lister les compétences ;
- récupérer une compétence ;
- modifier une compétence.

La suppression d'une compétence globale reste volontairement hors périmètre MVP.

La phase 7.1.15.4.3 vise à définir l'expérience utilisateur frontend permettant la gestion des compétences associées à un profil.

Aucun développement frontend ne doit être réalisé durant cette phase.

Cette phase produit uniquement le design fonctionnel et technique.

### Objectif

Permettre à un utilisateur :

- d'ajouter une compétence à un profil ;
- de modifier une compétence associée à un profil ;
- de supprimer une compétence associée à un profil.

La gestion concerne principalement ProfileSkill.

La gestion du catalogue global Skill reste secondaire.

### Principes directeurs

#### Principe 1

Le profil reste la source de vérité carrière principale.

#### Principe 2

L'édition des compétences doit se faire depuis Profiles.

#### Principe 3

Settings ne doit pas devenir un second point d'entrée des compétences.

#### Principe 4

La gestion d'une compétence globale et la gestion d'une compétence associée à un profil doivent rester clairement séparées.

#### Principe 5

Toute logique métier reste dans le backend.

#### Principe 6

Le frontend affiche uniquement les résultats des APIs.

#### Principe 7

Le MVP privilégie une expérience simple et rapide.

### Périmètre MVP

Inclus :

- ajouter une compétence à un profil ;
- modifier une compétence associée ;
- supprimer une compétence associée ;
- afficher les états de chargement ;
- afficher les erreurs utilisateur.

Exclus :

- suppression globale de Skill ;
- fusion de compétences ;
- renommage massif ;
- catégorisation avancée ;
- import CSV ;
- suggestions IA ;
- gestion avancée des catalogues.

### Architecture UX cible

ProfilesPage

↓

ProfileDetail

↓

Skills Section

↓

Add Skill
Edit Skill
Remove Skill

Toutes les actions liées aux compétences doivent rester dans le panneau ProfileDetail.

### État actuel

Le composant affiche déjà :

- liste des compétences du profil ;
- niveau ;
- expérience.

Aucune action CRUD n'est actuellement disponible.

### UX cible

#### Skills Section

La section Skills du profil doit contenir :

- titre Skills ;
- compteur de compétences ;
- bouton Add Skill.

Exemple :

Skills (12)

[ Add Skill ]

Python
FastAPI
Azure
...

### Ajout d'une compétence

#### Déclencheur

Bouton :

Add Skill

présent dans la section Skills.

#### Composant

AddProfileSkillModal

#### Champs

Skill :

- liste déroulante ;
- recherche textuelle ;
- sélection obligatoire.

Years of Experience :

- nombre entier ;
- optionnel.

Self Assessment Level :

- Beginner
- Intermediate
- Advanced
- Expert

#### Validation

Empêcher :

- compétence vide ;
- doublon déjà présent dans le profil.

#### Actions

Save

Cancel

#### Succès

- fermeture du modal ;
- refresh du profil ;
- nouvelle compétence visible immédiatement.

### Modification d'une compétence

#### Déclencheur

Icône Edit visible sur chaque compétence.

#### Composant

EditProfileSkillModal

#### Champs modifiables

Years of Experience

Self Assessment Level

#### Champs non modifiables

Skill

Profile

#### Actions

Save

Cancel

#### Succès

- fermeture du modal ;
- refresh du profil ;
- mise à jour visible immédiatement.

### Suppression d'une compétence

#### Déclencheur

Icône Delete visible sur chaque compétence.

#### Composant

DeleteProfileSkillDialog

#### Message

Remove this skill from the profile?

This action cannot be undone.

#### Actions

Remove

Cancel

#### Succès

- fermeture de la confirmation ;
- refresh du profil ;
- disparition immédiate de la compétence.

### États de chargement

#### Create

Saving...

#### Update

Saving...

#### Delete

Removing...

Les boutons doivent être désactivés pendant l'appel API.

### Gestion des erreurs

#### Erreur création

Unable to add skill.

#### Erreur modification

Unable to update skill.

#### Erreur suppression

Unable to remove skill.

#### Erreur réseau

Network error. Please try again.

### Architecture frontend prévue

Nouveaux composants :

- AddProfileSkillModal.tsx
- EditProfileSkillModal.tsx
- DeleteProfileSkillDialog.tsx

### Évolutions API frontend

Ajouter :

getSkills()

getSkill()

createProfileSkill()

updateProfileSkill()

deleteProfileSkill()

### Impact sur ProfileDetail

Ajouter :

Skills Header

↓

Add Skill Button

↓

Skill Cards

↓

Edit Button

Delete Button

### Flux utilisateur

Ajout

Profiles
↓
Select Profile
↓
Add Skill
↓
Save
↓
Backend
↓
Refresh Profile
↓
Skill Visible

Modification

Profiles
↓
Select Profile
↓
Edit Skill
↓
Save
↓
Backend
↓
Refresh Profile
↓
Updated Skill Visible

Suppression

Profiles
↓
Select Profile
↓
Delete Skill
↓
Confirm
↓
Backend
↓
Refresh Profile
↓
Skill Removed

### Décisions de design

#### DEC-7.1.15.4.3-001

Les compétences sont gérées depuis Profiles.

#### DEC-7.1.15.4.3-002

Les actions CRUD sont accessibles dans ProfileDetail.

#### DEC-7.1.15.4.3-003

La suppression concerne uniquement ProfileSkill.

#### DEC-7.1.15.4.3-004

La suppression globale de Skill reste hors MVP.

#### DEC-7.1.15.4.3-005

Les modals sont privilégiés pour maintenir la cohérence avec Profile CRUD.

#### DEC-7.1.15.4.3-006

Le profil est automatiquement rechargé après chaque action.

### Risques

#### Risque 1

Doublon de compétence dans un profil.

Mitigation :

Validation backend + frontend.

#### Risque 2

Confusion entre Skill et ProfileSkill.

Mitigation :

Ne jamais exposer la suppression globale de Skill.

#### Risque 3

Incohérence visuelle avec Profile CRUD.

Mitigation :

Réutiliser les mêmes patterns UX.

### Critères de fin

La phase est terminée lorsque :

- le design UX est validé ;
- les composants sont identifiés ;
- les APIs frontend sont identifiées ;
- les flux utilisateur sont définis ;
- les décisions de design sont documentées ;
- les risques sont documentés.

### Livrable

docs/skills-management-frontend-design.md

### Étape suivante recommandée

7.1.15.4.4 Frontend CRUD Implementation

Objectif :

Implémenter les composants frontend permettant :

- Add Profile Skill
- Edit Profile Skill
- Remove Profile Skill

Validation attendue :

- build frontend passant ;
- CRUD Skills visible dans Profiles ;
- validation visuelle réalisée.
