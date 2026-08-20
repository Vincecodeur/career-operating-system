# Multi Profile Opportunity Context - Frontend Design

## Phase

7.1.22.6 Frontend UX Design

## Status

Design

---

# 1. Goal

Define the frontend experience required to support multiple active profiles in the Opportunities workflow.

The design must introduce a clear distinction between:

- one Primary Profile;
- one or more Active Profiles.

The frontend must preserve the existing behavior for:

- opportunity ranking;
- opportunity card scores;
- opportunity filtering;
- opportunity details;
- application creation.

This document defines the expected user experience only.

No frontend implementation is performed during this phase.

---

# 2. Product Context

The system already supports multiple candidate profiles.

The current Opportunities page uses one selected profile context.

The selected profile currently controls:

- opportunity ranking;
- the matching score displayed on opportunity cards;
- the matching analysis displayed for the selected opportunity;
- the profile used during application creation.

The opportunity detail already supports comparison of multiple profile scores.

The Multi Profile Opportunity Context phase introduces multiple simultaneously active profiles while preserving a single Primary Profile for ranking and primary actions.

---

# 3. Core UX Concepts

## 3.1 Primary Profile

The Primary Profile is the main working profile for the Opportunities page.

Exactly one Primary Profile exists when at least one available profile exists.

The Primary Profile controls:

- opportunity ranking;
- score-based filtering;
- the score displayed on opportunity cards;
- the default profile used during application creation.

The Primary Profile must always be included in Active Profiles.

---

## 3.2 Active Profiles

Active Profiles are the profiles included in the multi-profile comparison context.

One or more profiles can be active simultaneously.

Active Profiles are used for:

- comparing matching scores;
- analysing one opportunity from several career perspectives;
- identifying which active profile best matches an opportunity;
- understanding whether an opportunity is relevant to several profiles.

Active Profiles do not control the main ranking unless the active profile is also the Primary Profile.

---

## 3.3 Available Profiles

Available Profiles are profiles that can be selected in the Opportunities context.

Available Profiles may be:

- active in the opportunity context;
- inactive in the opportunity context;
- selected as Primary Profile.

Archived profiles must not be automatically selected as Primary Profile.

Archived profiles must not be automatically activated.

The exact filtering of archived profiles must be confirmed during the repository audit before implementation.

---

# 4. UX Principles

The interface must make the following distinction immediately understandable:

```text
Primary Profile
=
profile used for ranking and primary actions
```

```text
Active Profiles
=
profiles used for comparison and analysis
```

The user must not confuse:

- active profile with archived profile;
- Primary Profile with best matching profile;
- Primary Profile with the only evaluated profile;
- profile activation with profile data modification.

The interface must remain usable when only one profile exists.

The existing single-profile experience must remain the simplest valid state.

---

# 5. Page Placement

The Opportunity Context section must appear near the top of the Opportunities page.

Recommended order:

```text
Page Header
↓
Opportunity Context
↓
Search and Filters
↓
Saved Searches
↓
Opportunity Results
```

The context must be visible before the user analyses or filters opportunities because the Primary Profile controls ranking and score-based filtering.

---

# 6. Opportunity Context Section

## 6.1 Section Title

```text
Opportunity Context
```

## 6.2 Description

```text
Choose the primary profile used for ranking and the profiles included in opportunity comparison.
```

The description must clearly communicate that Primary Profile and Active Profiles have different responsibilities.

---

# 7. Recommended Layout

The section should contain two distinct areas:

```text
Primary Profile
```

and:

```text
Active Profiles
```

Example:

```text
Opportunity Context

Primary Profile
[Technical Partnerships Manager ▼]

Active Profiles
☑ Technical Partnerships Manager
☑ Solution Architect
☐ Product Manager
☐ Head of Partnerships
```

The Primary Profile selector should be visually stronger than the Active Profiles controls because the Primary Profile controls the main Opportunities workflow.

---

# 8. Primary Profile Selector

## 8.1 Control

Use a single-select control.

Recommended component:

```text
Select dropdown
```

Example:

```text
Primary Profile

[Technical Partnerships Manager ▼]
```

Only one profile can be selected.

---

## 8.2 Helper Text

Display:

```text
Used for opportunity ranking, score filters, card scores and application creation.
```

This helper text explains the impact of changing the Primary Profile.

---

## 8.3 Default Selection

When available profiles exist and no context has been selected:

1. select the first available profile as Primary Profile;
2. include that profile in Active Profiles.

Example initial state:

```text
Primary Profile
Technical Partnerships Manager

Active Profiles
☑ Technical Partnerships Manager
```

The context is temporary and is not restored between sessions.

