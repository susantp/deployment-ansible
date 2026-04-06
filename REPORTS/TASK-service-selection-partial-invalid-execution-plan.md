# Problem Statement

Interactive service selection is too permissive and can trigger partial execution from malformed input.

## Confirmed Facts

- Invalid tokens are silently ignored.
- Duplicate valid selections are preserved.
- Mixed input can still launch build or deploy operations.

## Assumptions

- For this deployment tool, fail-fast validation is preferable to permissive partial acceptance.

## Affected Files Or Modules

- `src/cli/menu.py`

## Solution Strategy

- Validate every service-selection token.
- Emit a clear error and exit on the first invalid token class.
- Deduplicate accepted services while preserving selection order.

## Verification Steps

- Parse-check updated code.
- Re-run interactive service selection with mixed invalid input and confirm no work begins.
- Re-run with duplicate valid input and confirm only unique services are returned.
