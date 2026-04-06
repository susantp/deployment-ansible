# Problem Statement

Manual interactive mode duplicated menu options for operation and platform selection.

## Confirmed Facts

- Duplicate rendering came from mixed responsibilities between `src/cli/menu.py` and `src/cli/ui.py`.
- `menu.py` rendered operator-friendly labels first.
- `ui.py.select_from_menu()` rendered a second menu from the internal values mapping.

## Assumptions

- Shared UI helper should own menu rendering.
- Display labels and returned values need to remain separable.

## Affected Files Or Modules

- `src/cli/ui.py`
- `src/cli/menu.py`

## Solution Strategy

- Expanded `select_from_menu()` with optional `display_options`.
- Kept prompt lookup against the canonical `options` mapping.
- Updated `select_operation()` and `select_platform()` to use the shared helper once, passing human-friendly labels via `display_options`.

## Side Effects

- Shared helper is now more flexible for future menus that need display labels distinct from internal values.
- Manual interactive flow no longer prints duplicate lists.

## Verification Steps

- Parsed updated Python modules with `uv run python -m py_compile main.py src/cli/menu.py src/cli/ui.py src/cli/executor.py`.
- Re-ran manual interactive flow and confirmed single-render operation and platform menus.
