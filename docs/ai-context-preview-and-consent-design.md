# AI Context Preview And Consent Design

## Phase

7.1.23.12 AI Context Preview And Consent

### Statut

Implementation In Progress

Backend:
Completed

Frontend:
Pending

## Contexte

La phase 7.1.23.11 AI Context Contract a défini les données pouvant être utilisées par les futures fonctionnalités d’intelligence artificielle du Career Operating System.

Le contrat validé repose sur les principes suivants :

- le profil structuré constitue la source de vérité ;
- seules les données validées du profil peuvent être utilisées ;
- le contenu brut d’un CV ne doit pas être transmis à l’intelligence artificielle ;
- les propositions d’enrichissement non validées ne doivent pas être transmises ;
- les données techniques sensibles ne doivent jamais être transmises ;
- l’utilisateur doit pouvoir comprendre quelles données seront utilisées ;
- l’utilisateur doit donner un consentement explicite avant l’activation des fonctionnalités d’intelligence artificielle ;
- le consentement doit pouvoir être retiré.

Cette phase définit l’expérience utilisateur, les règles métier et l’architecture technique permettant :

- d’évaluer si un profil est prêt pour l’intelligence artificielle ;
- de présenter un aperçu du contexte qui pourra être transmis ;
- d’informer l’utilisateur sur les données exclues ;
- de recueillir un consentement explicite ;
- de mémoriser ce consentement ;
- de permettre sa révocation.

Aucun fournisseur réel d’intelligence artificielle n’est intégré pendant cette phase.

Aucun appel à un modèle externe n’est réalisé pendant cette phase.

---

## Objectif

Permettre à l’utilisateur de connaître précisément les catégories de données qui pourront être utilisées par les futures fonctionnalités d’intelligence artificielle avant tout appel à un fournisseur externe.

Le système doit fournir :

- un état AI Ready ou Not AI Ready ;
- la liste des informations obligatoires manquantes ;
- un aperçu des catégories incluses dans le contexte IA ;
- la liste des catégories explicitement exclues ;
- l’état du consentement utilisateur ;
- un mécanisme d’activation explicite ;
- un mécanisme de désactivation.

---

## Principes fondamentaux

### Principe 1 : source de vérité structurée

Le profil structuré enregistré dans l’application constitue la seule source de vérité transmise à l’intelligence artificielle.

Les CV servent à enrichir le profil.

Les CV ne sont pas directement transmis à l’intelligence artificielle.

### Principe 2 : données validées uniquement

Seules les informations présentes dans les données métier validées du profil peuvent être incluses dans le contexte IA.

Les propositions d’enrichissement avec le statut PENDING ne doivent jamais être incluses.

Les valeurs extraites d’un CV mais non acceptées par l’utilisateur ne doivent jamais être incluses.

### Principe 3 : transparence

L’utilisateur doit pouvoir comprendre :

- quelles catégories de données seront incluses ;
- quelles catégories ne seront pas incluses ;
- quelles informations obligatoires sont manquantes ;
- si le consentement a été accordé ;
- si une fonctionnalité IA est autorisée à effectuer un appel.

### Principe 4 : consentement explicite

Aucun appel à une fonctionnalité IA nécessitant la transmission de données ne doit être autorisé tant que le consentement n’a pas été explicitement accordé.

La simple consultation d’un profil ne constitue pas un consentement.

La présence d’un profil AI Ready ne constitue pas un consentement.

### Principe 5 : révocabilité

L’utilisateur doit pouvoir retirer le consentement.

Après révocation, aucun nouvel appel IA ne doit être autorisé.

### Principe 6 : séparation des responsabilités

Le backend est responsable :

- du calcul de l’état AI Ready ;
- de la construction du contexte IA ;
- de la validation du consentement ;
- de l’application des règles d’exclusion ;
- de la persistance des paramètres IA.

Le frontend est responsable :

- de l’affichage de l’état ;
- de l’affichage des catégories de données ;
- de l’affichage des informations manquantes ;
- de la demande de consentement ;
- de l’envoi du choix utilisateur au backend.

Le frontend ne doit pas être la seule protection empêchant un appel IA sans consentement.

---

## Distinction entre les concepts

### Profile Completeness

Profile Completeness évalue la complétude générale d’un profil.

Cette mesure peut inclure des éléments qui ne sont pas obligatoires pour le contexte IA, par exemple :

- la présence d’un CV ;
- les certifications ;
- les pays préférés ;
- les objectifs de carrière ;
- d’autres informations générales.

Profile Completeness est actuellement une visualisation calculée dans le frontend.

Profile Completeness ne doit pas être utilisé comme autorisation d’appel IA.

### AI Readiness

AI Readiness détermine si les informations minimales obligatoires pour construire un contexte IA fiable sont présentes.

AI Readiness est une règle distincte de Profile Completeness.

Un profil peut avoir un bon score de complétude mais ne pas être AI Ready.

Un profil peut être AI Ready sans avoir de certification.

