# Problem statement
Improve Dependency Inversion by removing direct infrastructure imports from the operation execution layer.

# Confirmed facts
- The executor previously depended directly on Docker and Ansible modules.
- The repository already had declarative operation definitions, so the remaining DIP issue was concrete dependency wiring.

# Assumptions
- Callable ports are sufficient for this repository size.

# Affected files or modules
- `src/core/ports.py`
- `src/core/services.py`
- `src/cli/executor.py`

# Solution strategy
- Added narrow callable ports in `src/core/ports.py` for build and deploy behavior.
- Added `src/core/services.py` to bind those ports to the current concrete Docker and Ansible implementations.
- Refactored `src/cli/executor.py` so execution functions depend on `ExecutionServices` instead of importing infrastructure modules directly.

# Verification steps
- Confirmed executor no longer imports `src/docker/builder.py` or `src/deploy/ansible.py` directly.
- Confirmed build and deploy flow still route to the same concrete implementations through the adapter.
