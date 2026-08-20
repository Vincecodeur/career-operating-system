# Application Profile Attribution - Frontend Technical Design

## Phase

7.1.22.10.5 Frontend Technical Design

## Statut

Design

## Date

2026-08-20

---

# 1. Objectif

Définir l’évolution frontend nécessaire pour attribuer et réattribuer explicitement un profil à une candidature.

Le frontend doit permettre :

- de présélectionner le Best Matching Profile lors d’une création depuis une opportunité ;
- d’afficher cette présélection avant toute création ;
- de permettre à l’utilisateur de modifier le profil proposé ;
- d’utiliser le Primary Profile comme fallback ;
- de créer la candidature uniquement après validation explicite ;
- de modifier le profil d’une candidature existante ;
- d’afficher l’événement `PROFILE_CHANGED` dans la timeline ;
- de préserver le profil lors des mises à jour de notes et de source ;
- de recharger le score de matching après une réattribution.

Le frontend ne doit pas :

- calculer un score de matching ;
- créer une candidature immédiatement au premier clic ;
- imposer le Best Matching Profile sans possibilité de modification ;
- réattribuer automatiquement une candidature existante ;
- modifier le Primary Profile lorsqu’une candidature change de profil ;
- créer plusieurs candidatures pour plusieurs Active Profiles.

---

# 2. Sources de conception

Ce design applique les règles définies dans :

```text
docs/application-profile-attribution-design.md
docs/application-profile-attribution-backend-design.md
DEC-063 - Application Workflow Lifecycle
DEC-065 - Opportunity To Application Conversion
DEC-071 - Multi Profile Opportunity Context
```

Règles produit applicables :

```text
1 Application
=
1 profile_id
```

```text
Création depuis une opportunité
=
Best Matching Profile présélectionné
```

```text
Best Matching Profile indisponible
=
Primary Profile présélectionné
```

```text
Le profil reste modifiable
avant la création
```

```text
Le profil peut être modifié
après la création
```

```text
Le contexte Opportunities
ne modifie jamais automatiquement
une candidature existante
```

---

# 3. État réel du frontend

## 3.1 OpportunitiesPage

Fichier :

```text
frontend/src/pages/OpportunitiesPage.tsx
```

La page charge déjà :

```text
les opportunités
les profils
les candidatures
les scores multi-profils
le matching du Primary Profile
les scores de classement
```

La page possède déjà :

```typescript
selectedProfileId;
activeProfileIds;
profileScores;
bestProfileScore;
selectedOffer;
creatingApplication;
```

Le `selectedProfileId` représente actuellement le Primary Profile.

Le `bestProfileScore` est calculé à partir des scores des Active Profiles.

---

## 3.2 Création actuelle depuis Opportunities

Le comportement actuel est :

```text
Create Application
↓
handlePrimaryAction()
↓
handleCreateApplication()
↓
POST /applications
```

La candidature est créée immédiatement avec :

```typescript
profile_id: selectedProfileId;
```

Le comportement actuel signifie :

```text
Application Profile
=
Primary Profile
```

Il n’existe aucun formulaire intermédiaire.

L’utilisateur ne peut pas vérifier ou modifier le profil avant la création.

---

## 3.3 Best Matching Profile actuel

La page calcule déjà :

```typescript
const activeProfileScores = profileScores.filter((score) =>
  activeProfileIds.includes(score.profile_id),
);
```

Puis :

```typescript
const bestProfileScore =
  [...activeProfileScores].sort(
    (a, b) => b.matching_score - a.matching_score,
  )[0] ?? null;
```

Le Best Matching Profile actif est donc déjà disponible dans le frontend.

Il est déjà affiché dans Opportunity Details.

Aucun nouveau calcul de matching frontend ne doit être ajouté.

La présélection réutilise uniquement le résultat existant.

---

## 3.4 ApplicationsPage

Fichier :

```text
frontend/src/pages/ApplicationsPage.tsx
```

La page possède déjà :

```text
liste des candidatures
détail d’une candidature
liste des profils
liste des opportunités
formulaire de création manuelle
mise à jour des notes
mise à jour de la source
transitions de statut
timeline
score de matching
```

