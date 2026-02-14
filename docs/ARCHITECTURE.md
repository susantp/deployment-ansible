# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    (Entry Point / Orchestrator)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─────────────────┬──────────────┐
                              ▼                 ▼              ▼
                    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
                    │   src/cli/   │  │  src/core/   │  │ src/docker/  │
                    │              │  │              │  │              │
                    │ • parser.py  │  │ • config.py  │  │ • builder.py │
                    │ • menu.py    │  │ • shell.py   │  │              │
                    │ • ui.py      │  │              │  └──────────────┘
                    │ • executor.py│  └──────────────┘         │
                    └──────────────┘         │                 │
                            │                │                 │
                            │                ▼                 │
                            │      ┌──────────────┐            │
                            │      │ config/      │            │
                            │      │              │            │
                            │      │ • services.  │            │
                            │      │   yaml       │            │
                            │      └──────────────┘            │
                            │                                  │
                            └──────────────┬───────────────────┘
                                          ▼
                                ┌──────────────┐
                                │ src/deploy/  │
                                │              │
                                │ • ansible.py │
                                └──────────────┘
```

## Module Dependencies

```
main.py
  ├─> src.cli.parser (parse CLI args)
  ├─> src.cli.menu (interactive menus)
  │     ├─> src.cli.ui (UI components)
  │     ├─> src.core.config (load services.yaml)
  │     └─> src.core.shell (print headers, console)
  └─> src.cli.executor (orchestrate operations)
        ├─> src.docker.builder (build images)
        │     ├─> src.core.config (load services.yaml)
        │     └─> src.core.shell (run commands, load env)
        └─> src.deploy.ansible (deploy images)
              └─> src.core.shell (run commands, load env)
```

## Data Flow

### Interactive Mode
```
User Input
    │
    ▼
┌─────────────────┐
│  main.py        │
│  (entry point)  │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  cli/menu.py    │
│  (show menu)    │
└─────────────────┘
    │
    ├─> Preset Selected ──────┐
    │                         │
    └─> Manual Selected       │
            │                 │
            ▼                 ▼
    ┌──────────────┐  ┌──────────────┐
    │ select_      │  │ handle_      │
    │ operation()  │  │ preset_flow()│
    │ select_      │  │              │
    │ platform()   │  │              │
    │ select_      │  │              │
    │ services()   │  │              │
    └──────────────┘  └──────────────┘
            │                 │
            └────────┬────────┘
                     ▼
            ┌──────────────┐
            │ cli/         │
            │ executor.py  │
            └──────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Build        Deploy       Both
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ docker/  │  │ deploy/  │  │ Both     │
│ builder  │  │ ansible  │  │ modules  │
└──────────┘  └──────────┘  └──────────┘
```

### CLI Mode
```
Command Line Args
    │
    ▼
┌─────────────────┐
│  main.py        │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  cli/parser.py  │
│  (parse args)   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│  cli/           │
│  executor.py    │
└─────────────────┘
    │
    ▼
(same as interactive)
```

## Configuration Philosophy

### Single Source of Truth
The tool uses the `.env` file as the single source of truth for all environment-specific variables. This ensures that both the Python orchestration layer and the Ansible deployment layer share the same configuration.

### Implementation Pattern
1. **`.env`**: Contains all secrets, paths, and connection details (e.g., `REMOTE_HOST`, `SSH_PRIVATE_KEY_FILE`).
2. **`config/group_vars/remote.yaml`**: Bridges the environment variables to Ansible using lookups:
   ```yaml
   ansible_host: "{{ lookup('env', 'REMOTE_HOST') }}"
   ansible_user: "{{ lookup('env', 'USER') }}"
   ```
3. **`config/inventory.ini`**: Contains only the logical grouping and nicknames for hosts, keeping infrastructure definition separate from connection details.

## Responsibility Matrix

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `main.py` | Entry point, orchestration | cli.parser, cli.menu, cli.executor |
| `cli/parser.py` | Parse CLI arguments | core.shell |
| `cli/menu.py` | Interactive menus | cli.ui, core.config, core.shell |
| `cli/ui.py` | Reusable UI components | core.shell |
| `cli/executor.py` | Orchestrate operations | docker.builder, deploy.ansible |
| `core/config.py` | Load YAML config | - |
| `core/shell.py` | Execute shell commands | - |
| `docker/builder.py` | Build Docker images | core.config, core.shell |
| `deploy/ansible.py` | Deploy via Ansible | core.shell |

## Extension Points

### Adding New Deployment Method
```python
# src/deploy/kubernetes.py
def deploy_to_k8s(images: list[str]):
    """Deploy to Kubernetes cluster."""
    pass

# Update src/cli/executor.py
from src.deploy.kubernetes import deploy_to_k8s

def execute_deploy(arch: str, services: list[str], method: str = "ansible"):
    if method == "kubernetes":
        deploy_to_k8s(images)
    else:
        deploy_images(images)
```

### Adding New Build System
```python
# src/docker/compose.py
def build_with_compose(service: str):
    """Build using docker-compose."""
    pass

# Update src/cli/executor.py
from src.docker.compose import build_with_compose

def execute_build(arch: str, services: list[str], method: str = "buildx"):
    if method == "compose":
        build_with_compose(service)
    else:
        build_service(service, arch)
```

### Adding Configuration Wizard
```python
# src/cli/wizard.py
def run_config_wizard():
    """Interactive configuration wizard."""
    pass

# Update main.py
from src.cli.wizard import run_config_wizard

if "--wizard" in sys.argv:
    run_config_wizard()
```

## Testing Strategy

### Unit Tests
```
tests/
├── test_cli/
│   ├── test_parser.py
│   ├── test_menu.py
│   └── test_ui.py
├── test_core/
│   ├── test_config.py
│   └── test_shell.py
├── test_docker/
│   └── test_builder.py
└── test_deploy/
    └── test_ansible.py
```

### Integration Tests
```
tests/integration/
├── test_build_flow.py
├── test_deploy_flow.py
└── test_full_workflow.py
```

## Performance Considerations

- **Lazy imports**: Import modules only when needed
- **Config caching**: Load config once, reuse
- **Parallel builds**: Can build multiple services in parallel
- **Async operations**: Future enhancement for concurrent deploys
