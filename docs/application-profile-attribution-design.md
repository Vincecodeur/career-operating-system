# Application Profile Attribution Design

## Phase

7.1.22.10 Application Profile Attribution

## Statut

Design

## Date

2026-08-20

---

# 1. Objectif

Définir les règles métier permettant d’attribuer un profil à une candidature dans un contexte multi-profils.

Le système supporte désormais :

```text
1 Primary Profile
+
1..N Active Profiles
+
1 Best Matching Profile par opportunité
```

Une candidature reste cependant associée à un seul profil.

Relation métier :

```text
Application
+
Profile
+
JobOffer
```

Ce document définit :

- quel profil est présélectionné lors de la création d’une candidature ;
- comment l’utilisateur peut modifier ce profil ;
- comment le `profile_id` est enregistré ;
- si le `profile_id` peut être modifié après la création ;
- l’impact d’un changement du Primary Profile ;
- les règles de validation ;
- les cas limites ;
- les éléments hors périmètre.

---

# 2. Contexte métier

Une même opportunité peut être évaluée indépendamment pour plusieurs profils actifs.

Exemple :

```text
Opportunity
Product Manager
92 %

Solution Architect
58 %

Technical Partnerships Manager
41 %
```

Dans cet exemple :

```text
Best Matching Profile
=
Product Manager
```

Le Primary Profile peut être différent du Best Matching Profile.

Exemple :

```text
Primary Profile
=
Technical Partnerships Manager

Best Matching Profile
=
Product Manager
```

La création d’une candidature doit permettre à l’utilisateur de choisir explicitement le profil qui sera réellement utilisé pour cette candidature.

Le système doit faciliter ce choix sans retirer à l’utilisateur le contrôle final.

---

# 3. Définitions

## 3.1 Primary Profile

Le Primary Profile est le profil principal du contexte Opportunities.

Le Primary Profile pilote :

- le classement des opportunités ;
- les filtres basés sur le score ;
- le score principal affiché sur les cartes ;
- le contexte d’analyse sélectionné par défaut.

Le Primary Profile n’est pas nécessairement le profil attribué à une nouvelle candidature.

---

## 3.2 Active Profiles

Les Active Profiles sont les profils inclus dans le contexte de comparaison d’une opportunité.

Les scores restent calculés indépendamment pour chaque profil actif.

L’activation de plusieurs profils ne crée pas automatiquement plusieurs candidatures.

---

## 3.3 Best Matching Profile

Le Best Matching Profile est le profil actif possédant le score de matching le plus élevé pour l’opportunité sélectionnée.

Exemple :

```text
Product Manager
92 %

Solution Architect
58 %

Technical Partnerships Manager
41 %
```

Résultat :

```text
Best Matching Profile
=
Product Manager
```

Le Best Matching Profile est calculé à partir des résultats de matching produits par le backend.

Le frontend ne calcule pas le score.

Le frontend ne détermine pas seul le Best Matching Profile à partir de règles métier locales.

---

## 3.4 Application Profile

L’Application Profile est le profil effectivement attribué à la candidature.

Il est enregistré dans :

```text
Application.profile_id
```

L’Application Profile peut initialement correspondre au Best Matching Profile, puis être modifié par l’utilisateur.

Après validation de la création, la valeur sélectionnée devient la source de vérité de la candidature.

---

# 4. Décisions produit validées

## Décision 1

Lorsqu’une candidature est créée depuis une opportunité, le Best Matching Profile est présélectionné.

Règle :

```text
Application Profile initial
=
Best Matching Profile
```

Exemple :

```text
Primary Profile
=
Technical Partnerships Manager

Best Matching Profile
=
Product Manager
```

Lors de l’ouverture du formulaire :

```text
Application Profile
=
Product Manager
```

Le système ne présélectionne pas automatiquement le Primary Profile si un Best Matching Profile valide est disponible.

---

## Décision 2

Le profil présélectionné reste modifiable avant validation.

Le formulaire de création affiche un sélecteur de profil.

L’utilisateur peut remplacer le Best Matching Profile par un autre profil disponible.

Exemple :

```text
Profil présélectionné
=
Product Manager

Choix utilisateur
=
Solution Architect
```

Résultat lors de la validation :

```text
Application.profile_id
=
Solution Architect
```

Le choix explicite de l’utilisateur remplace toujours la présélection automatique.

