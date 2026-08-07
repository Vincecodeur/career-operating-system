# Design System

## Objectif

Le Design System du Career Operating System définit les règles visuelles, ergonomiques et techniques qui garantissent une expérience utilisateur cohérente, maintenable et évolutive.

Le Design System doit :

- accélérer le développement frontend ;
- garantir une cohérence visuelle globale ;
- réduire les divergences entre écrans ;
- améliorer la maintenabilité ;
- préparer le produit aux futures fonctionnalités ;
- limiter la dette technique frontend.

Ce Design System doit être utilisé par tous les futurs modules :

- Dashboard
- Profiles
- Job Discovery
- Opportunity Analysis
- Opportunity Ranking
- Applications
- Career Roadmap
- Settings

---

# Vision Produit

## Positionnement

Career Operating System est :

- un SaaS ;
- une plateforme d'analyse ;
- un outil d'aide à la décision carrière.

Career Operating System n'est pas :

- un job board ;
- un ATS classique ;
- un réseau social ;
- une marketplace de recrutement.

---

# Direction Visuelle

## Style Général

Direction retenue :

Modern SaaS + Data Analytics

Inspirations :

- Linear
- Stripe
- Vercel
- GitHub
- Notion
- Azure Portal

---

## Philosophie

Priorité :

1. Lisibilité
2. Hiérarchie visuelle
3. Rapidité d'analyse
4. Confort d'utilisation
5. Cohérence

Le design doit mettre en avant :

- les décisions ;
- les opportunités ;
- les écarts ;
- les priorités.

---

# Thèmes

## Dark Mode

Décision :

Dark Mode par défaut.

Objectifs :

- réduire la fatigue visuelle ;
- améliorer l'expérience sur les dashboards ;
- renforcer l'identité SaaS moderne.

---

## Light Mode

Support obligatoire.

Toutes les interfaces doivent fonctionner en :

- Light Mode
- Dark Mode

---

# Layout Global

## Structure Générale

```text
+----------------------------------------------------------+
| Sidebar                                                  |
+----------------------+-----------------------------------+
|                      | Header                            |
|                      +-----------------------------------+
|                      |                                   |
| Sidebar             | Content Area                      |
|                      |                                   |
|                      |                                   |
+----------------------+-----------------------------------+
```

---

# Sidebar

## Largeur

```text
280px
```

Décision validée.

---

## Objectifs

La Sidebar contient :

- la navigation principale ;
- les entrées fonctionnelles ;
- l'identité produit.

---

## MVP

```text
Career OS

Dashboard
Account

Logout
```

---

## Vision Future

```text
Career OS

Dashboard

Profiles
Job Discovery
Opportunities
Applications
Roadmap

Settings

Logout
```

---

# Header

## Objectif

Le Header affiche :

- le contexte ;
- l'utilisateur ;
- les actions globales.

---

## MVP

```text
Career Operating System

admin@career-os.local
```

---

## Vision Future

```text
Titre de Page

Utilisateur
Langue
Thème
Notifications
Recherche
```

---

# Content Area

## Principes

- largeur fluide ;
- contenu centré ;
- marges cohérentes ;
- respirations importantes.

Le contenu doit rester la priorité visuelle principale.

---

# Densité d'Information

Décision validée :

```text
Aérée
```

Objectifs :

- faciliter la lecture ;
- éviter les murs d'information ;
- favoriser l'analyse.

---

# Espacements

## Échelle Officielle

```text
xs = 4px
sm = 8px
md = 16px
lg = 24px
xl = 32px
2xl = 48px
3xl = 64px
```

---

# Typographie

## Hiérarchie

### H1

Titre principal de page.

Exemple :

```text
Dashboard
```

---

### H2

Titre de section.

Exemple :

```text
Profiles
Applications
```

---

### H3

Sous-section.

Exemple :

```text
Top Opportunities
Matching Result
```

---

### Body

Texte principal.

---

### Muted

Texte secondaire.

---

# Palette

## Primary

Bleu.

Utilisation :

- actions principales ;
- liens ;
- boutons principaux.

---

## Success

Vert.

Utilisation :

- réussite ;
- validation ;
- score positif.

---

## Warning

Orange.

Utilisation :

- alerte ;
- attention ;
- information importante.

---

## Danger

Rouge.

