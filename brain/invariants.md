# Invariants

## Configuration Authority
- `PROJECT_ROOT / ".env"` is required at runtime and is loaded before normal execution.
- `config/services.yaml` is the canonical service registry.
- Service entries in `config/services.yaml` map service names to environment variable names, not directly to filesystem paths.
- Actual Docker build context paths come from environment variables such as `CONTEXT_VENDOR` and `CONTEXT_NGINX`.

## Image Naming
- Built and deployed images use the form `techbizz/<service>:latest-<arch>`.
- The deploy path assumes the same tag format produced by the build path.
- `arch` is user-facing shorthand (`amd`, `arm`), not the full Docker platform string.

## Architecture Mapping
- `amd -> linux/amd64/v2`
- `arm -> linux/arm64/v8`

## Deployment Contract
- Ansible inventory is expected at `config/inventory.ini`.
- The playbook is expected at `config/pull-up-prune.yaml`.
- Ansible host connection values are sourced from environment lookups in `config/group_vars/remote.yaml`.
- Deployment targets the `remote` host group and executes inside `DEPLOYMENT_DIRECTORY`.

## Remote Compose Assumptions
- The remote deployment directory already exists.
- The remote deployment directory already contains the compose project to refresh.
- Deploying images means pulling the specified tags, running `docker compose up -d`, optionally running Laravel migrations when `frankenphp` changed, and pruning unused Docker data.

## Fail-Fast Behavior
- Missing `.env`, missing config files, unknown services, unsupported architectures, or missing build contexts are treated as fatal and exit immediately.
- This repo prefers explicit operator feedback over recovery logic.
