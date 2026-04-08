# Problem statement
Improve Dependency Inversion in the operation execution path with minimal abstraction overhead.

# Confirmed facts
- The executor is the high-level orchestration module for build/deploy sequencing.
- Concrete Docker and Ansible modules are currently imported directly into the executor.

# Assumptions
- The repository should keep explicit, readable wiring.

# Affected files or modules
- `src/cli/executor.py`
- `src/core/`

# Solution strategy
1. Add a small ports module with callable type aliases for build and deploy operations.
2. Add an adapter/wiring module that binds those ports to the current Docker and Ansible implementations.
3. Refactor `src/cli/executor.py` to use the ports-backed adapter instead of importing infrastructure modules directly.
4. Keep all public CLI and orchestration behavior unchanged.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Inspect the executor flow to confirm it depends only on ports-backed wiring.
