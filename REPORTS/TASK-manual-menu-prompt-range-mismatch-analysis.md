# Problem Statement

Manual interactive mode shows prompt ranges that advertise `0` as a valid selection for operation and platform menus even though those menus accept only `1..n`.

## Confirmed Facts

- Current operation prompt shows `Select [0-3]` while valid options are `1`, `2`, and `3`.
- Current platform prompt shows `Select [0-2]` while valid options are `1` and `2`.
- `src/cli/ui.py` generates prompt text in `prompt_choice()` using only `max_option`, producing `Select [0-{max}]`.
- `prompt_choice()` does not inspect the minimum numeric option key.
- Top-level preset/manual selection legitimately includes `0`, so `Select [0-2]` is correct there.

## Assumptions

- Prompt ranges should reflect the actual accepted numeric keys.
- Shared helper logic should derive prompt range from the provided options mapping instead of assuming zero-based numbering.

## Root Cause Analysis

The shared prompt generator in `src/cli/ui.py` assumes all numbered menus start at `0`.

That assumption holds for the top-level preset menu but is false for operation and platform menus, which are one-based. As a result, the UI communicates an invalid choice as if it were valid.

## Affected Files Or Modules

- `src/cli/ui.py`

## Solution Strategy

- Update `prompt_choice()` to compute both the minimum and maximum numeric keys from the supplied options mapping.
- Generate `Select [min-max]` instead of hardcoding a zero-based lower bound.

## Side Effects

- Top-level menu prompt remains unchanged because its numeric keys do include `0`.
- One-based menus will now advertise the correct accepted range.

## Verification Steps

- Re-run manual mode and confirm operation prompt shows `Select [1-3]`.
- Confirm platform prompt shows `Select [1-2]`.
- Confirm top-level prompt still shows `Select [0-2]`.
