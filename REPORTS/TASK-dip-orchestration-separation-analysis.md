# Problem statement
Improve Dependency Inversion further by separating orchestration policy from infrastructure execution more strictly.

# Confirmed facts
- `src/cli/executor.py` still contains deploy planning policy by turning services plus architecture into image tags.
- Build and deploy adapters still accept primitive arguments instead of explicit orchestration request models.
- Policy and execution are closer than necessary even after ports and runner injection.

# Assumptions
- A small set of pure request/planning models is sufficient.
- The user wants better dependency direction without changing the deployment contract.

# Affected files or modules
- `src/cli/executor.py`
- `src/core/ports.py`
- `src/core/services.py`
- `src/core/`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
- Introduce pure orchestration request models and planning helpers.
- Refactor ports so infrastructure adapters consume explicit requests instead of primitive tuples/lists.
- Refactor executor to coordinate plans only, leaving infrastructure modules to execute requests.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Run `python3 -m compileall main.py src`.
- Confirm executor no longer constructs deploy image tags inline.
