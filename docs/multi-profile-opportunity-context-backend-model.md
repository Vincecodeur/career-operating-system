# Multi Profile Opportunity Context - Backend Model

## Phase

7.1.22.3 Backend Context Model

## Status

Design

---

# 1. Goal

Define the backend context model required to support multiple active profiles in the Opportunities workflow.

The model must distinguish between:

- one Primary Profile;
- one or more Active Profiles.

The model must preserve the current behavior of:

- opportunity matching;
- opportunity ranking;
- opportunity filtering;
- opportunity details;
- application creation.

This phase defines the backend contract only.

No backend implementation is performed during this phase.

---

# 2. Product Context

The system already supports multiple candidate profiles.

The current Opportunities workflow uses one selected profile context at a time.

The selected profile currently controls:

- opportunity ranking;
- opportunity card scores;
- matching analysis;
- application creation from an opportunity.

Opportunity details can already compare matching scores across multiple profiles.

The Multi Profile Opportunity Context phase introduces several simultaneously active profiles without removing the concept of a single profile responsible for ranking and primary actions.

---

# 3. Core Concepts

## 3.1 Primary Profile

The Primary Profile is the single profile that controls the main Opportunities workflow.

The Primary Profile is used for:

- opportunity ranking;
- score-based opportunity filtering;
- score displayed on opportunity cards;
- default profile attribution during application creation.

Only one Primary Profile can exist in an Opportunity Context.

---

## 3.2 Active Profiles

Active Profiles are the profiles included in multi-profile opportunity comparison.

Active Profiles are used for:

- displaying multiple matching scores;
- comparing career strategies;
- identifying which profile best matches an opportunity;
- understanding whether one opportunity is relevant to several profiles.

Several profiles can be active simultaneously.

The Primary Profile must always be included in Active Profiles.

---

## 3.3 Available Profiles

Available Profiles are the profiles that can potentially be selected as Primary Profile or included in Active Profiles.

A profile must exist and be available before it can be included in an Opportunity Context.

Archived profiles must not be automatically included in the active context.

The exact repository criteria used to identify available profiles must be confirmed during the repository audit before implementation.

---

# 4. Opportunity Context Model

The backend context contract is:

```python
class OpportunityContext(BaseModel):
    primary_profile_id: int
    active_profile_ids: list[int]
```

Example:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 22]
}
```

In this example:

```text
Primary Profile:
12

Active Profiles:
12
17
22
```

The Primary Profile controls ranking and primary actions.

All three active profiles can be used for comparison in opportunity details.

---

# 5. Context Lifecycle

The Opportunity Context is temporary.

The Opportunity Context is not persisted in PostgreSQL during the MVP.

The Opportunity Context is not stored as an ApplicationSetting.

The Opportunity Context is not stored as a global user preference.

The Opportunity Context is not restored between application sessions.

When a new Opportunities session starts:

1. the system loads the available profiles;
2. the first available profile becomes the Primary Profile;
3. the Primary Profile is included in Active Profiles.

Default example:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12]
}
```

This behavior preserves compatibility with the existing single-profile context.

---

# 6. Primary Profile Rules

## 6.1 Single Primary Profile

Exactly one Primary Profile must exist when at least one available profile exists.

Valid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17]
}
```

Invalid conceptual state:

```text
Primary Profile A
Primary Profile B
```

The context contract exposes only one `primary_profile_id`.

---

## 6.2 Primary Profile Must Be Active

The Primary Profile must always be included in `active_profile_ids`.

Valid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 22]
}
```

Invalid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [17, 22]
}
```

The backend must reject or normalize a context where the Primary Profile is not active.

The exact validation response will be defined during the Backend API Design phase.

---

## 6.3 Changing the Primary Profile

Changing the Primary Profile changes:

- the ranking profile;
- the score displayed on opportunity cards;
- score-based filtering;
- the default application profile.

Changing the Primary Profile does not automatically deactivate the previous Primary Profile.

Example before change:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17]
}
```

Example after selecting profile `17` as Primary Profile:

```json
{
  "primary_profile_id": 17,
  "active_profile_ids": [12, 17]
}
```

Both profiles remain active.

Only the Primary Profile changes.

---

## 6.4 Deactivating the Primary Profile

The Primary Profile cannot be deactivated while it remains Primary Profile.

