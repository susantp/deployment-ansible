# Problem statement
Reorganize the directory structure so it matches the architecture that now exists in code.

# Confirmed facts
- `src/core/` is the only flat area still combining multiple architectural roles.
- Current runtime and domain boundaries are already visible in code, so the filesystem can mirror them with low semantic risk.

# Assumptions
- Import-path churn is acceptable if behavior remains unchanged and docs are updated.

# Affected files or modules
- `src/core/`
- `main.py`
- `src/cli/`
- `src/docker/`
- `src/deploy/`
- `docs/DIRECTORY_STRUCTURE.md`

# Solution strategy
1. Create `src/core/domain/`, `src/core/contracts/`, and `src/core/runtime/`.
2. Move existing modules into those subdirectories based on their actual role.
3. Update imports across the codebase.
4. Update directory structure documentation.
5. Verify runtime and static behavior.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Run `python3 -m compileall main.py src`.
- Run startup and one non-interactive CLI smoke check.
