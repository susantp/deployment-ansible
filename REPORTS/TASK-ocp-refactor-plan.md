# Problem statement
Raise the repository's Open/Closed score from roughly 6/10 to about 7/10 without overengineering a stable small CLI.

# Confirmed facts
- Current extensibility pressure points are operation dispatch, image naming, and architecture mapping.
- SRP is acceptable already; the target is selective improvement to extension points.

# Assumptions
- New abstractions are acceptable only if they remove concrete hardcoded branching already present.

# Affected files or modules
- `src/cli/executor.py`
- `src/docker/builder.py`
- `src/core/`

# Solution strategy
1. Add a shared module in `src/core/` that owns image tag construction and supported architecture lookup.
2. Refactor build logic to consume that shared policy instead of owning local architecture mapping.
3. Refactor operation execution to use a registry of handlers instead of mode-specific conditionals.
4. Centralize validation and termination behind shared helpers in `src/core/shell.py`.
5. Organize operation definitions as declarative specs instead of a raw handler mapping.
6. Replace preset placeholder conventions with explicit preset specs and service resolvers.
7. Replace the tuple-based CLI parser with declarative command specs and normalized parsed results.
8. Centralize operation and platform choices so CLI validation and interactive menus derive from one source of truth.
9. Keep public inputs and outputs unchanged so no config, build, or deploy contract drifts.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Confirm the refactor preserved:
  - `build`, `deploy`, and `both` behavior
  - `techbizz/<service>:latest-<arch>` tags
  - `amd` and `arm` support only
