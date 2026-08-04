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
