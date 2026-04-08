# Problem statement
Create a first PySide6 GUI wrapper that gathers user input visually and delegates real execution to the existing non-interactive CLI path.

# Confirmed facts
- The GUI should stay thin and must not reimplement orchestration logic.
- The local project virtualenv is the correct runtime for the first version.

# Assumptions
- A single-window GUI is sufficient for the first iteration.

# Affected files or modules
- `pyproject.toml`
- `src/gui/__init__.py`
- `src/gui/app.py`
- `README.md`
- `docs/ARCHITECTURE.md`

# Solution strategy
- Added `PySide6` as a dependency.
- Added `src/gui/app.py` with:
  - mode and architecture selectors
  - service checklist loaded from `config/services.yaml`
  - command preview
  - `QProcess` runner using `.venv/bin/python -m main ...`
  - live stdout/stderr output panel
- Updated docs to explain local GUI launch and its wrapper role.

# Verification steps
- Confirmed the GUI starts in headless mode without import errors.
- Confirmed typing and bytecode compilation succeed.