Le formulaire de création manuelle contient déjà un sélecteur de profil.

Le détail affiche actuellement le profil, mais ne permet pas de le modifier.

---

## 3.5 API client

Fichier :

```text
frontend/src/services/api.ts
```

Le type actuel de mise à jour est :

```typescript
export type ApplicationUpdatePayload = {
  status: string;
  notes: string | null;
  source_type: string;
};
```

Le contrat ne contient pas encore :

```typescript
profile_id;
```

Les appels actuels à `updateApplication()` ne transmettent donc pas l’attribution du profil.

---

# 4. Architecture frontend cible

Le frontend conserve les responsabilités suivantes :

```text
affichage
sélection utilisateur
présélection à partir des données backend
gestion des dialogues
appel des APIs
rafraîchissement de l’état local
affichage des erreurs
```

Le backend reste responsable de :

```text
validation du profil
validation de l’offre
persistance de profile_id
création de PROFILE_CHANGED
validation des règles métier
```

Le frontend ne duplique pas les validations backend.

---

# 5. Flux cible depuis Opportunities

## 5.1 Flux général

```text
Utilisateur sélectionne une opportunité
↓
Scores des Active Profiles disponibles
↓
Utilisateur clique sur Create Application
↓
Boîte de dialogue ouverte
↓
Best Matching Profile présélectionné
↓
Utilisateur conserve ou modifie le profil
↓
Utilisateur confirme
↓
POST /applications
↓
Candidature créée
↓
Liste des candidatures rafraîchie
↓
Message de succès
```

La candidature n’est plus créée au premier clic.

---

## 5.2 Valeur présélectionnée

Règle :

```text
Si bestProfileScore existe
et correspond à un profil disponible
↓
bestProfileScore.profile_id
```

Fallback :

```text
Sinon
↓
selectedProfileId
```

Dernier fallback :

```text
Sinon
↓
aucune valeur
et création bloquée
```

Pseudo-code :

```typescript
function getDefaultApplicationProfileId() {
  if (
    bestProfileScore &&
    profiles.some((profile) => profile.id === bestProfileScore.profile_id)
  ) {
    return bestProfileScore.profile_id;
  }

  if (
    selectedProfileId !== null &&
    profiles.some((profile) => profile.id === selectedProfileId)
  ) {
    return selectedProfileId;
  }

  return null;
}
```

---

# 6. Nouvel état dans OpportunitiesPage

Ajouter les états suivants :

```typescript
const [isCreateApplicationModalOpen, setIsCreateApplicationModalOpen] =
  useState(false);
```

```typescript
const [applicationProfileId, setApplicationProfileId] = useState<number | null>(
  null,
);
```

```typescript
const [applicationCreationError, setApplicationCreationError] = useState<
  string | null
>(null);
```

L’état existant peut être conservé :

```typescript
const [creatingApplication, setCreatingApplication] = useState(false);
```

Aucun état global n’est nécessaire.

Le profil sélectionné dans le formulaire reste local à la page.

---

# 7. Ouverture de la boîte de dialogue

## Fonction cible

Remplacer la création immédiate par une fonction d’ouverture :

```typescript
function openCreateApplicationModal() {
  if (!selectedOffer) {
    return;
  }

  const defaultProfileId = getDefaultApplicationProfileId();

  setApplicationProfileId(defaultProfileId);
  setApplicationCreationError(null);
  setIsCreateApplicationModalOpen(true);
}
```

La fonction ne réalise aucun appel API.

Elle prépare uniquement le formulaire.

---

# 8. Évolution de handlePrimaryAction

Le comportement d’ouverture d’une candidature existante reste inchangé.

Comportement cible :

```typescript
function handlePrimaryAction() {
  if (hasRelatedApplications && relatedApplications.length > 0) {
    navigate("/applications", {
      state: {
        applicationId: relatedApplications[0].id,
      },
    });

    return;
  }

  openCreateApplicationModal();
}
```

La fonction ne doit plus appeler directement :

```typescript
handleCreateApplication();
```

