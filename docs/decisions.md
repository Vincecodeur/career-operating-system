# Decisions

## DEC-001

Le projet est personnel.

---

## DEC-002

Le Job Board est un module.

Le produit principal est un Career Operating System.

---

## DEC-003

Stack retenue :

Frontend :
React
TypeScript
Vite

Backend :
FastAPI

Database :
PostgreSQL

---

## DEC-004

Architecture retenue :

Monolithe modulaire.

---

## DEC-005

Commencer par l'import manuel des offres.

L'automatisation viendra plus tard.

---

## DEC-006

Le scoring doit toujours être justifié.

Aucun score opaque.

---

## DEC-007

La documentation est optimisée pour la reprise de contexte Copilot.

---

## DEC-008

Le projet doit rester publiable sur GitHub.

---

## DEC-009

Aucune candidature automatique.

Le système recommande.

L'utilisateur décide.

---

## DEC-010

Le repository suit une architecture Frontend / Backend séparée.

Le backend expose une API REST.

Le frontend consomme exclusivement cette API.

Toute logique métier appartient au backend.

Le frontend est responsable de la présentation et de l'expérience utilisateur.

---

DEC-011

Les dossiers ne sont créés que lorsqu'ils deviennent nécessaires.

Le repository doit rester minimaliste.

Toute création de dossier doit être justifiée par un besoin immédiat.

À chaque création de dossier, Copilot doit indiquer :

- son chemin complet ;
- son rôle ;
- pourquoi il devient nécessaire maintenant.

---

DEC-012

Les dossiers ne sont créés que lorsqu'ils deviennent nécessaires.

Copilot doit toujours indiquer :

- le chemin complet ;
- la raison de création ;
- le lien avec la phase actuelle.

Aucun dossier vide ne doit être créé de manière anticipée.

---

## DEC-013

Le profil candidat est construit selon une approche hybride.

Source initiale :

- CV
- Profil LinkedIn

Puis enrichissement manuel.

Le système doit permettre à l'utilisateur de corriger,
compléter ou modifier les informations extraites.

Le profil candidat devient la source de vérité du système.

Les documents importés servent uniquement à créer ou mettre à jour ce profil.

---

## DEC-014

Le backend est construit dès le départ avec :

- FastAPI
- PostgreSQL
- SQLAlchemy

Aucune phase intermédiaire utilisant du stockage mémoire,
des fichiers JSON ou SQLite n'est prévue.

Le projet doit être aligné dès le départ avec son architecture cible.

L'objectif est de limiter les refactorings futurs tout en conservant une architecture simple.

---

## DEC-015

Le projet utilise une base PostgreSQL dédiée.

Database :

career_os

User :

career_os_user

Le projet ne doit pas utiliser la base postgres par défaut.

Chaque projet possède sa propre base de données.

---

## DEC-016

Le domaine Profile est l'agrégat racine du système.

Tous les futurs domaines métier
(Jobs, Applications, Matching, Career Planning)
s'appuient sur le Profile.

Le développement fonctionnel commence toujours
par les besoins du Profile.

---

## DEC-017

Le système supporte plusieurs profils candidats.

Objectif :

Permettre différentes stratégies de carrière.

Exemples :

- Profil actuel
- Profil Product Manager
- Profil Solution Architect
- Profil Head of Partnerships

---

## DEC-018

Le modèle Profile V1 contient uniquement
les informations de pilotage de carrière.

Les compétences, langues, certifications
et expériences seront gérées dans des tables dédiées.

Le modèle Profile doit rester léger
et représenter la vue synthétique du candidat.

---

## DEC-019

SQLAlchemy create_all() est utilisé uniquement
pour les phases initiales du projet.

Toute évolution future du schéma devra être gérée
via un système de migrations.

Alembic sera introduit lorsque le modèle métier
commencera à évoluer régulièrement.

---

## DEC-020

Le projet utilise un catalogue central de compétences.

Les compétences sont stockées dans une entité dédiée : Skill.

Les profils candidats ne stockent pas directement les compétences sous forme de texte libre.

Les profils référencent les compétences via une relation dédiée.

Objectif :

Permettre un futur moteur de matching fiable entre :

- les compétences du profil candidat ;
- les compétences demandées par les offres d'emploi.

Cette approche évite les doublons et incohérences comme :

- Python
- python
- PYTHON
- Python Programming

Le catalogue central permettra plus tard d'ajouter :

