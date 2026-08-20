# Application Profile Attribution - Backend Technical Design

## Phase

7.1.22.10.4 Backend Technical Design

## Statut

Design

## Date

2026-08-20

---

# 1. Objectif

Définir l’évolution backend nécessaire pour supporter l’attribution et la réattribution du profil d’une candidature.

Le backend doit permettre :

- de créer une candidature avec un `profile_id` explicitement sélectionné ;
- de valider que le profil existe et peut être utilisé ;
- de modifier le `profile_id` d’une candidature existante ;
- d’enregistrer la modification dans la timeline ;
- de préserver les autres données de la candidature ;
- de garantir qu’un changement du contexte Opportunities ne modifie pas les candidatures existantes.

Le backend ne doit pas :

- créer automatiquement une candidature ;
- choisir silencieusement un profil à la place de l’utilisateur ;
- créer plusieurs candidatures pour plusieurs profils actifs ;
- modifier une candidature existante après un recalcul de matching ;
- persister le Primary Profile ou les Active Profiles dans `Application`.

---

# 2. Sources de conception

Ce design technique applique les règles définies dans :

```text
docs/application-profile-attribution-design.md
DEC-063 - Application Workflow Lifecycle
DEC-065 - Opportunity To Application Conversion
DEC-071 - Multi Profile Opportunity Context
```

Décisions produit applicables :

```text
1 Application
=
1 profile_id
```

```text
Best Matching Profile
=
présélection lors de la création depuis une opportunité
```

```text
Le profil présélectionné reste modifiable
avant validation
```

```text
Application.profile_id peut être modifié
après création
```

```text
Un changement du Primary Profile
ne modifie aucune candidature existante
```

---

# 3. État réel du repository

## 3.1 Module Applications

Le module actuel contient :

```text
backend/app/applications/event_models.py
backend/app/applications/models.py
backend/app/applications/router.py
backend/app/applications/schemas.py
```

Il n’existe actuellement aucun fichier :

```text
service.py
services.py
repository.py
```

La logique applicative est directement implémentée dans :

```text
backend/app/applications/router.py
```

---

## 3.2 Modèle Application

Le modèle possède déjà :

```python
profile_id: Mapped[int] = mapped_column(
    ForeignKey("profiles.id"),
    nullable=False,
)
```

Le modèle contient également :

```python
job_offer_id
status
notes
source_type
created_at
updated_at
```

Conséquence :

```text
Aucune nouvelle colonne n’est nécessaire.
```

---

## 3.3 Schéma de création

`ApplicationCreate` hérite de `ApplicationBase`.

`ApplicationBase` contient déjà :

```python
profile_id: int
job_offer_id: int
status: str
notes: str | None
source_type: str
```

L’API de création accepte donc déjà un `profile_id`.

Le problème actuel n’est pas le contrat de création.

Le problème actuel est l’absence de validation métier explicite de ce profil.

---

## 3.4 Schéma de modification

Le schéma actuel est :

```python
class ApplicationUpdate(BaseModel):
    status: str
    notes: str | None = None
    source_type: str = "MANUAL"
```

Il ne permet pas d’envoyer un nouveau `profile_id`.

La réattribution n’est donc pas disponible dans le contrat backend actuel.

---

## 3.5 Route de création

La route actuelle est :

```text
POST /applications
```

Elle crée directement :

```python
Application(
    profile_id=application.profile_id,
    job_offer_id=application.job_offer_id,
    status=application.status,
    notes=application.notes,
    source_type=application.source_type,
)
```

La route ne vérifie pas explicitement :

- que le profil existe ;
- que le profil est disponible ;
- que le profil n’est pas archivé ;
- que l’offre existe.

Ces contrôles doivent être évalués et ajoutés dans l’évolution backend.

---

## 3.6 Route de modification

La route actuelle est :

```text
PUT /applications/{application_id}
```

Elle modifie :

```python
status
notes
source_type
```

Elle ne modifie pas :

```python
profile_id
```

Elle ne génère pas d’événement de timeline pour les modifications générales.

---

## 3.7 Timeline

Le modèle `ApplicationEvent` contient déjà :

```python
application_id
event_type
old_value
new_value
event_date
created_at
```

