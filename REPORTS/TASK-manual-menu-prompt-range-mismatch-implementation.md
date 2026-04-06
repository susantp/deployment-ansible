# Problem Statement

Manual interactive menus advertised zero-based prompt ranges for one-based option sets.

## Confirmed Facts

- `prompt_choice()` previously generated `Select [0-{max}]`.
- Operation and platform menus do not accept `0`.
- Top-level preset/manual selection does accept `0`.

## Assumptions

- Shared prompt generation should derive bounds from the actual numeric keys in the options mapping.

## Affected Files Or Modules

- `src/cli/ui.py`

## Solution Strategy

- Updated `prompt_choice()` to compute `min_option` and `max_option` from numeric keys.
- Prompt text now reflects the actual range present in the provided options mapping.

## Side Effects

- Zero-based menus keep their zero-based prompt.
- One-based menus now show the correct lower bound.

## Verification Steps

- Parsed updated modules with `uv run python -m py_compile main.py src/cli/menu.py src/cli/ui.py src/cli/executor.py`.
- Re-ran interactive flow to confirm prompt ranges for top-level, operation, and platform menus.