---

## Décision 3

Le `profile_id` peut être modifié après la création de la candidature.

Une candidature existante peut être réattribuée à un autre profil disponible.

Exemple avant modification :

```text
Application 42
profile_id
=
Product Manager
```

Exemple après modification :

```text
Application 42
profile_id
=
Solution Architect
```

La modification doit être explicite.

Le système ne modifie jamais automatiquement le `profile_id` d’une candidature existante.

---

## Décision 4

Un changement du Primary Profile n’a aucun impact sur les candidatures existantes.

Exemple :

```text
Application 42
profile_id
=
Product Manager
```

Puis :

```text
Primary Profile
=
Solution Architect
```

Résultat :

```text
Application 42
profile_id
=
Product Manager
```

Le changement du contexte Opportunities ne réattribue aucune candidature existante.

---

# 5. Règle générale d’attribution

Le flux d’attribution est le suivant :

```text
Opportunity sélectionnée
↓
Scores des Active Profiles disponibles
↓
Best Matching Profile identifié par le backend
↓
Best Matching Profile présélectionné
↓
Utilisateur conserve ou modifie le profil
↓
Validation utilisateur
↓
Application créée avec le profile_id sélectionné
```

Règle finale :

```text
Application.profile_id
=
profil sélectionné au moment de la validation
```

La présélection est une suggestion.

La sélection validée par l’utilisateur est la décision finale.

---

# 6. Périmètre de la présélection

## 6.1 Profils éligibles

Le Best Matching Profile doit être recherché parmi les Active Profiles du contexte courant.

Un profil inactif dans le contexte ne doit pas être présélectionné automatiquement.

Un profil archivé ne doit pas être présélectionné.

Un profil inexistant ne doit pas être présélectionné.

---

## 6.2 Profil disponible pour modification

Le sélecteur de profil doit proposer les profils disponibles autorisés par le produit.

Pour le MVP, un profil archivé ne doit pas pouvoir être sélectionné pour une nouvelle candidature.

Une candidature existante associée à un profil ensuite archivé conserve son `profile_id`.

L’archivage ultérieur du profil ne doit pas réattribuer automatiquement la candidature.

---

# 7. Détermination du Best Matching Profile

Le Best Matching Profile est déterminé à partir des scores de matching backend.

Règle :

```text
Best Matching Profile
=
profil actif avec le matching_score le plus élevé
```

Exemple :

```text
Primary Profile
Technical Partnerships Manager
72 %

Active Profile
Product Manager
89 %

Active Profile
Solution Architect
81 %
```

Résultat :

```text
Best Matching Profile
=
Product Manager
```

Profil présélectionné dans le formulaire :

```text
Product Manager
```

Le Primary Profile reste inchangé.

La présélection du Best Matching Profile ne transforme pas le Best Matching Profile en Primary Profile.

---

# 8. Gestion des égalités

Plusieurs profils peuvent obtenir le même score maximal.

Exemple :

```text
Product Manager
88 %

Solution Architect
88 %
```

Une règle déterministe est nécessaire.

Règle MVP :

```text
Si le Primary Profile fait partie des profils ex æquo,
le Primary Profile est présélectionné.
```

Exemple :

```text
Primary Profile
=
Solution Architect

Product Manager
88 %

Solution Architect
88 %
```

Résultat :

```text
Application Profile présélectionné
=
Solution Architect
```

Si le Primary Profile ne fait pas partie des profils ex æquo, le premier profil retourné par l’API backend dans l’ordre déterministe du classement est présélectionné.

Le backend doit fournir un ordre stable.

Le frontend ne doit pas inventer une règle différente.

---

# 9. Absence de score disponible

Il est possible que les scores ne soient pas disponibles.

Exemples :

- erreur de chargement ;
- aucun résultat de matching ;
- aucun Active Profile évaluable ;
- opportunité incomplète ;
- endpoint indisponible.

Dans ce cas, le système utilise le Primary Profile comme fallback.

Règle :

```text
Si Best Matching Profile indisponible
↓
Application Profile initial
=
Primary Profile
```

Le formulaire reste modifiable.

Si aucun profil valide n’est disponible, la création de candidature doit être bloquée avec un message explicite.

Le système ne doit jamais envoyer un `profile_id` vide ou inventé.

---

# 10. Création depuis une opportunité

