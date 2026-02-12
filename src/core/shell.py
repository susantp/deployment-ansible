"""Shell command execution utilities."""
import os
import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()


def load_env(env_path: Path):
    """Load .env file manually into os.environ."""
    if not env_path.exists():
        console.print(f"[yellow]⚠️  Warning: .env file not found at {env_path}[/yellow]")
        return
    with env_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


def run(cmd: list[str], desc: str):
    """Run a shell command with clear feedback."""
    console.print(f"\n[bold cyan]▶️  {desc}[/bold cyan]")
    try:
        subprocess.run(cmd, check=True)
        console.print(f"[bold green]✅ {desc} completed.[/bold green]")
    except subprocess.CalledProcessError:
        console.print(f"[bold red]❌ {desc} failed.[/bold red]")
        sys.exit(1)


def print_header(title: str):
    """Print a styled header."""
    console.print(Panel(f"[bold white]{title}[/bold white]", border_style="blue", expand=False))
