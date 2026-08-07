# Frontend Architecture

## Objectif

Ce document décrit l'architecture frontend réelle du Career Operating System à la fin de la phase 5.8.8.

Il sert de référence pour :

- comprendre l'organisation du frontend ;
- faciliter la reprise du projet ;
- éviter les décisions contradictoires ;
- préparer les prochaines phases métier ;
- limiter les refactorings inutiles.

Le frontend est une couche de présentation.

Toute logique métier appartient au backend FastAPI.

Le frontend ne doit pas :

- calculer le matching ;
- calculer les scores ;
- classer les opportunités ;
- appliquer des règles métier ;
- dupliquer la logique backend.

Le frontend consomme les APIs FastAPI et affiche les résultats.

---

STACK FRONTEND ACTUELLE

Stack utilisée :

- React
- TypeScript
- Vite
- React Router
- Zustand
- TanStack Query
- React Hook Form
- Zod
- Tailwind CSS
- Lucide React

---

STRUCTURE ACTUELLE

frontend/src

App.css
App.tsx
index.css
main.tsx

assets/
hero.png
react.svg
vite.svg

components/
ApplicationTracker.tsx
Dashboard.tsx
JobOfferList.tsx
MatchingResult.tsx
OpportunityRanking.tsx
ProfileList.tsx

components/ui/
Card.tsx
PageHeader.tsx
Section.tsx
StatCard.tsx

layouts/
AppLayout.tsx

lib/
queryClient.ts

pages/
AccountPage.tsx
ApplicationsPage.tsx
DashboardPage.tsx
ForgotPasswordPage.tsx
LoginPage.tsx
OpportunitiesPage.tsx
ProfilesPage.tsx
SettingsPage.tsx

providers/
AppProviders.tsx

routes/
ProtectedRoute.tsx
router.tsx

services/
api.ts
authApi.ts

stores/
authStore.ts
uiStore.ts

---

RESPONSABILITÉ DES DOSSIERS

ASSETS

Le dossier assets contient les ressources statiques.

Exemples :

- hero.png
- react.svg
- vite.svg

Règles :

- aucune logique applicative ;
- aucun appel API ;
- aucun état React ;
- uniquement des fichiers statiques.

---

COMPONENTS

Le dossier components contient les composants React réutilisables liés à l'affichage.

Composants actuels :

- Dashboard
- ProfileList
- JobOfferList
- MatchingResult
- OpportunityRanking
- ApplicationTracker

Responsabilités :

- afficher des données ;
- structurer une partie d'écran ;
- recevoir les données via props ;
- rester réutilisables lorsque c'est possible.

Interdictions :

- ne pas contenir de logique métier complexe ;
- ne pas appeler directement les APIs backend ;
- ne pas calculer les scores ou rankings ;
- ne pas gérer directement le routing global.

---

COMPONENTS/UI

Le dossier components/ui contient les premières briques du Design System.

Composants actuels :

- Card
- PageHeader
- Section
- StatCard

Responsabilités :

- fournir des composants génériques ;
- rester indépendants des domaines métier ;
- être réutilisables dans toutes les pages ;
- assurer une cohérence visuelle minimale.

Règles :

- un composant UI ne doit pas connaître les domaines Profile, Opportunity ou Application ;
- un composant UI ne doit pas contenir d'appel API ;
- un composant UI ne doit pas gérer d'état métier ;
- un composant UI doit être simple et composable.

---

LAYOUTS

Le dossier layouts contient les structures globales d'affichage.

Layout actuel :

- AppLayout

Responsabilités :

- afficher la Sidebar ;
- afficher le Header ;
- afficher la zone de contenu principale ;
- rendre les routes enfants via Outlet.

Structure :

Sidebar

- Header
- Main Content

Règles :

- un layout ne contient pas de logique métier ;
- un layout peut contenir de la navigation ;
- un layout peut lire l'utilisateur connecté ;
- un layout peut déclencher la déconnexion ;
- un layout ne doit pas appeler les APIs métier.