---

## 8.4 Changing the Primary Profile

When the user selects a different Primary Profile:

- the new Primary Profile becomes active automatically if it was inactive;
- the previous Primary Profile remains active;
- opportunity ranking updates;
- opportunity card scores update;
- score-based filtering uses the new Primary Profile;
- future application creation uses the new Primary Profile by default.

Example before change:

```text
Primary Profile
Technical Partnerships Manager

Active Profiles
☑ Technical Partnerships Manager
☑ Solution Architect
```

Example after selecting Solution Architect:

```text
Primary Profile
Solution Architect

Active Profiles
☑ Technical Partnerships Manager
☑ Solution Architect
```

No profile is deactivated automatically.

---

# 9. Active Profiles Selector

## 9.1 Control

Use a multi-select control.

For the MVP, a list of checkboxes is recommended because:

- the number of personal profiles is expected to remain limited;
- all profile names remain visible;
- activation state is immediately understandable;
- the Primary Profile can be visibly protected.

Example:

```text
Active Profiles

☑ Technical Partnerships Manager
☑ Solution Architect
☐ Product Manager
☐ Head of Partnerships
```

---

## 9.2 Helper Text

Display:

```text
Active profiles are included in opportunity comparison.
```

---

## 9.3 Activation

When the user activates an additional profile:

- the profile is added to the comparison context;
- the profile does not become Primary automatically;
- the opportunity ranking does not change;
- the main score displayed on opportunity cards does not change;
- the profile becomes available in the opportunity comparison display.

---

## 9.4 Deactivation

When the user deactivates a secondary Active Profile:

- the profile is removed from the comparison context;
- the Primary Profile remains unchanged;
- the opportunity ranking remains unchanged;
- the profile is no longer emphasized in the active comparison.

---

## 9.5 Primary Profile Protection

The Primary Profile cannot be deactivated while it remains Primary Profile.

The checkbox corresponding to the Primary Profile must be:

```text
checked
```

and:

```text
disabled
```

Recommended helper text:

```text
The primary profile must remain active.
```

To deactivate the current Primary Profile, the user must first select another profile as Primary Profile.

---

## 9.6 Minimum Selection

At least one Active Profile must always exist when available profiles exist.

Because the Primary Profile must remain active, the interface cannot reach an empty Active Profiles state.

---

# 10. Profile Status Indicators

Each profile displayed in the Opportunity Context should expose its contextual status.

Recommended labels:

```text
Primary
```

```text
Active
```

```text
Inactive
```

Example:

```text
Technical Partnerships Manager
Primary

Solution Architect
Active

Product Manager
Inactive
```

These labels refer only to the Opportunities context.

They must not be confused with profile archival status.

---

# 11. Primary Profile and Best Match Distinction

The Primary Profile is selected by the user.

The Best Matching Profile is determined by matching scores.

The two profiles can be different.

Example:

```text
Technical Partnerships Manager
Primary Profile
82%

Solution Architect
Best Match
91%
```

The interface must never imply that the Primary Profile is automatically the Best Matching Profile.

Recommended labels:

```text
Primary Profile
```

and:

```text
Best Match
```

The labels must remain separate.

---

# 12. Opportunity List Behavior

## 12.1 Opportunity Visibility

Multiple Active Profiles do not automatically hide opportunities.

The existing opportunity visibility rules remain unchanged.

The Opportunities list continues to use:

- keyword search;
- application status;
- source;
- location;
- discovery preferences;
- Primary Profile score.

Secondary Active Profile scores do not override the Primary Profile score filter.

---

## 12.2 Ranking

Opportunity ranking continues to use the Primary Profile only.

Changing Active Profiles without changing the Primary Profile must not modify ranking.

Changing the Primary Profile must update ranking.

---

# 13. Opportunity Card Design

## 13.1 Main Score

The opportunity card continues to display the Primary Profile matching score.

Example:

```text
Senior Technical Partnerships Manager

Match 82%

Technical Partnerships Manager
```

The card must not display:

- an average score;
- a combined score;
- the highest Active Profile score as the main score.

---

## 13.2 Primary Profile Identification

The card should identify which profile explains the displayed score.

Recommended display:

```text
Match 82%

Primary:
Technical Partnerships Manager
```

A compact version may be used if space is limited:

```text
TPM · 82%
```

The exact abbreviation strategy must not be implemented unless profile labels remain unambiguous.

---

## 13.3 Additional Active Profile Indicator

The MVP may display a compact comparison indicator.

Example:

```text
2 other active profiles
```

or:

```text
3 profiles compared
```

This indicator must not replace the Primary Profile score.

