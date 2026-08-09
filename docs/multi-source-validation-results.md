# Multi-Source Validation Results

## Phase

6.1.8 Multi-Source Validation

## Statut

Validated with reservations

## Date de validation

2026-08-09

## Objectif

Valider le fonctionnement simultané des connecteurs supportés par le pipeline Job Discovery.

La validation couvre :

- ConnectorRegistry
- DiscoveryScheduler
- DiscoveryService
- NormalizationService
- JobOfferRepository
- PostgreSQL
- FastAPI
- Frontend Opportunities
- déduplication fonctionnelle

Aucune nouvelle source n'a été ajoutée pendant cette phase.

Aucune fonctionnalité IA n'a été ajoutée pendant cette phase.

Aucune modification du moteur de matching n'a été réalisée pendant cette phase.

---

## Sources concernées

Sources attendues :

- France Travail
- LinkedIn
- Greenhouse

Sources techniques exclues de la validation métier :

- mock

---

## Résumé exécutif

La validation multi-source confirme que Career Operating System peut afficher et exploiter des offres provenant de plusieurs sources dans un même catalogue d'opportunités.

Les données exposées par l'API montrent trois sources présentes :

- France Travail
- LinkedIn
- Greenhouse

La synchronisation multi-source via DiscoveryScheduler a été exécutée avec trois connecteurs :

- france_travail
- linkedin
- greenhouse

Résultat global du scheduler :

- connecteurs traités : 3
- offres récupérées : 67
- offres importées : 67

Résultat API après synchronisation :

- France Travail : 133 offres
- Greenhouse : 16 offres
- LinkedIn : 2 offres

La phase valide le fonctionnement multi-source global du système avec une réserve importante : le connecteur LinkedIn est bien enregistré et exécuté, mais il ne retourne actuellement aucune offre lors de la synchronisation.

---

## Validation 1 - ConnectorRegistry

### Objectif

Vérifier que les connecteurs attendus sont enregistrés dans le registre central.

### Résultat observé

Le ConnectorRegistry contient les connecteurs suivants :

- mock
- france_travail
- linkedin
- greenhouse

### Conclusion

Validé.

Le système connaît les connecteurs nécessaires à la validation multi-source.

---

## Validation 2 - Configuration

### Objectif

Vérifier que les connecteurs nécessaires sont configurables.

### Résultat observé

Les paramètres suivants sont présents dans la configuration locale :

- DISCOVERY_ENABLED
- DISCOVERY_INTERVAL_MINUTES
- DISCOVERY_CONNECTORS
- GREENHOUSE_BOARD_TOKEN
- GREENHOUSE_API_URL
- GREENHOUSE_TIMEOUT
- LINKEDIN_API_URL
- LINKEDIN_ACCESS_TOKEN
- FRANCE_TRAVAIL_API_URL
- FRANCE_TRAVAIL_TOKEN_URL

### Point d'attention

Le fichier local .env contient des secrets et ne doit jamais être copié dans le chat ou commité.

Les secrets France Travail exposés pendant la validation doivent être considérés comme compromis et doivent être renouvelés.

### Conclusion

Validé avec action de sécurité requise.

---

## Validation 3 - DiscoveryScheduler multi-source

### Objectif

Vérifier que le scheduler peut exécuter plusieurs connecteurs dans une même synchronisation.

### Commande exécutée

Depuis le dossier backend :

python -c "from app.jobs.scheduler import DiscoveryScheduler; scheduler = DiscoveryScheduler(enabled=True, connector_names=['france_travail','linkedin','greenhouse']); result = scheduler.run_once(); print(result)"

### Résultat observé

{
"connectors_processed": 3,
"offers_fetched": 67,
"offers_imported": 67,
"results": [
{
"connector_name": "france_travail",
"source_name": "France Travail",
"offers_fetched": 50,
"offers_imported": 50
},
{
"connector_name": "linkedin",
"source_name": "UNKNOWN",
"offers_fetched": 0,
"offers_imported": 0
},
{
"connector_name": "greenhouse",
"source_name": "Greenhouse",
"offers_fetched": 17,
"offers_imported": 17
}
]
}

### Analyse

Le scheduler a bien exécuté trois connecteurs.

France Travail a retourné :

- 50 offres récupérées
- 50 offres importées

Greenhouse a retourné :

- 17 offres récupérées
- 17 offres importées

LinkedIn a retourné :

- 0 offre récupérée
- 0 offre importée

Le connecteur LinkedIn est donc exécuté, mais il n'est pas opérationnel en collecte réelle au moment de cette validation.

### Conclusion

Validé avec réserve LinkedIn.

---

## Validation 4 - PostgreSQL

### Objectif

Vérifier que les offres multi-sources sont persistées dans PostgreSQL.

### Résultat observé

Les logs SQL montrent des opérations sur :

- job_offers
- job_sources
- job_offer_sources

Les opérations observées incluent :

- SELECT sur job_offers
- SELECT sur job_sources
- INSERT INTO job_offers
- INSERT INTO job_offer_sources
- UPDATE sur job_offers
- COMMIT

Les sources observées dans les logs incluent :

- France Travail
- Greenhouse

### Conclusion

Validé.

Le pipeline Connector → DiscoveryService → Repository → PostgreSQL fonctionne avec plusieurs sources.

---

## Validation 5 - API FastAPI

### Objectif

Vérifier que les offres multi-sources sont accessibles via l'API.

### Commande correcte

$offers = Invoke-RestMethod http://localhost:8000/job-offers

$offers | Group-Object source | Select-Object Name,Count

### Résultat observé