---

LIB

Le dossier lib contient les configurations techniques partagées.

Fichier actuel :

- queryClient.ts

Responsabilité :

- configuration centrale TanStack Query.

Règles :

- centraliser les configurations techniques ;
- éviter les duplications ;
- ne pas y mettre de logique métier.

---

PAGES

Le dossier pages contient les pages routables.

Pages actuelles :

- LoginPage
- ForgotPasswordPage
- DashboardPage
- ProfilesPage
- OpportunitiesPage
- ApplicationsPage
- SettingsPage
- AccountPage

Responsabilités :

- composer les composants ;
- définir le contenu principal d'une route ;
- organiser les sections ;
- utiliser les composants UI.

Règles :

- une page peut orchestrer des composants ;
- une page peut appeler un store ;
- une page peut appeler un hook ;
- une page ne doit pas contenir de logique métier lourde ;
- une page ne doit pas calculer les scores ou le matching.

---

PROVIDERS

Le dossier providers contient les providers React globaux.

Provider actuel :

- AppProviders

Responsabilités :

- encapsuler l'application ;
- centraliser les providers globaux ;
- éviter leur dispersion dans main.tsx.

Provider actuel :

- TanStack Query Provider

Providers futurs :

- Theme Provider
- i18n Provider
- Auth Bootstrap Provider

---

ROUTES

Le dossier routes contient la configuration du routing.

Fichiers :

- router.tsx
- ProtectedRoute.tsx

Responsabilités :

- définir les routes ;
- déclarer les routes publiques ;
- déclarer les routes protégées ;
- gérer les redirections.

Routes publiques :

- /login
- /forgot-password

Routes protégées :

- /dashboard
- /profiles
- /opportunities
- /applications
- /settings
- /account

Règles :

- routing centralisé ;
- les pages ne définissent pas leurs propres routes ;
- les routes protégées passent par ProtectedRoute ;
- les routes métier sont rendues dans AppLayout.

---

SERVICES

Le dossier services contient les accès API.

Fichiers :

- api.ts
- authApi.ts

Responsabilités :

- encapsuler les appels HTTP ;
- isoler les URLs backend ;
- retourner les données JSON ;
- gérer les erreurs techniques simples.

Règle obligatoire :

Aucun composant React ne doit appeler fetch directement.

Tous les appels API passent par services/.

---

STORES

Le dossier stores contient les stores Zustand.

Stores actuels :

- authStore
- uiStore

authStore :

- token ;
- utilisateur connecté ;
- authentification ;
- login ;
- logout ;
- récupération de l'utilisateur courant.

uiStore :

- état UI global ;
- futurs comportements UI partagés.

Règles :

- Zustand est réservé à l'état global local ;
- les données API métier ne doivent pas être stockées dans Zustand ;
- les données serveur doivent être gérées par TanStack Query.

---

ARCHITECTURE DE NAVIGATION

Structure actuelle :

AppProviders
↓
RouterProvider
↓
ProtectedRoute
↓
AppLayout
↓
Page

---

ROUTES PUBLIQUES

- /login
- /forgot-password

Ces routes ne passent pas par AppLayout.

---

ROUTES PROTÉGÉES

- /dashboard
- /profiles
- /opportunities
- /applications
- /settings
- /account

Ces routes passent par :

ProtectedRoute
↓
AppLayout
↓
Outlet

---

APPLAYOUT

Responsabilités :

- Sidebar ;
- Header ;
- Main Content Area ;
- Navigation ;
- Logout ;
- Informations utilisateur.

Navigation actuelle :

- Dashboard
- Profiles
- Opportunities
- Applications
- Settings
- Account
- Logout

---

PAGES ACTUELLES

DashboardPage

Responsabilité :

Afficher le Dashboard principal.

Contenu :

- Overview
- KPI Cards
- Profiles
- Opportunities
- Matching Analysis
- Applications

---

ProfilesPage