### AI Consent

AI Consent représente le choix explicite de l’utilisateur autorisant l’utilisation des données validées du profil par les fonctionnalités IA.

Le consentement est distinct de la disponibilité des données.

### Autorisation finale

Un appel IA est autorisé uniquement lorsque :

AI Ready
AND
AI Consent Accepted
AND
AI Features Enabled

Si l’une de ces conditions est fausse, aucun appel à un fournisseur IA ne doit être réalisé.

---

## AI Readiness

### Mode retenu

STRICT

### Règle générale

Un profil est AI Ready uniquement si toutes les données obligatoires sont disponibles.

### Données obligatoires

Le profil doit posséder :

- un Current Title renseigné ;
- au moins une Hard Skill validée ;
- au moins une Work Experience validée ;
- au moins une Language validée ;
- tous les champs Additional Profile Context obligatoires.

### Additional Profile Context obligatoire

En mode strict, les cinq champs suivants doivent être renseignés :

- Professional Summary ;
- Career Motivations ;
- Preferred Environment ;
- Non-Negotiables ;
- Additional Context.

Une valeur constituée uniquement d’espaces est considérée comme absente.

### Données non bloquantes

Les éléments suivants sont inclus dans le contexte lorsqu’ils existent, mais leur absence ne bloque pas AI Readiness :

- Full Name ;
- Location ;
- Years of Experience ;
- Short-Term Target Role ;
- Long-Term Target Role ;
- Remote Preference ;
- Preferred Countries ;
- Soft Skills ;
- Certifications.

### CV non obligatoire

La présence d’un CV n’est pas une condition AI Readiness.

Le profil structuré est la source de vérité.

Un profil peut donc être AI Ready sans CV si les informations structurées obligatoires sont présentes.

### Applications non prises en compte

Les candidatures ne participent pas au calcul AI Readiness.

Les candidatures ne font pas partie du contrat IA de cette phase.

### Historique des opportunités non pris en compte

L’historique des opportunités analysées ne participe pas au calcul AI Readiness.

Il n’est pas inclus dans le contexte IA de cette phase.

---

## Informations manquantes

Lorsque le profil n’est pas AI Ready, le système doit retourner une liste explicite des éléments manquants.

Valeurs fonctionnelles recommandées :

- Current title is missing
- At least one hard skill is required
- At least one work experience is required
- At least one language is required
- Professional summary is missing
- Career motivations are missing
- Preferred environment is missing
- Non-negotiables are missing
- Additional context is missing

Le système ne doit pas retourner uniquement un booléen sans explication.

---

## Données incluses dans l’aperçu

L’aperçu doit présenter les catégories prévues dans le contrat IA.

### Profile Identity

Données possibles :

- Current Title ;
- Location ;
- Years of Experience.

Le Full Name peut rester visible dans le profil, mais il ne doit pas être considéré comme nécessaire au raisonnement d’un fournisseur IA.

La phase d’implémentation doit appliquer le principe de minimisation et ne transmettre le Full Name que si un besoin fonctionnel explicite est démontré.

Pour le premier contrat MVP, la recommandation est de ne pas transmettre le Full Name au fournisseur IA.

### Career Goals

Données possibles :

- Short-Term Target Role ;
- Long-Term Target Role ;
- Remote Preference ;
- Preferred Countries.

### Hard Skills

Données possibles :

- nom de la compétence ;
- nombre d’années d’expérience ;
- niveau d’auto-évaluation.

Seules les compétences associées au profil structuré sont utilisées.

### Soft Skills

Données possibles :

- nom de la soft skill.

Les Soft Skills sont incluses lorsqu’elles existent.

Leur absence ne bloque pas AI Readiness.

### Languages

Données possibles :

- nom de la langue ;
- niveau de maîtrise.

Seules les langues associées au profil structuré sont utilisées.

### Certifications

Données possibles :

- nom de la certification ;
- organisme émetteur ;
- date d’obtention ;
- date d’expiration.

Le Credential ID ne doit pas être transmis par défaut.

Le Credential ID n’est pas nécessaire aux fonctionnalités de conseil ou d’analyse de compatibilité.

### Work Experiences

Données possibles :

- Company Name ;
- Job Title ;
- Start Date ;
- End Date ;
- Current Position ;
- Description.

Les identifiants techniques de base de données ne doivent pas être transmis au fournisseur IA.

### Additional Profile Context

Données incluses :

- Professional Summary ;
- Career Motivations ;
- Preferred Environment ;
- Non-Negotiables ;
- Additional Context.

---

## Données explicitement exclues

Les données suivantes ne doivent jamais être incluses dans le contexte IA de cette phase :

