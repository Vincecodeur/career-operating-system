# Design Direction

## Phase

5.7.6 Design Direction

## Objectif

Définir les principes UX, UI et Design System du Career Operating System avant toute implémentation frontend.

Ce document définit :

- la philosophie produit ;
- les principes UX ;
- l'identité visuelle ;
- la stratégie responsive ;
- la stratégie d'accessibilité ;
- les composants UI ;
- la stratégie de thème ;
- les technologies UI retenues.

Ce document sert de référence pour toutes les futures implémentations frontend.

---

# Product Positioning

Career Operating System n'est pas :

- un job board ;
- un site de recrutement ;
- un ATS ;
- une marketplace de l'emploi.

Career Operating System est :

- un outil d'analyse ;
- un outil de décision ;
- un dashboard carrière ;
- une plateforme d'intelligence carrière.

L'utilisateur doit avoir l'impression d'utiliser :

- un produit SaaS professionnel ;
- un outil d'analyse moderne ;
- un produit orienté données ;
- un outil de pilotage personnel.

---

# Design Philosophy

Principes directeurs :

- simplicité ;
- lisibilité ;
- rapidité ;
- efficacité ;
- cohérence ;
- maintenabilité.

Le design doit privilégier :

- la compréhension ;
- l'analyse ;
- la prise de décision.

Le design ne doit pas privilégier :

- l'effet visuel ;
- les animations inutiles ;
- les éléments décoratifs ;
- la complexité.

---

# UX Principles

## Dashboard First

Le Dashboard constitue le point d'entrée principal du produit.

L'utilisateur doit comprendre rapidement :

- sa situation actuelle ;
- ses meilleures opportunités ;
- ses candidatures en cours ;
- ses prochaines actions.

---

## Information Before Decoration

L'information est prioritaire sur le design.

Les données doivent rester le centre de l'expérience utilisateur.

---

## One Primary Action

Chaque page doit posséder :

- une action principale ;
- quelques actions secondaires.

Aucune page ne doit présenter plusieurs actions principales concurrentes.

---

## Explainability First

Toute information calculée doit être expliquée.

Les scores doivent toujours être accompagnés :

- de leurs critères ;
- de leurs points forts ;
- de leurs points faibles ;
- de leurs malus éventuels.

---

## User Remains In Control

Le système recommande.

L'utilisateur décide.

Aucune action critique n'est automatisée.

---

# Navigation Strategy

## Desktop

Sidebar gauche permanente.

Rétractable.

Ouverte par défaut.

Structure :

Pages publiques

- Login
- Forgot Password

Pages protégées

- Dashboard
- Profile
- Search Criteria
- Opportunities
- Applications
- Settings
- My Account

---

## Mobile

Sidebar fermée par défaut.

Ouverture via menu hamburger.

Priorité :

- consultation ;
- suivi des candidatures ;
- lecture des analyses.

---

# Layout Strategy

Structure globale :

Header léger

- Sidebar gauche
- Zone de contenu

Structure validée :

┌─────────────────────────────────────┐
│ Header │
├──────────────┬──────────────────────┤
│ Sidebar │ Content Area │
├──────────────┴──────────────────────┤
│ Footer │
└─────────────────────────────────────┘

---

# Language Strategy

## MVP

Langue principale :

English

---

## Post MVP

Support prévu :

- English
- Français

---

## Règle architecture

Toutes les chaînes doivent être externalisées.

Aucun texte d'interface ne doit être hardcodé dans les composants.

L'application doit être conçue pour supporter plusieurs langues.

---

# Theme Strategy

## MVP

Support :

- Light Theme
- Dark Theme

Les deux thèmes doivent être prévus dès l'architecture frontend.

---

# Color Strategy

## Couleur primaire

Bleu.

Objectifs :

- professionnel ;
- neutre ;
- SaaS ;
- lisible.

---

## Règle importante

Ne jamais utiliser directement une couleur dans les composants.

Passer uniquement par des variables de thème :

