# Problem statement
Refresh the developer-facing documentation so it accurately describes the current architecture, directory structure, and verified entrypoints.

# Confirmed facts
- The codebase now uses domain/contracts/runtime boundaries under `src/core/`.
- Interactive and CLI flows share canonical choice definitions.
- Verified entrypoints use `uv run -m main`.

# Assumptions
- New developers benefit more from current conceptual docs than from preserving historical wording.

# Affected files or modules
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/REFACTORING_SUMMARY.md`
- `brain/operations.md`

# Solution strategy
- Rewrote `README.md` around current ownership, runtime contracts, layout, and reading order.
- Rewrote `docs/ARCHITECTURE.md` around current layering and dependency direction.
- Replaced the stale refactoring summary with a current architecture-oriented summary.
- Updated `brain/operations.md` entrypoints to match verified commands.

# Verification steps
- Compared the new docs against the current tree and runtime behavior.
- Reused the verified startup command as the documentation reference.
