# Operations

## Entrypoints
- `uv run main.py` starts the normal operator flow.
- `uv run main.py <mode> <arch> <service...>` runs non-interactively.
- `uv run -m src.docker.builder <arch> <service...>` runs build-only logic.
- `uv run -m src.deploy.ansible <image...>` runs deploy-only logic.

## Modes
- `build`: build selected services only
- `deploy`: deploy selected services only
- `both`: build first, then deploy matching tags

## Interactive Presets
- Presets currently exist only for remote `build` and remote `deploy` on `amd`.
- Presets still require the operator to choose one or more services dynamically.

## Current Service Registry
- `nginx`
- `redis`
- `consumer`
- `vendor`
- `frankenphp`
- `postgres`
- `pgbouncer`

## Build Behavior Details
- Each service build resolves a context path from `.env`.
- Context existence is verified before Docker runs.
- Only `amd` images are pushed and then removed locally.
- `arm` images are built locally but are not pushed by current logic.

## Deploy Behavior Details
- Deploy receives a list of fully qualified image tags.
- The playbook pulls each image individually on the remote host.
- `docker compose up -d` is run after pulls.
- Migrations run only when compose output suggests the `frankenphp` container was recreated.

## Operator Prerequisites
- Local machine needs Python 3.12+, `uv`, Docker with Buildx, Ansible, and SSH access.
- Remote machine needs Docker Engine, Compose plugin, and the target compose stack already present.
