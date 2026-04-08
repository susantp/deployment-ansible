# Problem statement
Verify that command runner injection preserved behavior while improving dependency direction.

# Confirmed facts
- `source .venv/bin/activate && ty check` passes after the runner refactor.
- `python3 -m compileall main.py src` succeeds after the runner refactor.
- Subprocess execution is now centralized in the default runner implementation in `src/core/shell.py`.

# Assumptions
- Static checks are sufficient for this narrow refactor because command composition was preserved.

# Affected files or modules
- `src/core/ports.py`
- `src/core/shell.py`
- `src/core/services.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
- Validate the runner injection with type checking and compilation, then inspect dependency flow.

# Verification steps
- Ran `source .venv/bin/activate && ty check` successfully.
- Ran `python3 -m compileall main.py src` successfully.
- Inspected the touched modules to confirm build and deploy execution paths now depend on the injected runner.