The user must first select another active profile as Primary Profile.

Example initial state:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17]
}
```

To deactivate profile `12`, the context must first become:

```json
{
  "primary_profile_id": 17,
  "active_profile_ids": [12, 17]
}
```

Then profile `12` can be removed:

```json
{
  "primary_profile_id": 17,
  "active_profile_ids": [17]
}
```

This rule prevents an invalid context without a usable ranking profile.

---

# 7. Active Profile Rules

## 7.1 At Least One Active Profile

When available profiles exist, `active_profile_ids` must contain at least one profile identifier.

Valid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12]
}
```

Invalid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": []
}
```

The Primary Profile represents the minimum active context.

---

## 7.2 Multiple Active Profiles

Several profiles can be active simultaneously.

Example:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 22]
}
```

Each active profile remains independent.

Activating several profiles does not merge profile data.

Activating several profiles does not create a combined career profile.

Activating several profiles does not create a composite matching score.

---

## 7.3 Active Profile Uniqueness

`active_profile_ids` must not contain duplicate profile identifiers.

Valid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 22]
}
```

Invalid:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 17]
}
```

The backend contract must treat Active Profiles as a unique collection of profile identifiers.

---

## 7.4 Profile Existence

Each identifier in the context must reference an existing profile.

The backend must validate:

- `primary_profile_id`;
- every identifier in `active_profile_ids`.

A context referencing an unknown profile must be rejected.

The exact error contract will be defined during Backend API Design.

---

## 7.5 Archived Profiles

An archived profile must not be automatically selected as Primary Profile.

An archived profile must not be automatically included in Active Profiles.

The behavior for a previously active profile that becomes archived while the Opportunities page is open must be defined during Backend API Design and repository audit.

No assumption is made in this design about the current technical representation of profile activation beyond the existing archived or active profile state.

---

# 8. Matching Behavior

The existing matching engine remains profile-based.

Each score is calculated independently for one profile and one opportunity.

Conceptual relation:

```text
Profile
+
Opportunity
=
Matching Result
```

Example:

```text
Opportunity 501

Profile 12:
82%

Profile 17:
66%

Profile 22:
91%
```

The Multi Profile Opportunity Context does not change the matching formula.

The context only determines which profile results are emphasized or displayed.

---

## 8.1 Matching Calculation Scope

The model does not require creating a new combined matching engine.

The backend can continue to calculate scores independently for each available profile.

Active Profile selection must not modify the mathematical matching result.

Example:

```text
Profile 17 score before activation:
66%

Profile 17 score after activation:
66%
```

Activation changes context and visibility, not scoring.

---

## 8.2 Best Matching Profile

The best matching profile for an opportunity is the profile with the highest individual matching score among the compared profiles.

The current comparison scope must be explicitly selected during Backend API Design:

- all available profiles; or
- only Active Profiles.

This backend model recommends using Active Profiles for context-specific comparison while preserving existing all-profile endpoints until their impact has been audited.

No endpoint behavior is changed by this document alone.

---

# 9. Opportunity Ranking Behavior

Opportunity ranking continues to use only the Primary Profile.

Conceptual rule:

```text
Opportunity Ranking Score
=
Matching Score for Primary Profile
```

Example context:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17, 22]
}
```

Example scores:

```text
Opportunity A

Profile 12:
72%

Profile 17:
91%

Profile 22:
48%
```

The ranking score remains:

```text
72%
```

because profile `12` is the Primary Profile.

The system does not use:

- the highest score across Active Profiles;
- the average score across Active Profiles;
- the sum of scores;
- a weighted multi-profile score;
- a combined profile score.

This preserves deterministic and explainable ranking.

---

# 10. Opportunity Visibility Behavior

Multiple Active Profiles do not automatically hide opportunities.

The Opportunities list remains governed by the existing filtering behavior.

The Primary Profile controls score-based filters.

Example:

```text
Minimum matching score:
70%

Primary Profile score:
62%

Secondary Active Profile score:
91%
```

For the MVP, the score filter uses:

```text
Primary Profile score:
62%
```

The opportunity therefore does not pass the minimum score filter.

The secondary profile score does not override the Primary Profile filter.

Filtering by the highest active-profile score is explicitly deferred.

---

# 11. Opportunity Card Behavior

Opportunity cards continue to use the Primary Profile score.

Example:

```text
Primary Profile:
Technical Partnerships Manager

