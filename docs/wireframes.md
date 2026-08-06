# Wireframes

## Phase

5.7.5 Wireframes

## Objectif

Définir les wireframes basse fidélité du Career Operating System.

L'objectif n'est pas le design final.

L'objectif est de valider :

- la structure des écrans ;
- la navigation ;
- la hiérarchie des informations ;
- les parcours utilisateurs ;
- la densité d'information ;
- les interactions principales.

Les wireframes sont volontairement simples.

---

# Structure globale du layout

## Navigation desktop validée

Sidebar gauche permanente.

Header supérieur léger.

Zone centrale dédiée au contenu.

## Wireframe global

┌──────────────────────────────────────────────────────────────┐
│ Header │
├───────────────┬──────────────────────────────────────────────┤
│ Dashboard │ │
│ Profile │ │
│ Search │ Content Area │
│ Opportunities │ │
│ Applications │ │
│ Settings │ │
├───────────────┴──────────────────────────────────────────────┤
│ Footer optionnel │
└──────────────────────────────────────────────────────────────┘

---

# WF-00 Login

## Objectif

Permettre à l'utilisateur de s'authentifier.

## Wireframe

┌───────────────────────────────────────────┐
│ Career OS │
├───────────────────────────────────────────┤
│ Email │
│ [________________________] │
├───────────────────────────────────────────┤
│ Password │
│ [________________________] │
├───────────────────────────────────────────┤
│ [ Login ] │
├───────────────────────────────────────────┤
│ Forgot Password │
└───────────────────────────────────────────┘

## Actions

- Login
- Open Forgot Password

# WF-00.1 Forgot Password

## Objectif

Permettre à l'utilisateur de demander une réinitialisation de mot de passe.

## Wireframe

┌───────────────────────────────────────────┐
│ Forgot Password │
├───────────────────────────────────────────┤
│ Email │
│ [________________________] │
├───────────────────────────────────────────┤
│ [ Send Reset Link ] │
└───────────────────────────────────────────┘

## Actions

- Submit Email
- Return To Login

# WF-00.2 My Account

## Objectif

Afficher les informations du compte utilisateur.

## Wireframe

┌───────────────────────────────────────────┐
│ My Account │
├───────────────────────────────────────────┤
│ Email │
│ user@example.com │
├───────────────────────────────────────────┤
│ Language │
│ English │
├───────────────────────────────────────────┤
│ Theme │
│ Light / Dark │
├───────────────────────────────────────────┤
│ [ Save ] │
└───────────────────────────────────────────┘

## Actions

- Update Preferences
- Change Password
- Logout

# WF-01 Dashboard

## Objectif

Vue synthétique de la situation carrière.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Dashboard │
├───────────────────────────────────────────────────────────┤
│ Opportunities │ Applications │ Profiles │
│ 127 │ 12 │ 4 │
├───────────────────────────────────────────────────────────┤
│ Top Opportunities │
│ --------------------------------------------------------- │
│ Solution Architect Score 92 │
│ Senior TPM Score 88 │
│ Product Manager Score 84 │
├───────────────────────────────────────────────────────────┤
│ Recent Opportunities │
├───────────────────────────────────────────────────────────┤
│ Recommended Actions │
└───────────────────────────────────────────────────────────┘

## Actions

- Open Profile
- Open Opportunities
- Open Applications
- Open Search Criteria

---

# WF-02 Profile List

## Objectif

Afficher les profils candidats disponibles.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Profiles [+] │
├───────────────────────────────────────────────────────────┤
│ Current Profile > │
│ Solution Architect > │
│ Product Manager > │
│ Head Of Partnerships > │
└───────────────────────────────────────────────────────────┘

## Actions

- Create Profile
- Open Profile
- Delete Profile

---

# WF-03 Profile Details

## Objectif

Afficher et modifier un profil candidat.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Vincent - Solution Architect │
├───────────────────────────────────────────────────────────┤
│ General Information │
├───────────────────────────────────────────────────────────┤
│ Skills │
│ Python │
│ Azure │
│ APIs │
├───────────────────────────────────────────────────────────┤
│ Work Experience │
├───────────────────────────────────────────────────────────┤
│ Languages │
├───────────────────────────────────────────────────────────┤
│ Certifications │
├───────────────────────────────────────────────────────────┤
│ External Analyses │
├───────────────────────────────────────────────────────────┤
│ CV / Documents │
└───────────────────────────────────────────────────────────┘

## Actions

- Edit Profile
- Add Skill
- Add Experience
- Add Language
- Add Certification
- Add CV
- Add Analysis

---

# WF-04 Search Criteria List

## Objectif

Afficher les ensembles de critères de recherche.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Search Criteria [+] │
├───────────────────────────────────────────────────────────┤
│ France - Solution Architect > │
│ Europe - Product Manager > │
│ Remote - TPM > │
└───────────────────────────────────────────────────────────┘

## Actions

- Create Criteria
- Edit Criteria
- Delete Criteria

---

# WF-05 Search Criteria Details

