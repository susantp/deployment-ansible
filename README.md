# Bazarrify Deployment Tool

## Overview
`bazzarify-ansible` is a Python orchestration CLI for two linked workflows:
- build Docker images for Bazarify services
- deploy selected images to a remote host through Ansible

This repository is not the source repo for those services. It is the thin orchestration layer that turns service selections plus target architecture into canonical image tags and optional remote rollout.

## What This Repo Owns
- interactive and non-interactive operator flows
- service selection and mode selection
- canonical image-tag planning
- Docker build execution
- Ansible deployment execution

## What This Repo Does Not Own
- business logic for `vendor`, `consumer`, `frankenphp`, `nginx`, or other services
- server provisioning
- remote compose project authoring

## Current Architecture

### High-level flow
1. `main.py` selects interactive or CLI mode.
2. `src/cli/` resolves canonical inputs such as `build`, `deploy`, `both`, `amd`, and selected services.
3. `src/core/domain/` plans requests and owns shared policy.
4. `src/cli/executor.py` coordinates operations.
5. `src/docker/` and `src/deploy/` act as infrastructure adapters that execute the planned requests.

### Repository layout
- `main.py`: entrypoint
- `src/cli/`: menus, CLI parsing, UI helpers, operation execution
- `src/core/config.py`: config authority
- `src/core/domain/`: domain choices, policy, orchestration request planning
- `src/core/contracts/`: ports/contracts used by orchestration and adapters
- `src/core/runtime/`: runtime shell helpers and concrete dependency wiring
- `src/docker/`: Docker build adapter
- `src/deploy/`: Ansible deploy adapter
- `config/`: service registry, inventory, playbook, group vars
- `brain/`: durable repo memory and workflow rules
- `REPORTS/`: persisted task artifacts

## Runtime Contracts
- `.env` is required at runtime
- `config/services.yaml` is the canonical service registry
- built and deployed images use `techbizz/<service>:latest-<arch>`
- supported architectures:
  - `amd -> linux/amd64/v2`
  - `arm -> linux/arm64/v8`
- Ansible deploys through:
  - `config/inventory.ini`
  - `config/pull-up-prune.yaml`

## Requirements

### Local workstation
- Python `3.14+`
- `uv`
- Docker with Buildx
- Ansible
- SSH access to the target host

### Remote target
- Docker Engine
- Docker Compose plugin
- existing deployment directory containing the compose project

## Setup
1. Install dependencies:
```sh
uv sync
```

2. Create runtime config:
```sh
cp .env.example .env
```

3. Set the required environment values in `.env`, including:
- service build context env vars referenced by `config/services.yaml`
- SSH/private key settings
- `DEPLOYMENT_DIRECTORY`

4. Prepare inventory:
```sh
cp config/inventory.ini.template config/inventory.ini
```

5. Verify Ansible connectivity:
```sh
ansible remote -i config/inventory.ini -m ping
```

## Usage

### Interactive mode
```sh
uv run -m main
```

### Non-interactive mode
```sh
uv run -m main <mode> <arch> <service...>
```

Examples:
```sh
uv run -m main build amd vendor
uv run -m main both amd vendor consumer
```

### Direct module execution
Build only:
```sh
uv run -m src.docker.builder amd nginx vendor
```

Deploy only:
```sh
uv run -m src.deploy.ansible techbizz/nginx:latest-amd
```

## How To Read The Codebase
If you are new to the repo, this order is usually fastest:
1. `README.md`
2. `brain/repo-purpose.md`
3. `brain/invariants.md`
4. `docs/ARCHITECTURE.md`
5. `docs/DIRECTORY_STRUCTURE.md`

Then inspect:
- `main.py`
- `src/cli/`
- `src/core/domain/`
- `src/core/runtime/`

## Troubleshooting
- Build context errors usually mean `.env` does not define the context path expected by `config/services.yaml`.
- Deploy errors often mean `config/inventory.ini`, remote SSH access, or `.env` connection values are incomplete.
- Interactive startup will fail with `EOFError` only in non-interactive environments where no stdin is available.

## Further Reading
- [Architecture](docs/ARCHITECTURE.md)
- [Directory Structure](docs/DIRECTORY_STRUCTURE.md)
- [Refactoring Summary](docs/REFACTORING_SUMMARY.md)
