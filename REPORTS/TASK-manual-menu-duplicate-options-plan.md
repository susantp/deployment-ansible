# Problem Statement

Manual interactive mode shows duplicate option lines for operation and platform menus.

## Confirmed Facts

- Duplicate rendering comes from `menu.py` printing labels first and `ui.py.select_from_menu()` printing the internal values again.
- The same bug pattern affects both `select_operation()` and `select_platform()`.

## Assumptions

- One render per menu is the desired interaction model.
- Internal values should remain lowercase canonical values for downstream execution.

## Affected Files Or Modules

- `src/cli/ui.py`
- `src/cli/menu.py`

## Solution Strategy

- Add optional `display_options` support to `select_from_menu()` so the function can render user-friendly labels while returning canonical values.
- Remove the pre-rendering pattern from `select_operation()` and `select_platform()` and route both through the shared helper once.
- Keep existing validation and prompt behavior intact.

## Verification Steps

- Reproduce manual flow using scripted stdin and confirm the operation menu appears only once.
- Continue further into platform and service selection to confirm the flow no longer duplicates lists.
- Persist verification results in a task verification report.