## 10.1 Déclenchement

Le flux commence lorsque l’utilisateur sélectionne :

```text
Create Application
```

depuis une opportunité qui ne possède pas encore la candidature ciblée.

## 10.2 Formulaire obligatoire

La candidature ne doit pas être créée immédiatement au clic initial.

Un formulaire ou une boîte de dialogue doit permettre de vérifier au minimum :

```text
Application Profile
Opportunity
Initial Status
Source Type
```

## 10.3 Valeurs initiales

Valeurs MVP :

```text
Application Profile
=
Best Matching Profile

Fallback
=
Primary Profile

Opportunity
=
opportunité sélectionnée

Initial Status
=
Applied

Source Type
=
OPPORTUNITY
```

## 10.4 Validation

Avant l’envoi :

- un profil doit être sélectionné ;
- le profil doit exister ;
- le profil ne doit pas être archivé pour une nouvelle candidature ;
- l’opportunité doit exister ;
- le choix utilisateur doit être visible ;
- l’utilisateur doit pouvoir modifier le profil.

## 10.5 Persistance

Après validation :

```text
Application.profile_id
=
profil sélectionné

Application.job_offer_id
=
opportunité sélectionnée

Application.status
=
Applied

Application.source_type
=
OPPORTUNITY
```

---

# 11. Création manuelle

Pour une candidature créée manuellement, aucun Best Matching Profile n’est nécessairement disponible.

Règle MVP :

```text
Création manuelle
↓
Primary Profile présélectionné si disponible
↓
Utilisateur peut modifier le profil
↓
Validation
↓
Application.profile_id enregistré
```

Si aucun Primary Profile n’est disponible dans ce contexte, le premier profil disponible peut être proposé.

Le profil reste modifiable avant validation.

La création manuelle ne doit pas déclencher artificiellement un calcul de matching uniquement pour présélectionner un profil.

---

# 12. Modification après création

## 12.1 Règle

Le profil d’une candidature existante peut être modifié.

Le changement est déclenché explicitement par l’utilisateur.

## 12.2 Comportement attendu

Avant :

```text
Application 42
profile_id
=
12
```

Après modification :

```text
Application 42
profile_id
=
17
```

L’opportunité liée reste inchangée.

Le statut reste inchangé.

Les notes restent inchangées.

La source reste inchangée.

La timeline existante reste conservée.

## 12.3 Validation

Le nouveau profil :

- doit exister ;
- doit être disponible selon les règles métier ;
- ne doit pas être archivé au moment de la réattribution.

Une valeur inconnue doit être rejetée.

## 12.4 Audit métier

Une réattribution modifie une donnée structurante de la candidature.

Le changement doit être traçable dans l’historique applicatif.

Évolution attendue de la timeline :

```text
PROFILE_CHANGED
old_value
=
ancien profile_id

new_value
=
nouveau profile_id
```

Le nom définitif de l’événement devra être validé pendant le design backend de cette phase.

Aucun type d’événement ne doit être ajouté au code avant validation du contrat technique correspondant.

---

# 13. Indépendance du contexte Opportunities

Le contexte Opportunities et les candidatures existantes sont indépendants.

Les actions suivantes ne modifient pas une candidature existante :

- changement du Primary Profile ;
- activation d’un profil ;
- désactivation d’un profil ;
- changement du Best Matching Profile ;
- recalcul des scores ;
- changement du classement ;
- changement des filtres ;
- fin de session ;
- réinitialisation du contexte.

Principe :

```text
Opportunity Context
=
contexte temporaire d’analyse

Application.profile_id
=
donnée persistée de la candidature
```

La donnée persistée ne suit pas automatiquement le contexte temporaire.

---

# 14. Impact du recalcul du matching

Les scores peuvent évoluer après modification d’un profil ou d’une offre.

Exemple initial :

```text
Product Manager
92 %

Solution Architect
81 %
```

Candidature créée avec :

```text
profile_id
=
Product Manager
```

Après évolution du profil :

```text
Product Manager
76 %

Solution Architect
94 %
```

Résultat :

```text
Application.profile_id
reste
Product Manager
```

Le nouveau Best Matching Profile ne réattribue pas la candidature existante.

L’utilisateur peut choisir manuellement de modifier le profil de la candidature.

---

# 15. Plusieurs candidatures pour une même opportunité

