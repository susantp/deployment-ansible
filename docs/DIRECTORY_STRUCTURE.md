# Directory Structure Refactoring

## New Modular Structure

```
bazarify-ansible/
├── src/                          # All source code
│   ├── __init__.py
│   ├── cli/                      # Command-line interface
│   │   ├── __init__.py
│   │   ├── parser.py            # CLI argument parsing
│   │   ├── menu.py              # Interactive menu logic
│   │   ├── ui.py                # Reusable UI components
│   │   └── executor.py          # Operation orchestration
│   ├── core/                     # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py            # YAML configuration loading
│   │   └── shell.py             # Shell command execution
│   ├── docker/                   # Docker operations
│   │   ├── __init__.py
│   │   └── builder.py           # Image building logic
│   └── deploy/                   # Deployment operations
│       ├── __init__.py
│       └── ansible.py           # Ansible deployment
├── config/                       # Configuration files
│   ├── services.yaml            # Service definitions
│   ├── inventory.ini            # Ansible inventory
│   └── pull-up-prune.yaml       # Ansible playbook
├── docs/                         # Detailed documentation
│   ├── ARCHITECTURE.md
│   ├── DIRECTORY_STRUCTURE.md
│   └── REFACTORING_SUMMARY.md
├── main.py                       # Application entry point
├── pyproject.toml               # Project dependencies
└── README.md                     # Documentation
```

## Module Responsibilities

### `src/cli/` - Command-Line Interface
**Purpose**: Handle all user interaction (CLI args, menus, UI)

- **`parser.py`**: Parse and validate command-line arguments
- **`menu.py`**: Interactive menu flows (presets, manual selection)
- **`ui.py`**: Reusable UI components (menus, prompts)
- **`executor.py`**: Orchestrate build/deploy operations

### `src/core/` - Core Utilities
**Purpose**: Shared utilities used across the application

- **`config.py`**: YAML configuration file loading
- **`shell.py`**: Shell command execution, env loading, UI helpers

### `src/docker/` - Docker Operations
**Purpose**: Docker image building and management

- **`builder.py`**: Build Docker images for different platforms

### `src/deploy/` - Deployment Operations
**Purpose**: Deploy applications to remote servers

- **`ansible.py`**: Ansible-based deployment orchestration

## Benefits of New Structure

### 1. **Clear Separation of Concerns**
- Each directory has a single, well-defined purpose
- No mixing of build, deploy, and CLI logic

### 2. **Logical Grouping**
- Related functionality is grouped together
- Easy to find what you're looking for

### 3. **Scalability**
- Easy to add new deployment methods (e.g., `src/deploy/kubernetes.py`)
- Easy to add new build systems (e.g., `src/docker/compose.py`)

### 4. **Testability**
- Each module can be tested independently
- Clear dependencies between modules

### 5. **Discoverability**
- New developers can quickly understand the structure
- Self-documenting directory names

## Migration from Old Structure

### Old Structure Issues
```
scripts/                    # ❌ Vague name, mixed concerns
├── utils.py               # ❌ Generic utilities
├── build_image.py         # ❌ Docker logic in "scripts"
└── ansible_deploy_remote.py  # ❌ Deployment in "scripts"

services/                   # ❌ Misleading name (not services)
├── cli.py                 # ❌ CLI logic in "services"
├── menu.py                # ❌ Menu logic in "services"
├── ui.py                  # ❌ UI in "services"
└── executor.py            # ❌ Executor in "services"
```

### New Structure Benefits
```
src/cli/                    # ✅ Clear: All CLI-related code
src/core/                   # ✅ Clear: Shared utilities
src/docker/                 # ✅ Clear: Docker operations
src/deploy/                 # ✅ Clear: Deployment operations
```

## Import Examples

### Before
```python
from scripts.utils import run, load_config
from services.menu import PRESETS
from services.executor import execute_operation
```

### After
```python
from src.core.shell import run
from src.core.config import get_services_config, PROJECT_ROOT
from src.cli.menu import PRESETS
from src.cli.executor import execute_operation
```

## Direct Module Execution

You can still run modules directly:

```bash
# Build images directly
uv run -m src.docker.builder amd nginx vendor

# Deploy images directly
uv run -m src.deploy.ansible techbizz/nginx:latest-amd

# Run main CLI
uv run main.py
```

## Future Extensions

The new structure makes it easy to add:

- `src/docker/compose.py` - Docker Compose support
- `src/deploy/kubernetes.py` - Kubernetes deployment
- `src/cli/config_wizard.py` - Interactive configuration wizard
- `src/core/logging.py` - Centralized logging
- `src/core/validation.py` - Input validation utilities
