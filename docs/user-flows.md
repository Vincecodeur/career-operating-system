# User Flows

## Phase

5.7.3 User Flows

## Objectif

Décrire précisément les parcours utilisateurs du Career Operating System avant la phase Wireframes et avant toute évolution majeure du frontend.

Ce document définit :

- les parcours principaux ;
- les pages traversées ;
- les actions utilisateur ;
- les résultats attendus ;
- les cas alternatifs ;
- les règles fonctionnelles à respecter.

Le frontend ne doit pas calculer de logique métier.

Le backend reste responsable :

- du matching ;
- du scoring ;
- du ranking ;
- de l'analyse des opportunités ;
- des règles de filtrage métier.

---

## Vue d'ensemble des parcours MVP

Les parcours MVP couvrent le flux produit suivant :

Profile
↓
Search Criteria
↓
Job Discovery
↓
Opportunity Analysis
↓
Opportunity Ranking
↓
Decision Support
↓
Application Tracker

Les parcours principaux sont :

- UF-01 - Onboarding du premier profil
- UF-02 - Gestion d'un profil existant
- UF-03 - Gestion multi-profils
- UF-04 - Configuration des critères de recherche
- UF-05 - Collecte des opportunités
- UF-06 - Exploration des opportunités
- UF-07 - Analyse détaillée d'une opportunité
- UF-08 - Ouverture du lien source
- UF-09 - Conversion d'une opportunité en candidature
- UF-10 - Suivi manuel d'une candidature
- UF-11 - Archivage d'une opportunité
- UF-12 - Gestion des offres sans salaire
- UF-13 - Gestion des offres expirées
- UF-14 - Gestion des erreurs de source
- UF-15 - Consultation du Dashboard

---

# UF-01 - Onboarding du premier profil

## Objectif

Permettre à l'utilisateur de créer son premier profil candidat structuré.

Le profil structuré devient la source de vérité du système.

## Point de départ

L'utilisateur arrive dans l'application sans profil candidat existant.

## Pages traversées

Dashboard
↓
Profile
↓
Create Profile
↓
Profile Details

## Flux principal

1. L'utilisateur ouvre l'application.
2. Le Dashboard détecte qu'aucun profil candidat n'existe.
3. Le Dashboard affiche une action principale : Create first profile.
4. L'utilisateur clique sur Create first profile.
5. L'utilisateur arrive sur la page Profile.
6. L'utilisateur saisit les informations principales :
   - nom du profil ;
   - titre professionnel actuel ;
   - résumé professionnel ;
   - postes ciblés ;
   - pays ou régions cibles ;
   - work mode souhaité ;
   - salaire cible ;
   - type de contrat.
7. L'utilisateur ajoute ses compétences.
8. L'utilisateur ajoute ses expériences professionnelles.
9. L'utilisateur ajoute ses langues.
10. L'utilisateur ajoute ses certifications.
11. L'utilisateur peut ajouter un CV.
12. L'utilisateur peut ajouter une analyse externe, par exemple une analyse Copilot.
13. L'utilisateur sauvegarde le profil.

## Résultat attendu

Le profil est créé, sauvegardé et utilisé comme source de vérité pour les futures analyses.

## Cas alternatifs

### Profil incomplet

Si le profil ne contient pas les informations minimales nécessaires :

- le système sauvegarde le brouillon ;
- le système indique les champs à compléter ;
- le profil ne doit pas être utilisé pour un scoring complet tant que les données critiques sont absentes.

### CV non ajouté

Si aucun CV n'est ajouté :

- le profil reste valide ;
- le CV pourra être ajouté plus tard ;
- l'utilisateur peut continuer avec les données structurées saisies manuellement.

## Règles

- Le profil structuré est la source de vérité.
- Le CV est une source d'enrichissement.
- Une analyse Copilot est une source d'enrichissement.
- Les scores futurs doivent s'appuyer sur le profil structuré, pas directement sur le CV brut.

---

# UF-02 - Gestion d'un profil existant

## Objectif

Permettre à l'utilisateur de modifier ou enrichir un profil candidat existant.

## Point de départ

L'utilisateur possède au moins un profil candidat.

## Pages traversées

Dashboard
↓
Profile
↓
Profile Details

## Flux principal

1. L'utilisateur ouvre le Dashboard.
2. L'utilisateur accède à Profile.
3. Le système affiche la liste ou le sélecteur de profils.
4. L'utilisateur sélectionne un profil.
5. Le système affiche les informations du profil.
6. L'utilisateur modifie ou enrichit le profil.
7. L'utilisateur sauvegarde les changements.

