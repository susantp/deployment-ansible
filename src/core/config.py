"""Configuration loading utilities."""

import sys
from pathlib import Path
import yaml
from rich.console import Console

console = Console()


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
