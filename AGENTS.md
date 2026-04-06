# Agent Bootstrap

This repository is the deployment orchestration workspace for Bazarify service builds and remote rollouts. Use the local `brain/` directory as the durable source of repo-specific knowledge. Extend the brain in place. Do not create parallel memory systems.

## Required Read Order
1. `brain/README.md`
2. `brain/repo-purpose.md`
3. `brain/invariants.md`
4. `brain/operations.md`
5. `brain/skill-registry.md`
6. `brain/workflow.md`
7. `brain/reporting-rules.md`

## Operating Rules
- Treat `brain/` as the local memory authority for stable repo facts and workflow expectations.
- Prefer updating an existing focused brain note over creating duplicate summary files.
- Keep persisted task artifacts in `REPORTS/` only.
- For non-trivial work, persist analysis, plan, implementation, and verification reports before closing the task.
- Ground plans in inspected repository facts from code, config, docs, and current brain notes.
- Preserve the current deployment contract unless the task explicitly changes it:
  - `.env` is required runtime configuration
  - `config/services.yaml` maps service names to env var keys
  - images use `techbizz/<service>:latest-<arch>`
  - Ansible deploys through `config/inventory.ini` and `config/pull-up-prune.yaml`
- Do not create tool-specific planning or scratch directories such as `.cursor/`, `.ai/`, `.tmp/`, or alternate `memory/` trees.
- When behavior or operational expectations change, update the corresponding file in `brain/`.
- When a task is about architecture, refactoring, maintainability, or boundary discipline, apply the relevant repo-local skill from `brain/skills/`.
- When a task changes build or deploy behavior, apply the `safe-deployment-changes` skill and verify contract alignment across build, deploy, config, docs, and brain notes.

## Bootstrap Intent
- `brain/repo-purpose.md` explains what this repository owns.
- `brain/invariants.md` captures the contracts agents must not drift from accidentally.
- `brain/operations.md` captures actual operator entrypoints and behavior.
- `brain/skill-registry.md` lists reusable repo-local skills.
- `brain/workflow.md` defines the per-task lifecycle for persisted reporting.
- `brain/reporting-rules.md` defines report naming and content expectations.