---

# 9. Boîte de dialogue de création depuis Opportunities

## 9.1 Structure

La boîte de dialogue doit afficher :

```text
Create Application

Opportunity
[Opportunity title]

Best Matching Profile
[Profile name] - [Score] %

Application Profile
[Profile selector]

Initial Status
Applied

Source
Opportunity

[Cancel]
[Create Application]
```

---

## 9.2 Informations obligatoires

Le dialogue affiche :

- le titre de l’opportunité ;
- l’entreprise si disponible ;
- le Best Matching Profile si disponible ;
- le score du Best Matching Profile ;
- le profil qui sera attribué ;
- le statut initial ;
- la source ;
- une action Cancel ;
- une action Create Application.

---

## 9.3 Sélecteur Application Profile

Le champ est :

```text
modifiable
obligatoire
```

Exemple :

```tsx
<select
  value={applicationProfileId ?? ""}
  onChange={(event) => setApplicationProfileId(Number(event.target.value))}>
  {profiles.map((profile) => (
    <option key={profile.id} value={profile.id}>
      {profile.profile_name}
    </option>
  ))}
</select>
```

Seuls les profils disponibles chargés par la page doivent être proposés.

Les profils archivés sont déjà exclus si la liste `profiles` reste filtrée par `is_active`.

Le backend effectue néanmoins sa propre validation.

---

## 9.4 Best Matching Profile

Lorsque le résultat existe :

```text
Best Matching Profile
Product Manager
92 %
```

Lorsque le résultat est indisponible :

```text
Matching scores are unavailable.
The Primary Profile has been selected by default.
```

Le message ne doit pas prétendre qu’un profil est le meilleur si aucun score exploitable n’est disponible.

---

## 9.5 Override utilisateur

Lorsque l’utilisateur choisit un autre profil, le dialogue doit conserver l’affichage informatif du Best Matching Profile.

Exemple :

```text
Best Matching Profile
Product Manager - 92 %

Application Profile
Solution Architect
```

Les deux concepts restent visuellement distincts.

Le changement de l’Application Profile ne doit pas modifier :

```text
selectedProfileId
activeProfileIds
bestProfileScore
matching
ranking
```

---

# 10. Confirmation de création

## Fonction cible

```typescript
async function handleCreateApplication() {
  if (!selectedOffer || applicationProfileId === null) {
    setApplicationCreationError("An application profile is required.");

    return;
  }

  setCreatingApplication(true);
  setApplicationCreationError(null);

  try {
    await createApplication({
      profile_id: applicationProfileId,
      job_offer_id: selectedOffer.id,
      status: "Applied",
      notes: null,
      source_type: "OPPORTUNITY",
    });

    const refreshedApplications = await getApplications();

    setApplications(
      Array.isArray(refreshedApplications)
        ? refreshedApplications
        : (refreshedApplications.value ?? []),
    );

    setIsCreateApplicationModalOpen(false);
    setApplicationProfileId(null);
  } catch (error) {
    setApplicationCreationError(
      error instanceof Error ? error.message : "Unable to create application.",
    );
  } finally {
    setCreatingApplication(false);
  }
}
```

La fonction doit utiliser :

```text
applicationProfileId
```

et non :

```text
selectedProfileId
```

---

# 11. Fermeture de la boîte de dialogue

La fermeture doit nettoyer l’état temporaire :

```typescript
function closeCreateApplicationModal() {
  if (creatingApplication) {
    return;
  }

  setIsCreateApplicationModalOpen(false);
  setApplicationProfileId(null);
  setApplicationCreationError(null);
}
```

Le bouton Cancel est désactivé ou ignoré pendant l’appel de création afin d’éviter un état incohérent.

---

# 12. Gestion des erreurs dans OpportunitiesPage

## Profil absent

```text
An application profile is required.
```

## Profil rejeté par le backend

Afficher le message backend lorsqu’il est disponible.

Exemple :

```text
The selected profile is not available.
```

## Offre inexistante

```text
Job offer not found.
```

## Erreur générique

```text
Unable to create application.
```