Utilisation :

- suppression ;
- erreur ;
- état critique.

---

## Neutral

Gris.

Utilisation :

- bordures ;
- séparateurs ;
- éléments secondaires.

---

# Design Tokens

Tous les composants doivent utiliser :

```text
Couleurs centralisées
Espacements centralisés
Typographie centralisée
```

---

## Interdiction

Ne jamais :

```text
hardcoder des couleurs
hardcoder des espacements
dupliquer les styles
```

dans les composants métier.

---

# Composants Fondamentaux

## PageContainer

Responsabilité :

Conteneur principal d'une page.

Utilisé par :

- Dashboard
- Account
- Profiles
- Settings

---

## PageHeader

Responsabilité :

Titre principal de page.

Exemple :

```text
Dashboard

Overview of profiles,
opportunities and applications.
```

---

## Section

Responsabilité :

Regrouper un domaine métier.

Exemple :

```text
Profiles

Applications

Matching Analysis
```

---

## Card

Responsabilité :

Afficher un bloc d'information.

Utilisation :

- listes ;
- détails ;
- résultats.

---

## StatCard

Responsabilité :

Afficher une métrique.

Exemple :

```text
Profiles

1
```

---

## EmptyState

Responsabilité :

Afficher un état vide.

Exemple :

```text
No applications found.
```

---

## LoadingState

Responsabilité :

Afficher un chargement.

Exemple :

```text
Loading...
```

---

## ErrorState

Responsabilité :

Afficher une erreur.

Exemple :

```text
Unable to load dashboard data.
```

---

# Dashboard Design

## Structure Cible

```text
Dashboard

Overview

Profiles

Opportunities

Matching Analysis

Applications
```

---

# KPI Cards

Décision validée :

Oui.

---

## KPI MVP

```text
Profiles

Job Offers

Applications

Top Match
```

---

## Exemple

```text
+--------------------+
| Profiles           |
|         1          |
+--------------------+

+--------------------+
| Job Offers         |
|         2          |
+--------------------+

+--------------------+
| Applications       |
|         5          |
+--------------------+

+--------------------+
| Top Match          |
|        75%         |
+--------------------+
```

---

# Matching Analysis

Objectif :

Mettre en évidence :

- le score ;
- les forces ;
- les faiblesses ;
- les recommandations.

Le matching constitue l'une des informations les plus importantes du produit.

---

# Opportunity Ranking

Objectif :

Mettre en évidence :

- les meilleures opportunités ;
- les écarts ;
- les priorités.

---

# Applications

Objectif :

Présenter rapidement :

- les candidatures ;
- leur statut ;
- les actions nécessaires.

---

# Accessibilité

Objectif :

WCAG AA.

---

## Obligations

Navigation clavier :

```text
Oui
```

---

Focus visibles :

```text
Oui
```

---

Contrastes suffisants :

```text
Oui
```

---

HTML sémantique :

```text
Oui
```

---

# Responsive Design

Ordre de priorité :

```text
Desktop
Tablet
Mobile
```

Le MVP est Desktop First.

---

# Stack UI

## Styling

```text
Tailwind CSS
```

---

## Components

```text
shadcn/ui
```

---

## Icons

```text
Lucide React
```

---

# Composants Futurs

## DataTable

Utilisation :

- offres ;
- candidatures ;
- profils.

---

## Badge

Utilisation :

- statuts ;
- catégories ;
- scores.

---

## Modal

Utilisation :

- confirmation ;
- édition ;
- suppression.

---

## Drawer

Utilisation :

- détails rapides ;
- navigation mobile.

---

## Tabs

Utilisation :

- pages complexes ;
- analyses ;
- vues multiples.

---

# Règles de Développement

## Obligatoire

Créer des composants :

- réutilisables ;
- génériques ;
- documentés.

---

## Interdit

Ne pas :

- utiliser des styles inline permanents ;
- dupliquer les composants ;
- créer des couleurs locales ;
- créer des espacements locaux.

---

# Vision Long Terme

Le Design System doit permettre au Career Operating System de devenir :

- un SaaS moderne ;
- une plateforme de pilotage de carrière ;
- une plateforme d'analyse ;
- un outil quotidien d'aide à la décision.

Toute évolution visuelle future devra respecter les décisions définies dans ce document.