- fichier CV ;
- texte brut du CV ;
- aperçu du texte extrait du CV ;
- chemin de stockage du CV ;
- nom technique du fichier stocké ;
- contenu binaire du CV ;
- proposition d’enrichissement en attente ;
- proposition d’enrichissement rejetée ;
- valeur observée non validée ;
- historique complet des propositions d’enrichissement ;
- candidatures ;
- notes de candidatures ;
- chronologie des candidatures ;
- historique des opportunités ;
- historique de navigation ;
- mots de passe ;
- JWT ;
- refresh tokens ;
- tokens OAuth ;
- clés API ;
- chaînes de connexion ;
- variables d’environnement ;
- logs techniques ;
- stack traces ;
- données internes non nécessaires ;
- identifiants techniques sans valeur métier.

---

## AI Context Preview

### Emplacement retenu

L’aperçu est intégré dans Profile Detail.

Aucune nouvelle page n’est créée pour le MVP.

### Justification

Profile Detail contient déjà les informations structurées utilisées pour construire le contexte IA :

- informations générales ;
- objectifs de carrière ;
- contexte additionnel ;
- Hard Skills ;
- Soft Skills ;
- expériences ;
- langues ;
- certifications ;
- informations de complétude.

L’intégration dans Profile Detail évite :

- une duplication des informations ;
- un nouveau parcours de navigation ;
- une nouvelle page à maintenir ;
- une rupture avec le workflow de gestion du profil.

### Nouvelle section

Nom recommandé :

AI Context Readiness

### Position recommandée

La carte doit être placée après :

Profile Completeness
Missing Information
Recommended Actions

et avant :

General Information

Ordre cible :

Profile Header
Profile KPIs
Profile Completeness
Missing Information
Recommended Actions
AI Context Readiness
General Information
Additional Profile Context
Applications
CVs
Skills
Work Experiences
Languages
Certifications

### Raison du placement

L’utilisateur doit d’abord comprendre la qualité générale du profil.

L’utilisateur peut ensuite comprendre si le profil est suffisamment renseigné pour les fonctionnalités IA.

La carte AI Context Readiness ne doit pas dominer la page.

---

## Contenu de la carte AI Context Readiness

### État AI Ready

Afficher :

AI Ready

Message recommandé :

This profile contains the required validated information for AI features.

### État Not AI Ready

Afficher :

Not AI Ready

Message recommandé :

Complete the missing profile information before using AI features.

### Liste des informations manquantes

Lorsque le profil n’est pas prêt, afficher la liste retournée par le backend.

Exemple :

Missing required information:

- At least one language is required
- Career motivations are missing
- Non-negotiables are missing

### Catégories incluses

Afficher les catégories du contexte IA :

Information available to AI:

- Profile information
- Career goals
- Hard skills
- Soft skills
- Languages
- Certifications
- Work experiences
- Additional profile context

Une catégorie optionnelle absente peut être marquée comme :

Not provided

Elle ne doit pas être présentée comme transmise si elle ne contient aucune donnée.

### Catégories exclues

Afficher un message de transparence :

Not shared with AI:

- Raw CV files
- Unvalidated CV enrichment proposals
- Applications and application history
- Technical secrets and credentials

### État du consentement

Afficher l’un des états suivants :

AI consent: Accepted

ou :

AI consent: Not accepted

ou :

AI features: Disabled

---

## Niveau de détail de l’aperçu

### Décision MVP

La carte affiche :

- l’état AI Ready ;
- les éléments obligatoires manquants ;
- les catégories incluses ;
- les catégories exclues ;
- l’état du consentement.

La carte ne duplique pas l’intégralité des valeurs du profil.

Les valeurs détaillées restent visibles dans les sections existantes de Profile Detail.

### Raison

Afficher une copie complète de toutes les expériences, compétences et descriptions dans la carte créerait :

- une duplication importante ;
- une page plus longue ;
- un risque de divergence d’affichage ;
- une maintenance inutile.

Le composant d’aperçu doit expliquer le périmètre du contexte IA.

Il ne remplace pas les sections du profil.

---

## Consentement utilisateur

### Modèle retenu

Consentement unique et révocable.

### Portée

Le consentement est global pour le compte utilisateur MVP.

Il ne dépend pas d’un profil particulier.

Il s’applique à toutes les fonctionnalités IA utilisant le contrat validé.

### Première activation

Lors de la première activation de l’option Allow AI Features, le frontend doit afficher une confirmation explicite.

Titre recommandé :

Enable AI Features

Message recommandé :

AI features will use validated information from your structured profiles.

Raw CV files and unvalidated CV enrichment proposals will not be shared.

You can disable AI features at any time.

Actions :

Cancel
Enable AI Features

### Consentement explicite

Le consentement est accepté uniquement si l’utilisateur sélectionne explicitement :

Enable AI Features

Fermer la fenêtre ne constitue pas une acceptation.

Naviguer vers une autre page ne constitue pas une acceptation.

### Révocation

L’utilisateur peut désactiver :

Allow AI Features

La désactivation doit :

- empêcher tout nouvel appel IA ;
- conserver le fonctionnement déterministe du produit ;
- ne pas supprimer les données du profil ;
- ne pas modifier les scores ;
- ne pas modifier le matching ;
- ne pas modifier les opportunités ;
- ne pas modifier les candidatures.

