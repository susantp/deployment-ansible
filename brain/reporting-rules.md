# Reporting Rules

Persist non-trivial task artifacts in `REPORTS/`.

## Naming Convention
- `TASK-<issue-title>-analysis.md`
- `TASK-<issue-title>-plan.md`
- `TASK-<issue-title>-implementation.md`
- `TASK-<issue-title>-verification.md`

Use lowercase kebab-case for `<issue-title>` and keep the same issue title across reports for the same task.

## Required Sections
- Problem statement
- Confirmed facts
- Assumptions
- Affected files or modules
- Solution strategy
- Verification steps

## Rules
- Keep authoritative repo facts in `brain/`, not duplicated in every report.
- Reports should reference code paths and brain notes where useful.
- If scope changes materially, append an addendum or create a new report with a stable issue title plus a clear suffix.