The detailed multi-profile comparison remains in the opportunity detail.

---

## 13.4 Best Match Difference

If another Active Profile has a higher score than the Primary Profile, the card may display a secondary indicator:

```text
Best active match: Solution Architect · 91%
```

This indicator is optional for the MVP.

If implemented, it must remain visually secondary to the Primary Profile score and must not change ranking.

---

# 14. Opportunity Detail Design

The opportunity detail must contain a dedicated profile comparison section.

Recommended title:

```text
Profile Comparison
```

Recommended description:

```text
Compare how this opportunity matches the active career profiles.
```

---

# 15. Profile Comparison Display

## 15.1 Recommended Order

Profiles should be displayed in this order:

1. Primary Profile;
2. other Active Profiles ordered by matching score;
3. inactive profiles, only if the existing product decision keeps them visible.

The final inactive-profile visibility rule must be confirmed before implementation.

---

## 15.2 Recommended Card Example

```text
Profile Comparison

Technical Partnerships Manager
Primary Profile
82%

Solution Architect
Best Match
91%

Product Manager
Active Profile
54%
```

The Primary Profile remains first even when another profile has a higher score.

This preserves the working context while still exposing the Best Match.

---

## 15.3 Recommended Table Example

```text
Profile                          Context          Score
Technical Partnerships Manager  Primary          82%
Solution Architect              Active/Best      91%
Product Manager                 Active           54%
```

A table is suitable when the interface already displays matching sub-scores such as:

- skills;
- experience;
- work mode;
- location.

---

## 15.4 Primary Badge

Recommended badge:

```text
Primary
```

Visual purpose:

- identify the profile controlling ranking;
- explain the opportunity card score;
- explain the default application profile.

---

## 15.5 Active Badge

Recommended badge:

```text
Active
```

Visual purpose:

- identify profiles currently included in comparison;
- distinguish Active Profiles from other available profiles.

---

## 15.6 Best Match Badge

Recommended badge:

```text
Best Match
```

Visual purpose:

- identify the highest-score profile;
- support user decision-making;
- remain independent from the Primary Profile selection.

---

# 16. Matching Analysis Behavior

The detailed Matching Analysis section should continue to display the analysis for one selected profile at a time.

Recommended behavior:

- Primary Profile selected by default;
- user can switch between Active Profiles;
- changing the analysis profile does not change the Primary Profile;
- changing the analysis profile does not change opportunity ranking.

Example:

```text
Matching Analysis

Analyse profile:
[Technical Partnerships Manager ▼]
```

This analysis selector is distinct from the Primary Profile selector.

The exact selector behavior must be verified against the existing repository before implementation.

---

# 17. Application Creation Design

## 17.1 Application Rule

One Application remains associated with one Profile.

Multiple Active Profiles must not produce several applications automatically.

---

## 17.2 Default Profile

When the user starts application creation from an opportunity:

```text
Primary Profile
```

is selected by default.

Example:

```text
Create Application

Profile
[Technical Partnerships Manager ▼]
```

---

## 17.3 User Override

The user may select another available profile before confirming application creation.

Example:

```text
Primary Profile:
Technical Partnerships Manager

Selected Application Profile:
Solution Architect
```

The Application is created for Solution Architect only.

Changing the Application Profile does not change the Primary Profile.

---

## 17.4 Best Match Information

The dialog may show:

```text
Best Match:
Solution Architect · 91%
```

This is informational only.

The system must not automatically replace the Primary Profile with the Best Matching Profile during this phase.

Automatic Best Matching Profile Preselection remains covered by APP-005.

---

# 18. Empty States

## 18.1 No Profiles

If no profile exists:

```text
No profile available

Create a profile to rank and compare opportunities.
```

Recommended action:

```text
Create Profile
```

The exact navigation action must be verified against the existing router before implementation.

---

## 18.2 No Active Secondary Profile

If only the Primary Profile is active:

```text
Only the primary profile is currently active.

Activate another profile to compare career strategies.
```

This is a valid state.

---

## 18.3 No Matching Data

If matching data is unavailable for an Active Profile:

```text
Matching data unavailable for this profile.
```

The unavailable result must not be replaced by a score of zero unless the backend contract explicitly returns zero.

---

## 18.4 Archived Profiles

Archived profiles must not be suggested automatically.

If archived profiles are visible in the selector, they must be:

- clearly labelled;
- unavailable for activation;
- excluded from Primary Profile selection.

The exact behavior depends on the repository audit.

---

# 19. Loading States

## 19.1 Loading Profiles

Display:

```text
Loading profiles...
```

The context controls must remain disabled until profiles are loaded.

---