### Nouvelle activation après révocation

Après une révocation, une nouvelle activation doit demander à nouveau un consentement explicite.

---

## Persistance du consentement

### Domaine retenu

Settings.

### Stockage retenu

Table existante :

application_settings

### Nouvelle table

Aucune nouvelle table.

### Raison

Le domaine Settings persiste déjà des paramètres métier sous forme de clé et de valeur.

Le consentement global au niveau du compte MVP est compatible avec cette architecture.

### Clés recommandées

ai_features_enabled
ai_consent_accepted

### Valeurs

Les valeurs sont persistées sous forme de chaînes conformément au modèle ApplicationSetting existant.

Valeurs attendues :

true
false

### Valeurs par défaut

ai_features_enabled = false
ai_consent_accepted = false

Le système doit privilégier le refus par défaut.

L’absence d’une clé doit être interprétée comme false.

### Cohérence des deux clés

État actif valide :

ai_features_enabled = true
ai_consent_accepted = true

État désactivé valide :

ai_features_enabled = false
ai_consent_accepted = false

L’implémentation ne doit pas autoriser :

ai_features_enabled = true
ai_consent_accepted = false

Si cet état est rencontré, les fonctionnalités IA doivent être considérées comme désactivées.

---

## Contrat Settings cible

### Schéma de réponse conceptuel

{
"ai_features_enabled": false,
"ai_consent_accepted": false
}

### Schéma de mise à jour conceptuel

{
"ai_features_enabled": true,
"ai_consent_accepted": true
}

### Endpoint recommandé

GET /settings/ai

Objectif :

- récupérer l’état d’activation ;
- récupérer l’état du consentement.

### Endpoint de mise à jour recommandé

PUT /settings/ai

Objectif :

- activer les fonctionnalités IA avec consentement ;
- désactiver les fonctionnalités IA ;
- révoquer le consentement.

### Comportement attendu

Activation valide :

{
"ai_features_enabled": true,
"ai_consent_accepted": true
}

Désactivation valide :

{
"ai_features_enabled": false,
"ai_consent_accepted": false
}

Activation invalide :

{
"ai_features_enabled": true,
"ai_consent_accepted": false
}

Résultat recommandé :

HTTP 422

Le message doit indiquer que le consentement est obligatoire pour activer les fonctionnalités IA.

---

## Contrat AI Readiness cible

### Responsabilité

Le calcul final AI Readiness doit appartenir au backend.

### Raison

AI Readiness contrôle l’autorisation d’utiliser des fonctionnalités IA.

Cette règle ne doit pas résider uniquement dans React.

Le frontend peut afficher le résultat, mais ne doit pas constituer la seule source de décision.

### Endpoint recommandé

GET /profiles/{profile_id}/ai-context-preview

### Objectif

Retourner :

- l’état AI Ready ;
- les informations obligatoires manquantes ;
- les catégories disponibles ;
- les catégories non fournies ;
- les catégories exclues ;
- l’état du consentement ;
- l’état d’activation des fonctionnalités IA.

### Réponse conceptuelle

{
"profile_id": 2108,
"is_ai_ready": true,
"missing_required_information": [],
"available_categories": [
"PROFILE_INFORMATION",
"CAREER_GOALS",
"HARD_SKILLS",
"SOFT_SKILLS",
"LANGUAGES",
"CERTIFICATIONS",
"WORK_EXPERIENCES",
"ADDITIONAL_PROFILE_CONTEXT"
],
"missing_optional_categories": [],
"excluded_categories": [
"RAW_CV",
"UNVALIDATED_ENRICHMENT",
"APPLICATION_HISTORY",
"TECHNICAL_SECRETS"
],
"ai_features_enabled": true,
"ai_consent_accepted": true,
"ai_call_allowed": true
}

### Exemple non prêt

{
"profile_id": 2108,
"is_ai_ready": false,
"missing_required_information": [
"At least one language is required",
"Career motivations are missing"
],
"available_categories": [
"PROFILE_INFORMATION",
"CAREER_GOALS",
"HARD_SKILLS",
"WORK_EXPERIENCES"
],
"missing_optional_categories": [
"SOFT_SKILLS",
"CERTIFICATIONS"
],
"excluded_categories": [
"RAW_CV",
"UNVALIDATED_ENRICHMENT",
"APPLICATION_HISTORY",
"TECHNICAL_SECRETS"
],
"ai_features_enabled": true,
"ai_consent_accepted": true,
"ai_call_allowed": false
}

### Règle ai_call_allowed

ai_call_allowed =
is_ai_ready
AND
ai_features_enabled
AND
ai_consent_accepted

Le backend doit calculer cette valeur.

---

## Construction du contexte IA

### Décision

L’endpoint de preview ne doit pas appeler un fournisseur IA.

Il ne doit pas générer de prompt.

