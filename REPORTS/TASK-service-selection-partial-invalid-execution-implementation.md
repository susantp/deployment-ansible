# Problem Statement

Interactive service selection could partially accept malformed input and trigger real execution.

## Confirmed Facts

- The previous parser ignored invalid tokens and out-of-range selections.
- Duplicate indices produced duplicate service execution.

## Assumptions

- Deployment-tool input should be validated strictly before any build or deploy action starts.

## Affected Files Or Modules

- `src/cli/menu.py`

## Solution Strategy

- Updated `select_services()` to validate every provided token.
- Non-numeric tokens now trigger an explicit error and exit.
- Out-of-range selections now trigger an explicit error and exit.
- Duplicate valid selections are deduplicated while preserving user input order.

## Side Effects

- Partially valid mixed input no longer starts work.
- Repeated service numbers no longer produce repeated service execution.

## Verification Steps

- Parsed updated modules with `uv run python -m py_compile main.py src/cli/menu.py src/cli/ui.py src/cli/executor.py`.
- Verified invalid mixed input exits before build or deploy begins.
- Verified duplicate valid input collapses to a unique service list used downstream.
