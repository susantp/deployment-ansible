# Problem statement
Make orchestration policy more explicit and infrastructure execution more adapter-like.

# Confirmed facts
- Executor already chooses operations declaratively.
- The remaining separation issue is that plan construction still leaks into execution code paths.

# Assumptions
- Pure dataclasses and planner functions are enough; a heavy service layer is unnecessary.

# Affected files or modules
- `src/core/`
- `src/cli/executor.py`
- `src/docker/builder.py`
- `src/deploy/ansible.py`

# Solution strategy
1. Add pure orchestration models for build and deploy requests.
2. Add planner helpers that convert canonical inputs into those request models.
3. Update ports and execution services to use request models.
4. Refactor executor, Docker, and Ansible modules around those request contracts.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Run `python3 -m compileall main.py src`.
- Inspect dependency flow to confirm executor coordinates requests and adapters execute them.