La boîte de dialogue reste ouverte en cas d’erreur.

La sélection utilisateur reste conservée.

---

# 13. Type Profile utilisé dans OpportunitiesPage

Le type importé depuis `api.ts` possède les données nécessaires :

```typescript
id;
profile_name;
full_name;
is_active;
```

Le filtre actuel :

```typescript
const availableProfiles = profileList.filter(
  (profile: Profile) => profile.is_active,
);
```

doit être conservé.

La boîte de dialogue réutilise :

```text
profiles
```

et ne charge pas une deuxième liste de profils.

---

# 14. Best Matching Profile actif

Le Best Matching Profile utilisé pour la présélection doit être dérivé uniquement des Active Profiles.

La logique actuelle :

```typescript
const activeProfileScores = profileScores.filter((score) =>
  activeProfileIds.includes(score.profile_id),
);
```

doit être conservée.

Le Best Matching Profile de présélection ne doit pas provenir d’un profil non actif dans le contexte.

Le backend peut retourner les scores de plusieurs profils, mais le contexte frontend limite la présélection aux Active Profiles.

---

# 15. Gestion des égalités

Le frontend doit utiliser l’ordre déterministe des scores reçus.

Si le Primary Profile est ex æquo au meilleur score, le Primary Profile doit être préféré.

Fonction cible :

```typescript
function getBestActiveProfileScore() {
  const sortedScores = [...activeProfileScores].sort(
    (firstScore, secondScore) => {
      const scoreDifference =
        secondScore.matching_score - firstScore.matching_score;

      if (scoreDifference !== 0) {
        return scoreDifference;
      }

      if (firstScore.profile_id === selectedProfileId) {
        return -1;
      }

      if (secondScore.profile_id === selectedProfileId) {
        return 1;
      }

      return firstScore.profile_id - secondScore.profile_id;
    },
  );

  return sortedScores[0] ?? null;
}
```

Cette logique est une règle de sélection contextuelle.

Elle ne recalcule aucun score.

Une alternative acceptable consiste à recevoir l’ordre entièrement déterminé par le backend.

Le choix final devra rester identique dans les tests frontend et backend.

---

# 16. ApplicationsPage - Création manuelle

## 16.1 Comportement actuel

La boîte de dialogue manuelle possède déjà :

```text
Profile
Opportunity
Source
Notes
```

Le profil initial est actuellement :

```typescript
profiles[0].id;
```

---

## 16.2 Comportement cible

La création manuelle n’a pas nécessairement accès au contexte Opportunities.

Règle :

```text
Si un profileId est transmis dans navigation state
↓
utiliser ce profil

Sinon
↓
utiliser le premier profil disponible
```

Le profil reste modifiable.

Aucun appel supplémentaire au matching n’est nécessaire pour la création manuelle.

---

## 16.3 Profils disponibles

Le type local actuel est :

```typescript
type ProfileSummary = {
  id: number;
  full_name: string;
};
```

Il ne contient pas :

```typescript
is_active;
```

Le design recommande de supprimer ce type local et de réutiliser :

```typescript
type Profile
```

importé depuis `api.ts`.

Cela permet de filtrer explicitement :

```typescript
profiles.filter((profile) => profile.is_active);
```

Si le contrat réel de `/profiles` ne contient pas `is_active`, le type et le filtrage devront être ajustés à partir du schéma backend réel.

Aucune propriété ne doit être inventée dans l’implémentation.

---

# 17. Réattribution dans ApplicationsPage

## 17.1 Nouveaux états

Ajouter :

```typescript
const [isProfileChangeModalOpen, setIsProfileChangeModalOpen] = useState(false);
```

```typescript
const [profileChangeDraftId, setProfileChangeDraftId] = useState<number | null>(
  null,
);
```

```typescript
const [changingProfile, setChangingProfile] = useState(false);
```

```typescript
const [profileChangeError, setProfileChangeError] = useState<string | null>(
  null,
);
```

---

## 17.2 Ouverture

Dans Application Detail, le bloc Profile affiche actuellement :

```text
Profile name
Open Profile
```

Ajouter :

