# Problem statement
Verify that the build/deploy ports refactor preserved behavior and improved dependency direction cleanly.

# Confirmed facts
- `source .venv/bin/activate && ty check` passes after the ports refactor.
- Executor dependency direction is now executor -> services/ports -> concrete Docker and Ansible modules.

# Assumptions
- Static verification is sufficient for this narrow refactor because the concrete adapter preserves the previous function calls.

# Affected files or modules
- `src/core/ports.py`
- `src/core/services.py`
- `src/cli/executor.py`

# Solution strategy
- Validate type safety and inspect dependency flow after introducing the ports-backed adapter.

# Verification steps
- Ran `source .venv/bin/activate && ty check` successfully.
- Inspected executor imports to confirm they now depend on core wiring rather than infrastructure modules directly.
