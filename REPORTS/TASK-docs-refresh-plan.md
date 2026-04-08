# Problem statement
Bring the repository documentation in line with the current codebase so onboarding and maintenance are easier.

# Confirmed facts
- The code structure changed materially, but several docs still describe the earlier flat-core architecture.
- Current runtime verification already established the valid entrypoints and flow.

# Assumptions
- Rewriting outdated docs is preferable to trying to patch them incrementally.

# Affected files or modules
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/REFACTORING_SUMMARY.md`
- `brain/operations.md`

# Solution strategy
1. Update `README.md` with current layout, architecture concepts, and verified usage commands.
2. Rewrite `docs/ARCHITECTURE.md` to show the current dependency direction and data flow.
3. Refresh `docs/REFACTORING_SUMMARY.md` so it summarizes the current architecture rather than historical intermediate states.
4. Update `brain/operations.md` to reflect the verified entrypoints.

# Verification steps
- Compare doc references to the current source tree.
- Reuse the verified `uv run -m main` and `uv run -m main build amd nginx` commands as documented behavior checks.
