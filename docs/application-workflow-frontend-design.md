# Application Workflow Frontend Design

## Phase

7.1.17.7 Frontend Design

## Contexte

Le backend Application Workflow est terminé et validé.

Fonctionnalités backend disponibles :

- Application CRUD
- Application Notes
- Application Source Type
- Status Transition API
- Timeline API
- ApplicationEvent
- Workflow Lifecycle DEC-063

Le frontend actuel permet uniquement :

- visualisation des candidatures
- affichage du détail d’une candidature

L’objectif de cette phase est de définir l’expérience utilisateur cible avant toute implémentation React.

---

# Objectifs

Le module Applications doit permettre à l’utilisateur de :

- suivre ses candidatures
- comprendre leur progression
- consulter rapidement les informations importantes
- visualiser l’historique de progression
- piloter ses prochaines actions

Le module ne doit pas se comporter comme un ATS RH.

Le produit reste un Career Operating System.

---

# Décision UX retenue

Le MVP utilise :

- KPI Cards
- Application Cards
- Detail Panel

Architecture :

Applications Page

↓

KPI Cards

↓

Application Cards

-

Application Detail Panel

Cette approche a été retenue car elle offre :

- une meilleure expérience utilisateur
- une meilleure cohérence avec le reste du produit
- une réutilisation future dans Dashboard Evolution
- une complexité de développement limitée

Le Kanban est reporté hors MVP.

Le CRM Table est rejeté pour le MVP.

---

# Alternatives étudiées

## CRM Table

Exemple :

Company | Status | Source

Avantages :

- densité d’information
- filtrage facile

Inconvénients :

- faible valeur UX
- peu cohérent avec la vision Career Operating System

Décision :

Rejeté pour MVP.

---

## Kanban

Exemple :

Applied
Interview
Offer

Avantages :

- visuel
- pipeline clair

Inconvénients :

- complexité importante
- drag and drop futur
- faible valeur supplémentaire à ce stade

Décision :

Reporté Post-MVP.

---

## Master Detail Classique

Exemple :

Liste
→
Détail

Avantages :

- très simple

Inconvénients :

- peu moderne

Décision :

Non retenu.

---

## Cards + Detail Panel

Avantages :

- moderne
- clair
- réutilisable
- cohérent avec Dashboard Evolution

Décision :

Solution retenue.

---

# Applications Page Layout

Structure générale :

+-----------------------------------------------------+
| Applications + New |
+-----------------------------------------------------+

+----------+----------+----------+----------+---------+
| Total | Active | Interview| Offer | Hired |
+----------+----------+----------+----------+---------+

+----------------------+-----------------------------+
| Applications Cards | Application Detail Panel |
+----------------------+-----------------------------+

---

# KPI Cards

KPI affichés :

- Total Applications
- Active Applications
- Interviews
- Offers
- Accepted

Source :

Applications API

Responsabilité :

visualisation uniquement

Aucun calcul métier frontend.

---

# Application Cards

Chaque candidature est affichée sous forme de carte.

Informations affichées :

- Job Title
- Company
- Status Badge
- Source Type
- Last Updated Date

Exemple :

+----------------------------------+
| Product Manager |
| Google |
| |
| Interview |
| |
| Referral |
| Updated 17 Aug 2026 |
+----------------------------------+

---

# Application Detail Panel

Structure :

1. Application Information

2. Workflow

3. Notes

4. Timeline

---

## Application Information

Informations affichées :

- Job Title
- Company
- Profile
- Source Type
- Created Date
- Updated Date

---

# Workflow Section

Visualisation :

Applied
↓

Phone Screen
↓

Interview
↓

Offer
↓

Accepted

Sorties terminales :

- Rejected
- Withdrawn

Le statut actuel est mis en évidence.

Exemple :

[Applied] --- [Phone Screen] --- [Interview] --- [Offer] --- [Accepted]

Le statut courant utilise le style primaire.

---

# Workflow Actions

Le frontend affiche uniquement les transitions autorisées.

Exemple :

Current Status:

Interview

Actions disponibles :

- Move To Offer
- Mark Rejected
- Withdraw

Les transitions interdites ne sont jamais proposées.

---

# Notes Section

Objectif :

Conserver :

- recruiter feedback
- salary notes
- preparation notes
- follow-up notes

Champ :

Application.notes

Le MVP conserve un unique champ libre.

Aucun historique des notes.

---

# Timeline Section

Objectif :

Afficher l’historique métier de la candidature.

Source :

GET /applications/{id}/timeline

Données :

- old_value
- new_value
- event_date

Exemple :

Interview → Offer
17 Aug 2026

Phone Screen → Interview
15 Aug 2026

Applied → Phone Screen
12 Aug 2026

Timeline triée du plus récent au plus ancien.

---

# Source Tracking

Valeurs supportées :

- OPPORTUNITY
- MANUAL
- REFERRAL
- EXTERNAL

Affichage :

Badges.

Exemple :

[Referral]

ou

[Manual]

---

# Empty States

## Aucun résultat

Message :

No applications found.

Action :

Create your first application.

---

## Aucun élément sélectionné

Message :

Select an application to view details.

---

# Error States

## Impossible de charger les applications

Message :

Unable to load applications.

Action :

Retry.

---

## Impossible de charger la timeline

Message :

Unable to load application history.

Action :

Retry.

---

# Mobile Behaviour

Le MVP est desktop first.

Sur petits écrans :

Cards
↓

Detail Panel

Le panneau détail passe sous la liste.

Aucun design mobile spécifique MVP.

---

# Hors périmètre MVP

Exclus explicitement :

- Kanban
- Drag and Drop
- Calendar Integration
- Recruiter CRM
- Reminder System
- Email Synchronization
- AI Coaching
- Source Analytics
- Advanced Reporting

---

# Évolution Future

Phase 7.3 Dashboard Evolution :

Possibilités futures :

- Career Pipeline
- Kanban View
- Application Funnel
- Recruiter Analytics
- Success Rate Analytics
- Interview Rate Analytics

---

# Conclusion

Le MVP Application Workflow utilise :

- KPI Cards
- Application Cards
- Detail Panel
- Status Workflow
- Notes
- Timeline
- Source Tracking

Cette approche fournit :

- simplicité
- rapidité d’implémentation
- cohérence produit
- compatibilité avec les futures évolutions Career Dashboard