## Objectif

Configurer les critères de collecte et de scoring.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Search Criteria │
├───────────────────────────────────────────────────────────┤
│ Titles │
│ [ Solution Architect ] │
├───────────────────────────────────────────────────────────┤
│ Countries │
│ [ France ] [ UK ] │
├───────────────────────────────────────────────────────────┤
│ Work Mode │
│ ( ) Remote │
│ (X) Hybrid │
│ ( ) Onsite │
├───────────────────────────────────────────────────────────┤
│ Salary Minimum │
│ [ 70000 ] │
├───────────────────────────────────────────────────────────┤
│ Languages │
├───────────────────────────────────────────────────────────┤
│ Included Keywords │
├───────────────────────────────────────────────────────────┤
│ Excluded Keywords │
├───────────────────────────────────────────────────────────┤
│ Sources │
├───────────────────────────────────────────────────────────┤
│ [ Save ] │
└───────────────────────────────────────────────────────────┘

---

# WF-06 Opportunities List

## Objectif

Afficher les opportunités collectées et classées.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Opportunities │
├───────────────────────────────────────────────────────────┤
│ Filters │
│ Score > 80 │
│ France │
│ Hybrid │
├───────────────────────────────────────────────────────────┤
│ Solution Architect Score 92 > │
│ Senior TPM Score 88 > │
│ Product Manager Score 84 > │
├───────────────────────────────────────────────────────────┤
│ Pagination │
└───────────────────────────────────────────────────────────┘

## Actions

- Filter
- Sort
- Open Opportunity
- Archive
- Mark Interesting
- Mark Not Interesting

---

# WF-07 Opportunity Details

## Objectif

Expliquer la pertinence d'une opportunité.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Senior Solution Architect │
├───────────────────────────────────────────────────────────┤
│ Score : 92 │
│ Source : LinkedIn │
│ Salary : 80k - 95k │
│ Work Mode : Hybrid │
├───────────────────────────────────────────────────────────┤
│ Strengths │
│ - APIs │
│ - Partnerships │
│ - SaaS │
├───────────────────────────────────────────────────────────┤
│ Weaknesses │
│ - Kubernetes │
├───────────────────────────────────────────────────────────┤
│ Matching Skills │
├───────────────────────────────────────────────────────────┤
│ Missing Skills │
├───────────────────────────────────────────────────────────┤
│ [ Open Job Offer ] │
│ [ Convert To Application ] │
│ [ Archive ] │
└───────────────────────────────────────────────────────────┘

---

# WF-08 Applications List

## Objectif

Afficher les candidatures suivies.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Applications │
├───────────────────────────────────────────────────────────┤
│ Senior TPM Interview > │
│ Solution Architect Applied > │
│ Product Manager Rejected > │
└───────────────────────────────────────────────────────────┘

## Actions

- Open Application
- Update Status

---

# WF-09 Application Details

## Objectif

Afficher une candidature détaillée.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Application │
├───────────────────────────────────────────────────────────┤
│ Opportunity │
│ Senior TPM │
├───────────────────────────────────────────────────────────┤
│ Status │
│ [ Interview ▼ ] │
├───────────────────────────────────────────────────────────┤
│ Source Link │
├───────────────────────────────────────────────────────────┤
│ Opportunity Snapshot │
├───────────────────────────────────────────────────────────┤
│ [ Save ] │
└───────────────────────────────────────────────────────────┘

## Actions

- Change Status
- Open Opportunity
- Open Source Link

---

# WF-10 Settings

## Objectif

Centraliser les paramètres du système.

## Wireframe

┌───────────────────────────────────────────────────────────┐
│ Settings │
├───────────────────────────────────────────────────────────┤
│ General │
├───────────────────────────────────────────────────────────┤
│ AI Preferences │
├───────────────────────────────────────────────────────────┤
│ Synchronization │
├───────────────────────────────────────────────────────────┤
│ Sources │
├───────────────────────────────────────────────────────────┤
│ System Information │
└───────────────────────────────────────────────────────────┘

## Actions

- Modify Settings
- Save Settings

---

# Règles UX

- Sidebar gauche permanente.
- Header léger.
- Dashboard First.
- Responsive dès la conception.
- Mobile secondaire par rapport au desktop.
- Une seule action primaire visible par écran.
- Les scores sont toujours visibles.
- Les points forts et points faibles sont toujours visibles.
- L'utilisateur reste maître des décisions.
- Aucune candidature automatique.

---

# Critères de validation

La phase 5.7.5 est terminée lorsque :

- tous les wireframes MVP existent ;
- la navigation est validée ;
- la hiérarchie des informations est validée ;
- les parcours utilisateurs sont cohérents ;
- aucun écran majeur n'est manquant.

---

# Prochaine étape

Phase 5.7.6 - Design Direction

Objectif :

Définir :

- identité visuelle ;
- design system ;
- composants UI ;
- responsive ;
- accessibilité ;
- thème clair / sombre ;
- inspirations produit ;
- règles UI globales.
