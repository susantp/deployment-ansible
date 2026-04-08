# Problem statement
Improve Dependency Inversion by separating orchestration planning from infrastructure execution more strictly.

# Confirmed facts
- The executor previously contained deploy image planning logic.
- Build and deploy adapters previously accepted primitive arguments rather than explicit orchestration requests.

# Assumptions
- Small pure dataclasses are enough to model orchestration requests clearly.

# Affected files or modules
- `src/core/orchestration.py`
- `src/core/ports.py`
- `src/cli/executor.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
- Added `BuildRequest` and `DeployRequest` plus pure planner helpers in `src/core/orchestration.py`.
- Updated ports so infrastructure adapters consume request models instead of primitive arguments.
- Refactored the executor to coordinate planned requests rather than constructing deploy images inline.
- Refactored Docker and Ansible adapters to execute request models.

# Verification steps
- Confirmed executor now plans requests and delegates execution.
- Confirmed Docker and Ansible modules now behave as adapters over explicit request contracts.
