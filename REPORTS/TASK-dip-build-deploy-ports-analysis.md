# Problem statement
Raise Dependency Inversion by making the execution layer depend on build/deploy contracts rather than importing concrete Docker and Ansible implementations directly.

# Confirmed facts
- `src/cli/executor.py` currently imports `build_service` from `src/docker/builder.py`.
- `src/cli/executor.py` currently imports `deploy_images` from `src/deploy/ansible.py`.
- The executor already models operations declaratively, so the remaining tight coupling is at the infrastructure call boundary.

# Assumptions
- The user wants incremental DIP improvement, not a full framework or container setup.
- Runtime behavior should remain unchanged.

# Affected files or modules
- `src/cli/executor.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`
- `src/core/`

# Solution strategy
- Introduce narrow callable ports for building a service and deploying image tags.
- Move concrete adapter wiring to a dedicated module so the executor depends on ports instead of infrastructure modules.
- Preserve the existing operation flow and fail-fast behavior.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Confirm `build`, `deploy`, and `both` still delegate to the same concrete Docker and Ansible behavior.