- catégories de compétences ;
- niveaux de maîtrise ;
- synonymes ;
- relations avec les offres d'emploi.

## DEC-021

Les compétences d'un profil sont représentées par une table d'association dédiée : ProfileSkill.

ProfileSkill relie un Profile à une Skill.

Cette relation contient les informations spécifiques à la maîtrise de cette compétence par ce profil :

- years_of_experience ;
- self_assessment_level.

Le catalogue Skill reste générique.

Les informations de maîtrise appartiennent à la relation ProfileSkill, pas à Skill.

---

## DEC-022

Le projet expose une API dédiée pour associer les compétences aux profils.

L'association entre un profil et une compétence est gérée via ProfileSkill.

ProfileSkill permet de stocker les informations spécifiques à la maîtrise d'une compétence par un profil :

- years_of_experience ;
- self_assessment_level.

Le catalogue Skill reste générique.

Les données de maîtrise appartiennent à ProfileSkill.

---

## DEC-023

Les expériences professionnelles sont stockées dans une entité dédiée WorkExperience.

Une expérience appartient à un seul profil.

Les compétences restent stockées séparément dans le catalogue central Skills.

L'objectif est de séparer :

- ce que le candidat sait faire ;
- où et quand le candidat a acquis cette expérience.

WorkExperience permet de reconstruire le parcours professionnel du profil candidat sans mélanger les expériences avec les compétences.

---

## DEC-024

Le projet utilise un catalogue central de langues.

Les langues sont stockées dans une entité dédiée Language.

Les niveaux de maîtrise appartiennent à la relation ProfileLanguage.

L'objectif est de séparer :

- les langues disponibles ;
- le niveau réel du candidat pour chaque langue.

ProfileLanguage relie un Profile à une Language avec un proficiency_level.

Les niveaux recommandés sont :

- A1
- A2
- B1
- B2
- C1
- C2
- Native

---

### DEC-025

Le projet utilise un catalogue central de certifications.

Les certifications sont stockées dans une entité Certification.

Les informations relatives à la possession d'une certification par un candidat sont stockées dans ProfileCertification.

L'objectif est de séparer :

- les certifications disponibles ;
- les certifications réellement obtenues par le candidat.

ProfileCertification permet de gérer :

- la date d'obtention ;
- la date d'expiration ;
- l'identifiant de justificatif éventuel.

---

### DEC-026

Les offres d'emploi sont stockées dans une entité JobOffer.

La Phase 3 est limitée à l'import manuel des offres.

Aucune récupération automatique depuis un site tiers n'est prévue à ce stade.

L'objectif est de construire le premier consommateur des données du profil candidat avant l'introduction du moteur de matching.

Le modèle JobOffer V1 doit rester minimal et contenir uniquement les informations nécessaires à l'analyse d'une offre.

---

### DEC-027

Le projet utilise Pytest comme framework de tests automatisés.

Les tests automatisés sont introduits avant le Matching Engine afin de limiter les régressions.

Chaque nouveau domaine métier important devra progressivement être couvert par des tests automatisés.

---

### DEC-028

Les compétences requises par une offre sont stockées dans une relation dédiée JobOfferSkill.

JobOfferSkill relie une offre d'emploi à une compétence du catalogue central Skill.

Cette relation est utilisée comme fondation du futur moteur de matching.

Les compétences d'une offre ne sont pas stockées sous forme de texte libre afin de permettre une comparaison fiable avec les compétences du candidat.

---

### DEC-029

Le Matching Engine V1 compare uniquement les compétences du profil candidat et les compétences requises par une offre d'emploi.

Le score est calculé à partir du pourcentage de compétences de l'offre présentes dans le profil.

Les langues, certifications, expériences professionnelles et futures capacités IA sont exclues de la V1.

L'objectif est de valider le flux métier complet avant l'introduction de règles plus avancées.

---

### DEC-030

Le Frontend MVP adopte une approche Dashboard First.

L'utilisateur arrive sur un tableau de bord permettant de visualiser :

- les profils candidats ;
- les offres d'emploi ;
- les résultats de matching.

Le Frontend consomme exclusivement les APIs FastAPI existantes.

Aucune logique métier ne doit être implémentée dans React.

Le backend reste la source unique de vérité.

---

### DEC-031

Le Dashboard MVP affiche en priorité :

- les profils ;
- les offres d'emploi.

Le Dashboard ne calcule aucune logique métier.

Toutes les données affichées proviennent exclusivement des APIs backend.

Le Dashboard constitue une couche de visualisation.
