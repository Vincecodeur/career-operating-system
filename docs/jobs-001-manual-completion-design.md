# JOBS-001 - Manual Offer Completion Design

Date: 2026-09-15
Status: Draft
Phase: 7.1.31 (proposée, avant 7.1.28 MVP Closure Decision, même
pattern de reséquencement que DEC-081/7.1.29)

## Contexte

Les offres importées via LinkedIn Email Connector (DEC-086) ont
quality_level = PARTIAL : elles ne contiennent ni description réelle,
ni type de contrat, ni compétences extraites - seulement titre,
entreprise, ville, mode de travail et URL source.

Décision de séquencement (2026-09-15, confirmée par Vincent) :
JOBS-001 est traité avant la Phase 7.2 (AI Career Advisor / Gemini),
car les offres LinkedIn sont jugées les plus représentatives des
cibles de carrière réelles de Vincent, donc le meilleur jeu de
données pour valider la pertinence du matching avant de connecter un
vrai fournisseur IA.

## Objectif

Permettre à l'utilisateur de compléter manuellement, par simple
copier-coller depuis la page LinkedIn de l'offre, la description
réelle d'une offre PARTIAL, afin d'obtenir un score de matching
pertinent pour les offres qui l'intéressent.

## Décisions produit (validées par Vincent, 2026-09-15)

### 1. Emplacement

La complétion se fait depuis le Détail de l'Opportunité
(Opportunity Details), pas depuis une page ou une modale séparée.

Un tag/badge filtrable "Partial" est ajouté à la liste des
Opportunities, permettant d'afficher uniquement les offres
incomplètes (celles nécessitant une complétion manuelle).

### 2. Contenu à coller

Le champ couvre la totalité de la section LinkedIn
"À propos de l'offre d'emploi" (texte libre, y compris puces et
sauts de ligne). Aucune extraction/segmentation automatique du texte
collé (pas de séparation manuelle title/contract_type/skills à ce
stade) : c'est un remplissage brut du champ description.

Confirmé visuellement par Vincent (capture d'écran LinkedIn réelle,
offre "Architecte Solutions E-commerce (F/H)" chez DECADE,
2026-09-15) : le contenu à copier est structuré avec des sous-titres
en gras et des listes à puces multi-niveaux. Le champ de stockage
doit rester du texte libre sans mise en forme forcée.

### 3. Effet sur le calcul de matching

Tant qu'une offre reste PARTIAL, aucun calcul de matching n'est
effectué pour cette offre (score non calculé, pas de valeur
affichée ou une valeur explicitement "non disponible").

