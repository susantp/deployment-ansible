# Problem statement
The current directory structure no longer reflects the architectural boundaries introduced by the recent refactors. `src/core/` contains mixed concerns: domain choices and policies, dependency contracts, runtime wiring, shell helpers, and config authority.

# Confirmed facts
- `src/core/choices.py`, `src/core/policies.py`, and `src/core/orchestration.py` are pure domain/planning concerns.
- `src/core/ports.py` defines dependency contracts.
- `src/core/services.py` and `src/core/shell.py` are runtime wiring/execution concerns.
- `docs/DIRECTORY_STRUCTURE.md` no longer matches the current module surface.

# Assumptions
- The user wants the filesystem layout to align more closely with the current architecture without changing runtime behavior.
- Keeping top-level familiarity (`src/cli`, `src/docker`, `src/deploy`) is preferable to a fully new root package taxonomy.

# Affected files or modules
- `src/core/`
- import sites across `src/` and `main.py`
- `docs/DIRECTORY_STRUCTURE.md`

# Solution strategy
- Reorganize `src/core/` into focused subdirectories:
  - `src/core/domain/`
  - `src/core/contracts/`
  - `src/core/runtime/`
- Keep `src/core/config.py` in place as configuration authority.
- Update imports and docs to match the new structure.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Run `python3 -m compileall main.py src`.
- Run `uv run -m main` to interactive startup.
- Run `uv run -m main build amd nginx` as a smoke check.
