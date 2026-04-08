# Problem statement
Verify that the directory reorganization preserved behavior and did not break imports or runtime startup.

# Confirmed facts
- `source .venv/bin/activate && ty check` passes after the reorganization.
- `python3 -m compileall main.py src` succeeds after the reorganization.
- `uv run -m main` reaches the interactive prompt.
- `uv run -m main build amd nginx` enters the real Docker build path.

# Assumptions
- The `EOFError` seen in interactive startup is expected in this non-interactive execution environment and does not indicate an application bug.

# Affected files or modules
- `src/core/domain/`
- `src/core/contracts/`
- `src/core/runtime/`
- import sites across `main.py` and `src/`
- `docs/DIRECTORY_STRUCTURE.md`

# Solution strategy
- Verify static import resolution, compilation, startup, and one non-interactive smoke path after the move.

# Verification steps
- Ran `source .venv/bin/activate && ty check` successfully.
- Ran `python3 -m compileall main.py src` successfully.
- Ran `uv run -m main` and confirmed startup reached the prompt.
- Ran `uv run -m main build amd nginx` and confirmed the Docker build flow started.