## Actions possibles

- Modifier le titre professionnel.
- Modifier le résumé.
- Ajouter une compétence.
- Modifier une compétence.
- Supprimer une compétence.
- Ajouter une expérience.
- Modifier une expérience.
- Ajouter une langue.
- Modifier une langue.
- Ajouter une certification.
- Ajouter une analyse externe.
- Ajouter ou remplacer un CV.
- Modifier les préférences de poste.

## Résultat attendu

Le profil est mis à jour et les futures analyses utiliseront la nouvelle version du profil.

## Cas alternatifs

### Erreur de sauvegarde

Si la sauvegarde échoue :

- le système affiche une erreur claire ;
- les données saisies ne doivent pas être perdues côté interface ;
- l'utilisateur peut réessayer.

### Donnée supprimée par erreur

Le MVP ne nécessite pas forcément un historique complet des modifications.

Recommandation future :

- prévoir un historique de profil ;
- permettre de comparer l'évolution du profil dans le temps.

---

# UF-03 - Gestion multi-profils

## Objectif

Permettre à l'utilisateur de gérer plusieurs trajectoires professionnelles.

## Exemples de profils

- Profil actuel
- Profil Product Manager
- Profil Solution Architect
- Profil Head of Partnerships
- Profil Partnerships Leadership

## Pages traversées

Profile
↓
Create Profile
↓
Profile Details

## Flux principal

1. L'utilisateur ouvre la page Profile.
2. L'utilisateur clique sur Create Profile.
3. L'utilisateur choisit un nom de profil.
4. L'utilisateur configure les informations de ce profil.
5. L'utilisateur sauvegarde.
6. Le profil devient disponible dans le sélecteur de profils.

## Résultat attendu

Chaque profil peut être utilisé séparément pour analyser une opportunité.

## Exemple d'utilisation

Une même offre peut avoir :

- un score faible pour le profil actuel ;
- un score élevé pour un profil cible Solution Architect ;
- un score moyen pour un profil Product Manager.

## Règles

- Les profils ne doivent pas être mélangés.
- Les critères de recherche peuvent être globaux ou liés à un profil.
- Les analyses doivent toujours indiquer quel profil a été utilisé.

---

# UF-04 - Configuration des critères de recherche

## Objectif

Permettre à l'utilisateur de définir les critères utilisés pour collecter, filtrer et scorer les opportunités.

## Pages traversées

Dashboard
↓
Search Criteria
↓
Search Criteria Details

## Flux principal

1. L'utilisateur ouvre Search Criteria.
2. L'utilisateur sélectionne le profil concerné.
3. L'utilisateur définit les titres recherchés.
4. L'utilisateur définit les pays ou régions.
5. L'utilisateur définit le work mode souhaité.
6. L'utilisateur définit le salaire minimum.
7. L'utilisateur définit les types de contrat.
8. L'utilisateur définit les langues.
9. L'utilisateur ajoute des mots-clés inclus.
10. L'utilisateur ajoute des mots-clés exclus.
11. L'utilisateur active ou désactive les sources.
12. L'utilisateur sauvegarde les critères.

## Critères MVP

- Titres recherchés
- Pays
- Régions
- Work Mode
  - Remote
  - Hybrid
  - Onsite
- Salaire minimum
- Types de contrat
- Langues
- Mots-clés inclus
- Mots-clés exclus
- Sources activées

## Résultat attendu

Les critères sont sauvegardés et utilisés pour :

- la collecte ;
- le filtrage ;
- le scoring ;
- l'affichage des opportunités.

## Cas alternatifs

### Aucun critère défini

Si aucun critère n'est défini :

- le système ne doit pas lancer de collecte automatique ;
- le système doit demander à l'utilisateur de configurer au moins un critère minimal.

### Critères trop restrictifs

Si les critères retournent très peu ou aucune offre :

- le système affiche un message d'information ;
- le système peut suggérer d'élargir certains critères.

## Règles

- Les critères de recherche ne remplacent pas le profil.
- Le profil décrit le candidat.
- Les critères décrivent ce que l'utilisateur recherche.
- Le scoring doit tenir compte des deux.

---

# UF-05 - Collecte des opportunités

## Objectif

Récupérer des offres depuis plusieurs sources externes.

## Déclencheurs possibles

- Synchronisation manuelle depuis l'application.
- Collecte quotidienne planifiée plus tard.
- Script ou tâche planifiée après le MVP.

## Pages traversées

