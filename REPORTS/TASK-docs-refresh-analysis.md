# Problem statement
Developer-facing documentation no longer matches the current architecture and source tree, which makes it harder for a new developer to picture the system accurately.

# Confirmed facts
- `README.md` still describes `src/core/` as a flat utilities bucket.
- `docs/ARCHITECTURE.md` still references old module dependencies such as `src.core.shell` and older direct build/deploy coupling.
- `docs/REFACTORING_SUMMARY.md` describes an earlier architecture state and no longer reflects current orchestration boundaries.
- `brain/operations.md` still lists `uv run main.py` instead of the verified `uv run -m main` entrypoint.

# Assumptions
- The user wants documentation that helps a new developer understand the current architecture without reading the full codebase.

# Affected files or modules
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/REFACTORING_SUMMARY.md`
- `brain/operations.md`

# Solution strategy
- Refresh the README with current structure, flow, and entrypoints.
- Rewrite the architecture doc around the current domain/contracts/runtime separation.
- Replace stale refactoring summary content with a current boundary-oriented summary.
- Update the repo brain operations note to match verified entrypoints.

# Verification steps
- Check docs against current import paths and verified commands.
- Re-run the documented startup and CLI smoke commands where relevant.
