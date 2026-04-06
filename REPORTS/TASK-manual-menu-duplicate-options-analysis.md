# Problem Statement

Manual interactive mode renders duplicate option lists for operation and platform selection when started through `uv run -m main` and the user selects `0` for manual flow.

## Confirmed Facts

- Reproduction path:
  - start `uv run -m main`
  - select `0` for `Manual / Custom`
  - the `Operation` menu renders twice with different labels for the same choices
- Current output shows both:
  - `1. Build / 2. Deploy / 3. Both`
  - `1. build / 2. deploy / 3. both`
- `src/cli/menu.py` calls `display_menu_options(display_options, "Operation")`, then calls `select_from_menu(options, None, "Invalid operation")`.
- `src/cli/ui.py` implements `select_from_menu()` by calling `display_menu_options(options, header)` internally before prompting.
- The same pattern exists for `select_platform()`.

## Assumptions

- The intended UX is a single menu render per prompt, with human-friendly labels and internal values remaining separate.
- The duplicate rendering bug is limited to manual mode because preset mode does not call `select_operation()` or `select_platform()`.

## Root Cause Analysis

There is duplicated rendering responsibility between `src/cli/menu.py` and `src/cli/ui.py`.

- `menu.py` wants custom display labels (`Build`, `Deploy`, `Both`) but canonical returned values (`build`, `deploy`, `both`).
- `select_from_menu()` currently assumes it always owns rendering and only accepts one options mapping, so `menu.py` pre-renders the friendly labels and `ui.py` re-renders the canonical values.

The bug is therefore not in Rich or prompt handling. It is a boundary issue between menu orchestration and shared UI helpers.

## Affected Files Or Modules

- `src/cli/menu.py`
- `src/cli/ui.py`

## Solution Strategy

- Keep rendering responsibility inside `select_from_menu()`.
- Extend `select_from_menu()` so it can accept a separate `display_options` mapping for operator-facing labels while still returning canonical internal values.
- Update manual operation and platform selection to use the shared helper once instead of pre-rendering and re-rendering.

## Side Effects

- Shared UI helper signature will expand.
- Manual flow should display each selection list once.
- Preset flow and other call sites should remain behaviorally unchanged.

## Verification Steps

- Re-run interactive flow with manual mode input and confirm operation/platform lists render once.
- Confirm selected values still map to canonical internal values used downstream.