Plusieurs Active Profiles ne créent jamais automatiquement plusieurs candidatures.

Ce document n’autorise pas la création automatique d’une candidature par profil actif.

Le système reste fondé sur une action explicite de l’utilisateur.

La gestion de plusieurs candidatures distinctes pour une même opportunité et plusieurs profils doit respecter les contraintes d’unicité réellement présentes dans le modèle.

Aucune nouvelle règle d’unicité n’est introduite par ce document sans audit préalable du modèle `Application`.

---

# 16. Règles de suppression et d’archivage

## Profil archivé après création

Une candidature existante conserve son `profile_id`.

Le système ne réattribue pas automatiquement la candidature.

L’interface doit pouvoir signaler que le profil lié est archivé.

## Profil supprimé physiquement

Le comportement dépend des contraintes de clé étrangère existantes.

Aucune suppression physique de profil n’est introduite par cette phase.

Le projet utilise déjà une stratégie d’archivage pour les profils.

## Opportunité archivée

L’archivage de l’opportunité ne modifie pas l’attribution du profil de la candidature.

---

# 17. Responsabilités backend

Le backend est responsable de :

- valider l’existence du profil ;
- valider l’éligibilité du profil ;
- persister `Application.profile_id` ;
- retourner les scores multi-profils ;
- retourner un ordre déterministe des scores ;
- rejeter un `profile_id` invalide ;
- gérer la modification du profil d’une candidature ;
- tracer la réattribution si un événement dédié est retenu ;
- préserver les autres données lors d’une réattribution.

Le backend reste la source de vérité.

---

# 18. Responsabilités frontend

Le frontend est responsable de :

- afficher le Best Matching Profile retourné par le backend ;
- présélectionner le Best Matching Profile dans le formulaire ;
- utiliser le Primary Profile comme fallback lorsque nécessaire ;
- afficher le profil sélectionné ;
- permettre la modification avant validation ;
- permettre la modification après création ;
- afficher les erreurs backend ;
- ne pas créer plusieurs candidatures automatiquement ;
- ne pas modifier le Primary Profile lors du changement d’Application Profile ;
- ne pas recalculer le matching.

Le frontend ne doit pas :

- inventer un score ;
- fusionner plusieurs profils ;
- envoyer un profil inexistant ;
- réattribuer automatiquement une candidature ;
- remplacer silencieusement le choix utilisateur ;
- transformer le Best Matching Profile en Primary Profile.

---

# 19. Expérience utilisateur

## 19.1 Formulaire de création

Le formulaire doit afficher :

```text
Create Application

Opportunity
[Opportunity title]

Best Matching Profile
Product Manager - 92 %

Application Profile
[Product Manager ▼]

Status
[Applied]

Source
[Opportunity]

[Cancel]
[Create Application]
```

Le champ Application Profile est prérempli mais modifiable.

## 19.2 Distinction visuelle

L’interface doit distinguer clairement :

```text
Best Matching Profile
```

et :

```text
Application Profile
```

Exemple :

```text
Best Matching Profile
Product Manager - 92 %

Application Profile
Solution Architect
```

Cette différence est valide lorsqu’elle résulte d’un choix utilisateur.

## 19.3 Modification d’une candidature

Dans le détail d’une candidature :

```text
Profile
Solution Architect

[Change Profile]
```

L’action ouvre un sélecteur.

La modification requiert une validation explicite.

## 19.4 Confirmation

Avant une réattribution :

```text
Change Application Profile

Current Profile
Product Manager

New Profile
Solution Architect

This change will not modify the opportunity,
status, notes or timeline history.

[Cancel]
[Confirm Change]
```

---

# 20. Messages utilisateur

## Aucun profil disponible

```text
No available profile can be assigned to this application.
```

## Scores indisponibles

```text
Matching scores are unavailable.
The Primary Profile has been selected by default.
```

## Profil invalide

```text
The selected profile is not available.
Choose another profile.
```

## Réattribution réussie

```text
Application profile updated successfully.
```

## Réattribution impossible

```text
Unable to update the application profile.
```

Les libellés définitifs devront respecter la stratégie d’internationalisation du frontend.

---

# 21. Cas fonctionnels

## Cas 1 : Best Matching Profile différent du Primary Profile

Contexte :