La transition de statut crée déjà :

```python
ApplicationEvent(
    application_id=application.id,
    event_type="STATUS_CHANGED",
    old_value=current_status,
    new_value=new_status,
)
```

Le modèle existant peut donc stocker un événement :

```text
PROFILE_CHANGED
```

sans modification du schéma de base de données.

---

# 4. Architecture cible

## 4.1 Choix MVP

Le module Applications reste simple.

Aucun nouveau service n’est introduit dans ce jalon.

La logique reste dans :

```text
backend/app/applications/router.py
```

Justification :

- le module utilise déjà cette structure ;
- la modification reste limitée ;
- aucun service Applications n’existe actuellement ;
- introduire une nouvelle couche uniquement pour cette évolution créerait un refactoring plus large que le besoin ;
- la séparation en service pourra être décidée dans une phase dédiée si la logique Applications continue de croître.

Cette décision ne signifie pas que toute logique métier future doit rester dans le router.

Elle limite simplement le périmètre du présent jalon.

---

## 4.2 Flux de création cible

```text
POST /applications
↓
Validation du profil
↓
Validation de l’offre
↓
Création Application
↓
Commit
↓
Retour ApplicationResponse
```

Le backend reçoit le profil déjà sélectionné par l’utilisateur.

Le backend ne détermine pas le Best Matching Profile dans la route de création.

La présélection du Best Matching Profile appartient au workflow frontend, à partir des scores retournés par le backend.

La validation finale du `profile_id` appartient au backend.

---

## 4.3 Flux de réattribution cible

```text
PUT /applications/{application_id}
↓
Chargement Application
↓
Validation du nouveau profil
↓
Comparaison ancien profile_id / nouveau profile_id
↓
Mise à jour Application.profile_id
↓
Création PROFILE_CHANGED si valeur différente
↓
Mise à jour des autres champs
↓
Commit unique
↓
Retour ApplicationResponse
```

---

# 5. Modifications des schémas

## Fichier

```text
backend/app/applications/schemas.py
```

## 5.1 ApplicationUpdate

Le schéma cible devient :

```python
class ApplicationUpdate(BaseModel):
    profile_id: int
    status: str
    notes: str | None = None
    source_type: str = "MANUAL"
```

## Justification

Le frontend utilise déjà `PUT /applications/{application_id}` pour modifier :

- les notes ;
- la source ;
- le statut envoyé dans le payload général.

L’ajout de `profile_id` permet de conserver un contrat de mise à jour unique.

---

## 5.2 Compatibilité des consommateurs existants

L’ajout d’un champ obligatoire dans `ApplicationUpdate` impose de modifier tous les appels frontend existants à :

```typescript
updateApplication();
```

Les appels existants doivent toujours transmettre le `profile_id` actuel lorsque le profil n’est pas modifié.

Exemple :

```json
{
  "profile_id": 12,
  "status": "Applied",
  "notes": "Follow-up sent.",
  "source_type": "OPPORTUNITY"
}
```

Ce point est obligatoire pour éviter une régression de :

```text
Save Notes
Save Source
```

---

## 5.3 Alternative rejetée

Alternative :

```python
profile_id: int | None = None
```

puis ignorer le champ lorsqu’il est absent.

Cette option est rejetée pour ce jalon.

Raisons :

- le contrat complet doit représenter l’état cible de la ressource ;
- les consommateurs doivent transmettre explicitement l’attribution actuelle ;
- une valeur obligatoire réduit l’ambiguïté entre absence de modification et payload incomplet ;
- le projet utilise déjà un schéma de mise à jour complet pour `status`, `notes` et `source_type`.

---

# 6. Validation du profil

## 6.1 Existence

Avant création ou réattribution, le backend doit vérifier que le profil existe.

Requête conceptuelle :

```python
profile = db.query(Profile).filter(
    Profile.id == profile_id,
).first()
```

Si le profil n’existe pas :

```text
HTTP 404
```

Message :

```text
Profile not found.
```

---

## 6.2 Disponibilité

Le modèle Profile réel devra être utilisé pour vérifier l’état disponible ou archivé.

Le backend ne doit pas supposer le nom d’un champ non audité.

La règle fonctionnelle est :

