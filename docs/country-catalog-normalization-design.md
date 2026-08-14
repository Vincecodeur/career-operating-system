# Country Catalog Normalization Design

## Phase

7.1.16.16.3 Country Catalog Normalization Design

---

## Objective

Introduce a normalized Country Catalog used consistently across:

- candidate profiles;
- search preferences;
- opportunity locations;
- matching;
- reporting;
- future market intelligence.

The goal is to eliminate country naming inconsistencies and provide a standard geographic reference layer.

---

## Current Situation

The system currently does not have a dedicated country reference catalog.

Geographic information will become increasingly important for:

- candidate preferences;
- remote policies;
- relocation scenarios;
- opportunity filtering;
- geographic matching.

A dedicated catalog is required before these features are implemented.

---

## Problems To Solve

Examples:

United Kingdom
UK
Great Britain

France
FR

United States
USA
US
United States of America

Without normalization:

- filtering becomes unreliable;
- matching becomes inconsistent;
- analytics quality decreases;
- duplicate values appear.

---

## Design Principles

### Principle 1

One country = one canonical entry.

---

### Principle 2

All country references must point to a shared catalog.

---

### Principle 3

Country values must follow international standards.

---

### Principle 4

Human-readable labels remain available.

Users interact with country names.

The system stores standardized country codes.

---

## Recommended Country Model

Country

Fields:

id
iso_code
name

Example:

FR
France

GB
United Kingdom

PT
Portugal

ES
Spain

DE
Germany

US
United States

CA
Canada

---

## ISO Strategy

Recommendation:

ISO 3166-1 Alpha-2

Examples:

FR
GB
PT
ES
DE
US
CA

Benefits:

- international standard;
- interoperability;
- easier integrations;
- simpler filtering;
- future API compatibility.

---

## Profile Impact

Future profile preferences may reference:

Preferred Countries

Example:

France
United Kingdom
Portugal

Stored as:

FR
GB
PT

---

## Opportunity Impact

Job opportunities should progressively reference:

Country

instead of free-text geographic values.

Example:

Job Location

Country:

GB

City:

London

---

## Matching Impact

Future matching rules can compare:

Candidate Country Preferences

vs

Opportunity Country

using standardized values.

Example:

Candidate

Preferred Countries:

FR
GB

Opportunity:

GB

Result:

Country match.

---

## Search Criteria Impact

Future filters:

Country
Country Group
Region

Examples:

France

United Kingdom

Portugal

---

Filter implementation becomes deterministic.

---

## Country Groups

Future extension.

Examples:

EMEA
Europe
North America
South America
Middle East
Asia-Pacific

Not included in MVP.

---

## Remote Work Impact

Remote opportunities may still reference a country.

Examples:

Remote France

Remote United Kingdom

Remote Europe

A country catalog supports these scenarios.

---

## Relocation Scenarios

Future candidate preferences:

Relocation Allowed

Preferred Destinations

Countries become reference data.

---

## Analytics Impact

Potential future reports:

Most Frequent Countries

Most Demanded Countries

Country Distribution

Geographic Trends

Hiring Trends by Country

---

## Resolution Strategy

Imported data follows:

1. Exact Match
2. Normalized Match
3. Alias Match

Examples:

UK
United Kingdom

FR
France

USA
United States

↓

Canonical country entry.

---

## Country Alias Strategy

Future candidate:

CountryAlias

Fields:

id
country_id
alias

Example:

United Kingdom

Aliases:

UK
Britain
Great Britain

---

## Backend Impact

Future package:

backend/app/reference_data/

Potential entities:

Country
CountryAlias

Shared resolution services can reuse the existing reference-resolution strategy.

---

## Frontend Impact

Current:

No dedicated country selector.

Future:

Autocomplete selector

Controlled country list

No free-text country values

Shared component reused across:

- profile preferences;
- opportunity filters;
- settings.

---

## Seed Strategy

Catalog maintained in Git.

Example:

countries.json

Initial scope:

France
United Kingdom
Portugal
Spain
Germany
Italy
Netherlands
Belgium
Canada
United States

Additional countries may be added later.

---

## Example End-To-End Flow

Candidate Preference:

United Kingdom

↓

Resolution

↓

GB

↓

Stored In Database

↓

Used By Matching

↓

Used By Filters

↓

Used By Analytics

---

## Expected Outcome

The system gains:

- consistent geographic data;
- reliable filters;
- stronger matching;
- future relocation support;
- future reporting capabilities;
- reusable geographic reference data.

The Country Catalog becomes the geographic foundation of the Career Operating System.