```text
Change Profile
```

Fonction cible :

```typescript
function openProfileChangeModal() {
  if (!selectedApplication) {
    return;
  }

  setProfileChangeDraftId(selectedApplication.profile_id);
  setProfileChangeError(null);
  setIsProfileChangeModalOpen(true);
}
```

---

# 18. Boîte de dialogue de réattribution

## Structure

```text
Change Application Profile

Current Profile
Product Manager

New Profile
[Solution Architect ▼]

This change will update the profile used
for this application.

The opportunity, status, source, notes
and existing timeline will remain unchanged.

[Cancel]
[Confirm Change]
```

---

## Sélecteur

La liste contient uniquement les profils disponibles.

Le profil actuel peut rester sélectionné.

Le bouton de confirmation est désactivé si :

```text
aucun profil sélectionné
```

ou :

```text
profil sélectionné
=
profil actuel
```

---

# 19. Confirmation de réattribution

## Fonction cible

```typescript
async function confirmProfileChange() {
  if (!selectedApplication || profileChangeDraftId === null) {
    return;
  }

  if (profileChangeDraftId === selectedApplication.profile_id) {
    return;
  }

  setChangingProfile(true);
  setProfileChangeError(null);
  setActionMessage(null);

  try {
    const updatedApplication = await updateApplication(selectedApplication.id, {
      profile_id: profileChangeDraftId,
      status: selectedApplication.status,
      notes: selectedApplication.notes,
      source_type: selectedApplication.source_type,
    });

    setSelectedApplication(updatedApplication);

    replaceApplicationInList(updatedApplication);

    setNotesDraft(updatedApplication.notes ?? "");

    setSourceDraft(updatedApplication.source_type);

    await Promise.all([
      loadTimeline(updatedApplication.id),
      loadMatchingScore(updatedApplication),
    ]);

    setIsProfileChangeModalOpen(false);
    setProfileChangeDraftId(null);

    setActionMessage({
      type: "success",
      text: "Application profile updated successfully.",
    });
  } catch (error) {
    setProfileChangeError(
      error instanceof Error
        ? error.message
        : "Unable to update " + "the application profile.",
    );
  } finally {
    setChangingProfile(false);
  }
}
```

---

# 20. Rafraîchissement après réattribution

Après une réattribution, les éléments suivants doivent être mis à jour :

```text
selectedApplication
applications list
profile name displayed in the list
profile name displayed in details
matching score
timeline
```

Le score de matching doit être rechargé avec :

```text
nouveau profile_id
+
même job_offer_id
```

Le changement de profil ne modifie pas :

```text
selected opportunity
notes
source
status
Primary Profile
Active Profiles
```

---

# 21. Évolution du contrat API frontend

## Fichier

```text
frontend/src/services/api.ts
```

## Type actuel

```typescript
export type ApplicationUpdatePayload = {
  status: string;
  notes: string | null;
  source_type: string;
};
```

## Type cible

```typescript
export type ApplicationUpdatePayload = {
  profile_id: number;
  status: string;
  notes: string | null;
  source_type: string;
};
```

La fonction :

```typescript
updateApplication();
```

ne change pas de route.

Elle continue d’appeler :

```text
PUT /applications/{applicationId}
```

---

# 22. Adaptation de Save Notes

L’appel actuel transmet :

```typescript
{
  status: selectedApplication.status,
  notes: notesDraft,
  source_type:
    selectedApplication.source_type,
}
```

Il doit transmettre :

```typescript
{
  profile_id:
    selectedApplication.profile_id,
  status:
    selectedApplication.status,
  notes:
    notesDraft,
  source_type:
    selectedApplication.source_type,
}
```

Cette adaptation est obligatoire pour éviter une erreur de validation backend.

---

# 23. Adaptation de Save Source

L’appel actuel transmet :

```typescript
{
  status: selectedApplication.status,
  notes: notesDraft,
  source_type: sourceDraft,
}
```

Il doit transmettre :

```typescript
{
  profile_id:
    selectedApplication.profile_id,
  status:
    selectedApplication.status,
  notes:
    notesDraft,
  source_type:
    sourceDraft,
}
```