```text
Un profil indisponible ou archivé
ne peut pas être utilisé pour une nouvelle attribution.
```

L’implémentation devra réutiliser le champ d’état réellement présent dans `Profile`.

Aucun nouveau champ Profile ne doit être créé sans audit du modèle.

---

## 6.3 Profil déjà attribué puis archivé

Une candidature existante peut conserver un profil ensuite archivé.

Règle :

```text
Lecture de la candidature
=
autorisée

Conservation du profile_id existant
=
autorisée

Nouvelle attribution vers un profil archivé
=
refusée
```

Cela signifie que l’enregistrement existant reste valide.

Le backend bloque uniquement une nouvelle sélection ou réattribution vers un profil non disponible.

---

# 7. Validation de l’offre

Lors de la création, le backend doit vérifier que l’offre existe.

Requête conceptuelle :

```python
job_offer = db.query(JobOffer).filter(
    JobOffer.id == application.job_offer_id,
).first()
```

Si l’offre n’existe pas :

```text
HTTP 404
```

Message :

```text
Job offer not found.
```

La réattribution du profil ne modifie pas `job_offer_id`.

---

# 8. Évolution de create_application

## Fichier

```text
backend/app/applications/router.py
```

## Route

```text
POST /applications
```

## Comportement cible

1. valider le profil ;
2. valider l’offre ;
3. créer l’Application ;
4. persister le `profile_id` reçu ;
5. effectuer un commit ;
6. retourner l’Application créée.

Pseudo-code :

```python
profile = get_valid_profile(
    db=db,
    profile_id=application.profile_id,
)

job_offer = get_valid_job_offer(
    db=db,
    job_offer_id=application.job_offer_id,
)

new_application = Application(
    profile_id=profile.id,
    job_offer_id=job_offer.id,
    status=application.status,
    notes=application.notes,
    source_type=application.source_type,
)

db.add(new_application)
db.commit()
db.refresh(new_application)

return new_application
```

Le backend ne remplace pas le profil reçu par :

- le Primary Profile ;
- le Best Matching Profile ;
- le premier profil disponible ;
- un profil calculé localement.

Le profil reçu et validé est la décision utilisateur persistée.

---

# 9. Évolution de update_application

## Route

```text
PUT /applications/{application_id}
```

## Comportement cible

La route doit :

1. charger la candidature ;
2. retourner 404 si elle n’existe pas ;
3. valider le nouveau profil ;
4. mémoriser l’ancien `profile_id` ;
5. comparer l’ancien et le nouveau profil ;
6. mettre à jour `profile_id` ;
7. créer un événement si le profil a changé ;
8. mettre à jour les autres champs ;
9. effectuer un commit unique ;
10. rafraîchir et retourner la candidature.

Pseudo-code :

```python
application = db.query(Application).filter(
    Application.id == application_id,
).first()

if application is None:
    raise HTTPException(
        status_code=404,
        detail="Application not found.",
    )

profile = get_valid_profile(
    db=db,
    profile_id=application_update.profile_id,
)

old_profile_id = application.profile_id
new_profile_id = profile.id

application.profile_id = new_profile_id
application.status = application_update.status
application.notes = application_update.notes
application.source_type = application_update.source_type

if old_profile_id != new_profile_id:
    event = ApplicationEvent(
        application_id=application.id,
        event_type="PROFILE_CHANGED",
        old_value=str(old_profile_id),
        new_value=str(new_profile_id),
    )

    db.add(event)

db.commit()
db.refresh(application)

return application
```

---

# 10. Événement PROFILE_CHANGED

## Type

```text
PROFILE_CHANGED
```

## Déclenchement

L’événement est créé uniquement lorsque :

```text
ancien profile_id
≠
nouveau profile_id
```

## Aucun événement lorsque

```text
ancien profile_id
=
nouveau profile_id
```

## Valeurs

```text
old_value
=
ancien profile_id converti en chaîne

new_value
=
nouveau profile_id converti en chaîne
```

Exemple :

```python
ApplicationEvent(
    application_id=42,
    event_type="PROFILE_CHANGED",
    old_value="12",
    new_value="17",
)
```

## Transaction

