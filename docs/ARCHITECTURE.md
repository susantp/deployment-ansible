# Architecture Overview

## Intent
This repository is a deployment orchestrator. Its domain is:
- selecting services
- selecting operation mode
- selecting target architecture
- planning image tags
- executing Docker builds
- executing Ansible deploys

It does not own the application business domain of the services it builds.

## Current Layering

```text
main.py
  -> src/cli/
      -> src/core/domain/
      -> src/cli/executor.py
          -> src/core/runtime/services.py
              -> src/docker/
              -> src/deploy/
              -> src/core/runtime/shell.py
```

## Source Tree By Role

### Entrypoint
- `main.py`
  - chooses interactive or CLI mode
  - loads `.env`
  - delegates execution

### CLI
- `src/cli/parser.py`
  - parses CLI commands into canonical values
- `src/cli/menu.py`
  - handles interactive presets and manual selection
- `src/cli/ui.py`
  - reusable prompt/menu rendering
- `src/cli/executor.py`
  - coordinates build and deploy execution from planned requests

### GUI
- `src/gui/app.py`
  - collects user selections visually
  - launches the existing non-interactive command path
  - streams live stdout/stderr into the GUI

### Core Domain
- `src/core/domain/choices.py`
  - canonical operation and platform choices
- `src/core/domain/policies.py`
  - image-tag and architecture policy
- `src/core/domain/orchestration.py`
  - `BuildRequest`
  - `DeployRequest`
  - pure planner functions

### Core Contracts
- `src/core/contracts/ports.py`
  - narrow callable ports for build, deploy, and command running

### Core Runtime
- `src/core/runtime/services.py`
  - concrete dependency wiring
- `src/core/runtime/shell.py`
  - environment loading
  - fail-fast output/exit helpers
  - command execution

### Config Authority
- `src/core/config.py`
  - `PROJECT_ROOT`
  - `config/services.yaml` loading/caching

### Infrastructure Adapters
- `src/docker/builder.py`
  - executes `BuildRequest`
- `src/deploy/ansible.py`
  - executes `DeployRequest`

## Dependency Direction

The intended direction is:

```text
CLI / orchestration
  depends on
domain planning + contracts + runtime wiring
  which delegate to
infrastructure adapters
  which use
runtime shell execution
```

Important point:
- high-level orchestration should not need to know subprocess details
- infrastructure adapters should not own orchestration planning policy

## Planning vs Execution

### Planning
Planning is pure and lives in `src/core/domain/orchestration.py`.

Examples:
- turn `arch + services` into `BuildRequest` values
- turn `arch + services` into canonical deploy image tags

### Execution
Execution is adapter work:
- Docker adapter consumes a `BuildRequest`
- Ansible adapter consumes a `DeployRequest`
- command execution is delegated to the runtime runner

## Input Model

There are two input surfaces:
- interactive mode
- CLI mode
- GUI wrapper mode

They now share the same canonical choice registry in `src/core/domain/choices.py`.

That means:
- interactive menu numbers are UI-only
- CLI strings remain canonical values
- both resolve through one source of truth

## Runtime Contracts

### Required config
- `.env`
- `config/services.yaml`
- `config/pull-up-prune.yaml`
- `config/inventory.ini`

### Image naming
- `techbizz/<service>:latest-<arch>`

### Supported architectures
- `amd -> linux/amd64/v2`
- `arm -> linux/arm64/v8`

### Deploy contract
- deploy receives fully qualified image tags
- playbook pulls each image
- remote host refreshes compose stack

## Fail-Fast Philosophy

The repo intentionally fails early for:
- missing `.env`
- missing config files
- unknown services
- unsupported architectures
- missing build contexts

The goal is explicit operator feedback rather than recovery logic.

## Practical Reading Order
For a new developer:
1. `main.py`
2. `src/cli/parser.py`
3. `src/cli/menu.py`
4. `src/cli/executor.py`
5. `src/core/domain/`
6. `src/core/runtime/services.py`
7. `src/docker/builder.py`
8. `src/deploy/ansible.py`
