# Problem statement
Improve Dependency Inversion by separating command execution from build and deploy modules so they depend on a runner contract instead of owning subprocess calls directly.

# Confirmed facts
- `src/core/shell.py` currently wraps direct `subprocess.run(...)` execution in `run(...)`.
- `src/deploy/ansible.py` still calls `subprocess.run(...)` directly for Ansible execution.
- Build and deploy modules both depend on concrete command execution semantics.

# Assumptions
- A small callable runner port is sufficient for this repository.
- The user wants incremental DIP improvement without changing operator-visible behavior.

# Affected files or modules
- `src/core/shell.py`
- `src/core/ports.py`
- `src/core/services.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
- Add a command runner port and a default concrete implementation.
- Expose the runner through execution services so infrastructure modules can depend on injected command execution.
- Refactor Docker and Ansible modules to use the injected runner for command execution.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Confirm Docker and Ansible command paths route through the injected runner.