La mise à jour de l’Application et la création de l’événement doivent appartenir à la même transaction.

Un seul :

```python
db.commit()
```

est exécuté après les deux opérations.

Si la transaction échoue, ni la réattribution ni l’événement ne doivent être partiellement persistés.

---

# 11. Réutilisation de la timeline existante

La route existante :

```text
GET /applications/{application_id}/timeline
```

retourne déjà tous les `ApplicationEvent` triés par date décroissante.

Aucune nouvelle route timeline n’est nécessaire.

`ApplicationEventResponse` supporte déjà :

```python
event_type
old_value
new_value
event_date
```

Aucune modification de schéma n’est nécessaire pour exposer `PROFILE_CHANGED`.

Le frontend devra seulement apprendre à présenter ce nouveau type d’événement.

---

# 12. Fonctions auxiliaires

## Recommandation

Pour éviter de dupliquer les validations entre création et réattribution, ajouter des fonctions privées dans :

```text
backend/app/applications/router.py
```

Exemple conceptuel :

```python
def get_application_or_404(
    db: Session,
    application_id: int,
) -> Application:
    ...
```

```python
def get_profile_or_404(
    db: Session,
    profile_id: int,
) -> Profile:
    ...
```

```python
def get_job_offer_or_404(
    db: Session,
    job_offer_id: int,
) -> JobOffer:
    ...
```

La validation du caractère actif ou archivé peut être intégrée dans la fonction profil après audit du modèle réel.

## Limite

Ces fonctions restent internes au module.

Aucun nouveau package générique de validation n’est créé dans ce jalon.

---

# 13. Statut et profile_id

La réattribution du profil ne constitue pas une transition de statut.

Elle utilise :

```text
PUT /applications/{application_id}
```

et non :

```text
POST /applications/{application_id}/status
```

La route de transition de statut reste responsable uniquement de :

```text
VALID_TRANSITIONS
STATUS_CHANGED
```

Aucune logique `PROFILE_CHANGED` ne doit être ajoutée dans `transition_application_status()`.

---

# 14. Préservation des données

Lors d’une réattribution :

```text
profile_id
=
modifiable
```

Les données suivantes restent inchangées sauf si elles sont explicitement transmises par le contrat de mise à jour :

```text
id
job_offer_id
created_at
events existants
```

Le changement du profil ne doit pas automatiquement modifier :

```text
status
notes
source_type
job_offer_id
```

Le frontend doit transmettre leurs valeurs actuelles lorsqu’il utilise le schéma complet de mise à jour.

---

# 15. Invariants métier

Le backend doit préserver les invariants suivants.

## Invariant 1

```text
Application.profile_id
n’est jamais nul
```

## Invariant 2

```text
Application.job_offer_id
n’est jamais nul
```

## Invariant 3

```text
Une réattribution ne crée pas une nouvelle Application
```

## Invariant 4

```text
Une réattribution ne modifie pas job_offer_id
```

## Invariant 5

```text
Une réattribution crée au maximum
un événement PROFILE_CHANGED
```

## Invariant 6

```text
Aucun événement PROFILE_CHANGED
si le profile_id ne change pas
```

## Invariant 7

```text
Un changement du Primary Profile
ne déclenche aucune mise à jour backend
des Applications existantes
```

## Invariant 8

```text
Un recalcul du matching
ne déclenche aucune réattribution
```

---

# 16. Gestion des erreurs

## Application inconnue

```text
HTTP 404
Application not found.
```

## Profil inconnu

```text
HTTP 404
Profile not found.
```

## Profil indisponible

Code recommandé :

```text
HTTP 400
```

Message recommandé :

```text
The selected profile is not available.
```

Le code définitif doit utiliser la stratégie d’erreur déjà employée dans le domaine Profile.

## Offre inconnue

```text
HTTP 404
Job offer not found.
```

## Payload invalide

Validation Pydantic :

```text
HTTP 422
```

## Erreur de persistance

Le backend doit effectuer un rollback avant de propager l’erreur ou de retourner une réponse contrôlée.

Aucune donnée partielle ne doit rester persistée.

---

# 17. Migration de base de données

## Conclusion

```text
Aucune migration requise.
```

Justification :

