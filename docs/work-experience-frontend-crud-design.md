## WorkExperience Frontend CRUD Design

### Phase

7.1.15.5.3 Frontend CRUD Design

### Statut

Design

### Contexte

Le backend WorkExperience est maintenant complet côté CRUD.

Les phases suivantes ont été validées :

- 7.1.15.5.1 Backend CRUD Completion ;
- 7.1.15.5.2 Backend CRUD Validation.

Le backend dispose désormais des opérations suivantes :

- POST /work-experiences ;
- GET /work-experiences ;
- GET /work-experiences/{work_experience_id} ;
- GET /profiles/{profile_id}/work-experiences ;
- PUT /work-experiences/{work_experience_id} ;
- DELETE /work-experiences/{work_experience_id}.

Les tests backend WorkExperience sont passants.

Le frontend affiche actuellement les expériences professionnelles dans ProfileDetail, mais ne permet pas encore de les créer, modifier ou supprimer depuis l'interface.

Cette phase vise uniquement à définir le design frontend du CRUD WorkExperience.

Aucun développement frontend ne doit être réalisé pendant cette phase.

### Objectif

Définir l'expérience utilisateur et l'architecture frontend permettant de gérer les expériences professionnelles d'un profil depuis la page Profiles.

L'utilisateur doit pouvoir :

- ajouter une expérience professionnelle ;
- modifier une expérience professionnelle existante ;
- supprimer une expérience professionnelle existante.

### Principes directeurs

#### Principe 1

Le profil structuré reste la source de vérité carrière.

#### Principe 2

Les expériences professionnelles doivent être gérées depuis la page Profiles.

#### Principe 3

Settings ne doit pas devenir un point d'entrée pour gérer les expériences professionnelles.

#### Principe 4

Toute logique métier reste côté backend.

#### Principe 5

Le frontend consomme les APIs FastAPI et affiche les résultats.

#### Principe 6

L'expérience utilisateur doit rester cohérente avec les patterns déjà utilisés pour Profile CRUD et ProfileSkill CRUD.

#### Principe 7

Le MVP privilégie une implémentation simple, lisible et maintenable.

### État actuel du frontend

Le composant ProfileDetail affiche déjà :

- les informations générales du profil ;
- le compteur d'expériences ;
- la liste des expériences professionnelles ;
- le titre du poste ;
- le nom de l'entreprise ;
- la période ;
- la description.

Le composant ProfileDetail ne propose pas encore :

- bouton Add Experience ;
- bouton Edit Experience ;
- bouton Remove Experience.

Le composant ProfilesPage charge déjà les expériences avec :

getProfileWorkExperiences(profileId)

Le frontend ne possède pas encore :

- createWorkExperience ;
- updateWorkExperience ;
- deleteWorkExperience.

### Périmètre MVP

Inclus :

- ajout d'une expérience professionnelle ;
- modification d'une expérience professionnelle ;
- suppression d'une expérience professionnelle ;
- rafraîchissement automatique des données après mutation ;
- affichage des erreurs ;
- états loading/saving/deleting ;
- intégration dans ProfileDetail ;
- intégration dans ProfilesPage.

Exclus :

- drag and drop d'expériences ;
- tri manuel des expériences ;
- timeline avancée ;
- enrichissement automatique depuis un CV ;
- suggestion IA ;
- détection des trous de carrière ;
- validation métier avancée des dates ;
- gestion avancée du poste actuel.

### UX cible

#### Section Work Experience

La section Work Experience doit contenir :

- titre Work Experience ;
- bouton Add Experience ;
- liste des expériences existantes.

Chaque expérience doit afficher :

- job_title ;
- company_name ;
- start_date ;
- end_date ou Present ;
- description ;
- bouton Edit ;
- bouton Remove.

### Ajout d'une expérience

#### Déclencheur

Bouton :

Add Experience

présent dans la section Work Experience.

#### Composant prévu

AddWorkExperienceModal.tsx

#### Champs

Company Name

Job Title

Start Date

End Date

Is Current Position

Description

#### Validation frontend

Champs obligatoires :

- company_name ;
- job_title ;
- start_date ;
- description.

Champs optionnels :

- end_date.

Règle UX simple :

- si is_current_position = true, end_date peut rester vide.

#### Payload envoyé au backend

profile_id

company_name

job_title

start_date

end_date

is_current_position

description

#### Succès

Après création :

- fermeture du modal ;
- reload des détails du profil ;
- nouvelle expérience visible dans la section Work Experience ;
- compteur Experiences mis à jour.

#### Erreur

Afficher :

Unable to add work experience.

### Modification d'une expérience

#### Déclencheur

Bouton :

Edit

présent sur chaque carte Work Experience.

#### Composant prévu

EditWorkExperienceModal.tsx

#### Champs modifiables

Company Name

Job Title

Start Date

End Date

Is Current Position

Description

#### Champs non modifiables

id

profile_id

created_at

#### Succès

Après modification :

- fermeture du modal ;
- reload des détails du profil ;
- valeurs mises à jour visibles immédiatement.

#### Erreur

Afficher :

Unable to update work experience.

### Suppression d'une expérience

#### Déclencheur

Bouton :

Remove

présent sur chaque carte Work Experience.

#### Composant prévu

DeleteWorkExperienceDialog.tsx

#### Message de confirmation

