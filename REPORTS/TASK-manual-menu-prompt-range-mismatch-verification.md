# Problem Statement

Verify that interactive menu prompts now display correct numeric ranges for both zero-based and one-based menus.

## Confirmed Facts

- The shared prompt helper now computes both minimum and maximum numeric option keys.

## Assumptions

- Verifying the visible prompt text is sufficient because the issue is strictly UI guidance, not downstream execution.

## Affected Files Or Modules

- `src/cli/ui.py`

## Solution Strategy

- Re-run the interactive flow and inspect prompt text at each stage.

## Verification Steps

- Ran:
  - `uv run python -m py_compile main.py src/cli/menu.py src/cli/ui.py src/cli/executor.py`
- Started:
  - `uv run -m main`
- Observed:
  - top-level prompt: `Select [0-2]`
  - operation prompt: `Select [1-3]`
  - platform prompt: `Select [1-2]`
  - service prompt remained `Select [1-7] (space-separated for multiple)`
- Interrupted before executing any build or deploy action.

## Result

- Verification passed.
- Prompt ranges now match actual accepted choices across the tested manual-flow menus.
