# Greenhouse Connector Design

## Objective

Add Greenhouse as the second real job source of Career Operating System after France Travail.

The objective is to validate:

- multi-jobboard architecture;
- multi-source discovery;
- normalized offer ingestion;
- source-independent matching;
- source-independent ranking;
- source-independent opportunity analysis.

No frontend change is required during this phase.

The connector must integrate into the existing Job Discovery architecture.

---

## Scope

### Included

- GreenhouseConnector
- Greenhouse API integration
- Greenhouse → RawOffer mapping
- ConnectorRegistry integration
- automated tests

### Excluded

- frontend changes
- ranking changes
- matching changes
- scoring changes
- AI analysis changes
- multi-board support
- LinkedIn integration

---

## Greenhouse API Strategy

### Decision

Use the official Greenhouse Job Board API.

### Rationale

Validated characteristics:

- official API
- public GET endpoints
- no authentication required
- SaaS compatible
- stable JSON contract
- compatible with existing ConnectorInterface

### Endpoint

GET

/v1/boards/{board_token}/jobs

Example board token:

sonymusiccareersfrance

The board token will be configurable.

---

## Settings

New settings:

GREENHOUSE_BOARD_TOKEN

Example:

GREENHOUSE_BOARD_TOKEN=sonymusiccareersfrance

Future multi-board support is intentionally out of scope.

MVP supports a single board token.

---

## Connector Responsibilities

GreenhouseConnector must:

- call the Greenhouse API;
- retrieve published jobs;
- map jobs to RawOffer;
- return a list[RawOffer];
- never write into the database;
- never perform normalization;
- never perform matching;
- never perform ranking.

These responsibilities remain in the existing services.

---

## Expected Mapping

Greenhouse job

↓

RawOffer

### Source

source_name

Greenhouse

### Source Job Id

job.id

↓

source_job_id

### Source URL

job.absolute_url

↓

source_url

### Title

job.title

↓

title

### Company

job.company_name

↓

company

### City

job.location.name

↓

city

### Country

Unknown

No country is currently provided by the observed payload.

### Description

Detailed endpoint may be required.

If unavailable:

raw_description=""

The initial objective is successful import.

### Publication Date

job.first_published

↓

published_at_raw

### Payload

Complete Greenhouse job object

↓

raw_payload

---

## Error Handling

Connector must return:

[]

when:

- API returns an error;
- Greenhouse board does not exist;
- timeout occurs;
- payload is invalid.

This follows the current connector strategy.

---

## Connector Registry Integration

Register:

greenhouse

inside ConnectorRegistry.

Expected usage:

DiscoveryService

↓

ConnectorRegistry

↓

GreenhouseConnector

↓

RawOffer

---

## Discovery Service

No modification required.

Current architecture already supports additional connectors.

---

## Tests

Create:

backend/tests/test_greenhouse_connector.py

Required tests:

### Test 1

Connector returns list[RawOffer]

### Test 2

Greenhouse payload correctly maps to RawOffer

### Test 3

Invalid payload returns empty list

### Test 4

HTTP errors return empty list

### Test 5

Source name equals Greenhouse

---

## Validation Criteria

Phase is considered completed when:

- connector exists;
- connector registered;
- tests pass;
- Greenhouse data imports successfully;
- offers appear in PostgreSQL;
- offers are accessible through existing APIs.

Frontend validation belongs to the next phase.

---

## Out of Scope

- LinkedIn
- WTJ
- multi-board support
- AI recommendations
- job source prioritization
- advanced metadata enrichment

These topics belong to future phases.

---

## Expected Deliverables

backend/app/