- `Application.profile_id` existe déjà ;
- `profile_id` possède déjà une clé étrangère vers `profiles.id` ;
- `ApplicationEvent.event_type` accepte déjà une chaîne ;
- `old_value` et `new_value` acceptent déjà des chaînes ;
- aucune nouvelle table n’est nécessaire ;
- aucune nouvelle colonne n’est nécessaire.

La fonctionnalité est une évolution :

```text
de schéma API
+
de logique backend
+
de timeline
```

et non une évolution du schéma PostgreSQL.

---

# 18. Contrat API cible

## 18.1 Création

### Requête

```http
POST /applications
```

Payload :

```json
{
  "profile_id": 17,
  "job_offer_id": 501,
  "status": "Applied",
  "notes": null,
  "source_type": "OPPORTUNITY"
}
```

### Réponse

```json
{
  "id": 42,
  "profile_id": 17,
  "job_offer_id": 501,
  "status": "Applied",
  "notes": null,
  "source_type": "OPPORTUNITY",
  "created_at": "2026-08-20T18:00:00",
  "updated_at": "2026-08-20T18:00:00"
}
```

---

## 18.2 Réattribution

### Requête

```http
PUT /applications/42
```

Payload :

```json
{
  "profile_id": 22,
  "status": "Applied",
  "notes": null,
  "source_type": "OPPORTUNITY"
}
```

### Réponse

```json
{
  "id": 42,
  "profile_id": 22,
  "job_offer_id": 501,
  "status": "Applied",
  "notes": null,
  "source_type": "OPPORTUNITY",
  "created_at": "2026-08-20T18:00:00",
  "updated_at": "2026-08-20T18:10:00"
}
```

### Événement créé

```json
{
  "application_id": 42,
  "event_type": "PROFILE_CHANGED",
  "old_value": "17",
  "new_value": "22"
}
```

---

# 19. Tests backend à ajouter

## Fichier existant

```text
backend/tests/test_applications.py
```

Aucun nouveau fichier de test n’est requis si les tests Applications sont déjà centralisés dans ce fichier.

---

## 19.1 Création avec profil valide

```text
Given
un profil existant et disponible

When
POST /applications est appelé

Then
Application.profile_id correspond au payload
```

---

## 19.2 Création avec profil inconnu

```text
Given
un profile_id inconnu

When
POST /applications est appelé

Then
404 Profile not found
```

---

## 19.3 Création avec offre inconnue

```text
Given
un job_offer_id inconnu

When
POST /applications est appelé

Then
404 Job offer not found
```

---

## 19.4 Réattribution avec profil valide

```text
Given
une Application liée au profil 12

When
PUT /applications/{id}
avec profile_id 17

Then
Application.profile_id = 17
```

---

## 19.5 Timeline de réattribution

```text
Given
une Application liée au profil 12

When
le profil devient 17

Then
un événement PROFILE_CHANGED existe

And
old_value = "12"

And
new_value = "17"
```

---

## 19.6 Pas d’événement sans changement

```text
Given
une Application liée au profil 12

When
PUT utilise encore profile_id 12

Then
aucun événement PROFILE_CHANGED supplémentaire
```

---

## 19.7 Profil inconnu en réattribution

```text
Given
une Application existante

When
PUT utilise un profile_id inconnu

Then
404 Profile not found

And
Application.profile_id reste inchangé
```

---

## 19.8 Préservation des autres données

```text
Given
une Application existante

When
le profil change

Then
job_offer_id reste inchangé

And
created_at reste inchangé

And
status reste conforme au payload

And
notes restent conformes au payload

And
source_type reste conforme au payload
```

---

## 19.9 Timeline existante préservée

```text
Given
une Application avec des événements STATUS_CHANGED

When
le profil change

Then
les événements existants restent présents

And
PROFILE_CHANGED est ajouté
```

---

## 19.10 Non-régression des transitions

```text
Given
une Application réattribuée

When
une transition de statut valide est exécutée

Then
STATUS_CHANGED continue de fonctionner
```

---

# 20. Tests de compatibilité frontend attendus

Le backend design impose les évolutions frontend suivantes :

