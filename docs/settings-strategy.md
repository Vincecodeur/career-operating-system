# Settings Strategy — Per-User Migration (7.1.25)

## Contexte

DEC-081 (User Data Ownership And Isolation) a établi l'isolation des
données par utilisateur pour Profile et toutes ses entités dépendantes
(CV, Skills, Applications, etc.). L'audit de 7.1.25.1 a révélé que
`ApplicationSetting`, le domaine Settings dans son ensemble, restait
100% partagé entre tous les comptes utilisateurs — y compris le
consentement AI (ai_consent_accepted), ce qui contredit directement
DEC-078 (consentement explicite requis par personne).

## Décision retenue : Option B — Abandon du pattern EAV

Plutôt que d'ajouter un simple `user_id` à la table EAV existante
(`application_settings`, clé/valeur générique), le pattern est
entièrement réécrit vers des tables typées, une ligne par domaine par
utilisateur. Ce choix est motivé par la volonté de propreté à long
terme plutôt que par la rapidité d'implémentation.

## Nouveau schéma

### Table `user_settings` (remplace `application_settings`)

Une ligne par utilisateur, contenant tous les domaines de préférences
(Job Discovery, Search Criteria, Discovery Preferences, AI Settings).

```
id                                  PK
user_id                             FK users.id, UNIQUE, NOT NULL, indexed

discovery_enabled                   Boolean, default False
discovery_interval_minutes          Integer, default 1440
discovery_connectors                ARRAY(String), default []

search_target_job_titles            ARRAY(String), default []
search_preferred_countries          ARRAY(String), default []
search_work_modes                   ARRAY(String), default []
search_included_keywords            ARRAY(String), default []
search_excluded_keywords            ARRAY(String), default []

discovery_age_window                String, default '30_DAYS'
discovery_minimum_matching_score    Integer, default 25
discovery_show_archived             Boolean, default False
discovery_default_sort              String, default 'BEST_MATCH_FIRST'

ai_features_enabled                 Boolean, default False
ai_consent_accepted                 Boolean, default False

created_at
updated_at
```

### Table `saved_searches` (remplace le JSON blob dans `application_settings`)

Relation 1-N réelle vers `users`, plus de sérialisation JSON, plus de
limite de troncature à 2000 caractères.

```
id                    PK
user_id               FK users.id, NOT NULL, indexed
name                  String
keyword               String
application_status    String
source                String
location              String
sort_by               String
created_at
updated_at
```

### Suppression

`application_settings` (table EAV) est supprimée en fin de migration,
une fois la nouvelle table alimentée et validée.

## Décision — Profile.preferred_countries reste distinct de search_preferred_countries

Ces deux champs ne sont PAS fusionnés. Profile.preferred_countries est
une préférence déclarée par profil candidat (cohérent avec DEC-071
Multi Profile Opportunity Context, qui autorise plusieurs profils actifs
simultanément avec des préférences potentiellement différentes).
search_preferred_countries est un filtre de recherche actif à l'échelle
du compte, utilisé par le pipeline Job Discovery. Aucun mapping 1:1
cohérent n'existe entre les deux quand plusieurs profils sont actifs.

## Ordre d'implémentation

Le schéma est conçu et migré en une seule passe (une seule migration de
table, cohérent avec le choix de l'Option B). L'ordre de correction des
routers et de leurs tests suit toutefois une priorité :

1. AI Settings en premier (seul point contredisant une décision produit
   déjà actée, DEC-078)
2. Job Discovery Settings
3. Search Criteria Settings
4. Discovery Preferences Settings
5. Saved Searches

## Migration des données existantes

Une seule ligne de settings existe actuellement en base réelle (configurée
manuellement par Vincent via l'interface). Elle sera migrée vers
maw282003@gmail.com, suivant le même principe que la migration des 10
profils orphelins réalisée en 7.1.24.3.7 : aucune perte de données,
attribution au compte principal plutôt que suppression.

Un audit préalable (7.1.25.1) a confirmé 0 saved search existante en
base réelle : aucun risque de troncature JSON, migration simple sans
donnée à préserver sur ce point précis.

## Fichiers backend à créer

```
backend/app/settings/models.py          — réécrit (UserSettings, SavedSearch)
backend/app/settings/schemas.py         — réécrit (mêmes contrats API,
                                           donc aucun changement requis
                                           côté frontend pour les types)
backend/app/settings/service.py         — réécrit (accès direct aux colonnes
                                           typées, plus de get_value/set_value
                                           générique)
backend/app/settings/router.py          — modifié (ajout de
                                           get_current_user partout)
```

## Fichiers backend à modifier (dépendances)

```
backend/app/ai/context_service.py       — AIContextService doit recevoir
                                           user_id pour filtrer
                                           get_ai_settings()
backend/app/ai/router.py                — propager current_user.id vers
                                           AIContextService
```

## Fichiers de test à créer/modifier

```
backend/tests/test_settings.py          — à créer si inexistant, ou
                                           réécrire entièrement (ancien
                                           test probablement basé sur
                                           application_settings)
backend/tests/test_saved_searches.py    — à réécrire (nouvelle table
                                           dédiée au lieu du JSON blob)
backend/tests/ai/test_ai_context_service.py — à vérifier (dépend
                                           potentiellement de
                                           reset_ai_settings via
                                           SettingsService)
backend/tests/ai/test_ai_context_router.py  — à vérifier (idem)
backend/tests/conftest.py               — vérifier si une fixture
                                           applique déjà un reset AI
                                           settings global à adapter
```

## Fichiers frontend à modifier

```
frontend/src/services/api.ts            — ajout du header Authorization
                                           sur tous les appels Settings
                                           et Saved Searches (actuellement
                                           publics, à l'exception de
                                           getAISettings/updateAISettings
                                           qui restent aussi à corriger)
```

Aucun changement de type TypeScript n'est requis si les contrats
Pydantic (schemas.py) restent identiques en sortie — seule la source de
données change côté backend.

## Commandes de migration de données à exécuter

Avant toute suppression de `application_settings`, un script Python de
migration devra :
1. Lire la ligne unique existante via l'ancien SettingsService
2. Créer une ligne UserSettings pour maw282003@gmail.com avec ces valeurs
3. Vérifier que get_saved_searches() retourne bien une liste vide
   (déjà confirmé lors de l'audit 7.1.25.1)
