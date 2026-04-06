# Safe Deployment Changes Skill

Use this skill when a task touches:
- `src/docker/`
- `src/deploy/`
- `src/cli/executor.py`
- `config/services.yaml`
- `config/group_vars/remote.yaml`
- `config/pull-up-prune.yaml`
- `.env.example`
- any change to image tags, architecture handling, push behavior, or remote rollout assumptions

## Intent

Deployment code can fail late and expensively. This skill forces explicit contract checks before changing rollout behavior.

## Change Categories That Require Extra Care

### 1. Image Contract Changes
- image naming
- tag suffix conventions
- architecture mapping
- push and cleanup behavior

### 2. Build Contract Changes
- Docker build command structure
- build context resolution
- supported services
- supported architectures

### 3. Deploy Contract Changes
- Ansible inventory expectations
- env-to-Ansible variable bridging
- remote compose execution behavior
- migration triggers
- prune behavior

### 4. Operator Contract Changes
- CLI arguments
- preset behavior
- mode semantics
- required env variables

## Required Review Questions

Before implementation, answer:
- What exact contract is changing?
- Which module is the authority for that contract?
- Will the change break existing image names or deployment commands?
- Does the change require matching updates in docs, `.env.example`, or brain notes?
- What verification can prove the change without relying on assumption alone?

## Mandatory Verification Thinking

For affected tasks, verify at the right level:

### Code-level
- syntax or import validity
- control-flow correctness
- unchanged responsibilities between modules

### Contract-level
- image tags built by `src/docker/builder.py` still match what `src/cli/executor.py` deploys
- required env variables still line up with `config/services.yaml` and `.env.example`
- Ansible file paths and variable names remain aligned

### Operational-level
- local entrypoints still make sense for operators
- remote assumptions are still explicit
- fail-fast behavior still happens before expensive actions

## Default Verification Checklist

When relevant, check:
- `uv run main.py ...` argument flow still maps correctly
- service names in `config/services.yaml` still correspond to env variables
- deploy image list still matches build image list
- Ansible inventory/playbook references are unchanged or intentionally updated
- docs and `brain/` notes reflect the new contract

## Rules

- Do not change deployment behavior silently.
- Do not change image tags in one place only.
- Do not add new required env vars without updating `.env.example` and the relevant docs or brain notes.
- Do not relax fail-fast validation unless the task explicitly changes operator UX and the new behavior is documented.
- Prefer explicit operator-visible messages over hidden fallback logic.

## Report Expectations

For non-trivial deployment-contract changes, the reports in `REPORTS/` should explicitly capture:
- previous contract
- new contract
- affected files
- operational risks
- verification performed
