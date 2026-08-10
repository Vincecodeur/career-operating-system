## ProfileSkill Backend CRUD Design

### Phase

7.1.15.4.A ProfileSkill Backend CRUD Design

### Statut

Completed

### Contexte

Le repository audit a confirmé que le domaine ProfileSkill dispose actuellement des opérations suivantes :

- POST /profile-skills
- GET /profile-skills
- GET /profiles/{profile_id}/skills

Le domaine ProfileSkill ne dispose pas actuellement :

- d'une opération Update ;
- d'une opération Delete ;
- d'un schéma ProfileSkillUpdate ;
- d'une validation CRUD complète.

Cette limite bloque le développement du frontend Skills Management basé sur ProfileSkill.

Le design frontend réalisé précédemment prévoit :

- ajout d'une compétence à un profil ;
- modification d'une compétence associée à un profil ;
- suppression d'une compétence associée à un profil.

Ces opérations nécessitent des endpoints backend supplémentaires.

### Objectif

Compléter le CRUD backend du domaine ProfileSkill afin de permettre :

- la modification d'une compétence associée à un profil ;
- la suppression d'une compétence associée à un profil ;

sans modifier le catalogue global de compétences.

### Principes directeurs

#### Principe 1

Le profil structuré reste la source de vérité carrière.

#### Principe 2

ProfileSkill représente une relation métier.

#### Principe 3

Modifier une relation ProfileSkill ne doit jamais modifier la compétence globale Skill.

#### Principe 4

Supprimer une relation ProfileSkill ne doit jamais supprimer la compétence globale Skill.

#### Principe 5

Toute logique métier appartient au backend.

#### Principe 6

Les opérations CRUD doivent être validées par tests avant toute intégration frontend.

### État actuel

Modèle :

ProfileSkill

Clé primaire composite :

- profile_id
- skill_id

Champs modifiables :

- years_of_experience
- self_assessment_level

Champs non modifiables :

- profile_id
- skill_id
- created_at

### CRUD cible

#### Create

Déjà implémenté.

POST /profile-skills

#### Read

Déjà implémenté.

GET /profile-skills

GET /profiles/{profile_id}/skills

#### Update

À implémenter.

PUT /profile-skills/{profile_id}/{skill_id}

#### Delete

À implémenter.

DELETE /profile-skills/{profile_id}/{skill_id}

### Schéma à ajouter

#### ProfileSkillUpdate

Champs :

- years_of_experience
- self_assessment_level

Structure cible :

years_of_experience:int

self_assessment_level:str

### Endpoint Update

#### Route

PUT /profile-skills/{profile_id}/{skill_id}

#### Payload

{
"years_of_experience": 5,
"self_assessment_level": "Advanced"
}

#### Réponse

ProfileSkillResponse

#### Comportement

Rechercher :

- profile_id
- skill_id

Si la relation existe :

- mettre à jour years_of_experience ;
- mettre à jour self_assessment_level ;
- sauvegarder ;
- retourner la relation mise à jour.

#### Erreurs

404

Profile skill relationship not found.

### Endpoint Delete

#### Route

DELETE /profile-skills/{profile_id}/{skill_id}

#### Réponse

ProfileSkillResponse

#### Comportement

Rechercher :

- profile_id
- skill_id

Si la relation existe :

- supprimer la relation ;
- commit ;
- retourner la relation supprimée.

#### Erreurs

404

Profile skill relationship not found.

### Règles métier

#### Règle 1

ProfileSkill est une relation.

La suppression est un hard delete.

#### Règle 2

Skill n'est jamais supprimé.

#### Règle 3

Le catalogue Skill reste intact après suppression.

#### Règle 4

Le profile reste intact.

#### Règle 5

Les clés profile_id et skill_id sont immuables.

### Validation attendue

#### Validation Update

Créer une relation :

Profile 1
↓
Skill 2

Modifier :

years_of_experience

Puis vérifier :

GET /profiles/{profile_id}/skills

Les nouvelles valeurs doivent être visibles.

#### Validation Delete

Créer une relation.

Supprimer la relation.

Vérifier :

GET /profiles/{profile_id}/skills

La relation ne doit plus exister.

Vérifier :

GET /skills

La compétence doit toujours exister.

### Tests à ajouter

#### Update

test_update_profile_skill

Objectif :

vérifier qu'une relation est correctement mise à jour.

#### Update Not Found

test_update_profile_skill_not_found

Objectif :

retourner 404.

#### Delete

test_delete_profile_skill

Objectif :

supprimer la relation.

#### Delete Not Found

test_delete_profile_skill_not_found

Objectif :

retourner 404.

### Validation Swagger attendue

POST /profile-skills

GET /profile-skills

GET /profiles/{profile_id}/skills

PUT /profile-skills/{profile_id}/{skill_id}

DELETE /profile-skills/{profile_id}/{skill_id}

404 update

404 delete

### Impact Backend

Fichiers à modifier :

backend/app/profile/profile_skill_router.py

backend/app/profile/profile_skill_schemas.py

Fichiers à créer :

backend/tests/test_profile_skills.py

### Impact Frontend

Aucun pendant cette phase.

Le frontend sera traité dans une phase ultérieure.

### Décisions de design

#### DEC-PS-001

ProfileSkill est prioritaire sur Skill pour le MVP.

#### DEC-PS-002

La suppression concerne uniquement la relation ProfileSkill.

#### DEC-PS-003

Skill reste un catalogue partagé.

#### DEC-PS-004

Les clés profile_id et skill_id sont immuables.

#### DEC-PS-005

Le frontend Skills Management dépend du CRUD backend ProfileSkill complet.

### Risques

#### Risque 1

Suppression accidentelle du catalogue Skill.

Mitigation :

Supprimer uniquement ProfileSkill.

#### Risque 2

Modification des clés composites.

Mitigation :

Interdire leur modification.

#### Risque 3

Frontend développé avant backend complet.

Mitigation :

Respecter Backend → Tests → Validation → Frontend.

### Critères de fin

La phase est terminée lorsque :

- ProfileSkillUpdate existe ;
- PUT ProfileSkill existe ;
- DELETE ProfileSkill existe ;
- tests CRUD passants ;
- validation Swagger réalisée ;
- commit technique effectué ;
- documentation synchronisée.

### Livrable

docs/profile-skill-backend-crud-design.md

### Implementation Status

Completed.

Implemented :

- ProfileSkillUpdate
- PUT /profile-skills/{profile_id}/{skill_id}
- DELETE /profile-skills/{profile_id}/{skill_id}

Tests :

- test_create_profile_skill
- test_list_profile_skills
- test_list_skills_for_profile
- test_update_profile_skill
- test_update_profile_skill_not_found
- test_delete_profile_skill
- test_delete_profile_skill_not_found

Validation :

- 7 ProfileSkill tests passants
- 143 tests backend passants
- Swagger validation réalisée

Technical Commit :

- b1db1ca - feat: complete profile skill crud backend

### Étape suivante recommandée

7.1.15.4.B ProfileSkill Backend CRUD Completion

Objectif :

Implémenter :

- ProfileSkillUpdate
- PUT /profile-skills/{profile_id}/{skill_id}
- DELETE /profile-skills/{profile_id}/{skill_id}

Validation attendue :

- tests backend passants ;
- validation Swagger réussie ;
- aucun changement frontend dans cette phase.
