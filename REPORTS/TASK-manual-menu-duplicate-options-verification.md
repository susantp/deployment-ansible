# Problem Statement

Verify that manual interactive mode no longer duplicates operation and platform menu options.

## Confirmed Facts

- The shared helper now accepts separate display labels and return values.
- Manual selection code now routes both operation and platform menus through one render path.

## Assumptions

- Stopping the interactive run after platform selection is sufficient to verify the duplicate-render regression because the bug occurred before service execution.

## Affected Files Or Modules

- `src/cli/ui.py`
- `src/cli/menu.py`

## Solution Strategy

- Verify syntax and imports.
- Reproduce the interactive flow through manual mode and inspect prompt output directly.

## Verification Steps

- Ran:
  - `uv run python -m py_compile main.py src/cli/menu.py src/cli/ui.py src/cli/executor.py`
- Started:
  - `uv run -m main`
- Entered:
  - `0` to select manual mode
  - `1` to select build mode
- Observed:
  - `Operation` menu rendered once with `Build`, `Deploy`, `Both`
  - `Platform` menu rendered once with `AMD (linux/amd64)` and `ARM (linux/arm64)`
- Interrupted after platform prompt to avoid starting an actual build.

## Result

- Verification passed.
- The duplicate option rendering regression is fixed for the manual flow path that previously reproduced it.