```text
Primary Profile
Technical Partnerships Manager

Active Profiles
Technical Partnerships Manager
Product Manager
Solution Architect

Best Matching Profile
Product Manager
```

Action :

```text
Create Application
```

Résultat :

```text
Application Profile présélectionné
=
Product Manager
```

---

## Cas 2 : utilisateur remplace le profil présélectionné

Présélection :

```text
Product Manager
```

Choix utilisateur :

```text
Solution Architect
```

Résultat :

```text
Application.profile_id
=
Solution Architect
```

---

## Cas 3 : modification après création

État initial :

```text
Application.profile_id
=
Product Manager
```

Action :

```text
Change Profile
→ Solution Architect
```

Résultat :

```text
Application.profile_id
=
Solution Architect
```

Les autres données restent inchangées.

---

## Cas 4 : changement du Primary Profile

État :

```text
Application.profile_id
=
Product Manager
```

Nouveau contexte :

```text
Primary Profile
=
Solution Architect
```

Résultat :

```text
Application.profile_id
=
Product Manager
```

---

## Cas 5 : Best Matching Profile indisponible

Contexte :

```text
Primary Profile
=
Technical Partnerships Manager

Matching scores
=
unavailable
```

Résultat :

```text
Application Profile présélectionné
=
Technical Partnerships Manager
```

Le profil reste modifiable.

---

## Cas 6 : plusieurs profils ex æquo, Primary Profile inclus

Scores :

```text
Primary Profile
Solution Architect
88 %

Product Manager
88 %
```

Résultat :

```text
Application Profile présélectionné
=
Solution Architect
```

---

## Cas 7 : profil archivé après création

État initial :

```text
Application.profile_id
=
Product Manager
```

Puis :

```text
Product Manager archived
```

Résultat :

```text
Application.profile_id
reste inchangé
```

Aucune réattribution automatique.

---

# 22. Compatibilité avec les décisions existantes

## DEC-009

Aucune candidature automatique.

Cette phase conserve l’action explicite de l’utilisateur.

La présélection d’un profil ne crée pas automatiquement une candidature.

## DEC-017

Le système supporte plusieurs profils candidats.

Cette phase permet de choisir lequel de ces profils est attribué à une candidature.

## DEC-033

Le ranking reste piloté par le backend.

Cette phase ne modifie pas le ranking.

## DEC-063

Une Application reste liée à un unique `profile_id`.

Cette phase conserve ce modèle et définit les règles d’attribution et de réattribution.

## DEC-065

Une opportunité peut créer une candidature liée à un profil.

Cette phase précise comment ce profil est présélectionné et validé.

## DEC-071

Le Primary Profile, les Active Profiles et le Best Matching Profile restent distincts.

Cette phase utilise le Best Matching Profile comme présélection de l’Application Profile.

Le choix utilisateur reste prioritaire.

Le changement de l’Application Profile ne modifie pas le Primary Profile.

---

# 23. Évolution de périmètre par rapport à DEC-071

DEC-071 indiquait que l’automatic Best Matching Profile preselection restait reportée à APP-005.

La décision produit prise pendant la phase 7.1.22.10 est désormais :

```text
Le Best Matching Profile est présélectionné
lors de la création d’une candidature depuis une opportunité.
```

Cette nouvelle décision modifie le périmètre prévu par DEC-071.

Conséquence documentaire obligatoire :

- DEC-071 devra être amendée ou complétée par une nouvelle DEC ;
- APP-005 devra être retirée du post-MVP backlog ou marquée comme intégrée au MVP ;
- `roadmap.md` devra être synchronisé ;
- `project-memory.md` devra être synchronisé ;
- `architecture.md` devra être synchronisé ;
- `handoff-prompt.md` devra être synchronisé.

Ces modifications seront réalisées uniquement pendant la phase de documentation dédiée, après validation technique et fonctionnelle.

---

# 24. Relation avec APP-005

APP-005 définit :

```text
Best Matching Profile Preselection
```

avec :

- présélection automatique du profil au meilleur score ;
- possibilité de modification par l’utilisateur ;
- maintien de la compatibilité du workflow.

Les décisions validées dans ce document couvrent désormais ce besoin pour la création depuis une opportunité.

APP-005 ne doit plus rester présenté comme entièrement hors périmètre MVP après implémentation et validation de cette phase.

État cible après clôture :