- tous les appels à `updateApplication()` doivent fournir `profile_id` ;
- le type `ApplicationUpdatePayload` doit contenir `profile_id` ;
- Save Notes doit conserver le profil courant ;
- Save Source doit conserver le profil courant ;
- la réattribution doit réutiliser la même API ;
- les erreurs 404 et 400 doivent être affichées proprement.

Ces modifications seront détaillées dans le design frontend dédié.

---

# 21. Ordre d’implémentation backend

## Étape 1

Étendre les tests de création avec validation du profil et de l’offre.

## Étape 2

Ajouter les validations à `create_application()`.

## Étape 3

Étendre `ApplicationUpdate` avec `profile_id`.

## Étape 4

Ajouter les tests de réattribution.

## Étape 5

Implémenter la mise à jour du `profile_id`.

## Étape 6

Ajouter `PROFILE_CHANGED`.

## Étape 7

Valider la timeline.

## Étape 8

Exécuter les tests Applications ciblés.

## Étape 9

Exécuter toute la suite backend.

## Étape 10

Effectuer un commit backend dédié.

---

# 22. Fichiers backend concernés

## Fichiers à modifier

```text
backend/app/applications/schemas.py
backend/app/applications/router.py
backend/tests/test_applications.py
```

## Fichiers sans modification attendue

```text
backend/app/applications/models.py
backend/app/applications/event_models.py
```

## Migration

```text
Aucun fichier Alembic
Aucune migration SQL
```

---

# 23. Hors périmètre backend

Ce design ne demande pas au backend de :

- persister le Primary Profile ;
- persister les Active Profiles ;
- modifier le moteur de matching ;
- modifier la formule de scoring ;
- modifier le ranking ;
- calculer un score combiné ;
- créer plusieurs Applications ;
- réattribuer automatiquement une Application ;
- changer le profil après recalcul du matching ;
- fermer APP-005 avant validation de bout en bout ;
- modifier les Saved Searches ;
- modifier les Discovery Preferences ;
- modifier les Search Criteria.

---

# 24. Risques identifiés

## Risque 1

Ajouter `profile_id` comme champ obligatoire dans `ApplicationUpdate` casse les consommateurs qui ne le transmettent pas.

Mitigation :

```text
Modifier tous les appels frontend
dans le même jalon d’intégration.
```

## Risque 2

La création accepte actuellement des identifiants sans validation applicative explicite.

Mitigation :

```text
Ajouter les validations avant création.
```

## Risque 3

Une réattribution peut être persistée sans timeline si la création de l’événement n’est pas transactionnelle.

Mitigation :

```text
Un commit unique.
```

## Risque 4

Un profil archivé peut être proposé par le frontend.

Mitigation :

```text
Filtrage frontend
+
validation backend obligatoire.
```

## Risque 5

Le frontend peut afficher un score correspondant à l’ancien profil après réattribution.

Mitigation :

```text
Recharger le matching après mise à jour.
```

---

# 25. Critères de fin backend

La partie backend de 7.1.22.10 est terminée lorsque :

```text
✓ profile_id validé à la création
✓ job_offer_id validé à la création
✓ profile_id accepté par ApplicationUpdate
✓ profile_id modifiable après création
✓ profil inconnu rejeté
✓ profil indisponible rejeté
✓ PROFILE_CHANGED créé lors d’une réattribution
✓ aucun événement si profile_id ne change pas
✓ timeline existante préservée
✓ job_offer_id inchangé
✓ aucune migration PostgreSQL
✓ tests Applications verts
✓ suite backend verte
✓ aucun impact sur matching et ranking
```

---

# 26. Décision technique finale

L’attribution initiale et la réattribution utilisent le champ existant :

```text
Application.profile_id
```

La création continue d’utiliser :

```text
POST /applications
```

La réattribution utilise la route existante :

```text
PUT /applications/{application_id}
```

Le contrat `ApplicationUpdate` est étendu avec :

```text
profile_id
```

Chaque changement réel de profil crée :

```text
PROFILE_CHANGED
```

dans la timeline.

Aucune migration de base de données n’est requise.

La logique reste dans le router Applications pour limiter le périmètre du jalon et respecter la structure actuelle du module.

Toute extraction future vers un service dédié devra faire l’objet d’une décision ou d’un refactoring séparé.
