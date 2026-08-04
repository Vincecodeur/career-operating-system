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