Cette adaptation conserve l’attribution existante.

---

# 24. Transition de statut

La transition de statut utilise une route dédiée :

```text
POST /applications/{application_id}/status
```

Le payload reste :

```typescript
{
  status: string;
}
```

Aucun `profile_id` ne doit être ajouté à ce contrat.

La transition de statut ne modifie pas l’attribution du profil.

---

# 25. Timeline PROFILE_CHANGED

## 25.1 Données backend

La timeline recevra :

```json
{
  "event_type": "PROFILE_CHANGED",
  "old_value": "12",
  "new_value": "17"
}
```

## 25.2 Affichage utilisateur

Affichage recommandé :

```text
Application Profile Changed
Product Manager → Solution Architect
```

## 25.3 Traduction des identifiants

L’événement contient des identifiants sous forme de chaînes.

Le composant Timeline doit utiliser la table de correspondance des profils pour afficher les noms.

Si un identifiant ne peut pas être résolu :

```text
Profile 12 → Profile 17
```

Le frontend ne doit pas masquer l’événement.

---

# 26. Évolution de ApplicationTimeline

## Fichier probable

```text
frontend/src/components/ApplicationTimeline.tsx
```

Le composant doit reconnaître :

```text
STATUS_CHANGED
PROFILE_CHANGED
```

Pour `PROFILE_CHANGED`, il doit afficher :

```text
Application Profile Changed
```

Les valeurs `old_value` et `new_value` doivent être converties en libellés de profils.

## Évolution des propriétés

Le composant peut recevoir :

```typescript
profileNames: Record<number, string>;
```

ou une fonction :

```typescript
getProfileName: (profileId: number) => string;
```

Exemple recommandé :

```tsx
<ApplicationTimeline
  events={timeline}
  createdAt={selectedApplication.created_at}
  getProfileName={getProfileName}
/>
```

Le choix exact dépend de la structure réelle du composant, qui devra être auditée avant modification.

---

# 27. États de chargement

## Création depuis Opportunities

Pendant la création :

```text
bouton Create Application désactivé
sélecteur désactivé
bouton Cancel protégé
libellé Creating...
```

## Réattribution

Pendant la réattribution :

```text
sélecteur désactivé
Confirm Change désactivé
Cancel protégé
libellé Updating...
```

Les actions multiples doivent être empêchées.

---

# 28. Accessibilité

Les dialogues doivent :

- posséder un titre visible ;
- associer chaque label à son champ ;
- permettre la navigation clavier ;
- placer le focus initial sur le champ Application Profile ;
- permettre la fermeture avec Cancel ;
- empêcher les soumissions multiples ;
- exposer les erreurs près des actions ;
- conserver un contraste suffisant ;
- éviter de transmettre l’information uniquement par couleur.

Le Best Matching Profile doit être accompagné d’un texte explicite.

Une icône seule ne suffit pas.

---

# 29. Comportement responsive

Les dialogues doivent rester utilisables sur une largeur réduite.

Recommandation :

```text
width: 100 %
max-width: xl
padding horizontal
```

Les boutons peuvent passer sur plusieurs lignes si nécessaire.

Le sélecteur utilise toute la largeur disponible.

Les informations Opportunity, Best Matching Profile et Application Profile doivent rester lisibles sans tableau horizontal.

---

# 30. Composant partagé ou implémentation locale

## Décision MVP

Les deux dialogues peuvent rester dans leurs pages respectives :

```text
OpportunitiesPage
→ Create Application dialog

ApplicationsPage
→ Change Application Profile dialog
```

Aucun composant abstrait partagé n’est requis dans le premier jalon.

Justification :

- les deux dialogues ont des objectifs différents ;
- les données affichées sont différentes ;
- une abstraction prématurée augmenterait le périmètre ;
- le repository utilise déjà plusieurs dialogues locaux aux pages.

Une extraction future pourra être réalisée si la duplication réelle le justifie.

---

# 31. Fichiers frontend concernés

## Fichiers à modifier

