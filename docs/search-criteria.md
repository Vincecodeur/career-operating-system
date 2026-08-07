# Search Criteria

## Objectif

Définir les critères de recherche d'opportunités professionnelles du MVP.

Ce document fixe :

- les critères géographiques ;
- les critères de poste ;
- les critères de contrat ;
- les critères de télétravail ;
- les critères de salaire ;
- les mots-clés positifs ;
- les mots-clés exclus ;
- les règles de fraîcheur ;
- les règles de qualité ;
- le rattachement des critères aux profils candidats.

Ce document ne décrit pas encore l'implémentation technique.

Il prépare les futures phases :

- Offer Normalization ;
- First External Source ;
- Multi Source Support ;
- Scheduled Synchronization ;
- Opportunity Analysis ;
- Matching V2.

---

CONTEXTE

Career Operating System est un système d'intelligence carrière.

Le Job Discovery doit permettre d'identifier des opportunités pertinentes avant analyse, scoring et ranking.

Les Search Criteria servent à filtrer ou qualifier les offres collectées avant leur analyse par les moteurs métier.

Les critères de recherche ne remplacent pas le Matching Engine.

Ils servent à limiter le bruit et à mieux orienter la collecte.

---

DÉCISIONS VALIDÉES

MARCHÉ MVP

Pays :

- France

Zone géographique principale :

- Paris

Rayon accepté :

- Paris + 10 km

Hors périmètre MVP :

- France entière
- Europe
- Remote international
- autres pays

---

FONCTION CIBLE

Fonction principale ciblée :

- Integration Architect

Famille métier associée :

- Partnerships
- Technical Partnerships
- Partner Integrations
- Ecosystem Integrations
- Partner Solutions

---

TITRES RECHERCHÉS

Titres prioritaires :

- Integration Architect
- Partner Integration Manager
- Technical Partnerships Manager
- Strategic Partnerships Manager
- Partner Solutions Architect
- Partner Success Manager
- Technology Partnerships Manager
- Channel Partnerships Manager
- Alliance Manager
- Ecosystem Manager

Ces titres servent de base à la phase Search Criteria.

Ils pourront évoluer dans les futures phases si les résultats sont trop larges ou trop restrictifs.

---

TYPE DE CONTRAT

Contrat accepté au MVP :

- CDI

Contrats hors périmètre MVP :

- CDD
- Freelance
- Stage
- Alternance
- Temps partiel
- Volontariat

Les offres ne correspondant pas au contrat CDI doivent être exclues ou fortement pénalisées selon la future stratégie d'implémentation.

---

WORK MODE

Valeurs normalisées :

- Remote
- Hybrid
- Onsite

Modes acceptés au MVP :

- Remote
- Hybrid
- Onsite

Préférence métier :

- Hybrid

Règle MVP :

Les offres Remote, Hybrid et Onsite restent acceptées.

Cependant, Hybrid est considéré comme le mode préféré pour le profil cible.

Cette préférence devra être utilisée plus tard dans :

- le scoring ;
- le ranking ;
- l'analyse d'opportunité.

---

SALAIRE

Salaire minimum souhaité :

- 70 000 € brut annuel

Règle importante :

Une offre sans salaire reste éligible.

Aucune offre ne doit être automatiquement exclue uniquement parce que le salaire n'est pas renseigné.

Une offre sans salaire pourra recevoir un malus lors d'une phase d'analyse ultérieure.

---

LANGUES ACCEPTÉES

Langues acceptées :

- Français
- Anglais

Priorité :

- priorité égale entre français et anglais

Règle MVP :

Les offres rédigées en français ou en anglais sont acceptées.

Aucune préférence de langue n'est appliquée au MVP.

---

MOTS-CLÉS POSITIFS

Mots-clés principaux :

- Integration
- Architect
- API
- Ecommerce

Ces mots-clés sont considérés comme des signaux positifs.

Ils peuvent apparaître dans :

- le titre ;
- la description ;
- les responsabilités ;
- les compétences demandées ;
- les technologies ;
- le contexte d'intégration.

---

MOTS-CLÉS À EXCLURE

Mots-clés d'exclusion :

- Stage
- Intern
- Freelance

Une offre contenant ces termes doit être exclue ou fortement pénalisée.

Raison :

Ces termes ne correspondent pas au périmètre MVP défini :

- CDI ;
- rôle senior ;
- poste professionnel permanent.

---

SÉNIORITÉ

Niveau ciblé :

- Senior

Hors périmètre MVP :

- Junior
- Entry Level
- Intern
- Graduate
- Apprentice

Les niveaux Lead, Director ou VP ne sont pas exclus par principe, mais ils ne sont pas le coeur du MVP.

---

ENTREPRISES

Stratégie MVP :

- toutes les entreprises sont acceptées.