- --primary
- --secondary
- --accent
- --background
- --foreground
- --success
- --warning
- --danger

Objectif :

Permettre un futur rebranding sans refactoring.

---

# Typography Strategy

Police recommandée :

Inter

Pourquoi :

- excellente lisibilité ;
- standard SaaS ;
- moderne ;
- open source.

Hiérarchie :

- H1
- H2
- H3
- Body
- Caption

---

# Density Strategy

Medium Density.

Le produit doit afficher beaucoup d'information sans devenir difficile à lire.

Objectif :

- limiter le scroll ;
- conserver une bonne lisibilité ;
- favoriser l'analyse.

---

# Opportunity Presentation Strategy

## Liste des opportunités

Format retenu :

Tableau.

Pourquoi :

- comparaison rapide ;
- analyse ;
- tri ;
- filtrage.

Cartes non retenues pour le MVP.

---

## Affichage du score

Format :

Score + Badge

Exemple :

92%
Excellent Fit

---

## Affichage des forces et faiblesses

Format :

Listes simples.

Exemple :

Strengths

- APIs
- SaaS
- Partnerships

Weaknesses

- Kubernetes
- Azure Certifications

---

# Profile Strategy

Les profils sont affichés sous forme de cartes.

Pourquoi :

- faible volume ;
- meilleure lisibilité ;
- plus simple que les tableaux.

---

# Notification Strategy

Format retenu :

Toast Notifications.

Pas de centre de notifications dans le MVP.

Utilisation :

- sauvegarde réussie ;
- erreur ;
- synchronisation ;
- suppression ;
- mise à jour.

---

# Pagination Strategy

Pagination classique.

Pas d'Infinite Scroll.

Pourquoi :

- plus prévisible ;
- plus simple ;
- adapté aux outils professionnels.

---

# Responsive Strategy

Approche :

Desktop First.

Ordre de priorité :

1. Desktop
2. Tablet
3. Mobile

Le produit est principalement utilisé pour :

- l'analyse ;
- la comparaison ;
- le suivi.

---

# Accessibility Strategy

Objectif :

WCAG AA.

Principes :

- contrastes suffisants ;
- navigation clavier ;
- focus visibles ;
- labels explicites ;
- structure sémantique correcte.

---

# UI Technology Strategy

## Framework UI

shadcn/ui

---

## Styling

Tailwind CSS

---

## Icônes

Lucide Icons

---

## Framework

React

---

## Language

TypeScript

---

# Product Inspirations

Produits de référence :

- Linear
- Notion
- GitHub
- Atlassian Jira

Inspirations recherchées :

- clarté ;
- rapidité ;
- sobriété ;
- efficacité.

---

# Anti-Patterns

À éviter :

- dashboard surchargé ;
- animations excessives ;
- couleurs agressives ;
- infinite scroll ;
- menus complexes ;
- popups inutiles ;
- design type réseau social ;
- design type job board marketing.

---

# Design System Rules

Tous les composants doivent :

- être réutilisables ;
- être documentés ;
- supporter le thème clair ;
- supporter le thème sombre ;
- respecter l'accessibilité ;
- être cohérents visuellement.

---

# MVP Design Scope

Inclus :

- Dashboard
- Profile
- Search Criteria
- Opportunities
- Applications
- Settings

Exclus :

- Market Intelligence
- Career Roadmap
- Application Assistant
- Interview Preparation

---

# Critères de validation

La phase 5.7.6 est terminée lorsque :

- les principes UX sont définis ;
- les principes UI sont définis ;
- la stratégie responsive est définie ;
- la stratégie accessibilité est définie ;
- la stratégie thème est définie ;
- la bibliothèque UI est choisie ;
- le design system est défini.

---

# Prochaine étape

Phase 5.7.7 Frontend Structure Plan

Objectif :

Définir la structure technique cible du frontend :

- React Router ;
- layouts ;
- pages ;
- composants ;
- services ;
- hooks ;
- design system ;
- organisation des dossiers ;
- stratégie d'implémentation.
