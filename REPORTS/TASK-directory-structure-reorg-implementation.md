# Problem statement
Reorganize the directory structure so the filesystem reflects the architecture now present in code.

# Confirmed facts
- `src/core/` previously mixed domain, contracts, runtime wiring, and shell execution in one flat directory.
- The code already expressed those boundaries logically, so the filesystem could be aligned without changing behavior.

# Assumptions
- Keeping top-level `src/cli`, `src/docker`, and `src/deploy` stable preserves operator familiarity.

# Affected files or modules
- `src/core/domain/`
- `src/core/contracts/`
- `src/core/runtime/`
- import sites across `main.py` and `src/`
- `docs/DIRECTORY_STRUCTURE.md`

# Solution strategy
- Created:
  - `src/core/domain/`
  - `src/core/contracts/`
  - `src/core/runtime/`
- Moved:
  - `choices.py`, `policies.py`, `orchestration.py` into `domain/`
  - `ports.py` into `contracts/`
  - `services.py`, `shell.py` into `runtime/`
- Updated imports and documentation to match the new structure.

# Verification steps
- Confirmed static imports resolve after the move.
- Confirmed startup and CLI execution still follow the same runtime behavior.