Opportunity Card:
Match 82%
```

The card does not display a combined score.

The card does not display the average of Active Profiles.

The card does not change ranking because another active profile has a higher score.

Additional Active Profile indicators may be introduced by the frontend design, but the Primary Profile score remains the card's main ranking score.

---

# 12. Opportunity Detail Behavior

Opportunity details support multi-profile comparison.

The detail view can display matching results for:

- the Primary Profile;
- Active Profiles;
- optionally other available profiles if preserved by the existing comparison endpoint.

The frontend must visually distinguish:

- the Primary Profile;
- active secondary profiles;
- inactive profiles, if inactive profiles remain displayed;
- the best matching profile.

Example:

```text
Technical Partnerships Manager
Primary Profile
82%

Solution Architect
Active Profile
91%

Product Manager
Inactive Profile
54%
```

The exact visual representation belongs to Frontend UX Design.

---

# 13. Application Creation Behavior

An Application remains associated with exactly one Profile.

Conceptual relation:

```text
Application
+
Profile
+
Opportunity
```

Multiple active profiles do not create multiple applications automatically.

When an application is created from an opportunity:

1. the Primary Profile is preselected;
2. the user may select another profile before validation;
3. one Application is created for the selected profile.

Example:

```text
Primary Profile:
Technical Partnerships Manager

Active Profiles:
Technical Partnerships Manager
Solution Architect

Create Application
↓
Technical Partnerships Manager preselected
↓
User may select Solution Architect
↓
One application is created
```

Automatic selection of the profile with the highest score remains outside this phase.

The existing APP-005 backlog item continues to cover Best Matching Profile Preselection.

---

# 14. API Contract

## 14.1 Request Contract

The proposed request contract is:

```python
class OpportunityContextRequest(BaseModel):
    primary_profile_id: int
    active_profile_ids: list[int]
```

Example:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17]
}
```

---

## 14.2 Response Contract

The minimal response contract can reflect the validated context:

```python
class OpportunityContextResponse(BaseModel):
    primary_profile_id: int
    active_profile_ids: list[int]
```

Example:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12, 17]
}
```

The response can be enriched later if the repository audit demonstrates a concrete need for:

- profile names;
- profile availability;
- profile archived state;
- validation warnings.

These additions are not included in the minimal contract at this stage.

---

# 15. Validation Rules

The backend context validator must enforce the following rules.

## OPPORTUNITY_CONTEXT_001

```text
Primary Profile is required.
```

---

## OPPORTUNITY_CONTEXT_002

```text
At least one Active Profile is required.
```

---

## OPPORTUNITY_CONTEXT_003

```text
Primary Profile must be included in Active Profiles.
```

---

## OPPORTUNITY_CONTEXT_004

```text
Active Profile identifiers must be unique.
```

---

## OPPORTUNITY_CONTEXT_005

```text
Primary Profile must exist.
```

---

## OPPORTUNITY_CONTEXT_006

```text
Every Active Profile must exist.
```

---

## OPPORTUNITY_CONTEXT_007

```text
An archived profile cannot be automatically selected as Primary Profile.
```

The exact HTTP status codes and response payloads are deferred to Backend API Design.

---

# 16. Empty Profile State

If no available profile exists, no valid Opportunity Context can be created.

Expected conceptual state:

```text
Primary Profile:
None

