# Ansible Deployment

## Overview
This repository provides a thin orchestration layer around two repeatable tasks:
1. Build multi-architecture Docker images for services with `docker buildx`.
2. Deploy already-built images to one or more remote hosts via an Ansible playbook that pulls the images, runs `docker compose up`, and prunes unused artifacts.

Use the helper scripts in `run.py` to interactively build, deploy, or do both in sequence, or call the underlying modules directly when you need tighter control in CI.

## Repository layout
- `run.py` – CLI entry point; routes to the build or deploy helpers.
- `scripts/build_image.py` – builds (and for AMD pushes) Docker images for the services the platform supports.
- `scripts/ansible_deploy_remote.py` – loads project environment variables and runs `ansible-playbook` with the provided image list.
- `scripts/utils.py` – lightweight helpers for loading `.env` files and running commands with friendly logging.
- `config/` – inventory template, group variables, and the `pull-up-prune.yaml` playbook executed on remote hosts.

## Requirements
### Local workstation
- Python 3.10+ (only standard library modules are used).
- Docker with the Buildx plugin and logged-in access to the `techbizz` Docker Hub namespace.
- Ansible 2.12+ available on the PATH.
- SSH access to each remote host listed in the inventory.

### Remote targets
- Docker Engine and the Compose plugin installed and usable by the configured `ansible_user`.
- A directory that contains the `docker-compose.yml` file for the stack (referenced as `DEPLOYMENT_DIRECTORY`).
- Enough disk space for the pulled images and temporary build layers.

## Initial setup
1. **Copy the inventory template.**
   ```sh
   cp config/inventory.ini.template config/inventory.ini
   ```
   Replace `ansible_host` with the public IP or hostname of every target. Each host must belong to the `remote` group because the playbook is scoped to that group.

2. **Create/update `.env` in the repo root.** The helper scripts load it automatically. Provide at least:
   ```dotenv
   # Docker build contexts (absolute paths recommended)
   CONTEXT_NGINX=/path/to/nginx
   CONTEXT_CONSUMER=/path/to/consumer
   CONTEXT_VENDOR=/path/to/vendor
   CONTEXT_FRANKENPHP=/path/to/frankenphp
   CONTEXT_POSTGRES=/path/to/postgres
   CONTEXT_POSTGRES18=/path/to/postgres18

   # Values consumed by Ansible group vars
   SSH_PRIVATE_KEY_FILE=/Users/me/.ssh/id_rsa
   DEPLOYMENT_DIRECTORY=/opt/bazarify
   ```
   The `ansible_user` defaults to the current shell user through `lookup('env','USER')`. Override it per-host inside `config/inventory.ini` if needed.

3. **Verify Ansible connectivity.** Once the inventory and `.env` are in place, test the SSH hop:
   ```sh
   ansible remote -i config/inventory.ini -m ping
   ```

4. **Log in to Docker Hub.** Building AMD images triggers an automatic push + prune cycle, so `docker login` must succeed beforehand.

## Usage
### Quick orchestration via `run.py`
Run everything from one entry point:
```sh
python3 run.py <mode> <arch> <service...>
```
- `mode`: `build`, `deploy`, or `both` (build then deploy).
- `arch`: `amd` for `linux/amd64/v2`, `arm` for `linux/arm64/v8`.
- `service...`: one or more service keys from the context map (`nginx`, `consumer`, `vendor`, `frankenphp`, `postgres`, `postgres18`).

If you omit arguments, the script prompts for them interactively. Example full cycle:
```sh
python3 run.py both amd vendor consumer
```
This builds the two AMD images, pushes/removes the local tags, then deploys them sequentially.

### Building images directly
You can call the build helper without the wrapper:
```sh
python3 -m scripts.build_image amd vendor frankenphp
```
- The `.env` file defines the build context per service; blank values result in Docker using the repo root, so make sure paths are set.
- AMD builds push to Docker Hub and delete the local tag once the push succeeds to save disk space. ARM builds stay local.
- Add a new service by extending the `context_map` in `scripts/build_image.py` with the desired env var key.

### Deploying images directly
Deployment only needs the fully-qualified image references:
```sh
python3 -m scripts.ansible_deploy_remote techbizz/vendor:latest-amd techbizz/consumer:latest-amd
```
Under the hood this runs:
```sh
ansible-playbook -i config/inventory.ini config/pull-up-prune.yaml \
  --extra-vars '{"docker_images":["techbizz/vendor:latest-amd","techbizz/consumer:latest-amd"]}'
```
The playbook performs, per host:
1. `cd` into `DEPLOYMENT_DIRECTORY`.
2. `docker image pull` on every item in `docker_images`.
3. `docker compose up -d` to refresh the stack.
4. `docker system prune -f` for cleanup.

Ensure the remote directory already contains the compose file(s); this repo purposely does not ship application manifests.

## Troubleshooting
- **`docker buildx` errors** – confirm that Buildx is enabled (`docker buildx ls`) and that the platform string matches your builder instance. Enable the experimental CLI if required.
- **Authentication failures when pushing** – re-run `docker login` for the `techbizz` namespace or provide a `DOCKER_CONFIG` pointing to valid credentials.
- **`ansible-playbook` cannot connect** – double-check `ansible_host`, reachable SSH port, and that `SSH_PRIVATE_KEY_FILE` points to a key with access. Use `ANSIBLE_HOST_KEY_CHECKING=False` in the environment if you are still accepting fingerprints.
- **Compose command not found remotely** – install the Docker Compose plugin or alias `docker compose` appropriately on the hosts.
- **Missing deploy directory** – create `DEPLOYMENT_DIRECTORY` on every host and place the desired `docker-compose.yml` there; the playbook does not clone repos.

## Next steps
- Wire the scripts into CI/CD by invoking `python3 run.py build ...` on tagged releases and `python3 -m scripts.ansible_deploy_remote ...` from your release pipeline.
- Parameterize additional Ansible tasks (backups, health checks, etc.) by editing `config/pull-up-prune.yaml` or adding roles.
