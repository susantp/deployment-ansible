# Problem statement
The repository scores lower on Open/Closed than desired because extending operations, architecture support, and image-tag rules currently requires editing existing branching and duplicated literals.

# Confirmed facts
- Operation dispatch is hardcoded with `if mode in {...}` branching in `src/cli/executor.py`.
- Architecture mapping is hardcoded inside `src/docker/builder.py`.
- Canonical image tag construction is duplicated between `src/docker/builder.py` and `src/cli/executor.py`.
- The deployment contract remains `.env` plus `config/services.yaml`, with images named `techbizz/<service>:latest-<arch>`.
- Validation failures and termination policy are repeated inline across CLI, build, deploy, and config modules.

# Assumptions
- The user wants a maintainability refactor, not a behavior change.
- The repository will remain small, so abstractions should stay explicit and low-indirection.

# Affected files or modules
- `src/cli/executor.py`
- `src/docker/builder.py`
- `src/core/`

# Solution strategy
- Introduce a shared policy module for architecture mapping and image tag construction.
- Replace hardcoded operation branching with an operation registry that keeps execution additive.
- Centralize validation failure and termination helpers so modules depend on one exit policy instead of repeating print-plus-exit blocks.
- Preserve current CLI behavior and fail-fast exits.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Run a lightweight smoke read of the touched modules for unchanged flow and contracts.
