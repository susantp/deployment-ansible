# Problem Statement

Prompt ranges in manual interactive menus advertise invalid zero selections.

## Confirmed Facts

- The shared prompt helper hardcodes a lower bound of `0`.
- Not all menus in this repo are zero-based.

## Assumptions

- Prompt text should be derived from actual numeric option keys.

## Affected Files Or Modules

- `src/cli/ui.py`

## Solution Strategy

- Compute numeric option bounds dynamically in `prompt_choice()`.
- Preserve existing custom prompt override support.
- Verify both zero-based and one-based menus after the change.

## Verification Steps

- Check top-level menu prompt remains `Select [0-2]`.
- Check operation prompt becomes `Select [1-3]`.
- Check platform prompt becomes `Select [1-2]`.