Une fois l'offre complétée (description ajoutée), le calcul de
matching redevient possible pour cette offre - déclenché soit
manuellement (à la demande, ex: prochaine consultation de l'offre),
soit par un processus planifié existant, selon ce que l'audit
technique révèle sur le mode de calcul actuel (calcul à la volée
vs valeur persistée).

Point à vérifier impérativement lors de l'audit avant implémentation
(voir section Repository Audit ci-dessous) : le moteur de matching
actuel (calculate_profile_scores_for_job_offer(), DEC-083) semble
calculer le score à la demande à chaque appel API, sans persistance
d'un score stocké. Si c'est confirmé, "calcul après complétion,
manuel ou planifié" se traduit simplement par : le endpoint de
matching doit court-circuiter/refuser le calcul si
quality_level == PARTIAL, et fonctionner normalement dès que
quality_level change - sans mécanisme de planification dédié à
construire. Cette hypothèse doit être confirmée, pas supposée.

### 4. Contrat API (recommandation Copilot, validée par Vincent)

Nouvel endpoint dédié et étroit, plutôt qu'une extension d'un
endpoint générique de mise à jour de JobOffer.

Nom provisoire (à confirmer lors de l'audit du router jobs/
existant) :

PATCH /job-offers/{id}/complete-description

Requête :
{
"description": "<texte collé depuis LinkedIn>"
}

Comportement :

- accepte uniquement le champ description (aucun autre champ de
  JobOffer n'est modifiable via cet endpoint)
- met à jour quality_level (valeur exacte de l'enum à confirmer lors
  de l'audit - PARTIAL -> FULL ou équivalent)
- authentifié (cohérent avec le reste de l'API, même si JobOffer
  reste un catalogue global par conception - DEC-081)
- rejette la requête si l'offre n'existe pas (404) ou si elle n'est
  pas PARTIAL (comportement exact à définir : erreur explicite,
  ou no-op silencieux si déjà complète - à trancher lors du design
  technique détaillé)

## Hors périmètre (JOBS-001)

- extraction automatique de contract_type ou skills depuis le texte
  collé (reste un champ description brut uniquement)
- édition d'autres champs de l'offre (titre, entreprise, ville,
  mode de travail) via ce workflow
- application de cette complétion manuelle à d'autres sources que
  LinkedIn Email (France Travail, Greenhouse ont déjà des
  descriptions complètes par construction)
- planification automatique périodique du recalcul de matching
  (sauf si l'audit révèle que ce mécanisme existe déjà et doit
  simplement être étendu)

## Prochaine étape

7.1.31.1 Repository Audit, avant toute implémentation, devant
confirmer :

- structure réelle actuelle du router app/jobs/ (nom des fichiers,
  endpoints déjà existants pour JobOffer)
- valeurs exactes de l'enum quality_level (nom du champ, valeurs
  possibles - PARTIAL/FULL/MINIMAL ou autres)
- mode de calcul réel du matching (à la volée vs persisté) pour
  trancher le point 3 ci-dessus
- présence ou absence d'un endpoint de filtrage existant sur
  OpportunitiesPage pouvant accueillir le nouveau filtre "Partial"
- format exact retourné par l'API pour quality_level (déjà exposé
  au frontend ou non)

## Related Decisions

- DEC-086 - LinkedIn Email Connector Replaces API/Scraping Approach
- DEC-039 - Explainable Opportunity Scoring
- DEC-081 - User Data Ownership And Isolation (JobOffer reste
  global)

## Design technique détaillé (post-audit, 2026-09-15)

### Constat d'audit majeur

JobOfferResponse (app/jobs/schemas.py) n'expose actuellement que :
id, title, company_name, location, source, source_url, description,
created_at. Aucun des champs ajoutés au modèle depuis la Phase 3
(city, region, work_mode, contract_type, quality_level, status, etc.)
n'est exposé au frontend. Ce n'est pas un défaut introduit par
JOBS-001, mais un écart de schéma préexistant, découvert en auditant
ce fichier pour JOBS-001. Puisque ce fichier doit de toute façon être
modifié, quality_level y est ajouté dans le cadre de cette phase,
sans élargir davantage le scope (city/region/work_mode restent hors
périmètre, non nécessaires ici).

### Valeur retenue pour "offre complète"

quality_level passe de "PARTIAL" à "COMPLETE" (valeur choisie plutôt
que "FULL", pour éviter toute ambiguïté avec une notion de temps
plein). Reste un champ String(20) libre, pas un enum Python - cohérent
avec l'implémentation actuelle, aucun changement de type de colonne.

### Backend

#### 1. app/jobs/schemas.py

JobOfferResponse enrichi avec :
quality_level: str
description: str (déjà présent)

Nouveau schéma d'entrée :
class JobOfferDescriptionUpdate(BaseModel):
description: str

#### 2. app/jobs/router.py

Nouvel endpoint :

    @router.patch(
        "/job-offers/{job_offer_id}/complete-description",
        response_model=JobOfferResponse,
    )
    def complete_job_offer_description(
        job_offer_id: int,
        payload: JobOfferDescriptionUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        job_offer = db.query(JobOffer).filter(
            JobOffer.id == job_offer_id
        ).first()

        if job_offer is None:
            raise HTTPException(
                status_code=404,
                detail="Job offer not found.",
            )

        job_offer.description = payload.description
        job_offer.description_raw = payload.description
        job_offer.quality_level = "COMPLETE"

        db.commit()
        db.refresh(job_offer)

        return job_offer

Authentifié (current_user requis), cohérent avec le endpoint cleanup
existant, même si JobOffer reste un catalogue global (DEC-081) - la
modification d'une donnée partagée justifie une authentification,
contrairement à sa simple lecture.

Aucune validation de contenu du texte collé n'est appliquée (accepté
tel quel, y compris avec puces/sauts de ligne - cohérent avec la
décision produit "remplissage brut").

#### 3. app/matching/service.py

calculate_matching_result() modifiée pour retourner un résultat
explicite "non calculable" si job_offer.quality_level == "PARTIAL",
avant tout calcul de score. Approche technique exacte (nouveau champ
optionnel sur MatchingResult, ex. is_calculable: bool, ou exception
métier dédiée gérée par le router) à trancher lors de l'implémentation,
pas dans ce document de design - dépend de la structure exacte de
MatchingResult (app/matching/schemas.py, non encore audité à ce
stade).

Ce comportement remplace le 0.0 silencieux actuellement retourné par
calculate_skills_score() quand job_offer_skill_ids est vide (déjà le
cas pour toutes les offres LinkedIn Email aujourd'hui) : au lieu d'un
score trompeur, un signal explicite "offre incomplète, complétez-la
avant de voir un score" doit être retourné.

Aucune modification de calculate_profile_scores_for_job_offer() n'est
anticipée au-delà de la propagation du même comportement (à confirmer
lors de l'implémentation, car cette fonction appelle
calculate_matching_result() en boucle pour chaque profil).

### Frontend

#### 1. Type JobOffer (à localiser dans services/api.ts)

Ajout du champ quality_level: string au type existant (nom exact du
type à confirmer - non trouvé lors de cet audit, recherche limitée à
JobOffer/quality_level/getJobOffers).

#### 2. Nouvelle fonction API

    export async function completeJobOfferDescription(
        jobOfferId: number,
        description: string,
    ) {
        const response = await fetch(
            `${API_BASE_URL}/job-offers/${jobOfferId}/complete-description`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    ...getAuthHeaders(),
                },
                body: JSON.stringify({ description }),
            },
        );

        if (!response.ok) {
            throw new Error("Unable to complete job offer description.");
        }

        return response.json();
    }

