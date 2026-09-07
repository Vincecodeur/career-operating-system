# Best Profile Recommendation Architecture Review (7.1.26)

## Contexte

DEC-072 (Application Profile Attribution) documents a tie-breaking rule
for the Best Matching Profile recommendation:

```
When several Profiles have the same matching score:
- the Primary Profile is preferred;
- if the tie remains, the lowest profile_id is preferred.
```

The 7.1.26.1 repository audit found that this rule exists in the
codebase, but only inside `frontend/src/pages/OpportunitiesPage.tsx`
(the `bestProfileScore` computation), not in the backend. This
contradicts DEC-032 ("Le frontend ne doit réaliser aucun calcul de
matching. Le score [...] sont entièrement produits par l'API backend.")
and DEC-039 (Explainable Opportunity Scoring), both of which place all
ranking/decision logic in the backend.

Meanwhile, the backend function `calculate_profile_scores_for_job_offer()`
already computes an `is_best_match` field on `ProfileOpportunityScore`,
but uses a simpler rule (highest score only, no tie-break), and this
field is silently ignored by the code path that recommends a profile at
Application creation time.

## Two distinct concepts, not one

The audit confirmed two different uses of "best matching profile" exist
in the frontend, serving different purposes. Both must be preserved:

1. **Table-wide best match** (`profileScores`): every profile owned by
   the user is scored and displayed in the profile comparison table. Each
   row's `is_best_match` flag drives the "🥇 Best Match" badge. This
   concerns ALL of the user's profiles, regardless of whether they are
   currently "Active" in the Opportunity Context (DEC-071).

2. **Active-profile-only recommendation** (`bestProfileScore`): used
   exclusively to pre-select a profile when opening the Create Application
   dialog. This must only consider profiles currently in the user's Active
   Profiles set (DEC-071), consistent with DEC-072 ("the recommended
   Profile is determined from existing backend matching results" within
   the Opportunity Context).

These are not the same computation and must not be collapsed into one.

## Decision

The tie-breaking rule (score desc → Primary Profile → lowest profile_id)
moves entirely to the backend. The frontend stops computing
`bestProfileScore` locally and instead consumes `is_best_match` values
already computed by the backend.

Since DEC-071 established that the Opportunity Context (Primary Profile,
Active Profiles) is intentionally NOT persisted during the MVP, the
backend cannot infer this context on its own. It must receive it as
transient, optional query parameters on each request. No new database
column or table is introduced.

## Backend Changes

### `backend/app/matching/service.py`

`calculate_profile_scores_for_job_offer()` gains two new optional
parameters:

```python
def calculate_profile_scores_for_job_offer(
    job_offer_id: int,
    db: Session,
    user_id: int,
    primary_profile_id: int | None = None,
    active_profile_ids: list[int] | None = None,
) -> list[ProfileOpportunityScore]:
```

Behavior:

- `profiles` query is unchanged (all profiles owned by `user_id`) so the
  full table display (concept 1 above) is unaffected.
- If `active_profile_ids` is provided and non-empty, `is_best_match` is
  computed only among the subset of scores whose `profile_id` is in that
  list. Scores for profiles outside that subset always have
  `is_best_match = False`.
- If `active_profile_ids` is None or empty, `is_best_match` is computed
  among all scores (current behavior preserved, e.g. for callers that
  don't yet pass an Opportunity Context).
- Tie-breaking order when selecting the best score:

1. highest `matching_score`
2. `profile_id == primary_profile_id` preferred
3. lowest `profile_id`

This exactly reproduces the frontend `bestProfileScore` sort comparator,
moved server-side.

### `backend/app/matching/router.py`

`get_profile_scores_for_job_offer()` gains two optional query
parameters, forwarded to the service:

```python
@router.get(
    "/matching/job-offers/{job_offer_id}/profiles",
    response_model=list[ProfileOpportunityScore],
)
def get_profile_scores_for_job_offer(
    job_offer_id: int,
    primary_profile_id: int | None = None,
    active_profile_ids: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
```

`active_profile_ids` is accepted as a comma-separated string (e.g.
`12,17,22`) for simplicity over the query string, then parsed into
`list[int]` before being passed to the service. No validation beyond
integer parsing is required; unknown or foreign profile_ids are
naturally ignored since the service only ever scores profiles already
confirmed to belong to `user_id`.

## Frontend Changes

### `frontend/src/services/api.ts`

`getProfileScoresForJobOffer()` gains two optional parameters:

```typescript
export async function getProfileScoresForJobOffer(
    jobOfferId: number,
    primaryProfileId?: number | null,
    activeProfileIds?: number[],
): Promise<ProfileOpportunityScore[]> {
```

Builds the query string conditionally (omit params when not provided),
appends to the existing URL, keeps the existing `getAuthHeaders()` call
unchanged.

### `frontend/src/pages/OpportunitiesPage.tsx`

- The call site is updated to pass `selectedProfileId` and
  `activeProfileIds` to `getProfileScoresForJobOffer()`.
- The local `bestProfileScore` computation (the sort/tie-break block) is
  removed entirely.
- `getDefaultApplicationProfileId()` is simplified to read `is_best_match`
  directly from `profileScores` (filtered to `activeProfileIds` client-side
  only for the fallback check that the resulting profile still exists in
  `profiles`), instead of recomputing a local best score.

No other component is affected. `MatchingResult`, `ApplicationsPage.tsx`
and `api.ts` types (`ProfileOpportunityScore`) remain unchanged in shape.

## Consistency With DEC-071

DEC-071 explicitly forbids persisting the Opportunity Context:
"No new PostgreSQL table is introduced for Opportunity Context. No new
Profile column is introduced for Opportunity Context." This design
respects that constraint: `primary_profile_id` and `active_profile_ids`
are passed as transient request parameters on every call, never stored.

## Testing Strategy

New backend tests to add to `backend/tests/test_matching.py`:

- `test_profile_scores_best_match_prefers_primary_profile_on_tie`
- `test_profile_scores_best_match_uses_lowest_id_on_full_tie`
- `test_profile_scores_best_match_restricted_to_active_profiles`
- `test_profile_scores_best_match_falls_back_to_all_profiles_when_no_active_ids_given`

Existing tests `test_profile_scores_only_one_best_match` and
`test_profile_scores_sorted_descending` must continue passing unchanged,
since the default behavior (no query params) is preserved.

No frontend test suite currently exists for OpportunitiesPage.tsx logic
(confirmed absence of a dedicated test file during 7.1.26.1 audit); no
new frontend automated test is introduced by this decision, consistent
with the project's current testing scope (backend-only automated
coverage, frontend validated manually per project methodology).

## Out Of Scope

- APP-005 (Automatic Best Matching Profile Acceptance) remains deferred
  to post-MVP; this review only fixes WHERE the recommendation is
  calculated, not whether it bypasses user confirmation.
- No change to the matching score formula itself (DEC-039, Matching V2
  weights) is introduced.
- No change to `calculate_matching_result()` (single profile / single
  offer) or `rank_job_offers_for_profile()`.