Il ne doit pas créer d’explication IA.

Il doit uniquement :

- charger les données validées du profil ;
- évaluer AI Readiness ;
- identifier les catégories disponibles ;
- identifier les catégories absentes ;
- appliquer les exclusions ;
- lire l’état des paramètres IA ;
- retourner un aperçu.

### Contexte détaillé

Le payload détaillé destiné au futur fournisseur n’a pas besoin d’être retourné intégralement au frontend pendant cette phase.

Le frontend dispose déjà des informations du profil dans les sections existantes.

### Données provenant du CV

Aucune donnée n’est récupérée directement depuis :

- la table CV ;
- le fichier stocké ;
- le texte brut extrait ;
- les propositions d’enrichissement.

Les informations initialement issues d’un CV peuvent être utilisées uniquement lorsqu’elles ont été validées et intégrées dans le profil structuré.

---

## Architecture backend cible

### Composant recommandé

Créer un service dédié au contexte IA.

Nom recommandé :

AIContextService

### Responsabilités

AIContextService est responsable de :

- charger ou recevoir les données structurées nécessaires ;
- calculer AI Readiness ;
- construire l’aperçu du contexte ;
- appliquer les règles d’exclusion ;
- déterminer si un appel IA est autorisé.

### Responsabilités interdites

AIContextService ne doit pas :

- appeler un fournisseur IA ;
- construire un prompt ;
- modifier le profil ;
- accepter automatiquement une proposition d’enrichissement ;
- lire le contenu brut d’un CV ;
- calculer un score de matching ;
- modifier le consentement sans action utilisateur.

### Relation avec AIExplanationService

AIExplanationService reste responsable de l’explication d’un résultat déterministe.

AIContextService est responsable de la préparation et de la validation du contexte profil.

Les deux services restent séparés.

### Relation avec SettingsService

SettingsService reste responsable de la persistance des paramètres :

- ai_features_enabled ;
- ai_consent_accepted.

AIContextService peut lire ces paramètres pour déterminer :

ai_call_allowed

---

## Architecture frontend cible

### ProfileDetail

Ajouter une nouvelle carte :

AI Context Readiness

Le composant ProfileDetail ne doit pas recalculer seul la readiness finale.

ProfileDetail affiche le résultat retourné par le backend.

### ProfilesPage

ProfilesPage doit :

- charger le preview pour le profil sélectionné ;
- gérer l’état de chargement ;
- gérer l’état d’erreur ;
- transmettre le résultat à ProfileDetail ;
- recharger le preview après une modification du profil.

### SettingsPage

Ajouter une section :

AI Features

Contenu :

- Allow AI Features ;
- état actuel ;
- texte de transparence ;
- action d’activation ;
- action de désactivation.

### Client API frontend

Ajouter les contrats et fonctions permettant :

- de récupérer les paramètres IA ;
- de modifier les paramètres IA ;
- de récupérer AI Context Preview pour un profil.

---

## Fichiers backend potentiellement impactés

### Fichiers à modifier

backend/app/settings/schemas.py
backend/app/settings/service.py
backend/app/settings/router.py

### Fichiers potentiellement créés

Décision recommandée :

backend/app/ai/context_schemas.py
backend/app/ai/context_service.py

Alternative acceptable :

backend/app/ai/schemas.py
backend/app/ai/services.py

La création de fichiers séparés est recommandée afin de ne pas mélanger :

- AI Explanation ;
- AI Profile Context ;
- AI Readiness ;
- AI Consent.

### Router possible

L’endpoint de preview peut être placé dans un nouveau router IA :

backend/app/ai/router.py

ou dans le router Profile.

Recommandation :

backend/app/ai/router.py

avec la route :

GET /profiles/{profile_id}/ai-context-preview

Raison :

- la ressource évaluée est un profil ;
- la responsabilité métier appartient au domaine AI Context ;
- la route reste compréhensible pour le frontend.

### Intégration application

Si un nouveau router est créé, le routeur principal FastAPI devra l’enregistrer.

Le fichier exact doit être confirmé avant implémentation.

---

## Fichiers frontend potentiellement impactés

### Fichiers à modifier

frontend/src/services/api.ts
frontend/src/pages/ProfilesPage.tsx
frontend/src/components/ProfileDetail.tsx
frontend/src/pages/SettingsPage.tsx

### Fichier recommandé à créer

frontend/src/components/AIContextReadinessCard.tsx

### Fichier recommandé pour le consentement

frontend/src/components/AIConsentDialog.tsx

### Responsabilité de AIContextReadinessCard

Afficher uniquement :

- état readiness ;
- informations manquantes ;
- catégories disponibles ;
- catégories optionnelles absentes ;
- catégories exclues ;
- état du consentement ;
- état d’activation.

### Responsabilité de AIConsentDialog

Afficher :

- les informations utilisées ;
- les données exclues ;
- le caractère révocable du consentement ;
- les boutons Cancel et Enable AI Features.

