# Problem statement
Verify that orchestration-policy separation preserved behavior and improved dependency direction.

# Confirmed facts
- `source .venv/bin/activate && ty check` passes after the orchestration separation refactor.
- `python3 -m compileall main.py src` succeeds after the orchestration separation refactor.
- Executor no longer constructs deploy image tags inline.

# Assumptions
- Static checks are sufficient for this slice because command composition and request data remained explicit and unchanged in meaning.

# Affected files or modules
- `src/core/orchestration.py`
- `src/core/ports.py`
- `src/cli/executor.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
- Validate the refactor with type checking, compilation, and direct inspection of the dependency flow.

# Verification steps
- Ran `source .venv/bin/activate && ty check` successfully.
- Ran `python3 -m compileall main.py src` successfully.
- Inspected the executor and adapter modules to confirm planning is now centralized in pure orchestration helpers.
