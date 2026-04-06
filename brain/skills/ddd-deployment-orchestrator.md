# DDD Deployment Orchestrator Skill

Source inspiration:
- [NeoLabHQ context-engineering-kit ddd plugin](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/ddd)

Use this skill when working on:
- architecture or module boundaries
- refactoring for clarity
- naming and responsibility alignment
- code review focused on maintainability
- preventing orchestration code from absorbing infrastructure or product-domain logic

## Intent

Apply Clean Architecture, SOLID, and DDD thinking in a way that fits this repository.

This repo is a deployment orchestrator. Its domain is:
- service selection
- image tag construction
- build execution
- deploy execution
- configuration resolution

This repo does not own the business domain of the built services.

## Repo-Specific Rules

### 1. Keep the orchestration boundary thin
- `main.py` coordinates flow only.
- `src/cli/` handles input and selection.
- `src/core/` handles shared infrastructure helpers.
- `src/docker/` owns Docker build behavior.
- `src/deploy/` owns remote deployment behavior.
- Do not move service business rules from sibling repos into this repository.

### 2. Prefer direct contracts over clever abstractions
- Keep service naming, arch mapping, and image tag rules explicit.
- Add abstractions only when they remove repeated behavior across real use cases.
- For this repo size, extra indirection is usually worse than explicit code.

### 3. Preserve configuration authority
- `.env` remains runtime authority for environment-specific values.
- `config/services.yaml` remains the canonical service registry.
- Do not scatter path or host authority across multiple new files unless the task explicitly restructures config ownership.

### 4. Use domain-specific naming
- Name functions by operator intent such as `build_service`, `deploy_images`, `execute_operation`.
- Avoid vague helpers that mix concerns under generic names like `process`, `handle_data`, or `run_task`.

### 5. Keep side effects at the edges
- Parsing, mapping, and selection logic should stay separate from shell execution.
- Validation should happen before expensive Docker or Ansible actions.
- Shell calls, Docker calls, and Ansible calls are boundary effects and should stay easy to trace.

### 6. Maintain fail-fast behavior
- Missing env, invalid service names, unsupported architectures, and missing files should stop early with clear operator feedback.
- Do not replace explicit exits with silent fallback behavior unless the task explicitly changes operator experience.

### 7. Review heuristics
- Reject coupling that makes deploy logic depend on CLI presentation details.
- Reject coupling that makes build logic depend on Ansible-specific assumptions unless that contract is intentionally shared.
- Reject changes that make this repo the owner of application runtime rules from `vendor`, `consumer`, `frankenphp`, or other sibling services.
- Prefer simple data flow: input -> validate -> map -> execute.

## How To Apply It

For a non-trivial task:
1. Read `brain/invariants.md` and `brain/operations.md`.
2. Identify which module owns the change.
3. Check whether the proposed change introduces a new abstraction or justifies an existing one.
4. Keep side effects localized and contracts explicit.
5. If architecture or operating expectations changed, update the relevant `brain/` note.

## Notes On The External Plugin

The upstream plugin describes a broad DDD and code-quality framework with persistent rules and contextual commands, including setup of formatting guidance and automatic rule activation. This local skill is a distilled adaptation for `bazzarify-ansible`, not a full mirror of that plugin.