Responsabilité :

Future gestion des profils.

Statut :

Skeleton MVP

---

OpportunitiesPage

Responsabilité :

Future exploration des opportunités.

Statut :

Skeleton MVP

---

ApplicationsPage

Responsabilité :

Futur suivi des candidatures.

Statut :

Skeleton MVP

---

SettingsPage

Responsabilité :

Futurs paramètres applicatifs.

Statut :

Skeleton MVP

---

AccountPage

Responsabilité :

Afficher les informations du compte connecté.

Fonctionnalités :

- email utilisateur ;
- statut utilisateur ;
- logout.

---

LoginPage

Responsabilité :

Connexion utilisateur.

S'appuie sur :

- authApi ;
- authStore ;
- backend /auth/login.

---

ForgotPasswordPage

Responsabilité :

Placeholder de réinitialisation de mot de passe.

Statut :

Placeholder MVP

Réinitialisation réelle :

Non implémentée

---

DESIGN SYSTEM ACTUEL

Composants disponibles :

- Card
- PageHeader
- Section
- StatCard

---

RÈGLES FRONTEND

Règle 1

Aucune logique métier dans React.

Le backend calcule :

- matching ;
- scoring ;
- ranking.

---

Règle 2

Tous les appels API passent par services/.

---

Règle 3

Les pages composent les composants.

Les composants n'importent jamais les pages.

---

Règle 4

Les composants UI sont génériques.

Correct :

- Card
- Section
- StatCard

Incorrect :

- OpportunityCard dans components/ui
- ProfileSummary dans components/ui

---

Règle 5

Zustand est limité à l'état global local.

TanStack Query doit gérer les données serveur.

---

Règle 6

Les pages skeleton ne contiennent pas encore de logique métier avancée.

Elles servent à stabiliser :

- routes ;
- navigation ;
- layout ;
- structure produit.

---

CONVENTIONS DE NOMMAGE

Pages

Format :

<Name>Page.tsx

Exemples :

- DashboardPage.tsx
- ProfilesPage.tsx
- ApplicationsPage.tsx

---

Components

Format :

<Name>.tsx

Exemples :

- Dashboard.tsx
- MatchingResult.tsx
- OpportunityRanking.tsx

---

UI Components

Format :

<Name>.tsx

Exemples :

- Card.tsx
- Section.tsx
- StatCard.tsx

---

Stores

Format :

<domain>Store.ts

Exemples :

- authStore.ts
- uiStore.ts

---

Services

Format :

<domain>Api.ts

ou

api.ts

Exemples :

- authApi.ts
- api.ts

---

STRUCTURE CIBLE FUTURE

src/
components/
components/ui/
features/
hooks/
layouts/
lib/
pages/
providers/
routes/
services/
stores/

---

DOSSIER FEATURES FUTUR

Le dossier features n'existe pas encore.

Domaines candidats :

- features/profiles
- features/opportunities
- features/applications
- features/search-criteria
- features/job-discovery
- features/settings

Règle :

Ne pas créer features avant qu'un domaine ait réellement besoin de composants, hooks, services ou schemas dédiés.

---

ÉTAT À LA FIN DE LA PHASE 5.8.8

Livré :

- Authentication
- Protected Routes
- App Providers
- App Layout
- Sidebar
- Header
- Dashboard
- Tailwind CSS
- Design System Foundation
- Dashboard Component Modernization
- MVP Page Skeletons

Pages disponibles :

- Dashboard
- Profiles
- Opportunities
- Applications
- Settings
- Account
- Login
- Forgot Password

La structure frontend est désormais suffisamment stable pour être documentée et servir de base aux futures fonctionnalités métier.

---

PROCHAINE ÉTAPE

Après validation et commit de ce document :

Phase 5.8.9 Frontend Structure Documentation

Puis préparation des futures fonctionnalités :

- Search Criteria
- Job Discovery
- Job Sources
- Opportunity Analysis
- Market Intelligence
- Career Planning