## 19.2 Loading Ranking

When the Primary Profile changes:

```text
Updating opportunity ranking...
```

The interface should preserve the current list until the updated ranking is available, if compatible with the existing implementation.

---

## 19.3 Loading Comparison

When Active Profiles change:

```text
Updating profile comparison...
```

Only the comparison section should show a loading state when possible.

The entire Opportunities page should not be blocked unnecessarily.

---

# 20. Error States

## 20.1 Profiles Loading Error

Display:

```text
Unable to load profiles.
```

The Opportunities context must not silently fall back to an unknown profile.

---

## 20.2 Ranking Error

Display:

```text
Unable to rank opportunities for the selected primary profile.
```

The frontend must not fabricate matching scores.

---

## 20.3 Comparison Error

Display:

```text
Unable to load profile comparison.
```

The error must remain local to the comparison section when possible.

---

## 20.4 Invalid Context

If the backend rejects the context:

```text
The selected opportunity context is invalid.
```

The frontend should restore the last valid context if one exists.

The detailed recovery strategy must be defined after the API contract is verified.

---

# 21. Accessibility

The Opportunity Context must support keyboard navigation.

Requirements:

- every checkbox has a visible label;
- the Primary Profile selector has an associated label;
- disabled controls explain why they are disabled;
- badges do not rely on colour alone;
- focus states remain visible;
- screen readers can identify Primary, Active and Best Match statuses;
- status changes should be announced where technically appropriate.

The interface must not use icons as the only indication of profile status.

---

# 22. Responsive Behavior

The project remains desktop first.

Recommended desktop layout:

```text
Primary Profile selector
Active Profiles controls
```

displayed in two columns when space allows.

Recommended narrow layout:

```text
Primary Profile
↓
Active Profiles
```

displayed in one column.

The profile names must remain readable without horizontal scrolling.

Advanced mobile optimisation remains outside the MVP unless required by the existing layout.

---

# 23. Visual Hierarchy

Recommended priority:

```text
1. Primary Profile
2. Active Profiles
3. Opportunity filters
4. Opportunity list
5. Profile comparison
```

Primary Profile should use the strongest visual emphasis.

Active Profiles should use a clear but secondary visual treatment.

Best Match should be visually noticeable without replacing the Primary Profile context.

---

# 24. Interaction Rules Summary

## Primary Profile Change

```text
User selects another Primary Profile
↓
New Primary Profile is activated if needed
↓
Previous Primary Profile remains active
↓
Ranking updates
↓
Card scores update
↓
Score filters use the new Primary Profile
↓
Application default profile updates
```

---

## Activate Secondary Profile

```text
User activates another profile
↓
Profile joins comparison
↓
Ranking remains unchanged
↓
Card main score remains unchanged
↓
Opportunity detail comparison updates
```

---

## Deactivate Secondary Profile

```text
User deactivates a secondary profile
↓
Profile leaves active comparison
↓
Ranking remains unchanged
↓
Primary Profile remains unchanged
```

---

## Attempt to Deactivate Primary Profile

```text
User attempts to deactivate Primary Profile
↓
Action is disabled
↓
Interface explains that another Primary Profile must be selected first
```

---

## Create Application

```text
User clicks Create Application
↓
Primary Profile is preselected
↓
User can select another profile
↓
One Application is created
```

---

# 25. Current Single-Profile Compatibility

The existing workflow remains supported as:

```text
Primary Profile:
Technical Partnerships Manager

Active Profiles:
Technical Partnerships Manager
```

In this state:

- ranking behaves as today;
- opportunity cards behave as today;
- filtering behaves as today;
- application creation behaves as today;
- profile comparison contains one active profile.

The multi-profile context must not make the single-profile workflow harder to use.

---

# 26. MVP Scope

The frontend MVP includes:

- Primary Profile selector;
- Active Profiles multi-select;
- automatic inclusion of Primary Profile in Active Profiles;
- prevention of Primary Profile deactivation;
- Primary Profile score on opportunity cards;
- Active Profiles comparison in opportunity details;
- Primary Profile as default during application creation;
- manual Application Profile override;
- empty states;
- loading states;
- error states.

---

# 27. Out of Scope

The frontend MVP does not include:

- persistent Opportunity Context;
- last selected Primary Profile restoration;
- last selected Active Profiles restoration;
- drag and drop profile ordering;
- profile favourites;
- profile folders;
- profile priority weighting;
- average multi-profile score;
- maximum-score ranking;
- combined multi-profile ranking;
- automatic opportunity hiding based on secondary profiles;
- automatic Best Matching Profile preselection;
- simultaneous creation of several Applications;
