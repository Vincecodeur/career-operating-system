# Multi Profile Opportunity Context - Backend Tests Design

## Phase

7.1.22.5 Backend Tests

## Status

Design

---

# Goal

Define the backend validation scenarios required for the Multi Profile Opportunity Context.

The objective is to verify:

- OpportunityContext integrity;
- Primary Profile rules;
- Active Profiles rules;
- ranking compatibility;
- application workflow compatibility;
- backward compatibility with the existing single-profile model.

No test implementation is performed during this phase.

---

# Scope

Covered:

- context validation
- profile selection rules
- active profile rules
- ranking rules
- application creation rules

Not covered:

- frontend behavior
- UI state
- visual rendering
- persistence
- profile selector UX

---

# Test Categories

## Context Validation

### TEST-CTX-001

Primary Profile is required.

Input:

```json
{
  "active_profile_ids": [12]
}
```

Expected:

```text
Validation error
```

---

### TEST-CTX-002

At least one active profile is required.

Input:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": []
}
```

Expected:

```text
Validation error
```

---

### TEST-CTX-003

Primary Profile must belong to Active Profiles.

Input:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [17, 22]
}
```

Expected:

```text
Validation error
```

---

### TEST-CTX-004

Duplicate active profile identifiers are rejected.

Input:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 17]
}
```

Expected:

```text
Validation error
```

---

### TEST-CTX-005

Unknown Primary Profile is rejected.

Expected:

```text
Validation error
```

---

### TEST-CTX-006

Unknown Active Profile is rejected.

Expected:

```text
Validation error
```

---

# Single Profile Compatibility

### TEST-COMP-001

Single profile context remains valid.

Input:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12]
}
```

Expected:

```text
Valid context
```

---

### TEST-COMP-002

Existing ranking workflow remains unchanged.

Expected:

```text
Ranking uses Primary Profile
```

---

### TEST-COMP-003

Existing matching score remains unchanged.

Expected:

```text
Same matching result
before and after context activation
```

---

# Multi Active Profiles

### TEST-MULTI-001

Multiple active profiles are accepted.

Input:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 22]
}
```

Expected:

```text
Valid context
```

---

### TEST-MULTI-002

Changing Primary Profile keeps Active Profiles unchanged.

Before:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17]
}
```

After:

```json
{
  "primary_profile_id": 17,
  "active_profile_ids": [12, 17]
}
```

Expected:

```text
Valid context
```

---

### TEST-MULTI-003

Primary Profile cannot be removed while still primary.

Expected:

```text
Validation error
```

---

# Ranking Rules

### TEST-RANK-001

Ranking uses Primary Profile only.

Scores:

```text
Profile A = 70
Profile B = 91
```

Primary:

```text
Profile A
```

Expected:

```text
Ranking score = 70
```

---

### TEST-RANK-002

Highest secondary score does not affect ranking.

Expected:

```text
No ranking modification
```

---

# Application Workflow

### TEST-APP-001

Application remains linked to a single profile.

Expected:

```text
1 Application
=
1 Profile
```

---

### TEST-APP-002

Primary Profile is preselected.

Expected:

```text
Primary Profile selected by default
```

---

### TEST-APP-003

User can override profile selection.

Expected:

```text
Application created with user-selected profile
```

---

# Non Regression

### TEST-NR-001

Opportunities endpoint remains compatible.

---

### TEST-NR-002

Matching endpoint remains compatible.

---

### TEST-NR-003

Application endpoint remains compatible.

---

### TEST-NR-004

Existing multi-profile score comparison remains compatible.

---

# Exit Criteria

Backend test design phase is complete when:

- validation scenarios are identified;
- compatibility scenarios are identified;
- ranking scenarios are identified;
- application scenarios are identified;
- regression scenarios are identified.

No automated tests are implemented during this phase.