Le composant ne doit pas persister directement les données sans passer par le client API.

---

## Scénarios utilisateur

### Scénario 1 : profil complet, IA désactivée

Conditions :

- profil AI Ready ;
- ai_features_enabled = false ;
- ai_consent_accepted = false.

Affichage attendu :

AI Ready
AI consent: Not accepted
AI features: Disabled

L’utilisateur peut aller dans Settings pour activer les fonctionnalités IA.

### Scénario 2 : profil incomplet, IA désactivée

Conditions :

- profil Not AI Ready ;
- IA désactivée.

Affichage attendu :

Not AI Ready

La liste des informations manquantes est visible.

L’utilisateur peut compléter le profil.

### Scénario 3 : première activation

Conditions :

- l’utilisateur active Allow AI Features ;
- aucun consentement n’a encore été accepté.

Comportement attendu :

- ouverture du dialogue de consentement ;
- affichage des catégories incluses ;
- affichage des catégories exclues ;
- confirmation explicite requise.

### Scénario 4 : consentement annulé

Action :

- l’utilisateur ferme le dialogue ;
- ou sélectionne Cancel.

Résultat :

ai_features_enabled = false
ai_consent_accepted = false

Aucun appel IA n’est autorisé.

### Scénario 5 : consentement accepté

Action :

- l’utilisateur sélectionne Enable AI Features.

Résultat :

ai_features_enabled = true
ai_consent_accepted = true

Si le profil est AI Ready :

ai_call_allowed = true

### Scénario 6 : IA activée, profil non prêt

Conditions :

- consentement accepté ;
- fonctionnalités IA activées ;
- profil incomplet.

Résultat :

ai_call_allowed = false

Le système affiche les informations manquantes.

### Scénario 7 : révocation

Action :

- l’utilisateur désactive Allow AI Features.

Résultat :

ai_features_enabled = false
ai_consent_accepted = false
ai_call_allowed = false

### Scénario 8 : profil modifié après consentement

Conditions :

- le consentement est déjà accepté ;
- une donnée obligatoire est supprimée.

Résultat :

- le consentement reste un choix global ;
- le profil devient Not AI Ready ;
- aucun nouvel appel IA pour ce profil n’est autorisé ;
- les informations manquantes sont affichées.

### Scénario 9 : second profil

Conditions :

- consentement global accepté ;
- profil A AI Ready ;
- profil B Not AI Ready.

Résultat :

Profil A:
ai_call_allowed = true

Profil B:
ai_call_allowed = false

Le consentement est global.

La readiness reste calculée indépendamment pour chaque profil.

---

## Gestion des erreurs

### Erreur de chargement du preview

Message frontend recommandé :

Unable to load AI context readiness.

Le système ne doit pas considérer le profil comme AI Ready en cas d’erreur.

### Erreur de chargement des paramètres

Message frontend recommandé :

Unable to load AI settings.

Les fonctionnalités IA doivent être considérées comme désactivées jusqu’à obtention d’un état valide.

### Erreur de sauvegarde du consentement

Message frontend recommandé :

Unable to update AI settings.

Le frontend ne doit pas afficher le consentement comme accepté tant que le backend n’a pas confirmé la persistance.

### Profil introuvable

Résultat recommandé :

HTTP 404
Profile not found.

### État de consentement incohérent

Si :

ai_features_enabled = true
ai_consent_accepted = false

le backend doit retourner :

ai_call_allowed = false

---

## Sécurité et confidentialité

### Minimisation

Seules les données nécessaires au cas d’usage doivent être utilisées.

### Secret by default

Les données techniques sont exclues par défaut.

### Refus par défaut

En cas d’absence de paramètre :

AI Features Disabled
Consent Not Accepted

### Pas de prompt dans les logs

Ne jamais journaliser :

- le contexte complet ;
- le prompt complet ;
- les descriptions complètes des expériences ;
- le contexte additionnel complet ;
- des secrets ;
- des tokens.

### Journalisation autorisée

Informations possibles :

- profile_id ;
- is_ai_ready ;
- ai_features_enabled ;
- ai_consent_accepted ;
- ai_call_allowed ;
- nombre de catégories disponibles ;
- type d’erreur ;
- timestamp.

### Données personnelles

Le Full Name n’est pas nécessaire dans le premier payload transmis à un fournisseur IA.

Le Full Name peut rester visible dans l’interface Profile Detail.

---

## Tests backend attendus

### Settings

Tester :

- récupération des paramètres IA par défaut ;
- activation avec consentement ;
- désactivation ;
- refus d’une activation sans consentement ;
- persistance des paramètres ;
- interprétation false en cas de clé absente.

### AI Readiness

Tester :

- profil complet considéré AI Ready ;
- profil sans Current Title non prêt ;
- profil sans Hard Skill non prêt ;
- profil sans Work Experience non prêt ;
- profil sans Language non prêt ;
- profil sans Professional Summary non prêt ;
- profil sans Career Motivations non prêt ;
- profil sans Preferred Environment non prêt ;
- profil sans Non-Negotiables non prêt ;
- profil sans Additional Context non prêt ;
- absence de Soft Skills non bloquante ;
- absence de Certification non bloquante ;
- absence de CV non bloquante.