#### 3. OpportunitiesPage.tsx - nouveau filtre

Suit exactement le pattern existant (applicationFilter, sourceFilter,
locationFilter) :

    const [qualityFilter, setQualityFilter] = useState("ALL");

    const matchesQuality =
        qualityFilter === "ALL"
            ? true
            : offer.quality_level === qualityFilter;

Intégré dans filteredOffers, hasActiveFilters, reset filters, et
potentiellement dans le résumé de recherche (getSearchSummary) et les
Saved Searches, en cohérence avec les 3 filtres déjà en place.

Valeurs du select : "ALL" / "PARTIAL" (affiché "Partial" ou
"Incomplete") / "COMPLETE".

#### 4. Détail de l'Opportunité (composant exact non encore audité)

Zone de saisie (textarea) visible uniquement quand
quality_level === "PARTIAL", avec bouton de soumission appelant
completeJobOfferDescription(). Une fois complétée, rafraîchissement
de l'offre affichée (quality_level devient "COMPLETE", le score de
matching redevient calculable au prochain appel).

Composant exact à identifier lors de l'implémentation (probablement
dans OpportunitiesPage.tsx directement, ou un composant dédié type
OpportunityDetailPanel - non confirmé par cet audit).

### Points restant à auditer avant l'implémentation (non bloquants pour valider ce design)

- app/matching/schemas.py (structure de MatchingResult, pour décider
  comment représenter "non calculable")
- nom exact du type TypeScript JobOffer et du composant de détail
  d'opportunité côté frontend
- tests existants sur calculate_matching_result() et
  calculate_skills_score(), pour évaluer l'impact de régression du
  changement de comportement sur les offres à quality_level PARTIAL
  déjà en base (136 offres LinkedIn concernées)

## Prochaine étape

7.1.31.2 Backend Implementation, après validation de ce design par
Vincent.

### Représentation "non calculable" (post-audit app/matching/schemas.py)

MatchingResult, RankedJobOffer et ProfileOpportunityScore ont
actuellement tous leurs champs obligatoires (aucun Optional). Plutôt
que de restructurer ces 3 schémas en profondeur, un champ unique est
ajouté aux 3 :

    is_calculable: bool = True

Propagé aux 3 schémas car rank_job_offers_for_profile() et
calculate_profile_scores_for_job_offer() appellent tous deux
calculate_matching_result() en boucle - laisser un score affiché dans
le classement ou la comparaison multi-profils pendant qu'il est
bloqué dans le détail créerait une incohérence contraire à DEC-039.

Quand is_calculable = False (job_offer.quality_level == "PARTIAL") :

- tous les scores numériques (\*\_score) = 0.0 (valeur neutre, jamais
  affichée comme un vrai résultat grâce au flag is_calculable)
- matching_skills, missing_skills, strengths, weaknesses = listes
  vides
- explanations = liste contenant une seule ScoreExplanation
  (criterion="completeness", message expliquant que l'offre doit
  être complétée avant tout calcul)
- opportunity_analysis = OpportunityAnalysis(
  verdict="incomplete",
  recommendation="complete_description",
  summary="This offer is missing a description and cannot be
  scored yet. Complete it manually to enable matching."
  )

calculate_matching_result() vérifie job_offer.quality_level en tout
début de fonction, avant tout calcul de score, et retourne
immédiatement ce résultat neutre si PARTIAL - sans toucher aux
fonctions de calcul existantes (calculate_skills_score(), etc.),
qui restent inchangées et ne sont simplement pas appelées dans ce cas.

Le frontend utilise is_calculable pour :

- masquer le score / afficher un badge "Not scored yet" au lieu d'un
  pourcentage, partout où un score est affiché (Opportunity Details,
  cartes, classement, tableau de comparaison multi-profils)
- afficher le formulaire de complétion manuelle dans Opportunity
  Details quand is_calculable est false

## Design finalisé, prêt pour implémentation

Décisions actées :

1. quality_level: "PARTIAL" -> "COMPLETE" (Vincent, 2026-09-15)
2. is_calculable: bool ajouté à MatchingResult, RankedJobOffer,
   ProfileOpportunityScore (Copilot, validé implicitement par
   l'absence d'objection sur l'approche technique)

Prochaine étape : 7.1.31.2 Backend Implementation.