Active Profiles:
[]
```

This state is not a valid context for ranking or profile-based matching.

The Opportunities workflow must display an explicit no-profile state.

The exact frontend message and available action belong to Frontend UX Design.

The exact backend response belongs to Backend API Design.

---

# 17. Persistence Strategy

The Opportunity Context is not persisted in the MVP.

No new PostgreSQL table is introduced.

No new column is added to Profile.

No `primary_profile_id` is added to ApplicationSetting.

No list of active profile identifiers is stored in ApplicationSetting.

No last selected profile is restored between sessions.

The context exists only for the current Opportunities workflow session.

This decision avoids introducing a hidden global profile preference.

---

# 18. Compatibility Analysis

## 18.1 Profile Domain

No Profile data model change is required by this design.

The Profile domain remains the source of profile information.

Profile archival remains independent from context activation.

---

## 18.2 Matching Domain

The matching engine remains unchanged.

Matching continues to evaluate one profile against one opportunity.

No combined score is introduced.

---

## 18.3 Ranking Domain

The ranking domain continues to receive one profile identifier.

That identifier is the Primary Profile identifier.

No multi-profile ranking algorithm is introduced.

---

## 18.4 Applications Domain

The Application model remains linked to one profile.

No many-to-many relationship between Application and Profile is introduced.

No multi-profile application is introduced.

---

## 18.5 Settings Domain

The Opportunity Context is not a persistent setting.

Saved Searches remain independent from Opportunity Context.

Discovery Preferences remain independent from Opportunity Context.

Search Criteria Settings remain independent from Opportunity Context.

---

## 18.6 Frontend Compatibility

The current selected profile can become the initial Primary Profile.

The current profile selector can evolve into:

- a Primary Profile selector;
- an Active Profiles selector.

The existing single-profile behavior is equivalent to:

```json
{
  "primary_profile_id": 12,
  "active_profile_ids": [12]
}
```

This provides backward-compatible behavior.

---

# 19. Non-Goals

This phase does not introduce:

- persistent profile context;
- global default profile;
- last selected profile restoration;
- combined multi-profile ranking;
- average multi-profile score;
- maximum-score ranking;
- profile data merging;
- automatic opportunity hiding based on secondary profiles;
- automatic best-profile selection;
- simultaneous creation of several applications;
- matching formula changes;
- notification rules;
- profile-specific Saved Searches.

---

# 20. Deferred Decisions

The following decisions are deferred.

## 20.1 Best Matching Profile Preselection

Automatically preselecting the highest-scoring profile during application creation remains covered by APP-005.

---

## 20.2 Multi-Profile Opportunity Visibility

Displaying an opportunity when at least one Active Profile reaches the minimum matching score is deferred.

The MVP continues to use the Primary Profile for score filtering.

---

## 20.3 Combined Multi-Profile Ranking

Ranking based on:

- maximum active score;
- average active score;
- weighted active scores;
- strategic profile priority;

is not included.

---

## 20.4 Persistent Context

Persisting:

- Primary Profile;
- Active Profiles;
- last profile selection;

is not included.

---

## 20.5 Profile-Specific Saved Searches

Saved Searches do not store:

- Primary Profile;
- Active Profiles;
- profile context.

This can be reconsidered only after the Multi Profile Opportunity Context workflow has been validated.

---

# 21. Repository Audit Requirements

Before implementation, the following real repository elements must be audited:

- Profile model;
- Profile schemas;
- Profile list endpoint;
- profile archival behavior;
- matching endpoints;
- ranked opportunity endpoints;
- multi-profile score endpoint;
- application creation endpoint;
- Opportunities frontend profile selector;
- profile score comparison UI;
- existing tests.

The audit must verify which parts of this design are already implemented and which parts require change.

No implementation must be generated from this design document alone.

---

# 22. Testing Expectations

Future backend tests must cover at least:

```text
Primary Profile exists.
Primary Profile belongs to Active Profiles.
At least one Active Profile exists.
Active Profile identifiers are unique.
Unknown Primary Profile is rejected.
Unknown Active Profile is rejected.
Single-profile context remains supported.
Multiple Active Profiles are supported.
Ranking continues to use Primary Profile.
Application creation remains linked to one profile.
```

The exact test files and fixtures must be determined from the actual repository structure during implementation.

---

# 23. Completion Criteria

The Backend Context Model design is complete when:

- Primary Profile is defined;
- Active Profiles are defined;
- context invariants are defined;
- ranking behavior is defined;
- filtering behavior is defined;
- matching compatibility is defined;
- application compatibility is defined;
- persistence strategy is defined;
- API contracts are proposed;
- non-goals are explicit;
- deferred decisions are explicit;
- repository audit requirements are documented.

---

# 24. Final Decision

The Multi Profile Opportunity Context introduces:

```text
1 Primary Profile
+
1..N Active Profiles
```

The Primary Profile controls:

```text
- ranking;
- score-based filtering;
- opportunity card score;
- default application profile.
```

Active Profiles control:

```text
- multi-profile comparison;
- opportunity analysis across career strategies;
- best matching profile identification.
```

The matching engine remains profile-specific.

The ranking remains based on the Primary Profile.

Applications remain associated with one profile.

The context is temporary and is not persisted during the MVP.