Settings ou Search Criteria
↓
Job Discovery Process
↓
Opportunities

## Flux principal

1. L'utilisateur déclenche une synchronisation.
2. Le système lit les critères de recherche.
3. Le système identifie les sources activées.
4. Le système interroge les sources disponibles.
5. Le système récupère les offres.
6. Le système normalise les données.
7. Le système stocke les offres.
8. Le système conserve le lien source.
9. Le système affiche les nouvelles opportunités dans Opportunities.

## Sources possibles

- API officielle
- Flux public exploitable
- Scraping si aucune API exploitable n'existe
- Import manuel si nécessaire

## Résultat attendu

Les offres collectées sont stockées dans le système et disponibles dans la page Opportunities.

## Cas alternatifs

### Source indisponible

Si une source est indisponible :

- l'erreur est enregistrée ;
- les autres sources continuent ;
- l'utilisateur voit que la source a échoué.

### Aucune offre trouvée

Si aucune offre n'est trouvée :

- le système affiche un message clair ;
- les critères restent sauvegardés ;
- l'utilisateur peut ajuster ses critères.

### Offre déjà existante

Si l'offre existe déjà :

- le système évite le doublon ;
- le système peut mettre à jour les données si nécessaire.

## Règles

- API first.
- Scraping uniquement si aucune API exploitable n'existe.
- Aucune méthode agressive ou non maintenable ne doit être introduite.
- Chaque offre doit conserver son lien source.
- LinkedIn fait partie des sources visées par le MVP, mais la méthode technique reste à définir.

---

# UF-06 - Exploration des opportunités

## Objectif

Permettre à l'utilisateur de consulter les offres collectées.

## Pages traversées

Dashboard
↓
Opportunities
↓
Opportunity Details

## Flux principal

1. L'utilisateur ouvre Opportunities.
2. Le système affiche la liste des offres collectées.
3. Chaque offre affiche les informations principales.
4. L'utilisateur applique des filtres.
5. L'utilisateur trie les offres.
6. L'utilisateur ouvre une opportunité.

## Informations affichées dans la liste

- Titre du poste
- Entreprise
- Localisation
- Work Mode
- Source
- Score
- Niveau de pertinence
- Date de collecte
- Statut
- Salaire si disponible
- Indicateur sans salaire si applicable
- Indicateur archivé si applicable

## Filtres MVP

- Toutes les opportunités
- Opportunités pertinentes
- Opportunités intéressantes
- Opportunités non intéressantes
- Opportunités archivées
- Opportunités sans salaire
- Source
- Work Mode
- Pays
- Score minimum

## Résultat attendu

L'utilisateur identifie rapidement les opportunités à analyser en priorité.

## Règles

- La liste affiche les scores calculés par le backend.
- La liste ne calcule aucun score côté frontend.
- Les filtres d'affichage ne modifient pas les données métier.

---

# UF-07 - Analyse détaillée d'une opportunité

## Objectif

Expliquer pourquoi une opportunité est pertinente ou non.

## Pages traversées

Opportunities
↓
Opportunity Details

## Flux principal

1. L'utilisateur clique sur une opportunité.
2. Le système affiche le détail de l'offre.
3. Le système affiche le score global.
4. Le système affiche les points forts.
5. Le système affiche les points faibles.
6. Le système affiche les compétences correspondantes.
7. Le système affiche les compétences manquantes.
8. Le système affiche les éventuels malus.
9. L'utilisateur décide de l'action suivante.

## Informations affichées

- Titre de l'offre
- Entreprise
- Source
- Lien source
- Description
- Localisation
- Work Mode
- Salaire
- Langue
- Date de publication
- Date de collecte
- Score global
- Niveau de pertinence
- Points forts
- Points faibles
- Compétences correspondantes
- Compétences manquantes
- Malus éventuels
- Statut de l'offre

## Actions possibles

- Open Job Offer
- Mark as Interesting
- Mark as Not Interesting
- Archive
- Convert to Application

## Résultat attendu

L'utilisateur comprend clairement pourquoi une offre mérite ou non son attention.

## Règles

- Aucun score opaque.
- Chaque score doit être explicable.
- Les points forts et points faibles doivent être compréhensibles.
- Les malus doivent être affichés.
- Le backend produit l'analyse.
- Le frontend affiche l'analyse.

---

# UF-08 - Ouvrir le lien source de l'offre

## Objectif

Permettre à l'utilisateur d'accéder à l'offre originale pour postuler sur le site externe.

## Pages traversées

Opportunity Details
↓
External Job Board

## Flux principal