### AI Context Preview

Tester :

- catégories disponibles correctes ;
- catégories optionnelles absentes correctes ;
- catégories exclues toujours présentes ;
- aucune donnée CV brute retournée ;
- aucune proposition d’enrichissement en attente retournée ;
- aucune candidature retournée ;
- aucun secret retourné.

### Autorisation

Tester :

ready + enabled + consent
= allowed

Tester :

not ready + enabled + consent
= not allowed

Tester :

ready + disabled + consent
= not allowed

Tester :

ready + enabled + no consent
= not allowed

---

## Tests frontend attendus

Si aucun framework de test frontend n’est disponible, une validation fonctionnelle manuelle est obligatoire.

Scénarios à valider :

- carte AI Context Readiness visible ;
- état AI Ready visible ;
- état Not AI Ready visible ;
- informations manquantes visibles ;
- catégories incluses visibles ;
- catégories exclues visibles ;
- consentement non accepté visible ;
- activation ouvre le dialogue ;
- Cancel ne sauvegarde rien ;
- Enable sauvegarde le consentement ;
- désactivation révoque le consentement ;
- erreur backend gérée ;
- changement de profil recharge la readiness ;
- modification du profil recharge la readiness ;
- absence de certification non bloquante ;
- absence de soft skills non bloquante ;
- absence de CV non bloquante.

---

## Validation technique attendue

### Backend

Validation réalisée depuis le dossier backend :

python -m compileall app tests
pytest tests\ai\ -q
pytest tests\test_ai_settings.py -q
pytest -q

Résultats :

- compilation validée ;
- import de l’application FastAPI validé ;
- 59 tests AI passants ;
- 8 tests AI Settings passants ;
- 304 tests backend passants ;
- git diff --check validé.

### Frontend

Depuis le dossier frontend :

npm run build

### Qualité Git

Depuis la racine :

git diff --check
git status

### État d’implémentation

#### Backend

Statut :

Completed

Implémenté :

- AISettingsResponse ;
- AISettingsUpdate ;
- GET /settings/ai ;
- PUT /settings/ai ;
- persistance ai_features_enabled ;
- persistance ai_consent_accepted ;
- validation de cohérence du consentement ;
- AIContextPreviewResponse ;
- AIContextService ;
- calcul STRICT de AI Readiness ;
- calcul de ai_call_allowed ;
- GET /profiles/{profile_id}/ai-context-preview ;
- catégories disponibles ;
- catégories optionnelles absentes ;
- catégories exclues ;
- gestion HTTP 404 pour un profil inconnu ;
- enregistrement du router dans FastAPI.

Fichiers backend créés :

- backend/app/ai/context_schemas.py
- backend/app/ai/context_service.py
- backend/app/ai/router.py

Fichiers backend modifiés :

- backend/app/main.py
- backend/app/settings/schemas.py
- backend/app/settings/service.py
- backend/app/settings/router.py

Tests créés :

- backend/tests/ai/test_ai_context_router.py
- backend/tests/ai/test_ai_context_service.py
- backend/tests/test_ai_settings.py

Validation :

- 8 tests AI Context Router passants ;
- 14 tests AI Context Service passants ;
- 8 tests AI Settings passants ;
- 59 tests AI passants ;
- 304 tests backend passants ;
- aucune régression détectée.

Commit technique :

2cc84d3 - feat(ai): add AI context preview, readiness and consent backend

#### Frontend

Statut :

Pending

Éléments restant à implémenter :

- contrats API frontend ;
- fonctions GET /settings/ai et PUT /settings/ai ;
- fonction GET AI Context Preview ;
- AIConsentDialog ;
- section AI Features dans SettingsPage ;
- AIContextReadinessCard ;
- intégration dans ProfileDetail ;
- chargement depuis ProfilesPage ;
- gestion des erreurs ;
- rechargement après modification du profil ;
- build frontend ;
- validation fonctionnelle.

---

## Critères de fin

La phase est terminée uniquement lorsque :

- AI Context Preview est défini ;
- le mode AI Readiness STRICT est implémenté ;
- AI Readiness est calculé par le backend ;
- les informations obligatoires manquantes sont retournées ;
- le consentement est explicite ;
- le consentement est révocable ;
- les fonctionnalités IA sont désactivées par défaut ;
- les paramètres sont persistés via ApplicationSetting ;
- aucune nouvelle table n’est créée ;
- le preview est visible dans Profile Detail ;
- les paramètres IA sont visibles dans Settings ;
- le contenu brut des CV est exclu ;
- les enrichissements non validés sont exclus ;
- les candidatures sont exclues ;
- les tests backend passent ;
- le build frontend passe ;
- la validation fonctionnelle est réalisée ;
- la documentation est synchronisée ;
- le commit technique est réalisé ;
- le commit documentaire est réalisé ;
- Git est propre.

