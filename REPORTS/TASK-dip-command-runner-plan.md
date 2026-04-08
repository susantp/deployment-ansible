# Problem statement
Reduce direct subprocess coupling in infrastructure modules by introducing an injectable command runner.

# Confirmed facts
- Current build and deploy modules still hardwire command execution semantics.
- Execution services already exist and are a natural place to carry a runner dependency.

# Assumptions
- Reusing the existing console output style is desirable.

# Affected files or modules
- `src/core/ports.py`
- `src/core/services.py`
- `src/core/shell.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
1. Add a runner port describing command execution.
2. Add a default runner implementation in `src/core/shell.py`.
3. Extend execution services to carry the runner dependency.
4. Refactor build and deploy modules to use the injected runner instead of direct subprocess calls.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Inspect the dependency flow to confirm subprocess usage is centralized in the runner implementation.
