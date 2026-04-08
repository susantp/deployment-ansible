# Problem statement
Create a thin PySide6 wrapper for the existing CLI workflow.

# Confirmed facts
- Existing non-interactive flow already works and is the correct execution path for a GUI wrapper.
- A GUI wrapper only needs to gather inputs and display process output.

# Assumptions
- A single main window is sufficient for the first version.

# Affected files or modules
- `pyproject.toml`
- `src/gui/`
- developer-facing docs

# Solution strategy
1. Add `PySide6` to dependencies.
2. Add a `src/gui/` package with:
   - a main window
   - input controls for mode, arch, and services
   - a live log panel
   - a subprocess/QProcess runner using `.venv/bin/python`
3. Add minimal docs for launching the GUI locally.
4. Verify imports, typing, and startup.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Run the GUI module to verify import/startup.
- Smoke check a generated command path visually or through a short run.