---

## Hors périmètre

Cette phase n’inclut pas :

- OpenAIProvider ;
- AzureOpenAIProvider ;
- appel réel à un modèle IA ;
- calcul IA d’un score ;
- modification IA d’un score ;
- modification automatique du profil ;
- ingestion directe d’un CV par un modèle IA ;
- consentement par profil ;
- consentement à chaque appel ;
- historique de consentement ;
- version juridique du consentement ;
- stockage des prompts ;
- stockage des réponses IA ;
- chat IA ;
- streaming ;
- embeddings ;
- RAG ;
- agents ;
- analyse des candidatures ;
- analyse de l’historique des opportunités ;
- personnalisation du consentement par catégorie de données.

---

## Décisions

### DEC-AIC-001

AI Context Preview est intégré dans Profile Detail.

### DEC-AIC-002

Aucune nouvelle page dédiée n’est créée dans le MVP.

### DEC-AIC-003

AI Readiness utilise le mode STRICT.

### DEC-AIC-004

AI Readiness est distinct de Profile Completeness.

### DEC-AIC-005

AI Readiness est calculé par le backend.

### DEC-AIC-006

Le consentement est unique, global et révocable.

### DEC-AIC-007

Le consentement n’est pas demandé à chaque appel IA.

### DEC-AIC-008

Le consentement est persisté via le domaine Settings existant.

### DEC-AIC-009

Aucune nouvelle table n’est créée.

### DEC-AIC-010

Les fonctionnalités IA sont désactivées par défaut.

### DEC-AIC-011

Le fichier CV et son texte brut sont exclus.

### DEC-AIC-012

Les propositions d’enrichissement non validées sont exclues.

### DEC-AIC-013

Les candidatures et leur historique sont exclus du contrat MVP.

### DEC-AIC-014

Les certifications et les Soft Skills sont optionnelles pour AI Readiness.

### DEC-AIC-015

La présence d’un CV n’est pas obligatoire pour AI Readiness.

### DEC-AIC-016

Un appel IA nécessite simultanément :

AI Ready
AI Features Enabled
AI Consent Accepted

### DEC-AIC-017

La carte d’aperçu ne déclenche aucun appel IA.

### DEC-AIC-018

Le Full Name n’est pas transmis au fournisseur IA dans le contrat MVP recommandé.

---

## Fichiers envisagés

### Backend à modifier

backend/app/settings/schemas.py
backend/app/settings/service.py
backend/app/settings/router.py
backend/app/main.py ou fichier d’enregistrement des routers

### Backend à créer

backend/app/ai/context_schemas.py
backend/app/ai/context_service.py
backend/app/ai/router.py

### Tests backend à modifier ou créer

backend/tests/test_ai_settings.py
backend/tests/ai/test_ai_context_service.py
backend/tests/ai/test_ai_context_router.py

Les noms exacts doivent être confirmés contre le repository avant implémentation.

### Frontend à modifier

frontend/src/services/api.ts
frontend/src/pages/ProfilesPage.tsx
frontend/src/components/ProfileDetail.tsx
frontend/src/pages/SettingsPage.tsx

### Frontend à créer

frontend/src/components/AIContextReadinessCard.tsx
frontend/src/components/AIConsentDialog.tsx

---

## Séquence d’implémentation recommandée

1. Confirmer les fichiers backend réels
2. Ajouter les schémas Settings IA
3. Ajouter la persistance Settings IA
4. Ajouter les endpoints Settings IA
5. Ajouter les schémas AI Context Preview
6. Ajouter AIContextService
7. Ajouter l’endpoint de preview
8. Ajouter les tests backend
9. Exécuter la suite backend
10. Ajouter les types et fonctions API frontend
11. Ajouter AIConsentDialog
12. Ajouter la section AI Features dans Settings
13. Ajouter AIContextReadinessCard
14. Intégrer la carte dans ProfileDetail
15. Recharger le preview après modification du profil
16. Exécuter le build frontend
17. Réaliser la validation fonctionnelle
18. Réaliser l’audit de cohérence
19. Créer le commit technique
20. Mettre à jour la documentation
21. Créer le commit documentaire
22. Vérifier que Git est propre

---

### Prochaine étape recommandée

Phase :

7.1.23.12 Frontend Implementation

Objectif :

- auditer les fichiers frontend réels ;
- ajouter les contrats API AI Settings ;
- ajouter les contrats API AI Context Preview ;
- créer AIConsentDialog ;
- intégrer AI Features dans SettingsPage ;
- créer AIContextReadinessCard ;
- intégrer la carte dans ProfileDetail ;
- charger le preview depuis ProfilesPage ;
- valider le build frontend ;
- réaliser la validation fonctionnelle.

Le backend est terminé et ne doit plus être modifié sans anomalie démontrée.
