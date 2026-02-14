# Bazarrify Deployment Tool

## Overview
This repository provides a modular orchestration layer for managing Docker builds and Ansible deployments. It simplifies the process of:
1. Building multi-architecture Docker images with `docker buildx`.
2. Deploying images to remote hosts via Ansible playbooks that pull images, refresh stacks with `docker compose`, and perform cleanup.

The tool features a rich interactive CLI, preset support, and direct module execution for CI/CD integration.

## Repository Layout
- `main.py` – CLI entry point; handles both interactive and argument-based execution.
- `src/cli/` – Command-line interface logic (argument parsing, interactive menus, UI components).
- `src/core/` – Core utilities for configuration loading and shell execution.
- `src/docker/` – Logic for building and pushing multi-arch Docker images.
- `src/deploy/` – Logic for triggering Ansible-based remote deployments.
- `config/` – Configuration files including service definitions (`services.yaml`), inventory, and playbooks.

## Requirements
### Local Workstation
- **Python 3.12+** – Managed via `uv` (recommended).
- **uv** – Modern Python package and project manager.
- **Docker** – With Buildx plugin and access to relevant registries.
- **Ansible** – Required for remote deployment tasks.
- **SSH Access** – Configured for target hosts in the inventory.

### Remote Targets
- **Docker Engine** and **Compose plugin**.
- Existing **deployment directory** containing the `docker-compose.yml` for the stack.

## Initial Setup

1. **Install dependencies** (using `uv`):
   ```sh
   uv sync
   ```

2. **Configure Services**:
   Edit `config/services.yaml` to define your services and their build contexts.

3. **Set up environment**:
   Copy the example environment file and fill in required paths:
   ```sh
   cp .env.example .env
   ```
   Provide values for `SSH_PRIVATE_KEY_FILE`, `DEPLOYMENT_DIRECTORY`, and service context paths.

4. **Prepare Ansible Inventory**:
   ```sh
   cp config/inventory.ini.template config/inventory.ini
   ```
   Update `config/inventory.ini` with your target host IPs/hostnames.

5. **Verify Connectivity**:
   ```sh
   ansible remote -i config/inventory.ini -m ping
   ```

## Usage

### Interactive CLI
Run the main orchestrator without arguments to enter the interactive menu:
```sh
uv run main.py
```
You can choose from defined **Presets** or use the **Manual** flow to select specific operations, architectures, and services.

### Command-Line Arguments
For non-interactive use or CI/CD:
```sh
uv run main.py <mode> <arch> <service...>
```
- `mode`: `build`, `deploy`, or `both`.
- `arch`: `amd` (linux/amd64) or `arm` (linux/arm64).
- `service...`: One or more services defined in `config/services.yaml`.

Example:
```sh
uv run main.py both amd vendor consumer
```

### Direct Module Execution
Modules can be executed directly for specific tasks:

**Building images:**
```sh
uv run -m src.docker.builder amd nginx vendor
```

**Deploying images:**
```sh
uv run -m src.deploy.ansible techbizz/nginx:latest-amd
```

## Troubleshooting
- **Buildx Errors**: Ensure `docker buildx ls` shows an active builder capable of the target platform.
- **Registry Failures**: Perform `docker login` for the namespace defined in your configuration.
- **Ansible Connection**: Verify the `SSH_PRIVATE_KEY_FILE` path in `.env` and that your public key is authorized on the remote host.
- **Missing Deploy Directory**: The tool expects the stack directory to exist on the remote host with a valid `docker-compose.yml`.

## Architecture & Refactoring
For more detailed information on the codebase structure and design decisions, please refer to:
- [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [DIRECTORY_STRUCTURE.md](docs/DIRECTORY_STRUCTURE.md)
- [REFACTORING_SUMMARY.md](docs/REFACTORING_SUMMARY.md)