```text
frontend/src/pages/OpportunitiesPage.tsx
frontend/src/pages/ApplicationsPage.tsx
frontend/src/services/api.ts
```

## Fichier probablement à modifier

```text
frontend/src/components/ApplicationTimeline.tsx
```

Sa modification dépend de l’audit de son contenu réel.

## Aucun nouveau composant obligatoire

```text
Aucun nouveau fichier React obligatoire
```

---

# 32. Tests frontend attendus

Le repository ne dispose pas encore d’une preuve fournie ici concernant un framework de tests frontend.

Aucun fichier de test ne doit être inventé sans audit préalable du frontend.

Les scénarios de validation obligatoires sont cependant définis ci-dessous.

---

## 32.1 Ouverture depuis Opportunities

```text
Given
une opportunité sans candidature

When
Create Application est sélectionné

Then
aucune candidature n’est créée immédiatement

And
la boîte de dialogue est affichée
```

---

## 32.2 Présélection Best Matching Profile

```text
Given
plusieurs Active Profiles

And
un Best Matching Profile disponible

When
la boîte de dialogue est ouverte

Then
Application Profile utilise
le Best Matching Profile
```

---

## 32.3 Override utilisateur

```text
Given
le Best Matching Profile présélectionné

When
l’utilisateur sélectionne un autre profil

And
confirme

Then
le payload contient le profil choisi
```

---

## 32.4 Fallback Primary Profile

```text
Given
aucun Best Matching Profile disponible

When
la boîte de dialogue est ouverte

Then
le Primary Profile est présélectionné
```

---

## 32.5 Création bloquée sans profil

```text
Given
aucun profil disponible

When
la création est demandée

Then
le bouton de confirmation est désactivé

And
aucun appel API n’est exécuté
```

---

## 32.6 Réattribution

```text
Given
une candidature attribuée au profil 12

When
le profil 17 est sélectionné

And
la modification est confirmée

Then
PUT /applications/{id}
contient profile_id 17
```

---

## 32.7 Rafraîchissement du matching

```text
Given
une réattribution réussie

When
la réponse backend est reçue

Then
le matching est rechargé
avec le nouveau profile_id
```

---

## 32.8 Timeline

```text
Given
un événement PROFILE_CHANGED

When
la timeline est affichée

Then
l’ancien et le nouveau profil
sont affichés
```

---

## 32.9 Notes non régressées

```text
Given
une candidature existante

When
les notes sont sauvegardées

Then
le payload conserve
le profile_id existant
```

---

## 32.10 Source non régressée

```text
Given
une candidature existante

When
la source est sauvegardée

Then
le payload conserve
le profile_id existant
```

---

## 32.11 Primary Profile inchangé

```text
Given
une candidature créée
avec un profil différent
du Primary Profile

When
la création est confirmée

Then
le Primary Profile reste inchangé
```

---

# 33. Validation manuelle

## Parcours 1

```text
Ouvrir Opportunities
Activer plusieurs profils
Choisir un Primary Profile
Sélectionner une opportunité
Vérifier le Best Matching Profile
Cliquer Create Application
Vérifier la présélection
Choisir un autre profil
Créer la candidature
Ouvrir Applications
Vérifier le profil attribué
```

## Parcours 2

```text
Ouvrir une candidature
Cliquer Change Profile
Sélectionner un autre profil
Confirmer
Vérifier le détail
Vérifier la liste
Vérifier le score de matching
Vérifier la timeline
```

## Parcours 3

```text
Modifier les notes
Vérifier que le profil ne change pas
Modifier la source
Vérifier que le profil ne change pas
Modifier le statut
Vérifier que le profil ne change pas
```

## Parcours 4

```text
Changer le Primary Profile
Retourner dans Applications
Vérifier que les candidatures existantes
conservent leur profile_id
```

---

# 34. Risques frontend

## Risque 1

La page continue de créer la candidature immédiatement.

Mitigation :

```text
Remplacer l’appel direct
par l’ouverture du dialogue.
```

## Risque 2

Le meilleur profil est pris parmi tous les profils au lieu des Active Profiles.

Mitigation :

