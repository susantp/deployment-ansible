# Problem statement
Improve Open/Closed characteristics without changing the repository's deployment contract or adding heavy indirection.

# Confirmed facts
- Image tag construction and architecture mapping were previously embedded in operational modules.
- Operation execution previously depended on hardcoded conditional branching.
- Validation failures previously depended on repeated inline `console.print(...)` plus `sys.exit(...)` blocks.

# Assumptions
- The user wanted a selective maintainability refactor, not framework-style abstraction.

# Affected files or modules
- `src/core/choices.py`
- `src/core/policies.py`
- `src/core/shell.py`
- `src/cli/executor.py`
- `src/cli/menu.py`
- `src/cli/parser.py`
- `src/docker/builder.py`
- `src/core/__init__.py`

# Solution strategy
- Added `src/core/policies.py` as the shared authority for:
  - supported architecture to Docker platform mapping
  - canonical image tag construction
- Added shared `fail(...)` and `exit_with_message(...)` helpers in `src/core/shell.py`.
- Refactored `src/docker/builder.py` to consume the shared policies instead of owning local architecture and tag rules.
- Refactored `src/cli/executor.py` to use an operation handler registry instead of direct branching by mode.
- Organized operation definitions in `src/cli/executor.py` as immutable `OperationSpec` values with indexed lookup.
- Replaced raw preset dictionaries in `src/cli/menu.py` with declarative `PresetSpec` values and explicit service resolvers.
- Replaced the tuple-based CLI parsing in `src/cli/parser.py` with declarative `CliCommand` specs and a normalized `ParsedCommand`.
- Added `src/core/choices.py` so operation and platform definitions are shared by CLI validation and interactive menu rendering.
- Migrated CLI, config, build, deploy, and entrypoint validation/termination to the shared helpers.

# Verification steps
- Confirmed `build`, `deploy`, and `both` still map to the same executable behavior.
- Confirmed image tags still use `techbizz/<service>:latest-<arch>`.
- Confirmed unsupported architectures still fail fast with operator feedback.
