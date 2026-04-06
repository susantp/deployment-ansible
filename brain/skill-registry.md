# Skill Registry

This file lists repo-local reusable skills stored under `brain/skills/`.

## Available Skills
- `ddd-deployment-orchestrator`
  - Path: `brain/skills/ddd-deployment-orchestrator.md`
  - Use when the task is about architecture, refactoring, boundaries, naming, code quality, or preventing orchestration logic from drifting into the wrong module.
- `safe-deployment-changes`
  - Path: `brain/skills/safe-deployment-changes.md`
  - Use when the task changes Docker build behavior, image tagging, Ansible deploy flow, remote execution assumptions, configuration contracts, or operator-facing rollout semantics.

## Rules
- Skills in `brain/skills/` are repo-local guidance, not external package installs.
- Distill external frameworks into repo-relevant operating rules instead of copying large third-party plugin trees verbatim.
- If a skill changes stable expectations, update this registry and the skill file together.