```text
Conserver activeProfileScores
comme périmètre de présélection.
```

## Risque 3

Save Notes ou Save Source échoue après ajout de `profile_id` obligatoire.

Mitigation :

```text
Modifier tous les appels
updateApplication().
```

## Risque 4

Le score affiché reste celui de l’ancien profil après réattribution.

Mitigation :

```text
Recharger loadMatchingScore().
```

## Risque 5

La timeline affiche uniquement des identifiants techniques.

Mitigation :

```text
Résoudre les identifiants
avec profileNames.
```

## Risque 6

Le changement d’Application Profile modifie par erreur le Primary Profile.

Mitigation :

```text
Ne jamais appeler
setSelectedProfileId()
pendant la création
ou la réattribution.
```

---

# 35. Ordre d’implémentation frontend

## Étape 1

Modifier le contrat :

```text
ApplicationUpdatePayload
```

pour inclure :

```text
profile_id
```

## Étape 2

Adapter Save Notes.

## Étape 3

Adapter Save Source.

## Étape 4

Ajouter la boîte de dialogue de création dans OpportunitiesPage.

## Étape 5

Brancher la présélection du Best Matching Profile.

## Étape 6

Ajouter le fallback Primary Profile.

## Étape 7

Ajouter l’override utilisateur.

## Étape 8

Ajouter Change Profile dans ApplicationsPage.

## Étape 9

Brancher la réattribution.

## Étape 10

Recharger détail, liste, matching et timeline.

## Étape 11

Afficher `PROFILE_CHANGED`.

## Étape 12

Exécuter le build frontend.

## Étape 13

Exécuter les validations manuelles.

## Étape 14

Effectuer un commit frontend dédié.

---

# 36. Critères de fin frontend

La partie frontend de 7.1.22.10 est terminée lorsque :

```text
✓ Create Application n’est plus immédiat
✓ une boîte de dialogue est affichée
✓ Best Matching Profile est présélectionné
✓ le Primary Profile sert de fallback
✓ l’utilisateur peut changer le profil
✓ le profil choisi est envoyé au backend
✓ Primary Profile reste inchangé
✓ Active Profiles restent inchangés
✓ Change Profile existe dans Applications
✓ la réattribution est confirmée explicitement
✓ le détail est rafraîchi
✓ la liste est rafraîchie
✓ le matching est rafraîchi
✓ la timeline est rafraîchie
✓ PROFILE_CHANGED est lisible
✓ Save Notes conserve profile_id
✓ Save Source conserve profile_id
✓ les transitions de statut restent fonctionnelles
✓ le build frontend passe
✓ la validation manuelle passe
```

---

# 37. Hors périmètre frontend

Ce design n’introduit pas :

- candidature automatique ;
- plusieurs candidatures automatiques ;
- persistance du Primary Profile ;
- persistance des Active Profiles ;
- changement automatique après recalcul ;
- changement automatique après modification du contexte ;
- modification du moteur de matching ;
- score combiné ;
- génération de CV ;
- sélection automatique d’un CV ;
- lettre de motivation ;
- soumission externe ;
- nouveau système de formulaires global ;
- nouveau gestionnaire d’état global ;
- refactoring complet de OpportunitiesPage ;
- refactoring complet de ApplicationsPage.

---

# 38. Décision technique finale

La création depuis Opportunities utilise désormais :

```text
Create Application
↓
Dialogue
↓
Best Matching Profile présélectionné
↓
Override utilisateur possible
↓
POST /applications
```

La création manuelle conserve son sélecteur de profil.

La réattribution utilise :

```text
Change Profile
↓
Dialogue de confirmation
↓
PUT /applications/{application_id}
↓
PROFILE_CHANGED
```

Le contrat frontend `ApplicationUpdatePayload` inclut `profile_id`.

Tous les appels existants à `updateApplication()` conservent explicitement le profil courant.

Le frontend réutilise les données de matching existantes.

Aucun score n’est calculé dans le frontend.

Le Primary Profile et l’Application Profile restent indépendants.

L’utilisateur conserve le contrôle final de l’attribution.