Name Count
Greenhouse 16
LinkedIn 2
France Travail 133

### Conclusion

Validé.

L'API expose bien des offres provenant de plusieurs sources.

---

## Validation 6 - Endpoint erroné

### Commande testée

curl http://localhost:8000/api/job-offers

### Résultat observé

{"detail":"Not Found"}

### Conclusion

L'endpoint /api/job-offers n'existe pas.

L'endpoint valide observé pendant la validation est :

http://localhost:8000/job-offers

Aucune correction backend n'est requise à ce stade si le frontend consomme déjà le bon endpoint.

---

## Validation 7 - Frontend Opportunities

### Objectif

Vérifier que les sources sont visibles dans le frontend.

### Résultat observé précédemment

Le frontend Opportunities affiche les offres Greenhouse avec :

- Source = Greenhouse
- Company = Sony Music Entertainment France
- détails de l'offre visibles
- lien source disponible

La validation API montre également que les sources France Travail, LinkedIn et Greenhouse sont disponibles dans les données consommables par le frontend.

### Conclusion

Validé.

Le frontend est compatible avec l'affichage multi-source.

---

## Validation 8 - Déduplication fonctionnelle

### Objectif

Vérifier qu'une nouvelle synchronisation ne provoque pas une création massive de doublons.

### Résultat observé

Après synchronisation multi-source, la répartition API est :

- Greenhouse : 16
- LinkedIn : 2
- France Travail : 133

Les logs montrent des opérations :

- SELECT avant insertion
- UPDATE sur certaines offres existantes
- INSERT uniquement lorsque nécessaire

### Analyse

Le comportement observé indique que le système recherche les offres existantes avant insertion.

Greenhouse reste stable à 16 offres visibles dans l'API malgré plusieurs passages.

LinkedIn reste stable à 2 offres visibles dans l'API.

France Travail augmente selon les imports effectués, mais aucune explosion artificielle de volume n'a été observée pendant cette validation.

### Conclusion

Déduplication validée fonctionnellement.

Limite :

Aucun test automatisé dédié à la déduplication multi-source n'a été ajouté dans cette phase.

---

## Validation 9 - Tests backend

### Objectif

Vérifier que l'intégration multi-source ne crée pas de régression backend.

### Résultat observé

Suite backend complète :

- 87 tests collectés
- 87 tests passants

### Conclusion

Validé.

Aucune régression backend détectée.

---

## Écart identifié - LinkedIn

### Fait observé

L'API retourne actuellement :

- LinkedIn : 2 offres

Mais le scheduler retourne :

- linkedin
- source_name = UNKNOWN
- offers_fetched = 0
- offers_imported = 0

### Interprétation

Le connecteur LinkedIn est bien enregistré et exécuté.

Cependant, la collecte LinkedIn ne retourne actuellement aucune offre.

Les deux offres LinkedIn visibles dans l'API semblent donc être des données historiques ou issues d'une validation précédente.

### Conclusion

LinkedIn ne bloque pas la validation multi-source globale, mais doit rester sous réserve.

Une investigation dédiée sera nécessaire avant de considérer LinkedIn comme une source réellement opérationnelle.

---

## Écart identifié - Sécurité

### Fait observé

Le fichier .env a été copié dans le chat pendant la validation.

Il contenait des identifiants France Travail.

### Risque

Les secrets exposés doivent être considérés comme compromis.

### Action requise

Renouveler le secret France Travail côté portail développeur.

Mettre à jour le fichier local :

backend/.env

Ne jamais commiter ce fichier.

Ne jamais recopier les secrets dans le chat.

Pour les prochaines validations, utiliser uniquement une version masquée :

FRANCE_TRAVAIL_CLIENT_ID=**_
FRANCE_TRAVAIL_CLIENT_SECRET=_**

---

## Décision de validation

La phase 6.1.8 Multi-Source Validation est considérée comme validée avec réserves.

### Validé

- ConnectorRegistry multi-source
- DiscoveryScheduler multi-source
- DiscoveryService multi-source
- PostgreSQL
- API /job-offers
- Frontend Opportunities
- coexistence de plusieurs sources
- tests backend passants
- déduplication fonctionnelle

### Réserves

- LinkedIn ne retourne actuellement aucune offre au moment de la synchronisation
- les secrets France Travail doivent être renouvelés
- la déduplication multi-source n'est pas encore couverte par un test automatisé dédié

---

## Résultat final

Sources visibles via API :

- France Travail : 133 offres
- Greenhouse : 16 offres
- LinkedIn : 2 offres

Résultat scheduler :

- France Travail : 50 offres récupérées, 50 importées
- LinkedIn : 0 offre récupérée, 0 importée
- Greenhouse : 17 offres récupérées, 17 importées

Tests backend :

- 87 tests passants

Conclusion :

Career Operating System supporte désormais un fonctionnement multi-source exploitable.

La plateforme peut afficher et gérer des opportunités provenant de plusieurs sources dans un catalogue unifié.

---

## Prochaines étapes recommandées

### Étape immédiate

Renouveler le secret France Travail.

### Étape documentaire

Synchroniser :

- docs/project-status.md
- docs/roadmap.md
- docs/handoff-prompt.md

avec la clôture de la phase 6.1.8.

### Étape produit suivante

Phase 7.0

AI Explanation Layer

Cette phase ne doit démarrer qu'après :

- renouvellement du secret France Travail ;
- commit documentaire de clôture 6.1.8 ;
- git status propre.

---

## Statut de clôture

Phase 6.1.8 Multi-Source Validation

Status:

Validated with reservations
