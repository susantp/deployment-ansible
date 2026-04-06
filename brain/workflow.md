# Task Workflow

All non-trivial work in this repository should follow this lifecycle.

## 1. Intake
- Identify the user request and the repo areas in scope.
- Read the required bootstrap files from `AGENTS.md`.
- Check whether the task changes stable behavior, operational contracts, or only local implementation details.

## 2. Analysis
- Inspect code, config, docs, and existing brain notes before proposing changes.
- Confirm the current contract from source files, not assumptions.
- Persist an analysis report in `REPORTS/` when the task is non-trivial or the user wants a durable record.

## 3. Planning
- Create an implementation plan after analysis, not before.
- Keep the plan tied to actual affected modules and verification steps.
- Persist the plan in `REPORTS/` for non-trivial work.

## 4. Implementation
- Apply the smallest durable change that satisfies the plan.
- Do not create parallel configuration or memory systems.
- If the task changes stable repo behavior, update the relevant `brain/` note in the same slice.

## 5. Verification
- Run checks that match the changed surface area.
- Verify behavior and operational assumptions, not just syntax.
- Persist a verification report in `REPORTS/` for non-trivial work.

## 6. Closeout
- If useful, persist an implementation report summarizing what changed.
- Remove temporary artifacts that were created only for the task.
- Leave `brain/` and `REPORTS/` coherent for the next agent.

## Default Reporting Expectation
- Discussion-heavy or non-trivial tasks should produce:
  - analysis
  - plan
  - implementation
  - verification
- Small one-line or obvious edits do not need forced paperwork unless the user asks for it.
