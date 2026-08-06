# Frontend Structure Plan

## Phase

5.7.7 Frontend Structure Plan

## Objectif

Définir la structure technique cible du frontend du Career Operating System avant toute évolution majeure du code.

Ce document définit :

- l'architecture React ;
- l'organisation des dossiers ;
- le routing ;
- les layouts ;
- l'authentification ;
- le state management ;
- le server state ;
- le design system ;
- l'internationalisation ;
- les conventions de développement.

Ce document sert de référence pour toutes les futures implémentations frontend.

---

# Architecture générale

Stack retenue :

- React
- TypeScript
- Vite
- React Router
- shadcn/ui
- Tailwind CSS
- Lucide Icons
- Zustand
- TanStack Query
- React Hook Form
- Zod

Objectifs :

- simplicité ;
- maintenabilité ;
- évolutivité ;
- typage fort ;
- architecture modulaire.

---

# Structure cible des dossiers

frontend/src

├── app
├── assets
├── components
├── features
├── hooks
├── layouts
├── lib
├── pages
├── providers
├── routes
├── services
├── stores
├── styles
├── types
└── i18n

---

# Description des dossiers

## app

Initialisation de l'application.

Contient :

- App.tsx
- configuration globale

---

## assets

Ressources statiques :

- logos
- images
- illustrations

---

## components

Composants UI réutilisables.

Exemples :

- DataTable
- ScoreBadge
- ApplicationStatusBadge
- LoadingSpinner
- ConfirmDialog

---

## features

Organisation par domaine métier.

Structure cible :

features/

- auth
- profiles
- search-criteria
- opportunities
- applications
- dashboard
- settings

Chaque domaine contient :

- components
- hooks
- services
- schemas
- types

---

## hooks

Hooks réutilisables.

Exemples :

- useAuth
- useTheme
- useDebounce
- usePagination

---

## layouts

Layouts principaux.

Contient :

- AuthLayout
- AppLayout

---

## lib

Bibliothèques et helpers génériques.

Exemples :

- api.ts
- queryClient.ts
- auth.ts
- utils.ts

---

## pages

Pages React Router.

Exemples :

- LoginPage
- DashboardPage
- ProfilePage
- OpportunitiesPage

---

## providers

Providers globaux.

Exemples :

- QueryProvider
- ThemeProvider
- AuthProvider

---

## routes

Configuration React Router.

---

## services

Clients API.

Exemples :

- authService
- profileService
- opportunityService
- applicationService

---

## stores

Stores Zustand.

Exemples :

- authStore
- uiStore

---

## styles

Styles globaux.

Exemples :

- globals.css

---

## types

Types TypeScript partagés.

---

## i18n

Internationalisation.

Contient :

- en
- fr

Architecture prévue dès le MVP.

---

# Routing Strategy

## Routes publiques

/login

/forgot-password

---

## Routes protégées

/dashboard

/profile

/profile/:id

/search-criteria

/search-criteria/:id

/opportunities

/opportunities/:id

/applications

/applications/:id

/settings

/account

---

# Layout Strategy

## Auth Layout

Utilisé pour :

- Login
- Forgot Password

Structure :

Logo
↓
Formulaire
↓
Footer simple

---

## App Layout

Utilisé pour toutes les pages métier.

Structure :

Header

- Sidebar
- Content Area

  ***

# Authentication Strategy

## MVP

Authentification requise.

Un seul compte utilisateur.

Compte créé manuellement.

Pas d'inscription publique.

---

## Technologie

JWT Access Token

-

Refresh Token

---

## Flux

Login
↓
Access Token
↓
Protected Routes
↓
Refresh Token automatique

---

## Protection des routes

Toutes les pages métier nécessitent une authentification.

Utilisateur non connecté :

→ redirection Login

---

# User Management Strategy

Le MVP reste mono-utilisateur.

Cependant l'architecture doit être compatible avec une évolution future :

User
↓
Profiles
↓
Search Criteria
↓
Applications

Tous les futurs domaines doivent être compatibles avec un user_id.

---

# State Management Strategy

## Zustand

Utilisation limitée aux états globaux.

Exemples :

- utilisateur connecté
- thème
- préférences UI
- état sidebar

Ne pas utiliser Zustand pour :

- données API
- listes métier
- cache serveur

---

# Server State Strategy

## TanStack Query

Responsable :

- cache
- loading
- retry
- invalidation
- synchronisation serveur

Toutes les données backend passent par TanStack Query.

---

# Forms Strategy

## React Hook Form

Utilisé pour :

- Profile
- Search Criteria
- Login
- Account

---

# Validation Strategy

## Zod

Utilisé pour :

- validation frontend
- validation formulaires
- typage partagé

Objectif :

Une seule définition de schéma.

---

# Design System Strategy

Bibliothèque retenue :

shadcn/ui

Composants standardisés.

Objectifs :

- réutilisables ;
- accessibles ;
- cohérents ;
- maintenables.

---

# Theme Strategy

Support natif :

- Light Theme
- Dark Theme

Implémenté dès le MVP.

---

# Color Strategy

Couleur primaire :

Blue

Mais jamais utilisée directement.

Variables obligatoires :

- --primary
- --secondary
- --accent
- --background
- --foreground
- --success
- --warning
- --danger

Objectif :

Support futur du rebranding.

---

# Typography Strategy

Police :

Inter

Hiérarchie :

- H1
- H2
- H3
- Body
- Caption

---

# Internationalisation

## MVP

Langue principale :

English

---

## Post MVP

Ajout immédiat prévu :

French

---

## Règle

Aucune chaîne UI hardcodée dans un composant.

Toutes les chaînes passent par le système i18n.

---

# Accessibility Strategy

Objectif :

WCAG AA

Principes :

- navigation clavier ;
- focus visibles ;
- contrastes suffisants ;
- labels explicites ;
- structure sémantique.

---

# Responsive Strategy

Approche :

Desktop First

Priorité :

1. Desktop
2. Tablet
3. Mobile

Sidebar :

Desktop
→ ouverte

Mobile
→ fermée

---

# Architecture des pages MVP

## Auth

- Login
- Forgot Password
- My Account

---

## Dashboard

- Dashboard

---

## Profiles

- Profile List
- Profile Details

---

## Search Criteria

- Search Criteria List
- Search Criteria Details

---

## Opportunities

- Opportunities List
- Opportunity Details

---

## Applications

- Applications List
- Application Details

---

## Settings

- Settings

---

# Plan d'implémentation recommandé

## Étape 1

Infrastructure frontend

- React Router
- App Layout
- Auth Layout
- Theme Provider
- TanStack Provider

---

## Étape 2

Authentification

- Login
- JWT
- Refresh Token
- Protected Routes

---

## Étape 3

Navigation

- Sidebar
- Header
- Routing

---

## Étape 4

Migration Dashboard

Intégration du Dashboard existant dans la nouvelle architecture.

---

## Étape 5

Pages métier MVP

Ordre recommandé :

- Profiles
- Search Criteria
- Opportunities
- Applications
- Settings

---

# Critères de validation

La phase 5.7.7 est terminée lorsque :

- la structure frontend est définie ;
- les routes sont définies ;
- l'authentification est définie ;
- le state management est défini ;
- le design system est défini ;
- l'internationalisation est définie ;
- le plan d'implémentation est défini.

---

# Résultat attendu

À l'issue de cette phase :

- toute la vision frontend est documentée ;
- le design est documenté ;
- la structure technique est documentée ;
- le développement peut reprendre sans nouvelle décision d'architecture majeure.
