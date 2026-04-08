# Problem statement
Verify that the Open/Closed refactor preserved behavior and kept the codebase type-clean.

# Confirmed facts
- `source .venv/bin/activate && ty check` passes after the refactor.
- No config, inventory, playbook, or image-tag contract was changed.
- Validation still fails fast, but the policy is now centralized in `src/core/shell.py`.

# Assumptions
- Static verification is sufficient for this slice because the refactor is localized and preserves existing command composition.

# Affected files or modules
- `src/core/choices.py`
- `src/core/policies.py`
- `src/core/shell.py`
- `src/cli/executor.py`
- `src/cli/menu.py`
- `src/cli/parser.py`
- `src/docker/builder.py`

# Solution strategy
- Validate the refactor with type checking and direct inspection of the touched execution paths.

# Verification steps
- Ran `source .venv/bin/activate && ty check` successfully.
- Inspected the updated modules to confirm:
  - `execute_operation()` dispatches via declarative operation specs
  - presets are defined as declarative specs with explicit service resolution
  - CLI parsing routes through declarative command specs and returns a normalized parsed command
  - CLI validation and interactive menu choices derive from one shared choice registry
  - `build_service()` resolves architecture through shared policy
  - deploy image names are built from one shared helper
  - validation and termination now route through shared helpers instead of repeated inline exits
