# Problem statement
Add a first GUI version for the repository that collects user inputs visually but still relies on the existing non-interactive command flow for real execution.

# Confirmed facts
- The current tool is CLI-first, with verified non-interactive entrypoint `uv run -m main <mode> <arch> <service...>`.
- The local development environment includes a project virtualenv at `.venv/`.
- The codebase already centralizes canonical choices and orchestration flow, so a GUI wrapper can remain thin.

# Assumptions
- The first GUI version is a local-development/operator tool, not a packaged desktop distribution.
- The GUI should invoke the project venv interpreter directly rather than rely on shell activation.

# Affected files or modules
- `pyproject.toml`
- `src/gui/`
- `README.md`
- `docs/ARCHITECTURE.md`

# Solution strategy
- Add `PySide6` as a project dependency.
- Create a small GUI package that:
  - collects mode, arch, and service selections
  - runs `.venv/bin/python -m main <mode> <arch> <service...>`
  - streams stdout/stderr into a live log panel
- Keep the GUI as a wrapper only; do not reimplement orchestration logic.

# Verification steps
- Run `source .venv/bin/activate && ty check`.
- Launch the GUI module non-interactively enough to catch import/startup errors.
- Confirm the generated command targets the local `.venv` interpreter and existing CLI entrypoint.
