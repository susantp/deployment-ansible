# Problem Statement

Service selection in interactive mode accepts mixed valid and invalid tokens, silently discards invalid entries, preserves duplicates, and can start real build or deploy work from a partially invalid selection.

## Confirmed Facts

- `src/cli/menu.py::select_services()` parses space-separated tokens and appends valid numeric selections.
- Non-numeric tokens are ignored silently.
- Out-of-range numeric tokens are ignored silently.
- Duplicate numeric selections produce duplicate service entries.
- Reproduction used manual mode input `1 1 99 foo 2` at the service prompt.
- That input started real work for selected valid services instead of rejecting the selection.
- Because duplicates were preserved, repeated service indices can trigger repeated execution of the same service.

## Assumptions

- Interactive operator input should be fail-fast and explicit.
- If any provided service token is invalid, the prompt should reject the whole selection instead of proceeding with partial execution.
- Duplicate selections should collapse to a unique ordered list because building or deploying the same service twice from one prompt is not useful.

## Root Cause Analysis

`select_services()` currently treats the prompt as a best-effort collector instead of a validator.

- It attempts integer conversion token-by-token.
- It ignores parse failures and range failures.
- It returns whatever valid services were accumulated.

That behavior is too permissive for deployment tooling because malformed operator input can still launch expensive or state-changing actions.

## Affected Files Or Modules

- `src/cli/menu.py`

## Solution Strategy

- Parse all tokens first.
- Reject the whole selection when any token is non-numeric or out of range.
- Deduplicate valid services while preserving input order.
- Keep the existing post-selection empty-check behavior in the calling flow.

## Side Effects

- Mixed valid and invalid input will now stop immediately with a clear error instead of partially executing.
- Repeated service numbers will no longer trigger duplicate execution.

## Verification Steps

- Confirm invalid mixed input such as `1 1 99 foo 2` exits before execution.
- Confirm duplicate-only input such as `1 1 2` resolves to unique ordered services.
- Confirm valid multi-select input still works.
