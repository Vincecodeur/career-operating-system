# LinkedIn Connector Design

## Document Information

Project:
Career Operating System

Phase:
6.1.1 LinkedIn Connector Design

Status:
Design

Purpose:
Define the target architecture for integrating LinkedIn into the Job Discovery pipeline.

Scope:
Architecture and design only.

Out of Scope:

- Implementation
- API integration
- Scraping implementation
- Authentication implementation
- Frontend development
- Automated tests

---

## Objective

Add LinkedIn as the primary Job Discovery source for the MVP.

The LinkedIn connector must integrate into the existing Discovery pipeline without introducing specific logic into the Matching Engine, Ranking Engine or Opportunity Analysis components.

The connector must only be responsible for retrieving opportunities and transforming them into the standardized RawOffer format.

---

## Current Architecture

Current Job Discovery flow:

External Source
↓
Connector
↓
RawOffer
↓
NormalizationService
↓
NormalizedJobOffer
↓
DiscoveryService
↓
JobOfferRepository
↓
JobOffer
↓
Matching Engine
↓
Opportunity Ranking
↓
Opportunity Analysis
↓
Frontend

The LinkedIn connector must reuse this pipeline without modification.

---

## Existing Connector Model

Current connector contract:

ConnectorInterface
↓
fetch_job_offers()
↓
list[RawOffer]

All connectors must implement the same interface.

The DiscoveryService must not need to know the implementation details of each source.

This principle must remain unchanged.

---

## LinkedIn Positioning

Role:
Primary Job Discovery source

Priority:
Critical

Market:
France

Target Profiles:

- Integration Architect
- Partner Integration Manager
- Technical Partnerships Manager
- Strategic Partnerships Manager
- Partner Solutions Architect
- Partner Success Manager
- Technology Partnerships Manager
- Channel Partnerships Manager
- Alliance Manager
- Ecosystem Manager

Expected Benefits:

- Higher concentration of target opportunities
- Better coverage of partnership and integration positions
- Better quality descriptions
- Better coverage of senior opportunities

---

## API First Strategy

Project Rule:

API First

Preferred order:

1. Official API
2. Official partner integration
3. Approved documented data source
4. Limited scraping fallback

The connector design must preserve this order.

---

## LinkedIn Constraints

Known Constraints:

- LinkedIn is the primary source targeted by the MVP.
- Access conditions may differ depending on program eligibility.
- API availability must be validated before implementation.
- Rate limits must be evaluated before implementation.
- Authentication requirements must be evaluated before implementation.

If a suitable API cannot be used for the MVP, the project documentation already allows a limited fallback strategy specifically for LinkedIn.

No implementation decision is taken during this phase.

---

## Connector Responsibilities

The LinkedIn connector must:

- retrieve opportunities
- identify the source
- preserve the source URL
- preserve the publication date
- preserve the raw description
- preserve source metadata
- transform data into RawOffer

The connector must not:

- calculate matching scores
- calculate rankings
- perform opportunity analysis
- apply business scoring rules
- deduplicate opportunities

These responsibilities belong to existing backend services.

---

## RawOffer Mapping Strategy

Minimum fields expected:

source_name
source_job_id
source_url

title

company

raw_description

city
region
country

contract_type_raw

work_mode_raw

salary_raw

published_at_raw

language_raw

retrieved_at

raw_payload

The mapping philosophy must remain identical to the France Travail connector.

---

## Search Criteria Compatibility

The connector must support the existing search strategy.

Target country:
France

Target area:
Paris + 10 km

Preferred work mode:
Hybrid

Accepted work modes:

- Remote
- Hybrid
- Onsite

Priority keywords:

- Integration
- Architect
- API
- Ecommerce

Excluded keywords:

- Stage
- Intern
- Freelance

The connector must provide sufficient raw data for these rules to be applied later by the existing services.

The connector itself must not enforce these rules.

This responsibility belongs to discovery, normalization and matching layers.

Relevant search criteria are already documented in the project. 【1-ea4224】

---

## Deduplication Strategy

Current project decision:

Keep the most complete version of a duplicated offer.

Example:

LinkedIn

- title
- company
- description
- work mode

France Travail

- title
- company
- short description

Result:
Keep LinkedIn version if it contains more useful information.

The LinkedIn connector must not contain deduplication logic.

---

## Error Handling Strategy

Connector failures must not stop Job Discovery.

Expected behavior:

LinkedIn Failure
↓
Log Error
↓
Return Empty Result
↓
Continue Discovery Pipeline

Benefits:

- resilient synchronization
- independent source management
- simplified troubleshooting

---

## Security Strategy

Credentials must never be hardcoded.

Credentials must be stored in:

.env

Settings management must follow the same pattern already used for France Travail.

No secrets must be committed to Git.

---

## Extensibility Strategy

The connector architecture must remain source-agnostic.

Future sources may include:

- Indeed
- Glassdoor
- Welcome To The Jungle
- Greenhouse
- Lever
- Ashby
- Workday
- SmartRecruiters

The LinkedIn connector must not introduce source-specific assumptions into shared services.

---

## Success Criteria

Phase 6.1.1 will be considered complete when:

- LinkedIn architecture is documented
- Connector responsibilities are defined
- API First strategy is documented
- Fallback strategy is documented
- RawOffer mapping strategy is documented
- Integration points are documented
- Security requirements are documented
- Extensibility requirements are documented

No code is expected during this phase.

---

## Risks

Risk:
Official access unavailable

Mitigation:
Fallback strategy evaluation

Risk:
Rate limiting

Mitigation:
Daily synchronization strategy

Risk:
Changes in source accessibility

Mitigation:
Connector isolation behind ConnectorInterface

Risk:
Source-specific data quality differences

Mitigation:
NormalizationService remains the single normalization layer

---

## Deliverables

Phase Deliverable:

docs/linkedin-connector-design.md

Result:

A documented architecture ready for the future implementation phases while preserving the current Job Discovery design principles.

---

## Next Planned Phase

6.1.2 LinkedIn Connector Technical Design

Objectives:

- Define authentication strategy
- Define configuration model
- Define connector class structure
- Define error handling implementation
- Define testing strategy
- Define persistence integration strategy

No implementation yet.