1. L'utilisateur consulte une opportunité.
2. L'utilisateur clique sur Open Job Offer.
3. Le système ouvre le lien source.
4. L'utilisateur consulte ou postule sur le site externe.

## Résultat attendu

L'utilisateur reste maître de la candidature.

## Règles

- Le système ne postule pas automatiquement.
- Le système n'envoie pas automatiquement de CV.
- Le système conserve uniquement le lien source.
- L'utilisateur décide de postuler ou non.

---

# UF-09 - Conversion d'une opportunité en candidature

## Objectif

Créer une candidature suivie à partir d'une opportunité intéressante.

## Pages traversées

Opportunity Details
↓
Convert to Application
↓
Applications

## Flux principal

1. L'utilisateur analyse une opportunité.
2. L'utilisateur décide de postuler.
3. L'utilisateur ouvre le lien source.
4. L'utilisateur postule sur le site externe.
5. L'utilisateur revient dans l'application.
6. L'utilisateur clique sur Convert to Application.
7. Le système crée une candidature liée à l'offre.
8. Le système affiche la candidature dans Applications.

## Statut initial recommandé

Applied

ou

Not Applied si l'utilisateur veut suivre une offre avant postulation.

## Résultat attendu

L'opportunité devient une candidature suivie.

## Cas alternatifs

### L'utilisateur n'a pas encore postulé

Le système peut créer une candidature au statut Not Applied.

### L'opportunité est déjà liée à une candidature

Le système ne doit pas créer de doublon.

## Règles

- Une candidature est liée à un profil.
- Une candidature est liée à une offre.
- Le suivi reste manuel.
- Aucune synchronisation automatique avec un job board n'est prévue dans le MVP.

---

# UF-10 - Suivi manuel d'une candidature

## Objectif

Permettre à l'utilisateur de suivre le cycle de vie d'une candidature.

## Pages traversées

Dashboard
↓
Applications
↓
Application Details

## Flux principal

1. L'utilisateur ouvre Applications.
2. Le système affiche les candidatures.
3. L'utilisateur sélectionne une candidature.
4. L'utilisateur modifie son statut.
5. Le système sauvegarde le statut.
6. Le Dashboard reflète la mise à jour.

## Statuts MVP

- Not Applied
- Applied
- Interview
- Offer
- Rejected
- Accepted

## Informations affichées

- Titre de l'offre
- Entreprise
- Profil associé
- Statut
- Date de création
- Dernière mise à jour
- Lien source
- Score initial si disponible

## Résultat attendu

L'utilisateur suit manuellement l'avancement de ses candidatures.

## Règles

- Le système ne déduit pas automatiquement le statut.
- L'utilisateur met à jour le statut manuellement.
- Le statut doit rester simple dans le MVP.

---

# UF-11 - Archivage d'une opportunité

## Objectif

Permettre à l'utilisateur de retirer une opportunité de la vue active tout en la conservant.

## Pages traversées

Opportunities
↓
Opportunity Details
↓
Archive

## Flux principal

1. L'utilisateur consulte une opportunité.
2. L'utilisateur décide qu'elle n'est pas pertinente.
3. L'utilisateur clique sur Archive.
4. Le système archive l'opportunité.
5. L'opportunité disparaît de la vue active.
6. L'opportunité reste disponible dans les filtres archivés.

## Résultat attendu

La liste active reste propre sans supprimer les données utiles.

## Règles

- Une offre archivée est conservée.
- Une offre archivée peut servir aux analyses marché futures.
- L'utilisateur peut afficher ou masquer les offres archivées.

---

# UF-12 - Gestion des offres sans salaire

## Objectif

Traiter les offres sans information salariale sans les exclure automatiquement.

## Flux principal

1. Une offre est collectée sans salaire.
2. Le système stocke l'offre.
3. Le système applique un indicateur "salary not provided".
4. Le scoring peut appliquer un malus.
5. Le malus est affiché dans l'analyse.

## Résultat attendu

L'offre reste éligible mais son manque d'information salariale est visible.

## Règles

- Une offre sans salaire n'est pas exclue.
- Un malus peut être appliqué.
- Le malus doit être explicite.
- L'utilisateur doit comprendre l'impact du salaire manquant.

---

# UF-13 - Gestion des offres expirées

## Objectif

Conserver les offres expirées tout en les retirant de la vue active.

## Flux principal

1. Le système détecte ou reçoit une information d'expiration.
2. L'offre est marquée comme expired.
3. L'offre est archivée.
4. L'offre reste disponible pour historique et analyse.

