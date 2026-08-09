# LinkedIn Connector Backend Design

## Document Information

Project:
Career Operating System

Phase:
6.1.2 LinkedIn Connector Backend

Status:
Technical Design

Prerequisite:
Phase 6.1.1 LinkedIn Connector Design completed.

Purpose:
Define the backend implementation strategy for the LinkedIn connector while preserving the existing Job Discovery architecture.

Scope:
Backend implementation only.

Out of Scope:

- Frontend visualization
- End-to-end validation
- AI features
- Opportunity Analysis
- Matching logic changes

---

## Objective

Implement a LinkedInConnector compatible with the current ConnectorInterface contract.

The implementation must integrate into the existing Discovery pipeline without requiring modifications to:

- DiscoveryService
- NormalizationService
- JobOfferRepository
- Matching Engine
- Opportunity Ranking
- Opportunity Analysis

The connector must only produce RawOffer objects.

Existing architecture must remain unchanged.

Reference architecture:
ConnectorInterface
→ RawOffer
→ NormalizationService
→ NormalizedJobOffer
→ DiscoveryService
→ JobOfferRepository
→ Database

This pipeline already exists and is validated.

---

## Current Architecture

Current connectors:

- MockSourceConnector
- FranceTravailConnector

Registered sources:

- mock
- france_travail

Connector registration currently relies on ConnectorRegistry.

Target state:

- mock
- france_travail
- linkedin

No DiscoveryService modification required.

DiscoveryService already supports multiple connectors through ConnectorRegistry.

---

## Files To Create

backend/app/jobs/connectors/linkedin_connector.py

backend/tests/test_linkedin_connector.py

---

## Files To Modify

backend/app/core/settings.py

backend/app/jobs/connectors/connector_registry.py

---

## Connector Structure

Class:

LinkedInConnector

Inheritance:

ConnectorInterface

Constant:

SOURCE_NAME = "LinkedIn"

Public methods:

fetch_job_offers()

Private methods:

\_map_offer_to_raw_offer()

\_extract_source_url()

Potential future methods:

fetch_access_token()

build_search_payload()

validate_response()

Only fetch_job_offers() is mandatory for this phase.

Connector must remain simple.

---

## Settings Configuration

New settings expected:

LINKEDIN_CLIENT_ID

LINKEDIN_CLIENT_SECRET

LINKEDIN_API_URL

LINKEDIN_TIMEOUT

Example structure:

LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET
LINKEDIN_API_URL
LINKEDIN_TIMEOUT

Configuration pattern must reuse the same strategy already implemented for France Travail.

No credentials must be hardcoded.

Credentials must remain exclusively in .env.

---

## ConnectorRegistry Integration

Current state:

{
"mock": MockSourceConnector,
"france_travail": FranceTravailConnector,
}

Target state:

{
"mock": MockSourceConnector,
"france_travail": FranceTravailConnector,
"linkedin": LinkedInConnector,
}

No further Registry change required.

---

## RawOffer Mapping Strategy

Output type:

list[RawOffer]

Mandatory fields:

source_name
source_job_id

title

raw_description

retrieved_at

Recommended fields:

company
city
country
source_url
work_mode_raw
contract_type_raw
salary_raw
published_at_raw
language_raw

The contract must remain fully compatible with RawOffer.

---

## Mapping Example

Incoming LinkedIn payload

{
"id": "123456",
"title": "Technical Partnerships Manager",
"company": "Example Company",
"location": "Paris",
"url": "...",
"description": "...",
"published_at": "...",
}

Produces

RawOffer(
source_name="LinkedIn",
source_job_id="123456",
source_url="...",
title="Technical Partnerships Manager",
company="Example Company",
raw_description="...",
city="Paris",
country="France",
retrieved_at=...
)

This follows the same pattern used by FranceTravailConnector.

---

## Error Handling Strategy

DiscoveryService must never fail because one connector fails.

Expected behavior:

Connector Exception
↓
Handled by connector
↓
Empty list returned
↓
DiscoveryService continues

Target outcome:

Source Failure
≠
Global Discovery Failure

The multi-source architecture is already based on connector isolation.

---

## Logging Strategy

Errors should be logged.

Examples:

Authentication failure

Rate limit

Unexpected response structure

Network timeout

No business decision should be based on logs.

Logs are operational only.

---

## DiscoveryService Compatibility

No change required.

Current DiscoveryService flow:

Connector
↓
fetch_job_offers()
↓
RawOffer
↓
NormalizationService
↓
JobOfferRepository

LinkedInConnector must simply conform to ConnectorInterface.

---

## Test Strategy

New test file:

backend/tests/test_linkedin_connector.py

Tests required:

test_linkedin_connector_implements_interface

test_fetch_job_offers_returns_raw_offers

test_linkedin_offer_maps_to_rawoffer

test_empty_response_returns_empty_list

test_connector_handles_invalid_response

Target philosophy:

Mock external calls.

No real LinkedIn dependency.

Test structure should mirror FranceTravailConnector tests.

---

## Acceptance Criteria

Phase 6.1.2 is complete when:

- LinkedInConnector exists
- ConnectorInterface implemented
- Settings integrated
- ConnectorRegistry integrated
- RawOffer mapping implemented
- Unit tests created
- Existing tests remain green
- New tests pass

Not required:

- Frontend changes
- Source visualization
- End-to-end validation

Those belong to later phases:

6.1.3 Source Visualization Frontend

6.1.4 End-to-End Validation

according to the roadmap. 【1-0946e3】

---

## Risks

Risk:
LinkedIn response format changes

Mitigation:
Dedicated mapping layer

Risk:
Authentication changes

Mitigation:
Centralized settings

Risk:
Rate limiting

Mitigation:
Connector isolation

Risk:
Partial data

Mitigation:
NormalizationService remains responsible for normalization

---

## Deliverables

Files created:

backend/app/jobs/connectors/linkedin_connector.py

backend/tests/test_linkedin_connector.py

Files modified:

backend/app/core/settings.py

backend/app/jobs/connectors/connector_registry.py

Expected result:

A backend LinkedIn connector fully integrated into the existing multi-source architecture without impacting DiscoveryService, Matching Engine, Opportunity Ranking or Opportunity Analysis.

---

## Next Planned Phase

6.1.3 Source Visualization Frontend

Objectives:

- Display source information
- Display LinkedIn-origin opportunities
- Visual validation
- User verification

No backend changes expected during that phase.
