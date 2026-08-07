# First External Source

## Objectif

Connecter la première source réelle d'offres d'emploi afin de valider le pipeline complet Job Discovery.

Cette phase doit permettre de démontrer que le système est capable de :

- se connecter à une source externe ;
- récupérer des offres ;
- normaliser les données ;
- persister les offres ;
- retrouver les offres depuis la base de données.

Cette phase constitue la première validation de bout en bout du domaine Job Discovery.

---

CONTEXTE

Les phases précédentes ont permis de définir :

- les sources cibles ;
- les critères de recherche ;
- le modèle normalisé d'offre ;
- les règles de déduplication ;
- les règles de qualité ;
- les règles d'archivage.

Le système dispose désormais d'un modèle JobOffer normalisé.

L'objectif n'est plus de définir la structure.

L'objectif est désormais de valider le flux complet avec une vraie source externe.

---

SOURCE RETENUE

Source principale MVP :

France Travail

Justification :

- API officielle disponible ;
- recherche d'offres disponible ;
- détail des offres disponible ;
- données structurées ;
- source stable ;
- cohérente avec la stratégie API First.

Plan B :

LinkedIn

Utilisation uniquement si les accès France Travail ne sont pas disponibles.

---

STRATÉGIE D'INTÉGRATION

Approche :

API First

Le système doit privilégier l'API officielle France Travail.

Aucun scraping n'est prévu dans cette phase.

Le scraping LinkedIn reste uniquement une stratégie de secours.

---

ENVIRONNEMENTS

Ordre cible :

1. Sandbox
2. Production

Objectif :

Valider le fonctionnement sur un environnement de test avant utilisation réelle.

---

AUTHENTIFICATION

Type retenu :

OAuth2

Le connecteur France Travail devra être conçu autour d'une stratégie OAuth2.

L'implémentation exacte dépendra de la documentation officielle obtenue lors de l'ouverture des accès.

---

ARCHITECTURE CIBLE

Flux complet :

France Travail
↓
Connector
↓
Raw Offer
↓
Normalization
↓
Normalized JobOffer
↓
Database
↓
API
↓
Frontend

Aucune phase du pipeline ne doit être contournée.

---

OBJECTIF TECHNIQUE

Valider :

Source
↓
Normalization
↓
Database

Le MVP ne cherche pas encore à optimiser les performances.

Le MVP cherche uniquement à valider le fonctionnement complet.

---

VOLUME MVP

Objectif initial :

50 offres

Pourquoi :

- suffisamment représentatif ;
- facile à vérifier ;
- rapide à analyser ;
- compatible avec les premiers tests.

---

RECHERCHE MVP

Les critères de recherche utilisés doivent être cohérents avec :

docs/job-sources.md

et

docs/search-criteria.md

Critères actuels :

- France
- Paris + 10 km
- Integration Architect
- CDI
- Français ou Anglais

Les futurs critères avancés sont hors périmètre.

---

DONNÉES ATTENDUES

Chaque offre récupérée doit fournir autant que possible :

- titre ;
- entreprise ;
- description ;
- ville ;
- pays ;
- contrat ;
- salaire ;
- URL source ;
- date de publication.

Les données récupérées seront ensuite normalisées.

---

MAPPING VERS JOBOFFER

Le connecteur ne doit jamais exposer directement les objets France Travail.

Toutes les données doivent être transformées vers :

JobOffer

JobSource

JobOfferSource

définis dans :

docs/offer-normalization.md

---

PERSISTANCE

Décision :

Persistance immédiate en base

Les offres récupérées doivent être sauvegardées.

Le MVP ne se limite pas à un affichage temporaire.

---

DÉDUPLICATION

Les règles définies dans offer-normalization.md s'appliquent.

Détection :

title

- company
- city

Si doublon :

- conserver l'offre ;
- mettre à jour les données ;
- conserver les différentes sources.

---

MISE À JOUR DES OFFRES

Lorsqu'une offre déjà connue est retrouvée :

Action :

mise à jour

Le système ne doit pas créer systématiquement une nouvelle offre.

---

GESTION DES ERREURS

Principe :

Logger et continuer

En cas d'erreurs :

- enregistrer l'erreur ;
- enregistrer le contexte ;
- poursuivre le traitement lorsque cela reste possible.

Objectif :

éviter qu'une offre invalide bloque l'ensemble de la collecte.

---

PRÉREQUIS

Avant le début du développement :

- demande d'accès France Travail réalisée ;
- identifiants reçus ;
- accès Sandbox validé.

Si l'accès n'est pas disponible :

- activation automatique du mode Mock Source.

Le développement du pipeline ne doit jamais être bloqué par une dépendance externe.
