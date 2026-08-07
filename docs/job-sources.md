# Job Sources

## Objectif

Définir les sources d'opportunités professionnelles du MVP afin de préparer les futures phases Job Discovery.

Ce document fixe :

- les sources autorisées ;
- la stratégie de collecte ;
- les données obligatoires ;
- les règles de déduplication ;
- le périmètre MVP ;
- les priorités de collecte.

Aucune implémentation technique n'est décidée dans ce document.

---

CONTEXTE

Career Operating System est un système d'intelligence carrière.

Le Job Discovery n'est pas un simple agrégateur d'offres.

Son objectif est de :

- identifier les meilleures opportunités ;
- comparer les opportunités ;
- alimenter le moteur de matching ;
- alimenter le système de ranking ;
- faciliter la prise de décision.

Les offres collectées constituent une matière première pour les futures analyses.

---

DÉCISIONS VALIDÉES

MARCHÉ MVP

Pays couvert :

- France

Les futures extensions internationales sont hors périmètre MVP.

---

FONCTION CIBLE MVP

Fonction principale recherchée :

- Integration Architect

Titres actuellement ciblés :

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

Le système devra rester extensible à d'autres familles de postes.

---

CONTRATS MVP

Types de contrats acceptés :

- CDI

Hors périmètre MVP :

- CDD
- Freelance
- Stage
- Alternance
- Temps partiel

---

WORK MODE MVP

Valeurs normalisées :

- Remote
- Hybrid
- Onsite

Préférence MVP :

- Hybrid

Cette normalisation devra être réutilisée dans :

- Search Criteria ;
- filtrage ;
- matching ;
- ranking ;
- analyses futures.

---

STRATÉGIE DE COLLECTE

APPROCHE GÉNÉRALE

Décision :

API First

Principes :

- privilégier les APIs officielles ;
- privilégier les sources documentées ;
- privilégier les intégrations stables ;
- éviter le scraping lorsque des APIs exploitables existent.

Le scraping n'est autorisé que lorsqu'aucune API réaliste et exploitable n'existe.

---

CAS PARTICULIER LINKEDIN

Décision :

API First

Exception validée :

Si aucune API réaliste et exploitable n'est disponible pour le MVP, un scraping limité pourra être utilisé.

Cette exception est actuellement limitée à LinkedIn.

---

FRÉQUENCE CIBLE

Fréquence retenue :

- Quotidienne

Objectifs :

- disposer d'opportunités fraîches ;
- limiter les appels inutiles ;
- maintenir une architecture simple.

---

SOURCES MVP

SOURCE 1

LinkedIn

Rôle :

- source principale du MVP.

Motivations :

- forte présence des offres ciblées ;
- couverture importante du marché français ;
- qualité généralement élevée des annonces ;
- adoption massive par les recruteurs.

Priorité :

Critique

---

SOURCE 2

France Travail

Rôle :

- source complémentaire du MVP.

Motivations :

- source institutionnelle ;
- volume important d'offres ;
- couverture de sociétés moins visibles sur LinkedIn ;
- complément pertinent pour le marché français.

Priorité :

Haute

---

SOURCE PRIORITY MATRIX

Priority 1

- LinkedIn

Priority 2

- France Travail

Priority 3

- Sources futures hors MVP

---

SOURCES EXPLICITEMENT HORS PÉRIMÈTRE MVP

Les sources suivantes ne sont pas prioritaires pour la première version :

- Indeed
- Glassdoor
- Welcome To The Jungle
- Greenhouse
- Lever
- Workday
- Ashby
- SmartRecruiters
- Sites carrières individuels

Ces sources pourront être étudiées ultérieurement.

---

MODÈLE MINIMAL D'OFFRE

CHAMPS OBLIGATOIRES

Une offre ne peut pas être exploitée sans :

- titre ;
- ville ;
- pays ;
- description ;
- URL source ;
- date de publication ;
- type de contrat.

---

CHAMPS SOUHAITÉS

Ces informations améliorent la qualité du matching mais ne sont pas obligatoires :

- entreprise ;
- télétravail ;
- salaire ;
- séniorité ;
- technologies ;
- compétences.

---

CHAMPS FUTURS

Non requis au MVP :

- avantages ;
- taille de l'entreprise ;
- note employeur ;
- informations financières ;
- informations ESG ;
- diversité et inclusion ;
- données RH avancées.

---

QUALITÉ DES OFFRES

Le système doit privilégier les offres :

- récentes ;
- complètes ;
- exploitables pour le matching.

Une offre incomplète reste acceptable si les champs obligatoires sont présents.

---

RÈGLE SALAIRE

Les offres sans salaire restent exploitables.

Aucune exclusion automatique liée à l'absence de salaire n'est prévue.

Une offre sans salaire pourra recevoir un malus lors des futures phases d'analyse mais reste éligible.

---

DÉDUPLICATION

DÉCISION RETENUE

Conserver la version la plus complète.

---

JUSTIFICATION

Cette stratégie :

- reste simple ;
- évite les règles de fusion complexes ;
- préserve la meilleure qualité de données ;
- convient au MVP.

---

EXEMPLE

Même offre détectée :

Source A

- titre ;
- description courte.

Source B

- titre ;
- description complète ;
- salaire ;
- télétravail.

Résultat :

Conserver Source B.

---

CRITÈRES DE SUCCÈS

La phase Job Sources sera considérée comme terminée lorsque :

- les sources MVP seront figées ;
- les champs obligatoires seront validés ;
- les règles de déduplication seront validées ;
- la stratégie API First sera documentée ;
- la stratégie LinkedIn sera documentée ;
- la stratégie de collecte quotidienne sera documentée.

---

HORS PÉRIMÈTRE

Cette phase ne traite pas :

- l'implémentation technique ;
- les APIs ;
- le scraping détaillé ;
- le stockage ;
- la normalisation ;
- le matching ;
- le ranking ;
- l'analyse d'opportunités.

Ces sujets appartiennent aux phases suivantes.

---

SORTIE ATTENDUE DES FUTURES PHASES

Les futures phases Job Discovery devront produire :

- une liste normalisée d'offres ;
- une source identifiable ;
- une date de collecte ;
- une URL d'origine ;
- des données exploitables par le Matching Engine ;
- des données exploitables par Opportunity Ranking.

Cette phase définit uniquement les sources et les règles de collecte.

---

PROCHAINE PHASE

5.9.2 Search Criteria

Objectif :

Définir précisément :

- les mots-clés recherchés ;
- les mots-clés exclus ;
- les zones géographiques ;
- les critères de télétravail ;
- les critères de séniorité ;
- les seuils de qualité ;
- les règles de filtrage avant matching.