Il n'y a pas de liste prioritaire.

Il n'y a pas de liste d'exclusion.

Les entreprises pourront être scorées plus tard selon :

- secteur ;
- taille ;
- maturité produit ;
- stack technique ;
- pertinence carrière.

---

FRAÎCHEUR DES OFFRES

Durée maximale de fraîcheur :

- 7 jours

Règle MVP :

Une offre publiée il y a plus de 7 jours peut être conservée en base, mais elle n'est plus considérée comme fraîche.

Les offres plus anciennes pourront être :

- archivées ;
- conservées pour historique ;
- exclues des recommandations prioritaires.

---

QUALITÉ DES OFFRES

Décision MVP :

- conserver toutes les offres puis scorer leur qualité.

Le système ne doit pas rejeter automatiquement une offre incomplète si les champs obligatoires minimum sont disponibles.

Les offres doivent ensuite pouvoir être comparées selon leur niveau de complétude.

---

CHAMPS OBLIGATOIRES

Une offre doit idéalement contenir :

- titre ;
- ville ;
- pays ;
- description ;
- URL source ;
- date de publication ;
- type de contrat.

Si un champ obligatoire manque, l'offre pourra être marquée comme incomplète.

La stratégie d'exclusion précise sera définie lors de la phase Offer Normalization.

---

CHAMPS SOUHAITÉS

Champs souhaités :

- entreprise ;
- télétravail ;
- salaire ;
- séniorité ;
- technologies ;
- compétences.

Ces champs améliorent la qualité de l'analyse mais ne sont pas strictement obligatoires au MVP.

---

CRITÈRES PRINCIPAUX DE PERTINENCE

Critères prioritaires :

1. Localisation
2. Description complète
3. Titre du poste

Ces critères doivent être pris en compte avant les critères secondaires.

---

PRIORITÉ DE FILTRAGE

Priorité recommandée :

1. Exclure les offres hors contrat
2. Exclure les offres hors localisation
3. Exclure les offres clairement hors rôle
4. Qualifier les offres selon les mots-clés positifs
5. Qualifier la fraîcheur
6. Qualifier la complétude
7. Laisser le Matching Engine évaluer la pertinence finale

---

RELATION AVEC LES PROFILS

Décision validée :

Les Search Criteria sont rattachés à chaque Profile.

Raison :

Le système supporte plusieurs profils candidats.

Chaque profil peut avoir :

- ses propres titres ciblés ;
- ses propres critères géographiques ;
- ses propres préférences de contrat ;
- ses propres critères de séniorité ;
- ses propres mots-clés positifs ;
- ses propres mots-clés exclus.

Cette approche est cohérente avec la philosophie multi-profils du projet.

---

EXEMPLE DE SEARCH CRITERIA MVP

Nom :

Integration Architect - Paris

Profile :

Profil cible Integration Architect

Pays :

France

Localisation :

Paris + 10 km

Contrat :

CDI

Work mode accepté :

Remote
Hybrid
Onsite

Work mode préféré :

Hybrid

Salaire minimum souhaité :

70 000 € brut annuel

Langues :

Français
Anglais

Titres ciblés :

Integration Architect
Partner Integration Manager
Technical Partnerships Manager
Partner Solutions Architect
Technology Partnerships Manager

Mots-clés positifs :

Integration
Architect
API
Ecommerce

Mots-clés exclus :

Stage
Intern
Freelance

Fraîcheur :

7 jours

Stratégie qualité :

Conserver toutes les offres puis scorer leur qualité.

---

HORS PÉRIMÈTRE

Cette phase ne traite pas :

- l'implémentation du modèle de données ;
- les endpoints API ;
- les formulaires frontend ;
- la collecte réelle d'offres ;
- la normalisation ;
- le scraping ;
- le matching ;
- le ranking ;
- l'analyse d'opportunité.

Ces sujets appartiennent aux phases suivantes.

---

CRITÈRES DE SUCCÈS

La phase Search Criteria sera considérée comme terminée lorsque :

- les critères géographiques seront définis ;
- les mots-clés positifs seront définis ;
- les mots-clés exclus seront définis ;
- le type de contrat cible sera défini ;
- le work mode sera défini ;
- le salaire minimum souhaité sera défini ;
- la fraîcheur des offres sera définie ;
- la relation Profile → Search Criteria sera définie ;
- les règles de filtrage MVP seront documentées.

---

PROCHAINE PHASE

5.9.3 Offer Normalization

Objectif :

Définir comment transformer les offres collectées depuis différentes sources en un format interne commun.

La normalisation devra tenir compte :

- des champs obligatoires ;
- des champs souhaités ;
- des sources ;
- de la fraîcheur ;
- de la qualité des données ;
- de la déduplication ;
- des critères de recherche définis dans ce document.
