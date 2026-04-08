# Problem statement
Improve Dependency Inversion by moving command execution behind an injected runner contract.

# Confirmed facts
- Build and deploy modules previously depended on direct command execution behavior.
- Execution services already provided a suitable place to carry concrete dependency wiring.

# Assumptions
- A callable runner port is sufficient for this repository size.

# Affected files or modules
- `src/core/ports.py`
- `src/core/shell.py`
- `src/core/services.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
- Added `RunCommandPort` in `src/core/ports.py`.
- Added `run_command(...)` as the default concrete runner implementation in `src/core/shell.py`.
- Extended `ExecutionServices` in `src/core/services.py` to include the runner dependency.
- Refactored Docker and Ansible modules to execute commands through the injected runner instead of owning direct subprocess execution.

# Verification steps
- Confirmed Docker build, push, and cleanup now route through `execution_services.run_command(...)`.
- Confirmed Ansible deploy now routes through `execution_services.run_command(...)`.