## Résultat attendu

Les offres expirées ne polluent pas la vue active mais restent exploitables.

## Règles

- Les offres expirées sont conservées.
- Les offres expirées sont archivées.
- Les offres expirées peuvent être utilisées pour l'analyse marché.
- L'utilisateur peut filtrer les offres expirées.

---

# UF-14 - Gestion des erreurs de source

## Objectif

Gérer les erreurs lors de la collecte d'offres.

## Cas possibles

- API indisponible
- Identifiants invalides
- Format de réponse inattendu
- Scraping cassé
- Source désactivée
- Limite d'appel atteinte

## Flux principal

1. Le système tente de collecter les offres.
2. Une source échoue.
3. L'erreur est enregistrée.
4. Les autres sources continuent.
5. L'utilisateur voit un statut d'erreur sur la source.

## Résultat attendu

Une erreur sur une source ne bloque pas tout le système.

## Règles

- Une source en erreur ne bloque pas les autres sources.
- L'erreur doit être visible.
- Le système ne doit pas inventer de données.
- Les données incomplètes doivent être signalées.

---

# UF-15 - Consultation du Dashboard

## Objectif

Donner une vue synthétique de la situation carrière.

## Pages traversées

Dashboard

## Contenu affiché

- Nombre total d'opportunités collectées
- Nombre d'opportunités pertinentes
- Nombre d'opportunités à analyser
- Nombre de candidatures en cours
- Meilleures opportunités
- Dernières opportunités collectées
- Actions recommandées
- Alertes éventuelles

## Actions possibles

- Aller vers Profile
- Aller vers Search Criteria
- Aller vers Opportunities
- Ouvrir une opportunité
- Aller vers Applications
- Lancer une synchronisation manuelle si disponible

## Résultat attendu

L'utilisateur comprend rapidement :

- la situation actuelle ;
- les meilleures opportunités ;
- les actions à traiter ;
- les candidatures en cours.

## Règles

- Le Dashboard synthétise.
- Le Dashboard ne remplace pas les pages métier.
- Le Dashboard ne calcule pas de logique métier.
- Les données affichées proviennent du backend.

---

# Règles transverses

## Règle 1 - Source de vérité

Le profil structuré enregistré dans l'application constitue la source de vérité.

Les autres sources servent uniquement à enrichir ce profil.

## Règle 2 - Décision utilisateur

Le système recommande.

L'utilisateur décide.

Aucune candidature automatique n'est réalisée.

## Règle 3 - Explicabilité

Tout score doit être explicable.

Le système doit afficher :

- les critères utilisés ;
- les points forts ;
- les points faibles ;
- les compétences correspondantes ;
- les compétences manquantes ;
- les malus éventuels.

## Règle 4 - Backend responsable de la logique métier

Le backend est responsable :

- du matching ;
- du scoring ;
- du ranking ;
- de l'analyse des offres ;
- des règles de filtrage métier.

Le frontend affiche les résultats.

## Règle 5 - Conservation des opportunités

Les opportunités collectées doivent conserver :

- leur source ;
- leur lien d'origine ;
- leur date de collecte ;
- leur statut ;
- leur statut d'archivage.

## Règle 6 - API First

La collecte des offres suit l'ordre de priorité suivant :

1. API officielle
2. Flux public exploitable
3. Scraping si aucune API exploitable n'existe

## Règle 7 - LinkedIn dans le MVP

LinkedIn fait partie des sources visées par le MVP.

La méthode technique sera définie pendant la phase Job Discovery.

Aucune hypothèse technique spécifique n'est retenue dans ce document.

---

# Pages concernées par les flux

## Pages MVP

- Dashboard
- Profile
- Search Criteria
- Opportunities
- Opportunity Details
- Applications
- Settings

## Pages futures

- Job Sources
- Market Intelligence
- Career Roadmap
- Interview Preparation
- Application Assistant

---

# Sortie attendue de la phase 5.7.3

La phase 5.7.3 est terminée lorsque :

- les parcours principaux sont documentés ;
- les parcours alternatifs sont documentés ;
- les règles transverses sont documentées ;
- les pages traversées sont identifiées ;
- les flux sont suffisamment clairs pour préparer l'inventaire détaillé des pages.

---

# Prochaine étape

Après validation de ce document :

Phase 5.7.4 - Page Inventory

Objectif :

Définir précisément chaque page de l'application :

- nom de la page ;
- rôle ;
- contenu ;
- composants ;
- actions ;
- données backend nécessaires ;
- statut MVP ou futur.
