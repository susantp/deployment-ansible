# Problem statement
Verify that the first PySide6 GUI wrapper is wired correctly to the current repo and local virtualenv.

# Confirmed facts
- `source .venv/bin/activate && ty check` passes after the GUI addition.
- `python3 -m compileall src/gui` succeeds.
- Headless startup via `QT_QPA_PLATFORM=offscreen` succeeds for `src.gui.app`.

# Assumptions
- Headless Qt startup is a sufficient verification of imports, widget construction, and local interpreter resolution for this first version.

# Affected files or modules
- `pyproject.toml`
- `src/gui/app.py`
- `README.md`
- `docs/ARCHITECTURE.md`

# Solution strategy
- Validate types, compilation, and GUI startup without requiring an interactive desktop session.

# Verification steps
- Ran `source .venv/bin/activate && ty check` successfully.
- Ran `python3 -m compileall src/gui` successfully.
- Ran:
  - `QT_QPA_PLATFORM=offscreen .venv/bin/python -c "from PySide6.QtCore import QTimer; from PySide6.QtWidgets import QApplication; from src.gui.app import MainWindow; import sys; app = QApplication(sys.argv); window = MainWindow(); QTimer.singleShot(0, app.quit); app.exec()"`
  - and confirmed startup succeeded.