```text
APP-005
=
Implemented through 7.1.22.10
and 7.1.22.11
```

La clôture d’APP-005 ne doit intervenir qu’après :

- validation backend ;
- validation frontend ;
- validation fonctionnelle ;
- validation de la modification après création ;
- synchronisation documentaire.

---

# 25. Hors périmètre

Cette phase ne couvre pas :

- création automatique d’une candidature ;
- création d’une candidature pour chaque Active Profile ;
- fusion de plusieurs profils ;
- score multi-profils combiné ;
- changement automatique d’une candidature existante ;
- réattribution automatique après recalcul du matching ;
- réattribution automatique après changement du Primary Profile ;
- persistance du contexte Opportunities ;
- profil global par défaut ;
- sélection d’un CV spécifique au profil ;
- génération d’un CV adapté ;
- lettre de motivation ;
- candidature automatique sur une plateforme externe ;
- intelligence artificielle pour choisir le profil ;
- modification du matching ;
- modification du ranking.

---

# 26. Impacts techniques à auditer

Avant toute implémentation, les éléments suivants doivent être vérifiés dans le repository réel :

```text
Application model
ApplicationCreate schema
ApplicationUpdate schema
Application router
Application service
ApplicationEvent model
ApplicationEvent types
Create Application frontend flow
Manual Application frontend flow
OpportunitiesPage
ApplicationsPage
API client
Matching multi-profile endpoint
Profile availability rules
Profile archive rules
Database uniqueness constraints
Existing application tests
Existing matching tests
```

Aucune signature technique n’est définie définitivement dans ce document sans cet audit.

---

# 27. Tests fonctionnels attendus

## Création avec Best Matching Profile

```text
Given
plusieurs Active Profiles

And
un Best Matching Profile existe

When
le formulaire de création est ouvert

Then
le Best Matching Profile est présélectionné
```

## Override avant création

```text
Given
un Best Matching Profile est présélectionné

When
l’utilisateur sélectionne un autre profil

Then
la candidature est créée avec le profil choisi
```

## Modification après création

```text
Given
une candidature existante

When
l’utilisateur change son profil

Then
Application.profile_id est mis à jour
```

## Stabilité après changement de contexte

```text
Given
une candidature existante

When
le Primary Profile change

Then
Application.profile_id reste inchangé
```

## Stabilité après recalcul

```text
Given
une candidature existante

When
le Best Matching Profile change

Then
Application.profile_id reste inchangé
```

## Fallback Primary Profile

```text
Given
aucun Best Matching Profile disponible

When
le formulaire de création est ouvert

Then
le Primary Profile est présélectionné
```

## Profil invalide

```text
Given
un profile_id inconnu ou archivé

When
la création ou la réattribution est demandée

Then
la demande est rejetée
```

---

# 28. Critères de succès du design

La phase de design est considérée comme terminée lorsque les règles suivantes sont acceptées :

```text
✓ une Application conserve un seul profile_id
✓ Best Matching Profile présélectionné à la création
✓ profil présélectionné modifiable avant validation
✓ choix utilisateur prioritaire
✓ profile_id modifiable après création
✓ changement toujours explicite
✓ changement du Primary Profile sans impact rétroactif
✓ changement du Best Matching Profile sans impact rétroactif
✓ fallback vers Primary Profile si score indisponible
✓ aucune création automatique de plusieurs candidatures
✓ aucune modification du matching
✓ aucune modification du ranking
✓ impact APP-005 identifié
✓ impact DEC-071 identifié
```

---

# 29. Décision finale

Pour une candidature créée depuis une opportunité :

```text
Best Matching Profile
↓
Présélection du formulaire
↓
Utilisateur conserve ou modifie le profil
↓
Validation
↓
Application.profile_id persisté
```

Pour une candidature créée manuellement :

```text
Primary Profile ou premier profil disponible
↓
Présélection du formulaire
↓
Utilisateur conserve ou modifie le profil
↓
Validation
↓
Application.profile_id persisté
```

Après création :

```text
Application.profile_id
peut être modifié explicitement par l’utilisateur
```

Les événements suivants ne modifient jamais automatiquement une candidature existante :

```text
changement du Primary Profile
changement des Active Profiles
changement du Best Matching Profile
recalcul du matching
nouvelle session
```

Le choix utilisateur validé reste la source de vérité de l’attribution de la candidature.
