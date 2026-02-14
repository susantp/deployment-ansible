"""Configuration loading utilities."""

import sys
from pathlib import Path
from typing import Optional, Any
import yaml
from rich.console import Console

console = Console()

# Discovery of Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SERVICES_YAML = CONFIG_DIR / "services.yaml"

_cached_config: Optional[dict[str, Any]] = None


def load_config(config_path: Path) -> dict:
    """Load configuration from a YAML file."""
    if not config_path.exists():
        console.print(
            f"[bold red]❌ Configuration file not found at {config_path}[/bold red]"
        )
        sys.exit(1)

    with config_path.open() as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            console.print(f"[bold red]❌ Failed to parse YAML: {e}[/bold red]")
            sys.exit(1)


def get_services_config() -> dict[str, Any]:
    """Load and cache the services configuration."""
    global _cached_config
    if _cached_config is None:
        _cached_config = load_config(SERVICES_YAML)
    return _cached_config