Remove this work experience?

This action cannot be undone.

#### Succès

Après suppression :

- fermeture de la confirmation ;
- reload des détails du profil ;
- expérience retirée de la liste ;
- compteur Experiences mis à jour.

#### Erreur

Afficher :

Unable to remove work experience.

### Architecture frontend prévue

#### Nouveaux composants

frontend/src/components/AddWorkExperienceModal.tsx

frontend/src/components/EditWorkExperienceModal.tsx

frontend/src/components/DeleteWorkExperienceDialog.tsx

#### Fichiers à modifier

frontend/src/services/api.ts

frontend/src/components/ProfileDetail.tsx

frontend/src/pages/ProfilesPage.tsx

### APIs frontend à ajouter

#### createWorkExperience

POST /work-experiences

Payload :

- profile_id
- company_name
- job_title
- start_date
- end_date
- is_current_position
- description

#### updateWorkExperience

PUT /work-experiences/{work_experience_id}

Payload :

- company_name
- job_title
- start_date
- end_date
- is_current_position
- description

#### deleteWorkExperience

DELETE /work-experiences/{work_experience_id}

### Intégration dans ProfileDetail

Ajouter de nouvelles props :

onAddWorkExperience

onEditWorkExperience

onDeleteWorkExperience

Ajouter dans la section Work Experience :

- bouton Add Experience ;
- bouton Edit sur chaque expérience ;
- bouton Remove sur chaque expérience.

### Intégration dans ProfilesPage

Ajouter les states :

isAddWorkExperienceModalOpen

isEditWorkExperienceModalOpen

isDeleteWorkExperienceDialogOpen

selectedWorkExperience

isSavingWorkExperience

isDeletingWorkExperience

workExperienceMutationError

Ajouter les handlers :

handleAddWorkExperience

handleUpdateWorkExperience

handleDeleteWorkExperience

Réutiliser :

reloadSelectedProfileDetails(profileId)

après chaque mutation.

### Flux utilisateur

#### Add Work Experience

Profiles

↓

Select Profile

↓

Work Experience

↓

Add Experience

↓

Save

↓

POST /work-experiences

↓

Reload profile details

↓

Experience visible

#### Edit Work Experience

Profiles

↓

Select Profile

↓

Work Experience

↓

Edit

↓

Save

↓

PUT /work-experiences/{work_experience_id}

↓

Reload profile details

↓

Updated experience visible

#### Remove Work Experience

Profiles

↓

Select Profile

↓

Work Experience

↓

Remove

↓

Confirm

↓

DELETE /work-experiences/{work_experience_id}

↓

Reload profile details

↓

Experience removed

### Décisions de design

#### DEC-WE-FE-001

La gestion des expériences professionnelles se fait depuis Profiles.

#### DEC-WE-FE-002

Les actions CRUD WorkExperience sont placées dans ProfileDetail.

#### DEC-WE-FE-003

La création d'expérience est incluse dans le frontend CRUD WorkExperience.

#### DEC-WE-FE-004

Les modals sont utilisées pour Add et Edit afin de rester cohérent avec Profile CRUD et ProfileSkill CRUD.

#### DEC-WE-FE-005

La suppression utilise un dialog de confirmation.

#### DEC-WE-FE-006

Après chaque mutation, les détails du profil sont rechargés.

#### DEC-WE-FE-007

Aucune logique métier complexe liée aux dates n'est ajoutée dans le frontend pendant cette phase.

### Risques

#### Risque 1

Créer une expérience sans profil sélectionné.

Mitigation :

Désactiver l'action si aucun profil n'est sélectionné.

#### Risque 2

Confusion entre suppression d'une expérience et suppression du profil.

Mitigation :

Utiliser un message clair dans DeleteWorkExperienceDialog.

#### Risque 3

Erreur de format de date.

Mitigation :

Utiliser des inputs date et envoyer des dates au format YYYY-MM-DD.

#### Risque 4

Complexité excessive autour du poste actuel.

Mitigation :

Garder la règle simple : is_current_position peut être vrai avec end_date null.

#### Risque 5

Incohérence visuelle avec les autres CRUD.

Mitigation :

Réutiliser les patterns visuels de CreateProfileModal, EditProfileModal, DeleteProfileDialog et ProfileSkill CRUD.

### Critères de fin de la phase design

La phase est terminée lorsque :

- le design UX Add/Edit/Delete WorkExperience est défini ;
- les composants frontend à créer sont identifiés ;
- les fichiers frontend à modifier sont identifiés ;
- les APIs frontend à ajouter sont définies ;
- les flux utilisateur sont documentés ;
- les décisions de design sont documentées ;
- les risques sont documentés.

### Livrable

docs/work-experience-frontend-crud-design.md

### Étape suivante recommandée

7.1.15.5.4 Frontend CRUD Implementation

Objectif :

Implémenter le CRUD frontend WorkExperience dans Profiles.

Livrables attendus :

- AddWorkExperienceModal.tsx ;
- EditWorkExperienceModal.tsx ;
- DeleteWorkExperienceDialog.tsx ;
- createWorkExperience ;
- updateWorkExperience ;
- deleteWorkExperience ;
- intégration dans ProfileDetail.tsx ;
- intégration dans ProfilesPage.tsx ;
- build frontend validé ;
- validation visuelle Add/Edit/Remove Work Experience.
